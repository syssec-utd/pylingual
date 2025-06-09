def readline(self, use_raw=None, prompt=''):
    """Read a line of input. EOFError will be raised on EOF.

        Note: some user interfaces may decide to arrange to call
        DebuggerOutput.write() first with the prompt rather than pass
        it here.. If `use_raw' is set raw_input() will be used in that
        is supported by the specific input input. If this option is
        left None as is normally expected the value from the class
        initialization is used.
        """
    if use_raw is None:
        use_raw = self.use_raw
        pass
    if use_raw:
        try:
            inp = input(prompt)
            return inp
        except ValueError:
            raise EOFError
        pass
    else:
        line = self.input.readline()
        if not line:
            raise EOFError
        return line.rstrip('\n')
    pass