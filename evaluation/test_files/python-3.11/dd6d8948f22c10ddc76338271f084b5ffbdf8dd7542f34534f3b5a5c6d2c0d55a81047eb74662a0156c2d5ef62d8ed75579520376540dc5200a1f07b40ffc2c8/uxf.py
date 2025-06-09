"""The API documentation is in the accompanying README.md file."""
import collections
import datetime
import enum
import functools
import gzip
import io
import os
import pathlib
import sys
import urllib.request
from xml.sax.saxutils import escape, unescape
import editabletuple
__version__ = '1.1.2'
VERSION = 1.0
UTF8 = 'utf-8'
_MAX_IDENTIFIER_LEN = 60
_SEP = ' '
_KEY_TYPES = frozenset({'int', 'date', 'datetime', 'str', 'bytes'})
_VALUE_TYPES = frozenset(_KEY_TYPES | {'bool', 'real'})
_ANY_VALUE_TYPES = frozenset(_VALUE_TYPES | {'list', 'map', 'table'})
_BOOL_FALSE = frozenset({'no'})
_BOOL_TRUE = frozenset({'yes'})
_CONSTANTS = frozenset(_BOOL_FALSE | _BOOL_TRUE)
_BAREWORDS = frozenset(_ANY_VALUE_TYPES | _CONSTANTS)
RESERVED_WORDS = frozenset(_ANY_VALUE_TYPES | {'null'} | _CONSTANTS)
_MISSING = object()

def on_error(lino, code, message, *, filename='-', fail=False, verbose=True):
    """The default on_error() error handler.
    Is called with the line number (lino), error code, error message,
    and filename. The filename may be '-' or empty if the UXF is created in
    memory rather than loaded from a file. If fail is True it means the
    error is unrecoverable, so the normal action would be to raise. If
    verbose is True the normal action is to print a textual version of the
    error data to stderr."""
    text = f'uxf.py:{filename}:{lino}:#{code}:{message}'
    if fail:
        raise Error(text)
    if verbose:
        print(text, file=sys.stderr)

def _validate_format(name, value):
    if name == 'indent':
        return value if value == '' or (value.isspace() and len(value) < 33) else '  '
    if name == 'wrap_width':
        return value if value is None or value == 0 or 40 <= value <= 240 else 96
    if name == 'realdp':
        return value if value is None or 0 <= value <= 15 else None
    if name == 'max_short_len':
        return value if 24 <= value <= 60 else 32
Format = editabletuple.editableobject('Format', 'indent', 'wrap_width', 'realdp', 'max_short_len', defaults=('  ', 96, None, 10, 32), validator=_validate_format, doc='Specifies various aspects of how a UXF file is dumped to file or\nto a string.\n`indent` defaults to 2 spaces and may be an empty string or up to 32 spaces\n`wrap_width` defaults to 96 characters and may be None (use the default) or 40<=240\n`realdp` defaults to None which means use however many digits after the\ndecimal place are needed to represent the given `real` (i.e., Python\n`float`); if not None specify an int 0<=15\n`max_short_len` defaults to 32 and must be 24<=60')

class Uxf:

    def __init__(self, value=None, *, custom='', tclasses=None, comment=None):
        """value may be a list, List, tuple, dict, Map, or Table and will
        default to a List if not specified; if given tclasses must be a dict
        whose values are TClasses and whose corresponding keys are the
        TClasses' ttypes (i.e., their names); if given the comment is a
        file-level comment that follows the uxf header and precedes any
        TClasses and the value"""
        self.value = value
        self.custom = custom
        self.comment = comment
        self._tclasses = {}
        self.tclasses = tclasses if tclasses is not None else {}
        self.imports = {}
        self.on_error = functools.partial(on_error, filename='')

    def add_tclasses(self, tclass, *tclasses):
        for tclass in (tclass,) + tclasses:
            if not tclass.ttype:
                raise Error('#200:cannot add an unnamed TClass')
            _add_to_tclasses(self.tclasses, tclass, lino=0, code=690, on_error=self.on_error)

    @property
    def tclasses(self):
        return self._tclasses

    @tclasses.setter
    def tclasses(self, tclasses):
        for ttype, tclass in tclasses.items():
            if not ttype:
                raise Error('#694:cannot set an unnamed TClass')
            self._tclasses[ttype] = tclass

    @property
    def import_filenames(self):
        """A utility useful for some UXF processors. This yields all the
        unique import filenames."""
        seen = set()
        for filename in self.imports.values():
            if filename not in seen:
                yield filename
                seen.add(filename)

    @property
    def value(self):
        """The List, Map, or Table that holds all the Uxf's data."""
        return self._value

    @value.setter
    def value(self, value):
        """Replaces all the Uxf's data with the given collection."""
        if value is None:
            value = List()
        elif isinstance(value, list):
            value = List(value)
        elif isinstance(value, dict):
            value = Map(value)
        elif isinstance(value, (set, frozenset, tuple, collections.deque)):
            value = List()
        if not _is_uxf_collection(value):
            raise Error(f'#100:Uxf value must be a list, List, dict, Map, or Table, got {value.__class__.__name__}')
        self._value = value

    def dump(self, filename_or_filelike, *, on_error=on_error, format=Format()):
        """Convenience method that wraps the module-level dump() function"""
        dump(filename_or_filelike, self, on_error=on_error, format=format)

    def dumps(self, *, on_error=on_error, format=Format()):
        """Convenience method that wraps the module-level dumps()
        function"""
        return dumps(self, on_error=on_error, format=format)

    def load(self, filename_or_filelike, *, on_error=on_error, drop_unused=False, replace_imports=False):
        """Convenience method that wraps the module-level load()
        function"""
        filename = filename_or_filelike if isinstance(filename_or_filelike, (str, pathlib.Path)) else '-'
        value, custom, tclasses, imports, comment = _loads(_read_text(filename_or_filelike), filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports)
        self.value = value
        self.custom = custom
        self.tclasses = tclasses
        self.comment = comment

    def loads(self, uxt, filename='-', *, on_error=on_error, drop_unused=False, replace_imports=False):
        """Convenience method that wraps the module-level loads()
        function"""
        value, custom, tclasses, imports, comment = _loads(uxt, filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports)
        self.value = value
        self.custom = custom
        self.tclasses = tclasses
        self.comment = comment

def load(filename_or_filelike, *, on_error=on_error, drop_unused=False, replace_imports=False, _imported=None, _is_import=False):
    """
    Returns a Uxf object.

    filename_or_filelike is sys.stdin or a filename or an open readable file
    (text mode UTF-8 encoded, optionally gzipped).
    """
    filename = filename_or_filelike if isinstance(filename_or_filelike, (str, pathlib.Path)) else '-'
    value, custom, tclasses, imports, comment = _loads(_read_text(filename_or_filelike), filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports, _imported=_imported, _is_import=_is_import)
    uxo = Uxf(value, custom=custom, tclasses=tclasses, comment=comment)
    uxo.imports = imports
    return uxo

def loads(uxt, filename='-', *, on_error=on_error, drop_unused=False, replace_imports=False, _imported=None, _is_import=False):
    """
    Returns a Uxf object.

    uxt must be a string of UXF data.
    """
    value, custom, tclasses, imports, comment = _loads(uxt, filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports, _imported=_imported, _is_import=_is_import)
    uxo = Uxf(value, custom=custom, tclasses=tclasses, comment=comment)
    uxo.imports = imports
    return uxo

def _loads(uxt, filename='-', *, on_error=on_error, drop_unused=False, replace_imports=False, _imported=None, _is_import=False):
    tokens, custom, text = _tokenize(uxt, filename, on_error=on_error)
    value, comment, tclasses, imports = _parse(tokens, filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports, _imported=_imported, _is_import=_is_import)
    return (value, custom, tclasses, imports, comment)

def _tokenize(uxt, filename='-', *, on_error=on_error):
    lexer = _Lexer(filename, on_error=on_error)
    tokens = lexer.tokenize(uxt)
    return (tokens, lexer.custom, uxt)

def _read_text(filename_or_filelike):
    if not isinstance(filename_or_filelike, (str, pathlib.Path)):
        return filename_or_filelike.read()
    try:
        try:
            with gzip.open(filename_or_filelike, 'rt', encoding=UTF8) as file:
                return file.read()
        except gzip.BadGzipFile:
            with open(filename_or_filelike, 'rt', encoding=UTF8) as file:
                return file.read()
    except OSError as err:
        raise Error(f'#102:failed to read UXF text: {err}')

