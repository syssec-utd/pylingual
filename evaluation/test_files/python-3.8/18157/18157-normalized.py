def get(self, label_sn):
    """
        Get tags by a label's sn key

        :param label_sn: A corresponding label's ``sn`` key.
        :type label_sn: str or int

        :return: A list of matching tags. An empty list is returned if there are
            not any matches
        :rtype: list of dict

        :raises: This will raise a
            :class:`ServerException<logentries_api.exceptions.ServerException>`
            if there is an error from Logentries
        """
    tags = self.list()
    return [tag for tag in tags if str(label_sn) in tag.get('args', {}).values()]