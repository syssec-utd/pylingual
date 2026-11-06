from __future__ import annotations

import functools
import gc
import redis
import yaml
import logging
import threading

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from pylingual.masking.model_disasm import (
    encode_opcodes,
    fix_jump_targets,
    normalize_masks,
    restore_masks,
)
from pylingual.utils.tracked_list import TrackedDataset, TRANSLATION_STEP
from pylingual.utils.lazy import lazy_import

if TYPE_CHECKING:
    import torch
    import transformers
else:
    lazy_import("torch")
    lazy_import("transformers")

logger = logging.getLogger(__name__)

# translator with caching
class CacheTranslator:
    """
    Adds cache support for statement translation

    :param translator : The loaded translation model
    :param maxsize : The maximum amount of cached items
    """

    def __init__(self, model: transformers.T5ForConditionalGeneration, tokenizer: transformers.PreTrainedTokenizerFast, *, cache_namespace: str, redis_cache_server_ip: str = None, redis_port: int = 1679, device="cpu", maxsize=50000):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.cache = OrderedDict()
        self.maxsize = maxsize
        roles = ("bos", "eos", "pad", "unk", "mask", "cls", "sep")
        self.decode_excluded_ids = {identifier for role in roles if (identifier := getattr(tokenizer, f"{role}_token_id", None)) is not None}
        self.decode_excluded_ids.update(identifier for group in model.generation_config.bad_words_ids or [] for identifier in group)
        self.model.to(self.device)
        self.model.eval()

        # Redis Caching
        self.redis_enabled = redis_cache_server_ip is not None

        if self.redis_enabled:
            self.redis_db = redis.StrictRedis(host=redis_cache_server_ip, port=redis_port, db=0, encoding="utf-8", decode_responses=True)
            self.redis_namespace_prefix = f"{cache_namespace}:"

    def __getitem__(self, item):
        self.cache.move_to_end(item)
        return self.cache[item]

    def _translate_and_decode(self, batch: list[str]) -> list[str]:
        """Translate a single batch of requests"""
        batch = [encode_opcodes(text) for text in batch]
        encoded = self.tokenizer(batch, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            output = self.model.generate(**encoded, max_length=512)

        decoded_results = []
        for tokens in output:
            # explicitly filter out the special tokens we want to skip: <pad>, <s>, </s>, <unk>, <mask>
            filtered_tokens = [tok for tok in tokens.tolist() if tok not in self.decode_excluded_ids]
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

def _load_tokenizer(config, task, token):
    return _cached_first(transformers.PreTrainedTokenizerFast.from_pretrained, config["REPO"], revision=config["REVISION"], subfolder=task, token=token)


def _free_device_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def _single_slot_cache(fn):
    """Keep only the latest models loaded, freeing the old ones first; falls back to CPU on GPU OOM."""
    lock = threading.Lock()
    loaded_key = loaded_models = None

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal loaded_key, loaded_models
        key = (args, tuple(sorted(kwargs.items())))
        with lock:
            if loaded_key == key:
                return loaded_models
            loaded_key = loaded_models = None
            _free_device_memory()
            try:
                loaded_models = fn(*args, **kwargs)
            except torch.OutOfMemoryError:
                logger.warning("Not enough GPU memory to load models, falling back to CPU")
                _free_device_memory()
                loaded_models = fn(*args, **{**kwargs, "device": torch.device("cpu")})
            loaded_key = key
            return loaded_models

    return wrapper

@_single_slot_cache
def load_models(
    config_file: Path = Path("pylingual/decompiler_config.yaml"),
    redis_cache_server_ip: str = None,
    redis_port: int = 1679,
    token=False,
    device: torch.device | None = None,
) -> tuple[transformers.Pipeline, CacheTranslator]:
    logger.info("Loading universal models...")
    with config_file.open() as f:
        config = yaml.safe_load(f)
    seg_config = config["SEGMENTATION_MODEL"]
    stmt_config = config["STATEMENT_MODEL"]
    tokenizer_config = config["TOKENIZER"]

    #################################
    # Segmentation model components #
    #################################
    segmentation_model = _cached_first(
        transformers.AutoModelForTokenClassification.from_pretrained,
        pretrained_model_name_or_path=seg_config["REPO"],
        revision=seg_config["REVISION"],
        token=token,
    )

    segmentation_tokenizer = _load_tokenizer(tokenizer_config, "segmentation", token)
    if segmentation_model.get_input_embeddings().num_embeddings != len(segmentation_tokenizer):
        raise ValueError("Segmentation model vocabulary differs from its frozen tokenizer")
    if device is not None:
        logger.info(f"Using {device} for models")
    elif torch.cuda.is_available():
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
   
    translation_tokenizer = _load_tokenizer(tokenizer_config, "statement", token)
    if translation_model.get_input_embeddings().num_embeddings != len(translation_tokenizer):
        raise ValueError("Translation model vocabulary differs from its frozen tokenizer")
    namespace = f"{stmt_config['REPO']}@{stmt_config['REVISION']}:{tokenizer_config['REPO']}@{tokenizer_config['REVISION']}"
    translator = CacheTranslator(
        translation_model,
        translation_tokenizer,
        cache_namespace=namespace,
        redis_cache_server_ip=redis_cache_server_ip,
        redis_port=redis_port,
        device=device,
    )
    return segmenter, translator
