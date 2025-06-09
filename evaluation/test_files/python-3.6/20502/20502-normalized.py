def last_error(self):
    """Get the output of the last command exevuted."""
    if not len(self.log):
        raise RuntimeError('Nothing executed')
    try:
        errs = [l for l in self.log if l[1] != 0]
        return errs[-1][2]
    except IndexError:
        return 'no last error'