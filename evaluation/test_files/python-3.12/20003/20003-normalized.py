def p_create_instance_event_statement_1(self, p):
    """statement : CREATE EVENT INSTANCE variable_name OF event_specification TO variable_access"""
    p[0] = CreateInstanceEventNode(variable_name=p[4], event_specification=p[6], to_variable_access=p[8])