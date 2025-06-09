def _managers_changed(self, name, old, new):
    """
        Strip slashes from directories before updating.
        """
    for key in new:
        if '/' in key:
            raise ValueError('Expected directory names w/o slashes.  Got [%s]' % key)
        self.managers = {k.strip('/'): v for k, v in new.items()}