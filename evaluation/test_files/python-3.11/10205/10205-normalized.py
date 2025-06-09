def get_logs(self, join_newline=True):
    """'get_logs will return the complete history, joined by newline
        (default) or as is.
        """
    if join_newline:
        return '\n'.join(self.history)
    return self.history