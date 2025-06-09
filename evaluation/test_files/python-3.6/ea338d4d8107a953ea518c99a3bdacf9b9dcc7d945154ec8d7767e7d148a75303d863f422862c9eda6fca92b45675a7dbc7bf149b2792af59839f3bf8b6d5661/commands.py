import time
from argparse import Namespace
from typing import Dict, Optional
import bitmath
from croud.api import Client
from croud.clusters.exceptions import AsyncOperationNotFound
from croud.config import get_output_format
from croud.printer import print_error, print_info, print_response, print_success
from croud.tools.spinner import HALO
from croud.util import require_confirmation

def clusters_get(args: Namespace) -> None:
    client = Client.from_args(args)
    (data, errors) = client.get(f'/api/v2/clusters/{args.id}/')
    print_response(data=data, errors=errors, output_fmt=get_output_format(args))

def clusters_list(args: Namespace) -> None:
    if args.org_id:
        url = f'/api/v2/organizations/{args.org_id}/clusters/'
    else:
        url = '/api/v2/clusters/'
    params = {}
    if args.project_id:
        params['project_id'] = args.project_id
    client = Client.from_args(args)
    (data, errors) = client.get(url, params=params)
    print_response(data=data, errors=errors, keys=['id', 'name', 'num_nodes', 'crate_version', 'project_id', 'username', 'fqdn', 'channel'], output_fmt=get_output_format(args))

def clusters_deploy(args: Namespace) -> None:
    body = {'cluster': {'crate_version': args.version, 'name': args.cluster_name, 'password': args.password, 'product_name': args.product_name, 'product_tier': args.tier, 'username': args.username, 'channel': args.channel}, 'project_id': args.project_id, 'subscription_id': args.subscription_id}
    if args.unit:
        body['cluster']['product_unit'] = args.unit
    _handle_edge_params(body['cluster'], args)
    client = Client.from_args(args)
    org_id = _lookup_organization_id_for_project(client, args, args.project_id)
    if not org_id:
        return
    (data, errors) = client.post(f'/api/v2/organizations/{org_id}/clusters/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'fqdn', 'url'], output_fmt=get_output_format(args))
    if errors or not data:
        return
    print_info('Cluster creation initiated. It may take a few minutes to complete.')
    _wait_for_completed_operation(client=client, cluster_id=data['id'], request_params={'type': 'CREATE', 'limit': 1})
    (data, errors) = client.get(f"/api/v2/clusters/{data['id']}/")
    print_response(data=data, errors=errors, keys=['id', 'name', 'fqdn', 'url'], output_fmt=get_output_format(args))

def clusters_scale(args: Namespace) -> None:
    body = {'product_unit': args.unit}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/scale/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'num_nodes'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Cluster scaling initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'SCALE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'num_nodes'], output_fmt=get_output_format(args))

def clusters_upgrade(args: Namespace) -> None:
    body = {'crate_version': args.version}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/upgrade/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'crate_version'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Cluster upgrade initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'UPGRADE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'crate_version'], output_fmt=get_output_format(args))

@require_confirmation('Are you sure you want to delete the cluster?', cancel_msg='Cluster deletion cancelled.')
def clusters_delete(args: Namespace) -> None:
    client = Client.from_args(args)
    (data, errors) = client.delete(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, success_message='Cluster deleted.', output_fmt=get_output_format(args))

def clusters_restart_node(args: Namespace) -> None:
    client = Client.from_args(args)
    (data, errors) = client.delete(f'/api/v2/clusters/{args.cluster_id}/nodes/{args.ordinal}')
    print_response(data=data, errors=errors, keys=['code', 'status'], success_message='Node restarted. It may take a few minutes to complete the changes.', output_fmt=get_output_format(args))

def clusters_set_deletion_protection(args: Namespace) -> None:
    body = {'deletion_protected': args.value}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/deletion-protection/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'deletion_protected'], success_message='Cluster deletion protection status successfully updated', output_fmt=get_output_format(args))

def clusters_set_suspended(args: Namespace) -> None:
    body = {'suspended': args.value}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/suspend/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'suspended'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Updating the cluster status initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'SUSPEND', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'suspended'], output_fmt=get_output_format(args))

