from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = "\n---\nauthor:\n    - Joris Weijters (@molekuul)\nmodule: aix_inittab\nshort_description: Manages the inittab on AIX\ndescription:\n    - Manages the inittab on AIX.\nextends_documentation_fragment:\n    - community.general.attributes\nattributes:\n  check_mode:\n    support: full\n  diff_mode:\n    support: none\noptions:\n  name:\n    description:\n    - Name of the inittab entry.\n    type: str\n    required: true\n    aliases: [ service ]\n  runlevel:\n    description:\n    - Runlevel of the entry.\n    type: str\n    required: true\n  action:\n    description:\n    - Action what the init has to do with this entry.\n    type: str\n    choices:\n    - boot\n    - bootwait\n    - hold\n    - initdefault\n    - 'off'\n    - once\n    - ondemand\n    - powerfail\n    - powerwait\n    - respawn\n    - sysinit\n    - wait\n  command:\n    description:\n    - What command has to run.\n    type: str\n    required: true\n  insertafter:\n    description:\n    - After which inittabline should the new entry inserted.\n    type: str\n  state:\n    description:\n    - Whether the entry should be present or absent in the inittab file.\n    type: str\n    choices: [ absent, present ]\n    default: present\nnotes:\n  - The changes are persistent across reboots.\n  - You need root rights to read or adjust the inittab with the C(lsitab), C(chitab), C(mkitab) or C(rmitab) commands.\n  - Tested on AIX 7.1.\nrequirements:\n- itertools\n"
EXAMPLES = '\n# Add service startmyservice to the inittab, directly after service existingservice.\n- name: Add startmyservice to inittab\n  community.general.aix_inittab:\n    name: startmyservice\n    runlevel: 4\n    action: once\n    command: echo hello\n    insertafter: existingservice\n    state: present\n  become: true\n\n# Change inittab entry startmyservice to runlevel "2" and processaction "wait".\n- name: Change startmyservice to inittab\n  community.general.aix_inittab:\n    name: startmyservice\n    runlevel: 2\n    action: wait\n    command: echo hello\n    state: present\n  become: true\n\n- name: Remove startmyservice from inittab\n  community.general.aix_inittab:\n    name: startmyservice\n    runlevel: 2\n    action: wait\n    command: echo hello\n    state: absent\n  become: true\n'
RETURN = '\nname:\n    description: Name of the adjusted inittab entry\n    returned: always\n    type: str\n    sample: startmyservice\nmsg:\n    description: Action done with the inittab entry\n    returned: changed\n    type: str\n    sample: changed inittab entry startmyservice\nchanged:\n    description: Whether the inittab changed or not\n    returned: always\n    type: bool\n    sample: true\n'
try:
    from itertools import izip
except ImportError:
    izip = zip
from ansible.module_utils.basic import AnsibleModule

def check_current_entry(module):
    existsdict = {'exist': False}
    lsitab = module.get_bin_path('lsitab')
    rc, out, err = module.run_command([lsitab, module.params['name']])
    if rc == 0:
        keys = ('name', 'runlevel', 'action', 'command')
        values = out.split(':')
        values = map(lambda s: s.strip(), values)
        existsdict = dict(izip(keys, values))
        existsdict.update({'exist': True})
    return existsdict

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True, aliases=['service']), runlevel=dict(type='str', required=True), action=dict(type='str', choices=['boot', 'bootwait', 'hold', 'initdefault', 'off', 'once', 'ondemand', 'powerfail', 'powerwait', 'respawn', 'sysinit', 'wait']), command=dict(type='str', required=True), insertafter=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'present'])), supports_check_mode=True)
    result = {'name': module.params['name'], 'changed': False, 'msg': ''}
    mkitab = module.get_bin_path('mkitab')
    rmitab = module.get_bin_path('rmitab')
    chitab = module.get_bin_path('chitab')
    rc = 0
    current_entry = check_current_entry(module)
    if module.params['state'] == 'present':
        new_entry = module.params['name'] + ':' + module.params['runlevel'] + ':' + module.params['action'] + ':' + module.params['command']
        if not current_entry['exist'] or (module.params['runlevel'] != current_entry['runlevel'] or module.params['action'] != current_entry['action'] or module.params['command'] != current_entry['command']):
            if current_entry['exist']:
                if not module.check_mode:
                    rc, out, err = module.run_command([chitab, new_entry])
                if rc != 0:
                    module.fail_json(msg='could not change inittab', rc=rc, err=err)
                result['msg'] = 'changed inittab entry' + ' ' + current_entry['name']
                result['changed'] = True
            elif not current_entry['exist']:
                if module.params['insertafter']:
                    if not module.check_mode:
                        rc, out, err = module.run_command([mkitab, '-i', module.params['insertafter'], new_entry])
                elif not module.check_mode:
                    rc, out, err = module.run_command([mkitab, new_entry])
                if rc != 0:
                    module.fail_json(msg='could not adjust inittab', rc=rc, err=err)
                result['msg'] = 'add inittab entry' + ' ' + module.params['name']
                result['changed'] = True
    elif module.params['state'] == 'absent':
        if current_entry['exist']:
            if not module.check_mode:
                rc, out, err = module.run_command([rmitab, module.params['name']])
                if rc != 0:
                    module.fail_json(msg='could not remove entry from inittab)', rc=rc, err=err)
            result['msg'] = 'removed inittab entry' + ' ' + current_entry['name']
            result['changed'] = True
    module.exit_json(**result)
if __name__ == '__main__':
    main()