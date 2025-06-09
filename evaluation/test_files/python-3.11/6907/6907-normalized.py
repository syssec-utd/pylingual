def _extensions(self):
    """
        Extract the extention from the given block.
        Plus get its referer.
        """
    upstream_lines = Download(self.iana_url, return_data=True).text().split('<span class="domain tld">')
    regex_valid_extension = '(/domains/root/db/)(.*)(\\.html)'
    for block in upstream_lines:
        if '/domains/root/db/' in block:
            matched = Regex(block, regex_valid_extension, return_data=True, rematch=True).match()[1]
            if matched:
                referer = self._referer(matched)
                yield (matched, referer)