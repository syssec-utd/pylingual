def _get_objs(self):
    """A generator yielding all protobuf object data in the file. It is the
        main parser of the stream encoding.
        """
    while True:
        count = self._read_varint()
        if count == 0:
            break
        for _ in range(count):
            size = self._read_varint()
            if size == 0:
                raise EOFError('unexpected EOF.')
            yield self._fd.read(size)
        if self._group_delim:
            yield (self._delimiter() if self._delimiter is not None else None)