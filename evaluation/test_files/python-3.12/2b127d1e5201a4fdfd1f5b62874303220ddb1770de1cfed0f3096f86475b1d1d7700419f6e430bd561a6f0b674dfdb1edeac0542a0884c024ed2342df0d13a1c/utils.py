import base64
import codecs
import io
import logging
import os
import pickle
import random
import subprocess
import sys
import tempfile
import time
import json
import traceback
import types
import typing as tp
import uuid
import warnings
from functools import lru_cache, wraps
from pathlib import Path
from threading import Thread
from enum import Enum
from django.conf import settings
from django.middleware.gzip import GZipMiddleware
from django.urls import re_path, include
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.cache import caches, InvalidCacheBackendError
from django.core.paginator import Paginator as BasePaginator
from django.template import loader
from django.utils import translation, functional
from django.utils.translation import get_language
from django.utils.module_loading import import_string as import_class
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from . import exceptions as ex
from .tools import multikeysort
logger: logging.Logger = logging.getLogger('vstutils')
ON_POSIX = 'posix' in sys.builtin_module_names

def deprecated(func: tp.Callable):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    def new_func(*args, **kwargs):
        warnings.warn(f'Call to deprecated function {func.__name__}.', category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return new_func

def list_to_choices(items_list: tp.Iterable, response_type: tp.Callable=list) -> tp.Iterable[tp.Tuple[str, str]]:
    """
    Method to create django model choices from flat list of values.

    :param items_list: list of flat values.
    :param response_type: casting type of returned mapping
    :return: list of tuples from `items_list` values
    """
    return response_type(map(lambda x: (x, x), items_list))

def is_member_descriptor(obj):
    try:
        return type(obj).__name__ == 'member_descriptor'
    except:
        return False

@lru_cache()
def current_lang(lang=None):
    from vstutils.api.models import Language
    try:
        return Language.objects.get(code=lang or get_language())
    except Exception:
        return Language.objects.all().first()

def get_render(name: tp.Text, data: tp.Dict, trans: tp.Text='en') -> tp.Text:
    """
    Render string from template.

    :param name: -- full template name
    :type name: str
    :param data: -- dict of rendered vars
    :type data: dict
    :param trans: -- translation for render. Default 'en'.
    :type trans: str
    :return: -- rendered string
    :rtype: str
    """
    cur_language = translation.get_language()
    try:
        if trans != cur_language:
            translation.activate(trans)
        config = loader.get_template(name)
        result = config.render(data, data.pop('request', None)).replace('\r', '')
    finally:
        if trans != cur_language:
            translation.activate(cur_language)
    return result

def encode(key, clear):
    """
    Encode string by Vigenère cipher.

    :param key: -- secret key for encoding
    :type key: str
    :param clear: -- clear value  for encoding
    :type clear: str
    :return: -- encoded string
    :rtype: str
    """
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(clear[i]) + ord(key_c)) % 256))
    return base64.urlsafe_b64encode(''.join(enc).encode()).decode()

def decode(key, enc):
    """
    Decode string from encoded by Vigenère cipher.

    :param key: -- secret key for encoding
    :type key: str
    :param enc: -- encoded string for decoding
    :type enc: str
    :return: -- decoded string
    :rtype: str
    """
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(enc[i]) - ord(key_c)) % 256))
    return ''.join(dec)

def get_if_lazy(obj):
    with raise_context():
        if isinstance(obj, functional.LazyObject):
            obj._setup() if obj._wrapped == functional.empty else None
            return obj._wrapped
    return obj

def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None, **kwargs):
    """
    Wrapper over :func:`django.core.mail.send_mail` which provide additional named arguments.
    """
    connection = connection or get_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection, **kwargs)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    return mail.send()

def send_template_email_handler(subject: tp.Text, email_from: tp.Text, email: tp.Union[tp.List, tp.Text], template_name: tp.Text, context_data: tp.Optional[tp.Dict]=None, **kwargs) -> tp.SupportsInt:
    """
    Function for email sending.
    The function convert recipient to list and set context before sending if it possible.

    :param subject: mail subject.
    :param email_from: sender that be setup in email.
    :param email: list of strings or single string, with email addresses of recipients
    :param template_name: relative path to template in `templates` directory, must include extension in file name.
    :param context_data: dictionary with context for rendering message template.
    :param kwargs: additional named arguments for `send_mail`
    :return: Number of emails sent.
    """
    recipient_list = email if isinstance(email, (list, tuple)) else [email]
    if context_data is None:
        context = {}
    elif not isinstance(context_data, dict):
        context = dict(context_data)
    else:
        context = context_data.copy()
    return send_mail(subject=subject, message='', from_email=email_from, recipient_list=recipient_list, html_message=loader.render_to_string(template_name, context=context, request=context.pop('request', None)), **kwargs)

