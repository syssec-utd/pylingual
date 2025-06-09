def subscribe(self, user_token, topic):
    """
        Subscribe a user to the given topic.

        :param str user_token: The token of the user.
        :param str topic: The topic.
        :raises `requests.exceptions.HTTPError`: If an HTTP error occurred.
        """
    response = _request('POST', url=self.url_v1('/user/subscriptions/' + topic), user_agent=self.user_agent, user_token=user_token)
    _raise_for_status(response)