def default_option(self, fn, optstr):
    """Make an entry in the options_table for fn, with value optstr"""
    if fn not in self.lsmagic():
        error('%s is not a magic function' % fn)
    self.options_table[fn] = optstr