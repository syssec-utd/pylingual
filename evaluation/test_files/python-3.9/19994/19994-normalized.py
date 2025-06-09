def p_statement_list_1(self, p):
    """statement_list : statement SEMICOLON statement_list"""
    p[0] = p[3]
    if p[1] is not None:
        p[0].children.insert(0, p[1])