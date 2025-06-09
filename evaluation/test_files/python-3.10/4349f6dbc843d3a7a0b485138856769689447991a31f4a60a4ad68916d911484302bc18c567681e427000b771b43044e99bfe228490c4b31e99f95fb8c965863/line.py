"""Lambda Functions"""
import re
import sys
import json
import uuid
import random
import socket
import getpass
import hashlib
from threading import Thread
__all__ = list(globals())
s128 = bytes(range(128)).decode()
s127 = bytes(range(32, 127)).decode()
empty = lambda *v, **kv: None
freeze = lambda fn, *v, **kv: lambda : fn(*v, **kv)
t = lambda arr: list(zip(*arr))
md5 = lambda b: hashlib.md5(b).hexdigest()
mask = lambda p: open(p + '.inv', 'wb').write(bytes((255 - b for b in open(p, 'rb').read())))
start = lambda func, *args, **kwargs: Thread(target=func, args=args, kwargs=kwargs).start()
create = lambda file: open(file, 'w').close()
pprint = lambda *value, file=sys.stdout: print(' '.join(map(str, value)) + '\n', end='', file=file)
dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)
sort_kv = lambda d, reverse=False: sorted(d.items(), key=lambda item: item[1], reverse=reverse)
sort_key = lambda d, reverse=False: sorted(d, key=d.__getitem__, reverse=reverse)
sort_num = lambda s: [(s, int(n)) for (s, n) in re.findall('(\\D+)(\\d+)', 'a%s0' % s)]
str2dict = lambda s: dict(re.findall('(.*?):(.*)', s))
tuple2item = lambda item: item if len(item) > 1 else item[0]
unique = lambda arr: sorted(set(arr), key=arr.index)
pc_ip = lambda : socket.gethostbyname(socket.gethostname())
pc_mac = lambda : '-'.join(re.findall('..', uuid.uuid1().hex[-12:].upper()))
pc_user = lambda : getpass.getuser()
randombytes = lambda n: bytes((random.randint(0, 255) for i in range(n)))
join = lambda *s, sp='': sp.join(s)
__all__ = [k for k in globals() if k not in __all__]