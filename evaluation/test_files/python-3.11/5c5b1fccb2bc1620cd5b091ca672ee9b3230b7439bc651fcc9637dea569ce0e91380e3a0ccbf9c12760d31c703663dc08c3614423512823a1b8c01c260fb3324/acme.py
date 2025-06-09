"""
ACME API client.
"""
from . import get_version
from .crypto import export_certificate_for_acme, generate_header, jose_b64, sign_request, sign_request_v2
from .errors import AccountAlreadyExistsError, AcmeError
from .model import Order, Challenge
from collections import namedtuple
import copy
import datetime
import hashlib
import logging
import requests
import time
from urllib.parse import urljoin, urlparse
logger = logging.getLogger(__name__)
DEFAULT_HEADERS = {'User-Agent': 'automatoes {} (https://candango.org/p/automatoes)'.format(get_version())}

class Acme:

    def __init__(self, url, account, directory='directory', verify=None):
        self.url = url
        self.account = None
        self.directory = directory
        self.directory_cache = None
        self.verify = verify
        self.set_account(account)

    def set_account(self, account):
        self.account = account

    @property
    def key(self):
        if self.account is None:
            return None
        return self.account.key

    def get_directory(self):
        return self.get('/directory')

    def get_nonce(self):
        """
        Gets a new nonce.
        """
        return self.get('/directory').headers.get('Replay-Nonce')

    def get_headers(self):
        """
        Builds a new pair of headers for signed requests.
        """
        header = generate_header(self.account.key)
        protected_header = copy.deepcopy(header)
        protected_header['nonce'] = self.get_nonce()
        return (header, protected_header)

    def register(self, email):
        """
        Registers the current account on the server.
        """
        response = self.post('/acme/new-reg', {'resource': 'new-reg', 'contact': ['mailto:{}'.format(email)]})
        uri = response.headers.get('Location')
        if response.status_code == 201:
            self.account.uri = uri
            terms = response.links.get('terms-of-service')
            return RegistrationResult(contents=_json(response), uri=uri, terms=terms['url'] if terms else None)
        elif response.status_code == 409:
            raise AccountAlreadyExistsError(response, uri)
        raise AcmeError(response)

    def get_registration(self):
        """
        Gets available account information from the server.
        """
        response = self.post(self.account.uri, {'resource': 'reg'})
        if str(response.status_code).startswith('2'):
            return _json(response)
        raise AcmeError(response)

    def update_registration(self, params=None):
        """
        Updates registration information on the server.
        """
        params = params or {}
        params['resource'] = 'reg'
        response = self.post(self.account.uri, params)
        if str(response.status_code).startswith('2'):
            return True
        raise AcmeError(response)

    def new_authorization(self, domain, type='dns'):
        """
        Requests a new authorization for the specified domain.
        :return Order
        """
        response = self.post('/acme/new-authz', {'resource': 'new-authz', 'identifier': {'type': type, 'value': domain}})
        if response.status_code == 201:
            return NewAuthorizationResult(_json(response), response.headers.get('Location'))
        raise AcmeError(response)

    def validate_authorization(self, uri, _type, key_authorization=None):
        """
        Marks the specified validation as complete.
        """
        response = self.post(uri, {'resource': 'challenge', 'type': _type, 'keyAuthorization': key_authorization})
        if str(response.status_code).startswith('2'):
            return True
        raise AcmeError(response)

    def get_authorization(self, uri):
        """
        Returns the authorization status.
        """
        response = self.get(uri)
        try:
            return response.json()
        except (ValueError, TypeError, AttributeError) as e:
            raise AcmeError(e)

    def issue_certificate(self, csr):
        http_headers = {'Accept': 'application/pkix-cert'}
        response = self.post('/acme/new-cert', {'resource': 'new-cert', 'csr': csr}, headers=http_headers)
        if response.status_code == 201:
            chain = response.links.get('up')
            if chain:
                chain = requests.get(chain['url'], headers=DEFAULT_HEADERS).content
            return IssuanceResult(response.content, response.headers.get('Location'), chain)
        raise AcmeError(response)

    def revoke_certificate(self, cert):
        response = self.post('/acme/revoke-cert', {'resource': 'revoke-cert', 'certificate': cert})
        if response.status_code == 200:
            return True
        raise AcmeError(response)

    def get(self, path, headers=None):
        _headers = DEFAULT_HEADERS.copy()
        if headers:
            _headers.update(headers)
        kwargs = {'headers': _headers}
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.get(self.path(path), **kwargs)

    def post(self, path, body, headers=None):
        _headers = DEFAULT_HEADERS.copy()
        _headers['Content-Type'] = 'application/json'
        if headers:
            _headers.update(headers)
        header, protected = self.get_headers()
        body = sign_request(self.account.key, header, protected, body)
        kwargs = {'headers': _headers}
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.post(self.path(path), data=body, **kwargs)

    def path(self, path):
        if path.startswith('https'):
            return path
        if path.startswith('http'):
            path = urlparse(path).path
        url_parsed = urlparse(self.url)
        if url_parsed.path != '':
            url_parsed_path = url_parsed.path
            if url_parsed_path.startswith('/'):
                url_parsed_path = url_parsed_path[1:]
            if path.startswith('/'):
                path = path[1:]
            path = '%s/%s' % (url_parsed_path, path)
        return urljoin(self.url, path)
