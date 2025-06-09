def date(self):
    """DATE command.

        Coordinated Universal time from the perspective of the usenet server.
        It can be used to provide information that might be useful when using
        the NEWNEWS command.

        See <http://tools.ietf.org/html/rfc3977#section-7.1>

        Returns:
            The UTC time according to the server as a datetime object.

        Raises:
            NNTPDataError: If the timestamp can't be parsed.
        """
    (code, message) = self.command('DATE')
    if code != 111:
        raise NNTPReplyError(code, message)
    ts = date.datetimeobj(message, fmt='%Y%m%d%H%M%S')
    return ts