def _load(self, load_dict):
    """Loads data from `load_dict`

        Reconstruction of sparse matrices similar to the :class:`~pypet.parameter.SparseParameter`.

        """
    for key in list(load_dict.keys()):
        if key in load_dict:
            if SparseResult.IDENTIFIER in key:
                new_key = key.split(SparseResult.IDENTIFIER)[0]
                is_dia = load_dict.pop(new_key + SparseResult.IDENTIFIER + 'is_dia')
                name_list = SparseParameter._get_name_list(is_dia)
                rename_list = ['%s%s%s' % (new_key, SparseResult.IDENTIFIER, name) for name in name_list]
                data_list = [load_dict.pop(name) for name in rename_list]
                matrix = SparseParameter._reconstruct_matrix(data_list)
                self._data[new_key] = matrix
            else:
                self._data[key] = load_dict[key]