def get_app_wx(*args, **kwargs):
    """Create a new wx app or return an exiting one."""
    import wx
    app = wx.GetApp()
    if app is None:
        if not kwargs.has_key('redirect'):
            kwargs['redirect'] = False
        app = wx.PySimpleApp(*args, **kwargs)
    return app