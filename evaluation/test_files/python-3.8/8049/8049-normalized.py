def _file_default_fields():
    """
    Default fields returned by a file query.
    """
    return [files.c.name, files.c.created_at, files.c.parent_name]