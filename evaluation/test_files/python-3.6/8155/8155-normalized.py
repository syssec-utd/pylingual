def consume(self, amt, request_token):
    """Consume an a requested amount

        :type amt: int
        :param amt: The amount of bytes to request to consume

        :type request_token: RequestToken
        :param request_token: The token associated to the consumption
            request that is used to identify the request. So if a
            RequestExceededException is raised the token should be used
            in subsequent retry consume() request.

        :raises RequestExceededException: If the consumption amount would
            exceed the maximum allocated bandwidth

        :rtype: int
        :returns: The amount consumed
        """
    with self._lock:
        time_now = self._time_utils.time()
        if self._consumption_scheduler.is_scheduled(request_token):
            return self._release_requested_amt_for_scheduled_request(amt, request_token, time_now)
        elif self._projected_to_exceed_max_rate(amt, time_now):
            self._raise_request_exceeded_exception(amt, request_token, time_now)
        else:
            return self._release_requested_amt(amt, time_now)