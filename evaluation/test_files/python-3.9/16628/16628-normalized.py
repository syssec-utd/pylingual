def __sig_from_func(self, func):
    """Extract function signature, default arguments, keyword-only
        arguments, and whether or not variable positional or keyword
        arguments are allowed.  This also supports calling unbound instance
        methods by passing an object instance as the first argument;
        however, unbound classmethod and staticmethod objects are not
        callable, so we do not attempt to support them here."""
    if isinstance(func, types.MethodType):
        argspec = getfullargspec(func.__func__)
        self.pargl = argspec[0][1:]
    else:
        argspec = getfullargspec(func)
        self.pargl = argspec[0][:]
    if argspec[3] is not None:
        def_offset = len(self.pargl) - len(argspec[3])
        self.def_argv = dict(((self.pargl[def_offset + i], argspec[3][i]) for i in range(len(argspec[3]))))
    else:
        self.def_argv = {}
    self.var_pargs = argspec[1] is not None
    self.var_kargs = argspec[2] is not None
    self.kargl = argspec[4]
    if argspec[5] is not None:
        self.def_argv.update(argspec[5])