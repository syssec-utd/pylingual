def process_word(word: str, to_lower: bool=False, append_case: Optional[str]=None) -> Tuple[str]:
    """Converts word to a tuple of symbols, optionally converts it to lowercase
    and adds capitalization label.

    Args:
        word: input word
        to_lower: whether to lowercase
        append_case: whether to add case mark
            ('<FIRST_UPPER>' for first capital and '<ALL_UPPER>' for all caps)

    Returns:
        a preprocessed word
    """
    if all((x.isupper() for x in word)) and len(word) > 1:
        uppercase = '<ALL_UPPER>'
    elif word[0].isupper():
        uppercase = '<FIRST_UPPER>'
    else:
        uppercase = None
    if to_lower:
        word = word.lower()
    if word.isdigit():
        answer = ['<DIGIT>']
    elif word.startswith('http://') or word.startswith('www.'):
        answer = ['<HTTP>']
    else:
        answer = list(word)
    if to_lower and uppercase is not None:
        if append_case == 'first':
            answer = [uppercase] + answer
        elif append_case == 'last':
            answer = answer + [uppercase]
    return tuple(answer)