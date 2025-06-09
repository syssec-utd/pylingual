def _signature(self, *parts):
    """
        Creates signature for the session.
        """
    signature = hmac.new(six.b(self.secret), digestmod=hashlib.sha1)
    signature.update(six.b('|'.join(parts)))
    return signature.hexdigest()