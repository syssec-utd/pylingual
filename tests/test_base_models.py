"""Universal model loading and frozen opcode preprocessing."""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import huggingface_hub
import pytest
import torch
from tokenizers import AddedToken, Tokenizer, models as token_models, pre_tokenizers, processors
from transformers import PreTrainedTokenizerFast
import yaml

from pylingual import models
from pylingual.opcode_models import OpcodeRegistry, OpcodeSegmenter


@pytest.fixture
def inputs(tmp_path):
    tokens = ["[PAD]", "[CLS]", "[SEP]", "[UNK]", "[MASK]", "LOAD_CONST", "<mask_0>", "None", "<SEP>", "Python", "3.15:"]
    opcodes = ["LOAD_CONST", "RETURN_VALUE"]
    atomic = [f"<opcode:{name}>" for name in opcodes] + [f"<future_opcode_{i:02d}>" for i in range(64)]
    vocabulary = {token: i for i, token in enumerate(tokens + atomic)}
    backend = Tokenizer(token_models.WordLevel(vocabulary, unk_token="[UNK]"))
    backend.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    backend.post_processor = processors.TemplateProcessing(single="[CLS] $A [SEP]", special_tokens=[("[CLS]", 1), ("[SEP]", 2)])
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, pad_token="[PAD]", cls_token="[CLS]", sep_token="[SEP]", unk_token="[UNK]", mask_token="[MASK]")
    tokenizer.add_tokens([AddedToken(token) for token in atomic])
    # Real statement tokenizers also mark ordinary Python/source masks special.
    tokenizer.add_special_tokens({"additional_special_tokens": ["None", "<mask_0>"]})
    data = {
        "format": 1,
        "preprocessing": "opcode-field-placeholders-v1",
        "known_opcodes": {name: {"token": f"<opcode:{name}>", "id": vocabulary[f"<opcode:{name}>"]} for name in opcodes},
        "reserved_slots": [{"slot": i, "token": f"<future_opcode_{i:02d}>", "id": vocabulary[f"<future_opcode_{i:02d}>"]} for i in range(64)],
        "source_generation_forbidden_ids": [vocabulary[token] for token in atomic],
    }
    path = tmp_path / "opcode_registry.json"
    path.write_text(json.dumps(data))
    return tokenizer, data, path


class SegmentModel(torch.nn.Module):
    def __init__(self, tokenizer):
        super().__init__()
        self.embedding = torch.nn.Embedding(len(tokenizer), 1)
        self.config = SimpleNamespace(max_position_embeddings=128, id2label={0: "B", 1: "I", 2: "E"})
        self.tokenizer = tokenizer

    def get_input_embeddings(self):
        return self.embedding

    def forward(self, input_ids, **kwargs):
        logits = torch.zeros((*input_ids.shape, 3), device=input_ids.device)
        logits[..., 1] = 3
        logits[..., 0][input_ids == self.tokenizer.convert_tokens_to_ids("<opcode:LOAD_CONST>")] = 9
        logits[..., 2][input_ids == self.tokenizer.convert_tokens_to_ids("<opcode:RETURN_VALUE>")] = 9
        return SimpleNamespace(logits=logits)


class TranslationModel(SegmentModel):
    def generate(self, **kwargs):
        self.last_generation = kwargs
        ids = [0, 1, self.tokenizer.convert_tokens_to_ids("None"), self.tokenizer.convert_tokens_to_ids("<mask_0>"), self.tokenizer.convert_tokens_to_ids("<opcode:LOAD_CONST>"), self.tokenizer.convert_tokens_to_ids("<future_opcode_00>"), 2]
        return torch.tensor([ids] * len(kwargs["input_ids"]))


def test_registry_changes_only_opcode_fields(inputs):
    tokenizer, data, path = inputs
    registry = OpcodeRegistry.load(path, tokenizer)
    assert registry.bind("E-> ^~> TARGET_1 LOAD_CONST LOAD_CONST <mask_0> <SEP> RETURN_VALUE") == "E-> ^~> TARGET_1 <opcode:LOAD_CONST> LOAD_CONST <mask_0> <SEP> <opcode:RETURN_VALUE>"
    with pytest.raises(ValueError, match="opcode"):
        registry.bind("UNKNOWN_OPCODE")
    assert len(registry.forbidden_ids) == 66


