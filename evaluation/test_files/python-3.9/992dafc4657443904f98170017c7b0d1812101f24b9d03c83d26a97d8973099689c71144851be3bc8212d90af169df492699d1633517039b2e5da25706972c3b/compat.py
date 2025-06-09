"""
Copyright (c) 2006-2022 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
from __future__ import division
import binascii
import functools
import math
import os
import random
import sys
import time
import uuid

class WichmannHill(random.Random):
    """
    Reference: https://svn.python.org/projects/python/trunk/Lib/random.py
    """
    VERSION = 1

    def seed(self, a=None):
        """Initialize internal state from hashable object.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If a is not None or an int or long, hash(a) is used instead.

        If a is an int or long, a is used directly.  Distinct values between
        0 and 27814431486575L inclusive are guaranteed to yield distinct
        internal states (this guarantee is specific to the default
        Wichmann-Hill generator).
        """
        if a is None:
            try:
                a = int(binascii.hexlify(os.urandom(16)), 16)
            except NotImplementedError:
                a = int(time.time() * 256)
        if not isinstance(a, int):
            a = hash(a)
        (a, x) = divmod(a, 30268)
        (a, y) = divmod(a, 30306)
        (a, z) = divmod(a, 30322)
        self._seed = (int(x) + 1, int(y) + 1, int(z) + 1)
        self.gauss_next = None

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        (x, y, z) = self._seed
        x = 171 * x % 30269
        y = 172 * y % 30307
        z = 170 * z % 30323
        self._seed = (x, y, z)
        return (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0

    def getstate(self):
        """Return internal state; can be passed to setstate() later."""
        return (self.VERSION, self._seed, self.gauss_next)

    def setstate(self, state):
        """Restore internal state from object returned by getstate()."""
        version = state[0]
        if version == 1:
            (version, self._seed, self.gauss_next) = state
        else:
            raise ValueError('state with version %s passed to Random.setstate() of version %s' % (version, self.VERSION))

    def jumpahead(self, n):
        """Act as if n calls to random() were made, but quickly.

        n is an int, greater than or equal to 0.

        Example use:  If you have 2 threads and know that each will
        consume no more than a million random numbers, create two Random
        objects r1 and r2, then do
            r2.setstate(r1.getstate())
            r2.jumpahead(1000000)
        Then r1 and r2 will use guaranteed-disjoint segments of the full
        period.
        """
        if n < 0:
            raise ValueError('n must be >= 0')
        (x, y, z) = self._seed
        x = int(x * pow(171, n, 30269)) % 30269
        y = int(y * pow(172, n, 30307)) % 30307
        z = int(z * pow(170, n, 30323)) % 30323
        self._seed = (x, y, z)

    def __whseed(self, x=0, y=0, z=0):
        """Set the Wichmann-Hill seed from (x, y, z).

        These must be integers in the range [0, 256).
        """
        if not type(x) == type(y) == type(z) == int:
            raise TypeError('seeds must be integers')
        if not (0 <= x < 256 and 0 <= y < 256 and (0 <= z < 256)):
            raise ValueError('seeds must be in range(0, 256)')
        if 0 == x == y == z:
            t = int(time.time() * 256)
            t = int(t & 16777215 ^ t >> 24)
            (t, x) = divmod(t, 256)
            (t, y) = divmod(t, 256)
            (t, z) = divmod(t, 256)
        self._seed = (x or 1, y or 1, z or 1)
        self.gauss_next = None

    def whseed(self, a=None):
        """Seed from hashable object's hash code.

        None or no argument seeds from current time.  It is not guaranteed
        that objects with distinct hash codes lead to distinct internal
        states.

        This is obsolete, provided for compatibility with the seed routine
        used prior to Python 2.1.  Use the .seed() method instead.
        """
        if a is None:
            self.__whseed()
            return
        a = hash(a)
        (a, x) = divmod(a, 256)
        (a, y) = divmod(a, 256)
        (a, z) = divmod(a, 256)
        x = (x + a) % 256 or 1
        y = (y + a) % 256 or 1
        z = (z + a) % 256 or 1
        self.__whseed(x, y, z)

def patchHeaders(headers):
    if headers is not None and (not hasattr(headers, 'headers')):
        if isinstance(headers, dict):

            class _(dict):

                def __getitem__(self, key):
                    for key_ in self:
                        if key_.lower() == key.lower():
                            return super(_, self).__getitem__(key_)
                    raise KeyError(key)

                def get(self, key, default=None):
                    try:
                        return self[key]
                    except KeyError:
                        return default
            headers = _(headers)
        headers.headers = ['%s: %s\r\n' % (header, headers[header]) for header in headers]
    return headers

def cmp(a, b):
    """
    >>> cmp("a", "b")
    -1
    >>> cmp(2, 1)
    1
    """
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

def choose_boundary():
    """
    >>> len(choose_boundary()) == 32
    True
    """
    retval = ''
    try:
        retval = uuid.uuid4().hex
    except AttributeError:
        retval = ''.join((random.sample('0123456789abcdef', 1)[0] for _ in xrange(32)))
    return retval

def round(x, d=0):
    """
    >>> round(2.0)
    2.0
    >>> round(2.5)
    3.0
    """
    p = 10 ** d
    if x > 0:
        return float(math.floor(x * p + 0.5)) / p
    else:
        return float(math.ceil(x * p - 0.5)) / p

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

        def __hash__(self):
            raise TypeError('hash not implemented')
    return K
if not hasattr(functools, 'cmp_to_key'):
    functools.cmp_to_key = cmp_to_key
if sys.version_info >= (3, 0):
    xrange = range
    buffer = memoryview
else:
    xrange = xrange
    buffer = buffer
try:
    from pkg_resources import parse_version as LooseVersion
except ImportError:
    from distutils.version import LooseVersion