def _get_all_positional_parameter_names(fn):
    """Returns the names of all positional arguments to the given function."""
    arg_spec = _get_cached_arg_spec(fn)
    args = arg_spec.args
    if arg_spec.defaults:
        args = args[:-len(arg_spec.defaults)]
    return args