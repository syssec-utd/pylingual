from FNLP import URL
from FCM.MCCollection import MCCollection
from FCM.FQ import Q
from F.LOG import Log
Log = Log('jURL')
F_STATUS = 'status'
F_URL = 'url'
F_DATE_UPDATED = 'dateUpdated'
F_SITE_NAME = 'siteName'
SOURCE = 'source'
URLS = 'urls'
URLS_COLLECTION = 'urls'
RSS_FIELD = 'rss'
COUNT = 'count'
QUEUED_STATUS = 'queued for download'
SUCCESSFUL_STATUS = 'successful download'
FAILED_STATUS = 'failed download'

class jURL(MCCollection):

    @classmethod
    def url_constructor(cls):
        nc = cls()
        nc.construct_mcollection(URLS_COLLECTION)
        return nc
    ' -> QUEUED (000) <- '

    @classmethod
    def GET_FROM_QUEUED(cls):
        nc = cls.url_constructor()
        return nc.base_query(Q.BASE(F_STATUS, QUEUED_STATUS))

    @classmethod
    def ADD_TO_QUEUED(cls, url):
        nc = cls.url_constructor()
        nc.add_url(url, QUEUED_STATUS)
        return nc

    @classmethod
    def UPDATE_TO_SUCCESS(cls, url):
        nc = cls.url_constructor()
        nc.update_url_status(url, SUCCESSFUL_STATUS)
        return nc

    @classmethod
    def UPDATE_TO_FAILED(cls, url):
        nc = cls.url_constructor()
        nc.update_url_status(url, FAILED_STATUS)
        return nc

    def add_by_status(self, url, status):
        return self.add_url(url, status)

    def build_query(self, url, status=QUEUED_STATUS):
        self.clear_query_builder()
        siteName = URL.get_site_name(url)
        dateUpdated = self.get_now_date()
        self.add_to_query_builder(F_DATE_UPDATED, dateUpdated)
        self.add_to_query_builder(F_STATUS, status)
        self.add_to_query_builder(F_SITE_NAME, siteName)
        self.add_to_query_builder(F_URL, url)

    def add_url(self, url, status=QUEUED_STATUS):
        self.build_query(url, status)
        return self.insert_record(self.query_builder)

    def add_urls(self, list_of_urls, status=QUEUED_STATUS):
        query_list = []
        for url in list_of_urls:
            self.build_query(url, status)
            query_list.append(self.query_builder)
        return self.add_records(query_list)

    def update_url_status(self, url, status):
        self.build_query(url, status)
        query1 = Q.BASE('url', url)
        return self.update_record(query1, self.query_builder)
if __name__ == '__main__':
    j = jURL.url_constructor()
    j.AD