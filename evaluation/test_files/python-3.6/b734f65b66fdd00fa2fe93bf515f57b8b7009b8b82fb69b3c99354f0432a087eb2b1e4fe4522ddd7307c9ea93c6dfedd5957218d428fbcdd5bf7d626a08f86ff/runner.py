import logging.config
import argparse
from aiohttp import web, TCPConnector, ClientSession
import configparser
import os.path
from heaserver.service import appproperty, appfactory
from heaserver.service import wstl
from typing import Callable, Iterable, Optional, Union, AsyncIterator, AsyncGenerator, Type
from yarl import URL
from .db.database import DatabaseManager
from heaobject.root import json_dumps
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_PORT = 8080
DEFAULT_BASE_URL = URL('http://localhost:' + str(DEFAULT_PORT))
DEFAULT_REGISTRY_URL = 'http://localhost:8080'
routes = web.RouteTableDef()

class Configuration:
    """
    Configuration information for the service.
    """

    def __init__(self, base_url: Union[str, URL]=DEFAULT_BASE_URL, port: Union[int, str]=DEFAULT_PORT, config_file: Optional[str]=None, config_str: Optional[str]=None):
        """
        Initializes the configuration object.

        :param base_url: the base URL of the service. Required.
        :param port: the port the service will listen on. Required.
        :param config_file: an optional INI file with configuration data.
        :param config_str: an optional configuration INI file as a string. Parsed after any config_file.
        """
        self.__base_url = URL(base_url) if base_url else DEFAULT_BASE_URL
        self.__port = int(port) if port else DEFAULT_PORT
        self.__parsed_config = configparser.ConfigParser()
        self.__config_file = config_file
        self.__config_str = config_str
        if config_file:
            self.__parsed_config.read(config_file)
        if config_str:
            self.__parsed_config.read_string(config_str)
        self.__parsed_config.read_dict({})

    @property
    def port(self) -> int:
        """
        The port this service will listen on.
        :return: a port number.
        """
        return self.__port

    @property
    def base_url(self) -> URL:
        """
        This service's base URL.
        :return: a URL.
        """
        return self.__base_url

    @property
    def parsed_config(self) -> configparser.ConfigParser:
        """
        Any configuration information parsed from an INI file or INI string.
        :return: a configparser.ConfigParser object.
        """
        result = configparser.ConfigParser()
        result.read_dict(self.__parsed_config)
        return result

    @property
    def config_file(self) -> Optional[str]:
        """
        The path to a config file.
        :return: the config file path string, or None.
        """
        return self.__config_file

    @property
    def config_str(self) -> Optional[str]:
        """
        A string containing an INI file, if provided in the constructor.
        :return: a config file string, or None.
        """
        return self.__config_str

def init(port: Union[int, str]=DEFAULT_PORT, base_url: Union[URL, str]=DEFAULT_BASE_URL, config_file: Optional[str]=None, config_string: Optional[str]=None, logging_level: Optional[str]=None) -> Configuration:
    """
    Sets a default logging level and returns a new Configuration object.

    :param port: the port the service will listen to. If omitted, the DEFAULT_PORT is used.
    :param base_url: the service's base URL. If omitted, the DEFAULT_BASE_URL is used.
    :param config_file:
    :param config_string:
    :param logging_level: configure the logging level. If omitted, logging will not be configured.
    :return:
    """
    if logging_level is not None:
        logging.basicConfig(level=logging_level)
    config = Configuration(base_url=base_url, port=port, config_file=config_file, config_str=config_string)
    return config

