def _init_client(self, from_archive=False):
    """Init client"""
    return AskbotClient(self.url, self.archive, from_archive)