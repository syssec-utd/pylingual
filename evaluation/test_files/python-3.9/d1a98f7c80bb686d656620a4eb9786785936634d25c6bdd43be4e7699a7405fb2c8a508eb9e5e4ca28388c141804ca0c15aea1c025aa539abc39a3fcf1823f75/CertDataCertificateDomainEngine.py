import requests
from netbluemind.python import serder
from enum import Enum

class CertDataCertificateDomainEngine(Enum):
    FILE = 'FILE'
    LETS_ENCRYPT = 'LETS_ENCRYPT'
    DISABLED = 'DISABLED'

class __CertDataCertificateDomainEngineSerDer__:

    def __init__(self):
        pass

    def parse(self, value):
        if value == None:
            return None
        instance = CertDataCertificateDomainEngine[value]
        return instance

    def encode(self, value):
        if value == None:
            return None
        instance = value.value
        return instance