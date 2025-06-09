def activate(cls, ctxt, args):
    """
        Initialize the extensions.  This loops over each extension
        invoking its ``activate()`` method; those extensions that
        return an object are considered "activated" and will be called
        at later phases of extension processing.

        :param ctxt: An instance of ``timid.context.Context``.
        :param args: An instance of ``argparse.Namespace`` containing
                     the result of processing command line arguments.

        :returns: An instance of ``ExtensionSet``.
        """
    debugger = ExtensionDebugger('activate')
    exts = []
    for ext in cls._get_extension_classes():
        debugger(ext)
        try:
            obj = ext.activate(ctxt, args)
        except Exception:
            exc_info = sys.exc_info()
            if not debugger.__exit__(*exc_info):
                six.reraise(*exc_info)
        else:
            if obj is not None:
                exts.append(obj)
                debugger.debug(2, 'Activating extension "%s.%s"' % (ext.__module__, ext.__name__))
    return cls(exts)