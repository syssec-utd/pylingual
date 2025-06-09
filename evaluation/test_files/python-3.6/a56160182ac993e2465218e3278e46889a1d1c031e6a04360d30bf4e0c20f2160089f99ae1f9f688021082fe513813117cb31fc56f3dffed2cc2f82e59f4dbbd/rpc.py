from contextlib import contextmanager
from http.client import HTTPConnection
from multiprocessing import Process, Event as event
from multiprocessing.synchronize import Event
from pathlib import Path
from random import choice
from socket import socket, AF_UNIX, SOCK_STREAM
from socketserver import UnixStreamServer
from string import ascii_letters, digits
from tempfile import mkdtemp
from threading import current_thread
from typing import Optional, Any, Union, Tuple, Dict, Set, ContextManager
from xmlrpc.client import Transport, ServerProxy
from xmlrpc.server import SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

class _UnixStreamXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    disable_nagle_algorithm = False

    def address_string(self) -> Any:
        return self.client_address

class UnixStreamXMLRPCServer(UnixStreamServer, SimpleXMLRPCDispatcher):

    def __init__(self, addr: Path, log_requests: bool=False, allow_none: bool=True, encoding: Optional[str]=None, bind_and_activate: bool=True, use_builtin_types: bool=True):
        self.logRequests = log_requests
        SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding, use_builtin_types)
        UnixStreamServer.__init__(self, str(addr), _UnixStreamXMLRPCRequestHandler, bind_and_activate)

class _UnixStreamHTTPConnection(HTTPConnection):

    def connect(self) -> None:
        self.sock = socket(AF_UNIX, SOCK_STREAM)
        self.sock.connect(self.host)

class _UnixStreamTransport(Transport):

    def __init__(self, socket_path: Path):
        self.socket_path = socket_path
        super().__init__()

    def make_connection(self, host: Union[Tuple[str, Dict[str, str]], str]):
        return _UnixStreamHTTPConnection(str(self.socket_path))

class UnixSocketRPCClient(ServerProxy):

    def __init__(self, addr: Path, **kwargs: Any):
        transport = _UnixStreamTransport(addr)
        super().__init__('http://', transport=transport, **kwargs)

def _random_string(length) -> str:
    return ''.join([choice(ascii_letters + digits) for _ in range(length)])

class ServedFunctionRegistrar:

    def __init__(self) -> None:
        self.served_functions: Dict[str, Set[str]] = {}

    def __call__(self, method):
        class_name = method.__qualname__.split('.')[-2]
        if class_name not in self.served_functions:
            self.served_functions[class_name] = set()
        self.served_functions[class_name].add(method.__name__)

        def decorate(*args, **kwargs):
            return method(*args, **kwargs)
        return decorate

class UnixSocketRPCServer:
    serve = ServedFunctionRegistrar()

    def __init__(self, socket_path: Optional[Path]=None):
        self.socket_path = socket_path or Path(mkdtemp()) / (_random_string(16) + '.sock')
        self.thread_name: Optional[str] = None

    @property
    def served(self) -> Set[str]:
        return UnixSocketRPCServer.serve.served_functions[self.__class__.__name__]

    def serve_forever(self, started_flag: Optional[Event]=None, thread_name: Optional[str]=None):
        if thread_name:
            current_thread().name = thread_name
        started_flag = started_flag or event()
        with UnixStreamXMLRPCServer(self.socket_path) as server:
            server.register_introspection_functions()
            for method_name in self.served:
                server.register_function(getattr(self, method_name), method_name)
            started_flag.set()
            server.serve_forever()

    def server_process(self, daemon: bool=True) -> Process:
        started = event()
        proc = Process(target=self.serve_forever, args=(started, self.thread_name), daemon=daemon)
        proc.start()
        started.wait()
        return proc

    @contextmanager
    def server(self, terminate_timeout: int=1) -> ContextManager[Path]:
        proc = self.server_process()
        try:
            yield self.socket_path
        finally:
            proc.terminate()
            proc.join(timeout=terminate_timeout)
            if proc.exitcode is None:
                proc.kill()
                proc.join()

    @contextmanager
    def proxy(self, terminate_timeout: int=1) -> ContextManager[UnixSocketRPCClient]:
        with self.server(terminate_timeout) as socket_path:
            yield UnixSocketRPCClient(socket_path)