from __future__ import annotations

import yaml
import logging

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from pylingual.masking.model_disasm import fix_jump_targets, normalize_masks, restore_masks
from pylingual.utils.lists import flatten
from pylingual.utils.tracked_list import TrackedDataset, TRANSLATION_STEP
from pylingual.utils.version import PythonVersion
from pylingual.utils.lazy import lazy_import

if TYPE_CHECKING:
    import torch
    import transformers
    import huggingface_hub
else:
    lazy_import("torch")
    lazy_import("transformers")
    lazy_import("huggingface_hub")

logger = logging.getLogger(__name__)


# translator with caching
class CacheTranslator:
    """
    Adds cache support for statement translation

    :param translator : The loaded translation model
    :param maxsize : The maximum amount of cached items
    """

    def __init__(self, translator: transformers.TranslationPipeline, maxsize=50000):
        self.translator = translator
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def __getitem__(self, item):
        self.cache.move_to_end(item)
        return self.cache[item]

    def _translate_and_decode(self, translation_requests: TrackedDataset | list[str], batch_size: int = 32, **kwargs) -> list[str]:
        # return_tensors=True prevents standard postprocessing which skips special tokens
        translation_result = self.translator(translation_requests, return_tensors=True, batch_size=batch_size, **kwargs)
        decoded_results = []
        for result in flatten(translation_result):
            # explicitly filter out the special tokens we want to skip: <pad>, <s>, </s>, <unk>, <mask>
            filtered_tokens = [tok for tok in result["translation_token_ids"].tolist() if tok not in [0, 1, 2, 3, 4]]
            # decode the remaining tokens
            decoded_results.append(self.translator.tokenizer.decode(filtered_tokens, skip_special_tokens=False))

        return decoded_results

    def _translate_with_backoff(self, translation_requests: TrackedDataset) -> list[str]:
        try:
            return self._translate_and_decode(translation_requests, batch_size=32)
        except Exception as e:
            logger.info(f"Lowering translation batch size ({e})")
        # Try with batch_size = 1 if normal translation fails:
        try:
            return self._translate_and_decode(translation_requests, batch_size=1)
        except Exception as e:
            logger.info(f"Lowering translation batch size ({e})")
        translation_results = []
        # try one-by-one if batch_size=1 fails
        for request in translation_requests:
            try:
                translation_results.append(self._translate_and_decode([request], batch_size=1)[0])
            except Exception:
                # last resort fallback
                translation_results.append("'''Decompiler error: line too long for translation. Please decompile this statement manually.'''")
        return translation_results

    def __call__(self, args: list, **_):
        normalized_args = [normalize_masks(fix_jump_targets(x)) for x in args]

        # New are those not in the local cache
        new = TrackedDataset(TRANSLATION_STEP, list({norm for norm, _ in normalized_args if norm not in self.cache}))

        # Now, "new" has been updated to those not in local
        for arg, result in zip(new.x, self._translate_with_backoff(new)):
            self.cache[arg] = result

        results = [restore_masks(self[norm], order) for norm, order in normalized_args]
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        return results


def load_models(config_file: Path = Path("pylingual/decompiler_config.yaml"), version: PythonVersion = PythonVersion(3.9), token=False) -> tuple[transformers.Pipeline, CacheTranslator]:
    logger.info(f"Loading models for {version}...")
    with config_file.open() as f:
        config = yaml.safe_load(f)
        seg_config = config[f"v{version}"]["SEGMENTATION_MODEL"]
        stmt_config = config[f"v{version}"]["STATEMENT_MODEL"]

    #################################
    # Segmentation model components #
    #################################
    segmentation_model = transformers.AutoModelForTokenClassification.from_pretrained(
        pretrained_model_name_or_path=seg_config["REPO"],
        revision=seg_config["REVISION"],
        token=token,
    )
    segmentation_tokenizer_file = huggingface_hub.hf_hub_download(repo_id=seg_config["TOKENIZER"], filename="tokenizer.json", token=token)
    segmentation_tokenizer = transformers.PreTrainedTokenizerFast(
        tokenizer_file=segmentation_tokenizer_file,
        unk_token="[UNK]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        sep_token="[SEP]",
        mask_token="[MASK]",
    )
    if torch.cuda.is_available():
        logger.info("Using CUDA GPU for models")
        device = torch.device("cuda:0")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        logger.info("Using MPS (Metal Performance Shaders) GPU for models")
        device = torch.device("mps")
    else:
        logger.warning("Using CPU for models")
        device = torch.device("cpu")
    segmenter = transformers.pipeline("token-classification", model=segmentation_model, tokenizer=segmentation_tokenizer, aggregation_strategy="none", device=device)
    #########################################
    # Sequence translation model components #
    #########################################
    translation_model = transformers.T5ForConditionalGeneration.from_pretrained(stmt_config["REPO"], revision=stmt_config["REVISION"], token=token)
    translation_tokenizer = transformers.RobertaTokenizer.from_pretrained(stmt_config["TOKENIZER"], token=token)
    translator = transformers.TranslationPipeline(model=translation_model, tokenizer=translation_tokenizer, max_length=512, truncation=False, device=device)

    return segmenter, CacheTranslator(translator)
