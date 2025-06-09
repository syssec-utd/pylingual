def get_serialized_value(self, ref_or_index, model_name=None):
    """
        Parameters
        ----------
        ref_or_index
        external_files_mode: str, default 'path'
            'path', 'pointer'
        model_file_path: str, default None
            if external files are asked in a relative fashion, relative path will be calculated relatively to
            model_file_path if given, else current directory

        Returns
        -------
        serialized value (only basic types: string, int, float, None, ...)
        """
    index = self._table._dev_descriptor.get_field_index(ref_or_index) if isinstance(ref_or_index, str) else ref_or_index
    value = self._data.get(index)
    value = value.serialize() if isinstance(value, (Link, RecordHook)) else value
    if isinstance(value, ExternalFile):
        value = os.path.join(get_external_files_dir_name(model_name=model_name), value.naive_short_ref)
    return value