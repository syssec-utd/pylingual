def splitOnWords(self, transaction, addrOffset=0):
    """
        :return: generator of TransPart instance
        """
    wordWidth = self.wordWidth
    end = addrOffset
    for tmp in transaction.walkFlatten(offset=addrOffset):
        if isinstance(tmp, OneOfTransaction):
            split = [self.splitOnWords(ch, end) for ch in tmp.possibleTransactions]
            yield from groupIntoChoices(split, wordWidth, tmp)
            end = addrOffset + tmp.possibleTransactions[0].bitAddrEnd
        elif isinstance(tmp, StreamTransaction):
            ch_len = tmp.child.bit_length()
            if end % self.wordWidth != 0 or ch_len != self.wordWidth:
                raise NotImplementedError(tmp)
            else:
                s = StreamOfFramePars(end, tmp)
                s.extend(self.splitOnWords(tmp.child, end))
                s.setIsLast(True)
                s.resolveEnd()
                yield s
                end = addrOffset + tmp.child.bitAddrEnd
        else:
            (base, end), tmpl = tmp
            startOfPart = base
            while startOfPart != end:
                wordIndex = startOfPart // wordWidth
                endOfWord = (wordIndex + 1) * wordWidth
                endOfPart = min(endOfWord, end)
                inFieldOffset = startOfPart - base
                yield TransPart(self, tmpl, startOfPart, endOfPart, inFieldOffset)
                startOfPart = endOfPart