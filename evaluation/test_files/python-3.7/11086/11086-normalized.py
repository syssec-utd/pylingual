def format_name(self, format_name):
    """Set the default format name.

        :param str format_name: The display format name.
        :raises ValueError: if the format is not recognized.

        """
    if format_name in self.supported_formats:
        self._format_name = format_name
    else:
        raise ValueError('unrecognized format_name "{}"'.format(format_name))