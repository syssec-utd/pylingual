def queryGitHubFromFile(self, filePath, gitvars={}, verbosity=0, **kwargs):
    """Submit a GitHub GraphQL query from a file.

        Can only be used with GraphQL queries.
        For REST queries, see the 'queryGitHub' method.

        Args:
            filePath (str): A relative or absolute path to a file containing
                a GraphQL query.
                File may use comments and multi-line formatting.
                .. _GitHub GraphQL Explorer:
                   https://developer.github.com/v4/explorer/
            gitvars (Optional[Dict]): All query variables.
                Defaults to empty.
                GraphQL Only.
            verbosity (Optional[int]): Changes output verbosity levels.
                If < 0, all extra printouts are suppressed.
                If == 0, normal print statements are displayed.
                If > 0, additional status print statements are displayed.
                Defaults to 0.
            **kwargs: Keyword arguments for the 'queryGitHub' method.

        Returns:
            Dict: A JSON style dictionary.

        """
    gitquery = self._readGQL(filePath, verbose=verbosity >= 0)
    return self.queryGitHub(gitquery, gitvars=gitvars, verbosity=verbosity, **kwargs)