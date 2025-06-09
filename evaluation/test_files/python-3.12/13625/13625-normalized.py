def parse_param(param, include_desc=False):
    """Parse a single typed parameter statement."""
    param_def, _colon, desc = param.partition(':')
    if not include_desc:
        desc = None
    else:
        desc = desc.lstrip()
    if _colon == '':
        raise ValidationError('Invalid parameter declaration in docstring, missing colon', declaration=param)
    param_name, _space, param_type = param_def.partition(' ')
    if len(param_type) < 2 or param_type[0] != '(' or param_type[-1] != ')':
        raise ValidationError('Invalid parameter type string not enclosed in ( ) characters', param_string=param_def, type_string=param_type)
    param_type = param_type[1:-1]
    return (param_name, ParameterInfo(param_type, [], desc))