def _get_arg(argname, args, kwargs):
    """
    Get an argument, either from kwargs or from the first entry in args.
    Raises a TypeError if argname not in kwargs and len(args) == 0.

    Mutates kwargs in place if the value is found in kwargs.
    """
    try:
        return (kwargs.pop(argname), args)
    except KeyError:
        pass
    try:
        return (args[0], args[1:])
    except IndexError:
        raise TypeError('No value passed for %s' % argname)