def fetch_items(self, category, **kwargs):
    """Fetch the pages

        :param category: the category of items to fetch
        :param kwargs: backend arguments

        :returns: a generator of items
        """
    from_date = kwargs['from_date']
    reviews_api = kwargs['reviews_api']
    mediawiki_version = self.client.get_version()
    logger.info('MediaWiki version: %s', mediawiki_version)
    if reviews_api:
        if mediawiki_version[0] == 1 and mediawiki_version[1] >= 27 or mediawiki_version[0] > 1:
            fetcher = self.__fetch_1_27(from_date)
        else:
            logger.warning('Reviews API only available in MediaWiki >= 1.27')
            logger.warning('Using the Pages API instead')
            fetcher = self.__fetch_pre1_27(from_date)
    else:
        fetcher = self.__fetch_pre1_27(from_date)
    for page_reviews in fetcher:
        yield page_reviews