def head(self, url):
    """head request, typically used for status code retrieval, etc.
    """
    bot.debug('HEAD %s' % url)
    return self._call(url, func=requests.head)