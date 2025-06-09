from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n    name: proxmox\n    short_description: Proxmox inventory source\n    version_added: "1.2.0"\n    author:\n        - Jeffrey van Pelt (@Thulium-Drake) <jeff@vanpelt.one>\n    requirements:\n        - requests >= 1.1\n    description:\n        - Get inventory hosts from a Proxmox PVE cluster.\n        - "Uses a configuration file as an inventory source, it must end in C(.proxmox.yml) or C(.proxmox.yaml)"\n        - Will retrieve the first network interface with an IP for Proxmox nodes.\n        - Can retrieve LXC/QEMU configuration as facts.\n    extends_documentation_fragment:\n        - constructed\n        - inventory_cache\n    options:\n      plugin:\n        description: The name of this plugin, it should always be set to C(community.general.proxmox) for this plugin to recognize it as it\'s own.\n        required: true\n        choices: [\'community.general.proxmox\']\n        type: str\n      url:\n        description:\n          - URL to Proxmox cluster.\n          - If the value is not specified in the inventory configuration, the value of environment variable C(PROXMOX_URL) will be used instead.\n          - Since community.general 4.7.0 you can also use templating to specify the value of the I(url).\n        default: \'http://localhost:8006\'\n        type: str\n        env:\n          - name: PROXMOX_URL\n            version_added: 2.0.0\n      user:\n        description:\n          - Proxmox authentication user.\n          - If the value is not specified in the inventory configuration, the value of environment variable C(PROXMOX_USER) will be used instead.\n          - Since community.general 4.7.0 you can also use templating to specify the value of the I(user).\n        required: true\n        type: str\n        env:\n          - name: PROXMOX_USER\n            version_added: 2.0.0\n      password:\n        description:\n          - Proxmox authentication password.\n          - If the value is not specified in the inventory configuration, the value of environment variable C(PROXMOX_PASSWORD) will be used instead.\n          - Since community.general 4.7.0 you can also use templating to specify the value of the I(password).\n          - If you do not specify a password, you must set I(token_id) and I(token_secret) instead.\n        type: str\n        env:\n          - name: PROXMOX_PASSWORD\n            version_added: 2.0.0\n      token_id:\n        description:\n          - Proxmox authentication token ID.\n          - If the value is not specified in the inventory configuration, the value of environment variable C(PROXMOX_TOKEN_ID) will be used instead.\n          - To use token authentication, you must also specify I(token_secret). If you do not specify I(token_id) and I(token_secret),\n            you must set a password instead.\n          - Make sure to grant explicit pve permissions to the token or disable \'privilege separation\' to use the users\' privileges instead.\n        version_added: 4.8.0\n        type: str\n        env:\n          - name: PROXMOX_TOKEN_ID\n      token_secret:\n        description:\n          - Proxmox authentication token secret.\n          - If the value is not specified in the inventory configuration, the value of environment variable C(PROXMOX_TOKEN_SECRET) will be used instead.\n          - To use token authentication, you must also specify I(token_id). If you do not specify I(token_id) and I(token_secret),\n            you must set a password instead.\n        version_added: 4.8.0\n        type: str\n        env:\n          - name: PROXMOX_TOKEN_SECRET\n      validate_certs:\n        description: Verify SSL certificate if using HTTPS.\n        type: boolean\n        default: true\n      group_prefix:\n        description: Prefix to apply to Proxmox groups.\n        default: proxmox_\n        type: str\n      facts_prefix:\n        description: Prefix to apply to LXC/QEMU config facts.\n        default: proxmox_\n        type: str\n      want_facts:\n        description:\n          - Gather LXC/QEMU configuration facts.\n          - When I(want_facts) is set to C(true) more details about QEMU VM status are possible, besides the running and stopped states.\n            Currently if the VM is running and it is suspended, the status will be running and the machine will be in C(running) group,\n            but its actual state will be paused. See I(qemu_extended_statuses) for how to retrieve the real status.\n        default: false\n        type: bool\n      qemu_extended_statuses:\n        description:\n          - Requires I(want_facts) to be set to C(true) to function. This will allow you to differentiate betweend C(paused) and C(prelaunch)\n            statuses of the QEMU VMs.\n          - This introduces multiple groups [prefixed with I(group_prefix)] C(prelaunch) and C(paused).\n        default: false\n        type: bool\n        version_added: 5.1.0\n      want_proxmox_nodes_ansible_host:\n        version_added: 3.0.0\n        description:\n          - Whether to set C(ansbile_host) for proxmox nodes.\n          - When set to C(true) (default), will use the first available interface. This can be different from what you expect.\n          - The default of this option changed from C(true) to C(false) in community.general 6.0.0.\n        type: bool\n        default: false\n      filters:\n        version_added: 4.6.0\n        description: A list of Jinja templates that allow filtering hosts.\n        type: list\n        elements: str\n        default: []\n      strict:\n        version_added: 2.5.0\n      compose:\n        version_added: 2.5.0\n      groups:\n        version_added: 2.5.0\n      keyed_groups:\n        version_added: 2.5.0\n'
EXAMPLES = '\n# Minimal example which will not gather additional facts for QEMU/LXC guests\n# By not specifying a URL the plugin will attempt to connect to the controller host on port 8006\n# my.proxmox.yml\nplugin: community.general.proxmox\nuser: ansible@pve\npassword: secure\n# Note that this can easily give you wrong values as ansible_host. See further below for\n# an example where this is set to `false` and where ansible_host is set with `compose`.\nwant_proxmox_nodes_ansible_host: true\n\n# Instead of login with password, proxmox supports api token authentication since release 6.2.\nplugin: community.general.proxmox\nuser: ci@pve\ntoken_id: gitlab-1\ntoken_secret: fa256e9c-26ab-41ec-82da-707a2c079829\n\n# The secret can also be a vault string or passed via the environment variable TOKEN_SECRET.\ntoken_secret: !vault |\n          $ANSIBLE_VAULT;1.1;AES256\n          62353634333163633336343265623632626339313032653563653165313262343931643431656138\n          6134333736323265656466646539663134306166666237630a653363623262636663333762316136\n          34616361326263383766366663393837626437316462313332663736623066656237386531663731\n          3037646432383064630a663165303564623338666131353366373630656661333437393937343331\n          32643131386134396336623736393634373936356332623632306561356361323737313663633633\n          6231313333666361656537343562333337323030623732323833\n\n# More complete example demonstrating the use of \'want_facts\' and the constructed options\n# Note that using facts returned by \'want_facts\' in constructed options requires \'want_facts=true\'\n# my.proxmox.yml\nplugin: community.general.proxmox\nurl: http://pve.domain.com:8006\nuser: ansible@pve\npassword: secure\nvalidate_certs: false\nwant_facts: true\nkeyed_groups:\n    # proxmox_tags_parsed is an example of a fact only returned when \'want_facts=true\'\n  - key: proxmox_tags_parsed\n    separator: ""\n    prefix: group\ngroups:\n  webservers: "\'web\' in (proxmox_tags_parsed|list)"\n  mailservers: "\'mail\' in (proxmox_tags_parsed|list)"\ncompose:\n  ansible_port: 2222\n# Note that this can easily give you wrong values as ansible_host. See further below for\n# an example where this is set to `false` and where ansible_host is set with `compose`.\nwant_proxmox_nodes_ansible_host: true\n\n# Using the inventory to allow ansible to connect via the first IP address of the VM / Container\n# (Default is connection by name of QEMU/LXC guests)\n# Note: my_inv_var demonstrates how to add a string variable to every host used by the inventory.\n# my.proxmox.yml\nplugin: community.general.proxmox\nurl: http://pve.domain.com:8006\nuser: ansible@pve\npassword: secure\nvalidate_certs: false\nwant_facts: true\nwant_proxmox_nodes_ansible_host: false\ncompose:\n  ansible_host: proxmox_ipconfig0.ip | default(proxmox_net0.ip) | ipaddr(\'address\')\n  my_inv_var_1: "\'my_var1_value\'"\n  my_inv_var_2: >\n    "my_var_2_value"\n\n# Specify the url, user and password using templating\n# my.proxmox.yml\nplugin: community.general.proxmox\nurl: "{{ lookup(\'ansible.builtin.ini\', \'url\', section=\'proxmox\', file=\'file.ini\') }}"\nuser: "{{ lookup(\'ansible.builtin.env\',\'PM_USER\') | default(\'ansible@pve\') }}"\npassword: "{{ lookup(\'community.general.random_string\', base64=True) }}"\n# Note that this can easily give you wrong values as ansible_host. See further up for\n# an example where this is set to `false` and where ansible_host is set with `compose`.\nwant_proxmox_nodes_ansible_host: true\n\n'
import itertools
import re
from ansible.module_utils.common._collections_compat import MutableMapping
from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.six import string_types
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.utils.display import Display
from ansible_collections.community.general.plugins.module_utils.version import LooseVersion
try:
    import requests
    if LooseVersion(requests.__version__) < LooseVersion('1.1.0'):
        raise ImportError
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
display = Display()

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    """ Host inventory parser for ansible using Proxmox as source. """
    NAME = 'community.general.proxmox'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.proxmox_url = None
        self.session = None
        self.cache_key = None
        self.use_cache = None

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('proxmox.yaml', 'proxmox.yml')):
                valid = True
            else:
                self.display.vvv('Skipping due to inventory source not ending in "proxmox.yaml" nor "proxmox.yml"')
        return valid

    def _get_session(self):
        if not self.session:
            self.session = requests.session()
            self.session.verify = self.get_option('validate_certs')
        return self.session

    def _get_auth(self):
        credentials = urlencode({'username': self.proxmox_user, 'password': self.proxmox_password})
        if self.proxmox_password:
            credentials = urlencode({'username': self.proxmox_user, 'password': self.proxmox_password})
            a = self._get_session()
            if a.verify is False:
                from requests.packages.urllib3 import disable_warnings
                disable_warnings()
            ret = a.post('%s/api2/json/access/ticket' % self.proxmox_url, data=credentials)
            json = ret.json()
            self.headers = {'Cookie': 'PVEAuthCookie={0}'.format(json['data']['ticket'])}
        else:
            self.headers = {'Authorization': 'PVEAPIToken={0}!{1}={2}'.format(self.proxmox_user, self.proxmox_token_id, self.proxmox_token_secret)}

    def _get_json(self, url, ignore_errors=None):
        if not self.use_cache or url not in self._cache.get(self.cache_key, {}):
            if self.cache_key not in self._cache:
                self._cache[self.cache_key] = {'url': ''}
            data = []
            s = self._get_session()
            while True:
                ret = s.get(url, headers=self.headers)
                if ignore_errors and ret.status_code in ignore_errors:
                    break
                ret.raise_for_status()
                json = ret.json()
                if 'data' not in json:
                    data = json
                    break
                elif isinstance(json['data'], MutableMapping):
                    data = json['data']
                    break
                else:
                    data = data + json['data']
                    break
            self._cache[self.cache_key][url] = data
        return self._cache[self.cache_key][url]

    def _get_nodes(self):
        return self._get_json('%s/api2/json/nodes' % self.proxmox_url)

    def _get_pools(self):
        return self._get_json('%s/api2/json/pools' % self.proxmox_url)

    def _get_lxc_per_node(self, node):
        return self._get_json('%s/api2/json/nodes/%s/lxc' % (self.proxmox_url, node))

    def _get_qemu_per_node(self, node):
        return self._get_json('%s/api2/json/nodes/%s/qemu' % (self.proxmox_url, node))

    def _get_members_per_pool(self, pool):
        ret = self._get_json('%s/api2/json/pools/%s' % (self.proxmox_url, pool))
        return ret['members']

    def _get_node_ip(self, node):
        ret = self._get_json('%s/api2/json/nodes/%s/network' % (self.proxmox_url, node))
        for iface in ret:
            try:
                return iface['address']
            except Exception:
                return None

    def _get_agent_network_interfaces(self, node, vmid, vmtype):
        result = []
        try:
            ifaces = self._get_json('%s/api2/json/nodes/%s/%s/%s/agent/network-get-interfaces' % (self.proxmox_url, node, vmtype, vmid))['result']
            if 'error' in ifaces:
                if 'class' in ifaces['error']:
                    errorClass = ifaces['error']['class']
                    if errorClass in ['Unsupported']:
                        self.display.v('Retrieving network interfaces from guest agents on windows with older qemu-guest-agents is not supported')
                    elif errorClass in ['CommandDisabled']:
                        self.display.v('Retrieving network interfaces from guest agents has been disabled')
                return result
            for iface in ifaces:
                result.append({'name': iface['name'], 'mac-address': iface['hardware-address'] if 'hardware-address' in iface else '', 'ip-addresses': ['%s/%s' % (ip['ip-address'], ip['prefix']) for ip in iface['ip-addresses']] if 'ip-addresses' in iface else []})
        except requests.HTTPError:
            pass
        return result

    def _get_vm_config(self, properties, node, vmid, vmtype, name):
        ret = self._get_json('%s/api2/json/nodes/%s/%s/%s/config' % (self.proxmox_url, node, vmtype, vmid))
        properties[self._fact('node')] = node
        properties[self._fact('vmid')] = vmid
        properties[self._fact('vmtype')] = vmtype
        plaintext_configs = ['description']
        for config in ret:
            key = self._fact(config)
            value = ret[config]
            try:
                if config == 'rootfs' or config.startswith(('virtio', 'sata', 'ide', 'scsi')):
                    value = 'disk_image=' + value
                if config == 'tags':
                    stripped_value = value.strip()
                    if stripped_value:
                        parsed_key = key + '_parsed'
                        properties[parsed_key] = [tag.strip() for tag in stripped_value.replace(',', ';').split(';')]
                if config == 'agent':
                    agent_enabled = 0
                    try:
                        agent_enabled = int(value.split(',')[0])
                    except ValueError:
                        if value.split(',')[0] == 'enabled=1':
                            agent_enabled = 1
                    if agent_enabled:
                        agent_iface_value = self._get_agent_network_interfaces(node, vmid, vmtype)
                        if agent_iface_value:
                            agent_iface_key = self.to_safe('%s%s' % (key, '_interfaces'))
                            properties[agent_iface_key] = agent_iface_value
                if config == 'lxc':
                    out_val = {}
                    for (k, v) in value:
                        if k.startswith('lxc.'):
                            k = k[len('lxc.'):]
                        out_val[k] = v
                    value = out_val
                if config not in plaintext_configs and isinstance(value, string_types) and all(('=' in v for v in value.split(','))):
                    try:
                        value = dict((key.split('=', 1) for key in value.split(',')))
                    except Exception:
                        continue
                properties[key] = value
            except NameError:
                return None

    def _get_vm_status(self, properties, node, vmid, vmtype, name):
        ret = self._get_json('%s/api2/json/nodes/%s/%s/%s/status/current' % (self.proxmox_url, node, vmtype, vmid))
        properties[self._fact('status')] = ret['status']
        if vmtype == 'qemu':
            properties[self._fact('qmpstatus')] = ret['qmpstatus']

    def _get_vm_snapshots(self, properties, node, vmid, vmtype, name):
        ret = self._get_json('%s/api2/json/nodes/%s/%s/%s/snapshot' % (self.proxmox_url, node, vmtype, vmid))
        snapshots = [snapshot['name'] for snapshot in ret if snapshot['name'] != 'current']
        properties[self._fact('snapshots')] = snapshots

    def to_safe(self, word):
        """Converts 'bad' characters in a string to underscores so they can be used as Ansible groups
        #> ProxmoxInventory.to_safe("foo-bar baz")
        'foo_barbaz'
        """
        regex = '[^A-Za-z0-9\\_]'
        return re.sub(regex, '_', word.replace(' ', ''))

    def _fact(self, name):
        """Generate a fact's full name from the common prefix and a name."""
        return self.to_safe('%s%s' % (self.facts_prefix, name.lower()))

    def _group(self, name):
        """Generate a group's full name from the common prefix and a name."""
        return self.to_safe('%s%s' % (self.group_prefix, name.lower()))

    def _can_add_host(self, name, properties):
        """Ensure that a host satisfies all defined hosts filters. If strict mode is
        enabled, any error during host filter compositing will lead to an AnsibleError
        being raised, otherwise the filter will be ignored.
        """
        for host_filter in self.host_filters:
            try:
                if not self._compose(host_filter, properties):
                    return False
            except Exception as e:
                message = 'Could not evaluate host filter %s for host %s - %s' % (host_filter, name, to_native(e))
                if self.strict:
                    raise AnsibleError(message)
                display.warning(message)
        return True

    def _add_host(self, name, variables):
        self.inventory.add_host(name)
        for (k, v) in variables.items():
            self.inventory.set_variable(name, k, v)
        variables = self.inventory.get_host(name).get_vars()
        self._set_composite_vars(self.get_option('compose'), variables, name, strict=self.strict)
        self._add_host_to_composed_groups(self.get_option('groups'), variables, name, strict=self.strict)
        self._add_host_to_keyed_groups(self.get_option('keyed_groups'), variables, name, strict=self.strict)

    def _handle_item(self, node, ittype, item):
        """Handle an item from the list of LXC containers and Qemu VM. The
        return value will be either None if the item was skipped or the name of
        the item if it was added to the inventory."""
        if item.get('template'):
            return None
        properties = dict()
        (name, vmid) = (item['name'], item['vmid'])
        want_facts = self.get_option('want_facts')
        if want_facts:
            self._get_vm_status(properties, node, vmid, ittype, name)
            self._get_vm_config(properties, node, vmid, ittype, name)
            self._get_vm_snapshots(properties, node, vmid, ittype, name)
        if not self._can_add_host(name, properties):
            return None
        self._add_host(name, properties)
        node_type_group = self._group('%s_%s' % (node, ittype))
        self.inventory.add_child(self._group('all_' + ittype), name)
        self.inventory.add_child(node_type_group, name)
        item_status = item['status']
        if item_status == 'running':
            if want_facts and ittype == 'qemu' and self.get_option('qemu_extended_statuses'):
                item_status = properties.get(self._fact('qmpstatus'), item_status)
        self.inventory.add_child(self._group('all_%s' % (item_status,)), name)
        return name

    def _populate_pool_groups(self, added_hosts):
        """Generate groups from Proxmox resource pools, ignoring VMs and
        containers that were skipped."""
        for pool in self._get_pools():
            poolid = pool.get('poolid')
            if not poolid:
                continue
            pool_group = self._group('pool_' + poolid)
            self.inventory.add_group(pool_group)
            for member in self._get_members_per_pool(poolid):
                name = member.get('name')
                if name and name in added_hosts:
                    self.inventory.add_child(pool_group, name)

    def _populate(self):
        default_groups = ['lxc', 'qemu', 'running', 'stopped']
        if self.get_option('qemu_extended_statuses'):
            default_groups.extend(['prelaunch', 'paused'])
        for group in default_groups:
            self.inventory.add_group(self._group('all_%s' % group))
        nodes_group = self._group('nodes')
        self.inventory.add_group(nodes_group)
        want_proxmox_nodes_ansible_host = self.get_option('want_proxmox_nodes_ansible_host')
        self._get_auth()
        hosts = []
        for node in self._get_nodes():
            if not node.get('node'):
                continue
            self.inventory.add_host(node['node'])
            if node['type'] == 'node':
                self.inventory.add_child(nodes_group, node['node'])
            if node['status'] == 'offline':
                continue
            if want_proxmox_nodes_ansible_host:
                ip = self._get_node_ip(node['node'])
                self.inventory.set_variable(node['node'], 'ansible_host', ip)
            for ittype in ('lxc', 'qemu'):
                node_type_group = self._group('%s_%s' % (node['node'], ittype))
                self.inventory.add_group(node_type_group)
            lxc_objects = zip(itertools.repeat('lxc'), self._get_lxc_per_node(node['node']))
            qemu_objects = zip(itertools.repeat('qemu'), self._get_qemu_per_node(node['node']))
            for (ittype, item) in itertools.chain(lxc_objects, qemu_objects):
                name = self._handle_item(node['node'], ittype, item)
                if name is not None:
                    hosts.append(name)
        self._populate_pool_groups(hosts)

    def parse(self, inventory, loader, path, cache=True):
        if not HAS_REQUESTS:
            raise AnsibleError('This module requires Python Requests 1.1.0 or higher: https://github.com/psf/requests.')
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)
        for o in ('url', 'user', 'password', 'token_id', 'token_secret'):
            v = self.get_option(o)
            if self.templar.is_template(v):
                v = self.templar.template(v, disable_lookups=False)
            setattr(self, 'proxmox_%s' % o, v)
        self.proxmox_url = self.proxmox_url.rstrip('/')
        if self.proxmox_password is None and (self.proxmox_token_id is None or self.proxmox_token_secret is None):
            raise AnsibleError('You must specify either a password or both token_id and token_secret.')
        if self.get_option('qemu_extended_statuses') and (not self.get_option('want_facts')):
            raise AnsibleError('You must set want_facts to True if you want to use qemu_extended_statuses.')
        self.cache_key = self.get_cache_key(path)
        self.use_cache = cache and self.get_option('cache')
        self.host_filters = self.get_option('filters')
        self.group_prefix = self.get_option('group_prefix')
        self.facts_prefix = self.get_option('facts_prefix')
        self.strict = self.get_option('strict')
        self._populate()