def sleep_for_rate_limit(self):
    """The fetching process sleeps until the rate limit is restored or
           raises a RateLimitError exception if sleep_for_rate flag is disabled.
        """
    if self.rate_limit is not None and self.rate_limit <= self.min_rate_to_sleep:
        seconds_to_reset = self.calculate_time_to_reset()
        if seconds_to_reset < 0:
            logger.warning('Value of sleep for rate limit is negative, reset it to 0')
            seconds_to_reset = 0
        cause = 'Rate limit exhausted.'
        if self.sleep_for_rate:
            logger.info('%s Waiting %i secs for rate limit reset.', cause, seconds_to_reset)
            time.sleep(seconds_to_reset)
        else:
            raise RateLimitError(cause=cause, seconds_to_reset=seconds_to_reset)