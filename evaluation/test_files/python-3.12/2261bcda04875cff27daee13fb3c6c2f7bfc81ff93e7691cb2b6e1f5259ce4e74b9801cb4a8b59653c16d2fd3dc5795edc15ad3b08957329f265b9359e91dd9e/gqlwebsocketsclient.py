from gql.transport.websockets import WebsocketsTransport

class GQLWebsocketslientError(Exception):
    pass

class GQLWebsocketsClient:

    def __init__(self, token=None, url=None, use_ssl=True):
        init_payload = {}
        protocol = 'wss://' if use_ssl else 'ws://'
        if token:
            init_payload['Authorization'] = 'Bearer ' + token
        self.__transport = WebsocketsTransport(url=protocol + url, init_payload=init_payload)

    def transport(self):
        return self.__transport