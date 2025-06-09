import base64
from typing import Any
import regex as re
from azuma import types
from azuma.exceptions import UnsupportedFeature
SUPPORTED_MODIFIERS = {'contains', 'all', 'base64', 'endswith', 'startswith', 're'}

def decode_base64(x: str):
    x = x.replace('\n', '')
    return base64.b64encode(x.encode()).decode()
MODIFIER_FUNCTIONS = {'contains': lambda x: f'.*{x}.*', 'base64': lambda x: decode_base64(x), 'endswith': lambda x: f'.*{x}$', 'startswith': lambda x: f'^{x}.*'}

def process_field_name(field_string: str):
    name_and_modifiers = field_string.split('|')
    name = name_and_modifiers.pop(0)
    modifiers = [_m for _m in name_and_modifiers if _m]
    unsupported = set(modifiers) - SUPPORTED_MODIFIERS
    if unsupported:
        raise UnsupportedFeature(f'Unsupported field modifiers used: {unsupported}')
    return (name, modifiers)
_NSC = NON_SPECIAL_CHARACTERS = '[^\\\\*?]*'
ESCAPED_SPECIAL_CHARACTER = '(?:\\\\[*?])'
ESCAPED_OTHER_CHARACTER = '(?:\\\\[^*?])'
ESCAPED_WILDCARD_PATTERN = re.compile(f'(?:{_NSC}{ESCAPED_SPECIAL_CHARACTER}*{ESCAPED_OTHER_CHARACTER})*')
UPTO_WILDCARD = re.compile('^([^\\\\?*]+|(?:\\\\[^?*\\\\])+)+')

def sigma_string_to_regex(original_value: str):
    value = original_value
    full_content: list[str] = []
    while value:
        match = UPTO_WILDCARD.match(value)
        if match:
            matched = match.group(0)
            full_content.append(re.escape(matched))
            value = value[len(matched):]
        elif value.startswith('*'):
            full_content.append('.*')
            value = value[1:]
        elif value.startswith('\\*'):
            full_content.append(re.escape('*'))
            value = value[2:]
        elif value.startswith('?'):
            full_content.append('.')
            value = value[1:]
        elif value.startswith('\\?'):
            full_content.append(re.escape('?'))
            value = value[2:]
        elif value.startswith('\\\\*'):
            full_content.append(re.escape('\\') + '.*')
            value = value[3:]
        elif value.startswith('\\\\?'):
            full_content.append(re.escape('\\') + '.')
            value = value[3:]
        elif value.startswith('\\'):
            full_content.append(re.escape('\\'))
            value = value[1:]
        else:
            raise ValueError(f'Could not parse string matching pattern: {original_value}')
    return ''.join(full_content)

def get_modified_value(value: str, modifiers: list[str] | None) -> str:
    if not modifiers:
        return f'^{value}$'
    for mod in modifiers:
        func = MODIFIER_FUNCTIONS.get(mod)
        value = func(value) if func else value
    return value

def apply_modifiers(value: str, modifiers: list[str]) -> types.Query:
    """
    Apply as many modifiers as we can during signature construction
    to speed up the matching stage as much as possible.
    """
    if 're' in modifiers:
        return re.compile(value, flags=re.IGNORECASE | re.V1 | re.DOTALL)
    if not ESCAPED_WILDCARD_PATTERN.fullmatch(value):
        reg_value = sigma_string_to_regex(value)
        value = get_modified_value(reg_value, modifiers)
        return re.compile(value, flags=re.IGNORECASE | re.V1 | re.DOTALL)
    value = get_modified_value(value, modifiers)
    value = str(value).replace('\\*', '*').replace('\\?', '?')
    return value.lower()

def normalize_field_map(field: dict[str, Any]) -> types.DetectionMap:
    out: types.DetectionMap = []
    for raw_key, value in field.items():
        key, modifiers = process_field_name(raw_key)
        if value is None:
            out.append((key, ([None], modifiers)))
            continue
        if isinstance(value, list):
            out.append((key, ([apply_modifiers(str(_v), modifiers) if _v is not None else None for _v in value], modifiers)))
            continue
        out.append((key, ([apply_modifiers(str(value), modifiers)], modifiers)))
    return out