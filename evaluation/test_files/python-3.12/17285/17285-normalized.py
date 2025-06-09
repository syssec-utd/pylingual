def dumps(obj):
    """
    Serializes a dictionary into ACF data.
    :param obj: A dictionary to serialize.
    :return: ACF data.
    """
    if not isinstance(obj, dict):
        raise TypeError('can only dump a dictionary as an ACF but got ' + type(obj).__name__)
    return '\n'.join(_dumps(obj, level=0)) + '\n'