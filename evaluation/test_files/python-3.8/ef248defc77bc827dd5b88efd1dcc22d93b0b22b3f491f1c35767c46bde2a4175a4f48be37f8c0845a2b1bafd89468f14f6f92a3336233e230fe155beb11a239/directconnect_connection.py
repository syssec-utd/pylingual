DOCUMENTATION = '\n---\nmodule: directconnect_connection\nversion_added: 1.0.0\nshort_description: Creates, deletes, modifies a DirectConnect connection\ndescription:\n  - Create, update, or delete a Direct Connect connection between a network and a specific AWS Direct Connect location.\n  - Upon creation the connection may be added to a link aggregation group or established as a standalone connection.\n  - The connection may later be associated or disassociated with a link aggregation group.\n  - Prior to release 5.0.0 this module was called C(community.aws.aws_direct_connect_connection).\n    The usage did not change.\nauthor:\n  - "Sloane Hertel (@s-hertel)"\noptions:\n  state:\n    description:\n      - The state of the Direct Connect connection.\n    choices:\n      - present\n      - absent\n    type: str\n    required: true\n  name:\n    description:\n      - The name of the Direct Connect connection. This is required to create a\n        new connection.\n      - One of I(connection_id) or I(name) must be specified.\n    type: str\n  connection_id:\n    description:\n      - The ID of the Direct Connect connection.\n      - Modifying attributes of a connection with I(forced_update) will result in a new Direct Connect connection ID.\n      - One of I(connection_id) or I(name) must be specified.\n    type: str\n  location:\n    description:\n      - Where the Direct Connect connection is located.\n      - Required when I(state=present).\n    type: str\n  bandwidth:\n    description:\n      - The bandwidth of the Direct Connect connection.\n      - Required when I(state=present).\n    choices:\n      - 1Gbps\n      - 10Gbps\n    type: str\n  link_aggregation_group:\n    description:\n      - The ID of the link aggregation group you want to associate with the connection.\n      - This is optional when a stand-alone connection is desired.\n    type: str\n  forced_update:\n    description:\n      - To modify I(bandwidth) or I(location) the connection needs to be deleted and recreated.\n      - By default this will not happen.  This option must be explicitly set to C(true) to change I(bandwith) or I(location).\n    type: bool\n    default: false\nextends_documentation_fragment:\n  - amazon.aws.common.modules\n  - amazon.aws.region.modules\n  - amazon.aws.boto3\n'
EXAMPLES = '\n\n# create a Direct Connect connection\n- community.aws.directconnect_connection:\n    name: ansible-test-connection\n    state: present\n    location: EqDC2\n    link_aggregation_group: dxlag-xxxxxxxx\n    bandwidth: 1Gbps\n  register: dc\n\n# disassociate the LAG from the connection\n- community.aws.directconnect_connection:\n    state: present\n    connection_id: dc.connection.connection_id\n    location: EqDC2\n    bandwidth: 1Gbps\n\n# replace the connection with one with more bandwidth\n- community.aws.directconnect_connection:\n    state: present\n    name: ansible-test-connection\n    location: EqDC2\n    bandwidth: 10Gbps\n    forced_update: true\n\n# delete the connection\n- community.aws.directconnect_connection:\n    state: absent\n    name: ansible-test-connection\n'
RETURN = "\nconnection:\n  description: The attributes of the direct connect connection.\n  type: complex\n  returned: I(state=present)\n  contains:\n    aws_device:\n      description: The endpoint which the physical connection terminates on.\n      returned: when the requested state is no longer 'requested'\n      type: str\n      sample: EqDC2-12pmo7hemtz1z\n    bandwidth:\n      description: The bandwidth of the connection.\n      returned: always\n      type: str\n      sample: 1Gbps\n    connection_id:\n      description: The ID of the connection.\n      returned: always\n      type: str\n      sample: dxcon-ffy9ywed\n    connection_name:\n      description: The name of the connection.\n      returned: always\n      type: str\n      sample: ansible-test-connection\n    connection_state:\n      description: The state of the connection.\n      returned: always\n      type: str\n      sample: pending\n    loa_issue_time:\n      description: The issue time of the connection's Letter of Authorization - Connecting Facility Assignment.\n      returned: when the LOA-CFA has been issued (the connection state will no longer be 'requested')\n      type: str\n      sample: '2018-03-20T17:36:26-04:00'\n    location:\n      description: The location of the connection.\n      returned: always\n      type: str\n      sample: EqDC2\n    owner_account:\n      description: The account that owns the direct connect connection.\n      returned: always\n      type: str\n      sample: '123456789012'\n    region:\n      description: The region in which the connection exists.\n      returned: always\n      type: str\n      sample: us-east-1\n"
import traceback
try:
    from botocore.exceptions import BotoCoreError
    from botocore.exceptions import ClientError
except ImportError:
    pass
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.direct_connect import DirectConnectError
from ansible_collections.amazon.aws.plugins.module_utils.direct_connect import associate_connection_and_lag
from ansible_collections.amazon.aws.plugins.module_utils.direct_connect import delete_connection
from ansible_collections.amazon.aws.plugins.module_utils.direct_connect import disassociate_connection_and_lag
from ansible_collections.amazon.aws.plugins.module_utils.retries import AWSRetry
from ansible_collections.community.aws.plugins.module_utils.modules import AnsibleCommunityAWSModule as AnsibleAWSModule
retry_params = {'retries': 10, 'delay': 5, 'backoff': 1.2, 'catch_extra_error_codes': ['DirectConnectClientException']}

