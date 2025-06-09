def _get_endpoint(self):
    """ Creates a generic endpoint connection that doesn't finish
        """
    return SSHCommandClientEndpoint.newConnection(reactor, b'/bin/cat', self.username, self.hostname, port=self.port, keys=self.keys, password=self.password, knownHosts=self.knownHosts)