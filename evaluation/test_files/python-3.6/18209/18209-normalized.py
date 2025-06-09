def xover_gen(self, range=None):
    """Generator for the XOVER command.

        The XOVER command returns information from the overview database for
        the article(s) specified.

        <http://tools.ietf.org/html/rfc2980#section-2.8>

        Args:
            range: An article number as an integer, or a tuple of specifying a
                range of article numbers in the form (first, [last]). If last is
                omitted then all articles after first are included. A range of
                None (the default) uses the current article.

        Returns:
            A list of fields as given by the overview database for each
            available article in the specified range. The fields that are
            returned can be determined using the LIST OVERVIEW.FMT command if
            the server supports it.

        Raises:
            NNTPReplyError: If no such article exists or the currently selected
                newsgroup is invalid.
        """
    args = None
    if range is not None:
        args = utils.unparse_range(range)
    (code, message) = self.command('XOVER', args)
    if code != 224:
        raise NNTPReplyError(code, message)
    for line in self.info_gen(code, message):
        yield line.rstrip().split('\t')