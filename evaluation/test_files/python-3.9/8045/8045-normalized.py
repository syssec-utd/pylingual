def directories_in_directory(db, user_id, db_dirname):
    """
    Return subdirectories of a directory.
    """
    fields = _directory_default_fields()
    rows = db.execute(select(fields).where(_is_in_directory(directories, user_id, db_dirname)))
    return [to_dict_no_content(fields, row) for row in rows]