def reload(self):
    """Reload source from disk and initialize state."""
    self.fload()
    lines = self.fobj.readlines()
    src_b = [l for l in lines if l.strip()]
    nblocks = len(src_b)
    self.src = ''.join(lines)
    self._silent = [False] * nblocks
    self._auto = [True] * nblocks
    self.auto_all = True
    self.nblocks = nblocks
    self.src_blocks = src_b
    self.src_blocks_colored = map(self.ip_colorize, self.src_blocks)
    self.reset()