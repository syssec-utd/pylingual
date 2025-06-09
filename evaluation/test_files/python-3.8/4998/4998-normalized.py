def fetch_from_archive(self):
    """Fetch the questions from an archive.

        It returns the items stored within an archive. If this method is called but
        no archive was provided, the method will raise a `ArchiveError` exception.

        :returns: a generator of items

        :raises ArchiveError: raised when an error occurs accessing an archive
        """
    if not self.archive:
        raise ArchiveError(cause='archive instance was not provided')
    self.client = self._init_client(from_archive=True)
    for item in self.fetch_items(self.archive.category, **self.archive.backend_params):
        yield self.metadata(item)