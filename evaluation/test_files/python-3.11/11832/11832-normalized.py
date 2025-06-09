def make_rr_subparser(subparsers, rec_type, args_and_types):
    """
    Make a subparser for a given type of DNS record
    """
    sp = subparsers.add_parser(rec_type)
    sp.add_argument('name', type=str)
    sp.add_argument('ttl', type=int, nargs='?')
    sp.add_argument(rec_type, type=str)
    for my_spec in args_and_types:
        argname, argtype = my_spec[:2]
        if len(my_spec) > 2:
            nargs = my_spec[2]
            sp.add_argument(argname, type=argtype, nargs=nargs)
        else:
            sp.add_argument(argname, type=argtype)
    return sp