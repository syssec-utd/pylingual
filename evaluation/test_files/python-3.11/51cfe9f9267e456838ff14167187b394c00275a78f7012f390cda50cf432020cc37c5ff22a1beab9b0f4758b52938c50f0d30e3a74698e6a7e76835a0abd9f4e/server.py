from i2cylib.crypto import DynKey16
from paho.mqtt import client
from i2cylib.network.I2TCP import Server, Handler
from i2cylib.utils import Logger, get_args, DirTree, i2TecHome
import json
if __name__ == '__main__':
    from config import DeviceConfig, Config
else:
    from config import DeviceConfig, Config
import time
import os
import threading
FEEDBACK_TOPIC = 'data'
CMD_TOPIC = 'request'
SYSTEMD_PATH = '/etc/systemd/system/i2llserver.service'

class PahoMqttSessionFlags(object):

    class __StatusObject(object):

        def __init__(self, is_connected, status):
            self.is_connected = is_connected
            self.status = status
    __flags = ['', 'incorrect protocol version', 'invalid client id', 'server is not available', 'invalid username or password', 'unauthorised visit']

    def __init__(self):
        pass

    def __getitem__(self, item):
        assert isinstance(item, int)
        if not item:
            ret = self.__StatusObject(True, self.__flags[item])
        elif 0 < item < 6:
            ret = self.__StatusObject(False, self.__flags[item])
        else:
            ret = self.__StatusObject(False, 'unknown error')
        return ret

