def init_virtualenv(self):
    """Add a virtualenv to sys.path so the user can import modules from it.
        This isn't perfect: it doesn't use the Python interpreter with which the
        virtualenv was built, and it ignores the --no-site-packages option. A
        warning will appear suggesting the user installs IPython in the
        virtualenv, but for many cases, it probably works well enough.
        
        Adapted from code snippets online.
        
        http://blog.ufsoft.org/2009/1/29/ipython-and-virtualenv
        """
    if 'VIRTUAL_ENV' not in os.environ:
        return
    if sys.executable.startswith(os.environ['VIRTUAL_ENV']):
        return
    warn('Attempting to work in a virtualenv. If you encounter problems, please install IPython inside the virtualenv.\n')
    if sys.platform == 'win32':
        virtual_env = os.path.join(os.environ['VIRTUAL_ENV'], 'Lib', 'site-packages')
    else:
        virtual_env = os.path.join(os.environ['VIRTUAL_ENV'], 'lib', 'python%d.%d' % sys.version_info[:2], 'site-packages')
    import site
    sys.path.insert(0, virtual_env)
    site.addsitedir(virtual_env)