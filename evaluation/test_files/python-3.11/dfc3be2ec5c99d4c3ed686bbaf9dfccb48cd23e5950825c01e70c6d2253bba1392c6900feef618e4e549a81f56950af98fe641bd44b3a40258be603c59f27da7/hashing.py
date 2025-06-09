"""A hashing utility for code."""
import collections
import dis
import enum
import functools
import hashlib
import importlib
import inspect
import io
import os
import pickle
import sys
import tempfile
import textwrap
import threading
import typing
import unittest.mock
import weakref
from typing import Any, Callable, Dict, List, Optional, Pattern, Union
from streamlit import config, file_util, type_util, util
from streamlit.errors import MarkdownFormattedException, StreamlitAPIException
from streamlit.folder_black_list import FolderBlackList
from streamlit.logger import get_logger
from streamlit.runtime.uploaded_file_manager import UploadedFile
_LOGGER = get_logger(__name__)
_PANDAS_ROWS_LARGE = 100000
_PANDAS_SAMPLE_SIZE = 10000
_NP_SIZE_LARGE = 1000000
_NP_SAMPLE_SIZE = 100000
_CYCLE_PLACEHOLDER = b'streamlit-57R34ML17-hesamagicalponyflyingthroughthesky-CYCLE'
_FOLDER_BLACK_LIST = None
_FFI_TYPE_NAMES = ['_cffi_backend.FFI', 'builtins.CompiledFFI']
_KERAS_TYPE_NAMES = ['keras.engine.training.Model', 'tensorflow.python.keras.engine.training.Model', 'tensorflow.python.keras.engine.functional.Functional']
Context = collections.namedtuple('Context', ['globals', 'cells', 'varnames'])
HashFuncsDict = Dict[Union[str, typing.Type[Any]], Callable[[Any], Any]]

class HashReason(enum.Enum):
    CACHING_FUNC_ARGS = 0
    CACHING_FUNC_BODY = 1
    CACHING_FUNC_OUTPUT = 2
    CACHING_BLOCK = 3

def update_hash(val: Any, hasher, hash_reason: HashReason, hash_source: Callable[..., Any], context: Optional[Context]=None, hash_funcs: Optional[HashFuncsDict]=None) -> None:
    """Updates a hashlib hasher with the hash of val.

    This is the main entrypoint to hashing.py.
    """
    hash_stacks.current.hash_reason = hash_reason
    hash_stacks.current.hash_source = hash_source
    ch = _CodeHasher(hash_funcs)
    ch.update(hasher, val, context)

class _HashStack:
    """Stack of what has been hashed, for debug and circular reference detection.

    This internally keeps 1 stack per thread.

    Internally, this stores the ID of pushed objects rather than the objects
    themselves because otherwise the "in" operator inside __contains__ would
    fail for objects that don't return a boolean for "==" operator. For
    example, arr == 10 where arr is a NumPy array returns another NumPy array.
    This causes the "in" to crash since it expects a boolean.
    """

    def __init__(self):
        self._stack: collections.OrderedDict[int, List[Any]] = collections.OrderedDict()
        self.hash_reason: Optional[HashReason] = None
        self.hash_source: Optional[Callable[..., Any]] = None

    def __repr__(self) -> str:
        return util.repr_(self)

    def push(self, val: Any):
        self._stack[id(val)] = val

    def pop(self):
        self._stack.popitem()

    def __contains__(self, val: Any):
        return id(val) in self._stack

    def pretty_print(self):

        def to_str(v):
            try:
                return 'Object of type %s: %s' % (type_util.get_fqn_type(v), str(v))
            except:
                return '<Unable to convert item to string>'
        return '\n'.join((to_str(x) for x in reversed(self._stack.values())))

class _HashStacks:
    """Stacks of what has been hashed, with at most 1 stack per thread."""

    def __init__(self):
        self._stacks: weakref.WeakKeyDictionary[threading.Thread, _HashStack] = weakref.WeakKeyDictionary()

    def __repr__(self) -> str:
        return util.repr_(self)

    @property
    def current(self) -> _HashStack:
        current_thread = threading.current_thread()
        stack = self._stacks.get(current_thread, None)
        if stack is None:
            stack = _HashStack()
            self._stacks[current_thread] = stack
        return stack
hash_stacks = _HashStacks()

