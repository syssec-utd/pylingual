def get_file(db, user_id, api_path, include_content, decrypt_func):
    """
    Get file data for the given user_id and path.

    Include content only if include_content=True.
    """
    query_fields = _file_default_fields()
    if include_content:
        query_fields.append(files.c.content)
    return _get_file(db, user_id, api_path, query_fields, decrypt_func)