def walkFlatten(self, offset: int=0, shouldEnterFn=_default_shouldEnterFn, otherObjItCtx: ObjIteratorCtx=_DummyIteratorCtx()) -> Generator[Union[Tuple[Tuple[int, int], 'TransTmpl'], 'OneOfTransaction'], None, None]:
    """
        Walk fields in instance of TransTmpl

        :param offset: optional offset for all children in this TransTmpl
        :param shouldEnterFn: function (transTmpl) which returns True
            when field should be split on it's children
        :param shouldEnterFn: function(transTmpl) which should return
            (shouldEnter, shouldUse) where shouldEnter is flag that means
            iterator should look inside of this actual object
            and shouldUse flag means that this field should be used
            (=generator should yield it)
        :return: generator of tuples ((startBitAddress, endBitAddress),
            TransTmpl instance)
        """
    t = self.dtype
    base = self.bitAddr + offset
    end = self.bitAddrEnd + offset
    shouldEnter, shouldYield = shouldEnterFn(self)
    if shouldYield:
        yield ((base, end), self)
    if shouldEnter:
        if isinstance(t, Bits):
            pass
        elif isinstance(t, HStruct):
            for ch in self.children:
                with otherObjItCtx(ch.origin.name):
                    yield from ch.walkFlatten(offset, shouldEnterFn, otherObjItCtx)
        elif isinstance(t, HArray):
            itemSize = (self.bitAddrEnd - self.bitAddr) // self.itemCnt
            for i in range(self.itemCnt):
                with otherObjItCtx(i):
                    yield from self.children.walkFlatten(base + i * itemSize, shouldEnterFn, otherObjItCtx)
        elif isinstance(t, HUnion):
            yield OneOfTransaction(self, offset, shouldEnterFn, self.children)
        elif isinstance(t, HStream):
            assert len(self.children) == 1
            yield StreamTransaction(self, offset, shouldEnterFn, self.children[0])
        else:
            raise TypeError(t)