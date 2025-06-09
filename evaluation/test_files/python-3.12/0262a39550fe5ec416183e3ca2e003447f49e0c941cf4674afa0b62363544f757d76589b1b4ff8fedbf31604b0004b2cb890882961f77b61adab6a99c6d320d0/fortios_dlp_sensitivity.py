from __future__ import absolute_import, division, print_function
__metaclass__ = type
ANSIBLE_METADATA = {'status': ['preview'], 'supported_by': 'community', 'metadata_version': '1.1'}
DOCUMENTATION = '\n---\nmodule: fortios_dlp_sensitivity\nshort_description: Create self-explanatory DLP sensitivity levels to be used when setting sensitivity under config fp-doc-source in Fortinet\'s FortiOS and\n   FortiGate.\ndescription:\n    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the\n      user to set and modify dlp feature and sensitivity category.\n      Examples include all parameters and values need to be adjusted to datasources before usage.\n      Tested with FOS v6.0.0\nversion_added: "2.0.0"\nauthor:\n    - Link Zheng (@chillancezen)\n    - Jie Xue (@JieX19)\n    - Hongbin Lu (@fgtdev-hblu)\n    - Frank Shen (@frankshen01)\n    - Miguel Angel Munoz (@mamunozgonzalez)\n    - Nicolas Thomas (@thomnico)\nnotes:\n    - Legacy fortiosapi has been deprecated, httpapi is the preferred way to run playbooks\n\nrequirements:\n    - ansible>=2.9\noptions:\n    access_token:\n        description:\n            - Token-based authentication.\n              Generated from GUI of Fortigate.\n        type: str\n        required: false\n    enable_log:\n        description:\n            - Enable/Disable logging for task.\n        type: bool\n        required: false\n        default: false\n    vdom:\n        description:\n            - Virtual domain, among those defined previously. A vdom is a\n              virtual instance of the FortiGate that can be configured and\n              used as a different unit.\n        type: str\n        default: root\n    member_path:\n        type: str\n        description:\n            - Member attribute path to operate on.\n            - Delimited by a slash character if there are more than one attribute.\n            - Parameter marked with member_path is legitimate for doing member operation.\n    member_state:\n        type: str\n        description:\n            - Add or delete a member under specified attribute path.\n            - When member_state is specified, the state option is ignored.\n        choices:\n            - \'present\'\n            - \'absent\'\n\n    state:\n        description:\n            - Indicates whether to create or remove the object.\n        type: str\n        required: true\n        choices:\n            - \'present\'\n            - \'absent\'\n    dlp_sensitivity:\n        description:\n            - Create self-explanatory DLP sensitivity levels to be used when setting sensitivity under config fp-doc-source.\n        default: null\n        type: dict\n        suboptions:\n            name:\n                description:\n                    - DLP Sensitivity Levels.\n                required: true\n                type: str\n'
EXAMPLES = '\n- hosts: fortigates\n  collections:\n    - fortinet.fortios\n  connection: httpapi\n  vars:\n   vdom: "root"\n   ansible_httpapi_use_ssl: yes\n   ansible_httpapi_validate_certs: no\n   ansible_httpapi_port: 443\n  tasks:\n  - name: Create self-explanatory DLP sensitivity levels to be used when setting sensitivity under config fp-doc-source.\n    fortios_dlp_sensitivity:\n      vdom:  "{{ vdom }}"\n      state: "present"\n      access_token: "<your_own_value>"\n      dlp_sensitivity:\n        name: "default_name_3"\n\n'
RETURN = '\nbuild:\n  description: Build number of the fortigate image\n  returned: always\n  type: str\n  sample: \'1547\'\nhttp_method:\n  description: Last method used to provision the content into FortiGate\n  returned: always\n  type: str\n  sample: \'PUT\'\nhttp_status:\n  description: Last result given by FortiGate on last operation applied\n  returned: always\n  type: str\n  sample: "200"\nmkey:\n  description: Master key (id) used in the last call to FortiGate\n  returned: success\n  type: str\n  sample: "id"\nname:\n  description: Name of the table used to fulfill the request\n  returned: always\n  type: str\n  sample: "urlfilter"\npath:\n  description: Path of the table used to fulfill the request\n  returned: always\n  type: str\n  sample: "webfilter"\nrevision:\n  description: Internal revision number\n  returned: always\n  type: str\n  sample: "17.0.2.10658"\nserial:\n  description: Serial number of the unit\n  returned: always\n  type: str\n  sample: "FGVMEVYYQT3AB5352"\nstatus:\n  description: Indication of the operation\'s result\n  returned: always\n  type: str\n  sample: "success"\nvdom:\n  description: Virtual domain used\n  returned: always\n  type: str\n  sample: "root"\nversion:\n  description: Version of the FortiGate\n  returned: always\n  type: str\n  sample: "v5.6.3"\n\n'
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import FortiOSHandler
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import check_legacy_fortiosapi
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import schema_to_module_spec
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import check_schema_versioning
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FAIL_SOCKET_MSG
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.data_post_processor import remove_invalid_fields
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.comparison import is_same_comparison
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.comparison import serialize

def filter_dlp_sensitivity_data(json):
    option_list = ['name']
    json = remove_invalid_fields(json)
    dictionary = {}
    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]
    return dictionary

def underscore_to_hyphen(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace('_', '-')] = underscore_to_hyphen(v)
        data = new_data
    return data

