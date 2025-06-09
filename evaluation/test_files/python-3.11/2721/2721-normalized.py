def get_subscription(self, topic_name, subscription_name):
    """
        Gets an existing subscription.

        topic_name:
            Name of the topic.
        subscription_name:
            Name of the subscription.
        """
    _validate_not_none('topic_name', topic_name)
    _validate_not_none('subscription_name', subscription_name)
    request = HTTPRequest()
    request.method = 'GET'
    request.host = self._get_host()
    request.path = '/' + _str(topic_name) + '/subscriptions/' + _str(subscription_name) + ''
    request.path, request.query = self._httpclient._update_request_uri_query(request)
    request.headers = self._update_service_bus_header(request)
    response = self._perform_request(request)
    return _convert_response_to_subscription(response)