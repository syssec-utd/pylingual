def next_token(self) -> str:
    """Advance the stream forward by one character and return the
        next token in the stream."""
    if self._idx < StreamReader.DEFAULT_INDEX:
        self._idx += 1
    else:
        c = self._stream.read(1)
        self._update_loc(c)
        self._buffer.append(c)
    return self.peek()