class _Cells:
    """
    This is basically a dict that allows us to push/pop frames of data.

    Python code objects are nested. In the following function:

        @st.cache()
        def func():
            production = [[x + y for x in range(3)] for y in range(5)]
            return production

    func.__code__ is a code object, and contains (inside
    func.__code__.co_consts) additional code objects for the list
    comprehensions. Those objects have their own co_freevars and co_cellvars.

    What we need to do as we're traversing this "tree" of code objects is to
    save each code object's vars, hash it, and then restore the original vars.
    """
    _cell_delete_obj = object()

    def __init__(self):
        self.values = {}
        self.stack = []
        self.frames = []

    def __repr__(self) -> str:
        return util.repr_(self)

    def _set(self, key, value):
        """
        Sets a value and saves the old value so it can be restored when
        we pop the frame. A sentinel object, _cell_delete_obj, indicates that
        the key was previously empty and should just be deleted.
        """
        self.stack.append((key, self.values.get(key, self._cell_delete_obj)))
        self.values[key] = value

    def pop(self):
        """Pop off the last frame we created, and restore all the old values."""
        idx = self.frames.pop()
        for key, val in self.stack[idx:]:
            if val is self._cell_delete_obj:
                del self.values[key]
            else:
                self.values[key] = val
        self.stack = self.stack[:idx]

    def push(self, code, func=None):
        """Create a new frame, and save all of `code`'s vars into it."""
        self.frames.append(len(self.stack))
        for var in code.co_cellvars:
            self._set(var, var)
        if code.co_freevars:
            if func is not None:
                assert len(code.co_freevars) == len(func.__closure__)
                for var, cell in zip(code.co_freevars, func.__closure__):
                    self._set(var, cell.cell_contents)
            else:
                for var in code.co_freevars:
                    self._set(var, var)

def _get_context(func) -> Context:
    varnames = {}
    if inspect.ismethod(func):
        varnames = {'self': func.__self__}
    return Context(globals=func.__globals__, cells=_Cells(), varnames=varnames)

def _int_to_bytes(i: int) -> bytes:
    num_bytes = (i.bit_length() + 8) // 8
    return i.to_bytes(num_bytes, 'little', signed=True)

def _key(obj: Optional[Any]) -> Any:
    """Return key for memoization."""
    if obj is None:
        return None

    def is_simple(obj):
        return isinstance(obj, bytes) or isinstance(obj, bytearray) or isinstance(obj, str) or isinstance(obj, float) or isinstance(obj, int) or isinstance(obj, bool) or (obj is None)
    if is_simple(obj):
        return obj
    if isinstance(obj, tuple):
        if all(map(is_simple, obj)):
            return obj
    if isinstance(obj, list):
        if all(map(is_simple, obj)):
            return ('__l', tuple(obj))
    if type_util.is_type(obj, 'pandas.core.frame.DataFrame') or type_util.is_type(obj, 'numpy.ndarray') or inspect.isbuiltin(obj) or inspect.isroutine(obj) or inspect.iscode(obj):
        return id(obj)
    return NoResult

