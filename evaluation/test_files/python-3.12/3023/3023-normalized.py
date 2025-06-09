def decodePeek(self, data):
    """Find which symbol index matches the given data (from peek, as a number)
        and return the number of bits decoded.
        Can also be used to figure out length of a symbol.
        """
    return (self.maxLength, Symbol(self, data & (1 << self.maxLength) - 1))