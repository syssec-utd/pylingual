def peek_text(self, text: str) -> bool:
    """Same as readText but doesn't consume the stream."""
    start = self._stream.index
    stop = start + len(text)
    if stop > self._stream.eos_index:
        return False
    return self._stream[self._stream.index:stop] == text