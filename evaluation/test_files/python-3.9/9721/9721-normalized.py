def withIndent(self, indent=1):
    """
        Create copy of this context with increased indent
        """
    ctx = copy(self)
    ctx.indent += indent
    return ctx