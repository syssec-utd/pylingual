def __sig_from_partial(self, inst):
    """Extract function signature from an existing partial instance."""
    self.pargl = list(inst.pargl)
    self.kargl = list(inst.kargl)
    self.def_argv = inst.def_argv.copy()
    self.var_pargs = inst.var_pargs
    self.var_kargs = inst.var_kargs