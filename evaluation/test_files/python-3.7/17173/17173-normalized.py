def trending_list(self, rating=None, limit=DEFAULT_SEARCH_LIMIT):
    """
        Suppose you expect the `trending` method to just give you a list rather
        than a generator. This method will have that effect. Equivalent to::

            >>> g = Giphy()
            >>> results = list(g.trending())
        """
    return list(self.trending(limit=limit, rating=rating))