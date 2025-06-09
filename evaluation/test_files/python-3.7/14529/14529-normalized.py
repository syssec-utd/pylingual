def get_list_information(self, query_params=None):
    """
        Get information for this list. Returns a dictionary of values.
        """
    return self.fetch_json(uri_path=self.base_uri, query_params=query_params or {})