class _CodeHasher:
    """A hasher that can hash code objects including dependencies."""

    def __init__(self, hash_funcs: Optional[HashFuncsDict]=None):
        self._hash_funcs: HashFuncsDict
        if hash_funcs:
            self._hash_funcs = {k if isinstance(k, str) else type_util.get_fqn(k): v for k, v in hash_funcs.items()}
        else:
            self._hash_funcs = {}
        self._hashes: Dict[Any, bytes] = {}
        self.size = 0

    def __repr__(self) -> str:
        return util.repr_(self)

    def to_bytes(self, obj: Any, context: Optional[Context]=None) -> bytes:
        """Add memoization to _to_bytes and protect against cycles in data structures."""
        tname = type(obj).__qualname__.encode()
        key = (tname, _key(obj))
        if key[1] is not NoResult:
            if key in self._hashes:
                return self._hashes[key]
        if obj in hash_stacks.current:
            return _CYCLE_PLACEHOLDER
        hash_stacks.current.push(obj)
        try:
            b = b'%s:%s' % (tname, self._to_bytes(obj, context))
            self.size += sys.getsizeof(b)
            if key[1] is not NoResult:
                self._hashes[key] = b
        except (UnhashableTypeError, UserHashError, InternalHashError):
            raise
        except BaseException as e:
            raise InternalHashError(e, obj)
        finally:
            hash_stacks.current.pop()
        return b

    def update(self, hasher, obj: Any, context: Optional[Context]=None) -> None:
        """Update the provided hasher with the hash of an object."""
        b = self.to_bytes(obj, context)
        hasher.update(b)

    def _file_should_be_hashed(self, filename: str) -> bool:
        global _FOLDER_BLACK_LIST
        if not _FOLDER_BLACK_LIST:
            _FOLDER_BLACK_LIST = FolderBlackList(config.get_option('server.folderWatchBlacklist'))
        filepath = os.path.abspath(filename)
        file_is_blacklisted = _FOLDER_BLACK_LIST.is_blacklisted(filepath)
        if file_is_blacklisted:
            return False
        return file_util.file_is_in_folder_glob(filepath, self._get_main_script_directory()) or file_util.file_in_pythonpath(filepath)

    def _to_bytes(self, obj: Any, context: Optional[Context]) -> bytes:
        """Hash objects to bytes, including code with dependencies.

        Python's built in `hash` does not produce consistent results across
        runs.
        """
        if isinstance(obj, unittest.mock.Mock):
            return self.to_bytes(id(obj))
        elif isinstance(obj, bytes) or isinstance(obj, bytearray):
            return obj
        elif type_util.get_fqn_type(obj) in self._hash_funcs:
            hash_func = self._hash_funcs[type_util.get_fqn_type(obj)]
            try:
                output = hash_func(obj)
            except BaseException as e:
                raise UserHashError(e, obj, hash_func=hash_func)
            return self.to_bytes(output)
        elif isinstance(obj, str):
            return obj.encode()
        elif isinstance(obj, float):
            return self.to_bytes(hash(obj))
        elif isinstance(obj, int):
            return _int_to_bytes(obj)
        elif isinstance(obj, (list, tuple)):
            h = hashlib.new('md5')
            for item in obj:
                self.update(h, item, context)
            return h.digest()
        elif isinstance(obj, dict):
            h = hashlib.new('md5')
            for item in obj.items():
                self.update(h, item, context)
            return h.digest()
        elif obj is None:
            return b'0'
        elif obj is True:
            return b'1'
        elif obj is False:
            return b'0'
        elif type_util.is_type(obj, 'pandas.core.frame.DataFrame') or type_util.is_type(obj, 'pandas.core.series.Series'):
            import pandas as pd
            if len(obj) >= _PANDAS_ROWS_LARGE:
                obj = obj.sample(n=_PANDAS_SAMPLE_SIZE, random_state=0)
            try:
                return b'%s' % pd.util.hash_pandas_object(obj).sum()
            except TypeError:
                return b'%s' % pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
        elif type_util.is_type(obj, 'numpy.ndarray'):
            h = hashlib.new('md5')
            self.update(h, obj.shape)
            if obj.size >= _NP_SIZE_LARGE:
                import numpy as np
                state = np.random.RandomState(0)
                obj = state.choice(obj.flat, size=_NP_SAMPLE_SIZE)
            self.update(h, obj.tobytes())
            return h.digest()
        elif inspect.isbuiltin(obj):
            return bytes(obj.__name__.encode())
        elif any((type_util.is_type(obj, typename) for typename in _FFI_TYPE_NAMES)):
            return self.to_bytes(None)
        elif type_util.is_type(obj, 'builtins.mappingproxy') or type_util.is_type(obj, 'builtins.dict_items'):
            return self.to_bytes(dict(obj))
        elif type_util.is_type(obj, 'builtins.getset_descriptor'):
            return bytes(obj.__qualname__.encode())
        elif isinstance(obj, UploadedFile):
            h = hashlib.new('md5')
            self.update(h, obj.name)
            self.update(h, obj.tell())
            self.update(h, obj.getvalue())
            return h.digest()
        elif hasattr(obj, 'name') and (isinstance(obj, io.IOBase) or isinstance(obj, tempfile._TemporaryFileWrapper)):
            h = hashlib.new('md5')
            obj_name = getattr(obj, 'name', 'wonthappen')
            self.update(h, obj_name)
            self.update(h, os.path.getmtime(obj_name))
            self.update(h, obj.tell())
            return h.digest()
        elif isinstance(obj, Pattern):
            return self.to_bytes([obj.pattern, obj.flags])
        elif isinstance(obj, io.StringIO) or isinstance(obj, io.BytesIO):
            h = hashlib.new('md5')
            self.update(h, obj.tell())
            self.update(h, obj.getvalue())
            return h.digest()
        elif any((type_util.get_fqn(x) == 'sqlalchemy.pool.base.Pool' for x in type(obj).__bases__)):
            cargs = obj._creator.__closure__
            cargs = [cargs[0].cell_contents, cargs[1].cell_contents] if cargs else None
            if cargs:
                cargs[1] = dict(collections.OrderedDict(sorted(cargs[1].items(), key=lambda t: t[0])))
            reduce_data = obj.__reduce__()
            for attr in ['_overflow_lock', '_pool', '_conn', '_fairy', '_threadconns', 'logger']:
                reduce_data[2].pop(attr, None)
            return self.to_bytes([reduce_data, cargs])
        elif type_util.is_type(obj, 'sqlalchemy.engine.base.Engine'):
            reduce_data = obj.__reduce__()
            reduce_data[2].pop('url', None)
            reduce_data[2].pop('logger', None)
            return self.to_bytes(reduce_data)
        elif type_util.is_type(obj, 'numpy.ufunc'):
            return bytes(obj.__name__.encode())
        elif type_util.is_type(obj, 'socket.socket'):
            return self.to_bytes(id(obj))
        elif any((type_util.get_fqn(x) == 'torch.nn.modules.module.Module' for x in type(obj).__bases__)):
            return self.to_bytes(id(obj))
        elif type_util.is_type(obj, 'tensorflow.python.client.session.Session'):
            return self.to_bytes(id(obj))
        elif type_util.is_type(obj, 'torch.Tensor') or type_util.is_type(obj, 'torch._C._TensorBase'):
            return self.to_bytes([obj.detach().numpy(), obj.grad])
        elif any((type_util.is_type(obj, typename) for typename in _KERAS_TYPE_NAMES)):
            return self.to_bytes(id(obj))
        elif type_util.is_type(obj, 'tensorflow.python.saved_model.load.Loader._recreate_base_user_object.<locals>._UserObject'):
            return self.to_bytes(id(obj))
        elif inspect.isroutine(obj):
            wrapped = getattr(obj, '__wrapped__', None)
            if wrapped is not None:
                return self.to_bytes(wrapped)
            if obj.__module__.startswith('streamlit'):
                return self.to_bytes('%s.%s' % (obj.__module__, obj.__name__))
            h = hashlib.new('md5')
            code = getattr(obj, '__code__', None)
            assert code is not None
            if self._file_should_be_hashed(code.co_filename):
                context = _get_context(obj)
                defaults = getattr(obj, '__defaults__', None)
                if defaults is not None:
                    self.update(h, defaults, context)
                h.update(self._code_to_bytes(code, context, func=obj))
            else:
                self.update(h, obj.__module__)
                self.update(h, obj.__name__)
            return h.digest()
        elif inspect.iscode(obj):
            if context is None:
                raise RuntimeError('context must be defined when hashing code')
            return self._code_to_bytes(obj, context)
        elif inspect.ismodule(obj):
            return self.to_bytes(obj.__name__)
        elif inspect.isclass(obj):
            return self.to_bytes(obj.__name__)
        elif isinstance(obj, functools.partial):
            h = hashlib.new('md5')
            self.update(h, obj.args)
            self.update(h, obj.func)
            self.update(h, obj.keywords)
            return h.digest()
        else:
            h = hashlib.new('md5')
            try:
                reduce_data = obj.__reduce__()
            except BaseException as e:
                raise UnhashableTypeError(e, obj)
            for item in reduce_data:
                self.update(h, item, context)
            return h.digest()

    def _code_to_bytes(self, code, context: Context, func=None) -> bytes:
        h = hashlib.new('md5')
        self.update(h, code.co_code)
        consts = [n for n in code.co_consts if not isinstance(n, str) or not n.endswith('.<lambda>')]
        self.update(h, consts, context)
        context.cells.push(code, func=func)
        for ref in get_referenced_objects(code, context):
            self.update(h, ref, context)
        context.cells.pop()
        return h.digest()

    @staticmethod
    def _get_main_script_directory() -> str:
        """Get the absolute path to directory of the main script."""
        import pathlib
        import __main__
        abs_main_path = pathlib.Path(__main__.__file__).resolve()
        return str(abs_main_path.parent)