def send_template_email(sync: bool=False, **kwargs):
    """
    Function executing sync or async email sending; according `sync` argument and settings variable "RPC_ENABLED".
    You can use this function to send message, it sends message asynchronously or synchronously.
    If you don't set settings for celery or don't have celery it sends synchronously mail.
    If celery is installed and configured and `sync` argument of the function is set to `False`,
    it sends asynchronously email.

    :param sync: argument for determining how send email, asynchronously or synchronously
    :param subject: mail subject.
    :param email: list of strings or single string, with email addresses of recipients
    :param template_name: relative path to template in `templates` directory, must include extension in file name.
    :param context_data: dictionary with context for rendering message template.
    """
    if sync or not settings.RPC_ENABLED:
        send_template_email_handler(email_from=settings.EMAIL_FROM_ADDRESS, **kwargs)
    else:
        from .tasks import SendEmailMessage
        SendEmailMessage.do(email_from=settings.EMAIL_FROM_ADDRESS, **kwargs)

def patch_gzip_response(response, request):
    if not response.status_code == 200:
        return
    GZipMiddleware.process_response(None, request, response)

def patch_gzip_response_decorator(func):

    def gzip_response_wrapper(view, request, *args, **kwargs):
        response = func(view, request, *args, **kwargs)
        with raise_context():
            patch_gzip_response(response, request)
        return response
    return gzip_response_wrapper

def translate(text: tp.Text) -> tp.Text:
    """
    The ``translate`` function supports translation message dynamically
    with standard i18n vstutils'es mechanisms usage.

    Uses :func:`django.utils.translation.get_language` to get the language code and
    tries to get the translation from the list of available ones.

    :param text: Text message which should be translated.
    """
    try:
        return current_lang(lang=get_language()).translate(text)
    except Exception:
        return text

def lazy_translate(text: tp.Text) -> functional.Promise:
    """
    The ``lazy_translate`` function has the same behavior as :func:`.translate`, but wraps it in a lazy promise.

    This is very useful, for example, for translating error messages in
    class attributes before the language code is known.

    :param text: Text message which should be translated.
    """
    return functional.lazy(translate, str)(text)

def create_view(model, **meta_options):
    """
    A simple function for getting the generated view by standard means, but with overloaded meta-parameters.
    This method can completely get rid of the creation of proxy models.

    Example:
        .. sourcecode:: python

            from vstutils.utils import create_view

            from .models import Host

            # Host model has full :class:`vstutils.api.base.ModelViewSet` view.
            # For overriding and create simple list view just setup this:
            HostListViewSet = create_view(
                HostList,
                view_class='list_only'
            )


    .. note::
        This method is also recommended in cases where there is a problem of recursive imports.


    :type model: Type[vstutils.models.BaseModel]
    :param model: Model class with `.get_view_class` method. This method also has :class:`vstutils.models.BModel`.
    :rtype: vstutils.api.base.GenericViewSet
    """
    return model.get_view_class(**meta_options)

class apply_decorators:
    """
    Decorator which apply list of decorators on method or class.

    Example:
        .. sourcecode:: python

            from vstutils.utils import apply_decorators

            def decorator_one(func):
                print(f"Decorated {func.__name__} by first decorator.")
                return func

            def decorator_two(func):
                print(f"Decorated {func.__name__} by second decorator.")
                return func

            @apply_decorators(decorator_one, decorator_two)
            def decorated_function():
                # Function decorated by both decorators.
                print("Function call.")
    """
    __slots__ = ('decorators',)

    def __init__(self, *decorators):
        self.decorators = decorators

    def __call__(self, func):
        for decorator in self.decorators:
            func = decorator(func)
        return func

class ClassPropertyMeta(type):

    def __setattr__(cls, key, value):
        obj = cls.__dict__.get(key, None)
        if isinstance(obj, ClassPropertyDescriptor):
            return obj.__set__(cls, value)
        return super().__setattr__(key, value)

