def set_timers(self):
    """Set renewal, rebinding times."""
    logger.debug('setting timeouts')
    self.set_timeout(self.current_state, self.renewing_time_expires, self.client.lease.renewal_time)
    self.set_timeout(self.current_state, self.rebinding_time_expires, self.client.lease.rebinding_time)