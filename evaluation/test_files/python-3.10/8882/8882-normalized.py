def readline(self, use_raw=None, prompt=''):
    """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting"""
    if self.closed:
        raise ValueError
    if 0 == len(self.input):
        self.closed = True
        raise EOFError
    line = self.input[0]
    del self.input[0]
    return line