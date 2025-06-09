def newnews_gen(self, pattern, timestamp):
    """Generator for the NEWNEWS command.

        Generates a list of message-ids for articles created since the specified
        timestamp for newsgroups with names that match the given pattern.

        See <http://tools.ietf.org/html/rfc3977#section-7.4>

        Args:
            pattern: Glob matching newsgroups of intrest.
            timestamp: Datetime object giving 'created since' datetime.

        Yields:
            A message-id as string.

        Note: If the datetime object supplied as the timestamp is naive (tzinfo
            is None) then it is assumed to be given as GMT. If tzinfo is set
            then it will be converted to GMT by this function.
        """
    if timestamp.tzinfo:
        ts = timestamp.asttimezone(date.TZ_GMT)
    else:
        ts = timestamp.replace(tzinfo=date.TZ_GMT)
    args = pattern
    args += ' ' + ts.strftime('%Y%m%d %H%M%S %Z')
    code, message = self.command('NEWNEWS', args)
    if code != 230:
        raise NNTPReplyError(code, message)
    for line in self.info_gen(code, message):
        yield line.strip()