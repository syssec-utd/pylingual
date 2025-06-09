def areSameHVals(a: Union[None, List[Value]], b: Union[None, List[Value]]) -> bool:
    """
    :return: True if two vectors of Value instances are same
    :note: not just equal
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    if len(a) == len(b):
        for a_, b_ in zip(a, b):
            if not isSameHVal(a_, b_):
                return False
        return True
    else:
        return False