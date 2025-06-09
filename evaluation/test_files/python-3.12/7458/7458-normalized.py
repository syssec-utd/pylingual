def get_command_audit(self, id, metrics=[]):
    """**Description**
            Get a command audit.

        **Arguments**
            - id: the id of the command audit to get.

        **Success Return Value**
            A JSON representation of the command audit.
        """
    url = '{url}/api/commands/{id}?from=0&to={to}{metrics}'.format(url=self.url, id=id, to=int(time.time() * 10 ** 6), metrics='&metrics=' + json.dumps(metrics) if metrics else '')
    res = requests.get(url, headers=self.hdrs, verify=self.ssl_verify)
    return self._request_result(res)