def read(self, f):
    """Read data from file-like object"""
    magic = f.read(len(self.magic))
    if not magic:
        return None
    if magic != self.magic:
        raise ValueError('Magic bytes not found! Read data: {}'.format(magic))
    header = self.header._make(self.header_struct.unpack(f.read(self.header_struct.size)))
    pwr_array = numpy.fromstring(f.read(header.size), dtype='float32')
    return (header, pwr_array)