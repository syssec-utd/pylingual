def has_source_code_tree_changed(self):
    """
        If a task succeeds & is re-run and didn't change, we might not
        want to re-run it if it depends *only* on source code
        :return:
        """
    global CURRENT_HASH
    directory = self.where
    CURRENT_HASH = dirhash(directory, 'md5', ignore_hidden=True, excluded_files=['.coverage', 'lint.txt'], excluded_extensions=['.pyc'])
    print('Searching ' + self.state_file_name)
    if os.path.isfile(self.state_file_name):
        with open(self.state_file_name, 'r+') as file:
            last_hash = file.read()
            if last_hash != CURRENT_HASH:
                file.seek(0)
                file.write(CURRENT_HASH)
                file.truncate()
                return True
            else:
                return False
    with open(self.state_file_name, 'w') as file:
        file.write(CURRENT_HASH)
        return True