import threading
from datetime import datetime
from functools import lru_cache
from typing import Any
import zmq
from .common import HEARTBEAT_TOPIC, HEARTBEAT_TOLERANCE

class RemoteException(Exception):
    """
    RPC remote exception
    """

    def __init__(self, value: Any) -> None:
        """
        Constructor
        """
        self._value = value

    def __str__(self) -> str:
        """
        Output error message
        """
        return self._value

class RpcClient:
    """"""

    def __init__(self) -> None:
        """Constructor"""
        self._context: zmq.Context = zmq.Context()
        self._socket_req: zmq.Socket = self._context.socket(zmq.REQ)
        self._socket_sub: zmq.Socket = self._context.socket(zmq.SUB)
        for socket in [self._socket_req, self._socket_sub]:
            socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
            socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 60)
        self._active: bool = False
        self._thread: threading.Thread = None
        self._lock: threading.Lock = threading.Lock()
        self._last_received_ping: datetime = datetime.utcnow()

    @lru_cache(100)
    def __getattr__(self, name: str) -> Any:
        """
        Realize remote call function
        """

        def dorpc(*args, **kwargs):
            if 'timeout' in kwargs:
                timeout = kwargs.pop('timeout')
            else:
                timeout = 30000
            req: list = [name, args, kwargs]
            with self._lock:
                self._socket_req.send_pyobj(req)
                n: int = self._socket_req.poll(timeout)
                if not n:
                    msg: str = f'Timeout of {timeout}ms reached for {req}'
                    raise RemoteException(msg)
                rep = self._socket_req.recv_pyobj()
            if rep[0]:
                return rep[1]
            else:
                raise RemoteException(rep[1])
        return dorpc

    def start(self, req_address: str, sub_address: str) -> None:
        """
        Start RpcClient
        """
        if self._active:
            return
        self._socket_req.connect(req_address)
        self._socket_sub.connect(sub_address)
        self._active = True
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        self._last_received_ping = datetime.utcnow()

    def stop(self) -> None:
        """
        Stop RpcClient
        """
        if not self._active:
            return
        self._active = False

    def join(self) -> None:
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = None

    def run(self) -> None:
        """
        Run RpcClient function
        """
        pull_tolerance: int = HEARTBEAT_TOLERANCE * 1000
        while self._active:
            if not self._socket_sub.poll(pull_tolerance):
                self.on_disconnected()
                continue
            (topic, data) = self._socket_sub.recv_pyobj(flags=zmq.NOBLOCK)
            if topic == HEARTBEAT_TOPIC:
                self._last_received_ping = data
            else:
                self.callback(topic, data)
        self._socket_req.close()
        self._socket_sub.close()

    def callback(self, topic: str, data: Any) -> None:
        """
        Callable function
        """
        raise NotImplementedError

    def subscribe_topic(self, topic: str) -> None:
        """
        Subscribe data
        """
        self._socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    def on_disconnected(self):
        """
        Callback when heartbeat is lost.
        """
        msg: str = f'RpcServer has no response over {HEARTBEAT_TOLERANCE} seconds, please check you connection.'
        print(msg)