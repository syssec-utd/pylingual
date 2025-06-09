def next(self):
    """NEXT command.
        """
    (code, message) = self.command('NEXT')
    if code != 223:
        raise NNTPReplyError(code, message)
    parts = message.split(None, 3)
    try:
        article = int(parts[0])
        ident = parts[1]
    except (IndexError, ValueError):
        raise NNTPDataError('Invalid NEXT status')
    return (article, ident)