import requests
import json
import os
import gzip
import shutil
import platform

class History(object):
    OK = 200
    _BASE_URL = 'https://data.thinknum.com'

    def __init__(self, client_id, client_secret, proxies={}, verify=True):
        self._client_id = client_id
        self._client_secret = client_secret
        self._proxies = proxies
        self._verify = verify
        self._token = None
        self._authenticate()
        self._headers = {'Authorization': 'token {token}'.format(token=self._token), 'X-API-Version': '20151130', 'Accept': 'application/json', 'User-Agent': 'Python API 1.94 / {local_version}'.format(local_version=platform.python_version())}
        self._dataset_id = None

    def _requests(self, method, url, headers={}, data={}, json={}, params={}, stream=False, allow_redirects=True):
        if method not in ['post', 'get']:
            raise Exception('Not allowed method')
        return getattr(requests, method)(url, headers=headers, data=data, json=json, params=params, stream=stream, proxies=self._proxies, verify=self._verify, allow_redirects=allow_redirects)

    def _authenticate(self):
        response = self._requests(method='post', url='{base_url}/api/authorize'.format(base_url=self._BASE_URL), data={'version': '20151130', 'client_id': self._client_id, 'client_secret': self._client_secret})
        if response.status_code != self.OK:
            raise Exception('Invalid autentication')
        self._token = json.loads(response.text)['auth_token']

    def get_dataset_list(self):
        response = self._requests(method='get', url='{base_url}/datasets/'.format(base_url=self._BASE_URL), headers=self._headers)
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)
        return json.loads(response.text).get('datasets', [])

    def get_history_list(self, dataset_id):
        if not dataset_id:
            raise Exception('Invalid dataset_id')
        response = self._requests(method='get', url='{base_url}/datasets/{dataset_id}/history/'.format(base_url=self._BASE_URL, dataset_id=dataset_id), headers=self._headers)
        history = json.loads(response.text)['history']
        return history

    def get_history_metadata(self, dataset_id, history_date):
        if not dataset_id:
            raise Exception('Invalid dataset_id')
        if not history_date:
            raise Exception('Invalid history_date')
        response = self._requests(method='get', url='{base_url}/datasets/{dataset_id}/history/{history_date}'.format(base_url=self._BASE_URL, dataset_id=dataset_id, history_date=history_date), headers=self._headers)
        return json.loads(response.text)

    def get_url(self, dataset_id, history_date):
        if not dataset_id:
            raise Exception('Invalid dataset_id')
        if not history_date:
            raise Exception('Invalid history_date')
        response = self._requests(method='get', url='{base_url}/datasets/{dataset_id}/history/{history_date}'.format(base_url=self._BASE_URL, dataset_id=dataset_id, history_date=history_date), headers=dict(self._headers, **{'Accept': 'text/csv', 'Accept-Encoding': 'gzip'}), allow_redirects=False)
        return response.headers['Location']

    def download(self, dataset_id, history_date, download_path=None, is_compressed=False):
        if not dataset_id:
            raise Exception('Invalid dataset_id')
        if not history_date:
            raise Exception('Invalid history_date')
        if not download_path:
            download_path = os.path.abspath(os.getcwd())
        with self._requests(method='get', url='{base_url}/datasets/{dataset_id}/history/{history_date}'.format(base_url=self._BASE_URL, dataset_id=dataset_id, history_date=history_date), headers=dict(self._headers, **{'Accept': 'text/csv', 'Accept-Encoding': 'gzip'}), stream=True) as r:
            gz_filepath = '{download_path}/{dataset_id}_{history_date}.csv.gz'.format(download_path=download_path, dataset_id=dataset_id, history_date=history_date)
            with open(gz_filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            if is_compressed:
                return gz_filepath
            csv_filepath = '{download_path}/{dataset_id}_{history_date}.csv'.format(download_path=download_path, dataset_id=dataset_id, history_date=history_date)
            with gzip.open(gz_filepath, 'rb') as f_in:
                with open(csv_filepath, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(gz_filepath)
            return csv_filepath