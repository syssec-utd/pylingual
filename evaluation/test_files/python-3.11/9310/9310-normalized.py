def normalize_dict(dict_):
    """
    Replaces all values that are single-item iterables with the value of its
    index 0.

    :param dict dict_:
        Dictionary to normalize.

    :returns:
        Normalized dictionary.

    """
    return dict([(k, v[0] if not isinstance(v, str) and len(v) == 1 else v) for k, v in list(dict_.items())])