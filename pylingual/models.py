from __future__ import annotations

import redis
import yaml
import logging

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING
from functools import lru_cache

from pylingual.masking.model_disasm import (
    fix_jump_targets,
    normalize_masks,
    restore_masks,
)
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

    def __init__(self, model: transformers.T5ForConditionalGeneration, tokenizer: transformers.RobertaTokenizer, python_version: str, redis_cache_server_ip: str = None, redis_port: int = 1679, device="cpu", maxsize=50000):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.model.to(self.device)

        # Redis Caching
        self.redis_enabled = redis_cache_server_ip is not None

        if self.redis_enabled:
            self.redis_db = redis.StrictRedis(host=redis_cache_server_ip, port=redis_port, db=0, encoding="utf-8", decode_responses=True)
            self.redis_namespace_prefix = f"{python_version}:"

    def __getitem__(self, item):
        self.cache.move_to_end(item)
        return self.cache[item]

    def _translate_and_decode(self, batch: list[str]) -> list[str]:
        """Translate a single batch of requests"""
        encoded = self.tokenizer(batch, return_tensors="pt", padding=True).to(self.device)

        with torch.no_grad():
            output = self.model.generate(**encoded, max_length=512)

        decoded_results = []
        for tokens in output:
            # explicitly filter out the special tokens we want to skip: <pad>, <s>, </s>, <unk>, <mask>
            filtered_tokens = [tok for tok in tokens.tolist() if tok not in [0, 1, 2, 3, 4]]
            # decode the remaining tokens
            decoded_results.append(self.tokenizer.decode(filtered_tokens, skip_special_tokens=False))

        return decoded_results

    def _translate_with_backoff(self, translation_requests: TrackedDataset | list[str], batch_size: int = 32) -> list[str]:
        translation_results = []
        # process in batches
        for i in range(0, len(translation_requests), batch_size):
            batch = translation_requests[i : i + batch_size]
            try:
                translation_results.extend(self._translate_and_decode(batch))
                continue
            except Exception as e:
                error = repr(e)
            # handled outside the except block so tensors can be freed
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if batch_size == 1:
                # fallback
                logger.info(f"Could not translate statement ({error})")
                translation_results.append("'''Decompiler error: line too long for translation. Please decompile this statement manually.'''")
            else:
                # retry with a smaller batch size
                logger.info(f"Lowering translation batch size to {batch_size // 2} ({error})")
                translation_results.extend(self._translate_with_backoff(batch, batch_size=batch_size // 2))
        return translation_results

    def __call__(self, args: list, check_timeout: callable = None, **_):
        normalized_args = [normalize_masks(fix_jump_targets(x)) for x in args]

        if self.redis_enabled:
            # Update local cache from redis
            to_fetch_from_redis = list({norm for norm, _ in normalized_args if norm not in self.cache})
            redis_results = {key: self.redis_db.get(f"{self.redis_namespace_prefix}{key}") for key in to_fetch_from_redis}
            for translation_key, translation_result in redis_results.items():
                if translation_result:
                    self.cache[translation_key] = translation_result

        # New are those not in the local cache
        new = TrackedDataset(
            TRANSLATION_STEP,
            # sorted by length so batches need less padding; order doesn't matter since results are keyed by request
            sorted({norm for norm, _ in normalized_args if norm not in self.cache}, key=len),
            check_timeout=check_timeout,
        )

        # Now, "new" has been updated to those not in local
        for arg, result in zip(new.x, self._translate_with_backoff(new)):
            self.cache[arg] = result
            if self.redis_enabled:
                self.redis_db.set(f"{self.redis_namespace_prefix}{arg}", self.cache[arg])

        results = [restore_masks(self[norm], order) for norm, order in normalized_args]
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        return results

# offline support if models are downloaded
def _cached_first(fn, *args, **kwargs):
    """Try the local HF cache first; fall back to downloading if it's missing."""
    try:
        result = fn(*args, local_files_only=True, **kwargs)
        # tokenizers don't raise when their files are missing, they come back with only the special tokens
        if isinstance(result, transformers.PreTrainedTokenizerBase) and len(result) <= len(result.all_special_tokens):
            raise OSError("tokenizer has no vocabulary")
        return result
    except (OSError, ValueError):
        logger.info(f"{getattr(fn, '__qualname__', fn)} not found in local cache for {args[:1]}, downloading...")
        return fn(*args, local_files_only=False, **kwargs)

@lru_cache(maxsize=1)
def load_models(
    config_file: Path = Path("pylingual/decompiler_config.yaml"),
    version: PythonVersion = PythonVersion(3.9),
    redis_cache_server_ip: str = None,
    redis_port: int = 1679,
    token=False,
) -> tuple[transformers.Pipeline, CacheTranslator]:
    logger.info(f"Loading models for {version}...")
    with config_file.open() as f:
        config = yaml.safe_load(f)
        seg_config = config[f"v{version}"]["SEGMENTATION_MODEL"]
        stmt_config = config[f"v{version}"]["STATEMENT_MODEL"]

    #################################
    # Segmentation model components #
    #################################
    segmentation_model = _cached_first(
        transformers.AutoModelForTokenClassification.from_pretrained,
        pretrained_model_name_or_path=seg_config["REPO"],
        revision=seg_config["REVISION"],
        token=token,
    )

    segmentation_tokenizer_file = _cached_first(
        huggingface_hub.hf_hub_download,
        repo_id=seg_config["TOKENIZER"],
        filename="tokenizer.json",
        token=token,
    )
    
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
    else:
        # MPS recompiles its Metal graph on every T5 decode step, which makes it far slower than
        # CPU for this workload, so it is not used even when available.
        logger.info("Using CPU for models")
        device = torch.device("cpu")
    segmenter = transformers.pipeline(
        "token-classification",
        model=segmentation_model,
        tokenizer=segmentation_tokenizer,
        aggregation_strategy="none",
        device=device,
    )
    #########################################
    # Sequence translation model components #
    #########################################
    
    translation_model = _cached_first(
        transformers.T5ForConditionalGeneration.from_pretrained,
        stmt_config["REPO"],
        revision=stmt_config["REVISION"],
        token=token,
    )
   
    translation_tokenizer = _cached_first(
        transformers.RobertaTokenizer.from_pretrained,
        stmt_config["TOKENIZER"],
        token=token,
    )

    return segmenter, CacheTranslator(translation_model, translation_tokenizer, python_version=version.as_str(), redis_cache_server_ip=redis_cache_server_ip, redis_port=redis_port, device=device)
