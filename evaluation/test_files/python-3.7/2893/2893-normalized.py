def pop(self, key, default=__marker):
    """od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.

        """
    if key in self:
        result = self[key]
        del self[key]
        return result
    if default is self.__marker:
        raise KeyError(key)
    return default