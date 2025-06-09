def set_completer_frame(self, frame=None):
    """Set the frame of the completer."""
    if frame:
        self.Completer.namespace = frame.f_locals
        self.Completer.global_namespace = frame.f_globals
    else:
        self.Completer.namespace = self.user_ns
        self.Completer.global_namespace = self.user_global_ns