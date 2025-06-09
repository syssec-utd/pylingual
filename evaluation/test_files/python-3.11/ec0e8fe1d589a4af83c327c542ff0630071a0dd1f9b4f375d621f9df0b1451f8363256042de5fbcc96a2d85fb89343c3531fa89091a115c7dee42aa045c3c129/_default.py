import logging
import os
from azure.identity import InteractiveBrowserCredential, DeviceCodeCredential
import requests
import re
from azure.identity._constants import EnvironmentVariables
from azure.identity._internal import get_default_authority, normalize_authority
from azure.identity.aio import AzurePowerShellCredential, EnvironmentCredential, ManagedIdentityCredential, SharedTokenCacheCredential, AzureCliCredential, VisualStudioCodeCredential
from ._chained import _ChainedTokenCredential
from ._token import _TokenFileCredential
try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, List
    from azure.core.credentials_async import AccessToken, AsyncTokenCredential
_LOGGER = logging.getLogger(__name__)

class _DefaultAzureCredential(_ChainedTokenCredential):
    """
    Based on Azure.Identity.DefaultAzureCredential from:
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/identity/azure-identity/azure/identity/_credentials/default.py

    The two key differences are:
    1) Inherit from _ChainedTokenCredential, which has 
       more aggressive error handling than ChainedTokenCredential
    2) Instantiate the internal credentials the first time the get_token gets called
       such that we can get the tenant_id if it was not passed by the user (but we don't
       want to do that in the constructor).
       We automatically identify the user's tenant_id for a given subscription 
       so that users with MSA accounts don't need to pass it.
       This is a mitigation for bug https://github.com/Azure/azure-sdk-for-python/issues/18975
       We need the following parameters to enable auto-detection of tenant_id
       - subscription_id
       - arm_base_url (defaults to the production url "https://management.azure.com/")
    """

    def __init__(self, **kwargs):
        self._successfull_tenant_id = None
        self.authority = kwargs.pop('authority', None)
        self.authority = normalize_authority(self.authority) if self.authority else get_default_authority()
        self.interactive_browser_tenant_id = kwargs.pop('interactive_browser_tenant_id', os.environ.get(EnvironmentVariables.AZURE_TENANT_ID))
        self.subscription_id = kwargs.pop('subscription_id', os.environ.get('SUBSCRIPTION_ID'))
        self.arm_base_url = kwargs.pop('arm_base_url', 'https://management.azure.com/')
        self.managed_identity_client_id = kwargs.pop('managed_identity_client_id', os.environ.get(EnvironmentVariables.AZURE_CLIENT_ID))
        self.shared_cache_username = kwargs.pop('shared_cache_username', os.environ.get(EnvironmentVariables.AZURE_USERNAME))
        self.shared_cache_tenant_id = kwargs.pop('shared_cache_tenant_id', os.environ.get(EnvironmentVariables.AZURE_TENANT_ID))
        self.vscode_tenant_id = kwargs.pop('visual_studio_code_tenant_id', os.environ.get(EnvironmentVariables.AZURE_TENANT_ID))
        self.exclude_token_file_credential = kwargs.pop('exclude_token_file_credential', False)
        self.exclude_environment_credential = kwargs.pop('exclude_environment_credential', False)
        self.exclude_managed_identity_credential = kwargs.pop('exclude_managed_identity_credential', False)
        self.exclude_shared_token_cache_credential = kwargs.pop('exclude_shared_token_cache_credential', False)
        self.exclude_visual_studio_code_credential = kwargs.pop('exclude_visual_studio_code_credential', False)
        self.exclude_cli_credential = kwargs.pop('exclude_cli_credential', False)
        self.exclude_interactive_browser_credential = kwargs.pop('exclude_interactive_browser_credential', True)
        self.exclude_device_code_credential = kwargs.pop('exclude_device_code_credential', False)
        self.exclude_powershell_credential = kwargs.pop('exclude_powershell_credential', False)
        super(_DefaultAzureCredential, self).__init__()

    def _initialize_credentials(self):
        if self.subscription_id is not None and self.arm_base_url is not None:
            if self.vscode_tenant_id is None:
                self.vscode_tenant_id = self._get_tenant_id(arm_base_url=self.arm_base_url, subscription_id=self.subscription_id)
            if self.shared_cache_tenant_id is None:
                self.shared_cache_tenant_id = self._get_tenant_id(arm_base_url=self.arm_base_url, subscription_id=self.subscription_id)
            if self.interactive_browser_tenant_id is None:
                self.interactive_browser_tenant_id = self._get_tenant_id(arm_base_url=self.arm_base_url, subscription_id=self.subscription_id)
        credentials = []
        if not self.exclude_token_file_credential:
            credentials.append(_TokenFileCredential())
        if not self.exclude_environment_credential:
            credentials.append(EnvironmentCredential(authority=self.authority))
        if not self.exclude_managed_identity_credential:
            credentials.append(ManagedIdentityCredential(client_id=self.managed_identity_client_id))
        if not self.exclude_shared_token_cache_credential and SharedTokenCacheCredential.supported():
            try:
                shared_cache = SharedTokenCacheCredential(username=self.shared_cache_username, tenant_id=self.shared_cache_tenant_id, authority=self.authority)
                credentials.append(shared_cache)
            except Exception as ex:
                _LOGGER.info("Shared token cache is unavailable: '%s'", ex)
        if not self.exclude_visual_studio_code_credential:
            credentials.append(VisualStudioCodeCredential(tenant_id=self.vscode_tenant_id))
        if not self.exclude_cli_credential:
            credentials.append(AzureCliCredential())
        if not self.exclude_powershell_credential:
            credentials.append(AzurePowerShellCredential())
        if not self.exclude_interactive_browser_credential:
            credentials.append(InteractiveBrowserCredential(tenant_id=self.interactive_browser_tenant_id))
        if not self.exclude_device_code_credential:
            credentials.append(DeviceCodeCredential(tenant_id=self.interactive_browser_tenant_id))
        self.credentials = credentials

    async def get_token(self, *scopes, **kwargs):
        """Request an access token for `scopes`.
        This method is called automatically by Azure SDK clients.
        :param str scopes: desired scopes for the access token. This method requires at least one scope.
        :raises ~azure.core.exceptions.ClientAuthenticationError: authentication failed. The exception has a
          `message` attribute listing each authentication attempt and its error message.
        """
        if self.credentials is None or len(self.credentials) == 0:
            self._initialize_credentials()
        return await super(_DefaultAzureCredential, self).get_token(*scopes, **kwargs)

    def _get_tenant_id(self, arm_base_url: str, subscription_id: str):
        if arm_base_url is None:
            raise ValueError('arm_base_url is mandatory parameter')
        if subscription_id is None:
            raise ValueError('subscription_id is mandatory parameter')
        if self._successfull_tenant_id is not None:
            return self._successfull_tenant_id
        try:
            uri = f'{arm_base_url}/subscriptions/' + f'{subscription_id}?api-version=2018-01-01'
            response = requests.get(uri)
            auth_header = response.headers['WWW-Authenticate']
            _LOGGER.debug(f"{'got the following auth header from'}the management endpoint: {auth_header}")
            trimmed_auth_header = auth_header[len('Bearer '):]
            trimmed_auth_header_parts = trimmed_auth_header.split(',')
            key_value_pairs = dict(map(lambda s: tuple(s.split('=')), trimmed_auth_header_parts))
            quoted_tenant_uri = key_value_pairs['authorization_uri']
            tenant_uri = quoted_tenant_uri[1:-1]
            _LOGGER.debug(f"{'got the following tenant uri from'}" + f'the authentication header: {tenant_uri}')
            regex = re.compile(pattern='([a-f0-9]+[-]){4}[a-f0-9]+', flags=re.IGNORECASE)
            self._successfull_tenant_id = regex.search(tenant_uri).group()
            return self._successfull_tenant_id
        except Exception as e:
            _LOGGER.debug(f'Failed to get tenant authority for subscription: {e}')
            return None