class LLMqttClient:

    def __init__(self, parent, device_config, watchdog_timeout=30):
        assert isinstance(parent, LLServer)
        assert isinstance(device_config, DeviceConfig)
        self.__parent = parent
        self.__client = parent.getMqttClient()
        assert isinstance(self.__client, client.Client)
        self.device_config = device_config
        self.topic_root = self.device_config.root_topic
        if self.topic_root[-1] == '/':
            self.topic_root = self.topic_root[:-1]
        self.logger = parent.logger
        self.__log_header = '[MQTT] [{}]'.format(self.topic_root)
        self.is_online = False
        self.__online_wdog_t0 = 0
        self.watchdog_timeout = watchdog_timeout
        self.__flow_cnt = 0
        self.__last_received_flow_cnt = 0
        self.keygen = DynKey16(device_config.dynkey16_psk.encode())
        self.live = True
        threading.Thread(target=self.__onlineWatchdog).start()

    def __onlineWatchdog(self):
        cnt = 0
        subscribed = False
        while self.__parent.live and self.live:
            if cnt < 20:
                time.sleep(0.1)
                cnt += 1
            else:
                if not subscribed and self.__client.is_connected():
                    try:
                        self.__client.subscribe(self.topic_root + '/' + FEEDBACK_TOPIC)
                        self.logger.INFO('{} feedback topic "{}" subscribed'.format(self.__log_header, self.topic_root + '/' + FEEDBACK_TOPIC))
                        subscribed = True
                    except Exception as err:
                        self.logger.ERROR('{} failed to subscribe topic, {}'.format(self.__log_header, err))
                if subscribed:
                    subscribed = self.__client.is_connected()
                last = self.is_online
                self.is_online = time.time() - self.__online_wdog_t0 < self.watchdog_timeout
                if last != self.is_online:
                    if self.is_online:
                        self.logger.INFO('{} device is now online'.format(self.__log_header))
                    else:
                        self.logger.WARNING('{} device is now offline'.format(self.__log_header))
                cnt = 0
                time.sleep(0.1)

    def __feedWatchdog(self):
        self.__online_wdog_t0 = time.time()

    def __encodePackage(self, cmd_id, payload):
        status = False
        data = b''
        try:
            data += bytes((self.__flow_cnt,))
            self.__flow_cnt += 1
            data += bytes((cmd_id,))
            data += int(len(payload)).to_bytes(2, 'big', signed=False)
            data += payload
            data += bytes((sum(data) % 256,))
            status = True
        except Exception as err:
            self.logger.WARNING('{} [decoder] failed to encode package, {}, raw hex: {}'.format(self.__log_header, err, data.hex()))
        return (status, data)

    def __decodePackage(self, data):
        status = False
        cmd_id = 0
        payload = b''
        try:
            self.__last_received_flow_cnt = data[0]
            cmd_id = data[1]
            length = int().from_bytes(data[2:4], 'big', signed=False)
            payload = data[4:4 + length]
            check_sum = sum(data[0:-1]) % 256
            status = check_sum == data[-1]
        except Exception as err:
            self.logger.WARNING('{} [decoder] failed to decode package, {}, raw hex: {}'.format(self.__log_header, err, data.hex()))
        return (status, cmd_id, payload)

    def messageHandler(self, msg):
        if len(self.topic_root) > len(msg.topic) or self.topic_root != msg.topic[:len(self.topic_root)]:
            return
        self.logger.DEBUG('{} [handler] received message: {}'.format(self.__log_header, msg.payload.hex()))
        status, cmd_id, payload = self.__decodePackage(msg.payload)
        if status:
            self.__feedWatchdog()
            if cmd_id == 0:
                self.__deviceTimeCheck(payload)
            elif cmd_id == 1:
                self.caliDeviceTime()
            elif cmd_id == 2:
                self.configurateDevice()
            elif cmd_id == 48:
                self.__storageOffset(payload)
                self.sendOkFlag()
            elif cmd_id == 255:
                pass

    def __storageOffset(self, feedback_payload):
        offset = int().from_bytes(feedback_payload, 'little', signed=False)
        self.logger.INFO('{} motor calibrated, offset: {}'.format(self.__log_header, offset))
        self.device_config.storage['motor_offset'] = offset

    def __deviceTimeCheck(self, feedback_payload):
        now = time.time()
        feedback = int().from_bytes(feedback_payload, 'little', signed=False)
        if abs(now - feedback) > 15:
            self.logger.INFO('{} device time {}, is not synchronised with server, real time now {}'.format(self.__log_header, feedback, int(now)))
            self.caliDeviceTime()

    def sendOkFlag(self):
        status, data = self.__encodePackage(238, int(time.time()).to_bytes(4, 'big', signed=True))
        if status:
            self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
            self.logger.DEBUG('{} [cmd] sending ok flag'.format(self.__log_header))

    def caliDeviceTime(self):
        status, data = self.__encodePackage(17, int(time.time()).to_bytes(4, 'little', signed=True))
        if status:
            self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
            self.logger.DEBUG('{} [cmd] requesting time calibration'.format(self.__log_header))

    def configurateDevice(self):
        status, data = self.__encodePackage(18, int(self.device_config.storage['motor_offset']).to_bytes(4, 'little', signed=True))
        if status:
            self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
            self.logger.DEBUG('{} [cmd] configuring device'.format(self.__log_header))

    def caliMotorOffset(self):
        status, data = self.__encodePackage(19, int(time.time()).to_bytes(4, 'little', signed=True))
        if status:
            self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
            self.logger.DEBUG('{} [cmd] calibrating motor offset'.format(self.__log_header))

    def unlock(self):
        if self.is_online:
            status, data = self.__encodePackage(32, int(time.time()).to_bytes(4, 'little', signed=True))
            if status:
                self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
                self.logger.DEBUG('{} [cmd] requesting unlock remotely'.format(self.__log_header))
        return self.keygen.keygen()

    def ringMotor(self):
        status, data = self.__encodePackage(33, int(time.time()).to_bytes(4, 'little', signed=True))
        if status:
            self.__client.publish(self.topic_root + '/' + CMD_TOPIC, data)
            self.logger.DEBUG('{} [cmd] requesting motor ringing'.format(self.__log_header))

