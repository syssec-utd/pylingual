def update_board(self, query_params=None):
    """
        Update this board's information. Returns a new board.
        """
    board_json = self.fetch_json(uri_path=self.base_uri, http_method='PUT', query_params=query_params or {})
    return self.create_board(board_json)