"""NetApp StorageGRID - Manage Tenant Identity Federation"""
from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = "\nmodule: na_sg_org_identity_federation\nshort_description: NetApp StorageGRID manage Tenant identity federation.\nextends_documentation_fragment:\n    - netapp.storagegrid.netapp.sg\nversion_added: '21.6.0'\nauthor: NetApp Ansible Team (@joshedmonds) <ng-ansibleteam@netapp.com>\ndescription:\n- Configure Tenant Identity Federation within NetApp StorageGRID.\n- If module is run with C(check_mode), a connectivity test will be performed using the supplied values without changing the configuration.\n- This module is idempotent if I(password) is not specified.\noptions:\n  state:\n    description:\n    - Whether identity federation should be enabled or not.\n    type: str\n    choices: ['present', 'absent']\n    default: present\n  username:\n    description:\n    - The username to bind to the LDAP server.\n    type: str\n  password:\n    description:\n    - The password associated with the username.\n    type: str\n  hostname:\n    description:\n    - The hostname or IP address of the LDAP server.\n    type: str\n  port:\n    description:\n    - The port used to connect to the LDAP server. Typically 389 for LDAP, or 636 for LDAPS.\n    type: int\n  base_group_dn:\n    description:\n    - The Distinguished Name of the LDAP subtree to search for groups.\n    type: str\n  base_user_dn:\n    description:\n    - The Distinguished Name of the LDAP subtree to search for users.\n    type: str\n  ldap_service_type:\n    description:\n    - The type of LDAP server.\n    choices: ['Active Directory', 'OpenLDAP', 'Other']\n    type: str\n  type:\n    description:\n    - The type of identity source.\n    - Default is 'ldap'.\n    type: str\n    default: ldap\n  ldap_user_id_attribute:\n    description:\n    - The LDAP attribute which contains the unique user name of a user.\n    - Should be configured if I(ldap_service_type=Other).\n    type: str\n  ldap_user_uuid_attribute:\n    description:\n    - The LDAP attribute which contains the permanent unique identity of a user.\n    - Should be configured if I(ldap_service_type=Other).\n    type: str\n  ldap_group_id_attribute:\n    description:\n    - The LDAP attribute which contains the group for a user.\n    - Should be configured if I(ldap_service_type=Other).\n    type: str\n  ldap_group_uuid_attribute:\n    description:\n    - The LDAP attribute which contains the group's permanent unique identity.\n    - Should be configured if I(ldap_service_type=Other).\n    type: str\n  tls:\n    description:\n    - Whether Transport Layer Security is used to connect to the LDAP server.\n    choices: ['STARTTLS', 'LDAPS', 'Disabled']\n    type: str\n    default: STARTTLS\n  ca_cert:\n    description:\n    - Custom certificate used to connect to the LDAP server.\n    - If a custom certificate is not supplied, the operating system CA certificate will be used.\n    type: str\n"
EXAMPLES = '\n  - name: test identity federation configuration\n    netapp.storagegrid.na_sg_org_identity_federation:\n      api_url: "https://<storagegrid-endpoint-url>"\n      auth_token: "storagegrid-auth-token"\n      validate_certs: false\n      state: present\n      ldap_service_type: "Active Directory"\n      hostname: "ad.example.com"\n      port: 389\n      username: "binduser"\n      password: "bindpass"\n      base_group_dn: "DC=example,DC=com"\n      base_user_dn: "DC=example,DC=com"\n      tls: "Disabled"\n    check_mode: yes\n\n  - name: configure identity federation with AD and TLS\n    netapp.storagegrid.na_sg_org_identity_federation:\n      api_url: "https://<storagegrid-endpoint-url>"\n      auth_token: "storagegrid-auth-token"\n      validate_certs: false\n      state: present\n      ldap_service_type: "Active Directory"\n      hostname: "ad.example.com"\n      port: 636,\n      username: "binduser"\n      password: "bindpass"\n      base_group_dn: "DC=example,DC=com"\n      base_user_dn: "DC=example,DC=com"\n      tls: "LDAPS"\n      ca_cert: |\n          -----BEGIN CERTIFICATE-----\n          MIIC+jCCAeICCQDmn9Gow08LTzANBgkqhkiG9w0BAQsFADA/..swCQYDVQQGEwJV\n          bXBsZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB..JFzNIXQEGnsgjV\n          JGU4giuvOLOZ8Q3gyuUbkSUQDjmjpMR8PliwJ6iW2Ity89Dv..dl1TaIYI/ansyZ\n          Uxk4YXeN6kUkrDtNxCg1McALzXVAfxMTtj2SFlLxne4Z6rX2..UyftQrfM13F1vY\n          gK8dBPz+l+X/Uozo/xNm7gxe68p9le9/pcULst1CQn5/sPqq..kgWcSvlKUItu82\n          lq3B2169rovdIaNdcvaQjMPhrDGo5rvLfMN35U3Hgbz41PL5..x2BcUE6/0ab5T4\n          qKBxKa3t9twj+zpUqOzyL0PFfCE+SK5fEXAS1ow4eAcLN+eB..gR/PuvGAyIPCtE\n          1+X4GrECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAFpO+04Ra..FMJPH6dBmzfb7l\n          k04BWTvSlur6HiQdXY+oFQMJZzyI7MQ8v9HBIzS0ZAzYWLp4..VZhHmRxnrWyxVs\n          u783V5YfQH2L4QnBDoiDefgxyfDs2PcoF5C+X9CGXmPqzst2..y/6tdOVJzdiA==\n          -----END CERTIFICATE-----\n'
RETURN = '\nresp:\n    description: Returns information about the StorageGRID tenant account identity source configuration.\n    returned: success\n    type: dict\n    sample: {\n        "id": "00000000-0000-0000-0000-000000000000",\n        "disable": false,\n        "hostname": "10.1.2.3",\n        "port": 389,\n        "username": "MYDOMAIN\\\\Administrator",\n        "password": "********",\n        "baseGroupDn": "DC=example,DC=com",\n        "baseUserDn": "DC=example,DC=com",\n        "ldapServiceType": "Active Directory",\n        "type": "ldap",\n        "disableTLS": false,\n        "enableLDAPS": false,\n        "caCert": "-----BEGIN CERTIFICATE----- abcdefghijkl123456780ABCDEFGHIJKL 123456/7890ABCDEFabcdefghijklABCD -----END CERTIFICATE-----\n"\n    }\n'
import json
import re
import ansible_collections.netapp.storagegrid.plugins.module_utils.netapp as netapp_utils
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netapp.storagegrid.plugins.module_utils.netapp_module import NetAppModule
from ansible_collections.netapp.storagegrid.plugins.module_utils.netapp import SGRestAPI

