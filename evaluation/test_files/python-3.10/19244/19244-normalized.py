def lookup_alphabet(charset):
    """
    retrieves a named charset or treats the input as a custom alphabet and use that
    """
    if charset in PRESETS:
        return PRESETS[charset]
    if len(charset) < 16:
        _logger.warning('very small alphabet in use, possibly a failed lookup?')
    return charset