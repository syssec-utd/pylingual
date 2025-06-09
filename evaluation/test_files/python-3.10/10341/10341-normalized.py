def configure(backends, raise_errors=False):
    """Instantiate and configures backends.

    :arg list-of-dicts backends: the backend configuration as a list of dicts where
        each dict specifies a separate backend.

        Each backend dict consists of two things:

        1. ``class`` with a value that is either a Python class or a dotted
           Python path to one

        2. ``options`` dict with options for the backend in question to
           configure it

        See the documentation for the backends you're using to know what is
        configurable in the options dict.

    :arg raise_errors bool: whether or not to raise an exception if something
        happens in configuration; if it doesn't raise an exception, it'll log
        the exception

    For example, this sets up a
    :py:class:`markus.backends.logging.LoggingMetrics` backend::

        markus.configure([
            {
                'class': 'markus.backends.logging.LoggingMetrics',
                'options': {
                    'logger_name': 'metrics'
                }
            }
        ])


    You can set up as many backends as you like.

    .. Note::

       During application startup, Markus should get configured before the app
       starts generating metrics. Any metrics generated before Markus is
       configured will get dropped.

       However, anything can call :py:func:`markus.get_metrics` and get a
       :py:class:`markus.main.MetricsInterface` before Markus has been
       configured including at module load time.

    """
    good_backends = []
    for backend in backends:
        clspath = backend['class']
        options = backend.get('options', {})
        if isinstance(clspath, str):
            (modpath, clsname) = split_clspath(clspath)
            try:
                __import__(modpath)
                module = sys.modules[modpath]
                cls = getattr(module, clsname)
            except Exception:
                logger.exception('Exception while importing %s', clspath)
                if raise_errors:
                    raise
                continue
        else:
            cls = clspath
        try:
            good_backends.append(cls(options))
        except Exception:
            logger.exception('Exception thrown while instantiating %s, %s', clspath, options)
            if raise_errors:
                raise
    _change_metrics(good_backends)