def get_items(self, query_params=None):
    """
        Get all the items for this label. Returns a list of dictionaries.
        Each dictionary has the values for an item.
        """
    return self.fetch_json(uri_path=self.base_uri + '/checkItems', query_params=query_params or {})