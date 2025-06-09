def get_connection_file(app=None):
    """Return the path to the connection file of an app
    
    Parameters
    ----------
    app : KernelApp instance [optional]
        If unspecified, the currently running app will be used
    """
    if app is None:
        from IPython.zmq.ipkernel import IPKernelApp
        if not IPKernelApp.initialized():
            raise RuntimeError('app not specified, and not in a running Kernel')
        app = IPKernelApp.instance()
    return filefind(app.connection_file, ['.', app.profile_dir.security_dir])