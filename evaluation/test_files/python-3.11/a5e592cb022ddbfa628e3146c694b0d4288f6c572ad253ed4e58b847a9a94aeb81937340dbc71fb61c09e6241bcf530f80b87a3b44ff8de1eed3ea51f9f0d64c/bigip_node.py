from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: bigip_node\nshort_description: Manages F5 BIG-IP LTM nodes\ndescription:\n  - Manages F5 BIG-IP LTM nodes.\nversion_added: "1.0.0"\noptions:\n  state:\n    description:\n      - Specifies the current state of the node. C(enabled) (All traffic\n        allowed), specifies the system sends traffic to this node regardless\n        of the node\'s state. C(disabled) (Only persistent or active connections\n        allowed), specifies the node can handle only persistent or\n        active connections. C(offline) (Only active connections allowed),\n        specifies the node can handle only active connections. In all\n        cases except C(absent), the node will be created if it does not yet\n        exist.\n      - Be particularly careful about changing the status of a node whose FQDN\n        cannot be resolved. These situations disable your ability to change their\n        C(state) to C(disabled) or C(offline). They will remain in an\n        *Unavailable - Enabled* state.\n    type: str\n    choices:\n      - present\n      - absent\n      - enabled\n      - disabled\n      - offline\n    default: present\n  name:\n    description:\n      - Specifies the name of the node.\n    type: str\n    required: True\n  monitors:\n    description:\n      - Specifies the health monitors the system currently uses to\n        monitor this node.\n    type: list\n    elements: str\n  address:\n    description:\n      - IP address of the node. This can be either IPv4 or IPv6. When creating a\n        new node, you must provide one of either C(address) or C(fqdn). This\n        parameter cannot be updated after it is set.\n    type: str\n    aliases:\n      - ip\n      - host\n  fqdn:\n    description:\n      - FQDN name of the node. This can be any name that is a valid RFC 1123 DNS\n        name. Therefore, the only characters that can be used are "A" to "Z",\n        "a" to "z", "0" to "9", the hyphen ("-") and the period (".").\n      - FQDN names must include at least one period; delineating the host from\n        the domain. For example, C(host.domain).\n      - FQDN names must end with a letter or a number.\n      - When creating a new node, you must provide one of either C(address) or C(fqdn) provided.\n        This parameter cannot be updated after it is set.\n    type: str\n    aliases:\n      - hostname\n  fqdn_address_type:\n    description:\n      - Specifies whether the FQDN of the node resolves to an IPv4 or IPv6 address.\n      - When creating a new node, if this parameter is not specified and C(fqdn) is\n        specified, this parameter will default to C(ipv4).\n      - This parameter cannot be changed after it has been set.\n    type: str\n    choices:\n      - ipv4\n      - ipv6\n      - all\n  fqdn_auto_populate:\n    description:\n      - Specifies whether the system automatically creates ephemeral nodes using\n        the IP addresses returned by the resolution of a DNS query for a node defined\n        by an FQDN.\n      - When C(yes), the system generates an ephemeral node for each IP address\n        returned in response to a DNS query for the FQDN of the node. Additionally,\n        when a DNS response indicates the IP address of an ephemeral node no longer\n        exists, the system deletes the ephemeral node.\n      - When C(no), the system resolves a DNS query for the FQDN of the node with the\n        single IP address associated with the FQDN.\n      - When creating a new node, if this parameter is not specified and C(fqdn) is\n        specified, this parameter will default to C(yes).\n      - This parameter cannot be changed after it has been set.\n    type: bool\n  fqdn_up_interval:\n    description:\n      - Specifies the interval at which a query occurs, when the DNS server is up.\n        The associated monitor attempts to probe three times, and marks the server\n        down if it there is no response within the span of three times the interval\n        value, in seconds.\n      - This parameter accepts a value of C(ttl) to query, based off of the TTL of\n        the FQDN. The default TTL interval is similar to specifying C(3600).\n      - When creating a new node, if this parameter is not specified and C(fqdn) is\n        specified, this parameter will default to C(3600).\n    type: str\n  fqdn_down_interval:\n    description:\n      - Specifies the interval in which a query occurs, when the DNS server is down.\n        The associated monitor continues polling as long as the DNS server is down.\n      - When creating a new node, if this parameter is not specified and C(fqdn) is\n        specified, this parameter will default to C(5).\n    type: int\n  description:\n    description:\n      - Specifies descriptive text that identifies the node.\n      - You can remove a description by either specifying an empty string, or by\n        specifying the special value C(none).\n    type: str\n  connection_limit:\n    description:\n      - Node connection limit. Setting this to C(0) disables the limit.\n    type: int\n  rate_limit:\n    description:\n      - Node rate limit (connections-per-second). Setting this to C(0) disables the limit.\n    type: int\n  ratio:\n    description:\n      - Node ratio weight. Valid values range from 1 through 100.\n      - When creating a new node, if this parameter is not specified, the default of\n        C(1) will be used.\n    type: int\n  dynamic_ratio:\n    description:\n      - The dynamic ratio number for the node. Used for dynamic ratio load balancing.\n      - When creating a new node, if this parameter is not specified, the default of\n        C(1) will be used.\n    type: int\n  availability_requirements:\n    description:\n      - If you activate more than one health monitor, specifies the number of health\n        monitors that must receive successful responses in order for the link to be\n        considered available.\n    type: dict\n    suboptions:\n      type:\n        description:\n          - Monitor rule type when C(monitors) is specified.\n          - When creating a new pool, if this value is not specified, the default of\n            \'all\' will be used.\n        type: str\n        required: True\n        choices:\n          - all\n          - at_least\n      at_least:\n        description:\n          - Specifies the minimum number of active health monitors that must be successful\n            before the link is considered up.\n          - This parameter is only relevant when a C(type) of C(at_least) is used.\n          - This parameter will be ignored if a type of C(all) is used.\n        type: int\n  partition:\n    description:\n      - Device partition to manage resources on.\n    type: str\n    default: Common\nextends_documentation_fragment: f5networks.f5_modules.f5\nauthor:\n  - Tim Rupp (@caphrim007)\n  - Wojciech Wypior (@wojtek0806)\n'
EXAMPLES = "\n- name: Add node\n  bigip_node:\n    host: 10.20.30.40\n    name: 10.20.30.40\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n\n- name: Add node with a single 'ping' monitor\n  bigip_node:\n    host: 10.20.30.40\n    name: mytestserver\n    monitors:\n      - /Common/icmp\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n\n- name: Modify node description\n  bigip_node:\n    name: 10.20.30.40\n    description: Our best server yet\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n\n- name: Delete node\n  bigip_node:\n    state: absent\n    name: 10.20.30.40\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n\n- name: Force node offline\n  bigip_node:\n    state: disabled\n    name: 10.20.30.40\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n\n- name: Add node by their FQDN\n  bigip_node:\n    fqdn: foo.bar.com\n    name: foobar.net\n    provider:\n      server: lb.mydomain.com\n      user: admin\n      password: secret\n  delegate_to: localhost\n"
RETURN = "\nmonitors:\n  description:\n    - Changed list of monitors for the node.\n  returned: changed and success\n  type: list\n  sample: ['icmp', 'tcp_echo']\ndescription:\n  description:\n    - Changed value for the description of the node.\n  returned: changed and success\n  type: str\n  sample: E-Commerce webserver in ORD\nsession:\n  description:\n    - Changed value for the internal session of the node.\n  returned: changed and success\n  type: str\n  sample: user-disabled\nstate:\n  description:\n    - Changed value for the internal state of the node.\n  returned: changed and success\n  type: str\n  sample: user-down\n"
import re
import time
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE, BOOLEANS_TRUE
from ..module_utils.bigip import F5RestClient
from ..module_utils.common import F5ModuleError, AnsibleF5Parameters, transform_name, f5_argument_spec, fq_name
from ..module_utils.icontrol import tmos_version
from ..module_utils.teem import send_teem

