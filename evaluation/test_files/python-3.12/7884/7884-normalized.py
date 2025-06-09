def _plant_trie(strings: _List[str]) -> dict:
    """Create a Trie out of a list of words and return an atomic regex pattern.

    The corresponding Regex should match much faster than a simple Regex union.
    """
    trie = {}
    for string in strings:
        d = trie
        for char in string:
            d[char] = char in d and d[char] or {}
            d = d[char]
        d[''] = None
    return trie