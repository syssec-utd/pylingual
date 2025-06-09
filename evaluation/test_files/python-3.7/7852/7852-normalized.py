def config(self, name='skype'):
    """
        Configure this endpoint to allow setting presence.

        Args:
            name (str): display name for this endpoint
        """
    self.conn('PUT', '{0}/users/ME/endpoints/{1}/presenceDocs/messagingService'.format(self.conn.msgsHost, self.id), auth=SkypeConnection.Auth.RegToken, json={'id': 'messagingService', 'type': 'EndpointPresenceDoc', 'selfLink': 'uri', 'privateInfo': {'epname': name}, 'publicInfo': {'capabilities': '', 'type': 1, 'skypeNameVersion': 'skype.com', 'nodeInfo': 'xx', 'version': '908/1.30.0.128'}})