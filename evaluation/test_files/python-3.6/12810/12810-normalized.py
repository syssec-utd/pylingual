def _store(self):
    """Returns a storage dictionary understood by the storage service.

        Sparse matrices are extracted similar to the :class:`~pypet.parameter.SparseParameter` and
        marked with the identifier `__spsp__`.

        """
    store_dict = {}
    for key in self._data:
        val = self._data[key]
        if SparseParameter._is_supported_matrix(val):
            (data_list, name_list, hash_tuple) = SparseParameter._serialize_matrix(val)
            rename_list = ['%s%s%s' % (key, SparseParameter.IDENTIFIER, name) for name in name_list]
            is_dia = int(len(rename_list) == 4)
            store_dict[key + SparseResult.IDENTIFIER + 'is_dia'] = is_dia
            for (idx, name) in enumerate(rename_list):
                store_dict[name] = data_list[idx]
        else:
            store_dict[key] = val
    return store_dict