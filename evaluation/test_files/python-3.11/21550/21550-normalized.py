def schema_validate(instance, schema, exc_class, *prefix, **kwargs):
    """
    Schema validation helper.  Performs JSONSchema validation.  If a
    schema validation error is encountered, an exception of the
    designated class is raised with the validation error message
    appropriately simplified and passed as the sole positional
    argument.

    :param instance: The object to schema validate.
    :param schema: The schema to use for validation.
    :param exc_class: The exception class to raise instead of the
                      ``jsonschema.ValidationError`` exception.
    :param prefix: Positional arguments are interpreted as a list of
                   keys to prefix to the path contained in the
                   validation error.
    :param kwargs: Keyword arguments to pass to the exception
                   constructor.
    """
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as exc:
        path = '/'.join((a if isinstance(a, six.string_types) else '[%d]' % a for a in itertools.chain(prefix, exc.path)))
        message = 'Failed to validate "%s": %s' % (path, exc.message)
        raise exc_class(message, **kwargs)