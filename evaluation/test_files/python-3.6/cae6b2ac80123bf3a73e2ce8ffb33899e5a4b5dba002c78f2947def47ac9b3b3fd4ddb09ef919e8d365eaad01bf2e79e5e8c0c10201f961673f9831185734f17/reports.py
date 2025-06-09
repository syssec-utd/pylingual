from ..client import Client

class Reports(Client):

    def request_report(self, record_type, data):
        self.uri_path = '/v2/sp/{}/report'.format(record_type)
        self.method = 'post'
        self.data = data
        return self.execute()

    def get_report(self, report_id):
        self.uri_path = '/v2/reports/{}'.format(report_id)
        self.method = 'get'
        return self.execute()

    def get_report_download_url(self, location):
        self.method = 'get'
        return self.execute_download(location)

    def get_report_download(self, report_id):
        self.uri_path = '/v2/reports/{}/download'.format(report_id)
        self.method = 'get'
        self.headers.pop('Content-Type')
        self.headers['Accept-encoding'] = 'gzip'
        return self.execute()