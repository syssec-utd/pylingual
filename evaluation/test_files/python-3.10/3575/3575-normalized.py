def track_request(self, name: str, url: str, success: bool, start_time: str=None, duration: int=None, response_code: str=None, http_method: str=None, properties: Dict[str, object]=None, measurements: Dict[str, object]=None, request_id: str=None):
    """
        Sends a single request that was captured for the application.
        :param name: The name for this request. All requests with the same name will be grouped together.
        :param url: The actual URL for this request (to show in individual request instances).
        :param success: True if the request ended in success, False otherwise.
        :param start_time: the start time of the request. The value should look the same as the one returned by :func:`datetime.isoformat()` (defaults to: None)
        :param duration: the number of milliseconds that this request lasted. (defaults to: None)
        :param response_code: the response code that this request returned. (defaults to: None)
        :param http_method: the HTTP method that triggered this request. (defaults to: None)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        :param request_id: the id for this request. If None, a new uuid will be generated. (defaults to: None)
        """
    self._client.track_request(name, url, success, start_time, duration, response_code, http_method, properties, measurements, request_id)