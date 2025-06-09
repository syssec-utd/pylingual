def get_version():
    """ str: The package version. """
    global_vars = {}
    source = read(os.path.join('capybara', 'version.py'))
    code = compile(source, 'version.py', 'exec')
    exec(code, global_vars)
    return global_vars['__version__']