def dlp_sensitivity(data, fos, check_mode=False):
    vdom = data['vdom']
    state = data['state']
    dlp_sensitivity_data = data['dlp_sensitivity']
    filtered_data = underscore_to_hyphen(filter_dlp_sensitivity_data(dlp_sensitivity_data))
    if check_mode:
        diff = {'before': '', 'after': filtered_data}
        mkey = fos.get_mkey('dlp', 'sensitivity', filtered_data, vdom=vdom)
        current_data = fos.get('dlp', 'sensitivity', vdom=vdom, mkey=mkey)
        is_existed = current_data and current_data.get('http_status') == 200 and isinstance(current_data.get('results'), list) and (len(current_data['results']) > 0)
        if state == 'present' or state is True:
            if mkey is None:
                return (False, True, filtered_data, diff)
            if is_existed:
                is_same = is_same_comparison(serialize(current_data['results'][0]), serialize(filtered_data))
                return (False, not is_same, filtered_data, {'before': current_data['results'][0], 'after': filtered_data})
            return (False, True, filtered_data, diff)
        if state == 'absent':
            if mkey is None:
                return (False, False, filtered_data, {'before': current_data['results'][0], 'after': ''})
            if is_existed:
                return (False, True, filtered_data, {'before': current_data['results'][0], 'after': ''})
            return (False, False, filtered_data, {})
        return (True, False, {'reason: ': 'Must provide state parameter'}, {})
    if state == 'present' or state is True:
        return fos.set('dlp', 'sensitivity', data=filtered_data, vdom=vdom)
    elif state == 'absent':
        return fos.delete('dlp', 'sensitivity', mkey=filtered_data['name'], vdom=vdom)
    else:
        fos._module.fail_json(msg='state must be present or absent!')

def is_successful_status(resp):
    return 'status' in resp and resp['status'] == 'success' or ('http_status' in resp and resp['http_status'] == 200) or ('http_method' in resp and resp['http_method'] == 'DELETE' and (resp['http_status'] == 404))

def fortios_dlp(data, fos, check_mode):
    fos.do_member_operation('dlp', 'sensitivity')
    if data['dlp_sensitivity']:
        resp = dlp_sensitivity(data, fos, check_mode)
    else:
        fos._module.fail_json(msg='missing task body: %s' % 'dlp_sensitivity')
    if check_mode:
        return resp
    return (not is_successful_status(resp), is_successful_status(resp) and (resp['revision_changed'] if 'revision_changed' in resp else True), resp, {})
versioned_schema = {'type': 'list', 'elements': 'dict', 'children': {'name': {'revisions': {'v7.2.2': True, 'v7.2.1': True, 'v7.2.0': True, 'v7.0.8': True, 'v7.0.7': True, 'v7.0.6': True, 'v7.0.5': True, 'v7.0.4': True, 'v7.0.3': True, 'v7.0.2': True, 'v7.0.1': True, 'v7.0.0': True, 'v6.4.4': True, 'v6.4.1': True, 'v6.4.0': True, 'v6.2.7': True, 'v6.2.5': True, 'v6.2.3': True, 'v6.2.0': True}, 'type': 'string'}}, 'revisions': {'v7.2.2': True, 'v7.2.1': True, 'v7.2.0': True, 'v7.0.8': True, 'v7.0.7': True, 'v7.0.6': True, 'v7.0.5': True, 'v7.0.4': True, 'v7.0.3': True, 'v7.0.2': True, 'v7.0.1': True, 'v7.0.0': True, 'v6.4.4': True, 'v6.4.1': True, 'v6.4.0': True, 'v6.2.7': True, 'v6.2.5': True, 'v6.2.3': True, 'v6.2.0': True}}

def main():
    module_spec = schema_to_module_spec(versioned_schema)
    mkeyname = 'name'
    fields = {'access_token': {'required': False, 'type': 'str', 'no_log': True}, 'enable_log': {'required': False, 'type': 'bool', 'default': False}, 'vdom': {'required': False, 'type': 'str', 'default': 'root'}, 'member_path': {'required': False, 'type': 'str'}, 'member_state': {'type': 'str', 'required': False, 'choices': ['present', 'absent']}, 'state': {'required': True, 'type': 'str', 'choices': ['present', 'absent']}, 'dlp_sensitivity': {'required': False, 'type': 'dict', 'default': None, 'options': {}}}
    for attribute_name in module_spec['options']:
        fields['dlp_sensitivity']['options'][attribute_name] = module_spec['options'][attribute_name]
        if mkeyname and mkeyname == attribute_name:
            fields['dlp_sensitivity']['options'][attribute_name]['required'] = True
    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    check_legacy_fortiosapi(module)
    versions_check_result = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        if 'access_token' in module.params:
            connection.set_option('access_token', module.params['access_token'])
        if 'enable_log' in module.params:
            connection.set_option('enable_log', module.params['enable_log'])
        else:
            connection.set_option('enable_log', False)
        fos = FortiOSHandler(connection, module, mkeyname)
        versions_check_result = check_schema_versioning(fos, versioned_schema, 'dlp_sensitivity')
        is_error, has_changed, result, diff = fortios_dlp(module.params, fos, module.check_mode)
    else:
        module.fail_json(**FAIL_SOCKET_MSG)
    if versions_check_result and versions_check_result['matched'] is False:
        module.warn('Ansible has detected version mismatch between FortOS system and your playbook, see more details by specifying option -vvv')
    if not is_error:
        if versions_check_result and versions_check_result['matched'] is False:
            module.exit_json(changed=has_changed, version_check_warning=versions_check_result, meta=result, diff=diff)
        else:
            module.exit_json(changed=has_changed, meta=result, diff=diff)
    elif versions_check_result and versions_check_result['matched'] is False:
        module.fail_json(msg='Error in repo', version_check_warning=versions_check_result, meta=result)
    else:
        module.fail_json(msg='Error in repo', meta=result)
if __name__ == '__main__':
    main()