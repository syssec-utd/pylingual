"""
@file
@brief Saves and reads a :epkg:`dataframe` into a :epkg:`zip` file.
"""
import os
from io import StringIO, BytesIO
try:
    from ujson import dumps
except ImportError:
    from json import dumps
import ijson

class JsonPerRowsStream:
    """
    Reads a :epkg:`json` streams and adds
    ``,``, ``[``, ``]`` to convert a stream containing
    one :epkg:`json` object per row into one single :epkg:`json` object.
    It only implements method *readline*.

    :param st: stream
    """

    def __init__(self, st):
        self.st = st
        self.begin = True
        self.newline = False
        self.end = True

    def seek(self, offset):
        """
        Change the stream position to the given byte offset.

        :param offset: offset, only 0 is implemented
        """
        self.st.seek(offset)

    def readline(self, size=-1):
        """
        Reads a line, adds ``,``, ``[``, ``]`` if needed.
        So the number of read characters is not recessarily
        the requested one but could be greater.
        """
        text = self.st.readline(size)
        if size == 0:
            return text
        if self.newline:
            text = ',' + text
            self.newline = False
        elif self.begin:
            text = '[' + text
            self.begin = False
        if text.endswith('\n'):
            self.newline = True
            return text
        if len(text) == 0 or len(text) < size:
            if self.end:
                self.end = False
                return text + ']'
            return text
        return text

    def read(self, size=-1):
        """
        Reads characters, adds ``,``, ``[``, ``]`` if needed.
        So the number of read characters is not recessarily
        the requested one but could be greater.
        """
        text = self.st.read(size)
        if isinstance(text, bytes):
            cst = (b'\n', b'\n,', b',', b'[', b']')
        else:
            cst = ('\n', '\n,', ',', '[', ']')
        if size == 0:
            return text
        if len(text) > 1:
            t1, t2 = (text[:len(text) - 1], text[len(text) - 1:])
            t1 = t1.replace(cst[0], cst[1])
            text = t1 + t2
        if self.newline:
            text = cst[2] + text
            self.newline = False
        elif self.begin:
            text = cst[3] + text
            self.begin = False
        if text.endswith(cst[0]):
            self.newline = True
            return text
        if len(text) == 0 or len(text) < size:
            if self.end:
                self.end = False
                return text + cst[4]
            return text
        return text

    def getvalue(self):
        """
        Returns the whole stream content.
        """

        def byline():
            line = self.readline()
            while line:
                yield line
                line = self.readline()
        return ''.join(byline())

def flatten_dictionary(dico, sep='_'):
    """
    Flattens a dictionary with nested structure to a dictionary with no
    hierarchy.

    :param dico: dictionary to flatten
    :param sep: string to separate dictionary keys by
    :return: flattened dictionary

    Inspired from `flatten_json
    <https://github.com/amirziai/flatten/blob/master/flatten_json.py>`_.
    """
    flattened_dict = {}

    def _flatten(obj, key):
        if obj is None:
            flattened_dict[key] = obj
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if not isinstance(k, str):
                    raise TypeError('All keys must a string.')
                k2 = k if key is None else f'{key}{sep}{k}'
                _flatten(v, k2)
        elif isinstance(obj, (list, set)):
            for index, item in enumerate(obj):
                k2 = k if key is None else f'{key}{sep}{index}'
                _flatten(item, k2)
        else:
            flattened_dict[key] = obj
    _flatten(dico, None)
    return flattened_dict

