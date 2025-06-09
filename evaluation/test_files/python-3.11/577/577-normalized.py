def _bind_parameters(operation, parameters):
    """ Helper method that binds parameters to a SQL query. """
    string_parameters = {}
    for name, value in iteritems(parameters):
        if value is None:
            string_parameters[name] = 'NULL'
        elif isinstance(value, basestring):
            string_parameters[name] = "'" + _escape(value) + "'"
        else:
            string_parameters[name] = str(value)
    return operation % string_parameters