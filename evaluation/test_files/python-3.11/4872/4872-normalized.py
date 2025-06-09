def _init_client(self, from_archive=False):
    """Init client"""
    return MattermostClient(self.url, self.api_token, max_items=self.max_items, sleep_for_rate=self.sleep_for_rate, min_rate_to_sleep=self.min_rate_to_sleep, sleep_time=self.sleep_time, archive=self.archive, from_archive=from_archive)