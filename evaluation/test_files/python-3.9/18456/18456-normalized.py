def count_types(self) -> int:
    """ Count subtypes """
    n = 0
    for s in self._hsig.values():
        if type(s).__name__ == 'Type':
            n += 1
    return n