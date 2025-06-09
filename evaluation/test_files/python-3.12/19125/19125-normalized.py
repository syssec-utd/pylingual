def p_function_call(p):
    """
    FunctionCall : NAME FormalArguments
    """
    if p[1] in ('node', 'text'):
        p[0] = ast.NodeType(p[1])
    else:
        p[0] = ast.FunctionCall(p[1], p[2])