class _Lexer:

    def __init__(self, filename, *, on_error=on_error):
        self.filename = filename
        self.on_error = functools.partial(on_error, filename=os.path.basename(filename))
        self.clear()

    def error(self, code, message, *, fail=False):
        self.on_error(self.lino, code, message, fail=fail)

    def clear(self):
        self.pos = 0
        self.lino = 0
        self.custom = None
        self.in_tclass = False
        self.tokens = []

    def tokenize(self, uxt):
        self.text = uxt
        self.scan_header()
        self.maybe_read_comment()
        while not self.at_end():
            self.scan_next()
        self.add_token(_Kind.EOF)
        return self.tokens

    def scan_header(self):
        i = self.text.find('\n')
        if i == -1:
            self.error(110, 'missing UXF file header or empty file', fail=True)
            return
        self.pos = i
        parts = self.text[:i].split(None, 2)
        if len(parts) < 2:
            self.error(120, 'invalid UXF file header', fail=True)
            return
        if parts[0] != 'uxf':
            self.error(130, 'not a UXF file', fail=True)
            return
        try:
            version = float(parts[1])
            if version > VERSION:
                self.error(141, f'version ({version}) > current ({VERSION})')
        except ValueError:
            self.error(151, 'failed to read UXF file version number')
        if len(parts) > 2:
            self.custom = parts[2]

    def maybe_read_comment(self):
        self.skip_ws()
        if not self.at_end() and self.text[self.pos] == '#':
            self.pos += 1
            if self.peek() == '<':
                self.pos += 1
                value = self.match_to('>', what='comment string')
                self.add_token(_Kind.COMMENT, unescape(value))
            else:
                self.error(160, f"invalid comment syntax: expected '<', got {self.peek()}")

    def at_end(self):
        return self.pos >= len(self.text)

    def scan_next(self):
        c = self.getch()
        if c.isspace():
            if c == '\n':
                self.lino += 1
        elif c == '(':
            if self.peek() == ':':
                self.pos += 1
                self.read_bytes()
            else:
                self.check_in_tclass()
                self.add_token(_Kind.TABLE_BEGIN)
        elif c == ')':
            self.add_token(_Kind.TABLE_END)
        elif c == '[':
            self.check_in_tclass()
            self.add_token(_Kind.LIST_BEGIN)
        elif c == '=':
            self.check_in_tclass()
            self.add_token(_Kind.TCLASS_BEGIN)
            self.in_tclass = True
        elif c == ']':
            self.add_token(_Kind.LIST_END)
        elif c == '{':
            self.check_in_tclass()
            self.add_token(_Kind.MAP_BEGIN)
        elif c == '}':
            self.in_tclass = False
            self.add_token(_Kind.MAP_END)
        elif c == '?':
            self.add_token(_Kind.NULL)
        elif c == '!':
            self.read_imports()
        elif c == '#':
            self.read_comment()
        elif c == '<':
            self.read_string()
        elif c == ':':
            self.read_field_vtype()
        elif c == '-' and isasciidigit(self.peek()):
            c = self.getch()
            self.read_negative_number(c)
        elif isasciidigit(c):
            self.read_positive_number_or_date(c)
        elif c.isalpha():
            self.read_name()
        else:
            self.error(170, f'invalid character encountered: {c!r}')

    def check_in_tclass(self):
        if self.in_tclass:
            self.in_tclass = False
            self.add_token(_Kind.TCLASS_END)

    def read_imports(self):
        this_file = _full_filename(self.filename)
        path = os.path.dirname(this_file)
        while True:
            value = self.match_to('\n', what='import')
            value = value.strip()
            if this_file == _full_filename(value, path):
                self.error(176, 'a UXF file cannot import itself', fail=True)
                return
            else:
                self.add_token(_Kind.IMPORT, value)
            if self.peek() == '!':
                self.getch()
            else:
                break

    def read_comment(self):
        if self.tokens and self.tokens[-1].kind in {_Kind.LIST_BEGIN, _Kind.MAP_BEGIN, _Kind.TABLE_BEGIN, _Kind.TCLASS_BEGIN}:
            if self.peek() != '<':
                self.error(180, f'a str must follow the # comment introducer, got {self.peek()!r}')
            self.pos += 1
            value = self.match_to('>', what='comment string')
            if value:
                self.add_token(_Kind.COMMENT, unescape(value))
        else:
            self.error(190, 'comments may only occur at the start of Lists, Maps, Tables, and TClasses')

    def read_string(self):
        value = self.match_to('>', what='string')
        self.add_token(_Kind.STR, unescape(value))

    def read_bytes(self):
        value = self.match_to(':)', what='bytes')
        try:
            self.add_token(_Kind.BYTES, bytes.fromhex(value))
        except ValueError as err:
            self.error(200, f'expected bytes, got {value!r}: {err}')

    def read_negative_number(self, c):
        is_real = False
        start = self.pos - 1
        while not self.at_end() and (c in '.eE' or isasciidigit(c)):
            if c in '.eE':
                is_real = True
            c = self.text[self.pos]
            self.pos += 1
        convert = float if is_real else int
        self.pos -= 1
        text = self.text[start:self.pos]
        try:
            value = convert(text)
            self.add_token(_Kind.REAL if is_real else _Kind.INT, -value)
        except ValueError as err:
            self.error(210, f'invalid number: {text!r}: {err}')

    def read_positive_number_or_date(self, c):
        start = self.pos - 1
        is_real, is_datetime, hyphens = self.read_number_or_date_chars(c)
        text = self.text[start:self.pos]
        convert, token = self.get_converter_and_token(is_real, is_datetime, hyphens, text)
        try:
            value = convert(text)
            self.add_token(token, value)
        except ValueError as err:
            if is_datetime and len(text) > 19:
                self.reread_datetime(text, convert)
            else:
                self.error(220, f'invalid number or date/time: {text!r}: {err}')

    def read_number_or_date_chars(self, c):
        is_real = is_datetime = False
        hyphens = 0
        while not self.at_end() and (c in '-+.:eET' or isasciidigit(c)):
            if c in '.eE':
                is_real = True
            elif c == '-':
                hyphens += 1
            elif c in ':T':
                is_datetime = True
            c = self.text[self.pos]
            self.pos += 1
        self.pos -= 1
        return (is_real, is_datetime, hyphens)

    def get_converter_and_token(self, is_real, is_datetime, hyphens, text):
        if is_datetime:
            return (datetime.datetime.fromisoformat, _Kind.DATE_TIME)
        if hyphens == 2:
            return (datetime.date.fromisoformat, _Kind.DATE)
        if is_real:
            return (float, _Kind.REAL)
        return (int, _Kind.INT)

    def reread_datetime(self, text, convert):
        try:
            value = convert(text[:19])
            self.add_token(_Kind.DATE_TIME, value)
            self.error(231, f'skipped timezone data, used {text[:19]!r}, got {text!r}')
        except ValueError as err:
            self.error(240, f'invalid datetime: {text!r}: {err}')

    def read_name(self):
        match = self.match_any_of(_BAREWORDS)
        if match in _BOOL_FALSE:
            self.add_token(_Kind.BOOL, False)
            return
        if match in _BOOL_TRUE:
            self.add_token(_Kind.BOOL, True)
            return
        if match in _ANY_VALUE_TYPES:
            self.add_token(_Kind.TYPE, match)
            return
        start = self.pos - 1
        if self.text[start] == '_' or self.text[start].isalpha():
            identifier = self.match_identifier(start, 'identifier')
            self.add_token(_Kind.IDENTIFIER, identifier)
        else:
            i = self.text.find('\n', self.pos)
            text = self.text[self.pos - 1:i if i > -1 else self.pos + 8]
            self.error(250, f'expected const or identifier, got {text!r}')

    def read_field_vtype(self):
        self.skip_ws()
        identifier = self.match_identifier(self.pos, 'field vtype')
        self.add_token(_Kind.TYPE, identifier)

    def peek(self):
        return '\x00' if self.at_end() else self.text[self.pos]

    def skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            if self.text[self.pos] == '\n':
                self.lino += 1
            self.pos += 1

    def getch(self):
        c = self.text[self.pos]
        self.pos += 1
        return c

    def match_identifier(self, start, what):
        while self.pos < len(self.text):
            if not self.text[self.pos].isalnum() and self.text[self.pos] != '_':
                break
            self.pos += 1
        identifier = self.text[start:self.pos][:_MAX_IDENTIFIER_LEN]
        if identifier:
            return identifier
        text = self.text[start:start + 10]
        self.error(260, f'expected {what}, got {text}…')

    def match_to(self, target, *, what):
        if not self.at_end():
            i = self.text.find(target, self.pos)
            if i > -1:
                text = self.text[self.pos:i]
                self.lino += text.count('\n')
                self.pos = i + len(target)
                return text
        self.error(270, f'unterminated {what}')

    def match_any_of(self, targets):
        if self.at_end():
            return None
        start = self.pos - 1
        for target in sorted(targets, key=lambda t: (len(t), t), reverse=True):
            if self.text.startswith(target, start):
                self.pos += len(target) - 1
                return target

    def add_token(self, kind, value=None):
        self.tokens.append(_Token(kind, value, lino=self.lino))

