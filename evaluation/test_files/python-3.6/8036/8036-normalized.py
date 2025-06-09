def delete_file(self, path):
    """
        Delete object corresponding to path.
        """
    if self.file_exists(path):
        self._delete_non_directory(path)
    elif self.dir_exists(path):
        self._delete_directory(path)
    else:
        self.no_such_entity(path)