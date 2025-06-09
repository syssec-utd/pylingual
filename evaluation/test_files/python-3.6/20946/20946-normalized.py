def seek(self, offset, whence=0):
    """
        Same as `file.seek()` but for the slice. Returns a value between
        `self.start` and `self.size` inclusive.
        
        raises:
            ValueError if the new seek position is not between 0 and
            `self.size`.
        """
    if self.closed:
        raise ValueError('I/O operation on closed file.')
    if whence == SEEK_SET:
        pos = offset
    elif whence == SEEK_CUR:
        pos = self.pos + offset
    elif whence == SEEK_END:
        pos = self.size + offset
    if not 0 <= pos <= self.size:
        raise ValueError('new position ({}) will fall outside the file slice range (0-{})'.format(pos, self.size))
    self.pos = pos
    return self.pos