class Error(Exception):
    pass

class _Token:

    def __init__(self, kind, value=None, lino=0):
        self.kind = kind
        self.value = value
        self.lino = lino

    def __str__(self):
        parts = [self.kind.name]
        if self.value is not None:
            parts.append(f'={self.value!r}')
        return f"{self.lino}:{''.join(parts)}"

    def __repr__(self):
        parts = [f'{self.__class__.__name__}({self.kind.name}']
        if self.value is not None:
            parts.append(f', {self.value!r}')
        parts.append(')')
        return ''.join(parts)

@enum.unique
class _Kind(enum.Enum):
    IMPORT = enum.auto()
    TCLASS_BEGIN = enum.auto()
    TCLASS_END = enum.auto()
    TABLE_BEGIN = enum.auto()
    TABLE_END = enum.auto()
    LIST_BEGIN = enum.auto()
    LIST_END = enum.auto()
    MAP_BEGIN = enum.auto()
    MAP_END = enum.auto()
    COMMENT = enum.auto()
    NULL = enum.auto()
    BOOL = enum.auto()
    INT = enum.auto()
    REAL = enum.auto()
    DATE = enum.auto()
    DATE_TIME = enum.auto()
    STR = enum.auto()
    BYTES = enum.auto()
    TYPE = enum.auto()
    IDENTIFIER = enum.auto()
    EOF = enum.auto()

    @property
    def is_scalar(self):
        return self in {_Kind.NULL, _Kind.BOOL, _Kind.INT, _Kind.REAL, _Kind.DATE, _Kind.DATE_TIME, _Kind.STR, _Kind.BYTES}

class List(collections.UserList):

    def __init__(self, seq=None, *, vtype=None, comment=None):
        """Takes an optional sequence (list, tuple, iterable)
        .data holds the actual list
        .comment holds an optional comment
        .vtype holds a UXF type name ('int', 'real', …)"""
        super().__init__(seq)
        self.vtype = vtype
        self.comment = comment

class Map(collections.UserDict):

    def __init__(self, d=None, *, ktype=None, vtype=None, comment=None):
        """Takes an optional dict
        .data holds the actual dict
        .comment holds an optional comment
        .ktype and .vtype hold a UXF type name ('int', 'str', …);
        .ktype may only be bytes, date, datetime, int, or str"""
        super().__init__(d)
        self.ktype = ktype
        self.vtype = vtype
        self.comment = comment
        self._pending_key = _MISSING

    @property
    def ktype(self):
        return self._ktype

    @ktype.setter
    def ktype(self, ktype):
        if ktype is not None and ktype not in _KEY_TYPES:
            raise Error(f'#280: ktype may only be bytes, date, datetime, int, or str, got {ktype}')
        self._ktype = ktype

    def _append(self, value):
        """This is for UXF readers; instead use: map[key] = value

        If there's no pending key, sets the value as the pending key;
        otherwise adds a new item with the pending key and this value and
        clears the pending key."""
        if self._pending_key is _MISSING:
            if not _is_key_type(value):
                prefix = 'map keys may only be of type int, date, datetime, str, or bytes, got '
                if isinstance(value, Table):
                    raise Error(f'#290:{prefix}a Table ( … ), maybe bytes (: … :) was intended?')
                else:
                    raise Error(f'#294:{prefix}{value.__class__.__name__} {value!r}')
            self._pending_key = value
        else:
            self.data[self._pending_key] = value
            self._pending_key = _MISSING

    @property
    def _next_is_key(self):
        return self._pending_key is _MISSING

def _check_name(name):
    if not name:
        raise Error('#298:fields and tables must have nonempty names')
    if isasciidigit(name[0]):
        raise Error(f'#300:names must start with a letter or underscore, got {name}')
    if name in RESERVED_WORDS:
        raise Error('#304:names cannot be the same as built-in type names or constants, got {name}')
    for c in name:
        if not (c == '_' or c.isalnum()):
            raise Error(f'#310:names may only contain letters, digits, or underscores, got {name}')

class TClass:

    def __init__(self, ttype, fields=None, *, comment=None):
        """The type of a Table
        .ttype holds the tclass's name (equivalent to a vtype or ktype
        name); it may not be the same as a built-in type name or constant
        .fields holds a sequence of field names or of fields of type Field
        .comment holds an optional comment

        This is best to use when you want to pass a sequence of fields:

            fields = [uxf.Field('x', 'int'), uxf.Field('y', 'int')]
            point_tclass = TClass('point', fields)

        Or no fields at all:

            fieldless_class = TClass('SomeEnumValue')
        """
        self.ttype = ttype
        self.fields = []
        self.comment = comment
        self._RecordClass = None
        if fields is not None:
            for field in fields:
                if isinstance(field, str):
                    self.fields.append(Field(field))
                else:
                    self.fields.append(field)

    @property
    def RecordClass(self):
        if self._RecordClass is None:
            self._make_RecordClass()
        return self._RecordClass

    def _make_RecordClass(self):
        if not self.ttype:
            raise Error("#340:can't use an unnamed table tclass")
        if not self.fields:
            raise Error("#350:can't create a table's tclass with no fields")
        self._RecordClass = editabletuple.editabletuple(f'UXF_{self.ttype}', *[field.name for field in self.fields])

    @property
    def ttype(self):
        return self._ttype

    @ttype.setter
    def ttype(self, ttype):
        if ttype is not None:
            _check_name(ttype)
        self._ttype = ttype

    @property
    def isfieldless(self):
        return not bool(self.fields)

    def append(self, name_or_field, vtype=None):
        if isinstance(name_or_field, Field):
            self.fields.append(name_or_field)
        else:
            self.fields.append(Field(name_or_field, vtype))

    def set_vtype(self, index, vtype):
        self.fields[index].vtype = vtype

    def __hash__(self):
        return hash(self.ttype)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        uttype = self.ttype.upper()
        uother = other.ttype.upper()
        if uttype != uother:
            return False
        if len(self.fields) != len(other.fields):
            return False
        for f1, f2 in zip(self.fields, other.fields):
            if f1 != f2:
                return False
        return True

    def __lt__(self, other):
        uttype = self.ttype.upper()
        uother = other.ttype.upper()
        if uttype != uother:
            return uttype < uother
        return self.ttype < other.ttype

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        if self.fields:
            fields = ', '.join((repr(field) for field in self.fields))
            fields = f' {fields}, '
        else:
            fields = ''
        return f'{self.__class__.__name__}({self.ttype!r},{fields}comment={self.comment!r})'

class Field:

    def __init__(self, name, vtype=None):
        """The type of one field in a Table
        .name holds the field's name (equivalent to a vtype or ktype name);
        may not be the same as a built-in type name or constant
        .vtype holds a UXF type name ('int', 'real', …)"""
        self.name = name
        self.vtype = vtype

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        _check_name(name)
        self._name = name

    def __eq__(self, other):
        return self.name == other.name and self.vtype == other.vtype

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {self.vtype!r})'

def table(ttype, fields, *, comment=None):
    """Convenience function for creating empty tables with a new tclass.
    See also the Table constructor."""
    return Table(TClass(ttype, fields), comment=comment)

