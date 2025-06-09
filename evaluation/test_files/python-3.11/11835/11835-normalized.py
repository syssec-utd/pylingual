def serialize(tokens):
    """
    Serialize tokens:
    * quote whitespace-containing tokens
    * escape semicolons
    """
    ret = []
    for tok in tokens:
        if ' ' in tok:
            tok = '"%s"' % tok
        if ';' in tok:
            tok = tok.replace(';', '\\;')
        ret.append(tok)
    return ' '.join(ret)