def init_cmd_line(description: str='A HEA microservice', default_port: int=DEFAULT_PORT) -> Configuration:
    """
    Parses command line arguments and configures the service accordingly. Must be called before anything else, if you
    want to use command line arguments to configure the service.

    :param description: optional description that will appear when the script is passed the -h or --help option.
    :param default_port: the optional port on which to listen if none is specified by command line argument. If omitted
    and no port is specified by command line argument, port 8080 is used.
    :return: a Configuration object.
    :raises ValueError: if any arguments are invalid.

    The following command line arguments are accepted:
        -b or --baseurl, which optionally sets the base URL of the service. If unspecified, the default is
        http://localhost:<port>, where port is the 8080 or the port number set by the --port argument.
        -p or --port, which optionally sets the port the microservice will listen on. The default is 8080.
        -f or --configuration, which optionally sets an INI file to use for additional configuration.
        -l or --logging, which optionally sets a standard logging configuration INI file. If unspecified, the
            DEFAULT_LOG_LEVEL variable will be used to set the default log level.

    Microservices must not call logging.getLogger until init has been called.

    The INI configuration file is parsed by the built-in configparser module and may contain the following settings:

    ;Base URL for the HEA registry service (default is http://localhost:8080/heaserver-server-registry)
    Registry = url of the HEA registry service

    ;See the documentation for the db object that you passed in for the config file properties that it expects.
    """
    assert default_port is not None
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-b', '--baseurl', metavar='baseurl', type=str, default=str(DEFAULT_BASE_URL), help='The base URL of the service')
    parser.add_argument('-p', '--port', metavar='port', type=int, default=default_port, help='The port on which the server will listen for connections')
    parser.add_argument('-f', '--configuration', metavar='configuration', type=str, help='Path to a HEA configuration file in INI format')
    parser.add_argument('-l', '--logging', metavar='logging', type=str, help='Standard logging configuration file')
    args = parser.parse_args()
    if args.logging and os.path.isfile(args.logging):
        logging.config.fileConfig(args.logging, disable_existing_loggers=False)
    else:
        logging.basicConfig(level=DEFAULT_LOG_LEVEL)
    logger = logging.getLogger(__name__)
    if args.configuration:
        logger.info('Parsing config file %s', args.configuration)
    if args.logging and os.path.isfile(args.logging):
        logger.debug('Parsing logging configuration file %s', args.logging)
    else:
        logger.debug('No logging configuration file found')
    baseurl_ = args.baseurl
    return Configuration(base_url=baseurl_[:-1] if baseurl_.endswith('/') else baseurl_, config_file=args.configuration, port=args.port)

def start(db: Optional[Type[DatabaseManager]]=None, wstl_builder_factory: Optional[Callable]=None, cleanup_ctx: Optional[Iterable[Callable[[web.Application], AsyncIterator[None]]]]=None, config: Optional[Configuration]=None) -> None:
    """
    Starts the microservice. It calls get_application() to get the AioHTTP app
    object, sets up a global HTTP client session object in the appproperty.HEA_CLIENT_SESSION property, and then calls
    AioHTTP's aiohttp.web.run_app() method with it to launch the service. It sets the
    application and request properties described in the documentation for get_application().

    :param db: a database manager type from the heaserver.server.db package, if database connectivity is needed. Sets
    the appproperty.HEA_DB application property to a database object created by this database manager.
    :param wstl_builder_factory: a zero-argument callable that will return a design-time WeSTL document. Optional if
    this service has no actions.
    :param cleanup_ctx: an iterable of asynchronous generators that will be passed into the aiohttp cleanup context.
    The generator should have a single yield statement that separates code to be run upon startup and code to be
    run upon shutdown. The shutdown code will run only if the startup code did not raise any exceptions. The startup
    code will run in sequential order. The shutdown code will run in reverse order.
    :param config: a Configuration instance.

    This function must be called after init.

    A 'registry' property is set in the application context with the registry service's base URL.
    """
    app = get_application(db=db() if db is not None else None, wstl_builder_factory=wstl_builder_factory, cleanup_ctx=cleanup_ctx, config=config)
    app.cleanup_ctx.append(client_session)
    web.run_app(app, port=config.port if config else DEFAULT_PORT)