class SgOrgIdentityFederation:
    """
    Configure and modify StorageGRID Tenant Identity Federation
    """

    def __init__(self):
        """
        Parse arguments, setup state variables,
        check parameters and ensure request module is installed
        """
        self.argument_spec = netapp_utils.na_storagegrid_host_argument_spec()
        self.argument_spec.update(dict(state=dict(required=False, type='str', choices=['present', 'absent'], default='present'), username=dict(required=False, type='str'), password=dict(required=False, type='str', no_log=True), hostname=dict(required=False, type='str'), port=dict(required=False, type='int'), base_group_dn=dict(required=False, type='str'), base_user_dn=dict(required=False, type='str'), ldap_service_type=dict(required=False, type='str', choices=['OpenLDAP', 'Active Directory', 'Other']), type=dict(required=False, type='str', default='ldap'), ldap_user_id_attribute=dict(required=False, type='str'), ldap_user_uuid_attribute=dict(required=False, type='str'), ldap_group_id_attribute=dict(required=False, type='str'), ldap_group_uuid_attribute=dict(required=False, type='str'), tls=dict(required=False, type='str', choices=['STARTTLS', 'LDAPS', 'Disabled'], default='STARTTLS'), ca_cert=dict(required=False, type='str')))
        parameter_map = {'username': 'username', 'password': 'password', 'hostname': 'hostname', 'port': 'port', 'base_group_dn': 'baseGroupDn', 'base_user_dn': 'baseUserDn', 'ldap_service_type': 'ldapServiceType', 'ldap_user_id_attribute': 'ldapUserIdAttribute', 'ldap_user_uuid_attribute': 'ldapUserUUIDAttribute', 'ldap_group_id_attribute': 'ldapGroupIdAttribute', 'ldap_group_uuid_attribute': 'ldapGroupUUIDAttribute', 'ca_cert': 'caCert'}
        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=True)
        self.na_helper = NetAppModule()
        self.parameters = self.na_helper.set_parameters(self.module.params)
        self.rest_api = SGRestAPI(self.module)
        self.data = {}
        if self.parameters['state'] == 'present':
            self.data['disable'] = False
        for k in parameter_map.keys():
            if self.parameters.get(k) is not None:
                self.data[parameter_map[k]] = self.parameters[k]
        if self.parameters.get('tls') == 'STARTTLS':
            self.data['disableTLS'] = False
            self.data['enableLDAPS'] = False
        elif self.parameters.get('tls') == 'LDAPS':
            self.data['disableTLS'] = False
            self.data['enableLDAPS'] = True
        else:
            self.data['disableTLS'] = True
            self.data['enableLDAPS'] = False

    def get_org_identity_source(self):
        api = 'api/v3/org/identity-source'
        (response, error) = self.rest_api.get(api)
        if error:
            self.module.fail_json(msg=error)
        else:
            return response['data']
        return None

    def update_identity_federation(self, test=False):
        api = 'api/v3/org/identity-source'
        params = {}
        if test:
            params['test'] = True
        (response, error) = self.rest_api.put(api, self.data, params=params)
        if error:
            self.module.fail_json(msg=error, payload=self.data)
        if response is not None:
            return response['data']
        else:
            return None

    def apply(self):
        """
        Perform pre-checks, call functions and exit
        """
        org_identity_source = self.get_org_identity_source()
        cd_action = self.na_helper.get_cd_action(org_identity_source, self.parameters)
        if cd_action is None and self.parameters['state'] == 'present':
            update = False
            for k in (i for i in self.data.keys() if i != 'password'):
                if self.data[k] != org_identity_source.get(k):
                    update = True
                    break
            if self.data.get('password') and self.parameters['state'] == 'present':
                update = True
                self.module.warn('Password attribute has been specified. Task is not idempotent.')
            if update:
                self.na_helper.changed = True
        if cd_action == 'delete':
            if org_identity_source.get('disable'):
                self.na_helper.changed = False
        result_message = ''
        resp_data = org_identity_source
        if self.na_helper.changed and (not self.module.check_mode):
            if cd_action == 'delete':
                self.data = dict(disable=True)
                resp_data = self.update_identity_federation()
                result_message = 'Tenant identity federation disabled'
            else:
                resp_data = self.update_identity_federation()
                result_message = 'Tenant identity federation updated'
        if self.module.check_mode:
            self.update_identity_federation(test=True)
            self.module.exit_json(changed=self.na_helper.changed, msg='Connection test successful')
        self.module.exit_json(changed=self.na_helper.changed, msg=result_message, resp=resp_data)

def main():
    """
    Main function
    """
    na_sg_org_identity_federation = SgOrgIdentityFederation()
    na_sg_org_identity_federation.apply()
if __name__ == '__main__':
    main()