def enumerate_json_items(filename, encoding=None, lines=False, flatten=False, fLOG=None):
    """
    Enumerates items from a :epkg:`JSON` file or string.

    :param filename: filename or string or stream to parse
    :param encoding: encoding
    :param lines: one record per row
    :param flatten: call @see fn flatten_dictionary
    :param fLOG: logging function
    :return: iterator on records at first level.

    It assumes the syntax follows the format: ``[ {"id":1, ...}, {"id": 2, ...}, ...]``.
    However, if option *lines* if true, the function considers that the
    stream or file does have one record per row as follows:

        {"id":1, ...}
        {"id": 2, ...}

    .. exref::
        :title: Processes a json file by streaming.

        The module :epkg:`ijson` can read a :epkg:`JSON` file by streaming.
        This module is needed because a record can be written on multiple lines.
        This function leverages it produces the following results.

        .. runpython::
            :showcode:

            from pandas_streaming.df.dataframe_io_helpers import enumerate_json_items

            text_json = b'''
                [
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": [{
                                "GlossEntry": {
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }
                            }]
                        }
                    }
                },
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": {
                                "GlossEntry": [{
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }]
                            }
                        }
                    }
                }
                ]
            '''

            for item in enumerate_json_items(text_json):
                print(item)

    The parsed json must have an empty line at the end otherwise
    the following exception is raised:
    `ijson.common.IncompleteJSONError: `
    `parse error: unallowed token at this point in JSON text`.
    """
    if isinstance(filename, str):
        if '{' not in filename and os.path.exists(filename):
            with open(filename, 'r', encoding=encoding) as f:
                for el in enumerate_json_items(f, encoding=encoding, lines=lines, flatten=flatten, fLOG=fLOG):
                    yield el
        else:
            st = StringIO(filename)
            for el in enumerate_json_items(st, encoding=encoding, lines=lines, flatten=flatten, fLOG=fLOG):
                yield el
    elif isinstance(filename, bytes):
        st = BytesIO(filename)
        for el in enumerate_json_items(st, encoding=encoding, lines=lines, flatten=flatten, fLOG=fLOG):
            yield el
    elif lines:
        for el in enumerate_json_items(JsonPerRowsStream(filename), encoding=encoding, lines=False, flatten=flatten, fLOG=fLOG):
            yield el
    else:
        if hasattr(filename, 'seek'):
            filename.seek(0)
        parser = ijson.parse(filename)
        current = None
        curkey = None
        stack = []
        nbyield = 0
        for i, (_, event, value) in enumerate(parser):
            if i % 1000000 == 0 and fLOG is not None:
                fLOG(f'[enumerate_json_items] i={i} yielded={nbyield}')
            if event == 'start_array':
                if curkey is None:
                    current = []
                else:
                    if not isinstance(current, dict):
                        raise RuntimeError(f'Type issue {type(current)}')
                    c = []
                    current[curkey] = c
                    current = c
                curkey = None
                stack.append(current)
            elif event == 'end_array':
                stack.pop()
                if len(stack) == 0:
                    current = None
                else:
                    current = stack[-1]
            elif event == 'start_map':
                c = {}
                if curkey is None:
                    if current is None:
                        current = []
                    current.append(c)
                else:
                    current[curkey] = c
                stack.append(c)
                current = c
                curkey = None
            elif event == 'end_map':
                stack.pop()
                current = stack[-1]
                if len(stack) == 1:
                    nbyield += 1
                    if flatten:
                        yield flatten_dictionary(current[-1])
                    else:
                        yield current[-1]
                    current.clear()
            elif event == 'map_key':
                curkey = value
            elif event in {'string', 'number', 'boolean'}:
                if curkey is None:
                    current.append(value)
                else:
                    current[curkey] = value
                    curkey = None
            elif event == 'null':
                if curkey is None:
                    current.append(None)
                else:
                    current[curkey] = None
                    curkey = None
            else:
                raise ValueError(f"Unknown event '{event}'")

class JsonIterator2Stream:
    """
    Transforms an iterator on :epkg:`JSON` items
    into a stream which returns an items as a string every time
    method *read* is called.
    The iterator could be one returned by @see fn enumerate_json_items.

    :param it: iterator
    :param kwargs: arguments to :epkg:`*py:json:dumps`

    .. exref::
        :title: Reshape a json file

        The function @see fn enumerate_json_items reads any
        :epkg:`json` even if every record is split over
        multiple lines. Class @see cl JsonIterator2Stream
        mocks this iterator as a stream. Each row is a single item.

        .. runpython::
            :showcode:

            from pandas_streaming.df.dataframe_io_helpers import enumerate_json_items, JsonIterator2Stream

            text_json = b'''
                [
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": [{
                                "GlossEntry": {
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }
                            }]
                        }
                    }
                },
                {
                    "glossary": {
                        "title": "example glossary",
                        "GlossDiv": {
                            "title": "S",
                            "GlossList": {
                                "GlossEntry": [{
                                    "ID": "SGML",
                                    "SortAs": "SGML",
                                    "GlossTerm": "Standard Generalized Markup Language",
                                    "Acronym": "SGML",
                                    "Abbrev": "ISO 8879:1986",
                                    "GlossDef": {
                                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                        "GlossSeeAlso": ["GML", "XML"]
                                    },
                                    "GlossSee": "markup"
                                }]
                            }
                        }
                    }
                }
                ]
            '''

            for item in JsonIterator2Stream(lambda: enumerate_json_items(text_json)):
                print(item)

    .. versionchanged:: 0.3
        The class takes a function which outputs an iterator and not an iterator.
        `JsonIterator2Stream(enumerate_json_items(text_json))` needs to be rewritten
        into JsonIterator2Stream(lambda: enumerate_json_items(text_json)).
    """

    def __init__(self, it, **kwargs):
        self.it = it
        self.kwargs = kwargs
        self.it0 = it()

    def seek(self, offset):
        """
        Change the stream position to the given byte offset.

        :param offset: offset, only 0 is implemented
        """
        if offset != 0:
            raise NotImplementedError('The iterator can only return at the beginning.')
        self.it0 = self.it()

    def write(self):
        """
        The class does not write.
        """
        raise NotImplementedError()

    def read(self):
        """
        Reads the next item and returns it as a string.
        """
        try:
            value = next(self.it0)
            return dumps(value, **self.kwargs)
        except StopIteration:
            return None

    def __iter__(self):
        """
        Iterates on each row. The behaviour is a bit tricky.
        It is implemented to be swalled by :func:`pandas.read_json` which
        uses :func:`itertools.islice` to go through the items.
        It calls multiple times `__iter__` but does expect the
        iterator to continue from where it stopped last time.
        """
        for value in self.it0:
            yield dumps(value, **self.kwargs)