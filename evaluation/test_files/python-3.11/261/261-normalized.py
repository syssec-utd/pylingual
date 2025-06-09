def _deep_string_coerce(content, json_path='json'):
    """
    Coerces content or all values of content if it is a dict to a string. The
    function will throw if content contains non-string or non-numeric types.

    The reason why we have this function is because the ``self.json`` field must be a
    dict with only string values. This is because ``render_template`` will fail
    for numerical values.
    """
    c = _deep_string_coerce
    if isinstance(content, six.string_types):
        return content
    elif isinstance(content, six.integer_types + (float,)):
        return str(content)
    elif isinstance(content, (list, tuple)):
        return [c(e, '{0}[{1}]'.format(json_path, i)) for i, e in enumerate(content)]
    elif isinstance(content, dict):
        return {k: c(v, '{0}[{1}]'.format(json_path, k)) for k, v in list(content.items())}
    else:
        param_type = type(content)
        msg = 'Type {0} used for parameter {1} is not a number or a string'.format(param_type, json_path)
        raise AirflowException(msg)