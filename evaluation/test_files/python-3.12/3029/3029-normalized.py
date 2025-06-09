def readTuple(self, stream):
    """Read symbol from stream. Returns symbol, length.
        """
    length, symbol = self.decodePeek(stream.peek(self.maxLength))
    stream.pos += length
    return (length, symbol)