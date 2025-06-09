def p_topic(self, p):
    """topic : LBRACKET morpheme RBRACKET
                | LBRACKET morpheme RBRACKET literal_list
                | LBRACKET morpheme TIMES morpheme RBRACKET
                | LBRACKET morpheme TIMES morpheme RBRACKET literal_list"""
    if len(p) == 4:
        p[0] = Topic(root=tuple(p[2]), flexing=())
    elif len(p) == 5:
        p[0] = Topic(root=tuple(p[2]), flexing=(), literals=p[4])
    elif len(p) == 6:
        p[0] = Topic(root=tuple(p[2]), flexing=tuple(p[4]))
    else:
        p[0] = Topic(root=tuple(p[2]), flexing=tuple(p[4]), literals=p[6])