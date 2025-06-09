def p_unrelate_statement_2(self, p):
    """statement : UNRELATE instance_name FROM instance_name ACROSS rel_id DOT phrase"""
    p[0] = UnrelateNode(from_variable_name=p[2], to_variable_name=p[4], rel_id=p[6], phrase=p[8])