class Parameters(AnsibleF5Parameters):
    api_map = {'monitor': 'monitors', 'connectionLimit': 'connection_limit', 'rateLimit': 'rate_limit'}
    api_attributes = ['description', 'address', 'fqdn', 'ratio', 'connectionLimit', 'rateLimit', 'monitor', 'session', 'state']
    returnables = ['monitors', 'description', 'fqdn', 'address', 'session', 'state', 'fqdn_auto_populate', 'fqdn_address_type', 'fqdn_up_interval', 'fqdn_down_interval', 'fqdn_name', 'connection_limit', 'ratio', 'rate_limit', 'availability_requirements']
    updatables = ['monitors', 'description', 'state', 'fqdn_up_interval', 'fqdn_down_interval', 'tmName', 'fqdn_auto_populate', 'fqdn_address_type', 'connection_limit', 'ratio', 'rate_limit']

    def to_return(self):
        result = {}
        try:
            for returnable in self.returnables:
                result[returnable] = getattr(self, returnable)
            result = self._filter_params(result)
            return result
        except Exception:
            return result

    @property
    def rate_limit(self):
        if self._values['rate_limit'] is None:
            return None
        if self._values['rate_limit'] == 'disabled':
            return 0
        return int(self._values['rate_limit'])

class Changes(Parameters):
    pass

