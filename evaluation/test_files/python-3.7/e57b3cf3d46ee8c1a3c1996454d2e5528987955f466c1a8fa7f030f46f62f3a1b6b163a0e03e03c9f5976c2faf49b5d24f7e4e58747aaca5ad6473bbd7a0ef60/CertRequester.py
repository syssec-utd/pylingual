import os
from pathlib import Path
import requests
from requests import Response

class CertRequester(requests.Session):

    def __init__(self, cert_path: Path, key_path: Path, first_part_url: str=''):
        super().__init__()
        self.cert_path = cert_path
        self.key_path = key_path
        self.first_part_url = first_part_url
        if not os.path.isfile(cert_path):
            raise FileNotFoundError(f'{cert_path} is not a valid path. Cert file does not exist.')
        if not os.path.isfile(key_path):
            raise FileNotFoundError(f'{key_path} is not a valid path. Key file does not exist.')

    def get(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().get(url=self.first_part_url + url, cert=(self.cert_path, self.key_path), **kwargs)

    def post(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().post(url=self.first_part_url + url, cert=(self.cert_path, self.key_path), **kwargs)

    def put(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().put(url=self.first_part_url + url, cert=(self.cert_path, self.key_path), **kwargs)

    def patch(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().patch(url=self.first_part_url + url, cert=(self.cert_path, self.key_path), **kwargs)

    def delete(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().delete(url=self.first_part_url + url, cert=(self.cert_path, self.key_path), **kwargs)

    @staticmethod
    def modify_kwargs_for_bearer_token(kwargs: dict) -> dict:
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        for arg in kwargs:
            if arg == 'headers':
                headers = kwargs[arg]
                if 'accept' not in headers:
                    headers['accept'] = ''
                if headers['accept'] is not None:
                    if headers['accept'] != '':
                        headers['accept'] = headers['accept'] + ', application/json'
                    else:
                        headers['accept'] = 'application/json'
                headers['Content-Type'] = 'application/vnd.awv.eminfra.v1+json'
                kwargs['headers'] = headers
        return kwargs