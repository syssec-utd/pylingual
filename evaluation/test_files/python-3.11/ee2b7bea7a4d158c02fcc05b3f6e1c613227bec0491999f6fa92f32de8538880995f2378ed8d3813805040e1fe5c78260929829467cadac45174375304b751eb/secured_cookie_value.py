import pickle as pickle
from rs4.protocols.sock.impl.http import http_date
import time
import random
from rs4 import pathtool
import os, sys
try:
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    from urllib import quote_plus, unquote_plus
import base64
import pickle
from hmac import new as hmac
_default_hash = None
if sys.version_info >= (2, 5):
    try:
        from hashlib import sha1 as _default_hash
    except ImportError:
        pass
if _default_hash is None:
    import sha as _default_hash

class UnquoteError(Exception):
    """Internal exception used to signal failures on quoting."""

class SecuredValue:
    hash_method = _default_hash
    serialization_method = pickle
    quote_base64 = True
    KEY = 'ATLSEC'

    def __init__(self, name, cookie, request, secret_key):
        self.name = '_' + name.upper()
        self.cookie = cookie
        self.request = request
        self.secret_key = secret_key
        self.data = None
        self.dirty = False
        self.__config = None
        self._source_verified = False

    def __contains__(self, k):
        self.data is None and self.unserialize()
        return k in self.data

    def _recal_expires(self, expires):
        return expires

    def clear(self):
        self.data is None and self.unserialize()
        self.set_default_data()
        self.dirty = True

    def validate(self):
        pass

    def source_verified(self):
        return self._source_verified

    def set_default_data(self):
        self.data = None

    def rollback(self):
        self.dirty = False

    def config(self, path=None, domain=None, secure=False, http_only=False, same_site=None):
        self.__config = (path, domain, secure, http_only, same_site)

    def set_cookie(self, expires):
        if expires != 0:
            data = self.serialize()
        else:
            data = ''
        if self.__config:
            self.cookie.set(self.KEY + self.name, data, expires, *self.__config)
        else:
            self.cookie.set(self.KEY + self.name, data, expires)
        self.dirty = False

    def unserialize(self):
        string = self.cookie.get_named_session_data(self.KEY + self.name)
        if not string:
            return self.set_default_data()
        self.unserialize_from_string(string.encode('utf8'))
        self.validate()

    def commit(self, expires=None):
        if not self.dirty or self.data is None:
            return
        self.set_cookie(self._recal_expires(expires))

    def quote(self, value):
        if self.serialization_method is not None:
            value = self.serialization_method.dumps(value, 1)
        if self.quote_base64:
            value = base64.b64encode(value)
            value = b''.join(value.splitlines()).strip()
        return value

    def unquote(self, value):
        try:
            if self.quote_base64:
                value = base64.b64decode(value)
            if self.serialization_method is not None:
                value = self.serialization_method.loads(value)
            return value
        except:
            raise UnquoteError

class SecuredDictValue(SecuredValue):

    def set_default_data(self):
        self.data = {}

    def __setitem__(self, k, v):
        self.set(k, v)

    def __delitem__(self, k):
        return self.remove(k)

    def __getitem__(self, k):
        return self.get(k)

    def __iter__(self):
        self.data is None and self.unserialize()
        return self.data.__iter()

    def has_key(self, k):
        self.data is None and self.unserialize()
        return k in self.data

    def items(self):
        self.data is None and self.unserialize()
        return list(self.data.items())

    def keys(self):
        self.data is None and self.unserialize()
        return list(self.data.keys())

    def values(self):
        self.data is None and self.unserialize()
        return list(self.data.values())

    def remove(self, k):
        self.data is None and self.unserialize()
        try:
            del self.data[k]
        except KeyError:
            pass
        else:
            self.dirty = True

    def set(self, k, v):
        self.data is None and self.unserialize()
        if type(k) is not type(''):
            raise TypeError('Session key must be string type')
        self.data[k] = v
        self.dirty = True

    def get(self, k, v=None):
        self.data is None and self.unserialize()
        return self.data.get(k, v)

    def serialize(self):
        if self.secret_key is None:
            raise RuntimeError('no secret key defined')
        result = []
        mac = hmac(self.secret_key, None, self.hash_method)
        for key, value in sorted(self.items(), key=lambda x: x[0]):
            result.append(quote_plus(key).encode('utf8') + b'=' + self.quote(value))
            mac.update(b'|' + result[-1])
        return (base64.b64encode(mac.digest()).strip() + b'?' + b'&'.join(result)).decode('utf8')

    def unserialize_from_string(self, string):
        items = {}
        try:
            base64_hash, data = string.split(b'?', 1)
        except:
            base64_hash, data, items = (b'', b'', {})
        else:
            mac = hmac(self.secret_key, None, self.hash_method)
            for item in data.split(b'&'):
                mac.update(b'|' + item)
                if not b'=' in item:
                    items = None
                    break
                key, value = item.split(b'=', 1)
                try:
                    key = unquote_plus(key.decode('utf8'))
                except UnicodeError:
                    pass
                items[key] = value
            try:
                client_hash = base64.b64decode(base64_hash)
            except Exception:
                items = client_hash = None
            if items is not None and client_hash == mac.digest():
                try:
                    for key, value in items.items():
                        items[key] = self.unquote(value)
                except UnquoteError:
                    items = {}
            else:
                items = {}
        self.data = items

class SecuredListValue(SecuredValue):

    def set_default_data(self):
        self.data = []

    def serialize(self):
        if self.secret_key is None:
            raise RuntimeError('no secret key defined')
        result = []
        mac = hmac(self.secret_key, None, self.hash_method)
        for value in sorted(self.data):
            result.append(self.quote(value))
            mac.update(b'|' + result[-1])
        return (base64.b64encode(mac.digest()).strip() + b'?' + b'&'.join(result)).decode('utf8')

    def unserialize_from_string(self, string):
        items = []
        try:
            base64_hash, data = string.split(b'?', 1)
        except:
            base64_hash, data, items = (b'', b'', [])
        else:
            try:
                client_hash = base64.b64decode(base64_hash)
            except Exception:
                items = client_hash = None
            mac = hmac(self.secret_key, None, self.hash_method)
            for item in data.split(b'&'):
                mac.update(b'|' + item)
                items.append(self.unquote(item))
            if client_hash != mac.digest():
                items = []
        self.data = items