def get_referenced_objects(code, context: Context) -> List[Any]:
    tos: Any = None
    lineno = None
    refs: List[Any] = []

    def set_tos(t):
        nonlocal tos
        if tos is not None:
            refs.append(tos)
        tos = t
    for op in dis.get_instructions(code):
        try:
            if op.starts_line is not None:
                lineno = op.starts_line
            if op.opname in ['LOAD_GLOBAL', 'LOAD_NAME']:
                if op.argval in context.globals:
                    set_tos(context.globals[op.argval])
                else:
                    set_tos(op.argval)
            elif op.opname in ['LOAD_DEREF', 'LOAD_CLOSURE']:
                set_tos(context.cells.values[op.argval])
            elif op.opname == 'IMPORT_NAME':
                try:
                    set_tos(importlib.import_module(op.argval))
                except ImportError:
                    set_tos(op.argval)
            elif op.opname in ['LOAD_METHOD', 'LOAD_ATTR', 'IMPORT_FROM']:
                if tos is None:
                    refs.append(op.argval)
                elif isinstance(tos, str):
                    tos += '.' + op.argval
                else:
                    tos = getattr(tos, op.argval)
            elif op.opname == 'DELETE_FAST' and tos:
                del context.varnames[op.argval]
                tos = None
            elif op.opname == 'STORE_FAST' and tos:
                context.varnames[op.argval] = tos
                tos = None
            elif op.opname == 'LOAD_FAST' and op.argval in context.varnames:
                set_tos(context.varnames[op.argval])
            elif tos is not None:
                refs.append(tos)
                tos = None
        except Exception as e:
            raise UserHashError(e, code, lineno=lineno)
    return refs