@require_confirmation('This will overwrite all existing CIDR restrictions. Continue?')
def clusters_set_ip_whitelist(args: Namespace) -> None:
    networks = args.net
    networks = networks.split(',')
    cidr = []
    for net in networks:
        if len(net) > 0:
            cidr.append({'cidr': net})
    body = {'ip_whitelist': cidr}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/ip-restrictions/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'ip_whitelist'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Updating the IP Network whitelist initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'ALLOWED_CIDR_UPDATE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'ip_whitelist'], output_fmt=get_output_format(args))

def _disk_size_transform(field):
    disk_size = str(bitmath.Byte(field['disk_size_per_node_bytes']).best_prefix())
    return f'Disk size: {disk_size}'

def clusters_expand_storage(args: Namespace) -> None:
    body = {'disk_size_per_node_bytes': args.disk_size_gb * 1024 * 1024 * 1024}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/storage/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'hardware_specs'], output_fmt=get_output_format(args), transforms={'hardware_specs': _disk_size_transform})
    if errors:
        return
    print_info('Cluster storage expansion initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'EXPAND_STORAGE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'hardware_specs'], output_fmt=get_output_format(args), transforms={'hardware_specs': _disk_size_transform})

def clusters_set_product(args: Namespace) -> None:
    body = {'product_name': args.product_name}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/product/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'product_name'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Changing the cluster product initiated. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'CHANGE_COMPUTE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'product_name'], output_fmt=get_output_format(args))

def clusters_set_backup_schedule(args: Namespace) -> None:
    body = {'backup_hours': args.backup_hours}
    client = Client.from_args(args)
    (data, errors) = client.put(f'/api/v2/clusters/{args.cluster_id}/backup-schedule/', body=body)
    print_response(data=data, errors=errors, keys=['id', 'name', 'backup_schedule'], output_fmt=get_output_format(args))
    if errors:
        return
    print_info('Changing the cluster backup schedule. It may take a few minutes to complete the changes.')
    _wait_for_completed_operation(client=client, cluster_id=args.cluster_id, request_params={'type': 'BACKUP_SCHEDULE_UPDATE', 'limit': 1})
    (data, errors) = client.get(f'/api/v2/clusters/{args.cluster_id}/')
    print_response(data=data, errors=errors, keys=['id', 'name', 'backup_schedule'], output_fmt=get_output_format(args))

def _handle_edge_params(body, args):
    if args.cpus:
        body.setdefault('hardware_specs', {})['cpus_per_node'] = args.cpus
    if args.disks:
        body.setdefault('hardware_specs', {})['disks_per_node'] = args.disks
    if args.disk_size_gb:
        body.setdefault('hardware_specs', {})['disk_size_per_node_bytes'] = args.disk_size_gb * 1024 * 1024 * 1024
    if args.disk_type:
        body.setdefault('hardware_specs', {})['disk_type'] = args.disk_type
    if args.memory_size_mb:
        body.setdefault('hardware_specs', {})['memory_per_node_bytes'] = args.memory_size_mb * 1024 * 1024

def _get_operation_status(client: Client, cluster_id: str, request_params: Dict):
    (data, errors) = client.get(f'/api/v2/clusters/{cluster_id}/operations/', params=request_params)
    if not data or len(data.get('operations', [])) == 0:
        raise AsyncOperationNotFound('Failed retrieving operation status.')
    operation = data['operations'][0]
    status = operation.get('status')
    feedback_data = operation.get('feedback_data', {})
    msg = feedback_data.get('message', None)
    return (status, msg)

def _wait_for_completed_operation(*, client: Client, cluster_id: str, request_params: Dict):
    last_status = None
    last_msg = None
    while True:
        try:
            (status, msg) = _get_operation_status(client=client, cluster_id=cluster_id, request_params=request_params)
        except AsyncOperationNotFound as e:
            print_error(str(e))
            break
        if status == 'SUCCEEDED':
            print_success('Operation completed.')
            break
        if status == 'FAILED':
            print_error('Your cluster operation has failed. Our operations team are investigating.')
            break
        if last_status != status or msg != last_msg:
            to_print = f'Status: {status} ({msg})' if msg else f'Status: {status}'
            print_info(to_print)
            last_status = status
            last_msg = msg
        with HALO:
            time.sleep(10)

def _lookup_organization_id_for_project(client: Client, args: Namespace, project_id: str) -> Optional[str]:
    (data, errors) = client.get(f'/api/v2/projects/{project_id}/')
    if not data or errors:
        print_response(data=data, errors=errors, output_fmt=get_output_format(args))
        return None
    return data.get('organization_id')