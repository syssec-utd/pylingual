from typing import Optional
from typing import Any
from aiohttp import web
from aiohttp import web_runner
system_setup_needed = False

class WebServer(object):

    def __init__(self, loop=None, url=None, args={}):
        from ..lib.util.asyn import get_event_loop
        from .multiuser import MultiuserHandlers
        global system_setup_needed
        self.manager = None
        self.system_queue = None
        self.system_worker_state = None
        self.info_of_running_jobs = None
        self.report_generation_ps = None
        self.args = args
        self.logger = args.get('logger')
        self.app = None
        self.cors = Optional[Any]
        self.runner = None
        self.site = None
        self.servermode = args.get('servermode', False)
        self.mu = MultiuserHandlers(servermode=self.servermode)
        self.wss = {}
        self.system_message_last_ids = {}
        self.system_message_db_conn = None
        self.host = args.get('host')
        self.port = args.get('port')
        if loop is None:
            loop = get_event_loop()
        self.ssl_context = args.get('ssl_context')
        self.loop = loop
        self.server_started = False
        self.system_setup_needed = system_setup_needed
        if args.get('headless') is False and url:
            self.loop.create_task(self.open_url(url))
        task = loop.create_task(self.start())
        task.add_done_callback(self.server_done)

    @web.middleware
    async def middleware(self, request, handler):
        from json import dumps
        import traceback
        from sys import stderr
        from aiohttp.web_exceptions import HTTPNotFound
        from aiohttp.web import Response
        from ..lib.exceptions import SystemMissingException
        global loop
        try:
            url_parts = request.url.parts
            response = await handler(request)
            nocache = False
            if url_parts[0] == '/':
                if len(url_parts) >= 3 and url_parts[2] == 'nocache':
                    nocache = True
            elif url_parts[0] == 'nocache':
                nocache = True
            if nocache:
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except SystemMissingException as e:
            if self.logger:
                self.logger.exception(e)
            self.system_setup_needed = True
            return Response(status=500, reason='SYSTEM_SETUP_NEEDED')
        except Exception as e:
            msg = 'Exception with {}'.format(request.rel_url)
            if self.logger:
                self.logger.info(msg)
                self.logger.exception(e)
            if self.args.get('debug'):
                if not isinstance(e, HTTPNotFound):
                    stderr.write(msg + '\n')
                    traceback.print_exc()
            return web.HTTPInternalServerError(text=dumps({'status': 'error', 'msg': traceback.format_exc()}))

    def server_done(self, task):
        from traceback import print_exc
        try:
            task.result()
        except Exception as e:
            if self.logger:
                self.logger.exception(e)
            if self.args.get('debug'):
                print_exc()
            self.server_started = None
            exit(1)

    async def open_url(self, url):
        from webbrowser import open as webbrowseropen
        from asyncio import sleep
        while self.server_started is False:
            await sleep(0.2)
        if self.server_started:
            webbrowseropen(url)

    def start_workers(self):
        self.start_job_worker()
        self.start_system_worker()

    def start_job_worker(self):
        from multiprocess import Process
        from .job_handlers import fetch_job_queue
        self.job_worker = Process(target=fetch_job_queue, args=(self.job_queue, self.info_of_running_jobs, self.report_generation_ps))
        self.job_worker.start()

    def start_system_worker(self):
        from multiprocess import Process
        from .system_worker import system_queue_worker
        assert self.manager is not None
        self.system_worker = Process(target=system_queue_worker, args=(self.system_queue, self.system_worker_state, self.local_modules_changed, self.manager))
        self.system_worker.start()

    def make_system_queue(self):
        if self.system_queue is not None:
            return self.system_queue
        if not self.manager:
            return None
        self.system_queue = self.manager.list()

    def make_system_worker_state(self):
        if self.system_worker_state is not None:
            return self.system_worker_state
        if not self.manager:
            return None
        self.system_worker_state = self.manager.dict()
        self.initialize_system_worker_state()

    def initialize_system_worker_state(self):
        from .consts import SYSTEM_STATE_INSTALL_KEY
        from .consts import SYSTEM_STATE_INSTALL_QUEUE_KEY
        assert self.system_worker_state is not None
        assert self.manager is not None
        self.system_worker_state[SYSTEM_STATE_INSTALL_KEY] = self.manager.dict()
        self.system_worker_state[SYSTEM_STATE_INSTALL_QUEUE_KEY] = self.manager.list()

    def make_job_queue_states(self):
        from multiprocess import Queue
        assert self.manager is not None
        self.job_queue = Queue()
        self.info_of_running_jobs = self.manager.list()
        self.report_generation_ps = self.manager.list()
        self.report_generation_ps.append('initial')

    def make_shared_states(self):
        from multiprocess import Manager
        self.manager = Manager()
        self.make_system_queue()
        self.make_system_worker_state()
        self.local_modules_changed = self.manager.Event()
        self.make_job_queue_states()
        self.wss = {}

    def make_store_handlers(self):
        from .store_handlers import StoreHandlers
        self.store_handlers = StoreHandlers(servermode=self.servermode, manager=self.manager, mu=self.mu, local_modules_changed=self.local_modules_changed, system_worker_state=self.system_worker_state, system_queue=self.system_queue, logger=self.logger)

    def make_job_handlers(self):
        from .job_handlers import JobHandlers
        self.job_handlers = JobHandlers(servermode=self.servermode, mu=self.mu, logger=self.logger, job_queue=self.job_queue, info_of_running_jobs=self.info_of_running_jobs, report_generation_ps=self.report_generation_ps)

    def make_multiuser_handlers(self):
        from .multiuser import MultiuserHandlers
        self.multiuser_handlers = MultiuserHandlers(servermode=self.servermode)

    def make_system_handlers(self):
        from .system_handlers import SystemHandlers
        self.system_handlers = SystemHandlers(servermode=self.servermode, mu=self.mu, logger=self.logger, system_queue=self.system_queue, system_worker_state=self.system_worker_state)

    def make_websocket_handlers(self):
        from .websocket_handlers import WebSocketHandlers
        self.websocket_handlers = WebSocketHandlers(system_worker_state=self.system_worker_state, wss=self.wss, system_message_last_ids=self.system_message_last_ids, logger=self.logger)

    def make_handlers(self):
        self.make_job_handlers()
        self.make_store_handlers()
        self.make_multiuser_handlers()
        self.make_system_handlers()
        self.make_websocket_handlers()

    async def start(self):
        from aiohttp import web
        import aiohttp_cors
        from .system_message_db import get_system_message_db_conn
        from .system_message_db import clear_system_message_db
        self.app = web.Application(loop=self.loop, middlewares=[self.middleware], client_max_size=1024 * 1024 * 1024 * 1024)
        options = {'*': aiohttp_cors.ResourceOptions()}
        self.cors = aiohttp_cors.setup(self.app, defaults=options)
        self.system_message_db_conn = get_system_message_db_conn()
        clear_system_message_db(self.system_message_db_conn)
        self.make_shared_states()
        self.make_handlers()
        self.setup_routes()
        self.start_workers()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = TCPSitePatched(self.runner, host=self.host, port=self.port, loop=self.loop, ssl_context=self.ssl_context)
        await self.site.start()
        self.server_started = True

    def setup_webapp_routes(self):
        from ..lib.exceptions import ModuleLoadingError
        from importlib.util import spec_from_file_location, module_from_spec
        from os.path import join, exists
        from os import listdir
        from ..lib.exceptions import SetupError
        from ..lib.system import get_modules_dir
        modules_dir = get_modules_dir()
        if modules_dir is None:
            return False
        webapps_dir = join(modules_dir, 'webapps')
        if exists(webapps_dir) is False:
            return False
        module_names = listdir(webapps_dir)
        for module_name in module_names:
            try:
                module_dir = join(webapps_dir, module_name)
                pypath = join(module_dir, 'route.py')
                if exists(pypath):
                    spec = spec_from_file_location('route', pypath)
                    if spec is None:
                        raise ModuleLoadingError(module_name=module_name)
                    module = module_from_spec(spec)
                    if spec.loader is None:
                        raise ModuleLoadingError(module_name=module_name)
                    spec.loader.exec_module(module)
                    if self.app is None:
                        raise SetupError()
                    for route in module.routes:
                        method, path, func_name = route
                        path = f'/webapps/{module_name}/' + path
                        self.app.router.add_route(method, path, func_name)
            except Exception as e:
                if self.logger:
                    self.logger.error(f'error loading webapp {module_name}')
                    self.logger.exception(e)
        return True

    def add_static_routes(self):
        from pathlib import Path
        assert self.app is not None
        source_dir = Path(__file__).absolute().parent
        self.app.router.add_static('/store', source_dir / 'webstore')
        self.app.router.add_static('/result', source_dir / 'webresult')
        self.app.router.add_static('/submit', source_dir / 'websubmit')
        self.app.router.add_static('/', source_dir / 'www')

    def setup_cors(self):
        from aiohttp_cors import ResourceOptions
        assert self.app is not None
        if not self.cors:
            return
        for resource in list(self.app.router.resources()):
            self.cors.add(resource, {'http://0.0.0.0:3000': ResourceOptions(allow_credentials=True, expose_headers='*', allow_headers='*', allow_methods='*')})

    def setup_routes(self):
        from .webresult import webresult
        from ..lib.exceptions import SetupError
        from ..lib.system import get_modules_dir
        from os.path import join
        from os.path import exists
        if self.app is None:
            raise SetupError()
        self.routes = list()
        self.routes.extend(self.store_handlers.routes)
        self.routes.extend(self.job_handlers.routes)
        self.routes.extend(self.multiuser_handlers.routes)
        self.routes.extend(self.system_handlers.routes)
        self.routes.extend(self.websocket_handlers.routes)
        self.routes.extend(webresult.routes)
        self.routes.append(['GET', '/', self.index])
        for route in self.routes:
            method, path, func_name = route
            self.app.router.add_route(method, path, func_name)
        self.add_static_routes()
        self.setup_webapp_routes()
        modules_dir = get_modules_dir()
        if modules_dir:
            if exists(join(modules_dir, 'annotators')):
                self.app.router.add_static('/modules/annotators/', join(modules_dir, 'annotators'))
            if exists(join(modules_dir, 'webapps')):
                self.app.router.add_static('/webapps', join(modules_dir, 'webapps'))
        self.setup_cors()

    def index(self, request):
        from aiohttp.web import FileResponse
        _ = request
        return FileResponse('www/index.html')

class TCPSitePatched(web_runner.BaseSite):
    __slots__ = ('loop', '_host', '_port', '_reuse_address', '_reuse_port')

    def __init__(self, runner, host=None, port=None, shutdown_timeout=60.0, ssl_context=None, backlog=128, reuse_address=None, reuse_port=None, loop=None):
        from ..lib.util.asyn import get_event_loop
        super().__init__(runner, shutdown_timeout=shutdown_timeout, ssl_context=ssl_context, backlog=backlog)
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if host is None:
            host = '0.0.0.0'
        self._host = host
        if port is None:
            port = 8443 if self._ssl_context else 8080
        self._port = port
        self._reuse_address = reuse_address
        self._reuse_port = reuse_port

    @property
    def name(self, args={}):
        from yarl import URL
        scheme = 'https' if args.get('ssl_enabled', False) else 'http'
        return str(URL.build(scheme=scheme, host=self._host, port=self._port))

    async def start(self):
        from ..lib.exceptions import SetupError
        await super().start()
        if self._runner.server is None:
            raise SetupError()
        _ = await self.loop.create_server(self._runner.server, self._host, self._port, ssl=self._ssl_context, backlog=self._backlog, reuse_address=self._reuse_address, reuse_port=self._reuse_port)