import requests
import yaml
import os
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
_LOG_FORMAT = '[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(asctime)s --> %(message)s'
g_logger = logging.getLogger()
logging.basicConfig(format=_LOG_FORMAT)
g_logger.setLevel(logging.INFO)
root_dir = os.path.abspath(os.path.dirname(__file__))
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    url_list = yaml.load(file, Loader=yaml.FullLoader)

class SignUp:

    def __init__(self, Askdata):
        self.username = Askdata.username
        self._token = Askdata._token
        self._env = Askdata._env
        self._domainlogin = Askdata._domainlogin.upper()
        self._headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer' + ' ' + self._token}
        if self._env == 'dev':
            self.base_url_security = url_list['BASE_URL_SECURITY_DEV']
        if self._env == 'qa':
            self.base_url_security = url_list['BASE_URL_SECURITY_QA']
        if self._env == 'prod':
            self.base_url_security = url_list['BASE_URL_SECURITY_PROD']

    def signup_user(self, username: str, password: str, firstname='-', secondname='-', title='-') -> dict:
        data = {'username': username, 'password': password, 'firstName': firstname, 'lastName': secondname, 'mobile': '-', 'title': title, 'email': username}
        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))
        authentication_url = self.base_url_security + '/domain/' + self._domainlogin + '/usersignup'
        r = s.post(url=authentication_url, headers=self._headers, json=data)
        logging.info('--- ------------ ----')
        logging.info('---- add user ---> {}  --- PENDING'.format(username))
        return r.json()