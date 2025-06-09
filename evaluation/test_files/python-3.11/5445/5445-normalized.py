def get_exception_handlers(node: astroid.node_classes.NodeNG, exception=Exception) -> List[astroid.ExceptHandler]:
    """Return the collections of handlers handling the exception in arguments.

    Args:
        node (astroid.NodeNG): A node that is potentially wrapped in a try except.
        exception (builtin.Exception or str): exception or name of the exception.

    Returns:
        list: the collection of handlers that are handling the exception or None.

    """
    context = find_try_except_wrapper_node(node)
    if isinstance(context, astroid.TryExcept):
        return [handler for handler in context.handlers if error_of_type(handler, exception)]
    return None