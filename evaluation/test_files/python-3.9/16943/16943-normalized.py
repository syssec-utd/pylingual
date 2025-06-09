def toarray(self):
    """
        Returns the contents as a local array.

        Will likely cause memory problems for large objects.
        """
    rdd = self._rdd if self._ordered else self._rdd.sortByKey()
    x = rdd.values().collect()
    return asarray(x).reshape(self.shape)