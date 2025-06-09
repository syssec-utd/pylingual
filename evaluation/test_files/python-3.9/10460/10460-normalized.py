def failure(self):
    """Update the timer to reflect a failed call"""
    self.short_interval += self.short_unit
    self.long_interval += self.long_unit
    self.short_interval = min(self.short_interval, self.max_short_timer)
    self.long_interval = min(self.long_interval, self.max_long_timer)
    self.update_interval()