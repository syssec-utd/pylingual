def setauth(self, basic_auth):
    """ setauth can be used during runtime to make sure that authentication is reset.
        it can be used when changing passwords/apikeys to make sure reconnects succeed """
    self.headers = []
    if basic_auth is not None:

        class auth_extractor:

            def __init__(self):
                self.headers = {}
        extractor = auth_extractor()
        basic_auth(extractor)
        for header in extractor.headers:
            self.headers.append('%s: %s' % (header, extractor.headers[header]))