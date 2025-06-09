def execute_file(self, path, hidden=False):
    """ Reimplemented to use the 'run' magic.
        """
    if sys.platform == 'win32':
        path = os.path.normpath(path).replace('\\', '/')
    if ' ' in path or "'" in path or '"' in path:
        path = '"%s"' % path.replace('"', '\\"')
    self.execute('%%run %s' % path, hidden=hidden)