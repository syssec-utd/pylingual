from __future__ import absolute_import, division, print_function
__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}
DOCUMENTATION = '\n---\nmodule: role\nauthor: "Wayne Witzel III (@wwitzel3)"\nshort_description: grant or revoke an Automation Platform Controller role.\ndescription:\n    - Roles are used for access control, this module is for managing user access to server resources.\n    - Grant or revoke Automation Platform Controller roles to users. See U(https://www.ansible.com/tower) for an overview.\noptions:\n    user:\n      description:\n        - User that receives the permissions specified by the role.\n        - Deprecated, use \'users\'.\n      type: str\n    users:\n      description:\n        - Users that receive the permissions specified by the role.\n      type: list\n      elements: str\n    team:\n      description:\n        - Team that receives the permissions specified by the role.\n        - Deprecated, use \'teams\'.\n      type: str\n    teams:\n      description:\n        - Teams that receive the permissions specified by the role.\n      type: list\n      elements: str\n    role:\n      description:\n        - The role type to grant/revoke.\n      required: True\n      choices: ["admin", "read", "member", "execute", "adhoc", "update", "use", "approval", "auditor", "project_admin", "inventory_admin", "credential_admin",\n                "workflow_admin", "notification_admin", "job_template_admin", "execution_environment_admin"]\n      type: str\n    target_team:\n      description:\n        - Team that the role acts on.\n        - For example, make someone a member or an admin of a team.\n        - Members of a team implicitly receive the permissions that the team has.\n        - Deprecated, use \'target_teams\'.\n      type: str\n    target_teams:\n      description:\n        - Team that the role acts on.\n        - For example, make someone a member or an admin of a team.\n        - Members of a team implicitly receive the permissions that the team has.\n      type: list\n      elements: str\n    inventory:\n      description:\n        - Inventory the role acts on.\n        - Deprecated, use \'inventories\'.\n      type: str\n    inventories:\n      description:\n        - Inventory the role acts on.\n      type: list\n      elements: str\n    job_template:\n      description:\n        - The job template the role acts on.\n        - Deprecated, use \'job_templates\'.\n      type: str\n    job_templates:\n      description:\n        - The job template the role acts on.\n      type: list\n      elements: str\n    workflow:\n      description:\n        - The workflow job template the role acts on.\n        - Deprecated, use \'workflows\'.\n      type: str\n    workflows:\n      description:\n        - The workflow job template the role acts on.\n      type: list\n      elements: str\n    credential:\n      description:\n        - Credential the role acts on.\n        - Deprecated, use \'credentials\'.\n      type: str\n    credentials:\n      description:\n        - Credential the role acts on.\n      type: list\n      elements: str\n    organization:\n      description:\n        - Organization the role acts on.\n        - Deprecated, use \'organizations\'.\n      type: str\n    organizations:\n      description:\n        - Organization the role acts on.\n      type: list\n      elements: str\n    lookup_organization:\n      description:\n        - Organization the inventories, job templates, projects, or workflows the items exists in.\n        - Used to help lookup the object, for organization roles see organization.\n        - If not provided, will lookup by name only, which does not work with duplicates.\n      type: str\n    project:\n      description:\n        - Project the role acts on.\n        - Deprecated, use \'projects\'.\n      type: str\n    projects:\n      description:\n        - Project the role acts on.\n      type: list\n      elements: str\n    instance_groups:\n      description:\n        - Instance Group the role acts on.\n      type: list\n      elements: str\n    state:\n      description:\n        - Desired state.\n        - State of present indicates the user should have the role.\n        - State of absent indicates the user should have the role taken away, if they have it.\n      default: "present"\n      choices: ["present", "absent"]\n      type: str\n\nextends_documentation_fragment: awx.awx.auth\n'
EXAMPLES = '\n- name: Add jdoe to the member role of My Team\n  role:\n    user: jdoe\n    target_team: "My Team"\n    role: member\n    state: present\n\n- name: Add Joe to multiple job templates and a workflow\n  role:\n    user: joe\n    role: execute\n    workflows:\n      - test-role-workflow\n    job_templates:\n      - jt1\n      - jt2\n    state: present\n'
from ..module_utils.controller_api import ControllerAPIModule

