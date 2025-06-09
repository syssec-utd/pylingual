def _set_compression(self, value):
    """ May be used to compress PDF files. Code is more readable
            for testing and inspection if not compressed. Requires a boolean. """
    if isinstance(value, bool):
        self.compression = value
    else:
        raise Exception(TypeError, '%s is not a valid option for compression' % value)