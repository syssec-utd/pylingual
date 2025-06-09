def _parse_validators(valids):
    """Parse a list of validator names or n-tuples, checking for errors.

    Returns:
        list((func_name, [args...])): A list of validator function names and a
            potentially empty list of optional parameters for each function.
    """
    outvals = []
    for val in valids:
        if isinstance(val, str):
            args = []
        elif len(val) > 1:
            args = val[1:]
            val = val[0]
        else:
            raise ValidationError('You must pass either an n-tuple or a string to define a validator', validator=val)
        name = 'validate_%s' % str(val)
        outvals.append((name, args))
    return outvals