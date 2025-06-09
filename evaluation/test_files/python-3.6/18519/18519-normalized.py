def read_hex_integer(self) -> bool:
    """
    read a hexadecimal number
    Read the following BNF rule else return False::

        readHexInteger = [
            [ '0'..'9' | 'a'..'f' | 'A'..'F' ]+
        ]
    """
    if self.read_eof():
        return False
    self._stream.save_context()
    c = self._stream.peek_char
    if c.isdigit() or ('a' <= c.lower() and c.lower() <= 'f'):
        self._stream.incpos()
        while not self.read_eof():
            c = self._stream.peek_char
            if not (c.isdigit() or ('a' <= c.lower() and c.lower() <= 'f')):
                break
            self._stream.incpos()
        return self._stream.validate_context()
    return self._stream.restore_context()