class LLServer(Server):

    def __init__(self, config, max_connections=20, secured_connection=True, max_buffer_size=50, watchdog_timeout=20):
        assert isinstance(config, Config)
        self.config = config
        self.__mqtt_flag_dict = PahoMqttSessionFlags()
        logger = Logger(config.log_file, level=config.log_level)
        super(LLServer, self).__init__(config.i2tcp_psk.encode('utf-8'), config.i2tcp_port, max_connections, logger, secured_connection, max_buffer_size, watchdog_timeout)
        self.__client = client.Client(self.config.mqtt_client_id)
        self.__client.username_pw_set(self.config.mqtt_user, self.config.mqtt_password)
        self.__client.on_connect = self.__onConnect
        self.__client.on_message = self.__onMessage
        self.__client.on_disconnect = self.__onDisconnect
        self.__client.reconnect_delay_set(1, 5)
        self.__ll_clients = []
        self.connection_status = self.__mqtt_flag_dict[255]
        self.__flag_mqtt_loop_running = False
        self.__flag_dead = False

    def __iter__(self):
        return self.__ll_clients

    def __len__(self):
        return len(self.__ll_clients)

    def __getitem__(self, item):
        return self.__ll_clients[item]

    def __onConnect(self, clt, userdata, flags, rc):
        self.connection_status = self.__mqtt_flag_dict[rc]
        if self.connection_status.is_connected:
            self.logger.INFO('[MQTT] successfully connected to host')
        else:
            self.logger.ERROR('[MQTT] failed to connect to MQTT server, {}, retrying'.format(self.connection_status.status))

    def __onMessage(self, clt, userdata, message):
        self.logger.DEBUG('[MQTT] [receiver] received massage from topic "{}"'.format(message.topic))
        for con in self.__ll_clients:
            assert isinstance(con, LLMqttClient)
            con.messageHandler(message)

    def __onDisconnect(self, clt, userdata, rc):
        self.connection_status = self.__mqtt_flag_dict[rc]
        self.logger.ERROR('[MQTT] unexpectedly disconnected from MQTT server, {}, retrying'.format(self.connection_status.status))

    def __i2tcpHandlerThread(self):
        self.threads.update({'i2tcpHandlerThread': True})
        handlers = []
        idle = False
        while self.live:
            con = self.get_connection(False)
            if isinstance(con, Handler):
                handlers.append(con)
            if idle:
                time.sleep(0.1)
            idle = True
            for con in handlers:
                if con.live:
                    pkg = con.get()
                    if pkg is not None:
                        con.logger.DEBUG('{} [I2LL] received command: {}'.format(con.log_header, pkg.hex()))
                        idle = False
                        cmd_id = pkg[0]
                        payload = pkg[1:]
                        if cmd_id == 1:
                            ret = b'\xf1'
                            ret += json.dumps(self.getAllMqttRootTopics()).encode('utf-8')
                            con.send(ret)
                        elif cmd_id == 16:
                            ret = b'\x01'
                            target_topic = payload.decode('utf-8')
                            clt = self.getDeviceClient(target_topic)
                            if clt is None:
                                ret += b'\x00'
                            elif clt.is_online:
                                ret += b'\x01'
                            else:
                                ret += b'\x00'
                            con.send(ret)
                        elif cmd_id == 17:
                            ret = b'\xe1'
                            target_topic = payload.decode('utf-8')
                            clt = self.getDeviceClient(target_topic)
                            if clt is not None:
                                ret += json.dumps(clt.device_config.storage).encode('utf-8')
                                con.send(ret)
                        elif cmd_id == 32:
                            ret = b'\x01\x01'
                            target_topic = payload.split(b',')[0].decode('utf-8')
                            json_dict = json.loads(payload[payload.index(b','):].decode('utf-8'))
                            clt = self.getDeviceClient(target_topic)
                            if clt is not None:
                                clt.device_config.storage.update(json_dict)
                                clt.configurateDevice()
                                con.send(ret)
                        elif cmd_id == 33:
                            ret = b'\x01\x01'
                            target_topic = payload.decode('utf-8')
                            clt = self.getDeviceClient(target_topic)
                            if clt is not None:
                                clt.caliMotorOffset()
                                con.send(ret)
                        elif cmd_id == 34:
                            ret = b'\xd2'
                            target_topic = payload.decode('utf-8')
                            clt = self.getDeviceClient(target_topic)
                            if clt is not None:
                                dynkey = clt.unlock()
                                con.send(ret + dynkey)
                        elif cmd_id == 35:
                            ret = b'\x01\x01'
                            target_topic = payload.decode('utf-8')
                            clt = self.getDeviceClient(target_topic)
                            if clt is not None:
                                clt.ringMotor()
                                con.send(ret)
            handlers = [ele for ele in handlers if ele.live]
        self.threads.update({'i2tcpHandlerThread': False})

    def __autoReconnectThread(self):
        self.threads.update({'mqttClientAutoReconnect': True})
        cnt = 50
        while self.live:
            if not self.__client.is_connected():
                cnt += 1
                time.sleep(0.1)
                if cnt > 50:
                    self.logger.INFO('[MQTT] connecting to MQTT server at {}:{}'.format(self.config.mqtt_host, self.config.mqtt_port))
                    try:
                        self.__client.connect(self.config.mqtt_host, self.config.mqtt_port)
                    except Exception as err:
                        self.logger.ERROR('[MQTT] failed to connect to MQTT server, {}, retrying in 5 seconds'.format(err))
                    cnt = 0
            try:
                self.__client.loop()
            except Exception as err:
                self.logger.ERROR('[MQTT] [loop] {}'.format(err))
        self.threads.update({'mqttClientAutoReconnect': False})

    def start(self, port=None):
        if self.__flag_dead:
            raise Exception('dead LL server')
        super(LLServer, self).start(port)
        threading.Thread(target=self.__autoReconnectThread).start()
        for device in self.config:
            self.__ll_clients.append(LLMqttClient(self, device))
        threading.Thread(target=self.__i2tcpHandlerThread).start()

    def kill(self):
        super(LLServer, self).kill()
        self.__ll_clients.clear()

    def getMqttClient(self):
        return self.__client

    def getAllMqttRootTopics(self):
        ret = []
        for con in self.__ll_clients:
            assert isinstance(con, LLMqttClient)
            ret.append(con.topic_root)
        return ret

    def getDeviceClient(self, root_topic):
        con: (LLMqttClient, None)
        for con in self.__ll_clients:
            assert isinstance(con, LLMqttClient)
            if con.topic_root in root_topic:
                return con