RegistrationResult = namedtuple('RegistrationResult', 'contents uri terms')
NewAuthorizationResult = namedtuple('NewAuthorizationResult', 'contents uri')
IssuanceResult = namedtuple('IssuanceResult', 'certificate location intermediate')

class AcmeV2(Acme):

    def __init__(self, url, account, directory='directory', verify=None, upgrade=False):
        super(AcmeV2, self).__init__(url, account, directory, verify)
        if self.is_uri_letsencrypt_acme_v1():
            if not upgrade:
                logger.warning("WARNING: The account is using Let's Encrypt discontinued ACME V1 url.")
                logger.warning('WARNING: Upgrading account to ACME V2 temporally.')
                logger.warning("WARNING: Please run 'manuale upgrade' to make the change permanently.")
                self.account.uri = self.letsencrypt_acme_uri_v1_to_v2()

    def is_uri_letsencrypt_acme_v1(self):
        if self.account is None:
            return False
        if self.account.uri is None:
            return False
        return 'acme-v01.api.letsencrypt.org' in self.account.uri

    def letsencrypt_acme_uri_v1_to_v2(self):
        if self.account is None:
            return None
        uri = self.account.uri.replace('acme-v01.api.letsencrypt.org', 'acme-v02.api.letsencrypt.org')
        return uri.replace('acme/reg', 'acme/acct')

    def head(self, path, headers=None):
        _headers = DEFAULT_HEADERS.copy()
        if headers:
            _headers.update(headers)
        kwargs = {'headers': _headers}
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.head(self.path(path), **kwargs)

    def get_headers(self, url=None):
        """
        Builds a new pair of headers for signed requests.
        """
        header = generate_header(self.account.key)
        protected_header = copy.deepcopy(header)
        protected_header['nonce'] = self.get_nonce()
        if url is not None:
            protected_header['url'] = url
        return protected_header

    def get_directory(self):
        if not self.directory_cache:
            self.directory_cache = self.get('/{}'.format(self.directory))
        return self.directory_cache

    def url_from_directory(self, what_url):
        response = self.get_directory()
        if response.status_code == 200:
            return response.json()[what_url]
        return None

    def terms_from_directory(self):
        response = self.get_directory()
        if response.status_code == 200:
            if 'meta' in response.json():
                if 'termsOfService' in response.json()['meta']:
                    return response.json()['meta']['termsOfService']
        return None

    def get_nonce(self):
        """ Gets a new nonce.
        """
        return self.head(self.url_from_directory('newNonce'), {'resource': 'new-reg', 'payload': None}).headers.get('Replay-Nonce')

    def register(self, email, terms_agreed=False):
        """Registers the current account on the server.
        """
        payload = {'termsOfServiceAgreed': terms_agreed, 'contact': ['mailto:{email}'.format(email=email)]}
        response = self.post(self.url_from_directory('newAccount'), payload)
        uri = response.headers.get('Location')
        if response.status_code == 201:
            self.account.uri = uri
            terms = self.terms_from_directory()
            return RegistrationResult(contents=_json(response), uri=uri, terms=terms)
        elif response.status_code == 409:
            raise AccountAlreadyExistsError(response, uri)
        raise AcmeError(response)

    def get_registration(self):
        """
        Get available account information from the server.
        """
        response = self.post_as_get(self.account.uri, kid=self.account.uri)
        if str(response.status_code).startswith('2'):
            return _json(response)
        raise AcmeError(response)

    def new_order(self, domains, type='dns'):
        """ Requests a new authorization for the specified domain.
        """
        domains_with_type = []
        if not isinstance(domains, list):
            domains = [domains]
        for domain in domains:
            domains_with_type.append({'type': 'dns', 'value': domain})
        response = self.post(self.url_from_directory('newOrder'), {'identifiers': domains_with_type}, kid=self.account.uri)
        if response.status_code == 201:
            return Order(contents=_json(response), uri=response.headers.get('Location'), ty_pe=type)
        raise AcmeError(response)

    def query_orders(self):
        """ Query existent order status

        :return: Order
        """
        raise NotImplementedError

    def query_order(self, order: Order):
        """ Query existent order status
        :param order: order to be challenged
        :return: Order
        """
        response = self.post_as_get(order.uri, kid=self.account.uri)
        if response.status_code == 200:
            return Order(contents=_json(response), uri=order.uri, ty_pe=order.type)
        raise AcmeError(response)

    def get_order_challenges(self, order: Order):
        """ Return all challenges from an order .
        :param order: order to be challenged
        :return: Order
        """
        domains = [identifier['value'] for identifier in order.contents['identifiers']]
        order_challenges = []
        for auth in order.contents['authorizations']:
            auth_response = _json(self.post_as_get(auth, self.account.uri))
            for challenge in auth_response['challenges']:
                key_authorization = '{}.{}'.format(challenge['token'], self.account.thumbprint)
                digest = hashlib.sha256()
                digest.update(key_authorization.encode('ascii'))
                if order.type in challenge['type']:
                    if 'expires' not in auth_response:
                        expire_date = datetime.datetime.now() + datetime.timedelta(days=2)
                        auth_response['expires'] = expire_date.strftime('%Y-%m-%dT%H:%M:%S')
                    order_challenges.append(Challenge(contents=challenge, domain=auth_response['identifier']['value'], expires=auth_response['expires'], status=auth_response['status'], ty_pe=order.type, key=jose_b64(digest.digest())))
        return order_challenges

    def verify_order_challenge(self, challenge: Challenge, timeout=5, retry_limit=5):
        """ Return all challenges from an order .
        :param challenge: A challenge from the order
        :param int timeout: timeout before check challenge status
        :param retry_limit: retry limit of checks of a challenge
        :return:
        """
        parsed_url = urlparse(self.url)
        host = parsed_url.hostname
        if parsed_url.port:
            host = '{}:{}'.format(host, parsed_url.port)
        response = _json(self.post(challenge.contents['url'], {}, {'Host': host}, kid=self.account.uri))
        retries = 0
        while response['status'] == 'pending':
            if retries < retry_limit:
                time.sleep(timeout)
                response = _json(self.post_as_get(challenge.contents['url'], kid=self.account.uri))
        return response

    def finalize_order(self, order: Order, csr):
        """ Marks the specified validation as complete.
        :param order: order to be finalized
        :param csr a certificate public key in base64
        :return:
        """
        response = self.post(order.contents['finalize'], {'csr': export_certificate_for_acme(csr)}, kid=self.account.uri)
        if _json(response)['status'] == 'valid':
            order.certificate_uri = _json(response)['certificate']
        if response.status_code == 200:
            return _json(response)
        raise AcmeError(response)

    def await_for_order_fulfillment(self, order, timeout=2, iterations=5):
        response = self.post_as_get(order.uri, kid=self.account.uri)
        iteration_count = 0
        while _json(response)['status'] != 'valid':
            if iteration_count == iterations:
                break
            time.sleep(timeout)
            response = self.post_as_get(order.uri, kid=self.account.uri)
            iteration_count += 1
        if _json(response)['status'] == 'valid':
            order.certificate_uri = _json(response)['certificate']
        if response.status_code == 200:
            return _json(response)
        raise AcmeError(response)

    def download_order_certificate(self, order):
        response = self.post_as_get(order.certificate_uri, kid=self.account.uri)
        if response.status_code == 200:
            order.certificate = response.content
            return response
        raise AcmeError(response)

    def revoke_certificate(self, cert):
        response = self.post(self.url_from_directory('revokeCert'), {'certificate': export_certificate_for_acme(cert)}, kid=self.account.uri)
        if response.status_code == 200:
            return response
        raise AcmeError(response)

    def post(self, path, body, headers=None, kid=None):
        _headers = DEFAULT_HEADERS.copy()
        _headers['Content-Type'] = 'application/jose+json'
        if headers:
            _headers.update(headers)
        protected = self.get_headers(url=self.path(path))
        if kid:
            protected['kid'] = kid
            protected.pop('jwk')
        body = sign_request_v2(self.account.key, protected, body)
        kwargs = {'headers': _headers}
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.post(self.path(path), data=body, **kwargs)

    def post_as_get(self, path, kid, headers=None):
        _headers = DEFAULT_HEADERS.copy()
        _headers['Content-Type'] = 'application/jose+json'
        if headers:
            _headers.update(headers)
        protected = self.get_headers(url=self.path(path))
        protected['kid'] = kid
        protected.pop('jwk')
        body = sign_request_v2(self.account.key, protected, None)
        kwargs = {'headers': _headers}
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.post(self.path(path), data=body, **kwargs)

def _json(response):
    try:
        return response.json()
    except ValueError as e:
        raise AcmeError('Invalid JSON response. {}'.format(e))