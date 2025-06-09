def uniq_in_order(iterable):
    result = []
    prev = None
    for char in iterable[0:]:
        if char != prev:
            result.append(char)
            prev = char
    return result