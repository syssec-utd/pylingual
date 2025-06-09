def get_first_name_last_name(self):
    """
        :rtype: str
        """
    names = []
    if self._get_first_names():
        names += self._get_first_names()
    if self._get_additional_names():
        names += self._get_additional_names()
    if self._get_last_names():
        names += self._get_last_names()
    if names:
        return helpers.list_to_string(names, ' ')
    else:
        return self.get_full_name()