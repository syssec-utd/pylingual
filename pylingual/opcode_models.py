"""The frozen base models' opcode-field and instruction-alignment contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from pylingual.utils.lazy import lazy_import

if TYPE_CHECKING:
    import torch
else:
    lazy_import("torch")

SEPARATOR = " <SEP> "
OPCODE_FIELD = re.compile(r"^(\s*(?:(?:E->|\^~>|v~>)\s+)*(?:(?:\d+|TARGET_\d+)\s+)?)([A-Z][A-Z0-9_]*)(?=\s|,|-FUTURE(?:\s|$)|$)")


class OpcodeRegistry:
    """Validate immutable token IDs. Untrained opcodes fail rather than acquiring bindings."""

    def __init__(self, data, tokenizer):
        if data.get("format") != 1 or data.get("preprocessing") != "opcode-field-placeholders-v1":
            raise ValueError("Unsupported opcode preprocessing contract")
        self.known = data.get("known_opcodes", {})
        slots = data.get("reserved_slots", [])
        if not self.known or not isinstance(self.known, dict) or len(slots) != 64:
            raise ValueError("Opcode registry requires known opcodes and 64 reserved slots")
        if {item.get("slot") for item in slots} != set(range(64)):
            raise ValueError("Invalid reserved opcode slots")
        entries = list(self.known.values()) + slots
        for name, entry in self.known.items():
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name) or entry.get("token") != f"<opcode:{name}>":
                raise ValueError("Invalid known opcode token")
        for entry in slots:
            if entry.get("token") != f"<future_opcode_{entry['slot']:02d}>":
                raise ValueError("Invalid reserved opcode token")
        ids = [entry.get("id") for entry in entries]
        if any(type(identifier) is not int or identifier < 0 for identifier in ids) or len(set(ids)) != len(ids):
            raise ValueError("Invalid or duplicate opcode IDs")
        if set(data.get("source_generation_forbidden_ids", [])) != set(ids):
            raise ValueError("Generation exclusions must cover all opcode IDs")
        for entry in entries:
            token, identifier = entry["token"], entry["id"]
            if tokenizer.convert_tokens_to_ids(token) != identifier or tokenizer(token, add_special_tokens=False)["input_ids"] != [identifier] or identifier in tokenizer.all_special_ids:
                raise ValueError("Opcode registry/tokenizer ID or atomicity mismatch")
        self.forbidden_ids = sorted(ids)

    @classmethod
    def load(cls, path, tokenizer):
        return cls(json.loads(Path(path).read_text()), tokenizer)

    def bind(self, bytecode):
        result = []
        for instruction in bytecode.split(SEPARATOR):
            match = OPCODE_FIELD.match(instruction)
            if match is None or match.group(2) not in self.known:
                raise ValueError(f"Unbound opcode field: {instruction[:100]!r}")
            result.append(instruction[: match.start(2)] + self.known[match.group(2)]["token"] + instruction[match.end(2) :])
        return SEPARATOR.join(result)


def _instruction_positions(tokenizer, bytecode):
    """Use character offsets, not WordPiece word IDs, for atomic AddedTokens."""
    spans, cursor = [], 0
    for instruction in bytecode.split(SEPARATOR):
        spans.append((cursor, cursor + len(instruction)))
        cursor += len(instruction) + len(SEPARATOR)
    encoded = tokenizer(bytecode, return_offsets_mapping=True)
    first, instruction = {}, 0
    for position, (start, end) in enumerate(encoded.pop("offset_mapping")):
        if start == end:
            continue
        while instruction < len(spans) and start >= spans[instruction][1]:
            instruction += 1
        if instruction == len(spans):
            continue
        left, right = spans[instruction]
        if end > left and start < right:
            if end > right and bytecode[right:end].strip():
                raise ValueError("Tokenizer token crosses an instruction boundary")
            first.setdefault(instruction, position)
    if set(first) != set(range(len(spans))):
        raise ValueError("Segmentation tokens do not cover every instruction")
    return encoded, list(first.values())


class OpcodeSegmenter:
    """Plain token classifier returning exactly one B/I/E result per instruction."""

    def __init__(self, model, tokenizer, registry):
        if model.config.id2label != {0: "B", 1: "I", 2: "E"}:
            raise ValueError("Segmentation model must use the trained B/I/E labels")
        self.model, self.tokenizer, self.registry = model, tokenizer, registry
        self.device = next(model.parameters()).device

    def instruction_token_lengths(self, instructions):
        return [len(self.tokenizer(self.registry.bind(text))["input_ids"]) for text in instructions]

    def __call__(self, requests, batch_size=8, **kwargs):
        if isinstance(requests, str):
            return self([requests], batch_size=batch_size, **kwargs)[0]
        if type(batch_size) is not int or batch_size < 1:
            raise ValueError("Positive segmentation batch size required")
        results = []
        self.model.eval()
        with torch.no_grad():
            for start in range(0, len(requests), batch_size):
                texts = [requests[i] for i in range(start, min(start + batch_size, len(requests)))]
                features, positions = [], []
                for text in texts:
                    encoded, first = _instruction_positions(self.tokenizer, self.registry.bind(text))
                    limit = self.model.config.max_position_embeddings - self.tokenizer.pad_token_id - 1
                    if len(encoded["input_ids"]) > limit:
                        raise ValueError("Segmentation window exceeds backbone positional capacity")
                    features.append(dict(encoded))
                    positions.append(first)
                batch = self.tokenizer.pad(features, padding=True, return_tensors="pt").to(self.device)
                scores = self.model(**batch).logits.softmax(-1)
                for text, first, row in zip(texts, positions, scores):
                    predictions, cursor = [], 0
                    for index, (raw, position) in enumerate(zip(text.split(SEPARATOR), first)):
                        confidence, label = row[position].max(-1)
                        predictions.append({"entity": self.model.config.id2label[int(label)], "score": float(confidence), "word": raw, "start": cursor, "end": cursor + len(raw), "index": index + 1})
                        cursor += len(raw) + len(SEPARATOR)
                    results.append(predictions)
        return results
