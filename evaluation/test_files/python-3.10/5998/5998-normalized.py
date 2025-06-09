def check_load_privatekey_callback_wrong_type(self):
    """
        Call the function with an encrypted PEM and a passphrase callback which
        returns a non-string.
        """
    for i in xrange(self.iterations * 10):
        try:
            load_privatekey(FILETYPE_PEM, self.ENCRYPTED_PEM, lambda *args: {})
        except ValueError:
            pass