class Table:
    """Used to store a UXF table.

    A Table has an optional list of fields (name, optional type) and (if it
    has fields), a records list which is a list of lists of values, with
    each sublist having the same number of items as the number of fields. It
    also has a .comment attribute. (Note that the lists in a Table are plain
    lists not UXF Lists.)

    Table's API is very similar to the list API, only it works in terms of
    whole records rather than individual field values. However, field values
    can be directly accessed using the field name or index.

    When a Table is iterated each record (row) is returned as a custom class
    instance, and in the process each record is converted from a list to a
    custom class instance if it isn't one already. The custom class allows
    fields to be accessed by name and by index.

    Some tables are fieldless, for example to represent enumerations.
    """

    def __init__(self, tclass=None, *, records=None, comment=None):
        """
        A Table may be created empty, e.g., Table(). However, if records is
        not None, then the tclass (of type TClass) must be given.

        .records can be a flat list of values (which will be put into a list
        of lists with each sublist being len(fields) long), or a list of
        lists in which case each list is _assumed_ to be len(fields) i.e.,
        len(tclass.fields), long

        comment is an optional str.

        .RecordClass is a read-only property holding a dynamically created
        custom class that is used when accessing a single record via [] or
        when iterating a table's records.

        See also the table() convenience function.
        """
        self._RecordClass = None
        self.tclass = tclass
        self.records = []
        self.comment = comment
        if records:
            if tclass is None:
                raise Error("#320:can't create a nonempty table without fields")
            elif not tclass.ttype:
                raise Error("#330:can't create an unnamed nonempty table")
            if isinstance(records, (list, List)):
                self.records = list(records)
            else:
                for value in records:
                    self._append(value)

    @property
    def RecordClass(self):
        if self.tclass is None:
            raise Error('#332:table has no tclass')
        return self.tclass.RecordClass

    @property
    def ttype(self):
        return self.tclass.ttype if self.tclass is not None else None

    @property
    def fields(self):
        return self.tclass.fields if self.tclass is not None else []

    def field(self, column):
        return self.tclass.fields[column]

    @property
    def _next_vtype(self):
        if self.tclass is not None:
            if self.tclass.isfieldless:
                return None
            if not self.records:
                return self.tclass.fields[0].vtype
            else:
                if len(self.records[-1]) == len(self.tclass):
                    return self.tclass.fields[0].vtype
                return self.tclass.fields[len(self.records[-1])].vtype

    def _append(self, value):
        """This is for UXF readers; instead use: table.append(record)

        Use to append a value to the table. The value will be added to
        the last record (row) if that isn't full, or as the first value in a
        new record (row)"""
        if not self.fields:
            raise Error("#334:can't append to a fieldless table")
        if not self.records or len(self.records[-1]) >= len(self.tclass):
            self.records.append([])
        self.records[-1].append(value)

    @property
    def is_scalar(self):
        for field in self.fields:
            if field.vtype is None:
                break
            if field.vtype not in _VALUE_TYPES:
                return False
        else:
            return True
        for record in self.records:
            for x in record:
                if not is_scalar(x):
                    return False
        return True

    def _classify(self, row):
        record = self.records[row]
        if not isinstance(record, self.RecordClass):
            record = self.records[row] = self.RecordClass(*record)
        return record

    def append(self, record):
        """Appends a record (either a RecordClass tuple or a sequence of
        field values) to the table"""
        if not isinstance(record, self.RecordClass):
            record = self.RecordClass(*record)
        self.records.append(record)

    def insert(self, index, record):
        """Inserts a record (either a RecordClass tuple or a sequence of
        field values) into the table at the given index position"""
        if not isinstance(record, self.RecordClass):
            record = self.RecordClass(*record)
        self.records.insert(index, record)

    @property
    def first(self):
        if self.records:
            return self[0]

    @property
    def second(self):
        if self.records:
            return self[1]

    @property
    def third(self):
        if self.records:
            return self[2]

    @property
    def fourth(self):
        if self.records:
            return self[3]

    @property
    def last(self):
        if self.records:
            return self[-1]

    def __getitem__(self, row):
        """Return the row-th record as a custom class.

        The returned record is an object reference to an editabletuple so
        any changes made to its fields will be reflected in the table."""
        return self._classify(row)

    def __setitem__(self, row, record):
        """Replace the row-th record as a custom class"""
        if not isinstance(record, self.RecordClass):
            record = self.RecordClass(*record)
        self.records[row] = record

    def __delitem__(self, row):
        """Deletes the table's row-th record"""
        del self.records[row]

    def __iter__(self):
        if not self.records:
            return
        for i in range(len(self.records)):
            record = self.records[i]
            if not isinstance(record, self.RecordClass):
                record = self.records[i] = self.RecordClass(*record)
            yield record

    def __len__(self):
        return len(self.records)

    def __str__(self):
        parts = []
        if self.tclass is not None:
            parts.append(f'ttype={self.ttype!r}')
            if self.fields:
                parts.append(f'fields={self.fields!r}')
        else:
            parts.append('(no fields)')
        if self.comment:
            parts.append(f'comment={self.comment!r}')
        parts.append(f'({len(self.records)} records)')
        return ' '.join(parts)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.tclass!r}, records={self.records!r}, comment={self.comment!r})'

def _parse(tokens, filename='-', *, on_error=on_error, drop_unused=False, replace_imports=False, _imported=None, _is_import=False):
    parser = _Parser(filename, on_error=on_error, drop_unused=drop_unused, replace_imports=replace_imports, _imported=_imported, _is_import=_is_import)
    data, comment = parser.parse(tokens)
    return (data, comment, parser.tclasses, parser.imports)

