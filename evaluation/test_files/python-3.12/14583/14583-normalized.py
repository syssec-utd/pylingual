def get_board(self, id, name=None):
    """
        Get a board

        Returns:
            Board: The board with the given `id`
        """
    return self.create_board(dict(id=id, name=name))