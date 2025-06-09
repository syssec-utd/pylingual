def normalize_enum_constant(s):
    """Return enum constant `s` converted to a canonical snake-case."""
    if s.islower():
        return s
    if s.isupper():
        return s.lower()
    return ''.join((ch if ch.islower() else '_' + ch.lower() for ch in s)).strip('_')