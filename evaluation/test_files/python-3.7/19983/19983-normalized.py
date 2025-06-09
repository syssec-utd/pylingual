def t_DOT(self, t):
    """\\."""
    t.endlexpos = t.lexpos + len(t.value)
    return t