class UsableChanges(Changes):

    @property
    def fqdn(self):
        result = dict()
        if self._values['fqdn_up_interval'] is not None:
            result['interval'] = self._values['fqdn_up_interval']
        if self._values['fqdn_down_interval'] is not None:
            result['downInterval'] = self._values['fqdn_down_interval']
        if self._values['fqdn_auto_populate'] is not None:
            result['autopopulate'] = self._values['fqdn_auto_populate']
        if self._values['fqdn_name'] is not None:
            result['tmName'] = self._values['fqdn_name']
        if self._values['fqdn_address_type'] is not None:
            result['addressFamily'] = self._values['fqdn_address_type']
        if not result:
            return None
        return result

    @property
    def monitors(self):
        monitor_string = self._values['monitors']
        if monitor_string is None:
            return None
        if '{' in monitor_string and '}' in monitor_string:
            tmp = monitor_string.strip('}').split('{')
            monitor = ''.join(tmp).rstrip()
            return monitor
        return monitor_string

class ReportableChanges(Changes):

    @property
    def monitors(self):
        if self._values['monitors'] is None:
            return []
        try:
            result = re.findall('/\\w+/[^\\s}]+', self._values['monitors'])
            result.sort()
            return result
        except Exception:
            return self._values['monitors']

    @property
    def availability_requirement_type(self):
        if self._values['monitors'] is None:
            return None
        if 'min ' in self._values['monitors']:
            return 'at_least'
        else:
            return 'all'

    @property
    def at_least(self):
        """Returns the 'at least' value from the monitor string.
        The monitor string for a Require monitor looks like this.
            min 1 of { /Common/gateway_icmp }
        This method parses out the first of the numeric values. This values represents
        the "at_least" value that can be updated in the module.
        Returns:
             int: The at_least value if found. None otherwise.
        """
        if self._values['monitors'] is None:
            return None
        pattern = 'min\\s+(?P<least>\\d+)\\s+of\\s+'
        matches = re.search(pattern, self._values['monitors'])
        if matches is None:
            return None
        return int(matches.group('least'))

    @property
    def availability_requirements(self):
        if self._values['monitors'] is None:
            return None
        result = dict()
        result['type'] = self.availability_requirement_type
        result['at_least'] = self.at_least
        return result

class ModuleParameters(Parameters):

    def _get_availability_value(self, type):
        if self._values['availability_requirements'] is None:
            return None
        if self._values['availability_requirements'][type] is None:
            return None
        return self._values['availability_requirements'][type]

    @property
    def monitors_list(self):
        if self._values['monitors'] is None:
            return []
        try:
            result = re.findall('/\\w+/[^\\s}]+', self._values['monitors'])
        except Exception:
            result = self._values['monitors']
        result.sort()
        return result

    @property
    def monitors(self):
        if self._values['monitors'] is None:
            return None
        if self._values['monitors'] == 'default':
            return 'default'
        if len(self._values['monitors']) == 1 and self._values['monitors'][0] == '':
            return '/Common/none'
        monitors = [fq_name(self.partition, x) for x in self.monitors_list]
        if len(self.monitors_list) > 1:
            if self.availability_requirement_type == 'at_least':
                if self.at_least > len(self.monitors_list):
                    raise F5ModuleError("The 'at_least' value must not exceed the number of 'monitors'.")
                monitors = ' '.join(monitors)
                result = 'min {0} of {{ {1} }}'.format(self.at_least, monitors)
            else:
                result = ' and '.join(monitors).strip()
            return result
        if len(self.monitors_list) == 1:
            return monitors[0]

    @property
    def availability_requirement_type(self):
        if self._values['availability_requirements'] is None:
            return None
        return self._values['availability_requirements']['type']

    @property
    def at_least(self):
        return self._get_availability_value('at_least')

    @property
    def fqdn_up_interval(self):
        if self._values['fqdn_up_interval'] is None:
            return None
        return str(self._values['fqdn_up_interval'])

    @property
    def fqdn_down_interval(self):
        if self._values['fqdn_down_interval'] is None:
            return None
        return str(self._values['fqdn_down_interval'])

    @property
    def fqdn_auto_populate(self):
        auto_populate = self._values.get('fqdn_auto_populate', None)
        if auto_populate in BOOLEANS_TRUE:
            return 'enabled'
        elif auto_populate in BOOLEANS_FALSE:
            return 'disabled'

    @property
    def fqdn_name(self):
        return self._values.get('fqdn', None)

    @property
    def fqdn(self):
        if self._values['fqdn'] is None:
            return None
        result = dict(addressFamily=self._values.get('fqdn_address_type', None), downInterval=self._values.get('fqdn_down_interval', None), interval=self._values.get('fqdn_up_interval', None), autopopulate=None, tmName=self._values.get('fqdn', None))
        auto_populate = self._values.get('fqdn_auto_populate', None)
        if auto_populate in BOOLEANS_TRUE:
            result['autopopulate'] = 'enabled'
        elif auto_populate in BOOLEANS_FALSE:
            result['autopopulate'] = 'disabled'
        return result

    @property
    def description(self):
        if self._values['description'] is None:
            return None
        elif self._values['description'] in ['none', '']:
            return ''
        return self._values['description']

