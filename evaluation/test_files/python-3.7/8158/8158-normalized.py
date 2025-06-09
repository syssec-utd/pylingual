def get_projected_rate(self, amt, time_at_consumption):
    """Get the projected rate using a provided amount and time

        :type amt: int
        :param amt: The proposed amount to consume

        :type time_at_consumption: float
        :param time_at_consumption: The proposed time to consume at

        :rtype: float
        :returns: The consumption rate if that amt and time were consumed
        """
    if self._last_time is None:
        return 0.0
    return self._calculate_exponential_moving_average_rate(amt, time_at_consumption)