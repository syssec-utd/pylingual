import json
import logging
import os
import socket
import sys
from ipaddress import _BaseAddress as BaseIPAddress
from ipaddress import _BaseNetwork as BaseIPNetwork
from ipaddress import ip_address
from pathlib import Path
from typing import Awaitable, Callable, Iterable, Optional
import aiodns
import netifaces
from .utils import curl
__all__ = ('detect_cloud', 'current_provider', 'get_instance_id', 'get_instance_ip', 'get_instance_type', 'get_instance_region')
log = logging.getLogger(__name__)

def is_containerized() -> bool:
    """
    Check if I am running inside a Linux container.
    """
    try:
        cginfo = Path('/proc/self/cgroup').read_text()
        if '/docker/' in cginfo or '/lxc/' in cginfo:
            return True
        return False
    except IOError:
        return False

def detect_cloud() -> Optional[str]:
    """
    Detect the cloud provider where I am running on.
    """
    if sys.platform.startswith('linux'):
        try:
            mb = Path('/sys/devices/virtual/dmi/id/board_vendor').read_text().lower()
            if 'amazon' in mb:
                return 'amazon'
        except IOError:
            pass
        try:
            bios = Path('/sys/devices/virtual/dmi/id/bios_version').read_text().lower()
            if 'google' in bios:
                return 'google'
            if 'amazon' in bios:
                return 'amazon'
        except IOError:
            pass
        try:
            dhcp = Path('/var/lib/dhcp/dhclient.eth0.leases').read_text()
            if 'unknown-245' in dhcp:
                return 'azure'
        except IOError:
            pass
    return None

def fetch_local_ipaddrs(cidr: BaseIPNetwork) -> Iterable[BaseIPAddress]:
    ifnames = netifaces.interfaces()
    proto = netifaces.AF_INET if cidr.version == 4 else netifaces.AF_INET6
    for ifname in ifnames:
        addrs = netifaces.ifaddresses(ifname).get(proto, None)
        if addrs is None:
            continue
        for entry in addrs:
            addr = ip_address(entry['addr'])
            if addr in cidr:
                yield addr
current_provider = detect_cloud()
if current_provider is None:
    log.info('Detected environment: on-premise setup')
    log.info('The agent node ID is set using the hostname.')
else:
    log.info(f'Detected environment: {current_provider} cloud')
    log.info('The agent node ID will follow the instance ID.')
_defined: bool = False
get_instance_id: Callable[[], Awaitable[str]]
get_instance_ip: Callable[[Optional[BaseIPNetwork]], Awaitable[str]]
get_instance_type: Callable[[], Awaitable[str]]
get_instance_region: Callable[[], Awaitable[str]]

def _define_functions():
    global _defined
    global get_instance_id
    global get_instance_ip
    global get_instance_type
    global get_instance_region
    if _defined:
        return
    if current_provider == 'amazon':
        _metadata_prefix = 'http://169.254.169.254/latest/meta-data/'
        _dynamic_prefix = 'http://169.254.169.254/latest/dynamic/'

        async def _get_instance_id() -> str:
            return await curl(_metadata_prefix + 'instance-id', lambda : f'i-{socket.gethostname()}')

        async def _get_instance_ip(subnet_hint: BaseIPNetwork=None) -> str:
            return await curl(_metadata_prefix + 'local-ipv4', '127.0.0.1')

        async def _get_instance_type() -> str:
            return await curl(_metadata_prefix + 'instance-type', 'unknown')

        async def _get_instance_region() -> str:
            doc = await curl(_dynamic_prefix + 'instance-identity/document', None)
            if doc is None:
                return 'amazon/unknown'
            region = json.loads(doc)['region']
            return f'amazon/{region}'
    elif current_provider == 'azure':
        _metadata_prefix = 'http://169.254.169.254/metadata/instance'

        async def _get_instance_id() -> str:
            data = await curl(_metadata_prefix, None, params={'version': '2017-03-01'}, headers={'Metadata': 'true'})
            if data is None:
                return f'i-{socket.gethostname()}'
            o = json.loads(data)
            return o['compute']['vmId']

        async def _get_instance_ip(subnet_hint: BaseIPNetwork=None) -> str:
            data = await curl(_metadata_prefix, None, params={'version': '2017-03-01'}, headers={'Metadata': 'true'})
            if data is None:
                return '127.0.0.1'
            o = json.loads(data)
            return o['network']['interface'][0]['ipv4']['ipaddress'][0]['ipaddress']

        async def _get_instance_type() -> str:
            data = await curl(_metadata_prefix, None, params={'version': '2017-03-01'}, headers={'Metadata': 'true'})
            if data is None:
                return 'unknown'
            o = json.loads(data)
            return o['compute']['vmSize']

        async def _get_instance_region() -> str:
            data = await curl(_metadata_prefix, None, params={'version': '2017-03-01'}, headers={'Metadata': 'true'})
            if data is None:
                return 'azure/unknown'
            o = json.loads(data)
            region = o['compute']['location']
            return f'azure/{region}'
    elif current_provider == 'google':
        _metadata_prefix = 'http://metadata.google.internal/computeMetadata/v1/'

        async def _get_instance_id() -> str:
            return await curl(_metadata_prefix + 'instance/id', lambda : f'i-{socket.gethostname()}', headers={'Metadata-Flavor': 'Google'})

        async def _get_instance_ip(subnet_hint: BaseIPNetwork=None) -> str:
            return await curl(_metadata_prefix + 'instance/network-interfaces/0/ip', '127.0.0.1', headers={'Metadata-Flavor': 'Google'})

        async def _get_instance_type() -> str:
            return await curl(_metadata_prefix + 'instance/machine-type', 'unknown', headers={'Metadata-Flavor': 'Google'})

        async def _get_instance_region() -> str:
            zone = await curl(_metadata_prefix + 'instance/zone', 'unknown', headers={'Metadata-Flavor': 'Google'})
            region = zone.rsplit('-', 1)[0]
            return f'google/{region}'
    else:
        _metadata_prefix = None

        async def _get_instance_id() -> str:
            return f'i-{socket.gethostname()}'

        async def _get_instance_ip(subnet_hint: BaseIPNetwork=None) -> str:
            if subnet_hint is not None and subnet_hint.prefixlen > 0:
                local_ipaddrs = [*fetch_local_ipaddrs(subnet_hint)]
                if local_ipaddrs:
                    return str(local_ipaddrs[0])
                raise RuntimeError('Could not find my IP address bound to subnet {}', subnet_hint)
            try:
                myself = socket.gethostname()
                resolver = aiodns.DNSResolver()
                result = await resolver.gethostbyname(myself, socket.AF_INET)
                return result.addresses[0]
            except aiodns.error.DNSError:
                return '127.0.0.1'

        async def _get_instance_type() -> str:
            return 'default'

        async def _get_instance_region() -> str:
            return os.environ.get('BACKEND_REGION', 'local')
    get_instance_id = _get_instance_id
    get_instance_ip = _get_instance_ip
    get_instance_type = _get_instance_type
    get_instance_region = _get_instance_region
    _defined = True
_define_functions()