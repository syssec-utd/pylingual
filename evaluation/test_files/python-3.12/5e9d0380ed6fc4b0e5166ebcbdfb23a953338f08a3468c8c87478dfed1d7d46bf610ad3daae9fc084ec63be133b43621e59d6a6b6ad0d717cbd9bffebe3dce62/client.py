import signal
import pytdbot
import asyncio
from platform import python_implementation, python_version
from os.path import join as join_path
from pathlib import Path
from getpass import getpass
from importlib import import_module
from typing import Callable, Union
from logging import getLogger, DEBUG
from base64 import b64encode
from deepdiff import DeepDiff
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread, main_thread
from ujson import dumps
from .tdjson import TDjson
from .handlers import Decorators, Handler
from .methods import Methods
from .types import Plugins, Result, LogStream, Update
from .filters import Filter
from .exception import StopHandlers, AuthorizationError
logger = getLogger(__name__)

class Client(Decorators, Methods):
    """Pytdbot, a TDLib client.

    Args:
        api_id (``int``):
            Identifier for Telegram API access, which can be obtained at https://my.telegram.org.

        api_hash (``str``):
            Identifier hash for Telegram API access, which can be obtained at https://my.telegram.org.

        database_encryption_key (``str`` | ``bytes``):
            Encryption key for database encryption.

        files_directory (``str``):
            Directory for storing files and database.

        token (``str``, *optional*):
            Bot token or phone number.

        lib_path (``str``, *optional*):
            Path to TDLib library. Defaults to ``None`` (auto-detect).

        plugins (:class:`~pytdbot.types.Plugins`, *optional*):
            Plugins to load.

        update_class (:class:`~pytdbot.types.Update`, *optional*):
            Update class to use. Defaults to :class:`~pytdbot.types.Update`.

        system_language_code (``str``, *optional*):
            System language code. Defaults to ``en``.

        device_model (``str``, *optional*):
            Device model. Defaults to ``None`` (auto-detect).

        use_test_dc (``bool``, *optional*):
            If set to true, the Telegram test environment will be used instead of the production environment. Defaults to ``False``.

        use_file_database (``bool``, *optional*):
            If set to true, information about downloaded and uploaded files will be saved between application restarts. Defaults to ``True``.

        use_chat_info_database (``bool``, *optional*):
            If set to true, the library will maintain a cache of users, basic groups, supergroups, channels and secret chats. Implies ``use_file_database``. Defaults to ``True``.

        use_message_database (``bool``, *optional*):
            If set to true, the library will maintain a cache of chats and messages. Implies use_chat_info_database. Defaults to ``True``.

        enable_storage_optimizer (``bool``, *optional*):
            If set to true, old files will automatically be deleted. Defaults to ``True``.

        ignore_file_names (``bool``, *optional*):
            If set to true, original file names will be ignored. Otherwise, downloaded files will be saved under names as close as possible to the original name. Defaults to ``False``.

        loop (:py:class:`asyncio.AbstractEventLoop`, *optional*):
            Event loop. Defaults to ``None`` (auto-detect).

        options (``dict``, *optional*):
            Pass key-value dictionary to set TDLib options. Check the list of available options at https://core.telegram.org/tdlib/options.

        sleep_threshold (``int``, *optional*):
            Sleep threshold for all ``FLOOD_WAIT_X`` a.k.a ``Too Many Requests: retry after`` errors occur to this client.
            If any request is rate limited (flood waited) the client will repeat the request after sleeping the required amount of seconds returned by the error. If the ``retry after`` value is higher than ``sleep_threshold`` the error is returned. Defaults to ``None`` (Disabled).

        workers (``int``, *optional*):
            Number of workers for handling updates. Defaults to ``5``.

        td_verbosity (``int``, *optional*):
            Verbosity level of TDLib. Defaults to ``2``.

        td_log (:class:`~pytdbot.types.LogStream`, *optional*):
            Log stream. Defaults to ``None`` (Log to ``stdout``).
    """

    def __init__(self, api_id: int, api_hash: str, database_encryption_key: Union[str, bytes], files_directory: str, token: str=None, lib_path: str=None, plugins: Plugins=None, update_class: Update=Update, system_language_code: str='en', device_model: str=None, use_test_dc: bool=False, use_file_database: bool=True, use_chat_info_database: bool=True, use_message_database: bool=True, enable_storage_optimizer: bool=True, ignore_file_names: bool=False, loop: asyncio.AbstractEventLoop=None, options: dict=None, sleep_threshold: int=None, workers: int=5, td_verbosity: int=2, td_log: LogStream=None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.database_encryption_key = database_encryption_key
        self.files_directory = files_directory
        self.lib_path = lib_path
        self.plugins = plugins
        self.update_class = update_class
        self.system_language_code = system_language_code
        self.device_model = device_model
        self.use_test_dc = use_test_dc
        self.use_file_database = use_file_database
        self.use_chat_info_database = use_chat_info_database
        self.use_message_database = use_message_database
        self.enable_storage_optimizer = enable_storage_optimizer
        self.ignore_file_names = ignore_file_names
        self.td_options = options
        self.sleep_threshold = sleep_threshold if isinstance(sleep_threshold, int) else 0
        self.workers = workers
        self.queue = asyncio.Queue()
        self.td_verbosity = td_verbosity
        self.connection_state: str = None
        self.is_running = None
        self.me = None
        self.is_authenticated = False
        self.options = {}
        self._check_init_args()
        self._handlers = {'initializer': [], 'finalizer': []}
        self._results = {}
        self._tdjson = TDjson(lib_path, td_verbosity)
        self._executor = ThreadPoolExecutor(5, 'Pytdbot')
        self._workers_tasks = None
        self._retry_after_prefex = 'Too Many Requests: retry after '
        self.__authorization_state = None
        self.__authorization = None
        self.__login = False
        self.__is_closing = False
        self.loop = loop if isinstance(loop, asyncio.AbstractEventLoop) else asyncio.get_event_loop()
        if plugins is not None:
            self._load_plugins()
        if isinstance(td_log, LogStream):
            self._tdjson.execute({'@type': 'setLogStream', 'log_stream': td_log.to_dict()})

    async def __aenter__(self):
        await self.start()
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.stop()
        except Exception:
            pass

    @property
    def authorization_state(self) -> str:
        """Current authorization state"""
        return self.__authorization_state

    async def start(self, login: bool=True) -> None:
        """Start pytdbot client.

        Args:
            login (``bool``, *optional*):
                Login after start. Defaults to ``True``.
        """
        if not self.is_running:
            logger.info('Starting pytdbot client...')
            self._workers_tasks = [self.loop.create_task(self._update_worker(x + 1)) for x in range(self.workers)]
            logger.info('Started with %s workers', self.workers)
            self.loop.create_task(self.__listen_loop())
        if login:
            await self.login()

    async def login(self) -> None:
        """Login to Telegram."""
        if self.is_authenticated:
            return
        self.__login = True
        await self.getOption('version')
        while self.authorization_state != 'authorizationStateReady':
            await asyncio.sleep(0.1)
            if self.authorization_state == 'authorizationStateClosed':
                return
        if not self.is_running:
            return
        self.me = await self.getMe()
        if self.me.is_error:
            logger.error('Get me error: {}'.format(self.me['message']))
        self.me = self.me.result
        self.is_authenticated = True
        logger.info('Logged in as {} {}'.format(self.me['first_name'], self.me['id'].__str__() if 'usernames' not in self.me else '@' + self.me['usernames']['editable_username']))

    def add_handler(self, update_type: str, func: Callable, filters: pytdbot.filters.Filter=None, position: int=None) -> None:
        """Add an update handler.

        Args:
            update_type (``str``):
                An update type.

            func (``Callable``):
                A callable function.

            filters (:class:`~pytdbot.filters.Filter`, *optional*):
                message filter.

            position (``int``, *optional*):
                The function position in handlers list. Defaults to ``None`` (append).

        Raises:
            TypeError
        """
        if not isinstance(update_type, str):
            raise TypeError('update_type must be str')
        elif not isinstance(func, Callable):
            raise TypeError('func must be callable')
        elif filters is not None and (not isinstance(filters, Filter)):
            raise TypeError('filters must be instance of pytdbot.filters.Filter')
        else:
            func = Handler(func, update_type, filters, position)
            if update_type not in self._handlers:
                self._handlers[update_type] = []
            if isinstance(position, int):
                self._handlers[update_type].insert(position, func)
            else:
                self._handlers[update_type].append(func)
        self._handlers[update_type].sort(key=lambda x: (x.position is None, x.position))

    def remove_handler(self, func: Callable) -> bool:
        """Remove an update handler.

        Args:
            func (``Callable``):
                A callable function.

        Raises:
            TypeError

        Returns:
            :py:class:`bool`: True if handler was removed, False otherwise.
        """
        if not isinstance(func, Callable):
            raise TypeError('func must be callable')
        for update_type in self._handlers:
            for handler in self._handlers[update_type]:
                if handler.func == func:
                    self._handlers[update_type].remove(handler)
                    self._handlers[update_type].sort(key=lambda x: (x.position is None, x.position))
                    return True
        return False

    async def invoke(self, request: dict, request_id: Union[str, int, dict]=None) -> Result:
        """Invoke a new TDLib request.

        Example:
            .. code-block:: python

                from pytdbot import Client

                async with Client(...) as client:
                    res = await client.invoke({"@type": "getOption", "name": "version"})
                    if not res.is_error:
                        print(res)

        Args:
            request (``dict``):
                The request to be sent.

            request_id (``str`` | ``int`` | ``dict``, *optional*):
                Request id. Defaults to ``None`` (random).

        Returns:
            :class:`~pytdbot.types.Result`
        """
        result = Result(request, request_id)
        self._results[result.id] = result
        if logger.root.level >= DEBUG:
            logger.debug('Sending: {}'.format(dumps(result.request, indent=4)))
        self.__send(result.request)
        await result
        if result.is_error:
            if result['code'] == 429:
                retry_after = self.get_retry_after_time(result['message'])
                if retry_after <= self.sleep_threshold:
                    result.reset()
                    logger.error('Sleeping for {}s (Caused by {})'.format(retry_after, result.request['@type']))
                    await asyncio.sleep(retry_after)
                    self._results[result.id] = result
                    self.__send(result.request)
                    await result
            elif not self.use_message_database and (result['code'] == 400 and result['message'] == 'Chat not found' and ('chat_id' in result.request)):
                chat_id = result.request['chat_id']
                logger.debug('Attempt to load chat {}'.format(chat_id))
                load_chat = await self.getChat(chat_id)
                if not load_chat.is_error:
                    logger.debug('Chat {} is loaded'.format(chat_id))
                    message_id = 0
                    if 'reply_to_message_id' in result.request:
                        message_id = result.request['reply_to_message_id']
                    elif 'message_id' in result.request:
                        message_id = result.request['message_id']
                    if message_id > 0:
                        await self.getMessage(chat_id, message_id)
                    result.reset()
                    self._results[result.id] = result
                    self.__send(result.request)
                    await result
                else:
                    logger.error("Couldn't load chat {}".format(chat_id))
        return result

    async def call_method(self, method: str, **kwargs) -> Result:
        """Call a method. with keyword arguments (``kwargs``) support

        Example:
            .. code-block:: python

                from pytdbot import Client

                async with Client(...) as client:
                    res = await client.call_method("getOption", name="version"})
                    if not res.is_error:
                        print(res)

        Args:
            method (``str``):
                TDLib method name

        Returns:
            :class:`~pytdbot.types.Result`
        """
        kwargs['@type'] = method
        return await self.invoke(kwargs)

    def run(self, login: bool=True) -> None:
        """Start the client and block until the client is stopped.

        Example:
            .. code-block:: python

                from pytdbot import Client

                client = Client(...)

                @client.on_updateNewMessage()
                async def new_message(c,update):
                    await update.reply_text('Hello!')

                client.run()

        Args:
            login (``bool``, *optional*):
                Login after start. Defaults to ``True``.
        """
        self._register_signal_handlers()
        self.loop.run_until_complete(self.start(login))
        self.loop.run_until_complete(self.idle())

    async def idle(self):
        """Idle and wait until the client is stopped."""
        while self.is_running:
            await asyncio.sleep(1)

    async def stop(self) -> bool:
        """Stop the client.

        Raises:
            `RuntimeError`:
                If the instance is already stopped.

        Returns:
            :py:class:`bool`: ``True`` on success.
        """
        if self.is_running is False and self.authorization_state == 'authorizationStateClosed':
            raise RuntimeError('Instance is not running')
        logger.info('Waiting for TDLib to close...')
        self.__is_closing = True
        await self.close()
        while self.authorization_state != 'authorizationStateClosed':
            await asyncio.sleep(0.1)
        else:
            self.__stop_client()
            logger.info('Instance closed')
            return True

    def __send(self, request: dict) -> None:
        return self._tdjson.send(request)

    async def __receive(self, timeout: float=2.0) -> dict:
        return await self.loop.run_in_executor(self._executor, self._tdjson.receive, timeout)

    def _check_init_args(self):
        if not isinstance(self.api_id, int):
            raise TypeError('api_id must be int')
        elif not isinstance(self.api_hash, str):
            raise TypeError('api_hash must be str')
        elif not isinstance(self.database_encryption_key, str) and (not isinstance(self.database_encryption_key, bytes)):
            raise TypeError('database_encryption_key must be str or bytes')
        elif not isinstance(self.files_directory, str):
            raise TypeError('files_directory must be str')
        elif not isinstance(self.td_verbosity, int):
            raise TypeError('td_verbosity must be int')
        elif not isinstance(self.workers, int):
            raise TypeError('workers must be int')
        elif type(Update) is not type(self.update_class):
            raise TypeError('update_class must be instance of class pytdbot.types.Update')
        if self.workers < 1:
            raise ValueError('workers must be greater than 0')

    def get_retry_after_time(self, error_message: str) -> int:
        """Get the retry after time from flood wait error message

        Args:
            error_message (``str``):
                The returned error message from TDLib.

        Returns:
            py:class:`int`
        """
        assert isinstance(error_message, str), 'error_message must be str'
        try:
            return int(error_message.removeprefix(self._retry_after_prefex))
        except Exception:
            return 0

    def _load_plugins(self):
        count = 0
        handlers = 0
        for path in sorted(Path(self.plugins.folder).rglob('*.py')):
            module_path = '.'.join(path.parent.parts + (path.stem,))
            try:
                module = import_module(module_path)
            except Exception:
                logger.exception('Failed to load plugin {}'.format(module_path))
            else:
                logger.debug('Plugin {} loaded'.format(module_path))
                for name in dir(module):
                    obj = getattr(module, name)
                    if hasattr(obj, '_handler') and isinstance(obj._handler, Handler):
                        if asyncio.iscoroutinefunction(obj._handler.func):
                            self.add_handler(obj._handler.update_type, obj._handler.func, obj._handler.filter, obj._handler.position)
                            logger.debug('Handler {} added from {}'.format(obj._handler.func, module_path))
                            handlers += 1
                        else:
                            logger.warn('Handler {} is not an async function from module {}'.format(obj._handler.func, module_path))
                count += 1
        logger.info('From {} plugins got {} handlers'.format(count, handlers))

    async def __listen_loop(self):
        try:
            self.is_running = True
            logger.info('Listening to updates...')
            while self.is_running:
                update = await self.__receive(100000.0)
                if update is None:
                    continue
                self._process_update(update)
        except Exception:
            logger.exception('Exception in __listen_loop')
        finally:
            self.is_running = False

    def _process_update(self, update):
        if '@client_id' in update:
            del update['@client_id']
        if '@type' not in update:
            logger.error('Unexpected update received: {}'.format(update))
            return
        elif '@extra' in update:
            if logger.root.level >= DEBUG:
                logger.debug('Recieved: {}'.format(dumps(update, indent=4)))
            if update['@extra']['request_id'] in self._results:
                result: Result = self._results.pop(update['@extra']['request_id'])
                result.set_result(update)
            elif update['@type'] == 'error' and 'option' in update['@extra']:
                logger.error('{}: {}'.format(update['@extra']['option'], update['message']))
        else:
            if update['@type'] == 'updateAuthorizationState':
                self.loop.create_task(self.__handle_authorization_state(update))
            elif update['@type'] == 'updateMessageSendSucceeded':
                self.loop.create_task(self.__handle_update_message_succeeded(update))
            elif update['@type'] == 'updateMessageSendFailed':
                self.loop.create_task(self.__handle_update_message_failed(update))
            elif update['@type'] == 'updateConnectionState':
                self.loop.create_task(self.__handle_connection_state(update))
            elif update['@type'] == 'updateOption':
                self.loop.create_task(self.__handle_update_option(update))
            elif update['@type'] == 'updateUser':
                self.loop.create_task(self.__handle_update_user(update))
            self.queue.put_nowait(update)

    async def __run_initializers(self, update):
        for initializer in self._handlers['initializer']:
            try:
                if isinstance(initializer.filter, Filter):
                    if asyncio.iscoroutinefunction(initializer.filter.func):
                        if not await initializer.filter.func(self, update):
                            continue
                    elif not initializer.filter.func(self, update):
                        continue
                await initializer.func(self, update)
            except StopHandlers as e:
                raise e
            except Exception:
                logger.exception('Initializer {} failed'.format(initializer))

    async def __run_handlers(self, update):
        update_type = update['@type']
        for handler in self._handlers[update_type]:
            try:
                if isinstance(handler.filter, Filter):
                    if asyncio.iscoroutinefunction(handler.filter.func):
                        if not await handler.filter.func(self, update):
                            continue
                    elif not handler.filter.func(self, update):
                        continue
                await handler.func(self, update)
            except StopHandlers as e:
                raise e
            except Exception:
                logger.exception('Exception in {}'.format(handler))

    async def __run_finalizers(self, update):
        for finalizer in self._handlers['finalizer']:
            try:
                if isinstance(finalizer.filter, Filter):
                    if asyncio.iscoroutinefunction(finalizer.filter.func):
                        if not await finalizer.filter.func(self, update):
                            continue
                    elif not finalizer.filter.func(self, update):
                        continue
                await finalizer.func(self, update)
            except Exception:
                logger.exception('Finalizer {} failed'.format(finalizer))

    async def _update_worker(self, worker_id: int):
        if not self.is_running:
            self.is_running = True
        while self.is_running:
            try:
                update = await self.queue.get()
                if '@type' not in update:
                    continue
                if logger.root.level >= DEBUG:
                    logger.debug('w{}: Received: {}'.format(worker_id, dumps(update, indent=4)))
                update_type = update['@type']
                if update_type in self._handlers:
                    update = self.update_class(self, update)
                    if update_type == 'updateNewMessage' and update['message']['is_outgoing'] and ('sending_state' in update['message']):
                        continue
                    try:
                        await self.__run_initializers(update)
                    except StopHandlers:
                        continue
                    else:
                        try:
                            await self.__run_handlers(update)
                        except StopHandlers:
                            pass
                    finally:
                        try:
                            await self.__run_finalizers(update)
                        except StopHandlers:
                            continue
            except Exception:
                logger.exception('Exception in _update_worker')

    async def set_td_paramaters(self):
        """Make a call to :meth:`~pytdbot.Client.setTdlibParameters` with the current client init parameters

        Raises:
            `AuthorizationError`
        """
        if isinstance(self.database_encryption_key, str):
            self.database_encryption_key = self.database_encryption_key.encode('utf-8')
        res = await self.setTdlibParameters(use_test_dc=self.use_test_dc, api_id=self.api_id, api_hash=self.api_hash, system_language_code=self.system_language_code, device_model=f'{python_implementation()} {python_version()}', use_file_database=self.use_file_database, use_chat_info_database=self.use_chat_info_database, use_message_database=self.use_message_database, use_secret_chats=False, system_version=None, enable_storage_optimizer=self.enable_storage_optimizer, ignore_file_names=self.ignore_file_names, files_directory=self.files_directory, database_encryption_key=b64encode(self.database_encryption_key).decode('utf-8'), database_directory=join_path(self.files_directory, 'database'), application_version=f'Pytdbot {pytdbot.__version__}')
        if res.is_error:
            raise AuthorizationError(res.result['message'])

    async def _set_bot_token(self):
        res = await self.checkAuthenticationBotToken(self.token)
        if res.is_error:
            raise AuthorizationError(res.result['message'])

    async def _set_options(self):
        if not isinstance(self.td_options, dict):
            return
        for k, v in self.td_options.items():
            v_type = type(v)
            if v_type is str:
                data = {'@type': 'optionValueString', 'value': v}
            elif v_type is int:
                data = {'@type': 'optionValueInteger', 'value': v}
            elif v_type is bool:
                data = {'@type': 'optionValueBoolean', 'value': v}
            else:
                raise ValueError(f'Option {k} has unsupported type {v_type}')
            self.__send({'@type': 'setOption', 'name': k, 'value': data, '@extra': {'option': k, 'value': v, 'request_id': ''}})
            logger.debug('Option {} sent with value {}'.format(k, str(v)))

    async def __handle_authorization_state(self, update):
        if update['@type'] == 'updateAuthorizationState':
            old_authorization_state = self.authorization_state
            self.__authorization_state = update['authorization_state']['@type']
            self.__authorization = update['authorization_state']
            logger.info('Authorization state changed to {}'.format(self.authorization_state.removeprefix('authorizationState')))
            if self.__login:
                if self.authorization_state == 'authorizationStateWaitTdlibParameters':
                    await self._set_options()
                    await self.set_td_paramaters()
                elif self.authorization_state == 'authorizationStateWaitPhoneNumber':
                    self._print_welcome()
                    await self.__handle_authorization_state_wait_phone_number()
                elif self.authorization_state == 'authorizationStateWaitEmailAddress':
                    await self.__handle_authorization_state_wait_email_address()
                elif self.authorization_state == 'authorizationStateWaitEmailCode':
                    await self.__handle_authorization_state_wait_email_code()
                elif self.authorization_state == 'authorizationStateWaitCode':
                    await self.__handle_authorization_state_wait_code()
                elif self.authorization_state == 'authorizationStateWaitRegistration':
                    await self.__handle_authorization_state_wait_registration()
                elif old_authorization_state != 'authorizationStateWaitPassword' and self.authorization_state == 'authorizationStateWaitPassword':
                    await self.__handle_authorization_state_wait_password()
                elif self.authorization_state == 'authorizationStateClosed' and self.__is_closing is False:
                    self.__stop_client()

    async def __handle_connection_state(self, update):
        if update['@type'] == 'updateConnectionState':
            self.connection_state: str = update['state']['@type']
            logger.info('Connection state changed to {}'.format(self.connection_state.removeprefix('connectionState')))

    async def __handle_update_message_succeeded(self, update):
        m_id = update['old_message_id'].__str__() + update['message']['chat_id'].__str__()
        if m_id in self._results:
            result: Result = self._results.pop(m_id)
            result.set_result(update['message'])

    async def __handle_update_message_failed(self, update):
        m_id = update['old_message_id'].__str__() + update['message']['chat_id'].__str__()
        if m_id in self._results:
            if update['error_code'] == 429:
                retry_after = update['message']['sending_state']['retry_after']
                if retry_after <= self.sleep_threshold:
                    result: Result = self._results.pop(m_id)
                    logger.error('Sleeping for {}s (Caused by {})'.format(int(retry_after), result.request['@type']))
                    await asyncio.sleep(retry_after)
                    res = await self.invoke(result.request)
                    self._results[res.result['id'].__str__() + update['message']['chat_id'].__str__()] = result
            else:
                result: Result = self._results.pop(m_id)
                result.set_result({'@type': 'error', 'code': update['error_code'], 'message': update['error_message']})

    async def __handle_update_option(self, update):
        if update['value']['@type'] == 'optionValueBoolean':
            self.options[update['name']] = bool(update['value']['value'])
        elif update['value']['@type'] == 'optionValueEmpty':
            self.options[update['name']] = None
        elif update['value']['@type'] == 'optionValueInteger':
            self.options[update['name']] = int(update['value']['value'])
        else:
            self.options[update['name']] = update['value']['value']
        if self.is_authenticated:
            logger.info('Option {} changed to {}'.format(update['name'], self.options[update['name']]))

    async def __handle_update_user(self, update):
        if self.is_authenticated and update['user']['id'] == self.me['id']:
            logger.info('Updating {} ({}) info'.format(self.me['first_name'], self.me['id'].__str__() if 'usernames' not in self.me else '@' + self.me['usernames']['editable_username']))
            try:
                deepdiff(self.me, update['user'])
            except Exception:
                logger.exception('deepdiff failed')
            self.me = update['user']

    async def __handle_authorization_state_wait_phone_number(self):
        if self.authorization_state != 'authorizationStateWaitPhoneNumber':
            return
        if not isinstance(self.token, str):
            while self.is_running:
                user_input = await self.__ainput('Enter a phone number or bot token: ')
                if user_input:
                    y_n = await self.__ainput('Is "{}" correct? (y/n): '.format(user_input))
                    if y_n == '' or y_n.lower() in ['y', 'yes']:
                        if ':' in user_input:
                            res = await self.checkAuthenticationBotToken(user_input)
                        else:
                            res = await self.setAuthenticationPhoneNumber(user_input)
                        if res.is_error:
                            print(res['message'])
                        else:
                            break
        else:
            if ':' in self.token:
                res = await self.checkAuthenticationBotToken(self.token)
            else:
                res = await self.setAuthenticationPhoneNumber(self.token)
            if res.is_error:
                raise AuthorizationError(res['message'])

    async def __handle_authorization_state_wait_email_address(self):
        if self.authorization_state == 'authorizationStateWaitEmailAddress':
            return
        while self.is_running:
            email_address = await self.__ainput('Enter your email address: ')
            res = await self.setAuthenticationEmailAddress(email_address)
            if res.is_error:
                print(res['message'])
            else:
                break

    async def __handle_authorization_state_wait_email_code(self):
        if self.authorization_state != 'authorizationStateWaitEmailCode':
            return
        while self.is_running:
            code = await self.__ainput('Enter the email authentication code you received: ')
            res = await self.checkAuthenticationEmailCode(code={'@type': 'emailAddressAuthenticationCode', 'code': code})
            if res.is_error:
                print(res['message'])
            else:
                break

    async def __handle_authorization_state_wait_code(self):
        if self.authorization_state != 'authorizationStateWaitCode':
            return
        code_type = self.__authorization['code_info']['type']['@type']
        if code_type == 'authenticationCodeTypeTelegramMessage':
            code_type = 'Telegram app'
        elif code_type == 'authenticationCodeTypeSms':
            code_type = 'SMS'
        elif code_type == 'authenticationCodeTypeCall':
            code_type = 'phone call'
        elif code_type == 'authenticationCodeTypeFlashCall':
            code_type = 'phone flush call'
        elif code_type == 'authenticationCodeTypeMissedCall':
            code_type = 'phone missed call'
        elif code_type == 'authenticationCodeTypeFragment':
            code_type = 'fragment.com SMS'
        while self.is_running:
            code = await self.__ainput('Enter the login code received via {}: '.format(code_type))
            res = await self.checkAuthenticationCode(code=code)
            if res.is_error:
                print(res['message'])
            else:
                break

    async def __handle_authorization_state_wait_registration(self):
        if self.authorization_state != 'authorizationStateWaitRegistration':
            return
        while self.is_running:
            first_name = await self.__ainput('Enter your first name: ')
            last_name = await self.__ainput('Enter your last name: ')
            res = await self.registerUser(first_name=first_name, last_name=last_name)
            if res.is_error:
                print(res['message'])
            else:
                break

    async def __handle_authorization_state_wait_password(self):
        if self.authorization_state != 'authorizationStateWaitPassword':
            return
        if self.__authorization['password_hint']:
            print('Your 2FA password hint is: {}'.format(self.__authorization['password_hint']))
        while self.is_running:
            password = await self.loop.run_in_executor(self._executor, getpass, 'Enter your 2FA password {}: '.format('(empty to recover)' if self.__authorization['has_recovery_email_address'] else ''))
            if password == '':
                if self.__authorization['has_recovery_email_address']:
                    y_n = await self.__ainput('Are you sure you want to recover your 2FA password? (y/n): ')
                    if y_n.lower() in ['y', 'yes']:
                        res = await self.requestAuthenticationPasswordRecovery()
                        if res.is_error:
                            raise AuthorizationError(res['message'])
                        else:
                            while True:
                                recovery_code = await self.__ainput('Enter your recovery code sent to {}: '.format(self.__authorization['recovery_email_address_pattern']))
                                res = await self.checkAuthenticationPasswordRecoveryCode(recovery_code)
                                if res.is_error:
                                    print(res['message'])
                                else:
                                    recover_res = await self.recoverAuthenticationPassword(recovery_code)
                                    if recover_res.is_error:
                                        raise AuthorizationError(recover_res['message'])
                                    return
                else:
                    print("You can't recover your 2FA password because you don't set any recovery email address")
            else:
                res = await self.checkAuthenticationPassword(password)
                if res.is_error:
                    print(res['message'])
                else:
                    break

    def __stop_client(self) -> None:
        self.is_authenticated = False
        self.is_running = False
        for worker_task in self._workers_tasks:
            worker_task.cancel()
        self._executor.shutdown(wait=False, cancel_futures=True)

    def _register_signal_handlers(self):

        def _handle_signal():
            self.loop.create_task(self.stop())
            for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT, signal.SIGSEGV):
                self.loop.remove_signal_handler(sig)
        if current_thread() is main_thread():
            try:
                for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT, signal.SIGSEGV):
                    self.loop.add_signal_handler(sig, _handle_signal)
            except NotImplementedError:
                pass

    def __ainput(self, prompt: str):
        return self.loop.run_in_executor(self._executor, input, prompt)

    def _print_welcome(self):
        print('Welcome to Pytdbot (v{}). {}'.format(pytdbot.__version__, pytdbot.__copyright__))
        print('Pytdbot is free software and comes with ABSOLUTELY NO WARRANTY. Licensed under the terms of {}.\n\n'.format(pytdbot.__license__))

def deepdiff(d1, d2):
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        return d1 == d2
    deep = DeepDiff(d1, d2, ignore_order=True, view='tree')
    for parent in deep.keys():
        for diff in deep[parent]:
            difflist = diff.path(output_format='list')
            key = '.'.join((v.__str__() for v in difflist))
            if parent in ['dictionary_item_added', 'values_changed']:
                logger.info(f'{key} changed to {diff.t2}')
            elif parent == 'dictionary_item_removed':
                logger.info(f'{key} removed')