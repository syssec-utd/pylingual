def copy(self):
    """
        Returns a new CLIContext instance that is a shallow copy of
        the original, much like dict's copy method.
        """
    context = CLIContext()
    for item in dir(self):
        if item[0] != '_' and item not in ('copy', 'write_headers'):
            setattr(context, item, getattr(self, item))
    return context