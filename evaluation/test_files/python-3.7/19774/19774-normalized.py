def load_name(self, name):
    """
        Implementation of the LOAD_NAME operation
        """
    if name in self.globals_:
        return self.globals_[name]
    b = self.globals_['__builtins__']
    if isinstance(b, dict):
        return b[name]
    else:
        return getattr(b, name)