def connection_status(client, connection_id):
    return connection_exists(client, connection_id=connection_id, connection_name=None, verify=False)

def connection_exists(client, connection_id=None, connection_name=None, verify=True):
    params = {}
    if connection_id:
        params['connectionId'] = connection_id
    try:
        response = AWSRetry.jittered_backoff(**retry_params)(client.describe_connections)(**params)
    except (BotoCoreError, ClientError) as e:
        if connection_id:
            msg = f'Failed to describe DirectConnect ID {connection_id}'
        else:
            msg = 'Failed to describe DirectConnect connections'
        raise DirectConnectError(msg=msg, last_traceback=traceback.format_exc(), exception=e)
    match = []
    connection = []
    if len(response.get('connections', [])) == 1 and connection_id:
        if response['connections'][0]['connectionState'] != 'deleted':
            match.append(response['connections'][0]['connectionId'])
            connection.extend(response['connections'])
    for conn in response.get('connections', []):
        if connection_name == conn['connectionName'] and conn['connectionState'] != 'deleted':
            match.append(conn['connectionId'])
            connection.append(conn)
    if verify and len(match) == 1:
        return match[0]
    elif verify:
        return False
    elif len(connection) == 1:
        return {'connection': connection[0]}
    return {'connection': {}}

def create_connection(client, location, bandwidth, name, lag_id):
    if not name:
        raise DirectConnectError(msg='Failed to create a Direct Connect connection: name required.')
    params = {'location': location, 'bandwidth': bandwidth, 'connectionName': name}
    if lag_id:
        params['lagId'] = lag_id
    try:
        connection = AWSRetry.jittered_backoff(**retry_params)(client.create_connection)(**params)
    except (BotoCoreError, ClientError) as e:
        raise DirectConnectError(msg=f'Failed to create DirectConnect connection {name}', last_traceback=traceback.format_exc(), exception=e)
    return connection['connectionId']

def changed_properties(current_status, location, bandwidth):
    current_bandwidth = current_status['bandwidth']
    current_location = current_status['location']
    return current_bandwidth != bandwidth or current_location != location

@AWSRetry.jittered_backoff(**retry_params)
def update_associations(client, latest_state, connection_id, lag_id):
    changed = False
    if 'lagId' in latest_state and lag_id != latest_state['lagId']:
        disassociate_connection_and_lag(client, connection_id, lag_id=latest_state['lagId'])
        changed = True
    if changed and lag_id or (lag_id and 'lagId' not in latest_state):
        associate_connection_and_lag(client, connection_id, lag_id)
        changed = True
    return changed

def ensure_present(client, connection_id, connection_name, location, bandwidth, lag_id, forced_update):
    if connection_id:
        latest_state = connection_status(client, connection_id=connection_id)['connection']
        if changed_properties(latest_state, location, bandwidth) and forced_update:
            ensure_absent(client, connection_id)
            return ensure_present(client=client, connection_id=None, connection_name=connection_name, location=location, bandwidth=bandwidth, lag_id=lag_id, forced_update=forced_update)
        elif update_associations(client, latest_state, connection_id, lag_id):
            return (True, connection_id)
    else:
        return (True, create_connection(client, location, bandwidth, connection_name, lag_id))
    return (False, connection_id)

@AWSRetry.jittered_backoff(**retry_params)
def ensure_absent(client, connection_id):
    changed = False
    if connection_id:
        delete_connection(client, connection_id)
        changed = True
    return changed

def main():
    argument_spec = dict(state=dict(required=True, choices=['present', 'absent']), name=dict(), location=dict(), bandwidth=dict(choices=['1Gbps', '10Gbps']), link_aggregation_group=dict(), connection_id=dict(), forced_update=dict(type='bool', default=False))
    module = AnsibleAWSModule(argument_spec=argument_spec, required_one_of=[('connection_id', 'name')], required_if=[('state', 'present', ('location', 'bandwidth'))])
    connection = module.client('directconnect')
    state = module.params.get('state')
    try:
        connection_id = connection_exists(connection, connection_id=module.params.get('connection_id'), connection_name=module.params.get('name'))
        if not connection_id and module.params.get('connection_id'):
            module.fail_json(msg=f"The Direct Connect connection {module.params['connection_id']} does not exist.")
        if state == 'present':
            (changed, connection_id) = ensure_present(connection, connection_id=connection_id, connection_name=module.params.get('name'), location=module.params.get('location'), bandwidth=module.params.get('bandwidth'), lag_id=module.params.get('link_aggregation_group'), forced_update=module.params.get('forced_update'))
            response = connection_status(connection, connection_id)
        elif state == 'absent':
            changed = ensure_absent(connection, connection_id)
            response = {}
    except DirectConnectError as e:
        if e.last_traceback:
            module.fail_json(msg=e.msg, exception=e.last_traceback, **camel_dict_to_snake_dict(e.exception.response))
        else:
            module.fail_json(msg=e.msg)
    module.exit_json(changed=changed, **camel_dict_to_snake_dict(response))
if __name__ == '__main__':
    main()