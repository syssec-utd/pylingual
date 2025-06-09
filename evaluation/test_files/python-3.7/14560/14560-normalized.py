def add_list(self, query_params=None):
    """
        Create a list for a board. Returns a new List object.
        """
    list_json = self.fetch_json(uri_path=self.base_uri + '/lists', http_method='POST', query_params=query_params or {})
    return self.create_list(list_json)