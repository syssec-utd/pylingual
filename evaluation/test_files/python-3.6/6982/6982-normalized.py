def whois(cls, whois_server, domain=None, timeout=None):
    """
        Implementation of UNIX whois.

        :param whois_server: The WHOIS server to use to get the record.
        :type whois_server: str

        :param domain: The domain to get the whois record from.
        :type domain: str

        :param timeout: The timeout to apply to the request.
        :type timeout: int

        :return: The whois record from the given whois server, if exist.
        :rtype: str|None
        """
    if domain is None:
        domain = PyFunceble.INTERN['to_test']
    if timeout is None:
        timeout = PyFunceble.CONFIGURATION['seconds_before_http_timeout']
    if whois_server:
        req = PyFunceble.socket.socket(PyFunceble.socket.AF_INET, PyFunceble.socket.SOCK_STREAM)
        if timeout % 3 == 0:
            req.settimeout(timeout)
        else:
            req.settimeout(3)
        try:
            req.connect((whois_server, 43))
        except PyFunceble.socket.error:
            return None
        req.send((domain + '\r\n').encode())
        response = b''
        while True:
            try:
                data = req.recv(4096)
            except (PyFunceble.socket.timeout, ConnectionResetError):
                req.close()
                return None
            response += data
            if not data:
                break
        req.close()
        try:
            return response.decode()
        except UnicodeDecodeError:
            return response.decode('utf-8', 'replace')
    return None