def get_application(db: Optional[DatabaseManager]=None, wstl_builder_factory: Optional[Callable[[], wstl.RuntimeWeSTLDocumentBuilder]]=None, cleanup_ctx: Optional[Iterable[Callable[[web.Application], AsyncIterator[None]]]]=None, config: Optional[Configuration]=None) -> web.Application:
    """
    Gets the aiohttp application object for this microservice. It is called by start() during normal operations, and
    by test cases when running tests.

    It registers cleanup context generators that set the following application properties:
    HEA_DB: a database object from the heaserver.server.db package.
    HEA_CLIENT_SESSION: a aiohttp.web.ClientSession HTTP client object. This property is only set if the testing
    argument is False. If running test cases, testing should be set to True, and the HEAAioHTTPTestCase class will
    handle creating and destroying HTTP clients instead.
    HEA_REGISTRY: The base URL for the registry service.
    HEA_COMPONENT: This service's base URL.
    HEA_WSTL_BUILDER_FACTORY: the wstl_builder_factory argument.

    :param db: a database object from the heaserver.server.db package, if database connectivity is needed.
    :param wstl_builder_factory: a zero-argument callable that will return a RuntimeWeSTLDocumentBuilder. Optional if
    this service has no actions. Typically, you will use the heaserver.service.wstl.get_builder_factory function to
    get a factory object.
    :param cleanup_ctx: an iterable of asynchronous generators that will be passed into the aiohttp cleanup context.
    The generator should have a single yield statement that separates code to be run upon startup and code to be
    run upon shutdown. The shutdown code will run only if the startup code did not raise any exceptions. Cleanup
    context generators cannot assume that any of the above application properties are available.
    :param config: a Configuration instance.
    :param testing: whether this function was called by a test case in a HEAAioHTTPTestCase object. Default is
    False.
    :return: an aiohttp application object.

    This function must be called after init, and it is called by start.

    A 'registry' property is set in the application context with the registry service's base URL.
    """
    logger = logging.getLogger(__name__)
    logger.info('Starting HEA')
    if not config:
        config = init()
    app = appfactory.new_app()
    if db:

        async def _db(app: web.Application) -> AsyncGenerator:
            if db:
                with db.database(config.parsed_config if config is not None else None) as database:
                    app[appproperty.HEA_DB] = database
                    yield
            else:
                app[appproperty.HEA_DB] = None
        app.cleanup_ctx.append(_db)

    async def _hea_registry(app: web.Application) -> AsyncGenerator:
        app[appproperty.HEA_REGISTRY] = config.parsed_config['DEFAULT'].get('Registry', DEFAULT_REGISTRY_URL) if config else None
        yield
    app.cleanup_ctx.append(_hea_registry)

    async def _hea_component(app: web.Application) -> AsyncGenerator:
        app[appproperty.HEA_COMPONENT] = str(config.base_url) if config else None
        yield
    app.cleanup_ctx.append(_hea_component)
    app.add_routes(routes)

    async def _hea_wstl_builder_factory(app: web.Application) -> AsyncGenerator:
        if wstl_builder_factory is None:
            logger.debug('No design-time WeSTL loader was provided.')
            wstl_builder_factory_ = wstl.builder_factory()
        else:
            wstl_builder_factory_ = wstl_builder_factory
        app[appproperty.HEA_WSTL_BUILDER_FACTORY] = wstl_builder_factory_
        yield
    app.cleanup_ctx.append(_hea_wstl_builder_factory)
    if cleanup_ctx is not None:
        for cb in cleanup_ctx:
            app.cleanup_ctx.append(cb)
    return app

async def client_session(app: web.Application) -> AsyncGenerator[None, None]:
    """
    Manages the global HTTP client session.

    :param app: the AioHTTP Application object.
    :return: an AsyncGenerator.
    """
    _logger = logging.getLogger(__name__)
    _logger.debug('Starting client session')
    app[appproperty.HEA_CLIENT_SESSION] = ClientSession(connector=TCPConnector(), connector_owner=True, json_serialize=json_dumps, raise_for_status=True)
    _logger.debug('Client session started')
    yield
    _logger.debug('Closing client session')
    await app[appproperty.HEA_CLIENT_SESSION].close()