from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.plugins.action import ActionBase
try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import AnsibleArgSpecValidator
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible.errors import AnsibleActionFail
from ansible_collections.cisco.dnac.plugins.plugin_utils.dnac import DNACSDK, dnac_argument_spec, dnac_compare_equality
from ansible_collections.cisco.dnac.plugins.plugin_utils.exceptions import InconsistentParameters
argument_spec = dnac_argument_spec()
argument_spec.update(dict(state=dict(type='str', default='present', choices=['present', 'absent']), profileDetails=dict(type='dict'), wirelessProfileName=dict(type='str')))
required_if = [('state', 'present', ['profileDetails'], True), ('state', 'absent', ['wirelessProfileName'], True)]
required_one_of = []
mutually_exclusive = []
required_together = []

class WirelessProfile(object):

    def __init__(self, params, dnac):
        self.dnac = dnac
        self.new_object = dict(profileDetails=params.get('profileDetails'), wireless_profile_name=params.get('wirelessProfileName'))

    def get_all_params(self, name=None, id=None):
        new_object_params = {}
        new_object_params['profile_name'] = name or self.new_object.get('wireless_profile_name')
        return new_object_params

    def create_params(self):
        new_object_params = {}
        new_object_params['profileDetails'] = self.new_object.get('profileDetails')
        return new_object_params

    def delete_by_name_params(self):
        new_object_params = {}
        new_object_params['wireless_profile_name'] = self.new_object.get('wireless_profile_name')
        return new_object_params

    def update_all_params(self):
        new_object_params = {}
        new_object_params['profileDetails'] = self.new_object.get('profileDetails')
        return new_object_params

    def get_object_by_name(self, name):
        result = None
        try:
            items = self.dnac.exec(family='wireless', function='get_wireless_profile', params=self.get_all_params(name=name))
            if isinstance(items, list):
                for i in items:
                    if isinstance(i, dict) and 'profileDetails' in i:
                        tmp = i.get('profileDetails')
                        if isinstance(tmp, dict) and tmp.get('name') == name:
                            result = dict(i)
                            break
        except Exception:
            result = None
        return result

    def get_object_by_id(self, id):
        result = None
        return result

    def exists(self):
        id_exists = False
        name_exists = False
        prev_obj = None
        o_id = self.new_object.get('id')
        name = self.new_object.get('name')
        name = name or self.new_object.get('wireless_profile_name')
        profile_details = self.new_object.get('profileDetails')
        if profile_details and profile_details.get('name'):
            name = name or profile_details.get('name')
        if o_id:
            prev_obj = self.get_object_by_id(o_id)
            id_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if not id_exists and name:
            prev_obj = self.get_object_by_name(name)
            name_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if id_exists:
            _name = prev_obj.get('name')
            _name = _name or prev_obj.get('wirelessProfileName')
            if _name:
                self.new_object.update(dict(wireless_profile_name=_name))
        if name_exists:
            _id = prev_obj.get('id')
            if id_exists and name_exists and (o_id != _id):
                raise InconsistentParameters("The 'id' and 'name' params don't refer to the same object")
            if _id:
                self.new_object.update(dict(id=_id))
        it_exists = prev_obj is not None and isinstance(prev_obj, dict)
        return (it_exists, prev_obj)

    def requires_update(self, current_obj):
        requested_obj = self.new_object
        obj_params = [('profileDetails', 'profileDetails'), ('wirelessProfileName', 'wireless_profile_name')]
        return any((not dnac_compare_equality(current_obj.get(dnac_param), requested_obj.get(ansible_param)) for dnac_param, ansible_param in obj_params))

    def create(self):
        result = self.dnac.exec(family='wireless', function='create_wireless_profile', params=self.create_params(), op_modifies=True)
        return result

    def update(self):
        id = self.new_object.get('id')
        name = self.new_object.get('name')
        result = None
        result = self.dnac.exec(family='wireless', function='update_wireless_profile', params=self.update_all_params(), op_modifies=True)
        return result

    def delete(self):
        id = self.new_object.get('id')
        name = self.new_object.get('name')
        name = name or self.new_object.get('wireless_profile_name')
        result = None
        if not name:
            prev_obj_id = self.get_object_by_id(id)
            name_ = None
            if prev_obj_id:
                name_ = prev_obj_id.get('name')
                name_ = name_ or prev_obj_id.get('wirelessProfileName')
            if name_:
                self.new_object.update(dict(wireless_profile_name=name_))
        result = self.dnac.exec(family='wireless', function='delete_wireless_profile', params=self.delete_by_name_params())
        return result

class ActionModule(ActionBase):

    def __init__(self, *args, **kwargs):
        if not ANSIBLE_UTILS_IS_INSTALLED:
            raise AnsibleActionFail("ansible.utils is not installed. Execute 'ansible-galaxy collection install ansible.utils'")
        super(ActionModule, self).__init__(*args, **kwargs)
        self._supports_async = False
        self._supports_check_mode = False
        self._result = None

    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(data=self._task.args, schema=dict(argument_spec=argument_spec), schema_format='argspec', schema_conditionals=dict(required_if=required_if, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive, required_together=required_together), name=self._task.action)
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result['changed'] = False
        self._check_argspec()
        dnac = DNACSDK(self._task.args)
        obj = WirelessProfile(self._task.args, dnac)
        state = self._task.args.get('state')
        response = None
        if state == 'present':
            obj_exists, prev_obj = obj.exists()
            if obj_exists:
                if obj.requires_update(prev_obj):
                    response = obj.update()
                    dnac.object_updated()
                else:
                    response = prev_obj
                    dnac.object_already_present()
            else:
                response = obj.create()
                dnac.object_created()
        elif state == 'absent':
            obj_exists, prev_obj = obj.exists()
            if obj_exists:
                response = obj.delete()
                dnac.object_deleted()
            else:
                dnac.object_already_absent()
        self._result.update(dict(dnac_response=response))
        self._result.update(dnac.exit_json())
        return self._result