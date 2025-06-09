def _referer(self, extension):
    """
        Return the referer for the given extension.

        :param extension: A valid domain extension.
        :type extension: str

        :return: The whois server to use to get the WHOIS record.
        :rtype: str
        """
    iana_record = self.lookup.whois(PyFunceble.CONFIGURATION['iana_whois_server'], 'hello.%s' % extension)
    if iana_record and 'refer' in iana_record:
        regex_referer = '(?s)refer\\:\\s+([a-zA-Z0-9._-]+)\\n'
        matched = Regex(iana_record, regex_referer, return_data=True, group=1).match()
        if matched:
            return matched
    if extension in self.manual_server:
        return self.manual_server[extension]
    return None