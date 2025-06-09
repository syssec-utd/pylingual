def _sort_versions(self, applicable_versions):
    """
        Bring the latest version (and wheels) to the front, but maintain the
        existing ordering as secondary. See the docstring for `_link_sort_key`
        for details. This function is isolated for easier unit testing.
        """
    return sorted(applicable_versions, key=self._candidate_sort_key, reverse=True)