class _Parser:

    def __init__(self, filename, *, on_error=on_error, drop_unused=False, replace_imports=False, _imported=None, _is_import=False):
        self.filename = filename
        self.on_error = functools.partial(on_error, filename=os.path.basename(filename))
        self.drop_unused = drop_unused
        self.replace_imports = replace_imports
        self._is_import = _is_import
        self.clear()
        if _imported is not None:
            self.imported = _imported
        if filename and filename != '-':
            filename = _full_filename(filename)
            if filename in self.imported:
                self.error(400, f'already imported {filename}', fail=True)
                return
            self.imported.add(filename)

    def error(self, code, message, *, fail=False):
        self.on_error(self.lino, code, message, fail=fail)

    def clear(self):
        self.stack = []
        self.imports = {}
        self.imported = set()
        self.tclasses = {}
        self.lino_for_tclass = {}
        self.used_tclasses = set()
        self.pos = -1
        self.lino = 0

    def parse(self, tokens):
        if not tokens:
            return
        self.tokens = tokens
        data = None
        comment = self._parse_file_comment()
        self._parse_imports()
        self._parse_tclasses()
        for i, token in enumerate(self.tokens):
            self.lino = token.lino
            kind = token.kind
            collection_start = self._is_collection_start(kind)
            if data is None and (not collection_start):
                self.error(402, f'expected a map, list, or table, got {token}')
            if collection_start:
                self._on_collection_start(token)
                if data is None:
                    data = self.stack[0]
            elif self._is_collection_end(kind):
                self._on_collection_end(token)
            elif kind is _Kind.COMMENT:
                self._handle_comment(i, token)
            elif kind is _Kind.IDENTIFIER:
                self._handle_identifier(i, token)
            elif kind is _Kind.TYPE:
                self._handle_type(i, token)
            elif kind is _Kind.STR:
                self._handle_str(i, token)
            elif kind.is_scalar:
                self._handle_scalar(i, token)
            elif kind is _Kind.EOF:
                break
            else:
                self.error(410, f'unexpected token, got {token}')
        if not self._is_import:
            self._check_tclasses()
        return (data, comment)

    def _check_tclasses(self):
        imported = set(self.imports.keys())
        if self.replace_imports:
            self._replace_imports(imported)
        defined = set(self.tclasses.keys())
        if self.drop_unused:
            self._drop_unused(defined)
        unused = defined - self.used_tclasses
        unused -= imported
        unused = {ttype for ttype in unused if not self.tclasses[ttype].isfieldless}
        if unused:
            self._report_problem(unused, 422, 'unused ttype')
        undefined = self.used_tclasses - defined
        if undefined:
            self._report_problem(undefined, 424, 'undefined ttype')

    def _replace_imports(self, imported):
        for ttype in imported:
            if ttype not in self.used_tclasses:
                del self.tclasses[ttype]
        self.imports.clear()
        imported.clear()

    def _drop_unused(self, defined):
        ttypes_for_filename = collections.defaultdict(set)
        for ttype, filename in self.imports.items():
            ttypes_for_filename[filename].add(ttype)
        for ttype in list(self.tclasses):
            if ttype not in self.used_tclasses:
                del self.tclasses[ttype]
                defined.discard(ttype)
                for filename in list(ttypes_for_filename):
                    ttypes_for_filename[filename].discard(ttype)
        for filename, ttypes in ttypes_for_filename.items():
            if not ttypes:
                for ttype, ifilename in list(self.imports.items()):
                    if filename == ifilename:
                        del self.imports[ttype]

    def _report_problem(self, diff, code, what):
        diff = sorted(diff)
        if len(diff) == 1:
            self.error(code, f'{what}: {diff[0]!r}')
        else:
            diff = ', '.join((repr(t) for t in diff))
            self.error(code, f'{what}s: {diff}')

    def _handle_comment(self, i, token):
        parent = self.stack[-1]
        prev_token = self.tokens[i - 1]
        if not self._is_collection_start(prev_token.kind):
            self.error(440, f'comments may only be put at the beginning of a map, list, or table, not after {prev_token}')
        parent.comment = token.value

    def _handle_identifier(self, i, token):
        if not self.stack:
            self.error(441, 'invalid UXF data')
            return
        parent = self.stack[-1]
        if self.tokens[i - 1].kind is _Kind.TYPE and (self.tokens[i - 2].kind is _Kind.MAP_BEGIN or (self.tokens[i - 2].kind is _Kind.COMMENT and self.tokens[i - 3].kind is _Kind.MAP_BEGIN)):
            self._handle_type_identifier(parent, token)
        elif self.tokens[i - 1].kind is _Kind.LIST_BEGIN or (self.tokens[i - 1].kind is _Kind.COMMENT and self.tokens[i - 2].kind is _Kind.LIST_BEGIN):
            self._handle_vtype_identifier(parent, token)
        elif self.tokens[i - 1].kind is _Kind.TABLE_BEGIN or (self.tokens[i - 1].kind is _Kind.COMMENT and self.tokens[i - 2].kind is _Kind.TABLE_BEGIN):
            self._handle_ttype_identifier(parent, token)
        else:
            self._handle_incorrect_identifier(token)

    def _handle_type_identifier(self, parent, token):
        tclass = self.tclasses.get(token.value)
        if tclass is None:
            self.error(442, f'expected map vtype, got {token}')
        elif tclass.ttype is None:
            self.error(444, f'tclass without a ttype, got {token}')
        else:
            parent.vtype = tclass.ttype
            self.used_tclasses.add(tclass.ttype)

    def _handle_vtype_identifier(self, parent, token):
        tclass = self.tclasses.get(token.value)
        if tclass is None:
            self.error(446, f'expected list vtype, got {token}')
        else:
            parent.vtype = tclass.ttype
            self.used_tclasses.add(tclass.ttype)

    def _handle_ttype_identifier(self, parent, token):
        tclass = self.tclasses.get(token.value)
        if tclass is None:
            self.error(450, f'expected table ttype, got {token}', fail=True)
        else:
            parent.tclass = tclass
            self.used_tclasses.add(tclass.ttype)
            if len(self.stack) > 1:
                grand_parent = self.stack[-2]
                vtype = getattr(grand_parent, 'vtype', None)
                if vtype is not None and vtype != 'table' and (vtype != tclass.ttype):
                    self.error(456, f'expected table value of type {vtype}, got value of type {tclass.ttype}')

    def _handle_incorrect_identifier(self, token):
        if token.value.upper() in {'TRUE', 'FALSE'}:
            self.error(458, 'boolean values are represented by yes or no')
        else:
            self.error(460, f'ttypes may only appear at the start of a map (as the value type), list, or table, {token}')

    def _handle_type(self, i, token):
        if not self.stack:
            self.error(469, 'invalid UXF data')
            return
        parent = self.stack[-1]
        if isinstance(parent, List):
            if parent.vtype is not None:
                self.error(470, f'can only have at most one vtype for a list, got {token}')
            parent.vtype = token.value
        elif isinstance(parent, Map):
            if parent.ktype is None:
                parent.ktype = token.value
            elif parent.vtype is None:
                parent.vtype = token.value
            else:
                self.error(480, f'can only have at most one ktype and one vtype for a map, got {token}')
        else:
            self.error(484, f'ktypes and vtypes are only allowed at the start of maps and lists, got {token}')

    def _handle_str(self, i, token):
        value = token.value
        vtype, message = self.typecheck(value)
        if value is not None and vtype is not None and (vtype in {'bool', 'int', 'real', 'date', 'datetime'}):
            new_value = naturalize(value)
            if new_value != value:
                self.error(486, f'converted str {value!r} to {vtype} {value}')
                value = new_value
            else:
                self.error(488, message)
        if not self.stack:
            self.error(489, 'invalid UXF data')
            return
        append_to_parent(self.stack[-1], value)

    def _handle_scalar(self, i, token):
        value = token.value
        vtype, message = self.typecheck(value)
        if value is not None and vtype is not None:
            if vtype == 'real' and isinstance(value, int):
                v = float(value)
                self.error(496, f'converted int {value} to real {v}')
                value = v
            elif vtype == 'int' and isinstance(value, float):
                v = round(value)
                self.error(498, f'converted real {value} to int {v}')
                value = v
            else:
                self.error(500, message)
        if not self.stack:
            self.error(501, 'invalid UXF data')
            return
        append_to_parent(self.stack[-1], value)

    def _on_collection_start(self, token):
        kind = token.kind
        if kind is _Kind.MAP_BEGIN:
            value = Map()
        elif kind is _Kind.LIST_BEGIN:
            value = List()
        elif kind is _Kind.TABLE_BEGIN:
            value = Table()
        else:
            self.error(504, f'expected to create map, list, or table, got {token}')
        if self.stack:
            _, message = self.typecheck(value)
            if message is not None:
                self.error(506, message)
            append_to_parent(self.stack[-1], value)
        self.stack.append(value)

    def _on_collection_end(self, token):
        if not self.stack:
            self.error(510, f'unexpected {token} suggests unmatched map, list, or table start/end pair')
            return
        parent = self.stack[-1]
        if token.kind is _Kind.LIST_END:
            Class = List
            closer = ']'
        elif token.kind is _Kind.MAP_END:
            Class = Map
            closer = '}'
        elif token.kind is _Kind.TABLE_END:
            Class = Table
            closer = ')'
        if not isinstance(parent, Class):
            self.error(512, f'expected {closer!r}, got {token.value!r}')
        self.stack.pop()

    def _is_collection_start(self, kind):
        return kind in {_Kind.MAP_BEGIN, _Kind.LIST_BEGIN, _Kind.TABLE_BEGIN}

    def _is_collection_end(self, kind):
        return kind in {_Kind.MAP_END, _Kind.LIST_END, _Kind.TABLE_END}

    def _parse_file_comment(self):
        if self.tokens:
            token = self.tokens[0]
            self.lino = token.lino
            if token.kind is _Kind.COMMENT:
                self.tokens = self.tokens[1:]
                return token.value
        return None

    def _parse_imports(self):
        offset = 0
        for index, token in enumerate(self.tokens):
            self.lino = token.lino
            if token.kind is _Kind.IMPORT:
                self._handle_import(token.value)
                offset = index + 1
        self.tokens = self.tokens[offset:]

    def _parse_tclasses(self):
        tclass = None
        offset = 0
        for index, token in enumerate(self.tokens):
            self.lino = token.lino
            if token.kind is _Kind.TCLASS_BEGIN:
                tclass, ok = self._handle_tclass_begin(tclass)
                if not ok:
                    return
            elif token.kind is _Kind.COMMENT:
                tclass.comment = token.value
            elif token.kind is _Kind.IDENTIFIER:
                if not self._handle_tclass_ttype(tclass, token.value):
                    return
            elif token.kind is _Kind.TYPE:
                if not self._handle_tclass_vtype(tclass, token):
                    return
            elif token.kind is _Kind.TCLASS_END:
                if not self._handle_tclass_end(tclass):
                    return
                offset = index + 1
            else:
                break
        self.tokens = self.tokens[offset:]

    def _handle_tclass_begin(self, tclass):
        if tclass is not None:
            if tclass.ttype is None:
                self.error(518, 'TClass without ttype', fail=True)
                return (None, False)
            _add_to_tclasses(self.tclasses, tclass, lino=self.lino, code=520, on_error=self.on_error)
            self.lino_for_tclass[tclass.ttype] = self.lino
        return (TClass(None), True)

    def _handle_tclass_ttype(self, tclass, value):
        if tclass is None:
            self.error(522, 'missing ttype; is an `=` missing?', fail=True)
            return False
        elif tclass.ttype is None:
            tclass.ttype = value
        else:
            tclass.append(value)
        return True

    def _handle_tclass_vtype(self, tclass, token):
        if not tclass:
            self.error(524, f'cannot use a built-in type name or constant as a tclass name, got {token}', fail=True)
            return False
        else:
            vtype = token.value
            tclass.set_vtype(-1, vtype)
            return True

    def _handle_tclass_end(self, tclass):
        if tclass is not None:
            if tclass.ttype is None:
                self.error(526, 'TClass without ttype', fail=True)
                return False
            _add_to_tclasses(self.tclasses, tclass, lino=self.lino, code=528, on_error=self.on_error)
            if tclass.ttype not in self.lino_for_tclass:
                self.lino_for_tclass[tclass.ttype] = self.lino
        return True

    def _handle_import(self, value):
        filename = text = None
        try:
            if value.startswith(('http://', 'https://')):
                text = self._url_import(value)
            elif '.' not in value:
                return self._system_import(value)
            else:
                filename = value
            if filename is not None:
                uxo = self._load_import(filename)
            elif text is not None:
                uxo = self._parse_url_text(text, value)
            else:
                self.error(540, f'there are no ttype definitions to import {value!r} ({filename!r})')
                return
            if uxo is None:
                self.error(541, 'invalid UXF data')
                return
            for ttype, tclass in uxo.tclasses.items():
                if _add_to_tclasses(self.tclasses, tclass, lino=self.lino, code=544, on_error=self.on_error):
                    self.imports[ttype] = value
        except _AlreadyImported:
            pass

    def _url_import(self, url):
        if url in self.imported:
            raise _AlreadyImported
        try:
            with urllib.request.urlopen(url) as file:
                return file.read().decode()
        except (UnicodeDecodeError, OSError) as err:
            if url == 'http://www.qtrac.eu/ttype-eg.uxf':
                return _TTYPE_EG_UXF
            self.error(550, f'failed to import {url!r}: {err}')
            raise _AlreadyImported
        finally:
            self.imported.add(url)

    def _parse_url_text(self, text, filename):
        try:
            return loads(text, filename=filename, on_error=self._on_import_error, _imported=self.imported, _is_import=True)
        except Error as err:
            self.error(530, f'failed to import {filename!r}: {err}')

    def _system_import(self, value):
        if value == 'complex':
            self._system_import_tclass(_ComplexTClass, value)
        elif value == 'fraction':
            self._system_import_tclass(_FractionTClass, value)
        elif value == 'numeric':
            self._system_import_tclass(_ComplexTClass, value)
            self._system_import_tclass(_FractionTClass, value)
        else:
            self.error(560, f'there is no system ttype import called {value!r}')
            raise _AlreadyImported

    def _system_import_tclass(self, tclass, name):
        if _add_to_tclasses(self.tclasses, tclass, lino=self.lino, code=570, on_error=self.on_error):
            self.imports[tclass.ttype] = name

    def _load_import(self, filename):
        fullname = self._get_fullname(filename)
        if fullname in self.imported:
            raise _AlreadyImported
        try:
            return load(fullname, on_error=self._on_import_error, _imported=self.imported, _is_import=True)
        except (FileNotFoundError, Error) as err:
            if fullname in self.imported:
                self.error(580, f'cannot do circular imports {fullname!r}', fail=True)
                return
            else:
                self.error(586, f'failed to import {fullname!r}: {err}')
            raise _AlreadyImported
        finally:
            self.imported.add(fullname)

    def _get_fullname(self, filename):
        """Searches in order: filename's path, cwd, UXF_PATHs"""
        paths = []
        if self.filename and self.filename != '-':
            paths.append(os.path.dirname(self.filename))
        if paths and paths[0] != '.':
            paths.append('.')
        uxf_paths = os.environ.get('UXF_PATH')
        if uxf_paths:
            paths += uxf_paths.split(';' if sys.platform.startswith('win') else ':')
        for path in paths:
            fullname = _full_filename(filename, path)
            if fullname in self.imported:
                raise _AlreadyImported
            if os.path.isfile(fullname):
                return fullname
        return _full_filename(filename)

    def _on_import_error(self, lino, code, message, *, filename, fail=False, verbose=True):
        if code == 418:
            return
        self.on_error(lino, code, message, filename=filename, fail=fail, verbose=verbose)

    def typecheck(self, value):
        if not self.stack:
            self.error(590, 'invalid UXF data')
            return (None, None)
        parent = self.stack[-1]
        if isinstance(parent, Map):
            vtype = parent.ktype if parent._next_is_key else parent.vtype
        elif isinstance(parent, List):
            vtype = parent.vtype
        else:
            vtype = parent._next_vtype
        if value is not None and vtype is not None:
            if vtype in _BUILT_IN_NAMES:
                if not isinstance(value, _TYPECHECK_CLASSES[vtype]):
                    message = f'expected {vtype}, got {value.__class__.__name__} {value}'
                    return (vtype, message)
            elif vtype not in self.tclasses:
                message = f'expected {vtype}, got {value.__class__.__name__} {value}'
                return (vtype, message)
        return (None, None)

