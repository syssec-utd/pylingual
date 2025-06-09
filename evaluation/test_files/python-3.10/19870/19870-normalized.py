def t_CARDINALITY(self, t):
    """(1C)"""
    t.endlexpos = t.lexpos + len(t.value)
    return t