class NoResult:
    """Placeholder class for return values when None is meaningful."""
    pass

class UnhashableTypeError(StreamlitAPIException):

    def __init__(self, orig_exc, failed_obj):
        msg = self._get_message(orig_exc, failed_obj)
        super(UnhashableTypeError, self).__init__(msg)
        self.with_traceback(orig_exc.__traceback__)

    def _get_message(self, orig_exc, failed_obj):
        args = _get_error_message_args(orig_exc, failed_obj)
        return ("\nCannot hash object of type `%(failed_obj_type_str)s`, found in %(object_part)s\n%(object_desc)s.\n\nWhile caching %(object_part)s %(object_desc)s, Streamlit encountered an\nobject of type `%(failed_obj_type_str)s`, which it does not know how to hash.\n\nTo address this, please try helping Streamlit understand how to hash that type\nby passing the `hash_funcs` argument into `@st.cache`. For example:\n\n```\n@st.cache(hash_funcs={%(failed_obj_type_str)s: my_hash_func})\ndef my_func(...):\n    ...\n```\n\nIf you don't know where the object of type `%(failed_obj_type_str)s` is coming\nfrom, try looking at the hash chain below for an object that you do recognize,\nthen pass that to `hash_funcs` instead:\n\n```\n%(hash_stack)s\n```\n\nPlease see the `hash_funcs` [documentation]\n(https://docs.streamlit.io/library/advanced-features/caching#the-hash_funcs-parameter)\nfor more details.\n            " % args).strip('\n')

class UserHashError(StreamlitAPIException):

    def __init__(self, orig_exc, cached_func_or_code, hash_func=None, lineno=None):
        self.alternate_name = type(orig_exc).__name__
        if hash_func:
            msg = self._get_message_from_func(orig_exc, cached_func_or_code, hash_func)
        else:
            msg = self._get_message_from_code(orig_exc, cached_func_or_code, lineno)
        super(UserHashError, self).__init__(msg)
        self.with_traceback(orig_exc.__traceback__)

    def _get_message_from_func(self, orig_exc, cached_func, hash_func):
        args = _get_error_message_args(orig_exc, cached_func)
        if hasattr(hash_func, '__name__'):
            args['hash_func_name'] = '`%s()`' % hash_func.__name__
        else:
            args['hash_func_name'] = 'a function'
        return ("\n%(orig_exception_desc)s\n\nThis error is likely due to a bug in %(hash_func_name)s, which is a\nuser-defined hash function that was passed into the `@st.cache` decorator of\n%(object_desc)s.\n\n%(hash_func_name)s failed when hashing an object of type\n`%(failed_obj_type_str)s`.  If you don't know where that object is coming from,\ntry looking at the hash chain below for an object that you do recognize, then\npass that to `hash_funcs` instead:\n\n```\n%(hash_stack)s\n```\n\nIf you think this is actually a Streamlit bug, please [file a bug report here.]\n(https://github.com/streamlit/streamlit/issues/new/choose)\n            " % args).strip('\n')

    def _get_message_from_code(self, orig_exc: BaseException, cached_code, lineno: int):
        args = _get_error_message_args(orig_exc, cached_code)
        failing_lines = _get_failing_lines(cached_code, lineno)
        failing_lines_str = ''.join(failing_lines)
        failing_lines_str = textwrap.dedent(failing_lines_str).strip('\n')
        args['failing_lines_str'] = failing_lines_str
        args['filename'] = cached_code.co_filename
        args['lineno'] = lineno
        return ('\n%(orig_exception_desc)s\n\nStreamlit encountered an error while caching %(object_part)s %(object_desc)s.\nThis is likely due to a bug in `%(filename)s` near line `%(lineno)s`:\n\n```\n%(failing_lines_str)s\n```\n\nPlease modify the code above to address this.\n\nIf you think this is actually a Streamlit bug, you may [file a bug report\nhere.] (https://github.com/streamlit/streamlit/issues/new/choose)\n        ' % args).strip('\n')

