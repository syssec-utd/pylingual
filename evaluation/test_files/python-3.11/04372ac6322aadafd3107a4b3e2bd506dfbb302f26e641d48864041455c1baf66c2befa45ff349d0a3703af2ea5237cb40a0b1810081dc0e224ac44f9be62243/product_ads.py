from ..client import Client

class ProductAds(Client):

    def get_product_ads_by_id(self, ad_id):
        self.method = 'get'
        self.uri_path = '/v2/sp/productAds/{}'.format(ad_id)
        return self.execute()

    def delete_product_ads_by_id(self, ad_id):
        self.method = 'delete'
        self.uri_path = '/v2/sp/productAds/{}'.format(ad_id)
        return self.execute()

    def get_product_ads(self, start_index: int=0, count: int=None, state_filter: str=None, campaign_id_filter: str=None, ad_group_id_filter: str=None, ad_id_filter: str=None):
        self.method = 'get'
        self.uri_path = '/v2/sp/productAds'
        self.params = {'startIndex': start_index, 'count': count, 'stateFilter': state_filter, 'campaignIdFilter': campaign_id_filter, 'adGroupIdFilter': ad_group_id_filter, 'adIdFilter': ad_id_filter}
        return self.execute()

    def create_product_ads(self, params):
        self.method = 'post'
        self.uri_path = '/v2/sp/productAds'
        self.data = params
        return self.execute()

    def update_product_ads(self, params):
        self.method = 'put'
        self.uri_path = '/v2/sp/productAds'
        self.data = params
        return self.execute()

    def get_product_ads_extended_by_id(self, ad_id):
        self.method = 'get'
        self.uri_path = '/v2/sp/productAds/extended/{}'.format(ad_id)
        return self.execute()

    def get_product_ads_extended(self, start_index: int=0, count: int=None, state_filter: str=None, campaign_id_filter: str=None, ad_group_id_filter: str=None, ad_id_filter: str=None):
        self.method = 'get'
        self.uri_path = '/v2/sp/productAds/extended'
        self.params = {'startIndex': start_index, 'count': count, 'stateFilter': state_filter, 'campaignIdFilter': campaign_id_filter, 'adGroupIdFilter': ad_group_id_filter, 'adIdFilter': ad_id_filter}
        return self.execute()

class ProductAdsV3(Client):

    def create_product_ads(self, data):
        self.method = 'post'
        self.uri_path = '/sp/productAds'
        self.data = data
        return self.execute()

    def get_product_ads_list(self, data):
        self.method = 'post'
        self.uri_path = '/sp/productAds/list'
        self.data = data
        return self.execute()

    def update_product_ads(self, data):
        self.method = 'put'
        self.uri_path = '/sp/productAds'
        self.data = data
        return self.execute()

    def delete_product_ads(self, data):
        self.method = 'post'
        self.uri_path = '/sp/productAds/delete'
        self.data = data
        return self.execute()