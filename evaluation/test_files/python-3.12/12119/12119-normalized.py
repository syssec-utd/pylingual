def from_json_data(cls, json_data, check_required=True, idd_or_buffer_or_path=None):
    """
        Parameters
        ----------
        json_data: dict
            Dictionary of serialized data (text, floats, ints, ...). For more information on data structure, create an
            Epm and use to_json_data or to_json.
        check_required: boolean, default True
            If True, will raise an exception if a required field is missing. If False, not not perform any checks.
        idd_or_buffer_or_path: (expert) to load using a custom idd

        Returns
        -------
        An Epm instance.
        """
    epm = cls(idd_or_buffer_or_path=idd_or_buffer_or_path, check_required=check_required)
    epm._dev_populate_from_json_data(json_data)
    return epm