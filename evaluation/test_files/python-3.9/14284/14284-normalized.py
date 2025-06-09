def get_full_time_interval(self):
    """Give the full time interval of the file. Note that the real interval
        can be longer because the sound file attached can be longer.

        :returns: Tuple of the form: ``(min_time, max_time)``.
        """
    return (0, 0) if not self.timeslots else (min(self.timeslots.values()), max(self.timeslots.values()))