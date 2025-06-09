def select_text(text, reading=False, prefer=None):
    """Select the correct text from the Japanese number, reading and
    alternatives"""
    if reading:
        text = text[1]
    else:
        text = text[0]
    if not isinstance(text, strtype):
        common = set(text) & set(prefer or set())
        if len(common) == 1:
            text = common.pop()
        else:
            text = text[0]
    return text