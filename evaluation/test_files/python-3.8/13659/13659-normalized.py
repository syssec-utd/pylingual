def find_all(container):
    """Find all annotated function inside of a container.

    Annotated functions are identified as those that:
    - do not start with a _ character
    - are either annotated with metadata
    - or strings that point to lazily loaded modules

    Args:
        container (object): The container to search for annotated functions.

    Returns:
        dict: A dict with all of the found functions in it.
    """
    if isinstance(container, dict):
        names = container.keys()
    else:
        names = dir(container)
    built_context = BasicContext()
    for name in names:
        if name.startswith('_'):
            continue
        if isinstance(container, dict):
            obj = container[name]
        else:
            obj = getattr(container, name)
        if isinstance(container, dict) and isinstance(obj, str):
            built_context[name] = obj
        elif hasattr(obj, 'metadata') and isinstance(getattr(obj, 'metadata'), AnnotatedMetadata):
            built_context[name] = obj
    return built_context