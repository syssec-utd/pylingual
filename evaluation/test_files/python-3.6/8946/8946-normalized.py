def handle_pass(self, signame, set_pass):
    """Set whether we pass this signal to the program (or not)
        when this signal is caught. If set_pass is True, Dbgr should allow
        your program to see this signal.
        """
    self.sigs[signame].pass_along = set_pass
    if set_pass:
        self.sigs[signame].b_stop = False
        pass
    return set_pass