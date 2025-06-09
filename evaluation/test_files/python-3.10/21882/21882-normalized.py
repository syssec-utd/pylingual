def show_all(self):
    """Show entire demo on screen, block by block"""
    fname = self.title
    title = self.title
    nblocks = self.nblocks
    silent = self._silent
    marquee = self.marquee
    for (index, block) in enumerate(self.src_blocks_colored):
        if silent[index]:
            (print >> io.stdout, marquee('<%s> SILENT block # %s (%s remaining)' % (title, index, nblocks - index - 1)))
        else:
            (print >> io.stdout, marquee('<%s> block # %s (%s remaining)' % (title, index, nblocks - index - 1)))
        (print >> io.stdout, block)
    sys.stdout.flush()