class ApiParameters(Parameters):

    @property
    def fqdn_up_interval(self):
        if self._values['fqdn'] is None:
            return None
        if 'interval' in self._values['fqdn']:
            return str(self._values['fqdn']['interval'])

    @property
    def fqdn_down_interval(self):
        if self._values['fqdn'] is None:
            return None
        if 'downInterval' in self._values['fqdn']:
            return str(self._values['fqdn']['downInterval'])

    @property
    def fqdn_address_type(self):
        if self._values['fqdn'] is None:
            return None
        if 'addressFamily' in self._values['fqdn']:
            return str(self._values['fqdn']['addressFamily'])

    @property
    def fqdn_auto_populate(self):
        if self._values['fqdn'] is None:
            return None
        if 'autopopulate' in self._values['fqdn']:
            return str(self._values['fqdn']['autopopulate'])

    @property
    def description(self):
        if self._values['description'] in [None, 'none']:
            return None
        return self._values['description']

    @property
    def availability_requirement_type(self):
        if self._values['monitors'] is None:
            return None
        if 'min ' in self._values['monitors']:
            return 'at_least'
        else:
            return 'all'

    @property
    def monitors_list(self):
        if self._values['monitors'] is None:
            return []
        try:
            result = re.findall('/\\w+/[^\\s}]+', self._values['monitors'])
        except Exception:
            result = self._values['monitors']
        result.sort()
        return result

    @property
    def monitors(self):
        if self._values['monitors'] is None:
            return None
        if self._values['monitors'] == 'default':
            return 'default'
        monitors = [fq_name(self.partition, x) for x in self.monitors_list]
        if len(self.monitors_list) > 1:
            if self.availability_requirement_type == 'at_least':
                monitors = ' '.join(monitors)
                result = 'min {0} of {{ {1} }}'.format(self.at_least, monitors)
            else:
                result = ' and '.join(monitors).strip()
            return result
        if len(self.monitors_list) == 1:
            return monitors[0]

    @property
    def at_least(self):
        """Returns the 'at least' value from the monitor string.

        The monitor string for a Require monitor looks like this.

            min 1 of { /Common/gateway_icmp }

        This method parses out the first of the numeric values. This values represents
        the "at_least" value that can be updated in the module.

        Returns:
             int: The at_least value if found. None otherwise.
        """
        if self._values['monitors'] is None:
            return None
        pattern = 'min\\s+(?P<least>\\d+)\\s+of\\s+'
        matches = re.search(pattern, self._values['monitors'])
        if matches is None:
            return None
        return matches.group('least')

class Difference(object):

    def __init__(self, want, have=None):
        self.want = want
        self.have = have

    def compare(self, param):
        try:
            result = getattr(self, param)
            return result
        except AttributeError:
            return self.__default(param)

    def __default(self, param):
        attr1 = getattr(self.want, param)
        try:
            attr2 = getattr(self.have, param)
            if attr1 != attr2:
                return attr1
        except AttributeError:
            return attr1

    @property
    def monitors(self):
        if self.want.monitors is None:
            return None
        if self.want.monitors == 'default' and self.have.monitors == 'default':
            return None
        if self.want.monitors == 'default' and self.have.monitors is None:
            return None
        if self.want.monitors == '/Common/none' and self.have.monitors == '/Common/none':
            return None
        if self.want.monitors == 'default' and len(self.have.monitors) > 0:
            return 'default'
        if self.have.monitors is None:
            return self.want.monitors
        if self.have.monitors != self.want.monitors:
            return self.want.monitors

    @property
    def state(self):
        result = None
        if self.want.state in ['present', 'enabled']:
            if self.have.session not in ['user-enabled', 'monitor-enabled']:
                result = dict(session='user-enabled', state='user-up')
        elif self.want.state == 'disabled':
            if self.have.session != 'user-disabled' or self.have.state == 'user-down':
                result = dict(session='user-disabled', state='user-up')
        elif self.want.state == 'offline':
            if self.have.state != 'user-down':
                result = dict(session='user-disabled', state='user-down')
        return result

    @property
    def description(self):
        if self.want.description is None:
            return None
        if self.have.description is None and self.want.description == '':
            return None
        if self.want.description != self.have.description:
            return self.want.description