def manual():
    print('ESP32-S3 Locking Lock Cloud Service\n    \n    i2llserver [setup/config/init] [-c]\n    \n    Usage:\n        -c --config             - set config path\n        \n        setup config init       - initiate server with guidance\n    \n    Examples:\n    > i2llserver init\n    > i2llserver -c $HOME/.i2tec\n    \n    ')

def main():
    args = get_args()
    root = DirTree(i2TecHome(), 'i2ll')
    root.fixPath(False)
    config = root.join('config.json')
    init = False
    for opt in args:
        if opt in ('-c', '--config'):
            argv = DirTree(args[opt])
            if not argv.exists():
                print('warning: config "{}" dose not exists, falling back to default'.format(argv))
            else:
                config = argv
        if opt == 0:
            argv = args[opt]
            if argv in ('init', 'setup', 'config'):
                init = True
    if not config.exists():
        print('no configuration file detected, do you wish to setup server and generate config file?')
        choice = input('(input Y for yes, others for No): ').upper()
        if choice in ('Y', 'YES'):
            init = True
    if init:
        create_new_config = True
        if config.exists():
            try:
                Config(config)
                create_new_config = False
            except Exception as err:
                print('warning: config file corrupted, {}, should we replace it with a new one instead?'.format(err))
                choice = input('(input Y for yes, others for No): ').upper()
                if choice in ('Y', 'YES'):
                    create_new_config = True
                else:
                    print('setup wizard will now exit, please edit the target config file to make it right')
                    return

        def edit_device(conf_obj: Config):

            def edit_specific_device(dev_conf_obj: DeviceConfig):
                _cin = input('  root topic (input nothing for default: {}): '.format(dev_conf_obj.root_topic))
                if _cin:
                    dev_conf_obj.root_topic = _cin
                _cin = input('  Dynkey16 PSK (input nothing for default: {}): '.format(dev_conf_obj.dynkey16_psk))
                if _cin:
                    dev_conf_obj.dynkey16_psk = _cin
                dev_conf_obj.saveConfig()
            print('editing device configurations')
            action_choice = None
            if len(conf_obj) > 0:
                print(' there are {} devices in config:')
                print('  [index] | [Device]')
                for ele in conf_obj:
                    assert isinstance(ele, DeviceConfig)
                    print('     {}       {}'.format(ele.device_index, ele))
            else:
                print(' there are no device config saved yet')
            print('  (A) Add   (E) Edit   (R) Remove  (Q) Quit')
            while action_choice is None:
                cin = input(' input letters above to chose your action: ')
                cin = cin.upper()
                if cin in ('A', 'ADD'):
                    action_choice = 0
                elif cin in ('E', 'EDIT'):
                    action_choice = 1
                elif cin in ('R', 'REMOVE'):
                    action_choice = 2
                elif cin in ('Q', 'QUIT'):
                    action_choice = 3
            if action_choice == 0:
                print(' -> Adding new device')
                dev_obj = conf_obj.addDevice()
                cin = input('  root topic (input nothing for default: {}): '.format(dev_obj.root_topic))
                if cin:
                    dev_obj.root_topic = cin
                cin = input('  Dynkey16 PSK (input nothing for default: {}): '.format(dev_obj.dynkey16_psk))
                if cin:
                    dev_obj.dynkey16_psk = cin
                dev_obj.saveConfig()
            elif action_choice == 1:
                if len(conf_obj) == 0:
                    print(' error: there is no device to edit')
                    return
                print(' -> Editing existed device')
                dev_obj = None
                while dev_obj is None:
                    cin = input('  input index of target device: ')
                    if cin:
                        try:
                            dev_obj = conf_obj.getDevice(int(cin))
                        except Exception:
                            continue
                    if dev_obj is None:
                        print('   error: please input correct index of device')
                dev_obj = conf_obj.addDevice()
                edit_specific_device(dev_obj)
            elif action_choice == 2:
                if len(conf_obj) == 0:
                    print(' error: there is no device to remove')
                    return
                print(' -> Removing existed device')
                res = False
                while not res:
                    cin = input('  input index of target device: ')
                    if cin:
                        try:
                            res = conf_obj.removeDevice(int(cin))
                        except Exception:
                            continue
                    if not res:
                        print('   error: please input correct index of device')
            else:
                return False
            return True

        def edit_globals(conf_obj: Config):
            print('editing global configurations')
            print(' -> editing MQTT settings')
            cin = input('  server host (input nothing for default: {}): '.format(conf_obj.mqtt_host))
            if cin:
                conf_obj.mqtt_host = cin
            fail = True
            while fail:
                try:
                    cin = input('  server port (input nothing for default: {}): '.format(conf_obj.mqtt_port))
                    if cin:
                        conf_obj.mqtt_port = int(cin)
                    fail = False
                except Exception as err:
                    print('   error: please input the correct type of value')
                    fail = True
            cin = input('  username (input nothing for default: {}): '.format(conf_obj.mqtt_user))
            if cin:
                conf_obj.mqtt_user = cin
            cin = input('  password (input nothing for default: {}): '.format(conf_obj.mqtt_password))
            if cin:
                conf_obj.mqtt_password = cin
            cin = input('  client ID (input nothing for default: {}): '.format(conf_obj.mqtt_client_id))
            if cin:
                conf_obj.mqtt_client_id = cin
            print(' -> editing I2TCP settings')
            fail = True
            while fail:
                try:
                    cin = input('  listen port (input nothing for default: {}): '.format(conf_obj.i2tcp_port))
                    if cin:
                        conf_obj.i2tcp_port = int(cin)
                    fail = False
                except Exception as err:
                    print('   error: please input the correct type of value')
                    fail = True
            cin = input('  PSK (input nothing for default: {}): '.format(conf_obj.i2tcp_psk))
            if cin:
                conf_obj.i2tcp_psk = cin
            print(' -> editing logging settings')
            cin = input('  log filename (input nothing for default: {}): '.format(conf_obj.log_file))
            if cin:
                conf_obj.log_file = cin
            fail = True
            while fail:
                try:
                    cin = input('  log level (input nothing for default: {}): '.format(conf_obj.log_level))
                    cin = cin.upper()
                    assert cin in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', '')
                    if cin:
                        conf_obj.log_level = cin
                    fail = False
                except Exception as err:
                    print('   error: please input correct value chose in DEBUG, INFO, WARNING, ERROR, CRITICAL')
                    fail = True

        def add_systemd(config_path: DirTree):
            if os.name != 'posix':
                print('error: sorry, we are currently not supported for auto startup on other OS than Linux')
                return
        if create_new_config:
            if config.exists():
                config.remove()
            config.fixPath()
            conf = Config(config)
            conf.saveConfig(new=True)
            edit_globals(conf)
            conf.saveConfig()
        else:
            conf = Config(config)
            print('config file already exists, do you wish to edit global config?')
            choice = input('(input Y for yes, others for No): ').upper()
            if choice in ('Y', 'YES'):
                edit_globals(conf)
                conf.saveConfig()
        edit = True
        while edit:
            edit = edit_device(conf)
        print('server is now ready, do you wish to make server auto start when system boot?')
        choice = input('(input Y for yes, others for No): ').upper()
        if choice in ('Y', 'YES'):
            add_systemd(config)
        return
    else:
        ll_srv = LLServer(Config(config))
        ll_srv.start()
        try:
            input('')
        except KeyboardInterrupt:
            pass
        ll_srv.kill()
if __name__ == '__main__':
    ll = LLServer(Config('sample/config.json'))
    ll.start()
    dev = ll[0]
    assert isinstance(dev, LLMqttClient)
    while not dev.is_online:
        time.sleep(1)
    dev.unlock()
    try:
        input('')
    except KeyboardInterrupt:
        pass
    ll.kill()