def set_client_certificate(self, certificate):
    """Sets client certificate for the request. """
    _certificate = BSTR(certificate)
    _WinHttpRequest._SetClientCertificate(self, _certificate)