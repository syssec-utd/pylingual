def getBusWordBitRange(self) -> Tuple[int, int]:
    """
        :return: bit range which contains data of this part on bus data signal
        """
    offset = self.startOfPart % self.parent.wordWidth
    return (offset + self.bit_length(), offset)