def create_connector_client(self, service_url: str) -> ConnectorClient:
    """
        Allows for mocking of the connector client in unit tests.
        :param service_url:
        :return:
        """
    client = ConnectorClient(self._credentials, base_url=service_url)
    client.config.add_user_agent(USER_AGENT)
    return client