def _add_to_tclasses(tclasses, tclass, *, lino, code, on_error):
    first_tclass = tclasses.get(tclass.ttype)
    if first_tclass is None:
        tclasses[tclass.ttype] = tclass
        return True
    if first_tclass == tclass:
        if tclass.comment and tclass.comment != first_tclass.comment:
            first_tclass.comment = tclass.comment
        return True
    else:
        on_error(lino, code, f'conflicting ttype definitions for {tclass.ttype}', fail=True)
    return False
_TYPECHECK_CLASSES = dict(collection=(List, Map, Table), bool=bool, bytes=(bytes, bytearray), date=datetime.date, datetime=datetime.datetime, int=int, list=List, map=Map, real=float, str=str, table=Table)
_BUILT_IN_NAMES = tuple(_TYPECHECK_CLASSES.keys())

def dump(filename_or_filelike, data, *, on_error=on_error, format=Format()):
    """
    filename_or_filelike is sys.stdout or a filename or an open writable
    file (text mode UTF-8 encoded). If filename_or_filelike is a filename
    with a .gz suffix then the output will be gzip-compressed.

    data is a Uxf object, or a list, List, dict, Map, or Table, that this
    function will write to the filename_or_filelike in UXF format.
    """
    close = False
    if isinstance(filename_or_filelike, (str, pathlib.Path)):
        filename_or_filelike = str(filename_or_filelike)
        opener = gzip.open if filename_or_filelike[-3:].upper().endswith('.GZ') else open
        file = opener(filename_or_filelike, 'wt', encoding=UTF8)
        close = True
    else:
        file = filename_or_filelike
    try:
        if not isinstance(data, Uxf):
            data = Uxf(data)
        _Writer(file, data, on_error, format)
    finally:
        if close:
            file.close()

def dumps(data, *, on_error=on_error, format=Format()):
    """
    data is a Uxf object, or a list, List, dict, Map, or Table that this
    function will write to a string in UXF format which will then be
    returned.
    """
    string = io.StringIO()
    if not isinstance(data, Uxf):
        data = Uxf(data)
    _Writer(string, data, on_error, format)
    return string.getvalue()

