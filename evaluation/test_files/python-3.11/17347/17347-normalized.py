def delete(self, filename=None):
    """Remove tags from a file."""
    if self.tags is not None:
        if filename is None:
            filename = self.filename
        else:
            warnings.warn('delete(filename=...) is deprecated, reload the file', DeprecationWarning)
        return self.tags.delete(filename)