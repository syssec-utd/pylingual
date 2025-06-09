def to_fmt(self) -> fmt.indentable:
    """
        Return an Fmt representation for pretty-printing
        """
    lsb = []
    if len(self._lsig) > 0:
        for s in self._lsig:
            lsb.append(s.to_fmt())
    block = fmt.block('(', ')', fmt.sep(', ', lsb))
    qual = 'tuple'
    txt = fmt.sep('', [qual, block])
    return txt