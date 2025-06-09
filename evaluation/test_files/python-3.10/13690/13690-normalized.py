def func(self, f, state):
    """Intended to be overridden by subclasses. Raises
        NotImplementedError."""
    message = 'Tried to use unimplemented lens {}.'
    raise NotImplementedError(message.format(type(self)))