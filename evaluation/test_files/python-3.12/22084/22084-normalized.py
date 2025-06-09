def object_to_primitive(obj):
    """
    convert object to primitive type so we can serialize it to data format like python.

    all primitive types: dict, list, int, float, bool, str, None
    """
    if obj is None:
        return obj
    if isinstance(obj, (int, float, bool, str)):
        return obj
    if isinstance(obj, (list, frozenset, set)):
        return [object_to_primitive(x) for x in obj]
    if isinstance(obj, dict):
        return dict([(object_to_primitive(k), object_to_primitive(v)) for k, v in obj.items()])
    data = vars(obj)
    assert isinstance(data, dict)
    return object_to_primitive(data)