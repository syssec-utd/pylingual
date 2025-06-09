def set_positional_info(node, p):
    """
    set positional information on a node
    """
    node.position = Position()
    node.position.label = p.lexer.label
    node.position.start_stream = p.lexpos(1)
    node.position.start_line = p.lineno(1)
    node.position.start_column = find_column(p.lexer.lexdata, node.position.start_stream)
    (_, node.position.end_stream) = p.lexspan(len(p) - 1)
    (_, node.position.end_line) = p.linespan(len(p) - 1)
    node.position.end_column = find_column(p.lexer.lexdata, node.position.end_stream) - 1
    node.character_stream = p.lexer.lexdata[node.position.start_stream:node.position.end_stream]