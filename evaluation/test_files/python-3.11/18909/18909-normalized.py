def try_convert(value):
    """Convert value to a numeric value or raise a ValueError
        if that isn't possible.

        """
    convertible = ForceNumeric.is_convertible(value)
    if not convertible or isinstance(value, bool):
        raise ValueError
    if isinstance(str(value), str):
        return ForceNumeric.str_to_num(value)
    return float(value)