def _convert_pyx_sources_to_c(self):
    """convert .pyx extensions to .c"""

    def pyx_to_c(source):
        if source.endswith('.pyx'):
            source = source[:-4] + '.c'
        return source
    self.sources = map(pyx_to_c, self.sources)