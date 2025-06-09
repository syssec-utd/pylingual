"""This module contains the client dealing with PaaS Orchestrator information."""
from orpy.client import base
from orpy import exceptions

class Info(object):
    """Get information about the Orchestrator."""

    def __init__(self, client):
        """Initialize client.

        :params client: An instance of OrpyClient.
        """
        self.client = client

    def get(self, **kwargs):
        """Get information about the Orchestrator.

        :param kwargs: Other arguments passed to the request client.

        :return: Information about the orchestrator.
        :rtype: orpy.client.base.OrchestratorInfo
        """
        try:
            resp, body = self.client.get('./info', **kwargs)
        except exceptions.ClientError:
            raise exceptions.InvalidUrlError(url=self.client.url)
        if resp.status_code == 200:
            body['url'] = self.client.url
            return base.OrchestratorInfo(body)
        else:
            raise exceptions.InvalidUrlError(url=self.client.url)