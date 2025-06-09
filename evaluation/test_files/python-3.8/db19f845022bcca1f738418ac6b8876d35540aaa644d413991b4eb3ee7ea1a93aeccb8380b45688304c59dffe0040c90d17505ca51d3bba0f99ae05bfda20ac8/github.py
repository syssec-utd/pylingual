import os
import getpass
import base64
import functools
import re
import pathlib
import itertools
import keyring
import nacl.public
import nacl.encoding
from requests_toolbelt import sessions
from . import repo

class Key(str):
    pass

class Repo(str):

    def __init__(self, name):
        self.session = self.get_session()

    @classmethod
    @functools.lru_cache()
    def get_session(cls):
        session = sessions.BaseUrlSession('https://api.github.com/repos/')
        session.headers.update(Accept='application/vnd.github.v3+json', Authorization=f'token {cls.load_token()}')
        return session

    @staticmethod
    def load_token():
        token = os.environ.get('GITHUB_TOKEN') or keyring.get_password('Github', username())
        assert token, 'Token not available'
        return token

    @classmethod
    def detect(cls):
        return cls(repo.get_project_metadata().project)

    @functools.lru_cache()
    def get_public_key(self):
        data = self.session.get(f'{self}/actions/secrets/public-key').json()
        key = Key(data['key'])
        key.id = data['key_id']
        return key

    def encrypt(self, value):
        src = self.get_public_key().encode('utf-8')
        pub_key = nacl.public.PublicKey(src, nacl.encoding.Base64Encoder())
        box = nacl.public.SealedBox(pub_key)
        cipher_text = box.encrypt(value.encode('utf-8'))
        return base64.b64encode(cipher_text).decode('utf-8')

    def add_secret(self, name, value):
        secret = f'{self}/actions/secrets/{name}'
        params = dict(encrypted_value=self.encrypt(value), key_id=self.get_public_key().id)
        resp = self.session.put(secret, json=params)
        resp.raise_for_status()
        return resp

    def create_release(self, tag):
        releases = f'{self}/releases'
        resp = self.session.post(releases, json=dict(tag_name=tag, name=tag))
        resp.raise_for_status()
        return resp

    @classmethod
    def find_needed_secrets(cls):
        """
        >>> list(Repo.find_needed_secrets())
        ['PYPI_TOKEN']
        """
        workflows = pathlib.Path('.github/workflows').iterdir()
        all = itertools.chain.from_iterable(map(cls.find_secrets, workflows))
        return itertools.filterfalse('GITHUB_TOKEN'.__eq__, all)

    @staticmethod
    def find_secrets(file):
        return (match.group(1) for match in re.finditer('\\${{\\s*secrets\\.(\\w+)\\s*}}', file.read_text()))

def username():
    return os.environ.get('GITHUB_USERNAME') or getpass.getuser()