"""Frozen input encoding and shared model loading."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
import torch
import yaml
from tokenizers import Tokenizer, models as token_models, pre_tokenizers, processors
from transformers import PreTrainedTokenizerFast, RobertaConfig, RobertaForTokenClassification
from transformers.modeling_outputs import TokenClassifierOutput

from pylingual import models
from pylingual.decompiler import Decompiler
from pylingual.masking.model_disasm import encode_opcodes
from pylingual.segmentation.segmentation_search_strategies import filter_subwords


@pytest.fixture
def tokenizer():
    tokens = ["[PAD]", "[CLS]", "[SEP]", "[UNK]", "[MASK]", "LOAD_CONST", "<mask_0>", "None", "<SEP>", "<opcode:LOAD_CONST>", "<opcode:RETURN_VALUE>", "<future_opcode_00>"]
    backend = Tokenizer(token_models.WordLevel({token: i for i, token in enumerate(tokens)}, unk_token="[UNK]"))
    backend.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    backend.post_processor = processors.TemplateProcessing(single="[CLS] $A [SEP]", special_tokens=[("[CLS]", 1), ("[SEP]", 2)])
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, pad_token="[PAD]", cls_token="[CLS]", sep_token="[SEP]", unk_token="[UNK]", mask_token="[MASK]")
    tokenizer.add_special_tokens({"additional_special_tokens": ["None", "<mask_0>"]})
    return tokenizer


class TranslationModel(torch.nn.Module):
    def __init__(self, tokenizer):
        super().__init__()
        self.embedding = torch.nn.Embedding(len(tokenizer), 1)
        self.generation_config = SimpleNamespace(bad_words_ids=[[9], [10], [11]])

    def get_input_embeddings(self):
        return self.embedding

    def generate(self, **kwargs):
        self.input_ids = kwargs["input_ids"]
        return torch.tensor([[0, 1, 7, 6, 9, 11, 2]] * len(self.input_ids))


def test_encoding_changes_only_opcode_fields():
    assert encode_opcodes("E-> ^~> TARGET_1 LOAD_CONST LOAD_CONST <mask_0> <SEP> RETURN_VALUE") == "E-> ^~> TARGET_1 <opcode:LOAD_CONST> LOAD_CONST <mask_0> <SEP> <opcode:RETURN_VALUE>"


@pytest.mark.parametrize("prefix", ["", "E-> ^~> TARGET_1 "])
def test_segmentation_selects_first_token_per_instruction(tokenizer, prefix):
    text = encode_opcodes(prefix + "LOAD_CONST LOAD_CONST <SEP> RETURN_VALUE")
    offsets = tokenizer(text, return_offsets_mapping=True)["offset_mapping"]
    predictions = [{"start": start, "end": end, "entity": "I", "score": 1.0} for start, end in offsets if start != end]
    predictions[0]["entity"], predictions[-1]["entity"] = "B", "E"
    assert [row["entity"] for row in filter_subwords(predictions, text)] == ["B", "E"]
    with pytest.raises(ValueError, match="instruction"):
        filter_subwords(predictions[:-1], text)


def test_segmentation_empty_code_object_has_no_boundaries():
    assert filter_subwords([], "") == []


@pytest.mark.parametrize("requests", [[""], ["", "LOAD_CONST None <SEP> RETURN_VALUE", "", "RETURN_VALUE", ""]])
def test_segmentation_preserves_empty_code_object_positions(tokenizer, requests):
    def predictions(texts, **kwargs):
        return [[{"start": start, "end": end, "entity": "I", "score": 1.0} for start, end in tokenizer(text, return_offsets_mapping=True)["offset_mapping"] if start != end] for text in texts]

    decompiler = Decompiler.__new__(Decompiler)
    decompiler.name = "empty-code-object-regression"
    decompiler.trust_lnotab = False
    decompiler.segmentation_requests = requests
    decompiler.segmenter = Mock(tokenizer=tokenizer, side_effect=predictions)
    decompiler.check_timeout = Mock()
    decompiler.update_starts_line = Mock()
    decompiler.run_segmentation()
    assert [len(result) for result in decompiler.segmentation_results] == [len(text.split(" <SEP> ")) if text else 0 for text in requests]
    assert all(not result or result[0]["entity"] == "B" for result in decompiler.segmentation_results)
    decompiler.update_starts_line.assert_called_once_with()


def test_translation_preserves_source_masks_and_uses_frozen_generation_settings(tokenizer):
    model = TranslationModel(tokenizer)
    translator = models.CacheTranslator(model, tokenizer, cache_namespace="statement@revision")
    assert translator._translate_and_decode(["LOAD_CONST LOAD_CONST"]) == ["None <mask_0>"]
    assert tokenizer.decode(model.input_ids[0], skip_special_tokens=False) == "[CLS] <opcode:LOAD_CONST> LOAD_CONST [SEP]"
    assert model.generation_config.bad_words_ids == [[9], [10], [11]]


def test_flat_configuration_pins_one_model_pair():
    config = yaml.safe_load((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    assert config == {
        "SEGMENTATION_MODEL": {"REPO": "syssec-utd/pylingual-shared-segmentation-v3", "REVISION": "37cfee8f8e7bc16c4050056ffcdead83f714c7cf"},
        "STATEMENT_MODEL": {"REPO": "syssec-utd/pylingual-shared-statement-v3", "REVISION": "a20bc4d28fe8641df0f90aa3665431368930c329"},
        "TOKENIZER": {"REPO": "syssec-utd/pylingual-shared-tokenizer-v1", "REVISION": "d23233a4bb237dcc3b1660e46a42f9189eaf0f6c"},
    }


def test_segmentation_preserves_reference_torch_confidence(tokenizer, tmp_path):
    config_file = tmp_path / "models.yaml"
    config_file.write_text((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    config = RobertaConfig(vocab_size=len(tokenizer), hidden_size=8, num_hidden_layers=1, num_attention_heads=2, intermediate_size=16, num_labels=3, id2label={0: "B", 1: "I", 2: "E"})
    model = RobertaForTokenClassification(config)
    # NumPy softmax rounds this confidence differently from Torch. The correction
    # search ranks these scores, so preserving only the winning label is not enough.
    logits = torch.tensor([-4.756705284118652, 7.19916296005249, 8.583805084228516])
    expected = float(logits.softmax(-1).max())
    model.forward = lambda input_ids, **kwargs: TokenClassifierOutput(logits=logits.expand(*input_ids.shape, 3))
    with (
        patch.object(models.transformers.AutoModelForTokenClassification, "from_pretrained", return_value=model),
        patch.object(models.transformers.T5ForConditionalGeneration, "from_pretrained", return_value=TranslationModel(tokenizer)),
        patch.object(models.transformers.PreTrainedTokenizerFast, "from_pretrained", return_value=tokenizer),
    ):
        segmenter, _ = models.load_models.__wrapped__(config_file, device=torch.device("cpu"))
    for predictions in segmenter(["LOAD_CONST None", "RETURN_VALUE"], batch_size=2):
        assert predictions
        assert all(row["entity"] == "E" for row in predictions)
        assert all(float(row["score"]) == expected for row in predictions)
    assert segmenter([]) == []
    assert segmenter("") == []
    assert [bool(row) for row in segmenter(["", "RETURN_VALUE", ""], batch_size=1)] == [False, True, False]
    with pytest.raises(ValueError, match="batch size"):
        segmenter(["RETURN_VALUE"], batch_size=0)
    assert not segmenter.model.training


def test_loading_reuses_segmentation_model_and_translation_cache(tokenizer, tmp_path):
    path = tmp_path / "models.yaml"
    path.write_text((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    segmentation, translation = TranslationModel(tokenizer), TranslationModel(tokenizer)
    with (
        patch.object(models.transformers.AutoModelForTokenClassification, "from_pretrained", return_value=segmentation) as seg_load,
        patch.object(models.transformers.T5ForConditionalGeneration, "from_pretrained", return_value=translation) as stmt_load,
        patch.object(models.transformers.PreTrainedTokenizerFast, "from_pretrained", return_value=tokenizer) as tokenizer_load,
        patch.object(models, "_free_device_memory"),
        patch.object(models.redis, "StrictRedis", return_value=Mock()),
    ):
        first = models.load_models(path, redis_cache_server_ip="localhost", device=torch.device("cpu"))
        last = models.load_models(path, redis_cache_server_ip="localhost", device=torch.device("cpu"))
    assert first[0] is last[0] and first[0].model is segmentation
    assert isinstance(first[0], models.OpcodeSegmenter)
    assert first[1] is last[1] and first[1].model is translation
    assert seg_load.call_count == stmt_load.call_count == 1
    assert tokenizer_load.call_count == 2
    assert {call.kwargs["subfolder"] for call in tokenizer_load.call_args_list} == {"statement", "segmentation"}
    assert first[1].redis_namespace_prefix.startswith("syssec-utd/pylingual-shared-statement-v3@a20bc4")
