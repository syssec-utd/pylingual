import textwrap
import functools
from enum import Enum
from types import MappingProxyType
from typing import Any, Set, Dict, List, Type, Union, Optional, Generator
from dataclasses import fields
from blocks import Event
from blocks.logger import logger
from blocks.db.types import Table

class Dialects(str, Enum):
    postgres: str = 'postgres'
    sqlite: str = 'sqlite'
_PLACEHOLDERS: 'MappingProxyType[str, str]' = MappingProxyType({Dialects.postgres: '%s', Dialects.sqlite: '?'})
KEYWORDS = ('INSERT', 'INTO', 'UPDATE', 'SELECT', 'FROM', 'SET', 'WHERE', 'ORDER BY', 'LIMIT')
DEFAULT_SEPARATOR = ','

class Query(object):

    def __init__(self, codec: Optional[Type[Union[Event, Table]]]=None, dialect: str=Dialects.postgres) -> None:
        message = ['You are using EXPERIMENTAL API for queries', 'which is currently unstable and absolutely buggy & unsafe!', 'Use it on your own risk!']
        logger.warning(' '.join(message))
        self.data: Dict[str, List[str]] = {k: [] for k in KEYWORDS}
        self._where: Set[str] = set()
        self._codec: Optional[Type[Union[Event, Table]]] = codec
        self._fields: List[str] = []
        self._placeholder: str = _PLACEHOLDERS[dialect]

    @property
    def codec(self) -> Type[Union[Event, Table]]:
        if self._codec is None:
            raise ValueError("Couldn't sent any codec during query build. Please, check your Query() instance.")
        return self._codec

    @property
    def text(self) -> str:
        return str(self)

    def parametrize(self, event: Union[Event, Table]) -> tuple:
        return tuple([getattr(event, f) for f in self._fields])

    def add(self, keyword: str, *args: Union[str, Type[Union[Event, Table]]]) -> 'Query':
        target = self.data[keyword]
        for arg in args:
            if keyword == 'INTO' and self.data.get('INSERT'):
                if not isinstance(arg, str):
                    raise ValueError('Wrong argument for INSERT INTO statement: {0} ({1})'.format(arg, type(arg)))
                insert = self.data.get('INSERT')
                if insert:
                    statement = ['INTO'] + [arg] + [', '.join(insert)]
                    self.data['INSERT'] = [' '.join(statement)]
                else:
                    target.append(_clean_up(arg))
            elif isinstance(arg, str):
                if keyword == 'WHERE' and arg in self._where:
                    fld = _clean_up(arg)
                    target.append(fld + (' = ' + self._placeholder))
                    self._fields.append(fld)
                else:
                    target.append(_clean_up(arg))
            else:
                self._codec = arg
                self._where = set((field.name for field in fields(arg)))
                if keyword == 'INSERT':
                    attrs = [attr.name for attr in fields(arg)]
                    flds = []
                    vals = []
                    for (ix, attr) in enumerate(attrs, 1):
                        self._fields.append(attr)
                        if ix == 1:
                            flds.append('(' + attr)
                            vals.append('(' + self._placeholder)
                        elif ix == len(attrs):
                            flds.append(attr + ')')
                            vals.append(self._placeholder + ')')
                        else:
                            flds.append(attr)
                            vals.append(self._placeholder)
                    into_table = self.data.get('INTO')
                    if into_table:
                        self.data['INSERT'] = ['INTO'] + into_table + flds
                    else:
                        self.data['INSERT'] = flds
                    self.data['VALUES'] = [', '.join(vals)]
                elif keyword == 'SET':
                    to_append = []
                    for field in fields(arg):
                        to_append.append(field.name + (' = ' + self._placeholder))
                        self._fields.append(field.name)
                    target += to_append
                else:
                    target += [field.name for field in fields(arg)]
        return self

    def __getattr__(self, name: str) -> Any:
        if not name.isupper():
            return getattr(super(), name)
        return functools.partial(self.add, name.replace('_', ' '))

    def __str__(self) -> str:
        return ''.join(self._lines())

    def _lines(self) -> Generator[str, None, None]:
        for (keyword, things) in self.data.items():
            if not things:
                continue
            yield '{0}\n'.format(keyword)
            yield from self._lines_keyword(keyword, things)

    def _lines_keyword(self, keyword: str, things: List[str]) -> Generator[str, None, None]:
        for (i, thing) in enumerate(things, 1):
            last = i == len(things)
            yield self._indent(thing)
            if not last:
                if keyword == 'WHERE':
                    yield ' AND '
                else:
                    yield DEFAULT_SEPARATOR
            yield '\n'
    _indent = functools.partial(textwrap.indent, prefix='    ')

def _clean_up(thing: str) -> str:
    return textwrap.dedent(thing.rstrip()).strip()