def remove_child(self, rhs):
    """Remove a given child element, specified by name or as element."""
    if type(rhs) is XMLElement:
        lib.lsl_remove_child(self.e, rhs.e)
    else:
        lib.lsl_remove_child_n(self.e, rhs)