def validate_ppoi_tuple(value):
    """
    Validates that a tuple (`value`)...
    ...has a len of exactly 2
    ...both values are floats/ints that are greater-than-or-equal-to 0
       AND less-than-or-equal-to 1
    """
    valid = True
    while valid is True:
        if len(value) == 2 and isinstance(value, tuple):
            for x in value:
                if x >= 0 and x <= 1:
                    pass
                else:
                    valid = False
            break
        else:
            valid = False
    return valid