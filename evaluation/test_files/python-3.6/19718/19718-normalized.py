def descovery(testdir):
    """Descover and load greencard tests."""
    from os.path import join, exists, isdir, splitext, basename, sep
    if not testdir or not exists(testdir) or (not isdir(testdir)):
        return None
    from os import walk
    import fnmatch
    import imp
    for (root, _, filenames) in walk(testdir):
        for filename in fnmatch.filter(filenames, '*.py'):
            path = join(root, filename)
            modulepath = splitext(root)[0].replace(sep, '.')
            imp.load_source(modulepath, path)