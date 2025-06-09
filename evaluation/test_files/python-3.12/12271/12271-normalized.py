def exit(self, status=0, msg=None):
    """
        Immediately exits Python with the given status (or 0) as the
        exit code and optionally outputs the msg using self.error.
        """
    if msg:
        self.error(msg)
    sys.exit(status)