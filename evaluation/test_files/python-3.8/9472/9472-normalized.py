def prepend_child(self, name):
    """Prepend a child element with the specified name."""
    return XMLElement(lib.lsl_prepend_child(self.e, str.encode(name)))