def _prepare_data_payload(data):
    """
        Make a copy of the `data` object, preparing it to be sent to the server.

        The data will be sent via x-www-form-urlencoded or multipart/form-data mechanisms. Both of them work with
        plain lists of key/value pairs, so this method converts the data into such format.
        """
    if not data:
        return None
    res = {}
    for (key, value) in viewitems(data):
        if value is None:
            continue
        if isinstance(value, list):
            value = stringify_list(value)
        elif isinstance(value, dict):
            if '__meta' in value and value['__meta']['schema_name'].endswith('KeyV3'):
                value = value['name']
            else:
                value = stringify_dict(value)
        else:
            value = str(value)
        res[key] = value
    return res