from getpass import getpass
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urljoin, urlparse
from tinynetrc import Netrc
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.run_utils import resolve_tracking_uri
CREDENTIALS_DIR = Path.home() / '.mlfoundry'
CREDENTIALS_FILE = CREDENTIALS_DIR / 'credentials.netrc'

def login(tracking_uri: Optional[str]=None, relogin: bool=False, api_key: Optional[str]=None) -> bool:
    """Save API key in local file system for a given `tracking_uri`.

    Args:
        tracking_uri (Optional[str], optional): tracking_uri for the given API key
        relogin (bool, optional): Overwrites the existing API key for the `tracking_uri` if
            set to `True`. If set to `False` and an API key is already present for
            the given `tracking_uri`, then the existing API key is kept untouched.
            Default is `False`.
        api_key (Optional[str], optional): The API key for the given `tracking_uri`.
            If `api_key` is not passed, this function prompts for the API key.

    Returns:
        bool: Returns `True` if the given API Key was persisted.
    """
    tracking_uri = resolve_tracking_uri(tracking_uri)
    return _Login(tracking_uri).login(relogin=relogin, api_key=api_key)

def get_stored_api_key(tracking_uri: str) -> Optional[str]:
    """Get API key for a `tracking_uri` from the local file system.

    Args:
        tracking_uri (str): tracking_uri

    Returns:
        Optional[str]: The stored API key for the `tracking_uri`. If not present
            then this function returns `None`.
    """
    return _Login(tracking_uri).fetch_api_key()

def _prompt_api_key(tracking_uri: str) -> str:
    api_key_link = urljoin(tracking_uri, '/settings')
    print(f'Please get your API key from {api_key_link}')
    api_key = getpass('Paste your API key and hit enter:')
    return api_key

class _Login:

    def __init__(self, tracking_uri: str, credentials_file_path: Union[Path, str]=CREDENTIALS_FILE):
        self.tracking_uri = tracking_uri
        self.tracking_host = urlparse(tracking_uri).netloc
        if not self.tracking_host:
            raise MlFoundryException(f'invalid url: {tracking_uri}')
        self.credentials_file_path = Path(credentials_file_path).absolute()
        if not self.credentials_file_path.exists():
            self.credentials_file_path.parent.mkdir(exist_ok=True, parents=True)
            self.credentials_file_path.touch(exist_ok=True)

    def fetch_api_key(self) -> Optional[str]:
        return Netrc(self.credentials_file_path)[self.tracking_host]['password']

    def login(self, relogin: bool=False, api_key: Optional[str]=None) -> bool:
        if relogin:
            api_key = api_key or _prompt_api_key(self.tracking_uri)
            self._save_api_key(api_key)
            return True
        existing_api_key = self.fetch_api_key()
        if not existing_api_key:
            api_key = api_key or _prompt_api_key(self.tracking_uri)
            self._save_api_key(api_key)
            return True
        print('API key is already configured.\nPlease use `mlfoundry login --relogin` or `mlfoundry.login(relogin=True)`to force relogin')
        return False

    def _save_api_key(self, api_key: str):
        print(f'Writing API key at {self.credentials_file_path}')
        with Netrc(self.credentials_file_path) as netrc:
            netrc[self.tracking_host]['password'] = api_key