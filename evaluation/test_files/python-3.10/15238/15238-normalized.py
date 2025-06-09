def transform(config):
    """
    Run in transform mode.

    """
    if transform_possible:
        ExampleLoader.register()
        (args, sys.argv[1:]) = (sys.argv[1:], config.args)
        try:
            return runpy.run_path(config.runner, run_name='__main__')
        finally:
            sys.argv[1:] = args