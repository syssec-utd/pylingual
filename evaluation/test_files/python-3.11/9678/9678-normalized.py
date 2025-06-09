def _loadFromArray(self, dtype: HdlType, bitAddr: int) -> int:
    """
        Parse HArray type to this transaction template instance

        :return: address of it's end
        """
    self.itemCnt = evalParam(dtype.size).val
    self.children = TransTmpl(dtype.elmType, 0, parent=self, origin=self.origin)
    return bitAddr + self.itemCnt * self.children.bitAddrEnd