class ClassPropertyDescriptor:
    __slots__ = ('fget', 'fset')
    meta = ClassPropertyMeta

    def __init__(self, fget: tp.Callable, fset: tp.Callable=None):
        self.fget, self.fset = (self._fix_function(fget), self._fix_function(fset))

    def __get__(self, obj, klass=None):
        if obj is not None:
            return self.fget.__get__(obj, obj)()
        return self.fget.__get__(obj, type(obj) if klass is None else klass)()

    def __set__(self, obj: tp.Any, value: tp.Any):
        if not self.fset:
            raise AttributeError("can't set attribute")
        if obj is not None:
            return self.fset.__get__(obj, obj)(value)
        return self.fset.__get__(obj, type(obj))(value)

    def setter(self, func: tp.Union[tp.Callable, classmethod]):
        self.fset = self._fix_function(func)
        return self

    @classmethod
    def _fix_function(cls, func):
        if func is None:
            return func
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        return func

class classproperty(ClassPropertyDescriptor):
    """
    Decorator which makes class method as class property.

    Example:
        .. sourcecode:: python

            from vstutils.utils import classproperty

            class SomeClass(metaclass=classproperty.meta):
                # Metaclass is needed for set attrs in class
                # instead of and not only object.

                some_value = None

                @classproperty
                def value(cls):
                    return cls.some_value

                @value.setter
                def value(cls, new_value):
                    cls.some_value = new_value
    """

class redirect_stdany:
    """
    Context for redirect any output to own stream.

    .. note::
        - On context return stream object.
        - On exit return old streams
    """
    __slots__ = ('stream', 'streams', '_old_streams')
    _streams: tp.ClassVar[tp.List[tp.Text]] = ['stdout', 'stderr']

    def __init__(self, new_stream=io.StringIO(), streams=None):
        """
        :param new_stream: -- stream where redirects all
        :type new_stream: object
        :param streams: -- names of streams like ``['stdout', 'stderr']``
        :type streams: list
        """
        self.streams = streams or self._streams
        self.stream = new_stream
        self._old_streams = {}

    def __enter__(self):
        for stream in self.streams:
            self._old_streams[stream] = getattr(sys, stream)
            setattr(sys, stream, self.stream)
        return self.stream

    def __exit__(self, exctype, excinst, exctb):
        for stream in self.streams:
            setattr(sys, stream, self._old_streams.pop(stream))

