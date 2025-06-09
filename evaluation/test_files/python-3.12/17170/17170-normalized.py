def search_list(self, term=None, phrase=None, limit=DEFAULT_SEARCH_LIMIT, rating=None):
    """
        Suppose you expect the `search` method to just give you a list rather
        than a generator. This method will have that effect. Equivalent to::

            >>> g = Giphy()
            >>> results = list(g.search('foo'))
        """
    return list(self.search(term=term, phrase=phrase, limit=limit, rating=rating))