class InternalHashError(MarkdownFormattedException):
    """Exception in Streamlit hashing code (i.e. not a user error)"""

    def __init__(self, orig_exc: BaseException, failed_obj: Any):
        msg = self._get_message(orig_exc, failed_obj)
        super(InternalHashError, self).__init__(msg)
        self.with_traceback(orig_exc.__traceback__)

    def _get_message(self, orig_exc: BaseException, failed_obj: Any) -> str:
        args = _get_error_message_args(orig_exc, failed_obj)
        return ("\n%(orig_exception_desc)s\n\nWhile caching %(object_part)s %(object_desc)s, Streamlit encountered an\nobject of type `%(failed_obj_type_str)s`, which it does not know how to hash.\n\n**In this specific case, it's very likely you found a Streamlit bug so please\n[file a bug report here.]\n(https://github.com/streamlit/streamlit/issues/new/choose)**\n\nIn the meantime, you can try bypassing this error by registering a custom\nhash function via the `hash_funcs` keyword in @st.cache(). For example:\n\n```\n@st.cache(hash_funcs={%(failed_obj_type_str)s: my_hash_func})\ndef my_func(...):\n    ...\n```\n\nIf you don't know where the object of type `%(failed_obj_type_str)s` is coming\nfrom, try looking at the hash chain below for an object that you do recognize,\nthen pass that to `hash_funcs` instead:\n\n```\n%(hash_stack)s\n```\n\nPlease see the `hash_funcs` [documentation]\n(https://docs.streamlit.io/library/advanced-features/caching#the-hash_funcs-parameter)\nfor more details.\n            " % args).strip('\n')

def _get_error_message_args(orig_exc: BaseException, failed_obj: Any) -> Dict[str, Any]:
    hash_reason = hash_stacks.current.hash_reason
    hash_source = hash_stacks.current.hash_source
    failed_obj_type_str = type_util.get_fqn_type(failed_obj)
    if hash_source is None or hash_reason is None:
        object_desc = 'something'
        object_part = ''
        additional_explanation = ''
    elif hash_reason is HashReason.CACHING_BLOCK:
        object_desc = 'a code block'
        object_part = ''
        additional_explanation = ''
    else:
        if hasattr(hash_source, '__name__'):
            object_desc = '`%s()`' % hash_source.__name__
            object_desc_specific = object_desc
        else:
            object_desc = 'a function'
            object_desc_specific = 'that function'
        if hash_reason is HashReason.CACHING_FUNC_ARGS:
            object_part = 'the arguments of'
        elif hash_reason is HashReason.CACHING_FUNC_BODY:
            object_part = 'the body of'
        elif hash_reason is HashReason.CACHING_FUNC_OUTPUT:
            object_part = 'the return value of'
    return {'orig_exception_desc': str(orig_exc), 'failed_obj_type_str': failed_obj_type_str, 'hash_stack': hash_stacks.current.pretty_print(), 'object_desc': object_desc, 'object_part': object_part}

def _get_failing_lines(code, lineno: int) -> List[str]:
    """Get list of strings (lines of code) from lineno to lineno+3.

    Ideally we'd return the exact line where the error took place, but there
    are reasons why this is not possible without a lot of work, including
    playing with the AST. So for now we're returning 3 lines near where
    the error took place.
    """
    source_lines, source_lineno = inspect.getsourcelines(code)
    start = lineno - source_lineno
    end = min(start + 3, len(source_lines))
    lines = source_lines[start:end]
    return lines