@pytest.mark.parametrize("damage", ["slots", "id", "forbidden", "preprocessing"])
def test_registry_rejects_incompatible_token_ids(inputs, damage):
    tokenizer, data, path = inputs
    if damage == "slots":
        data["reserved_slots"].pop()
    elif damage == "id":
        data["known_opcodes"]["LOAD_CONST"]["id"] = 0
    elif damage == "forbidden":
        data["source_generation_forbidden_ids"] = []
    else:
        data["preprocessing"] = "wrong-contract"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        OpcodeRegistry.load(path, tokenizer)


def test_segmentation_returns_one_prediction_per_instruction(inputs):
    tokenizer, _, path = inputs
    segmenter = OpcodeSegmenter(SegmentModel(tokenizer), tokenizer, OpcodeRegistry.load(path, tokenizer))
    text = "LOAD_CONST LOAD_CONST <SEP> RETURN_VALUE"
    results = segmenter([text, text], batch_size=1)
    assert [[r["entity"] for r in row] for row in results] == [["B", "E"], ["B", "E"]]
    assert [r["word"] for r in results[0]] == text.split(" <SEP> ")
    assert [r["index"] for r in results[0]] == [1, 2]
    assert segmenter.instruction_token_lengths(["LOAD_CONST LOAD_CONST"]) == [len(tokenizer("<opcode:LOAD_CONST> LOAD_CONST")["input_ids"])]
    assert segmenter(text) == results[0]
    with pytest.raises(ValueError):
        segmenter([text], batch_size=0)


def test_segmenter_checks_capacity_and_instruction_coverage(inputs):
    tokenizer, _, path = inputs
    model = SegmentModel(tokenizer)
    segmenter = OpcodeSegmenter(model, tokenizer, OpcodeRegistry.load(path, tokenizer))
    model.config.max_position_embeddings = 4
    with pytest.raises(ValueError, match="capacity"):
        segmenter(["LOAD_CONST LOAD_CONST <SEP> RETURN_VALUE"])


def test_translator_preserves_source_masks_and_forbids_input_only_tokens(inputs):
    tokenizer, _, path = inputs
    registry = OpcodeRegistry.load(path, tokenizer)
    model = TranslationModel(tokenizer)
    translator = models.CacheTranslator(model, tokenizer, registry, cache_namespace="statement@revision")
    assert translator._translate_and_decode(["LOAD_CONST LOAD_CONST"]) == ["None <mask_0>"]
    assert tokenizer.decode(model.last_generation["input_ids"][0], skip_special_tokens=False).startswith("[CLS] <opcode:LOAD_CONST> LOAD_CONST")
    assert model.last_generation["bad_words_ids"] == [[i] for i in registry.forbidden_ids]


