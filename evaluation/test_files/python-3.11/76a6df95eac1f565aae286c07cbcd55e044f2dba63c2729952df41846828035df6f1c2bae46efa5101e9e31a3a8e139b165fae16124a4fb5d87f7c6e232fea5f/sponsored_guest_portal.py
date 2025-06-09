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
from ansible_collections.cisco.ise.plugins.plugin_utils.ise import ISESDK, ise_argument_spec, ise_compare_equality, get_dict_result
from ansible_collections.cisco.ise.plugins.plugin_utils.exceptions import InconsistentParameters
argument_spec = ise_argument_spec()
argument_spec.update(dict(state=dict(type='str', default='present', choices=['present', 'absent']), name=dict(type='str'), description=dict(type='str'), portalType=dict(type='str'), portalTestUrl=dict(type='str'), settings=dict(type='dict'), customizations=dict(type='dict'), id=dict(type='str')))
required_if = [('state', 'present', ['id', 'name', 'settings'], True), ('state', 'absent', ['id', 'name', 'settings'], True)]
required_one_of = []
mutually_exclusive = []
required_together = []

class SponsoredGuestPortal(object):

    def __init__(self, params, ise):
        self.ise = ise
        self.new_object = dict(name=params.get('name'), description=params.get('description'), portal_type=params.get('portalType'), portal_test_url=params.get('portalTestUrl'), settings=params.get('settings'), customizations=params.get('customizations'), id=params.get('id'))

    def get_object_by_name(self, name):
        result = None
        gen_items_responses = self.ise.exec(family='sponsored_guest_portal', function='get_sponsored_guest_portals_generator')
        try:
            for items_response in gen_items_responses:
                items = items_response.response['SearchResult']['resources']
                result = get_dict_result(items, 'name', name)
                if result:
                    return result
        except (TypeError, AttributeError) as e:
            self.ise.fail_json(msg='An error occured when executing operation. Check the configuration of your API Settings and API Gateway settings on your ISE server. This collection assumes that the API Gateway, the ERS APIs and OpenAPIs are enabled. You may want to enable the (ise_debug: True) argument. The error was: {error}'.format(error=e))
        except Exception:
            result = None
            return result
        return result

    def get_object_by_id(self, id):
        try:
            result = self.ise.exec(family='sponsored_guest_portal', function='get_sponsored_guest_portal_by_id', handle_func_exception=False, params={'id': id}).response['SponsoredGuestPortal']
        except (TypeError, AttributeError) as e:
            self.ise.fail_json(msg='An error occured when executing operation. Check the configuration of your API Settings and API Gateway settings on your ISE server. This collection assumes that the API Gateway, the ERS APIs and OpenAPIs are enabled. You may want to enable the (ise_debug: True) argument. The error was: {error}'.format(error=e))
        except Exception:
            result = None
        return result

    def exists(self):
        id_exists = False
        name_exists = False
        prev_obj = None
        o_id = self.new_object.get('id')
        name = self.new_object.get('name')
        if o_id:
            prev_obj = self.get_object_by_id(o_id)
            id_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if not id_exists and name:
            prev_obj = self.get_object_by_name(name)
            name_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if name_exists:
            _id = prev_obj.get('id')
            if id_exists and name_exists and (o_id != _id):
                raise InconsistentParameters("The 'id' and 'name' params don't refer to the same object")
            if _id:
                prev_obj = self.get_object_by_id(_id)
        it_exists = prev_obj is not None and isinstance(prev_obj, dict)
        return (it_exists, prev_obj)

    def requires_update(self, current_obj):
        requested_obj = self.new_object
        obj_params = [('name', 'name'), ('description', 'description'), ('portalType', 'portal_type'), ('portalTestUrl', 'portal_test_url'), ('settings', 'settings'), ('customizations', 'customizations'), ('id', 'id')]
        return any((not ise_compare_equality(current_obj.get(ise_param), requested_obj.get(ansible_param)) for ise_param, ansible_param in obj_params))

    def create(self):
        result = self.ise.exec(family='sponsored_guest_portal', function='create_sponsored_guest_portal', params=self.new_object).response
        return result

    def update(self):
        id = self.new_object.get('id')
        name = self.new_object.get('name')
        result = None
        if not id:
            id_ = self.get_object_by_name(name).get('id')
            self.new_object.update(dict(id=id_))
        result = self.ise.exec(family='sponsored_guest_portal', function='update_sponsored_guest_portal_by_id', params=self.new_object).response
        return result

    def delete(self):
        id = self.new_object.get('id')
        name = self.new_object.get('name')
        result = None
        if not id:
            id_ = self.get_object_by_name(name).get('id')
            self.new_object.update(dict(id=id_))
        result = self.ise.exec(family='sponsored_guest_portal', function='delete_sponsored_guest_portal_by_id', params=self.new_object).response
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
        ise = ISESDK(params=self._task.args)
        obj = SponsoredGuestPortal(self._task.args, ise)
        state = self._task.args.get('state')
        response = None
        if state == 'present':
            obj_exists, prev_obj = obj.exists()
            if obj_exists:
                if obj.requires_update(prev_obj):
                    ise_update_response = obj.update()
                    self._result.update(dict(ise_update_response=ise_update_response))
                    obj_exists, updated_obj = obj.exists()
                    response = updated_obj
                    has_changed = None
                    has_changed = ise_update_response.get('UpdatedFieldsList').get('updatedField')
                    if len(has_changed) == 0 or (has_changed[0].get('newValue') == '' and has_changed[0].get('newValue') == has_changed[0].get('oldValue')):
                        self._result.pop('ise_update_response', None)
                        ise.object_already_present()
                    else:
                        ise.object_updated()
                else:
                    response = prev_obj
                    ise.object_already_present()
            else:
                ise_create_response = obj.create()
                obj_exists, created_obj = obj.exists()
                response = created_obj
                ise.object_created()
        elif state == 'absent':
            obj_exists, prev_obj = obj.exists()
            if obj_exists:
                obj.delete()
                response = prev_obj
                ise.object_deleted()
            else:
                ise.object_already_absent()
        self._result.update(dict(ise_response=response))
        self._result.update(ise.exit_json())
        return self._result