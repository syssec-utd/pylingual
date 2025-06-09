def _init_client(self, from_archive=False):
    """Init client"""
    return ReMoClient(self.url, self.archive, from_archive)