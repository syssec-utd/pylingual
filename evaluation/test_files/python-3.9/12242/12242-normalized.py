def get_group_by_id(self, group_id):
    """
        Returns a restclients.Group object for the group identified by the
        passed group ID.
        """
    self._valid_group_id(group_id)
    url = '{}/group/{}'.format(self.API, group_id)
    data = self._get_resource(url)
    return self._group_from_json(data.get('data'))