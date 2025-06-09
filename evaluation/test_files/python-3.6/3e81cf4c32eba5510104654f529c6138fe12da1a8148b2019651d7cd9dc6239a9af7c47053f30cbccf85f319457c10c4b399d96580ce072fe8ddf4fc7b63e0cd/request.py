import os
import socket
import logging
import requests
import certifi
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from mathtranslate.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
logger = logging.getLogger('tencentcloud_sdk_common')

def _get_proxy_from_env(host, varname='HTTPS_PROXY'):
    no_proxy = os.environ.get('NO_PROXY') or os.environ.get('no_proxy')
    if no_proxy and host in no_proxy:
        return None
    return os.environ.get(varname.lower()) or os.environ.get(varname.upper())

class ProxyConnection(object):

    def __init__(self, host, timeout=60, proxy=None, certification=None, is_http=False):
        self.request_host = host
        self.certification = certification
        if certification is None:
            self.certification = certifi.where()
        self.timeout = timeout
        self.proxy = None
        if is_http:
            proxy = proxy or _get_proxy_from_env(host, varname='HTTP_PROXY')
        else:
            proxy = proxy or _get_proxy_from_env(host, varname='HTTPS_PROXY')
        if proxy:
            self.proxy = {'http': proxy, 'https': proxy}
        self.request_length = 0

    def request(self, method, url, body=None, headers={}):
        self.request_length = 0
        headers.setdefault('Host', self.request_host)
        return requests.request(method=method, url=url, data=body, headers=headers, proxies=self.proxy, verify=self.certification, timeout=self.timeout)

class ApiRequest(object):

    def __init__(self, host, req_timeout=60, debug=False, proxy=None, is_http=False, certification=None):
        self.conn = ProxyConnection(host, timeout=req_timeout, proxy=proxy, certification=certification, is_http=is_http)
        url = urlparse(host)
        if not url.hostname:
            if is_http:
                host = 'http://' + host
            else:
                host = 'https://' + host
        self.host = host
        self.req_timeout = req_timeout
        self.keep_alive = False
        self.debug = debug
        self.request_size = 0
        self.response_size = 0

    def set_req_timeout(self, req_timeout):
        self.req_timeout = req_timeout

    def is_keep_alive(self):
        return self.keep_alive

    def set_keep_alive(self, flag=True):
        self.keep_alive = flag

    def set_debug(self, debug):
        self.debug = debug

    def _request(self, req_inter):
        if self.keep_alive:
            req_inter.header['Connection'] = 'Keep-Alive'
        if self.debug:
            logger.debug('SendRequest %s' % req_inter)
        if req_inter.method == 'GET':
            req_inter_url = '%s?%s' % (self.host, req_inter.data)
            return self.conn.request(req_inter.method, req_inter_url, None, req_inter.header)
        elif req_inter.method == 'POST':
            return self.conn.request(req_inter.method, self.host, req_inter.data, req_inter.header)
        else:
            raise TencentCloudSDKException('ClientParamsError', 'Method only support (GET, POST)')

    def send_request(self, req_inter):
        try:
            http_resp = self._request(req_inter)
            headers = dict(http_resp.headers)
            resp_inter = ResponseInternal(status=http_resp.status_code, header=headers, data=http_resp.text)
            self.request_size = self.conn.request_length
            self.response_size = len(resp_inter.data)
            logger.debug('GetResponse %s' % resp_inter)
            return resp_inter
        except Exception as e:
            raise TencentCloudSDKException('ClientNetworkError', str(e))

class RequestInternal(object):

    def __init__(self, host='', method='', uri='', header=None, data=''):
        if header is None:
            header = {}
        self.host = host
        self.method = method
        self.uri = uri
        self.header = header
        self.data = data

    def __str__(self):
        headers = '\n'.join(('%s: %s' % (k, v) for (k, v) in self.header.items()))
        return 'Host: %s\nMethod: %s\nUri: %s\nHeader: %s\nData: %s\n' % (self.host, self.method, self.uri, headers, self.data)

class ResponseInternal(object):

    def __init__(self, status=0, header=None, data=''):
        if header is None:
            header = {}
        self.status = status
        self.header = header
        self.data = data

    def __str__(self):
        headers = '\n'.join(('%s: %s' % (k, v) for (k, v) in self.header.items()))
        return 'Status: %s\nHeader: %s\nData: %s\n' % (self.status, headers, self.data)