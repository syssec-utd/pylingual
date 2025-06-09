def reduce_path(path):
    """Reduce absolute path to relative (if shorter) for easier readability."""
    relative_path = os.path.relpath(path)
    if len(relative_path) < len(path):
        return relative_path
    else:
        return path