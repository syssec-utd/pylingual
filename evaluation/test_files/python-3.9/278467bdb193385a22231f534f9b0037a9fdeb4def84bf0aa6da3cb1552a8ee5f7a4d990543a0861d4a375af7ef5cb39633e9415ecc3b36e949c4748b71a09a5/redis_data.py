from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: redis_data\nshort_description: Set key value pairs in Redis\nversion_added: 3.7.0\ndescription:\n   - Set key value pairs in Redis database.\nauthor: "Andreas Botzner (@paginabianca)"\nattributes:\n    check_mode:\n        support: full\n    diff_mode:\n        support: none\noptions:\n    key:\n        description:\n            - Database key.\n        required: true\n        type: str\n    value:\n        description:\n            - Value that key should be set to.\n        required: false\n        type: str\n    expiration:\n        description:\n            - Expiration time in milliseconds.\n              Setting this flag will always result in a change in the database.\n        required: false\n        type: int\n    non_existing:\n        description:\n            - Only set key if it does not already exist.\n        required: false\n        type: bool\n    existing:\n        description:\n            - Only set key if it already exists.\n        required: false\n        type: bool\n    keep_ttl:\n        description:\n            - Retain the time to live associated with the key.\n        required: false\n        type: bool\n    state:\n        description:\n            - State of the key.\n        default: present\n        type: str\n        choices:\n            - present\n            - absent\n\nextends_documentation_fragment:\n  - community.general.redis.documentation\n  - community.general.attributes\n\nseealso:\n    - module: community.general.redis_data_incr\n    - module: community.general.redis_data_info\n    - module: community.general.redis\n'
EXAMPLES = '\n- name: Set key foo=bar on localhost with no username\n  community.general.redis_data:\n    login_host: localhost\n    login_password: supersecret\n    key: foo\n    value: bar\n    state: present\n\n- name: Set key foo=bar if non existing with expiration of 30s\n  community.general.redis_data:\n    login_host: localhost\n    login_password: supersecret\n    key: foo\n    value: bar\n    non_existing: true\n    expiration: 30000\n    state: present\n\n- name: Set key foo=bar if existing and keep current TTL\n  community.general.redis_data:\n    login_host: localhost\n    login_password: supersecret\n    key: foo\n    value: bar\n    existing: true\n    keep_ttl: true\n\n- name: Set key foo=bar on redishost with custom ca-cert file\n  community.general.redis_data:\n    login_host: redishost\n    login_password: supersecret\n    login_user: someuser\n    validate_certs: true\n    ssl_ca_certs: /path/to/ca/certs\n    key: foo\n    value: bar\n\n- name: Delete key foo on localhost with no username\n  community.general.redis_data:\n    login_host: localhost\n    login_password: supersecret\n    key: foo\n    state: absent\n'
RETURN = "\nold_value:\n  description: Value of key before setting.\n  returned: on_success if state is C(present) and key exists in database.\n  type: str\n  sample: 'old_value_of_key'\nvalue:\n  description: Value key was set to.\n  returned: on success if state is C(present).\n  type: str\n  sample: 'new_value_of_key'\nmsg:\n  description: A short message.\n  returned: always\n  type: str\n  sample: 'Set key: foo to bar'\n"
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.redis import fail_imports, redis_auth_argument_spec, RedisAnsible

def main():
    redis_auth_args = redis_auth_argument_spec()
    module_args = dict(key=dict(type='str', required=True, no_log=False), value=dict(type='str', required=False), expiration=dict(type='int', required=False), non_existing=dict(type='bool', required=False), existing=dict(type='bool', required=False), keep_ttl=dict(type='bool', required=False), state=dict(type='str', default='present', choices=['present', 'absent']))
    module_args.update(redis_auth_args)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True, required_if=[('state', 'present', ('value',))], mutually_exclusive=[['non_existing', 'existing'], ['keep_ttl', 'expiration']])
    fail_imports(module)
    redis = RedisAnsible(module)
    key = module.params['key']
    value = module.params['value']
    px = module.params['expiration']
    nx = module.params['non_existing']
    xx = module.params['existing']
    keepttl = module.params['keep_ttl']
    state = module.params['state']
    set_args = {'name': key, 'value': value, 'px': px, 'nx': nx, 'xx': xx, 'keepttl': keepttl}
    result = {'changed': False}
    old_value = None
    try:
        old_value = redis.connection.get(key)
    except Exception as e:
        msg = 'Failed to get value of key: {0} with exception: {1}'.format(key, str(e))
        result['msg'] = msg
        module.fail_json(**result)
    if state == 'absent':
        if module.check_mode:
            if old_value is None:
                msg = 'Key: {0} not present'.format(key)
                result['msg'] = msg
                module.exit_json(**result)
            else:
                msg = 'Deleted key: {0}'.format(key)
                result['msg'] = msg
                module.exit_json(**result)
        try:
            ret = redis.connection.delete(key)
            if ret == 0:
                msg = 'Key: {0} not present'.format(key)
                result['msg'] = msg
                module.exit_json(**result)
            else:
                msg = 'Deleted key: {0}'.format(key)
                result['msg'] = msg
                result['changed'] = True
                module.exit_json(**result)
        except Exception as e:
            msg = 'Failed to delete key: {0} with exception: {1}'.format(key, str(e))
            result['msg'] = msg
            module.fail_json(**result)
    old_value = None
    try:
        old_value = redis.connection.get(key)
    except Exception as e:
        msg = 'Failed to get value of key: {0} with exception: {1}'.format(key, str(e))
        result['msg'] = msg
        module.fail_json(**result)
    result['old_value'] = old_value
    if old_value == value and keepttl is not False and (px is None):
        msg = 'Key {0} already has desired value'.format(key)
        result['msg'] = msg
        result['value'] = value
        module.exit_json(**result)
    if module.check_mode:
        result['msg'] = 'Set key: {0}'.format(key)
        result['value'] = value
        module.exit_json(**result)
    try:
        ret = redis.connection.set(**set_args)
        if ret is None:
            if nx:
                msg = 'Could not set key: {0}. Key already present.'.format(key)
            else:
                msg = 'Could not set key: {0}. Key not present.'.format(key)
            result['msg'] = msg
            module.fail_json(**result)
        msg = 'Set key: {0}'.format(key)
        result['msg'] = msg
        result['changed'] = True
        result['value'] = value
        module.exit_json(**result)
    except Exception as e:
        msg = 'Failed to set key: {0} with exception: {2}'.format(key, str(e))
        result['msg'] = msg
        module.fail_json(**result)
if __name__ == '__main__':
    main()