import socket
import struct
from typing import Optional
from urllib.parse import urlparse

def is_loopback(address):
    host: Optional[str] = None
    try:
        parsed_url = urlparse(address)
        host = parsed_url.hostname
    except ValueError:
        return False
    loopback_checker = {socket.AF_INET: lambda x: struct.unpack('!I', socket.inet_aton(x))[0] >> 32 - 8 == 127, socket.AF_INET6: lambda x: x == '::1'}
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            r = socket.getaddrinfo(host, None, family, socket.SOCK_STREAM)
        except socket.gaierror:
            continue
        for (family, _, _, _, sockaddr) in r:
            if loopback_checker[family](sockaddr[0]):
                return True
    if host in ('localhost',):
        return True
    return False