def flush(self, filename=None):
    """        Flush current stat to file        """
    if not filename:
        filename = self.file
    if filename:
        with open(filename, 'w') as handle:
            self.config.write(handle)