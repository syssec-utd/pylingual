def save(self):
    """Write changed .pth file back to disk"""
    if not self.dirty:
        return
    data = '\n'.join(map(self.make_relative, self.paths))
    if data:
        log.debug('Saving %s', self.filename)
        data = "import sys; sys.__plen = len(sys.path)\n%s\nimport sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)\n" % data
        if os.path.islink(self.filename):
            os.unlink(self.filename)
        f = open(self.filename, 'wt')
        f.write(data)
        f.close()
    elif os.path.exists(self.filename):
        log.debug('Deleting empty %s', self.filename)
        os.unlink(self.filename)
    self.dirty = False