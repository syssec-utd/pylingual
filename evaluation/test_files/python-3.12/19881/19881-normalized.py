def p_cardinality_1(self, p):
    """cardinality : NUMBER"""
    if p[1] != '1':
        raise ParsingException('illegal cardinality (%s) at %s:%d' % (p[1], p.lexer.filename, p.lineno(1)))
    p[0] = p[1]