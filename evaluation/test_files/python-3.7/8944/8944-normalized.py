def handle_print_stack(self, signame, print_stack):
    """Set whether we stop or not when this signal is caught.
        If 'set_stop' is True your program will stop when this signal
        happens."""
    self.sigs[signame].print_stack = print_stack
    return print_stack