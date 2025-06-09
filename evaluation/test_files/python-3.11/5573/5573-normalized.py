def preprocess_options(args, search_for):
    """look for some options (keys of <search_for>) which have to be processed
    before others

    values of <search_for> are callback functions to call when the option is
    found
    """
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('--'):
            try:
                option, val = arg[2:].split('=', 1)
            except ValueError:
                option, val = (arg[2:], None)
            try:
                cb, takearg = search_for[option]
            except KeyError:
                i += 1
            else:
                del args[i]
                if takearg and val is None:
                    if i >= len(args) or args[i].startswith('-'):
                        msg = 'Option %s expects a value' % option
                        raise ArgumentPreprocessingError(msg)
                    val = args[i]
                    del args[i]
                elif not takearg and val is not None:
                    msg = "Option %s doesn't expects a value" % option
                    raise ArgumentPreprocessingError(msg)
                cb(option, val)
        else:
            i += 1