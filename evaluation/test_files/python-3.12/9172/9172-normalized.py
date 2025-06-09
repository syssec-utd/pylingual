def log_shapes(logger):
    """
    Decorator to log the shapes of input and output dataframes

    It considers all the dataframes passed either as arguments or keyword arguments as inputs
    and all the dataframes returned as outputs.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            input_shapes = _get_dfs_shapes(*args, **kwargs)
            result = func(*args, **kwargs)
            output_shapes = _get_dfs_shapes(result)
            _log_shapes(logger, func.__name__, input_shapes, output_shapes)
            return result
        return wrapper
    return decorator