def main():
    argument_spec = dict(user=dict(), users=dict(type='list', elements='str'), team=dict(), teams=dict(type='list', elements='str'), role=dict(choices=['admin', 'read', 'member', 'execute', 'adhoc', 'update', 'use', 'approval', 'auditor', 'project_admin', 'inventory_admin', 'credential_admin', 'workflow_admin', 'notification_admin', 'job_template_admin', 'execution_environment_admin'], required=True), target_team=dict(), target_teams=dict(type='list', elements='str'), inventory=dict(), inventories=dict(type='list', elements='str'), job_template=dict(), job_templates=dict(type='list', elements='str'), workflow=dict(), workflows=dict(type='list', elements='str'), credential=dict(), credentials=dict(type='list', elements='str'), organization=dict(), organizations=dict(type='list', elements='str'), lookup_organization=dict(), project=dict(), projects=dict(type='list', elements='str'), instance_groups=dict(type='list', elements='str'), state=dict(choices=['present', 'absent'], default='present'))
    module = ControllerAPIModule(argument_spec=argument_spec)
    role_type = module.params.pop('role')
    role_field = role_type + '_role'
    state = module.params.pop('state')
    module.json_output['role'] = role_type
    resource_list_param_keys = {'credentials': 'credential', 'inventories': 'inventory', 'job_templates': 'job_template', 'organizations': 'organization', 'projects': 'project', 'target_teams': 'target_team', 'workflows': 'workflow', 'users': 'user', 'teams': 'team'}
    resources = {}
    for resource_group, old_name in resource_list_param_keys.items():
        if module.params.get(resource_group) is not None:
            resources.setdefault(resource_group, []).extend(module.params.get(resource_group))
        if module.params.get(old_name) is not None:
            resources.setdefault(resource_group, []).append(module.params.get(old_name))
    if module.params.get('lookup_organization') is not None:
        resources['lookup_organization'] = module.params.get('lookup_organization')
    if 'workflows' in resources:
        resources['workflow_job_templates'] = resources.pop('workflows')
    if 'target_teams' in resources:
        resources['teams'] = resources.pop('target_teams')
    lookup_data = {}
    if 'lookup_organization' in resources:
        lookup_data['organization'] = module.resolve_name_to_id('organizations', resources['lookup_organization'])
        resources.pop('lookup_organization')
    actor_data = {}
    missing_items = []
    resource_data = {}
    for key, value in resources.items():
        for resource in value:
            if key in resources:
                if key == 'organizations' or key == 'users':
                    lookup_data_populated = {}
                else:
                    lookup_data_populated = lookup_data
            data = module.get_one(key, name_or_id=resource, data=lookup_data_populated)
            if data is None:
                missing_items.append(resource)
            elif key == 'users' or key == 'teams':
                actor_data.setdefault(key, []).append(data)
            else:
                resource_data.setdefault(key, []).append(data)
    if len(missing_items) > 0:
        module.fail_json(msg='There were {0} missing items, missing items: {1}'.format(len(missing_items), missing_items), changed=False)
    associations = {}
    for actor_type, actors in actor_data.items():
        for key, value in resource_data.items():
            for resource in value:
                resource_roles = resource['summary_fields']['object_roles']
                if role_field not in resource_roles:
                    available_roles = ', '.join(list(resource_roles.keys()))
                    module.fail_json(msg='Resource {0} has no role {1}, available roles: {2}'.format(resource['url'], role_field, available_roles), changed=False)
                role_data = resource_roles[role_field]
                endpoint = '/roles/{0}/{1}/'.format(role_data['id'], actor_type)
                associations.setdefault(endpoint, [])
                for actor in actors:
                    associations[endpoint].append(actor['id'])
    for association_endpoint, new_association_list in associations.items():
        response = module.get_all_endpoint(association_endpoint)
        existing_associated_ids = [association['id'] for association in response['json']['results']]
        if state == 'present':
            for an_id in list(set(new_association_list) - set(existing_associated_ids)):
                response = module.post_endpoint(association_endpoint, **{'data': {'id': int(an_id)}})
                if response['status_code'] == 204:
                    module.json_output['changed'] = True
                else:
                    module.fail_json(msg='Failed to grant role. {0}'.format(response['json'].get('detail', response['json'].get('msg', 'unknown'))))
        else:
            for an_id in list(set(existing_associated_ids) & set(new_association_list)):
                response = module.post_endpoint(association_endpoint, **{'data': {'id': int(an_id), 'disassociate': True}})
                if response['status_code'] == 204:
                    module.json_output['changed'] = True
                else:
                    module.fail_json(msg='Failed to revoke role. {0}'.format(response['json'].get('detail', response['json'].get('msg', 'unknown'))))
    module.exit_json(**module.json_output)
if __name__ == '__main__':
    main()