def _list(api_list_class, arg_namespace, **extra):
    """ A common function for building methods of the "list showing".
    """
    if arg_namespace.starting_point:
        ordering_field = (arg_namespace.ordering or '').lstrip('-')
        if ordering_field in ('', 'datetime_uploaded', 'datetime_created'):
            arg_namespace.starting_point = parser.parse(arg_namespace.starting_point)
    items = api_list_class(starting_point=arg_namespace.starting_point, ordering=arg_namespace.ordering, limit=arg_namespace.limit, request_limit=arg_namespace.request_limit, **extra)
    items.constructor = lambda x: x
    try:
        pprint(list(items))
    except ValueError as e:
        print(e)