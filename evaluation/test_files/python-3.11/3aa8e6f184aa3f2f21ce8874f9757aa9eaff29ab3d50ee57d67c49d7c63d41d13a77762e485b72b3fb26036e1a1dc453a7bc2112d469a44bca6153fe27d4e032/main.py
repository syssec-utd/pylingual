import logging
from pprint import pprint
from schematics import types
from simplelogin.client import Client
from simplelogin import SimpleLoginApi
from simplelogin.definitions import Endpoint
API_KEY = 'tbuciuzwtovorvpkfwzteilpspzrajidtmdcquiwtacypnmxuuoitwxswtsp'
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = Client(API_KEY)
    api = SimpleLoginApi(client)
    pprint(api.get_user_info().to_native())