def t_GE(self, t):
    """\\>\\="""
    t.endlexpos = t.lexpos + len(t.value)
    return t