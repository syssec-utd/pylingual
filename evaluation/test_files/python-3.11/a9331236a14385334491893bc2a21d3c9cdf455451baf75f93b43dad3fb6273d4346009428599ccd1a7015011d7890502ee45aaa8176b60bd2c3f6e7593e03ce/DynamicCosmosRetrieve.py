import requests
import json
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.identity import ClientSecretCredential

class DynamicCosmosRetrieve:

    def __init__(self, kv_client_id, kv_client_secret, kv_tenant_id, key_vault_name, kv_func_url_key, kv_func_master_key):
        self.kv_client_id = kv_client_id
        self.kv_client_secret = kv_client_secret
        self.kv_tenant_id = kv_tenant_id
        self.key_vault_name = key_vault_name
        self.kv_func_url_key = kv_func_url_key
        self.kv_func_master_key = kv_func_master_key

    def authenticate_key_vault(self):
        credential = ClientSecretCredential(client_id=self.kv_client_id, client_secret=self.kv_client_secret, tenant_id=self.kv_tenant_id)
        return credential

    def kv_connect(self):
        KVUri = f'https://{self.key_vault_name}.vault.azure.net'
        credential = self.authenticate_key_vault()
        client = SecretClient(vault_url=KVUri, credential=credential)
        return client

    def kv_get_secret(self, client, secret_name):
        retrieved_secret = client.get_secret(secret_name)
        secret_value = retrieved_secret.value
        return secret_value

    def get_response(self, tenant):
        client = self.kv_connect()
        funcURL = self.kv_get_secret(client, self.kv_func_url_key)
        funcMasterKey = self.kv_get_secret(client, self.kv_func_master_key)
        funcURL = funcURL + tenant
        response = requests.get(funcURL, headers={'x-functions-key': funcMasterKey})
        self.jsonResponse = json.loads(response.text)

    def get_cosmos_details(self):
        return_cosmos_details = {}
        return_cosmos_details['cosmos_host'] = self.jsonResponse['appSettings']['tenantDBAppSettings']['endpointUrl']
        return_cosmos_details['cosmos_master_key'] = self.jsonResponse['appSettings']['tenantDBAppSettings']['primaryKey']
        return return_cosmos_details

    def get_instance_details(self):
        return_instance_details = {}
        app_settings = self.jsonResponse['appSettings']
        azure_datalake_settings = app_settings['azureDataLakeGen2Settings']
        return_instance_details['storage_access_key'] = azure_datalake_settings['accountKey']
        return_instance_details['storage_account_name'] = azure_datalake_settings['accountName']
        return_instance_details['storage_container_name'] = azure_datalake_settings['containerName']
        databricksADLSGen2AppSettings = app_settings['databricksADLSGen2AppSettings']
        return_instance_details['tenant_id'] = databricksADLSGen2AppSettings['tenantId']
        return_instance_details['app_id'] = databricksADLSGen2AppSettings['appId']
        return_instance_details['app_key'] = databricksADLSGen2AppSettings['appSecret']
        azureCognitiveSearchSettings = app_settings['azureCognitiveSearchSettings']
        return_instance_details['search_service_name'] = azureCognitiveSearchSettings['searchServiceName']
        return_instance_details['search_service_admin_key'] = azureCognitiveSearchSettings['searchServiceAdminKey']
        return return_instance_details