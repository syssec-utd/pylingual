from __future__ import absolute_import, division, unicode_literals
from types import ModuleType
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
from pip._vendor.six import text_type, PY3
if PY3:
    import xml.etree.ElementTree as default_etree
else:
    try:
        import xml.etree.cElementTree as default_etree
    except ImportError:
        import xml.etree.ElementTree as default_etree
__all__ = ['default_etree', 'MethodDispatcher', 'isSurrogatePair', 'surrogatePairToCodepoint', 'moduleFactoryFactory', 'supports_lone_surrogates']
try:
    _x = eval('"\\uD800"')
    if not isinstance(_x, text_type):
        _x = eval('u"\\uD800"')
        assert isinstance(_x, text_type)
except Exception:
    supports_lone_surrogates = False
else:
    supports_lone_surrogates = True

class MethodDispatcher(dict):
    """Dict with 2 special properties:

    On initiation, keys that are lists, sets or tuples are converted to
    multiple keys so accessing any one of the items in the original
    list-like object returns the matching value

    md = MethodDispatcher({("foo", "bar"):"baz"})
    md["foo"] == "baz"

    A default value which can be set through the default attribute.
    """

    def __init__(self, items=()):
        _dictEntries = []
        for name, value in items:
            if isinstance(name, (list, tuple, frozenset, set)):
                for item in name:
                    _dictEntries.append((item, value))
            else:
                _dictEntries.append((name, value))
        dict.__init__(self, _dictEntries)
        assert len(self) == len(_dictEntries)
        self.default = None

    def __getitem__(self, key):
        return dict.get(self, key, self.default)

    def __get__(self, instance, owner=None):
        return BoundMethodDispatcher(instance, self)

class BoundMethodDispatcher(Mapping):
    """Wraps a MethodDispatcher, binding its return values to `instance`"""

    def __init__(self, instance, dispatcher):
        self.instance = instance
        self.dispatcher = dispatcher

    def __getitem__(self, key):
        return self.dispatcher[key].__get__(self.instance)

    def get(self, key, default):
        if key in self.dispatcher:
            return self[key]
        else:
            return default

    def __iter__(self):
        return iter(self.dispatcher)

    def __len__(self):
        return len(self.dispatcher)

    def __contains__(self, key):
        return key in self.dispatcher

def isSurrogatePair(data):
    return len(data) == 2 and ord(data[0]) >= 55296 and (ord(data[0]) <= 56319) and (ord(data[1]) >= 56320) and (ord(data[1]) <= 57343)

def surrogatePairToCodepoint(data):
    char_val = 65536 + (ord(data[0]) - 55296) * 1024 + (ord(data[1]) - 56320)
    return char_val

def moduleFactoryFactory(factory):
    moduleCache = {}

    def moduleFactory(baseModule, *args, **kwargs):
        if isinstance(ModuleType.__name__, type('')):
            name = '_%s_factory' % baseModule.__name__
        else:
            name = b'_%s_factory' % baseModule.__name__
        kwargs_tuple = tuple(kwargs.items())
        try:
            return moduleCache[name][args][kwargs_tuple]
        except KeyError:
            mod = ModuleType(name)
            objs = factory(baseModule, *args, **kwargs)
            mod.__dict__.update(objs)
            if 'name' not in moduleCache:
                moduleCache[name] = {}
            if 'args' not in moduleCache[name]:
                moduleCache[name][args] = {}
            if 'kwargs' not in moduleCache[name][args]:
                moduleCache[name][args][kwargs_tuple] = {}
            moduleCache[name][args][kwargs_tuple] = mod
            return mod
    return moduleFactory

def memoize(func):
    cache = {}

    def wrapped(*args, **kwargs):
        key = (tuple(args), tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapped