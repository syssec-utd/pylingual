import requests
import random
import re
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

class ProxyChecker:

    def __init__(self):
        self.ip = self.get_ip()
        self.proxy_judges = ['http://proxyjudge.us/azenv.php', 'http://mojeip.net.pl/asdfa/azenv.php']

    def get_ip(self):
        r = self.send_query(url='https://api.ipify.org/')
        if not r:
            return ''
        return r['response']

    def send_query(self, proxy=False, url=None, user=None, password=None):
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        proxies = None
        if proxy:
            proxies = {'http': proxy, 'https': proxy}
        auth = None
        if user is not None and password is not None:
            auth = (user, password)
        try:
            response = session.get(url or random.choice(self.proxy_judges), proxies=proxies, auth=auth, timeout=5, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return False
        return {'timeout': int(response.elapsed.total_seconds() * 1000), 'response': response.text}

    def parse_anonymity(self, r):
        if self.ip in r:
            return 'Transparent'
        privacy_headers = ['VIA', 'X-FORWARDED-FOR', 'X-FORWARDED', 'FORWARDED-FOR', 'FORWARDED-FOR-IP', 'FORWARDED', 'CLIENT-IP', 'PROXY-CONNECTION']
        if any([header in r for header in privacy_headers]):
            return 'Anonymous'
        return 'Elite'

    def get_country(self, ip):
        r = self.send_query(url='https://ip2c.org/' + ip)
        if r and r['response'][0] == '1':
            r = r['response'].split(';')
            return [r[3], r[1]]
        return ['-', '-']

    def check_proxy(self, proxy, check_country=True, check_address=False, user=None, password=None):
        protocols = {}
        timeout = 0
        proxy_url = 'http://' + proxy
        r = self.send_query(proxy=proxy_url, user=user, password=password)
        if not r:
            return False
        protocols['http'] = r
        timeout += r['timeout']
        r = protocols['http']['response']
        if check_country:
            country = self.get_country(proxy.split(':')[0])
        anonymity = self.parse_anonymity(r)
        timeout = timeout // len(protocols)
        if check_address:
            remote_regex = 'REMOTE_ADDR = (\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})'
            remote_addr = re.search(remote_regex, r)
            if remote_addr:
                remote_addr = remote_addr.group(1)
        results = {'protocols': list(protocols.keys()), 'anonymity': anonymity, 'timeout': timeout}
        if check_country:
            results['country'] = country[0]
            results['country_code'] = country[1]
        if check_address:
            results['remote_address'] = remote_addr
        return results