def minute(self):
    """
        Extract the "minute" part from a date column.

        :returns: a single-column H2OFrame containing the "minute" part from the source frame.
        """
    fr = H2OFrame._expr(expr=ExprNode('minute', self), cache=self._ex._cache)
    if fr._ex._cache.types_valid():
        fr._ex._cache.types = {k: 'int' for k in self._ex._cache.types.keys()}
    return fr