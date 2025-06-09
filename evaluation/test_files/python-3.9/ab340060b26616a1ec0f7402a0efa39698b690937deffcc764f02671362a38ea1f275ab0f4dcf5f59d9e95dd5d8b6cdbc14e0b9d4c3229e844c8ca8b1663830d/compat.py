"""
httprunner.compat
~~~~~~~~~~~~~~~~~

This module handles import compatibility issues between Python 2 and
Python 3.
"""
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
try:
    import simplejson as json
except ImportError:
    import json
if is_py2:
    import urlparse
    from urllib import unquote
    ensure_ascii = True
    builtin_str = str
    bytes = str
    str = (unicode, bytes)
    basestring = basestring
    numeric_types = (int, long, float)
    integer_types = (int, long)
elif is_py3:
    import urllib.parse as urlparse
    from urllib.parse import unquote
    ensure_ascii = False
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)
    integer_types = (int,)