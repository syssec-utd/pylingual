def dispatch_command(function, *args, **kwargs):
    """
    A wrapper for :func:`dispatch` that creates a one-command parser.
    Uses :attr:`PARSER_FORMATTER`.

    This::

        dispatch_command(foo)

    ...is a shortcut for::

        parser = ArgumentParser()
        set_default_command(parser, foo)
        dispatch(parser)

    This function can be also used as a decorator.
    """
    parser = argparse.ArgumentParser(formatter_class=PARSER_FORMATTER)
    set_default_command(parser, function)
    dispatch(parser, *args, **kwargs)