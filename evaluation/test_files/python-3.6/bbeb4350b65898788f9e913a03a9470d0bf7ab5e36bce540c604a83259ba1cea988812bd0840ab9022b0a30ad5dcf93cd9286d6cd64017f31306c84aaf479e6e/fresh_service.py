import requests
from zeno_etl_libs.config.common import Config

class FreshService:

    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.api_token = secrets['FRESHSERVICE_API']

    def get_tickets(self, page, updated_since=None):
        _filter = ''
        if updated_since:
            updated_since = str(updated_since)
            updated_since = f'{updated_since[0:19]}Z'
            _filter = f'&updated_since={updated_since}'
        url = f'https://generico.freshservice.com/helpdesk/tickets/filter/all_tickets?order_type=desc&format=json{_filter}&page={page}'
        response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=requests.auth.HTTPBasicAuth(self.api_token, 'X'))
        if response.status_code == 200:
            return response.json()
        else:
            print(f'[ERROR]fresh service status code: {response.status_code}, response: {response.text}')
            return {}