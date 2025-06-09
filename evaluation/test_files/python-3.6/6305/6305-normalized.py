def check_list(var, num_terms):
    """ Check if a variable is a list and is the correct length.

    If variable is not a list it will make it a list of the correct length with
    all terms identical.
    """
    if not isinstance(var, list):
        if isinstance(var, tuple):
            var = list(var)
        else:
            var = [var]
        for _ in range(1, num_terms):
            var.append(var[0])
    if len(var) != num_terms:
        print('"%s" has the wrong number of terms; it needs %s. Exiting ...' % (var, num_terms))
        sys.exit(1)
    return var