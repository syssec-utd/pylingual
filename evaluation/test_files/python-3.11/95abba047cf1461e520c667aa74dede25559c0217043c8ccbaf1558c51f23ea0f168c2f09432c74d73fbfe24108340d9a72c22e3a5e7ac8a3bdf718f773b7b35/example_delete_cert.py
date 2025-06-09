import json
from volcengine.live.LiveService import LiveService
if __name__ == '__main__':
    live_service = LiveService()
    ak = ''
    sk = ''
    live_service.set_ak(ak)
    live_service.set_sk(sk)
    body = {'ChainID': ''}
    resp = live_service.delete_cert(body)
    print(resp)