class ModuleManager(object):

    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = F5RestClient(**self.module.params)
        self.have = None
        self.want = ModuleParameters(params=self.module.params)
        self.changes = UsableChanges()

    def _set_changed_options(self):
        changed = {}
        for key in Parameters.returnables:
            if getattr(self.want, key) is not None:
                changed[key] = getattr(self.want, key)
        if changed:
            self.changes = UsableChanges(params=changed)

    def _update_changed_options(self):
        diff = Difference(self.want, self.have)
        updatables = Parameters.updatables
        changed = dict()
        for k in updatables:
            change = diff.compare(k)
            if change is None:
                continue
            elif isinstance(change, dict):
                changed.update(change)
            else:
                changed[k] = change
        if changed:
            self.changes = UsableChanges(params=changed)
            return True
        return False

    def _announce_deprecations(self):
        warnings = []
        if self.want:
            warnings += self.want._values.get('__warnings', [])
        if self.have:
            warnings += self.have._values.get('__warnings', [])
        for warning in warnings:
            self.module.deprecate(msg=warning['msg'], version=warning['version'])

    def exec_module(self):
        start = datetime.now().isoformat()
        version = tmos_version(self.client)
        changed = False
        result = dict()
        state = self.want.state
        try:
            if state in ['present', 'enabled', 'disabled', 'offline']:
                changed = self.present()
            elif state == 'absent':
                changed = self.absent()
        except IOError as e:
            raise F5ModuleError(str(e))
        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        self._announce_deprecations()
        send_teem(start, self.client, self.module, version)
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def _check_required_creation_vars(self):
        if self.want.address is None and self.want.fqdn is None:
            raise F5ModuleError("At least one of 'address' or 'fqdn' is required when creating a node")
        elif self.want.address is not None and self.want.fqdn is not None:
            raise F5ModuleError("Only one of 'address' or 'fqdn' can be provided when creating a node")
        elif self.want.fqdn is not None:
            self.want.update(dict(address='any6'))

    def _munge_creation_state_for_device(self):
        if self.want.state in ['present', 'enabled']:
            self.want.update(dict(session='user-enabled', state='user-up'))
        elif self.want.state in 'disabled':
            self.want.update(dict(session='user-disabled', state='user-up'))
        else:
            self.want.update(dict(session='user-disabled', state='user-down', is_offline=True))

    def create(self):
        self._check_required_creation_vars()
        self._munge_creation_state_for_device()
        if self.want.fqdn_name:
            if self.want.fqdn_auto_populate is None:
                self.want.update({'fqdn_auto_populate': True})
            if self.want.fqdn_address_type is None:
                self.want.update({'fqdn_address_type': 'ipv4'})
            if self.want.fqdn_up_interval is None:
                self.want.update({'fqdn_up_interval': 3600})
            if self.want.fqdn_down_interval is None:
                self.want.update({'fqdn_down_interval': 5})
        if self.want.ratio is None:
            self.want.update({'ratio': 1})
        if self.want.dynamic_ratio is None:
            self.want.update({'dynamic_ratio': 1})
        self._set_changed_options()
        if self.module.check_mode:
            return True
        if self.want.address:
            self.changes.update({'address': self.want.address})
        if self.want.fqdn_up_interval is not None:
            self.changes.update({'fqdn_up_interval': self.want.fqdn_up_interval})
        if self.want.fqdn_down_interval is not None:
            self.changes.update({'fqdn_down_interval': self.want.fqdn_down_interval})
        if self.want.fqdn_auto_populate is not None:
            self.changes.update({'fqdn_auto_populate': self.want.fqdn_auto_populate})
        if self.want.fqdn_name is not None:
            self.changes.update({'fqdn_name': self.want.fqdn_name})
        if self.want.fqdn_address_type is not None:
            self.changes.update({'fqdn_address_type': self.want.fqdn_address_type})
        self.create_on_device()
        if not self.exists():
            raise F5ModuleError('Failed to create the node')
        if self.want.is_offline:
            self.update_node_offline_on_device()
        return True

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def update(self):
        self.have = self.read_current_from_device()
        if not self.should_update():
            return False
        if self.want.fqdn_auto_populate is not None:
            if self.want.fqdn_auto_populate != self.have.fqdn_auto_populate:
                raise F5ModuleError("The 'fqdn_auto_populate' parameter cannot be changed.")
        if self.want.fqdn_address_type is not None:
            if self.want.fqdn_address_type != self.have.fqdn_address_type:
                raise F5ModuleError("The 'fqdn_address_type' parameter cannot be changed.")
        if self.module.check_mode:
            return True
        self.update_on_device()
        if self.want.state == 'offline':
            self.update_node_offline_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError('Failed to delete the node.')
        return True

    def read_current_from_device(self):
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.name))
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status in [200, 201] or ('code' in response and response['code'] in [200, 201]):
            return ApiParameters(params=response)
        raise F5ModuleError(resp.content)

    def exists(self):
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.name))
        resp = self.client.api.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status == 404 or ('code' in response and response['code'] == 404):
            return False
        if resp.status in [200, 201] or ('code' in response and response['code'] in [200, 201]):
            return True
        errors = [401, 403, 409, 500, 501, 502, 503, 504]
        if resp.status in errors or ('code' in response and response['code'] in errors):
            if 'message' in response:
                raise F5ModuleError(response['message'])
            else:
                raise F5ModuleError(resp.content)

    def update_node_offline_on_device(self):
        params = dict(session='user-disabled', state='user-down')
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.name))
        resp = self.client.api.patch(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status in [200, 201] or ('code' in response and response['code'] in [200, 201]):
            return True
        raise F5ModuleError(resp.content)

    def update_on_device(self):
        params = self.changes.api_params()
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.name))
        if params:
            resp = self.client.api.patch(uri, json=params)
            try:
                response = resp.json()
            except ValueError as ex:
                raise F5ModuleError(str(ex))
            if resp.status in [200, 201] or ('code' in response and response['code'] in [200, 201]):
                return True
            raise F5ModuleError(resp.content)

    def create_on_device(self):
        params = self.changes.api_params()
        params['name'] = self.want.name
        params['partition'] = self.want.partition
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/'.format(self.client.provider['server'], self.client.provider['server_port'])
        resp = self.client.api.post(uri, json=params)
        try:
            response = resp.json()
        except ValueError as ex:
            raise F5ModuleError(str(ex))
        if resp.status in [200, 201] or ('code' in response and response['code'] in [200, 201]):
            self._wait_for_fqdn_checks()
            return True
        raise F5ModuleError(resp.content)

    def _wait_for_fqdn_checks(self):
        while True:
            have = self.read_current_from_device()
            if have.state == 'fqdn-checking':
                time.sleep(1)
            else:
                break

    def remove_from_device(self):
        uri = 'https://{0}:{1}/mgmt/tm/ltm/node/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.name))
        resp = self.client.api.delete(uri)
        if resp.status == 200:
            return True

class ArgumentSpec(object):

    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(name=dict(required=True), address=dict(aliases=['host', 'ip']), fqdn=dict(aliases=['hostname']), description=dict(), state=dict(choices=['absent', 'present', 'enabled', 'disabled', 'offline'], default='present'), partition=dict(default='Common', fallback=(env_fallback, ['F5_PARTITION'])), fqdn_address_type=dict(choices=['ipv4', 'ipv6', 'all']), fqdn_auto_populate=dict(type='bool'), fqdn_up_interval=dict(), fqdn_down_interval=dict(type='int'), connection_limit=dict(type='int'), rate_limit=dict(type='int'), ratio=dict(type='int'), dynamic_ratio=dict(type='int'), availability_requirements=dict(type='dict', options=dict(type=dict(choices=['all', 'at_least'], required=True), at_least=dict(type='int')), required_if=[['type', 'at_least', ['at_least']]]), monitors=dict(type='list', elements='str'))
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)

def main():
    spec = ArgumentSpec()
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)
    try:
        mm = ModuleManager(module=module)
        results = mm.exec_module()
        module.exit_json(**results)
    except F5ModuleError as ex:
        module.fail_json(msg=str(ex))
if __name__ == '__main__':
    main()