class _Writer:

    def __init__(self, file, uxo, on_error, format):
        self.file = file
        self.on_error = on_error
        self.format = format
        self.column = 0
        self.indent = 0
        self.closed = ''
        self.last_line = '\n'
        self.prev_last_line = '\n'
        self.pending = []
        self.write_header(uxo.custom)
        if uxo.comment is not None:
            self.file.write(f'#<{escape(uxo.comment)}>\n')
        if uxo.imports:
            self.write_imports(uxo.import_filenames)
        if uxo.tclasses:
            self.write_tclasses(uxo.tclasses, uxo.imports)
        self.write_value(uxo.value)
        self._write_pending('\n' if self.prev != '\n' else '', force=True)

    def error(self, code, message, *, fail=False):
        self.on_error(0, code, message, fail=fail)

    @property
    def prev(self):
        return self.last_line[-1] if self.last_line else '\x00'

    @property
    def had_space(self):
        return self.last_line.isspace()

    def write_header(self, custom):
        self.file.write(f'uxf {VERSION}')
        if custom:
            self.file.write(f' {custom}')
        self.file.write('\n')

    def write_imports(self, import_filenames):
        for filename in import_filenames:
            self.file.write(f'!{filename}\n')

    def write_tclasses(self, tclasses, imports):
        for ttype, tclass in sorted(tclasses.items(), key=lambda t: t[0].upper()):
            if imports and ttype in imports:
                continue
            self.file.write('=')
            column = self._write_tclass_comment(1, tclass)
            column = self._write_tclass_ttype(column, tclass)
            for field in tclass.fields:
                column = self._write_tclass_field(column, field)
            self.file.write('\n')

    def _write_tclass_comment(self, column, tclass):
        if tclass.comment:
            text = f'#<{escape(tclass.comment)}> '
            column += len(text)
            self.file.write(text)
        return column

    def _write_tclass_ttype(self, column, tclass):
        text = f'{tclass.ttype}'
        if self.format.wrap_width:
            if column + len(text) > self.format.wrap_width:
                self.file.write(f'\n{self.format.indent}')
                column = len(self.format.indent)
            else:
                column += len(text)
        self.file.write(text)
        return column

    def _write_tclass_field(self, column, field):
        text = f' {field.name}'
        if field.vtype is not None:
            text += f':{field.vtype}'
        if self.format.wrap_width:
            if column + len(text) > self.format.wrap_width:
                self.file.write(f'\n{self.format.indent}')
                column = len(self.format.indent)
            else:
                column += len(text)
        self.file.write(text)
        return column

    def write_value(self, item):
        if isinstance(item, (set, frozenset, tuple, collections.deque)):
            item = List(item)
        if isinstance(item, (list, List)):
            self.write_list(item)
        elif isinstance(item, (dict, Map)):
            self.write_map(item)
        elif isinstance(item, Table):
            self.write_table(item)
        else:
            self.write_scalar(item)

    def write_list(self, item):
        closed = self._write_nl_if_closed()
        prefix = self._collection_prefix(item)
        text = f'{self.tab}[{prefix}'
        if len(item) == 0:
            self._write_close(text, ']')
            return
        text = self._write_open(text)
        if len(item) == 1 or _are_short(self.format.max_short_len, *item):
            sep = _SEP if prefix and (not text.endswith(_SEP)) else ''
            self._write_short_list(sep, item)
        else:
            self.indent += 1
            if not closed or self.prev != '\n':
                self._write_one(f'\n{self.format.indent * self.indent}')
            self._write_list(item)
            self.indent -= 1
            self._write_nl(']')

    def _write_short_list(self, sep, item):
        for value in item:
            self._write_one_value(value, sep)
            sep = _SEP
        self._write_one(']')

    def _write_list(self, item):
        sep = ''
        for value in item:
            self._write_one_value(value, sep)
            sep = _SEP

    def write_map(self, item):
        closed = self._write_nl_if_closed()
        prefix = self._collection_prefix(item)
        text = f'{self.tab}{{{prefix}'
        if len(item) == 0:
            self._write_close(text, '}')
            return
        text = self._write_open(text)
        sep = _SEP if prefix and (not text.endswith(_SEP)) else ''
        if len(item) == 1:
            self._write_single_item_map(sep, item)
        elif _are_short(self.format.max_short_len, *list(item.values())):
            self._write_short_map(sep, item)
        else:
            self.indent += 1
            if not closed:
                self._write_one(f'\n{self.format.indent * self.indent}')
            self._write_map(item)
            self.indent -= 1
            self._write_nl('}')

    def _write_single_item_map(self, sep, item):
        key, value = list(item.items())[0]
        if sep:
            self._write_one(sep)
        self.write_scalar(key)
        self._write_one_value(value)
        self._write_one('}')

    def _write_short_map(self, sep, item):
        for key, value in item.items():
            if sep:
                self._write_one(sep)
            self.write_scalar(key)
            self._write_one_value(value)
            sep = _SEP
        self._write_one('}')

    def _write_map(self, item):
        for key, value in item.items():
            self._write_pre_item_nl('')
            self.write_scalar(key)
            scalar = is_scalar(value)
            if not scalar:
                self.indent += 1
            self._write_one_value(value)
            if not scalar:
                self.indent -= 1

    def _write_one_value(self, value, sep=_SEP):
        if sep and (not self.prev.isspace()) and (is_scalar(value) or _is_short(value, self.format)):
            self._write_one(sep)
        self.write_value(value)

    def write_table(self, item):
        closed = self._write_nl_if_closed()
        prefix = self._collection_prefix(item)
        text = f'{self.tab}({prefix}'
        if len(item) == 0:
            self._write_close(text, ')')
            return
        text = self._write_open(text)
        if len(item) == 1:
            sep = _SEP if prefix and (not text.endswith(_SEP)) else ''
            self._write_single_record_table(item[0], sep)
        else:
            self.indent += 1
            if not closed:
                self._write_one(f'\n{self.format.indent * self.indent}')
            self._write_table(item)
            self.indent -= 1
            self._write_nl(')')

    def _write_single_record_table(self, record, sep):
        self._write_one(sep)
        self._write_record(record)
        self._write_one(')')

    def _write_table(self, item):
        for record in item:
            self._write_pre_item_nl('')
            self._write_record(record)

    def _write_record(self, record):
        sep = ''
        for value in record:
            self._write_one(sep)
            self._write_one_value(value, sep)
            sep = _SEP

    def write_scalar(self, item):
        if item is None:
            self._write_one('?')
        elif isinstance(item, bool):
            self._write_one('yes' if item else 'no')
        elif isinstance(item, int):
            self._write_one(str(item))
        elif isinstance(item, float):
            if self.format.realdp is not None:
                item = round(item, self.format.realdp)
            text = str(item)
            if '.' not in text and 'e' not in text and ('E' not in text):
                text += '.0'
            self._write_one(text)
        elif isinstance(item, (datetime.date, datetime.datetime)):
            self._write_one(isoformat(item))
        elif isinstance(item, str):
            self._write_one(f'<{escape(item)}>')
        elif isinstance(item, (bytes, bytearray)):
            self._write_one(f'(:{item.hex().upper()}:)')
        else:
            self.error(561, f'unexpected item of type {item.__class__.__name__}: {item!r};consider using a ttype', fail=True)
            return
        return False

    @property
    def tab(self):
        if self.prev == '\n':
            return self.format.indent * self.indent
        return '' if self.prev.isspace() else _SEP

    def _write_nl(self, one):
        self._write_one('\n')
        self._write_one(self.format.indent * self.indent)
        self._write_one(one)

    def _write_pre_item_nl(self, one):
        self._write_one('\n')
        self._write_one(self.format.indent * self.indent)
        self._write_one(one)

    def _write_one(self, one):
        if (not one or one == self.prev == '\n') or (self.prev_last_line not in ']})' and (not self.prev_last_line.endswith(':)')) and (one == '\n') and self.had_space):
            return
        wrap_width = self.format.wrap_width
        if wrap_width and len(one) < wrap_width and (not one.isspace()) and (self.column + len(one) > wrap_width) and (not ('\n' in self.prev_last_line and self.had_space)):
            self._write_pending('\n')
            tab = self.format.indent * self.indent
            self._write_pending(tab)
            self._update(f'\n{tab}')
        self._write_pending(one)
        self._update(one)
        one = one.rstrip()
        if not one.endswith(':)') and one.endswith((']', '}', ')')):
            self.closed = one[-1]
        elif not self.prev.isspace():
            self.closed = ''

    def _update(self, text):
        i = text.rfind('\n')
        if i == -1:
            self.column += len(text)
        else:
            self.column = len(text[i + 1:])
            text = text[i:]
        self.prev_last_line = self.last_line
        self.last_line = text

    def _write_pending(self, text, *, force=False):
        if text.endswith('\n'):
            while self.pending and self.pending[-1].isspace():
                self.pending.pop()
            self.pending.append(text)
            force = True
        if force:
            text = ''.join(self.pending)
            self.file.write(text)
            self._update(text)
            self.pending.clear()
        else:
            self.pending.append(text)

    def _write_open(self, text):
        if text.endswith('>'):
            text += _SEP
        self._write_one(text)
        return text

    def _write_close(self, text, close):
        text += close
        self._write_one(text)

    def _write_nl_if_closed(self):
        closed = False
        if self.closed in ']})':
            self._write_one('\n')
            closed = True
        return closed

    def _collection_prefix(self, item):
        comment = getattr(item, 'comment', None)
        ktype = getattr(item, 'ktype', None)
        vtype = getattr(item, 'vtype', None)
        tclass = getattr(item, 'tclass', None)
        parts = []
        if comment is not None:
            parts.append(f'#<{escape(comment)}>')
        if ktype is not None:
            parts.append(ktype)
        if vtype is not None:
            parts.append(vtype)
        if tclass is not None:
            parts.append(tclass.ttype)
        return _SEP.join(parts) if parts else ''

