from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: vmware_guest_customization_info\nshort_description: Gather info about VM customization specifications\ndescription:\n    - This module can be used to gather information about customization specifications.\n    - All parameters and VMware object names are case sensitive.\nauthor:\n    - Abhijeet Kasurde (@Akasurde)\noptions:\n   spec_name:\n     description:\n     - Name of customization specification to find.\n     required: false\n     type: str\nextends_documentation_fragment:\n- community.vmware.vmware.documentation\n\n'
EXAMPLES = '\n- name: Gather info about all customization specification\n  community.vmware.vmware_guest_customization_info:\n    hostname: "{{ vcenter_hostname }}"\n    username: "{{ vcenter_username }}"\n    password: "{{ vcenter_password }}"\n  delegate_to: localhost\n  register: all_custom_spec_info\n\n- name: Gather info about customization specification with the given name\n  community.vmware.vmware_guest_customization_info:\n    hostname: "{{ vcenter_hostname }}"\n    username: "{{ vcenter_username }}"\n    password: "{{ vcenter_password }}"\n    spec_name: custom_linux_spec\n  delegate_to: localhost\n  register: custom_spec_info\n'
RETURN = '\ncustom_spec_info:\n    description: metadata about the customization specification\n    returned: always\n    type: dict\n    sample: {\n        "assignip-eee0d684-44b7-457c-8c55-2585590b0d99": {\n            "change_version": "1523438001",\n            "description": "sample description",\n            "dns_server_list": [],\n            "dns_suffix_list": [],\n            "domain": "None",\n            "hostname": "sample1",\n            "hw_clock_utc": null,\n            "last_updated_time": "2018-04-11T09:13:21+00:00",\n            "name": "sample",\n            "nic_setting_map": [\n                {\n                    "dns_domain": null,\n                    "gateway": [],\n                    "ip_address": "192.168.10.10",\n                    "net_bios": null,\n                    "nic_dns_server_list": [],\n                    "primary_wins": null,\n                    "secondry_wins": null,\n                    "subnet_mask": "255.255.255.0"\n                }\n            ],\n            "time_zone": null,\n            "type": "Linux"\n        },\n    }\n'
try:
    from pyVmomi import vim
except ImportError:
    pass
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible_collections.community.vmware.plugins.module_utils.vmware import PyVmomi, vmware_argument_spec

class VmwareCustomSpecManger(PyVmomi):

    def __init__(self, module):
        super(VmwareCustomSpecManger, self).__init__(module)
        self.cc_mgr = self.content.customizationSpecManager
        if self.cc_mgr is None:
            self.module.fail_json(msg='Failed to get customization spec manager.')

    def gather_custom_spec_info(self):
        """
        Gather information about customization specifications
        """
        spec_name = self.params.get('spec_name', None)
        specs_list = []
        if spec_name:
            if self.cc_mgr.DoesCustomizationSpecExist(name=spec_name):
                specs_list.append(spec_name)
            else:
                self.module.fail_json(msg="Unable to find customization specification named '%s'" % spec_name)
        else:
            available_specs = self.cc_mgr.info
            for spec_info in available_specs:
                specs_list.append(spec_info.name)
        spec_info = dict()
        for spec in specs_list:
            current_spec = self.cc_mgr.GetCustomizationSpec(name=spec)
            adapter_mapping_list = []
            for nic in current_spec.spec.nicSettingMap:
                temp_data = dict(mac_address=nic.macAddress, ip_address=nic.adapter.ip.ipAddress if hasattr(nic.adapter.ip, 'ipAddress') else None, subnet_mask=nic.adapter.subnetMask, gateway=list(nic.adapter.gateway), nic_dns_server_list=list(nic.adapter.dnsServerList), dns_domain=nic.adapter.dnsDomain, primary_wins=nic.adapter.primaryWINS, secondry_wins=nic.adapter.secondaryWINS, net_bios=nic.adapter.netBIOS)
                adapter_mapping_list.append(temp_data)
            current_hostname = None
            domain = None
            time_zone = None
            hw_clock = None
            if isinstance(current_spec.spec.identity, vim.vm.customization.LinuxPrep):
                if isinstance(current_spec.spec.identity.hostName, vim.vm.customization.PrefixNameGenerator):
                    current_hostname = current_spec.spec.identity.hostName.base
                elif isinstance(current_spec.spec.identity.hostName, vim.vm.customization.FixedName):
                    current_hostname = current_spec.spec.identity.hostName.name
                domain = current_spec.spec.identity.domain
                time_zone = current_spec.spec.identity.timeZone
                hw_clock = current_spec.spec.identity.hwClockUTC
            else:
                time_zone = current_spec.spec.identity.guiUnattended.timeZone
            spec_info[spec] = dict(name=current_spec.info.name, description=current_spec.info.description, type=current_spec.info.type, last_updated_time=current_spec.info.lastUpdateTime, change_version=current_spec.info.changeVersion, hostname=current_hostname, domain=domain, time_zone=time_zone, hw_clock_utc=hw_clock, dns_suffix_list=list(current_spec.spec.globalIPSettings.dnsSuffixList), dns_server_list=list(current_spec.spec.globalIPSettings.dnsServerList), nic_setting_map=adapter_mapping_list)
        return spec_info

def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(spec_name=dict(type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    pyv = VmwareCustomSpecManger(module)
    try:
        module.exit_json(custom_spec_info=pyv.gather_custom_spec_info())
    except Exception as exc:
        module.fail_json(msg='Failed to gather information with exception : %s' % to_text(exc))
if __name__ == '__main__':
    main()