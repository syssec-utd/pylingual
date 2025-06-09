import sys
from reconcile.utils import gql
import reconcile.openshift_base as ob
from reconcile import queries
from reconcile.utils.semver_helper import make_semver
from reconcile.utils.openshift_resource import OpenshiftResource as OR, ResourceKeyExistsError
from reconcile.utils.defer import defer
from reconcile.utils import expiration
ROLES_QUERY = '\n{\n  roles: roles_v1 {\n    name\n    users {\n      org_username\n      github_username\n    }\n    bots {\n      openshift_serviceaccount\n    }\n    access {\n      cluster {\n        name\n        auth {\n          service\n        }\n      }\n      clusterRole\n    }\n    expirationDate\n  }\n}\n'
QONTRACT_INTEGRATION = 'openshift-clusterrolebindings'
QONTRACT_INTEGRATION_VERSION = make_semver(0, 1, 0)

def construct_user_oc_resource(role, user):
    name = f'{role}-{user}'
    body = {'apiVersion': 'rbac.authorization.k8s.io/v1', 'kind': 'ClusterRoleBinding', 'metadata': {'name': name}, 'roleRef': {'name': role, 'kind': 'ClusterRole'}, 'subjects': [{'kind': 'User', 'name': user}]}
    return (OR(body, QONTRACT_INTEGRATION, QONTRACT_INTEGRATION_VERSION, error_details=name), name)

def construct_sa_oc_resource(role, namespace, sa_name):
    name = f'{role}-{namespace}-{sa_name}'
    body = {'apiVersion': 'rbac.authorization.k8s.io/v1', 'kind': 'ClusterRoleBinding', 'metadata': {'name': name}, 'roleRef': {'name': role, 'kind': 'ClusterRole'}, 'subjects': [{'kind': 'ServiceAccount', 'name': sa_name, 'namespace': namespace}], 'userNames': [f'system:serviceaccount:{namespace}:{sa_name}']}
    return (OR(body, QONTRACT_INTEGRATION, QONTRACT_INTEGRATION_VERSION, error_details=name), name)

def fetch_desired_state(ri, oc_map):
    gqlapi = gql.get_api()
    roles = expiration.filter(gqlapi.query(ROLES_QUERY)['roles'])
    users_desired_state = []
    namepsace = 'cluster'
    for role in roles:
        permissions = [{'cluster': a['cluster'], 'cluster_role': a['clusterRole']} for a in role['access'] or [] if None not in [a['cluster'], a['clusterRole']]]
        if not permissions:
            continue
        service_accounts = [bot['openshift_serviceaccount'] for bot in role['bots'] if bot.get('openshift_serviceaccount')]
        for permission in permissions:
            cluster_info = permission['cluster']
            cluster = cluster_info['name']
            if not oc_map.get(cluster):
                continue
            user_key = ob.determine_user_key_for_access(cluster_info)
            for user in role['users']:
                users_desired_state.append({'cluster': cluster, 'user': user[user_key]})
                if ri is None:
                    continue
                (oc_resource, resource_name) = construct_user_oc_resource(permission['cluster_role'], user[user_key])
                try:
                    ri.add_desired(cluster, namepsace, 'ClusterRoleBinding', resource_name, oc_resource)
                except ResourceKeyExistsError:
                    pass
            for sa in service_accounts:
                if ri is None:
                    continue
                (namespace, sa_name) = sa.split('/')
                (oc_resource, resource_name) = construct_sa_oc_resource(permission['cluster_role'], namespace, sa_name)
                try:
                    ri.add_desired(cluster, namepsace, 'ClusterRoleBinding', resource_name, oc_resource)
                except ResourceKeyExistsError:
                    pass
    return users_desired_state

@defer
def run(dry_run, thread_pool_size=10, internal=None, use_jump_host=True, defer=None):
    clusters = [cluster_info for cluster_info in queries.get_clusters() if cluster_info.get('managedClusterRoles')]
    (ri, oc_map) = ob.fetch_current_state(clusters=clusters, thread_pool_size=thread_pool_size, integration=QONTRACT_INTEGRATION, integration_version=QONTRACT_INTEGRATION_VERSION, override_managed_types=['ClusterRoleBinding'], internal=internal, use_jump_host=use_jump_host)
    defer(oc_map.cleanup)
    fetch_desired_state(ri, oc_map)
    ob.realize_data(dry_run, oc_map, ri, thread_pool_size)
    if ri.has_error_registered():
        sys.exit(1)