def is_scalar(x):
    """Returns True if x is None or a bool, int, float, datetime.date,
    datetime.datetime, str, bytes, or bytearray; otherwise returns False."""
    return x is None or isinstance(x, (bool, int, float, datetime.date, datetime.datetime, str, bytes, bytearray))

def _is_key_type(x):
    return isinstance(x, (int, datetime.date, datetime.datetime, str, bytes))

def _is_short(value, format):
    if isinstance(value, (bytes, bytearray, str)):
        return len(value) <= format.max_short_len
    if is_scalar(value) or len(value) == 1:
        return True
    if isinstance(value, (list, List)) and _are_short(format.max_short_len, *value):
        return True
    if isinstance(value, (dict, Map)) and _are_short(format.max_short_len, *list(value.values())):
        return True
    return False

def _are_short(max_short_len, *items):
    for x in items:
        if isinstance(x, (bytes, bytearray, str)):
            if len(x) > max_short_len:
                return False
        elif x is not None and (not isinstance(x, (bool, int, float, datetime.date, datetime.datetime))):
            return False
    return True

def _is_uxf_collection(value):
    return isinstance(value, (List, Map, Table))

def _full_filename(filename, path='.'):
    if os.path.isabs(filename):
        return filename
    return os.path.abspath(os.path.join(path, filename))

class _AlreadyImported(Exception):
    pass

def append_to_parent(parent, value):
    """Utility for UXF processors; see uxf.py and uxfconvert.py for examples
    of use."""
    if isinstance(parent, (Map, Table)):
        parent._append(value)
    else:
        parent.append(value)

def naturalize(s):
    """Given string s returns True if the string is 't', 'true', 'y', 'yes',
    or False if the string is 'f', 'false', 'n', 'no' (case-insensitive), or
    an int if s holds a parsable int, or a float if s holds a parsable
    float, or a datetime.datetime if s holds a parsable ISO8601 datetime
    string, or a datetime.date if s holds a parsable ISO8601 date string, or
    failing these returns the string s unchanged.
    """
    u = s.upper()
    if u in {'T', 'TRUE', 'Y', 'YES'}:
        return True
    if u in {'F', 'FALSE', 'N', 'NO'}:
        return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            try:
                if 'T' in s:
                    return datetime.datetime.fromisoformat(s)
                else:
                    return datetime.date.fromisoformat(s)
            except ValueError:
                return s

def canonicalize(name):
    """Given a name, returns a name that is a valid table or field name.
    is_table_name must be True (the default) for tables since table names
    have additional constraints. (See uxfconvert.py for uses.)"""
    prefix = 'UXF_'
    cs = []
    if name[0] == '_' or name[0].isalpha():
        cs.append(name[0])
    else:
        cs.append(prefix)
    for c in name[1:]:
        if c.isspace() or c in '/\\,;:.-':
            if not cs or cs[-1] != '_':
                cs.append('_')
        elif c == '_' or c.isalnum():
            cs.append(c)
    name = ''.join(cs)
    if name in RESERVED_WORDS:
        name = prefix + name
    elif not name:
        name = prefix
    if name == prefix:
        name += str(canonicalize.count)
        canonicalize.count += 1
    return name[:_MAX_IDENTIFIER_LEN]
canonicalize.count = 1

def isasciidigit(s):
    """Returns True if s matches /^[0-9]+$/."""
    return s.isascii() and s.isdigit()

def isoformat(dt):
    """Returns ISO8601 str representing the given date or datetime; in the
    latter case limited to 1-second resolution."""
    return dt.isoformat()[:19]
_ComplexTClass = TClass('Complex', (Field('Real', 'real'), Field('Imag', 'real')))
_FractionTClass = TClass('Fraction', (Field('numerator', 'int'), Field('denominator', 'int')))
_TTYPE_EG_UXF = 'uxf 1.0 Slides 0.1.0\n#<This is a simple example of an application-specific use of UXF.\nSee slides[12].py for examples of converting this format to HTML.>\n= Slide title body\n= #<title> h1 content\n= #<subtitle> h2 content\n= #<bullet item> B content\n= #<para> p content\n= #<image> img content image:bytes\n= #<monospace inline> m content\n= #<monospace block> pre content\n= #<italic> i content\n= url content link\n= #<newline with no content> nl\n[]\n'
if __name__ == '__main__':
    import argparse
    import contextlib
    import shutil
    import textwrap

    def get_usage(text):
        try:
            term_width = shutil.get_terminal_size()[0]
        except AttributeError:
            term_width = 80
        return '\n\n'.join(('\n'.join(textwrap.wrap(para.strip(), term_width)) for para in text.strip().split('\n\n') if para.strip()))
    parser = argparse.ArgumentParser(usage=get_usage("usage: uxf.py [-l|--lint] [-d|--dropunused] [-r|--replaceimports] [-iI|--indent=I] [-wW|--wrapwidth=W] <infile.uxf[.gz]> [<outfile.uxf[.gz]>]\n   or: python3 -m uxf ...same options as above...\n\nIf an outfile is specified and ends .gz it will be gzip-compressed.\nIf outfile is - output will be to stdout.\nIf you just want linting either don't specify an outfile at all or\nuse -l or --lint. Lint errors and fixes go to stderr.\n\nUse -d or --dropunused to drop unused ttype definitions and imports.\n\nUse -r or --replaceimports to replace imports with ttype definitions\nto make the outfile standalone (i.e., not dependent on any imports).\n\n(-d, -l, and -r may be grouped, e.g., -ldr, -dl, etc.)\n\nIndent defaults to 2 and accepts a range of 0-32.\n\nWrapwidth defaults to 96 and accepts 0 (no wrapping) or a range of 40-240.\n\nFor indent and wrapwidth the default is silently used if an out of range\nvalue is given.\n\nTo get an uncompressed .uxf file run: `uxf.py infile.uxf.gz outfile.uxf` or\nsimply `gunzip infile.uxf.gz`.\n\nTo produce a compressed and compact .uxf file run:\n`uxf.py -i0 -w0 infile.uxf outfile.uxf.gz`\n\nConverting uxf to uxf will alphabetically order any ttypes.\nHowever, the order of imports is preserved (with any duplicates removed)\nto allow later imports to override earlier ones.\n"))
    parser.add_argument('-l', '--lint', action='store_true', help='show lint errors')
    parser.add_argument('-d', '--dropunused', action='store_true', help='drop unused imports and ttypes')
    parser.add_argument('-r', '--replaceimports', action='store_true', help='replace imports with their used ttypes')
    parser.add_argument('-i', '--indent', type=int, default=2, help='indent (0-32; default 2)')
    parser.add_argument('-w', '--wrapwidth', type=int, default=96, help='wrapwidth (0 or 40-240; default 96)')
    parser.add_argument('infile', nargs=1, help='required UXF infile')
    parser.add_argument('outfile', nargs='?', help='optional UXF outfile')
    config = parser.parse_args()
    config.indent = ' ' * config.indent
    infile = config.infile[0]
    outfile = config.outfile
    if outfile is not None:
        with contextlib.suppress(FileNotFoundError):
            if os.path.samefile(infile, outfile):
                raise SystemExit(f"uxf.py:error:won't overwrite {outfile}")
    try:
        lint = config.lint or (config.lint is None and outfile is None)
        on_error = functools.partial(on_error, verbose=config.lint, filename=infile)
        uxo = load(infile, on_error=on_error, drop_unused=config.dropunused, replace_imports=config.replaceimports)
        do_dump = outfile is not None
        outfile = sys.stdout if outfile == '-' else outfile
        on_error = functools.partial(on_error, verbose=config.lint, filename=outfile)
        if do_dump:
            format = Format(indent=config.indent, wrap_width=config.wrapwidth)
            dump(outfile, uxo, on_error=on_error, format=format)
    except (OSError, Error) as err:
        message = str(err)
        if not message.startswith('uxf.py'):
            message = f'uxf.py:error:{message}'
        print(message, file=sys.stderr)