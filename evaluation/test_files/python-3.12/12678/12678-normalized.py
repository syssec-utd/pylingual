def _all_get_table_col(self, key, column, fullname):
    """ Creates a pytables column instance.

        The type of column depends on the type of `column[0]`.
        Note that data in `column` must be homogeneous!

        """
    val = column[0]
    try:
        if type(val) is int:
            return pt.IntCol()
        if isinstance(val, (str, bytes)):
            itemsize = int(self._prm_get_longest_stringsize(column))
            return pt.StringCol(itemsize)
        if isinstance(val, np.ndarray):
            if np.issubdtype(val.dtype, str) or np.issubdtype(val.dtype, bytes):
                itemsize = int(self._prm_get_longest_stringsize(column))
                return pt.StringCol(itemsize, shape=val.shape)
            else:
                return pt.Col.from_dtype(np.dtype((val.dtype, val.shape)))
        else:
            return pt.Col.from_dtype(np.dtype(type(val)))
    except Exception:
        self._logger.error('Failure in storing `%s` of Parameter/Result `%s`. Its type was `%s`.' % (key, fullname, repr(type(val))))
        raise