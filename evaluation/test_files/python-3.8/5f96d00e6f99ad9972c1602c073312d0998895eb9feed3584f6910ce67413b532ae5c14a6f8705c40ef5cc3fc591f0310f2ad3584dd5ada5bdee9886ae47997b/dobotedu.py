from DobotRPC import loggers, RPCClient, DobotlinkAdapter, NormalAdapter
from .function import Util, Face, Speech, Nlp, Ocr, Robot, Tmt
from .pyimageom import Pyimageom
from .device import LiteApi, MagicBoxApi, MagicianApi, MagicianGoApi, BetaGoApi
import requests
import json
import sounddevice
import soundfile
import playsound
import scipy
loggers.set_use_file(False)

class DobotEDU(object):

    def __init__(self, account: str=None, password: str=None):
        if account is not None and password is not None:
            try:
                url = 'https://dobotlab.dobot.cc/api/auth/login'
                headers = {'Content-Type': 'application/json'}
                payload = {'account': account, 'password': password}
                r = requests.post(url, headers=headers, data=json.dumps(payload))
                data = json.loads(r.content.decode())
                status = data['status']
                if status == 'error':
                    raise Exception(data['message'])
                token = data['data']['token']
            except Exception as e:
                token = None
                loggers.get('DobotEDU').exception(e)
                loggers.get('DobotEDU').error(f'Please check that the account name and password are correct.If correct, please contact the technician:{e}')
        else:
            token = None
            loggers.get('DobotEDU').info('You have not entered your username and password. AI API cannot be used!')
        self._rpc_client = RPCClient()
        self._py_rpc_client = RPCClient(port=10001)
        self._adapter = DobotlinkAdapter(self._rpc_client, is_sync=True)
        self._py_adapter = NormalAdapter(rpc_client=self._py_rpc_client, is_sync=True)
        self.__magician_api = MagicianApi(rpc_adapter=self._adapter)
        self.__lite_api = LiteApi(rpc_adapter=self._adapter)
        self.__magicbox_api = MagicBoxApi(rpc_adapter=self._adapter)
        self.__magiciango_api = MagicianGoApi(rpc_adapter=self._adapter)
        self.__betago = BetaGoApi(rpc_adapter=self._adapter)
        self.__dobot_objects = [self.__magician_api, self.__lite_api, self.__magicbox_api, self.__magiciango_api, self.__betago]
        self.__pyimageom = Pyimageom(rpc_adapter=self._py_adapter)
        self.__util = Util()
        self.__token = token
        self.__robot = Robot(self.__token)
        self.__face = Face(self.__token)
        self.__ocr = Ocr(self.__token)
        self.__nlp = Nlp(self.__token)
        self.__speech = Speech(self.__token)
        self.__tmt = Tmt(self.__token)
        self.__ai_objects = [self.__robot, self.__face, self.__ocr, self.__nlp, self.__speech, self.__tmt]

    def set_portname(self, port_name: str):
        for o in self.__dobot_objects:
            o._port_name = port_name

    def set_pause(self, on_pause):
        for i in self.__ai_objects:
            i.set_pause(on_pause)
        self.__util.set_pause(on_pause)
        self.__pyimageom.set_pause(on_pause)
        for o in self.__dobot_objects:
            o.set_pause(on_pause)

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token
        for i in self.__ai_objects:
            i.token = token

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url: str):
        for i in self.__ai_objects:
            i.url = url

    @property
    def face(self):
        return self.__face

    @property
    def ocr(self):
        return self.__ocr

    @property
    def nlp(self):
        return self.__nlp

    @property
    def speech(self):
        return self.__speech

    @property
    def robot(self):
        return self.__robot

    @property
    def tmt(self):
        return self.__tmt

    @property
    def util(self):
        return self.__util

    @property
    def pyimageom(self):
        return self.__pyimageom

    @property
    def beta_go(self):
        return self.__betago

    @property
    def magician(self):
        return self.__magician_api

    @property
    def m_lite(self):
        return self.__lite_api

    @property
    def magicbox(self):
        return self.__magicbox_api

    @property
    def magiciango(self):
        return self.__magiciango_api