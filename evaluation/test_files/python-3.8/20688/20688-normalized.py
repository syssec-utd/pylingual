def _processor(args):
    """
    A ``cli_tools`` processor function that interfaces between the
    command line and the ``timid()`` function.  This function is
    responsible for allocating a ``timid.context.Context`` object and
    initializing the activated extensions, and for calling those
    extensions' ``finalize()`` method.

    :param args: The ``argparse.Namespace`` object containing the
                 results of argument processing.
    """
    args.ctxt = context.Context(args.verbose, args.debug, args.directory)
    args.exts = extensions.ExtensionSet.activate(args.ctxt, args)
    args.ctxt.environment.update(args.environment)
    args.ctxt.variables.update(args.variables)
    try:
        result = (yield)
    except Exception as exc:
        if args.debug:
            traceback.print_exc(file=sys.stderr)
        result = exc
    result = args.exts.finalize(args.ctxt, result)
    if isinstance(result, Exception):
        result = str(result)
    yield result