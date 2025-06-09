from http import HTTPStatus
from re import match
from time import time
from typing import Any, Dict, Optional, Tuple, Type, TypeVar
from urllib.parse import urlparse
import requests
from aiohttp import ClientSession, ClientTimeout
from aiohttp.hdrs import AUTHORIZATION, CONTENT_TYPE, METH_DELETE, METH_GET, METH_HEAD, METH_OPTIONS, METH_PATCH, METH_POST, METH_PUT
from mime_parser.favorite import APPLICATION_JSON, MIME_APPLICATION_JSON_UTF8
from multidict import CIMultiDict
from type_serialize import serialize
from recc.driver.json import global_json_encoder
from recc.http import http_urls as u
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_packet import HttpResponse
from recc.http.http_payload import payload_to_class
from recc.http.http_utils import join_urls, v2_public_path
from recc.packet.user import SigninA, SignupQ
from recc.variables.http import DEFAULT_REQUEST_TIMEOUT_SECONDS, DEFAULT_SCHEME, URI_PATH_SEPARATOR

def normalize_url_path(path: str) -> str:
    if not path:
        return u.root
    if path[0] != u.root:
        return u.root + path
    return path

def request(host: str, port: int, path=u.root, scheme=DEFAULT_SCHEME, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS, data=None) -> Tuple[int, Optional[str]]:
    url = f'{scheme}://{host}:{port}{normalize_url_path(path)}'
    response = requests.get(url=url, data=data, timeout=timeout)
    code = response.status_code
    return (code, response.text if code == 200 else str())

def request_heartbeat(host: str, port: int, scheme=DEFAULT_SCHEME, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) -> Tuple[int, Optional[str]]:
    return request(host=host, port=port, path=u.api_heartbeat, scheme=scheme, timeout=timeout)

def wait_heartbeat(host: str, port: int, scheme=DEFAULT_SCHEME, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) -> None:
    begin = time()
    last_code = 0
    last_exception = None
    while time() - begin <= timeout:
        try:
            (last_code, _) = request_heartbeat(host=host, port=port, scheme=scheme, timeout=timeout)
            if last_code == 200:
                return
        except Exception as e:
            last_exception = e
    if last_exception:
        raise last_exception
    else:
        params = f'url={scheme}://{host}:{port},timeout={timeout}s,code={last_code}'
        raise TimeoutError(f'Heartbeat timeout ({params})')

def request_version(host: str, port: int, scheme=DEFAULT_SCHEME, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) -> Tuple[int, Optional[str]]:
    return request(host=host, port=port, path=u.api_version, scheme=scheme, timeout=timeout)

def has_http_scheme(address: str) -> bool:
    return match('^http(s)?://.*', address) is not None
_T = TypeVar('_T')