class Dict(dict):
    """
    Wrapper over `dict` which
    return JSON on conversion to string.
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.copy())

class tmp_file:
    """
    Temporary file with name
    generated and auto removed on close.

    **Attributes**:

    :param data: -- string to write in tmp file.
    :type data: str
    :param mode: -- file open mode. Default 'w'.
    :type mode: str
    :param bufsize: -- bufer size for tempfile.NamedTemporaryFile
    :type bufsize: int
    :param kwargs:  -- other kwargs for tempfile.NamedTemporaryFile

    """
    __slots__ = ('fd', 'path')

    def __init__(self, data: tp.Text='', mode: tp.Text='w', bufsize: int=-1, **kwargs):
        self.fd = tempfile.NamedTemporaryFile(mode, buffering=bufsize, **kwargs)
        self.path = Path(self.fd.name)
        if data:
            self.write(data)

    def write(self, wr_string: tp.Text):
        """
        Write to file and flush

        :param wr_string: -- writable string
        :type wr_string: str
        :return: None
        :rtype: None
        """
        result = self.fd.write(wr_string)
        self.fd.flush()
        return result

    def __getattr__(self, name: tp.Text):
        return getattr(self.fd, name)

    def __del__(self):
        with raise_context():
            self.fd.close()

    def __enter__(self):
        """
        :return: -- file object
        :rtype: tempfile.NamedTemporaryFile
        """
        return self

    def __exit__(self, type_e, value, tb):
        self.fd.close()

class tmp_file_context:
    """
    Context object for work with tmp_file.
    Auto close on exit from context and
    remove if file still exist.

    This context manager over :class:`.tmp_file`
    """
    __slots__ = ('tmp',)

    def __init__(self, *args, **kwargs):
        self.tmp: tempfile.NamedTemporaryFile = tmp_file(*args, **kwargs)

    def __enter__(self):
        return self.tmp

    def __exit__(self, type_e, value, tb):
        self.tmp.close()
        if self.tmp.path.exists():
            self.tmp.path.unlink()

class assertRaises:
    __slots__ = ('_kwargs', '_verbose', '_exclude', '_excepts', '_log', '__failed')

    def __init__(self, *args, **kwargs):
        """
        :param args: -- list of exception classes should be passed
        :type args: list,Exception
        :param exclude: -- list of exception classes should be raised
        :type exclude: list,Exception
        :param verbose: -- logging
        :type verbose: bool
        """
        self._kwargs = dict(**kwargs)
        self._verbose = kwargs.pop('verbose', settings.DEBUG)
        self._exclude = kwargs.pop('exclude', False)
        self._excepts = tuple(args)
        self.__failed = False

    def mark_as_failed(self):
        self.__failed = True

    def cleanup_fails(self):
        self.__failed = False

    @property
    def is_failed(self):
        return self.__failed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is not None and (not self._exclude and (not issubclass(exc_type, self._excepts)) or (self._exclude and issubclass(exc_type, self._excepts)))

class raise_context(assertRaises):
    """
    Context for exclude exceptions.
    """
    __slots__ = ()

    def execute(self, func: tp.Callable, *args, **kwargs):
        self.cleanup_fails()
        with self.__class__(self._excepts, **self._kwargs):
            try:
                return func(*args, **kwargs)
            except:
                self.mark_as_failed()
                type, value, traceback_obj = sys.exc_info()
                if self._verbose:
                    logger.debug(traceback.format_exc())
                raise
        return (type, value, traceback_obj)

    def __enter__(self):
        return self.execute

    def __call__(self, original_function: tp.Callable):

        def wrapper(*args, **kwargs):
            return self.execute(original_function, *args, **kwargs)
        return wrapper

class raise_context_decorator_with_default(raise_context):
    """
    Context for exclude errors and return default value.

    Example:
        .. sourcecode:: python

            from yaml import load
            from vstutils.utils import raise_context_decorator_with_default


            @raise_context_decorator_with_default(default={})
            def get_host_data(yaml_path, host):
                with open(yaml_path, 'r') as fd:
                    data = load(fd.read(), Loader=Loader)
                return data[host]
                # This decorator used when you must return some value even on error
                # In log you also can see traceback for error if it occur

            def clone_host_data(host):
                bs_data = get_host_data('inventories/aws/hosts.yml', 'build_server')
                ...

    """
    __slots__ = ('default_value',)

    def __init__(self, *args, **kwargs):
        self.default_value = kwargs.pop('default', None)
        super().__init__(*args, **kwargs)

    def execute(self, func: tp.Callable, *args, **kwargs):
        result = super().execute(func, *args, **kwargs)
        if self.is_failed:
            return self.default_value
        return result

class exception_with_traceback(raise_context):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            exc_val.traceback = traceback.format_exc()
            raise exc_val.with_traceback(exc_tb)

class BaseVstObject:
    """
    Default mixin-class for custom objects which needed to get settings and cache.
    """
    __slots__ = ()

    @classmethod
    def get_django_settings(cls, name: tp.Text, default: tp.Any=None):
        """
        Get params from Django settings.

        :param name: name of param
        :type name: str
        :param default: default value of param
        :type default: object
        :return: Param from Django settings or default.
        """
        return getattr(settings, name, default)

    @classmethod
    def get_django_cache(cls, cache_name: tp.Text='default'):
        try:
            return caches[cache_name]
        except InvalidCacheBackendError:
            return caches['default']

class SecurePickling(BaseVstObject):
    """
    Secured pickle wrapper by Vigenère cipher.


    .. warning::
        Do not use it with untrusted transport anyway.

    Example:
        .. sourcecode:: python

            from vstutils.utils import SecurePickling


            serializer = SecurePickling('password')

            # Init secret object
            a = {"key": "value"}
            # Serialize object with secret key
            pickled = serializer.dumps(a)
            # Deserialize object
            unpickled = serializer.loads(pickled)

            # Check, that object is correct
            assert a == unpickled

    """
    __slots__ = ('secure_key',)

    def __init__(self, secure_key: tp.Optional[tp.Text]=None):
        """
        :param secure_key: Secret key for encoding.
        """
        if secure_key is None:
            secure_key = self.get_django_settings('SECRET_KEY')
        self.secure_key = str(secure_key)

    def _encode(self, value: tp.Text):
        return encode(self.secure_key, value)

    def _decode(self, value: tp.Text):
        return decode(self.secure_key, value)

    def loads(self, value: tp.Any):
        return pickle.loads(codecs.decode(self._decode(value).encode(), 'base64'))

    def dumps(self, value: tp.Any):
        return self._encode(codecs.encode(pickle.dumps(value), 'base64').decode())

class Executor(BaseVstObject):
    """
    Command executor with realtime output write and line handling.
    By default and by design executor initialize string attribute ``output``
    which will be modifyed by ``+=`` operator with new lines by :meth:`.Executor.write_output`
    procedure. Override the method if you want change behavior.

    Executor class supports periodically (0.01 sec) handling process and execute some checks
    by overriding :meth:`.Executor.working_handler` procedure method. If you want disable this behavior
    override the method by None value or use :class:`.UnhandledExecutor`.
    """
    __slots__ = ('output', '__stdout__', '__stderr__', 'env')
    CANCEL_PREFIX: tp.ClassVar[tp.Text] = 'CANCEL_EXECUTE_'
    newlines: tp.ClassVar[tp.List[tp.Text]] = ['\n', '\r\n', '\r']
    STDOUT: tp.ClassVar[int] = subprocess.PIPE
    STDERR: tp.ClassVar[int] = subprocess.STDOUT
    DEVNULL: tp.ClassVar[int] = subprocess.DEVNULL
    CalledProcessError: tp.ClassVar[tp.Type[subprocess.CalledProcessError]] = subprocess.CalledProcessError
    env: tp.Dict[tp.Text, tp.Text]

    def __init__(self, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **environ_variables):
        """
        :type stdout: BinaryIO,int
        :type stderr: BinaryIO,int
        """
        self.output = ''
        self.__stdout__ = stdout
        self.__stderr__ = stderr
        self.env = environ_variables

    def write_output(self, line: tp.Text) -> None:
        """
        :param line: -- line from command output
        :type line: str
        :return: None
        :rtype: None
        """
        self.output += str(line)

    def _handle_process(self, proc: subprocess.Popen, stream: tp.Text):
        stream_object = getattr(proc, stream)
        while not stream_object.closed:
            self.working_handler(proc)
            time.sleep(0.01)

    def working_handler(self, proc: subprocess.Popen) -> None:
        """
        Additional handler for executions.

        :type proc: subprocess.Popen
        """

    def _unbuffered(self, proc: subprocess.Popen, stream: tp.Text='stdout'):
        """
        Unbuffered output handler.

        :type proc: subprocess.Popen
        :type stream: str
        :return:
        """
        if self.working_handler is not None:
            t = Thread(target=self._handle_process, args=(proc, stream))
            t.start()
        out = getattr(proc, stream)
        try:
            retcode = None
            while retcode is None:
                for line in iter(out.readline, ''):
                    yield line.rstrip()
                retcode = proc.poll()
        finally:
            out.close()

    def line_handler(self, line: tp.Text) -> None:
        if line is not None:
            with raise_context():
                self.write_output(line)

    def execute(self, cmd: tp.List[tp.Text], cwd: tp.Union[tp.Text, Path]) -> tp.Text:
        """
        Execute commands and output this.

        :param cmd: -- list of cmd command and arguments
        :type cmd: list
        :param cwd: -- workdir for executions
        :type cwd: str
        :return: -- string with full output
        :rtype: str
        """
        self.output = ''
        env = os.environ.copy()
        env.update(self.env)
        with subprocess.Popen(cmd, stdout=self.__stdout__, stderr=self.__stderr__, bufsize=0, universal_newlines=True, cwd=str(cwd), env=env, close_fds=ON_POSIX) as proc:
            for line in self._unbuffered(proc):
                self.line_handler(line)
            return_code = proc.poll()
            if return_code:
                logger.error(self.output)
                raise subprocess.CalledProcessError(return_code, cmd, output=str(self.output))
        return self.output

class UnhandledExecutor(Executor):
    """
    Class based on :class:`.Executor` but disables `working_handler`.
    """
    __slots__ = ()
    working_handler = None

class KVExchanger(BaseVstObject):
    """
    Class for transmit data using key-value fast (cache-like) storage between
    services. Uses same cache-backend as Lock.
    """
    __slots__ = ('key', 'timeout', '__djangocache__')
    TIMEOUT: tp.ClassVar[int] = 60

    @classproperty
    def PREFIX(cls):
        return f"{cls.get_django_settings('VST_PROJECT_LIB')}_exchange_"

    @classproperty
    def cache(cls):
        if hasattr(cls, '__djangocache__') and (not is_member_descriptor(cls.__djangocache__)):
            return cls.__djangocache__
        cls.__djangocache__ = cls.get_django_cache('locks')
        return cls.cache

    def __init__(self, key, timeout=None):
        self.key = self.PREFIX + str(key)
        self.timeout = timeout or self.TIMEOUT

    def send(self, value, ttl=None):
        return self.cache.add(self.key, value, ttl or self.timeout)

    def prolong(self, ttl=None):
        self.cache.touch(self.key, ttl or self.timeout)

    def get(self):
        value = self.cache.get(self.key)
        self.cache.delete(self.key)
        return value

    def delete(self):
        self.cache.delete(self.key)

class Lock(KVExchanger):
    """
    Lock class for multi-jobs workflow. Based on :class:`.KVExchanger`.
    The Lock allows only one thread to enter the part that's locked and shared
    between apps using one locks cache (see also `[locks] <config.html#locks-settings>`_).


    :param id: -- unique id for lock.
    :type id: int,str
    :param payload: -- lock additional info. Should be any boolean True value.
    :param repeat: -- time to wait lock.release. Default 1 sec.
    :type repeat: int
    :param err_msg: -- message for AcquireLockException error.
    :type err_msg: str

    .. note::
        - Used django.core.cache lib and settings in `settings.py`
        - Have Lock.SCHEDULER and Lock.GLOBAL id

    Example:
        .. sourcecode:: python

            from vstutils.utils import Lock

            with Lock("some_lock_identifier", repeat=30, err_msg="Locked by another proccess") as lock:
                # where
                # ``"some_lock_identifier"`` is unique id for lock and
                # ``30`` seconds lock is going wait until another process will release lock id.
                # After 30 sec waiting lock will raised with :class:`.Lock.AcquireLockException`
                # and ``err_msg`` value as text.
                some_code_execution()
                # ``lock`` object will has been automatically released after
                # exiting from context.

    Another example without context manager:
        .. sourcecode:: python

            from vstutils.utils import Lock

            # locked block after locked object created
            lock = Lock("some_lock_identifier", repeat=30, err_msg="Locked by another proccess")
            # deleting of object calls ``lock.release()`` which release and remove lock from id.
            del lock

    """
    __slots__ = ('id', 'payload_data')
    TIMEOUT: tp.ClassVar[int] = 60 * 60 * 24
    GLOBAL: tp.ClassVar[tp.Text] = 'global-deploy'
    SCHEDULER: tp.ClassVar[tp.Text] = 'celery-beat'

    class AcquireLockException(Exception):
        """ Exception which will raised on unreleased lock. """

    @classproperty
    def PREFIX(cls):
        return f"{cls.get_django_settings('VST_PROJECT_LIB')}_lock_"

    def __init__(self, id, payload=1, repeat=1, err_msg='', timeout=None):
        super().__init__(id, timeout)
        self.payload_data = f'{uuid.uuid4()}_{payload}'
        self.id, start = (None, time.time())
        while time.time() - start <= repeat:
            if self.send(self.payload_data) and (not time.sleep(random.random())) and (self.get() == self.payload_data):
                logger.debug(f'Acquire lock with id `{id}` and payload `{self.payload_data}`')
                self.id = id
                return
            time.sleep(random.random() / 10)
        raise self.AcquireLockException(err_msg)

    def get(self):
        return self.cache.get(self.key)

    def __enter__(self):
        return self

    def __exit__(self, type_e, value, tb):
        self.release()

    def release(self, force_release=False):
        if force_release or self.id is not None:
            self.cache.delete(self.key)

    def __del__(self):
        self.release()

class __LockAbstractDecorator:
    __slots__ = ('kwargs',)
    _err = 'Wait until the end.'
    _lock_key = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs['err_msg'] = self.kwargs.get('err_msg', self._err)

    def execute(self, func, *args, **kwargs):
        if self._lock_key is not None:
            with Lock(self._lock_key, **self.kwargs):
                return func(*args, **kwargs)
        return func(*args, **kwargs)

    def __call__(self, original_function):

        @wraps(original_function)
        def wrapper(*args, **kwargs):
            return self.execute(original_function, *args, **kwargs)
        return wrapper

class model_lock_decorator(__LockAbstractDecorator):
    """
    Decorator for functions where 'pk' kwarg exist
    for lock by id.

    .. warning::
        - On locked error raised ``Lock.AcquireLockException``
        - Method must have and called with ``pk`` named arg.

    """
    __slots__ = ('_lock_key',)
    _err = 'Object locked. Wait until unlock.'

    def execute(self, func, *args, **kwargs):
        self._lock_key = kwargs.get('pk', None)
        return super().execute(func, *args, **kwargs)

class Paginator(BasePaginator):
    """
    Class for fragmenting the query for small queries.
    """
    __slots__ = ()

    def __init__(self, qs, chunk_size=None):
        """
        :param qs: -- queryset for fragmenting
        :type qs: django.db.models.QuerySet
        :param chunk_size: -- size of the fragments.
        :type chunk_size: int
        """
        chunk_size = chunk_size or BaseVstObject().get_django_settings('PAGE_LIMIT', None)
        super().__init__(qs, chunk_size)

    def __iter__(self):
        for page in range(1, self.num_pages + 1):
            yield self.page(page)

    def items(self):
        for page in self:
            for obj in page.object_list:
                obj.paginator = self
                obj.page = page
                yield obj

class ObjectHandlers(BaseVstObject):
    """
    Handlers wrapper for get objects from some settings structure.

    Example:
        .. sourcecode:: python

            from vstutils.utils import ObjectHandlers

            '''
            In `settings.py` you should write some structure:

            SOME_HANDLERS = {
                "one": {
                    "BACKEND": "full.python.path.to.module.SomeClass"
                },
                "two": {
                    "BACKEND": "full.python.path.to.module.SomeAnotherClass",
                    "OPTIONS": {
                        "some_named_arg": "value"
                    }
                }
            }
            '''

            handlers = ObjectHandlers('SOME_HANDLERS')

            # Get class handler for 'one'
            one_backend_class = handlers['one']
            # Get object of backend 'two'
            two_obj = handlers.get_object()
            # Get object of backend 'two' with overriding constructor named arg
            two_obj_overrided = handlers.get_object(some_named_arg='another_value')

    """
    __slots__ = ('type', 'err_message', '__list__', '__loaded_backends__')
    type: tp.Text
    err_message: tp.Optional[tp.Text]

    def __init__(self, type_name: tp.Text, err_message: tp.Text=None):
        """
        :param type_name: -- type name for backends.Like name in dict.
        :type type_name: str
        """
        self.type = type_name
        self.err_message = err_message
        self.__list__: tp.Optional[tp.Dict[tp.Text, tp.Any]] = None
        self.__loaded_backends__: tp.Dict[tp.Text, tp.Any] = {}

    @property
    def objects(self):
        return {name: self[name] for name in self.list()}

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.items())

    def __getitem__(self, name: tp.Text) -> tp.Any:
        return self.backend(name)

    def __call__(self, name, obj):
        return self.get_object(name, obj)

    def __dict__(self):
        return self.items()

    def keys(self) -> tp.Iterable[tp.Text]:
        return self.objects.keys()

    def values(self) -> tp.Iterable:
        return dict(self).values()

    def items(self):
        return self.objects.items()

    def list(self) -> tp.Dict[tp.Text, tp.Dict[tp.Text, tp.Any]]:
        if self.__list__ is None:
            self.__list__ = self.get_django_settings(self.type, {})
        return self.__list__

    def _get_backend(self, backend):
        if backend in self.__loaded_backends__:
            return self.__loaded_backends__[backend]
        self.__loaded_backends__[backend] = import_class(backend)
        return self.__loaded_backends__[backend]

    def get_backend_data(self, name: tp.Text):
        return self.list()[name]

    def get_backend_handler_path(self, name: tp.Text):
        return self.get_backend_data(name).get('BACKEND', None)

    def backend(self, name: tp.Text):
        """
        Get backend class

        :param name: -- name of backend type
        :type name: str
        :return: class of backend
        :rtype: type,types.ModuleType,object
        """
        try:
            backend = self.get_backend_handler_path(name)
            if backend is None:
                raise ex.VSTUtilsException("Backend is 'None'.")
            return self._get_backend(backend)
        except KeyError or ImportError as err:
            msg = f'{name} ({self.err_message})' if self.err_message else name
            raise ex.UnknownTypeException(msg) from err

    def opts(self, name: tp.Text):
        return self.get_backend_data(name).get('OPTIONS', {})

    def get_object(self, name: tp.Text, *args, **kwargs):
        opts = self.opts(name)
        opts.update(kwargs)
        return self[name](*args, **opts)

class StaticFilesHandlers(ObjectHandlers):

    def opts(self, name):
        opts = super().opts(name)
        opts['name'] = name
        return opts

    def get_static_objects(self):
        for name in self.keys():
            for result in self.get_object(name).spa_static_list:
                yield result

    def get_sorted_list(self):
        return tuple(multikeysort(self.get_static_objects(), ['priority']))

class ModelHandlers(ObjectHandlers):
    """
    Handlers for some models like 'INTEGRATIONS' or 'REPO_BACKENDS'.
    Based on :class:`.ObjectHandlers` but more specific for working with models.
    All handlers backends get by first argument model object.

    **Attributes**:

    :param objects: -- dict of objects like: ``{<name>: <backend_class>}``
    :type objects: dict
    :param keys: -- names of supported backends
    :type keys: list
    :param values: -- supported backends classes
    :type values: list
    """
    __slots__ = ()

    def get_object(self, name: tp.Text, obj) -> tp.Any:
        """
        :param name: -- string name of backend
        :param name: str
        :param obj: -- model object
        :type obj: django.db.models.Model
        :return: backend object
        :rtype: object
        """
        return self[name](obj, **self.opts(name))

class URLHandlers(ObjectHandlers):
    """
    Object handler for GUI views. Uses `GUI_VIEWS` from settings.py.
    Based on :class:`.ObjectHandlers` but more specific to urlpatterns.

    Example:
        .. sourcecode:: python

            from vstutils.utils import URLHandlers


            # By default gets from `GUI_VIEWS` in `settings.py`
            urlpatterns = list(URLHandlers())
    """
    __slots__ = ('additional_handlers', '__handlers__', 'default_namespace')
    settings_urls: tp.ClassVar[tp.List[tp.Text]] = ['LOGIN_URL', 'LOGOUT_URL']
    additional_handlers: tp.List[tp.Text]

    def __init__(self, type_name: tp.Text='URLS', *args, **kwargs):
        self.additional_handlers = kwargs.pop('additional_handlers', ['VIEWS']) + [type_name]
        self.default_namespace = kwargs.pop('namespace', None)
        self.__handlers__ = None
        super().__init__(type_name, *args, **kwargs)

    @property
    def view_handlers(self):
        if not self.__handlers__:
            self.__handlers__ = tuple(map(self.__class__, self.additional_handlers))
        return self.__handlers__

    def get_backend_data(self, name: tp.Text):
        data = super().get_backend_data(name)
        if isinstance(data, str):
            for handler in self.view_handlers:
                try:
                    return handler.get_backend_data(data)
                except:
                    continue
            raise ex.VSTUtilsException(f'Invalid handler name "{data}"')
        return data

    def get_object(self, name: tp.Text, *argv, **kwargs):
        """
        Get url object tuple for urls.py

        :param name: url regexp from
        :type name: str
        :param argv: overrided args
        :param kwargs: overrided kwargs
        :return: url object
        :rtype: django.urls.re_path
        """
        regexp = name
        options = self.opts(regexp)
        options.update(kwargs)
        args = options.pop('view_args', argv)
        view_kwargs = options.pop('view_kwargs', {})
        csrf_enable = self.get_backend_data(regexp).get('CSRF_ENABLE', True)
        if regexp in self.settings_urls:
            regexp = f'^{self.get_django_settings(regexp)[1:]}'
        view_class = self[name]
        namespace = view_kwargs.pop('namespace', self.default_namespace)
        result: tp.Union[tp.Tuple, types.ModuleType]
        if isinstance(view_class, View) or hasattr(view_class, 'as_view'):
            view = view_class.as_view(**view_kwargs)
            if not csrf_enable:
                view = csrf_exempt(view)
            return re_path(regexp, view, *args, **options)
        elif isinstance(view_class, types.ModuleType) and hasattr(view_class, 'urlpatterns') and hasattr(view_class, 'app_name'):
            result = view_class
            namespace = None
        else:
            result = (view_class, 'gui')
        return re_path(regexp, include(result, namespace=namespace), *args, **view_kwargs)

    def urls(self) -> tp.Iterable:
        for regexp in self.list():
            yield self.get_object(regexp)

    def __iter__(self):
        return self.urls()

class BaseEnum(str, Enum):
    """
    BaseEnum extends `Enum` class and used to create enum-like objects that can be used in django serializers or
    django models.

    Example:

        .. sourcecode:: python

            from vstutils.models import BModel

            class ItemCLasses(BaseEnum):
                FIRST='FIRST'
                SECOND='SECOND'
                THIRD='THIRD'


            class MyDjangoModel(BModel):
                item_class = models.CharField(max_length=1024, choices=ItemCLasses.to_choices())

                @property
                def is_second(self):
                    # Function check is item has second class of instance
                    return ItemCLasses.SECOND.is_equal(self.item_class)

    """

    def __new__(cls, name):
        return str.__new__(cls, name)

    def __repr__(self):
        return repr(self.__str__())

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def get_names(cls):
        return tuple((x.name for x in cls))

    @classmethod
    def to_choices(cls):
        return list_to_choices(cls.get_names())

    def is_equal(self, cmp_str):
        return str(cmp_str) == str(self)

    def not_equal(self, cmp_str):
        return not self.is_equal(cmp_str)