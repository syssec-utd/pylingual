from __future__ import annotations

import functools
import gc
import logging
import re
import threading
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

import redis
import yaml

from pylingual.masking.model_disasm import (
    encode_opcodes,
    fix_jump_targets,
    normalize_masks,
    restore_masks,
)
from pylingual.translation_constraints import StatementLogitsProcessor, TokenizerConstraintIndex
from pylingual.utils.lazy import lazy_import
from pylingual.utils.tracked_list import TRANSLATION_STEP, TrackedDataset

if TYPE_CHECKING:
    import torch
    import transformers

    from pylingual.utils.version import PythonVersion
else:
    lazy_import("torch")
    lazy_import("transformers")

logger = logging.getLogger(__name__)

_MASK_INDEX_RE = re.compile(r"<mask_(\d+)>")
_FSTRING_OPCODES = ("FORMAT_VALUE", "BUILD_STRING")
_TRANSLATION_FALLBACK = "'''Decompiler error: line too long for translation. Please decompile this statement manually.'''"


def _mask_count(text: str) -> int:
    nums = [int(m) for m in _MASK_INDEX_RE.findall(text)]
    return (max(nums) + 1) if nums else 0


def _is_resource_error(exc: BaseException) -> bool:
    if isinstance(exc, (MemoryError, torch.OutOfMemoryError)):
        return True
    if isinstance(exc, RuntimeError):
        msg = str(exc).lower()
        return "out of memory" in msg or "cuda error" in msg or "cublas" in msg or "cudnn" in msg
    return False


