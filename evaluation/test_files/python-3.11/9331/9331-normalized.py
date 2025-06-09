def is_binary_string(content):
    """
        Return true if string is binary data.
        """
    textchars = bytearray([7, 8, 9, 10, 12, 13, 27]) + bytearray(range(32, 256))
    return bool(content.translate(None, textchars))