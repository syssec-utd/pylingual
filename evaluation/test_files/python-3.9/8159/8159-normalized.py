def record_consumption_rate(self, amt, time_at_consumption):
    """Record the consumption rate based off amount and time point

        :type amt: int
        :param amt: The amount that got consumed

        :type time_at_consumption: float
        :param time_at_consumption: The time at which the amount was consumed
        """
    if self._last_time is None:
        self._last_time = time_at_consumption
        self._current_rate = 0.0
        return
    self._current_rate = self._calculate_exponential_moving_average_rate(amt, time_at_consumption)
    self._last_time = time_at_consumption