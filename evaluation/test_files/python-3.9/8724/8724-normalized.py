def _execute_command(function, namespace_obj, errors_file, pre_call=None):
    """
    Assumes that `function` is a callable.  Tries different approaches
    to call it (with `namespace_obj` or with ordinary signature).
    Yields the results line by line.

    If :class:`~argh.exceptions.CommandError` is raised, its message is
    appended to the results (i.e. yielded by the generator as a string).
    All other exceptions propagate unless marked as wrappable
    by :func:`wrap_errors`.
    """
    if pre_call:
        pre_call(namespace_obj)

    def _call():
        if getattr(function, ATTR_EXPECTS_NAMESPACE_OBJECT, False):
            result = function(namespace_obj)
        else:
            _flat_key = lambda key: key.replace('-', '_')
            all_input = dict(((_flat_key(k), v) for (k, v) in vars(namespace_obj).items()))
            spec = get_arg_spec(function)
            positional = [all_input[k] for k in spec.args]
            kwonly = getattr(spec, 'kwonlyargs', [])
            keywords = dict(((k, all_input[k]) for k in kwonly))
            if spec.varargs:
                positional += getattr(namespace_obj, spec.varargs)
            varkw = getattr(spec, 'varkw', getattr(spec, 'keywords', []))
            if varkw:
                not_kwargs = [DEST_FUNCTION] + spec.args + [spec.varargs] + kwonly
                for k in vars(namespace_obj):
                    if k.startswith('_') or k in not_kwargs:
                        continue
                    keywords[k] = getattr(namespace_obj, k)
            result = function(*positional, **keywords)
        if isinstance(result, (GeneratorType, list, tuple)):
            for line in result:
                yield line
        elif result is not None:
            yield result
    wrappable_exceptions = [CommandError]
    wrappable_exceptions += getattr(function, ATTR_WRAPPED_EXCEPTIONS, [])
    try:
        result = _call()
        for line in result:
            yield line
    except tuple(wrappable_exceptions) as e:
        processor = getattr(function, ATTR_WRAPPED_EXCEPTIONS_PROCESSOR, lambda e: '{0.__class__.__name__}: {0}'.format(e))
        errors_file.write(compat.text_type(processor(e)))
        errors_file.write('\n')