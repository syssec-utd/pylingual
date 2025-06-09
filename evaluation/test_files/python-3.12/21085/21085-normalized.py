def get_url_rev(self):
    """
        Returns the correct repository URL and revision by parsing the given
        repository URL
        """
    error_message = "Sorry, '%s' is a malformed VCS url. Ihe format is <vcs>+<protocol>://<url>, e.g. svn+http://myrepo/svn/MyApp#egg=MyApp"
    assert '+' in self.url, error_message % self.url
    url = self.url.split('+', 1)[1]
    scheme, netloc, path, query, frag = urlparse.urlsplit(url)
    rev = None
    if '@' in path:
        path, rev = path.rsplit('@', 1)
    url = urlparse.urlunsplit((scheme, netloc, path, query, ''))
    return (url, rev)