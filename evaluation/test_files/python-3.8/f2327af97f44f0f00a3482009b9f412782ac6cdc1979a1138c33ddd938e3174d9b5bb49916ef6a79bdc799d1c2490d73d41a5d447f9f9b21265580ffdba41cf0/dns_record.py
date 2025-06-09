from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: dns_record\nshort_description: Manages DNS records on Vultr\ndescription:\n  - Create, update and remove DNS records.\nversion_added: "1.0.0"\nauthor: "René Moser (@resmo)"\noptions:\n  name:\n    description:\n      - The record name.\n    type: str\n    default: ""\n  domain:\n    description:\n      - The domain the record is related to.\n    type: str\n    required: true\n  type:\n    description:\n      - Type of the record.\n    default: A\n    choices:\n    - A\n    - AAAA\n    - CNAME\n    - NS\n    - MX\n    - SRV\n    - TXT\n    - CAA\n    - SSHFP\n    aliases: [ record_type ]\n    type: str\n  data:\n    description:\n      - Data of the record.\n      - Required if C(state=present).\n    type: str\n  ttl:\n    description:\n      - TTL of the record.\n    default: 300\n    type: int\n  priority:\n    description:\n      - Priority of the record.\n    type: int\n  multiple:\n    description:\n      - Whether to use more than one record with similar I(name) including no name and I(type).\n      - Only allowed for a few record types, e.g. C(type=A), C(type=NS) or C(type=MX).\n      - I(data) will not be updated, instead it is used as a key to find existing records.\n    default: no\n    type: bool\n  state:\n    description:\n      - State of the DNS record.\n    default: present\n    choices: [ present, absent ]\n    type: str\nextends_documentation_fragment:\n  - vultr.cloud.vultr_v2\n'
EXAMPLES = '\n- name: Ensure an A record exists\n  vultr.cloud.dns_record:\n    name: www\n    domain: example.com\n    data: 10.10.10.10\n    ttl: 3600\n\n- name: Ensure a second A record exists for round robin LB\n  vultr.cloud.dns_record:\n    name: www\n    domain: example.com\n    data: 10.10.10.11\n    ttl: 60\n    multiple: true\n\n- name: Ensure a CNAME record exists\n  vultr.cloud.dns_record:\n    name: web\n    type: CNAME\n    domain: example.com\n    data: www.example.com\n\n- name: Ensure MX record exists\n  vultr.cloud.dns_record:\n    type: MX\n    domain: example.com\n    data: "{{ item.data }}"\n    priority: "{{ item.priority }}"\n    multiple: true\n  with_items:\n    - { data: mx1.example.com, priority: 10 }\n    - { data: mx2.example.com, priority: 10 }\n    - { data: mx3.example.com, priority: 20 }\n\n- name: Ensure a record is absent\n  vultr.cloud.dns_record:\n    name: www\n    domain: example.com\n    state: absent\n\n- name: Ensure one MX record is absent if multiple exists\n  vultr.cloud.dns_record:\n    record_type: MX\n    domain: example.com\n    data: mx1.example.com\n    multiple: true\n    state: absent\n'
RETURN = '\n---\nvultr_api:\n  description: Response from Vultr API with a few additions/modification.\n  returned: success\n  type: dict\n  contains:\n    api_timeout:\n      description: Timeout used for the API requests.\n      returned: success\n      type: int\n      sample: 60\n    api_retries:\n      description: Amount of max retries for the API requests.\n      returned: success\n      type: int\n      sample: 5\n    api_retry_max_delay:\n      description: Exponential backoff delay in seconds between retries up to this max delay value.\n      returned: success\n      type: int\n      sample: 12\n    api_endpoint:\n      description: Endpoint used for the API requests.\n      returned: success\n      type: str\n      sample: "https://api.vultr.com/v2"\ndns_record:\n  description: Response from Vultr API.\n  returned: success\n  type: dict\n  contains:\n    id:\n      description: The ID of the DNS record.\n      returned: success\n      type: str\n      sample: cb676a46-66fd-4dfb-b839-443f2e6c0b60\n    name:\n      description: The name of the DNS record.\n      returned: success\n      type: str\n      sample: web\n    type:\n      description: The name of the DNS record.\n      returned: success\n      type: str\n      sample: A\n    data:\n      description: Data of the DNS record.\n      returned: success\n      type: str\n      sample: 10.10.10.10\n    priority:\n      description: Priority of the DNS record.\n      returned: success\n      type: int\n      sample: 10\n    ttl:\n      description: Time to live of the DNS record.\n      returned: success\n      type: int\n      sample: 300\n'
from ansible.module_utils.basic import AnsibleModule
from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec
RECORD_TYPES = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SRV', 'CAA', 'SSHFP']

class AnsibleVultrDnsRecord(AnsibleVultr):

    def query(self):
        multiple = self.module.params.get('multiple')
        name = self.module.params.get('name')
        data = self.module.params.get('data')
        record_type = self.module.params.get('type')
        result = dict()
        for resource in self.query_list():
            if resource.get('type') != record_type:
                continue
            if resource.get('name') == name:
                if not multiple:
                    if result:
                        self.module.fail_json(msg='More than one record with record_type=%s and name=%s params. Use multiple=yes for more than one record.' % (record_type, name))
                    else:
                        result = resource
                elif resource.get('data') == data:
                    return resource
        return result

def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(dict(domain=dict(type='str', required=True), name=dict(type='str', default=''), state=dict(type='str', choices=['present', 'absent'], default='present'), ttl=dict(type='int', default=300), type=dict(type='str', choices=RECORD_TYPES, default='A', aliases=['record_type']), multiple=dict(type='bool', default=False), priority=dict(type='int'), data=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['data']), ('multiple', True, ['data'])], supports_check_mode=True)
    vultr = AnsibleVultrDnsRecord(module=module, namespace='vultr_dns_record', resource_path='/domains/%s/records' % module.params.get('domain'), ressource_result_key_singular='record', resource_create_param_keys=['name', 'ttl', 'data', 'priority', 'type'], resource_update_param_keys=['name', 'ttl', 'data', 'priority'], resource_key_name='name')
    if module.params.get('state') == 'absent':
        vultr.absent()
    else:
        vultr.present()
if __name__ == '__main__':
    main()