# translator with caching
class CacheTranslator:
    """
    Adds cache support and inference-time lexical/mask constraints for statement translation.

    :param model : The loaded translation model
    :param tokenizer : The loaded statement tokenizer
    :param cache_namespace : Base namespace pinning model & tokenizer revisions
    :param maxsize : The maximum amount of cached items
    """

    def __init__(
        self,
        model: transformers.T5ForConditionalGeneration,
        tokenizer: transformers.PreTrainedTokenizerFast,
        *,
        cache_namespace: str,
        redis_cache_server_ip: str = None,
        redis_port: int = 1679,
        device="cpu",
        maxsize=50000,
        use_constraints: bool = True,
        use_version_prefix: bool | None = None,
        max_length: int = 512,
        retry_max_length: int = 1024,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.use_constraints = use_constraints
        if use_version_prefix is None:
            use_version_prefix = bool(getattr(getattr(model, "config", None), "pylingual_version_prefix", False))
        self.use_version_prefix = use_version_prefix
        self.max_length = max_length
        self.retry_max_length = max(max_length, retry_max_length)

        roles = ("bos", "eos", "pad", "unk", "mask", "cls", "sep")
        self.decode_excluded_ids = {identifier for role in roles if (identifier := getattr(tokenizer, f"{role}_token_id", None)) is not None}
        bad_words_ids = getattr(getattr(model, "generation_config", None), "bad_words_ids", None) or []
        self.decode_excluded_ids.update(identifier for group in bad_words_ids for identifier in group)
        self.constraint_index = TokenizerConstraintIndex(tokenizer, bad_words_ids=bad_words_ids) if use_constraints else None
        self.model.to(self.device)
        self.model.eval()

        policy_tag = f":c{int(self.use_constraints)}-ml{self.max_length}-{self.retry_max_length}-vp{int(self.use_version_prefix)}"

        # Redis Caching
        self.redis_enabled = redis_cache_server_ip is not None
        if self.redis_enabled:
            self.redis_db = redis.StrictRedis(host=redis_cache_server_ip, port=redis_port, db=0, encoding="utf-8", decode_responses=True)
            self.redis_namespace_prefix = f"{cache_namespace}{policy_tag}:"

    def __getitem__(self, item):
        self.cache.move_to_end(item)
        return self.cache[item]

    def _is_pre312(self, version: PythonVersion | tuple[int, int] | str | None) -> bool:
        if version is None:
            return False
        if isinstance(version, str):
            return tuple(map(int, version.split(".")[:2])) < (3, 12)
        if isinstance(version, tuple):
            return version[:2] < (3, 12)
        return version < (3, 12)

    def _version_str(self, version: PythonVersion | tuple[int, int] | str | None) -> str | None:
        if version is None:
            return None
        if isinstance(version, tuple):
            return f"{version[0]}.{version[1]}"
        return str(version)

    def _format_encoder_input(self, normalized_bytecode: str, version: PythonVersion | tuple[int, int] | str | None = None) -> str:
        encoded = encode_opcodes(normalized_bytecode)
        if self.use_version_prefix and version is not None:
            return f"v{self._version_str(version)} <SEP> {encoded}"
        return encoded

    def _cache_key(self, normalized_bytecode: str, version: PythonVersion | tuple[int, int] | str | None = None) -> str:
        if self.use_version_prefix and version is not None:
            return f"v{self._version_str(version)} <SEP> {normalized_bytecode}"
        if self.use_constraints and self._is_pre312(version) and any(op in normalized_bytecode for op in _FSTRING_OPCODES):
            return f"py<312:{normalized_bytecode}"
        return normalized_bytecode

    def _decode_sequence(self, token_ids: list[int]) -> str:
        filtered_tokens = [tok for tok in token_ids if tok not in self.decode_excluded_ids]
        return self.tokenizer.decode(filtered_tokens, skip_special_tokens=False, clean_up_tokenization_spaces=False)

    def _generate_batch(
        self,
        batch: list[str],
        *,
        version: PythonVersion | tuple[int, int] | str | None = None,
        max_length: int | None = None,
        num_beams: int = 1,
    ) -> torch.Tensor:
        eff_max_len = max_length if max_length is not None else self.max_length
        encoder_texts = [self._format_encoder_input(text, version) for text in batch]
        encoded = self.tokenizer(encoder_texts, return_tensors="pt", padding=True).to(self.device)

        gen_kwargs: dict = {"max_length": eff_max_len}
        if num_beams > 1:
            gen_kwargs["num_beams"] = num_beams
            gen_kwargs["num_return_sequences"] = num_beams
        if self.use_constraints and self.constraint_index is not None:
            mask_counts = [_mask_count(text) for text in batch]
            gen_kwargs["logits_processor"] = [
                StatementLogitsProcessor(
                    self.constraint_index,
                    mask_counts,
                    py_lt_312=self._is_pre312(version),
                    num_beams=num_beams,
                )
            ]

        with torch.no_grad():
            return self.model.generate(**encoded, **gen_kwargs)

    def _translate_and_decode(
        self,
        batch: list[str],
        *,
        version: PythonVersion | tuple[int, int] | str | None = None,
        max_length: int | None = None,
    ) -> list[str]:
        """Translate a single batch of requests, retrying cap-exhausted rows once at retry_max_length."""
        eff_max_len = max_length if max_length is not None else self.max_length
        output = self._generate_batch(batch, version=version, max_length=eff_max_len, num_beams=1)
        token_rows = [row.tolist() for row in output]
        decoded_results = [self._decode_sequence(toks) for toks in token_rows]

        # Retry only rows that exhausted max_length without natural EOS (never force-closing mid-expression)
        eos_id = self.tokenizer.eos_token_id
        if eos_id is not None and eff_max_len < self.retry_max_length:
            exhausted = [idx for idx, toks in enumerate(token_rows) if len(toks) >= eff_max_len and eos_id not in toks[1:]]
            if exhausted:
                retry_batch = [batch[idx] for idx in exhausted]
                retry_output = self._generate_batch(retry_batch, version=version, max_length=self.retry_max_length, num_beams=1)
                for idx, retry_row in zip(exhausted, retry_output):
                    decoded_results[idx] = self._decode_sequence(retry_row.tolist())

        return decoded_results

    def _translate_with_backoff(
        self,
        translation_requests: TrackedDataset | list[str],
        batch_size: int = 32,
        *,
        version: PythonVersion | tuple[int, int] | str | None = None,
    ) -> list[tuple[str, bool]]:
        """Translate in batches, backing off only on resource/OOM errors. Returns ``(text, cacheable)`` pairs."""
        translation_results: list[tuple[str, bool]] = []
        for i in range(0, len(translation_requests), batch_size):
            batch = translation_requests[i : i + batch_size]
            try:
                decoded = self._translate_and_decode(batch, version=version)
                translation_results.extend((text, True) for text in decoded)
                continue
            except Exception as e:
                if not _is_resource_error(e):
                    raise
                error = repr(e)
            # handled outside the except block so tensors can be freed
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if batch_size == 1:
                logger.info(f"Could not translate statement ({error})")
                translation_results.append((_TRANSLATION_FALLBACK, False))
            else:
                logger.info(f"Lowering translation batch size to {batch_size // 2} ({error})")
                translation_results.extend(self._translate_with_backoff(batch, batch_size=batch_size // 2, version=version))
        return translation_results

    def translate_beam(
        self,
        args: list[str],
        *,
        num_beams: int = 4,
        version: PythonVersion | tuple[int, int] | str | None = None,
        check_timeout: callable = None,
    ) -> list[list[str]]:
        """Return up to ``num_beams`` deduplicated candidate translations per request without mutating caches."""
        if not args:
            return []
        if check_timeout is not None:
            check_timeout()
        normalized_args = [normalize_masks(fix_jump_targets(x)) for x in args]
        norm_texts = [norm for norm, _ in normalized_args]
        try:
            output = self._generate_batch(norm_texts, version=version, max_length=self.retry_max_length, num_beams=num_beams)
        except Exception as e:
            if not _is_resource_error(e):
                raise
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info(f"Beam translation OOM ({e!r}); skipping beam retry")
            return [[] for _ in args]

        candidates_per_req: list[list[str]] = []
        rows_per_req = max(1, output.shape[0] // len(args))
        for idx, (_, order) in enumerate(normalized_args):
            seen: set[str] = set()
            cands: list[str] = []
            for b in range(rows_per_req):
                decoded = self._decode_sequence(output[idx * rows_per_req + b].tolist())
                restored = restore_masks(decoded, order)
                if restored not in seen:
                    seen.add(restored)
                    cands.append(restored)
            candidates_per_req.append(cands)
        return candidates_per_req

    def __call__(self, args: list, check_timeout: callable = None, *, version: PythonVersion | tuple[int, int] | str | None = None, **_):
        normalized_args = [normalize_masks(fix_jump_targets(x)) for x in args]
        keyed_args = [(self._cache_key(norm, version), norm, order) for norm, order in normalized_args]

        if self.redis_enabled:
            to_fetch_from_redis = list({key for key, _, _ in keyed_args if key not in self.cache})
            redis_results = {key: self.redis_db.get(f"{self.redis_namespace_prefix}{key}") for key in to_fetch_from_redis}
            for translation_key, translation_result in redis_results.items():
                if translation_result:
                    self.cache[translation_key] = translation_result

        # Deduplicate missing entries by cache key, preserving normalized bytecode for model input
        missing_by_key: dict[str, str] = {}
        for key, norm, _ in keyed_args:
            if key not in self.cache and key not in missing_by_key:
                missing_by_key[key] = norm

        ordered_missing = sorted(missing_by_key.items(), key=lambda kv: len(kv[1]))
        new_keys = [k for k, _ in ordered_missing]
        new = TrackedDataset(
            TRANSLATION_STEP,
            [norm for _, norm in ordered_missing],
            check_timeout=check_timeout,
        )

        uncached_fallbacks: dict[str, str] = {}
        for key, (result, cacheable) in zip(new_keys, self._translate_with_backoff(new, version=version)):
            if cacheable:
                self.cache[key] = result
                if self.redis_enabled:
                    self.redis_db.set(f"{self.redis_namespace_prefix}{key}", result)
            else:
                uncached_fallbacks[key] = result

        results = [
            restore_masks(self[key] if key in self.cache else uncached_fallbacks[key], order)
            for key, _, order in keyed_args
        ]
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        return results


class OpcodeSegmenter:
    """Keep the trained instruction confidences used by segmentation correction."""

    def __init__(self, model, tokenizer, device):
        self.model = model.to(device).eval()
        self.tokenizer = tokenizer
        self.device = device

    def __call__(self, requests, batch_size=8, **_):
        if isinstance(requests, str):
            return self([requests], batch_size=batch_size)[0]
        if type(batch_size) is not int or batch_size < 1:
            raise ValueError("Positive segmentation batch size required")
        results = []
        with torch.no_grad():
            for start in range(0, len(requests), batch_size):
                texts = [requests[i] for i in range(start, min(start + batch_size, len(requests)))]
                encoded = self.tokenizer(texts, padding=True, return_tensors="pt", return_offsets_mapping=True)
                offsets = encoded.pop("offset_mapping").tolist()
                # The correction search ranks these confidences. NumPy softmax in
                # the generic pipeline changes rounding and can change its candidates.
                scores = self.model(**encoded.to(self.device)).logits.softmax(-1)
                confidences, labels = scores.max(-1)
                for spans, row_scores, row_labels in zip(offsets, confidences.tolist(), labels.tolist()):
                    results.append([
                        {"start": left, "end": right, "entity": self.model.config.id2label[label], "score": confidence}
                        for (left, right), confidence, label in zip(spans, row_scores, row_labels)
                        if left != right
                    ])
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
) -> tuple[OpcodeSegmenter, CacheTranslator]:
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
    segmenter = OpcodeSegmenter(segmentation_model, segmentation_tokenizer, device)

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
        use_version_prefix=stmt_config.get("VERSION_PREFIX"),
    )
    return segmenter, translator
