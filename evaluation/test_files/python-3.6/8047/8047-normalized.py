def _file_where(user_id, api_path):
    """
    Return a WHERE clause matching the given API path and user_id.
    """
    (directory, name) = split_api_filepath(api_path)
    return and_(files.c.name == name, files.c.user_id == user_id, files.c.parent_name == directory)