class HttpClient:

    def __init__(self, address: str, *, timeout: Optional[float]=None, scheme: Optional[str]=None):
        if has_http_scheme(address):
            if scheme is not None:
                raise ValueError('The `schema` argument cannot be usedif `address` contains a schema')
            self.prefix = address
        elif scheme:
            self.prefix = f'{scheme}://{address}'
        else:
            self.prefix = f'{DEFAULT_SCHEME}://{address}'
        total_timeout = timeout if timeout else DEFAULT_REQUEST_TIMEOUT_SECONDS
        self.timeout = ClientTimeout(total=total_timeout)
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    @property
    def origin(self) -> str:
        if self.prefix[-1] == URI_PATH_SEPARATOR:
            return f'{self.prefix[0:-1]}'
        else:
            return f'{self.prefix}'

    @property
    def scheme(self) -> str:
        return urlparse(self.prefix).scheme

    @staticmethod
    def get_method_caller(method: str, session: ClientSession):
        if method == METH_HEAD:
            return session.head
        elif method == METH_GET:
            return session.get
        elif method == METH_DELETE:
            return session.delete
        elif method == METH_OPTIONS:
            return session.options
        elif method == METH_PATCH:
            return session.patch
        elif method == METH_POST:
            return session.post
        elif method == METH_PUT:
            return session.put
        else:
            raise NotImplementedError

    async def request(self, method: str, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        if path:
            origin = self.origin
            assert origin[-1] != URI_PATH_SEPARATOR
            if path[0] == URI_PATH_SEPARATOR:
                request_url = origin + path
            else:
                request_url = origin + URI_PATH_SEPARATOR + path
        else:
            request_url = self.prefix
        updated_headers = CIMultiDict[str]()
        if headers:
            for (key, value) in headers.items():
                updated_headers.add(key, value)
        if self.access_token and AUTHORIZATION not in updated_headers:
            token = BearerAuth(self.access_token).encode()
            updated_headers.add(AUTHORIZATION, token)
        request_body: str
        if text and data:
            raise ValueError('You must pass only one `text` or `data`')
        elif text:
            request_body = text
        elif data:
            request_body = global_json_encoder(serialize(data))
            if CONTENT_TYPE not in updated_headers:
                updated_headers.add(CONTENT_TYPE, str(MIME_APPLICATION_JSON_UTF8))
        else:
            request_body = ''
        await self.on_request_begin()
        try:
            async with ClientSession(timeout=self.timeout) as session:
                method_caller = self.get_method_caller(method, session)
                async with method_caller(url=request_url, data=request_body, headers=updated_headers) as response:
                    response_data: Any = None
                    if response.content_length > 0:
                        if response.status == HTTPStatus.OK and cls is not None:
                            response_data = payload_to_class(response.headers, await response.text(), cls)
                        elif response.content_type.startswith(APPLICATION_JSON):
                            response_data = await response.json()
                        else:
                            response_data = await response.text()
                    return HttpResponse(status=response.status, reason=response.reason, data=response_data, headers=response.headers)
        finally:
            await self.on_request_end()

    async def on_request_begin(self):
        pass

    async def on_request_end(self):
        pass

    async def get(self, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        return await self.request(METH_GET, path, headers, text, data, cls)

    async def post(self, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        return await self.request(METH_POST, path, headers, text, data, cls)

    async def patch(self, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        return await self.request(METH_PATCH, path, headers, text, data, cls)

    async def put(self, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        return await self.request(METH_PUT, path, headers, text, data, cls)

    async def delete(self, path: Optional[str]=None, headers: Optional[Dict[str, str]]=None, text: Optional[str]=None, data: Optional[Any]=None, cls: Optional[Type[_T]]=None) -> HttpResponse:
        return await self.request(METH_DELETE, path, headers, text, data, cls)

    async def signup_public(self, username: str, password: str) -> None:
        if not username:
            raise ValueError('A `username` argument is required.')
        if not password:
            raise ValueError('A `password` argument is required.')
        signup = SignupQ(username, SignupQ.encrypt_password(password))
        response = await self.post(v2_public_path(u.signup), data=signup)
        if response.status != HTTPStatus.OK:
            raise RuntimeError(f'Signup status error: {response.status}')

    async def signup_admin(self, username: str, password: str) -> None:
        signup = SignupQ(username, SignupQ.encrypt_password(password))
        response = await self.post(v2_public_path(u.signup_admin), data=signup)
        if response.status == HTTPStatus.SERVICE_UNAVAILABLE:
            pass
        elif response.status != HTTPStatus.OK:
            raise RuntimeError(f'Signup status error: {response.status}')

    async def signin(self, username: str, password: str, save_session=False) -> SigninA:
        auth = BasicAuth(username, SignupQ.encrypt_password(password))
        headers = {str(AUTHORIZATION): auth.encode()}
        response = await self.post(v2_public_path(u.signin), headers=headers, cls=SigninA)
        if response.status != HTTPStatus.OK:
            raise RuntimeError(f'Login status error: {response.status}')
        result = response.data
        assert result is not None
        assert result.user is not None
        assert isinstance(result, SigninA)
        if save_session:
            self.username = username
            self.password = password
            self.access_token = result.access
            self.refresh_token = result.refresh
        return result

    async def signup_and_in(self, username: str, password: str, save_session=True) -> None:
        if not username:
            raise ValueError('A `username` argument is required.')
        if not password:
            raise ValueError('A `password` argument is required.')
        await self.signup_admin(username, password)
        await self.signin(username, password, save_session=save_session)

    @staticmethod
    def join_urls(*paths: str, **kwargs: str) -> str:
        path = join_urls(*paths)
        return path.format(**kwargs) if kwargs else path