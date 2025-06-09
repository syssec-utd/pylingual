def _restore_replace(self):
    """
        Check if we need to replace ".gitignore" to ".keep".

        :return: The replacement status.
        :rtype: bool
        """
    if PyFunceble.path.isdir(self.base + '.git'):
        if 'PyFunceble' not in Command('git remote show origin').execute():
            return True
        return False
    return True