def inc(self, name, value=1):
    """ Increment value """
    clone = self._clone()
    clone._qsl = [(q, v) if q != name else (q, int(v) + value) for (q, v) in self._qsl]
    if name not in dict(clone._qsl).keys():
        clone._qsl.append((name, value))
    return clone