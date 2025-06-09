from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: openssl_privatekey_convert\nshort_description: Convert OpenSSL private keys\nversion_added: 2.1.0\ndescription:\n    - This module allows one to convert OpenSSL private keys.\n    - The default mode for the private key file will be C(0600) if I(mode) is not explicitly set.\nauthor:\n    - Felix Fontein (@felixfontein)\nextends_documentation_fragment:\n    - ansible.builtin.files\n    - community.crypto.attributes\n    - community.crypto.attributes.files\n    - community.crypto.module_privatekey_convert\nattributes:\n    check_mode:\n        support: full\n    diff_mode:\n        support: none\n    safe_file_operations:\n        support: full\noptions:\n    dest_path:\n        description:\n            - Name of the file in which the generated TLS/SSL private key will be written. It will have C(0600) mode\n              if I(mode) is not explicitly set.\n        type: path\n        required: true\n    backup:\n        description:\n            - Create a backup file including a timestamp so you can get\n              the original private key back if you overwrote it with a new one by accident.\n        type: bool\n        default: false\nseealso: []\n'
EXAMPLES = "\n- name: Convert private key to PKCS8 format with passphrase\n  community.crypto.openssl_privatekey_convert:\n    src_path: /etc/ssl/private/ansible.com.pem\n    dest_path: /etc/ssl/private/ansible.com.key\n    dest_passphrase: '{{ private_key_passphrase }}'\n    format: pkcs8\n"
RETURN = '\nbackup_file:\n    description: Name of backup file created.\n    returned: changed and if I(backup) is C(true)\n    type: str\n    sample: /path/to/privatekey.pem.2019-03-09@11:22~\n'
import os
from ansible.module_utils.common.text.converters import to_native
from ansible_collections.community.crypto.plugins.module_utils.io import load_file_if_exists, write_file
from ansible_collections.community.crypto.plugins.module_utils.crypto.basic import OpenSSLObjectError
from ansible_collections.community.crypto.plugins.module_utils.crypto.support import OpenSSLObject
from ansible_collections.community.crypto.plugins.module_utils.crypto.module_backends.privatekey_convert import select_backend, get_privatekey_argument_spec

class PrivateKeyConvertModule(OpenSSLObject):

    def __init__(self, module, module_backend):
        super(PrivateKeyConvertModule, self).__init__(module.params['dest_path'], 'present', False, module.check_mode)
        self.module_backend = module_backend
        self.backup = module.params['backup']
        self.backup_file = None
        module.params['path'] = module.params['dest_path']
        if module.params['mode'] is None:
            module.params['mode'] = '0600'
        module_backend.set_existing_destination(load_file_if_exists(self.path, module))

    def generate(self, module):
        """Do conversion."""
        if self.module_backend.needs_conversion():
            privatekey_data = self.module_backend.get_private_key_data()
            if not self.check_mode:
                if self.backup:
                    self.backup_file = module.backup_local(self.path)
                write_file(module, privatekey_data, 384)
            self.changed = True
        file_args = module.load_file_common_arguments(module.params)
        if module.check_file_absent_if_check_mode(file_args['path']):
            self.changed = True
        else:
            self.changed = module.set_fs_attributes_if_different(file_args, self.changed)

    def dump(self):
        """Serialize the object into a dictionary."""
        result = self.module_backend.dump()
        result['changed'] = self.changed
        if self.backup_file:
            result['backup_file'] = self.backup_file
        return result

def main():
    argument_spec = get_privatekey_argument_spec()
    argument_spec.argument_spec.update(dict(dest_path=dict(type='path', required=True), backup=dict(type='bool', default=False)))
    module = argument_spec.create_ansible_module(supports_check_mode=True, add_file_common_args=True)
    base_dir = os.path.dirname(module.params['dest_path']) or '.'
    if not os.path.isdir(base_dir):
        module.fail_json(name=base_dir, msg='The directory %s does not exist or the file is not a directory' % base_dir)
    module_backend = select_backend(module=module)
    try:
        private_key = PrivateKeyConvertModule(module, module_backend)
        private_key.generate(module)
        result = private_key.dump()
        module.exit_json(**result)
    except OpenSSLObjectError as exc:
        module.fail_json(msg=to_native(exc))
if __name__ == '__main__':
    main()