def test_default_config_pins_one_flat_model_pair_and_tokenizer_family():
    config = yaml.safe_load((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    assert set(config) == {"SEGMENTATION_MODEL", "STATEMENT_MODEL", "TOKENIZER"}
    assert config["STATEMENT_MODEL"]["REVISION"] == "a20bc4d28fe8641df0f90aa3665431368930c329"
    assert config["SEGMENTATION_MODEL"]["REVISION"] == "37cfee8f8e7bc16c4050056ffcdead83f714c7cf"
    assert config["TOKENIZER"]["REVISION"] == "d23233a4bb237dcc3b1660e46a42f9189eaf0f6c"
    assert all(set(entry) == {"REPO", "REVISION"} for entry in config.values())


def test_loading_reuses_one_model_pair_and_translation_cache(inputs, tmp_path):
    tokenizer, _, registry_path = inputs
    config = yaml.safe_load((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    path = tmp_path / "models.yaml"
    path.write_text(yaml.safe_dump(config))
    segmentation, translation = SegmentModel(tokenizer), TranslationModel(tokenizer)
    with (
        patch.object(models.transformers.AutoModelForTokenClassification, "from_pretrained", return_value=segmentation) as seg_load,
        patch.object(models.transformers.T5ForConditionalGeneration, "from_pretrained", return_value=translation) as stmt_load,
        patch.object(models.transformers.PreTrainedTokenizerFast, "from_pretrained", return_value=tokenizer) as tokenizer_load,
        patch.object(huggingface_hub, "hf_hub_download", return_value=str(registry_path)) as download,
        patch.object(models, "_free_device_memory"),
        patch.object(models.redis, "StrictRedis", return_value=Mock()),
    ):
        first = models.load_models(path, redis_cache_server_ip="localhost", device=torch.device("cpu"))
        last = models.load_models(path, redis_cache_server_ip="localhost", device=torch.device("cpu"))
    assert first[0] is last[0]
    assert first[1].model is last[1].model is translation
    assert first[1] is last[1]
    assert first[1].cache is last[1].cache
    statement, tokenizer_config = config["STATEMENT_MODEL"], config["TOKENIZER"]
    assert first[1].redis_namespace_prefix == f"{statement['REPO']}@{statement['REVISION']}:{tokenizer_config['REPO']}@{tokenizer_config['REVISION']}:"
    assert seg_load.call_count == stmt_load.call_count == 1
    assert tokenizer_load.call_count == download.call_count == 2
    assert all(call.kwargs["revision"] == "d23233a4bb237dcc3b1660e46a42f9189eaf0f6c" for call in tokenizer_load.call_args_list)
    assert {call.kwargs["subfolder"] for call in tokenizer_load.call_args_list} == {"statement", "segmentation"}


def test_redis_cache_is_namespaced_by_model_identity(inputs):
    tokenizer, _, path = inputs
    registry = OpcodeRegistry.load(path, tokenizer)
    with patch.object(models.redis, "StrictRedis", return_value=Mock()):
        first = models.CacheTranslator(TranslationModel(tokenizer), tokenizer, registry, redis_cache_server_ip="localhost", cache_namespace="statement@one")
        second = models.CacheTranslator(TranslationModel(tokenizer), tokenizer, registry, redis_cache_server_ip="localhost", cache_namespace="statement@two")
    assert first.redis_namespace_prefix == "statement@one:"
    assert second.redis_namespace_prefix == "statement@two:"


def test_loading_rejects_wrong_vocabulary_before_translation(inputs, tmp_path):
    tokenizer, _, registry_path = inputs
    path = tmp_path / "models.yaml"
    path.write_text((Path(models.__file__).parent / "decompiler_config.yaml").read_text())
    wrong = SegmentModel(tokenizer)
    wrong.embedding = torch.nn.Embedding(len(tokenizer) + 1, 1)
    with (
        patch.object(models.transformers.AutoModelForTokenClassification, "from_pretrained", return_value=wrong),
        patch.object(models.transformers.PreTrainedTokenizerFast, "from_pretrained", return_value=tokenizer),
        patch.object(huggingface_hub, "hf_hub_download", return_value=str(registry_path)),
        patch.object(models.transformers.T5ForConditionalGeneration, "from_pretrained") as translation,
        patch.object(models, "_free_device_memory"),
    ):
        with pytest.raises(ValueError, match="vocabulary"):
            models.load_models(path, device=torch.device("cpu"))
    translation.assert_not_called()


def test_segmentation_rejects_wrong_labels_and_empty_instructions(inputs):
    tokenizer, _, path = inputs
    registry = OpcodeRegistry.load(path, tokenizer)
    model = SegmentModel(tokenizer)
    segmenter = OpcodeSegmenter(model, tokenizer, registry)
    with pytest.raises(ValueError, match="opcode"):
        segmenter(["LOAD_CONST None <SEP> "])
    model.config.id2label = {0: "I", 1: "B", 2: "E"}
    with pytest.raises(ValueError, match="labels"):
        OpcodeSegmenter(model, tokenizer, registry)


def test_tokenizer_only_family_does_not_require_a_model_configuration(inputs, tmp_path):
    tokenizer, _, registry_path = inputs
    root = tmp_path / "tokenizer-only-family"
    tokenizer.save_pretrained(root / "segmentation")
    config = {"REPO": str(root), "REVISION": "frozen"}
    with patch.object(huggingface_hub, "hf_hub_download", return_value=str(registry_path)):
        loaded, registry = models._load_opcode_tokenizer(config, "segmentation", False)
    assert len(loaded) == len(tokenizer)
    assert registry.bind("LOAD_CONST None") == "<opcode:LOAD_CONST> None"
