import requests
import json
from netbluemind.python import serder
from netbluemind.python.client import BaseEndpoint
ISecurityToken_VERSION = '4.1.65076'

class ISecurityToken(BaseEndpoint):

    def __init__(self, apiKey, url, sessionIdentifier):
        self.url = url
        self.apiKey = apiKey
        self.base = url + '/auth/token/{sessionIdentifier}'
        self.sessionIdentifier_ = sessionIdentifier
        self.base = self.base.replace('{sessionIdentifier}', sessionIdentifier)

    def upgrade(self):
        postUri = '/_upgrade'
        __data__ = None
        __encoded__ = None
        queryParams = {}
        response = requests.put(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ISecurityToken_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def destroy(self):
        postUri = '/_delete'
        __data__ = None
        __encoded__ = None
        queryParams = {}
        response = requests.delete(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ISecurityToken_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)

    def renew(self):
        postUri = '/_renew'
        __data__ = None
        __encoded__ = None
        queryParams = {}
        response = requests.post(self.base + postUri, params=queryParams, verify=False, headers={'X-BM-ApiKey': self.apiKey, 'Accept': 'application/json', 'X-BM-ClientVersion': ISecurityToken_VERSION}, data=__encoded__)
        return self.handleResult__(None, response)