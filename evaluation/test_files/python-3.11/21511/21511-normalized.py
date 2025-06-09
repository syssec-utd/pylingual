def _hijack_gtk(self):
    """Hijack a few key functions in GTK for IPython integration.

        Modifies pyGTK's main and main_quit with a dummy so user code does not
        block IPython.  This allows us to use %run to run arbitrary pygtk
        scripts from a long-lived IPython session, and when they attempt to
        start or stop

        Returns
        -------
        The original functions that have been hijacked:
        - gtk.main
        - gtk.main_quit
        """

    def dummy(*args, **kw):
        pass
    orig_main, gtk.main = (gtk.main, dummy)
    orig_main_quit, gtk.main_quit = (gtk.main_quit, dummy)
    return (orig_main, orig_main_quit)