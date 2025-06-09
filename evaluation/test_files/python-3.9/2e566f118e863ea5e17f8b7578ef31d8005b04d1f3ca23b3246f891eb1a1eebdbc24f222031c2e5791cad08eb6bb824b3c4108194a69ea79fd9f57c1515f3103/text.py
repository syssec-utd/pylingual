"""Text processing utilities."""

def truncate_chars(val: str, num: int, end: str='...') -> str:
    """Truncates a string if it is longer than the specified number of characters.
    Truncated strings will end with `end`, an ellipsis by default."""
    val_length = len(val)
    end_length = len(end)
    if val_length < num:
        return val
    return f'{val[:num - end_length]}{end}'

def truncate_words(val: str, num: int, end: str='...') -> str:
    """Truncates a string down to the number of words passed as the first parameter."""
    words = val.split()
    if len(words) < num:
        return ' '.join(words)
    return ' '.join(words[:num]) + end