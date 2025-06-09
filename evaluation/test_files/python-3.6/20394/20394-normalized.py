def set_autoindent(self, value=None):
    """Set the autoindent flag, checking for readline support.

        If called with no arguments, it acts as a toggle."""
    if value != 0 and (not self.has_readline):
        if os.name == 'posix':
            warn('The auto-indent feature requires the readline library')
        self.autoindent = 0
        return
    if value is None:
        self.autoindent = not self.autoindent
    else:
        self.autoindent = value