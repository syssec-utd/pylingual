def register_handler(self, name, handler, esc_strings):
    """Register a handler instance by name with esc_strings."""
    self._handlers[name] = handler
    for esc_str in esc_strings:
        self._esc_handlers[esc_str] = handler