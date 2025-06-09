""" unit tests ONTAP Ansible module: na_ontap_software_update """
from __future__ import absolute_import, division, print_function
__metaclass__ = type
import pytest
import sys
from ansible_collections.netapp.ontap.tests.unit.compat.mock import patch
from ansible_collections.netapp.ontap.tests.unit.plugins.module_utils.ansible_mocks import assert_warning_was_raised, expect_and_capture_ansible_exception, call_main, create_module, create_and_apply, patch_ansible, print_warnings
from ansible_collections.netapp.ontap.tests.unit.framework.mock_rest_and_zapi_requests import patch_request_and_invoke, register_responses
from ansible_collections.netapp.ontap.tests.unit.framework.rest_factory import JOB_GET_API, rest_error_message, rest_responses
from ansible_collections.netapp.ontap.tests.unit.framework.zapi_factory import build_zapi_error, build_zapi_response, zapi_error_message, zapi_responses
import ansible_collections.netapp.ontap.plugins.module_utils.netapp as netapp_utils
from ansible_collections.netapp.ontap.plugins.modules.na_ontap_software_update import NetAppONTAPSoftwareUpdate as my_module, main as my_main
if not netapp_utils.has_netapp_lib():
    pytestmark = pytest.mark.skip('skipping as missing required netapp_lib')
if not netapp_utils.HAS_REQUESTS and sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('Skipping Unit Tests on 2.6 as requests is not available')

def cluster_image_info(mixed=False):
    version1 = 'Fattire__9.3.0'
    version2 = version1
    if mixed:
        version2 += '.1'
    return {'num-records': 1, 'attributes-list': [{'cluster-image-info': {'node-id': 'node4test', 'current-version': version1}}, {'cluster-image-info': {'node-id': 'node4test', 'current-version': version2}}], 'attributes': {'cluster-image-info': {'node-id': 'node4test', 'current-version': version1}}}

def software_update_info(status):
    if status == 'async_pkg_get_phase_complete':
        overall_status = 'completed'
    elif status == 'async_pkg_get_phase_running':
        overall_status = 'in_progress'
    else:
        overall_status = status
    return {'num-records': 1, 'progress-status': status, 'progress-details': 'some_details', 'failure-reason': 'failure_reason', 'attributes': {'ndu-progress-info': {'overall-status': overall_status, 'completed-node-count': '0', 'validation-reports': [{'validation-report-info': {'one_check': 'one', 'two_check': 'two'}}]}}}
cluster_image_validation_report_list = {'cluster-image-validation-report-list': [{'cluster-image-validation-report-list-info': {'required-action': {'required-action-info': {'action': 'some_action', 'advice': 'some_advice', 'error': 'some_error'}}, 'ndu-check': 'ndu_ck', 'ndu-status': 'ndu_st'}}, {'cluster-image-validation-report-list-info': {'required-action': {'required-action-info': {'action': 'other_action', 'advice': 'other_advice', 'error': 'other_error'}}, 'ndu-check': 'ndu_ck', 'ndu-status': 'ndu_st'}}]}
cluster_image_package_local_info = {'attributes-list': [{'cluster-image-package-local-info': {'package-version': 'Fattire__9.3.0'}}, {'cluster-image-package-local-info': {'package-version': 'Fattire__9.3.1'}}]}
ZRR = zapi_responses({'cluster_image_info': build_zapi_response(cluster_image_info()), 'cluster_image_info_mixed': build_zapi_response(cluster_image_info(True)), 'software_update_info_running': build_zapi_response(software_update_info('async_pkg_get_phase_running')), 'software_update_info_complete': build_zapi_response(software_update_info('async_pkg_get_phase_complete')), 'software_update_info_error': build_zapi_response(software_update_info('error')), 'cluster_image_validation_report_list': build_zapi_response(cluster_image_validation_report_list), 'cluster_image_package_local_info': build_zapi_response(cluster_image_package_local_info, 2), 'error_18408': build_zapi_error(18408, 'pkg exists!')})

def cluster_software_node_info(mixed=False):
    version1 = 'Fattire__9.3.0'
    version2 = 'GEN_MAJ_min_2' if mixed else version1
    return {'nodes': [{'name': 'node1', 'version': version1}, {'name': 'node2', 'version': version2}]}

def cluster_software_state_info(state):
    return {'state': state}
cluster_software_validation_results = {'validation_results': [{'action': {'message': 'Use NFS hard mounts, if possible.'}, 'issue': {'message': 'Cluster HA is not configured in the cluster.'}, 'status': 'warning', 'update_check': 'nfs_mounts'}]}

def cluster_software_download_info(state):
    return {'message': 'message', 'state': state}
SRR = rest_responses({'cluster_software_node_info': (200, cluster_software_node_info(), None), 'cluster_software_node_info_mixed': (200, cluster_software_node_info(True), None), 'cluster_software_validation_results': (200, cluster_software_validation_results, None), 'cluster_software_state_completed': (200, cluster_software_state_info('completed'), None), 'cluster_software_state_in_progress': (200, cluster_software_state_info('in_progress'), None), 'cluster_software_state_in_error': (200, cluster_software_state_info('in_error'), None), 'cluster_software_download_state_success': (200, cluster_software_download_info('success'), None), 'cluster_software_download_state_running': (200, cluster_software_download_info('running'), None), 'cluster_software_package_info_ft': (200, {'records': [{'version': 'Fattire__9.3.0'}]}, None), 'cluster_software_package_info_pte': (200, {'records': [{'version': 'PlinyTheElder'}]}, None), 'error_image_already_exists': (200, {}, 'Package image with the same name already exists'), 'error_download_in_progress': (200, {}, 'Software get operation already in progress')})
DEFAULT_ARGS = {'hostname': 'hostname', 'username': 'username', 'password': 'password', 'package_version': 'Fattire__9.3.0', 'package_url': 'abc.com', 'https': 'true', 'stabilize_minutes': 10}

@patch('time.sleep')
def test_ensure_apply_for_update_called(dont_sleep):
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-update', ZRR['success']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-package-delete', ZRR['success'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_ensure_apply_for_update_called_node(dont_sleep):
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-update', ZRR['success']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-package-delete', ZRR['success'])])
    module_args = {'use_rest': 'never', 'nodes': ['node_abc'], 'package_version': 'PlinyTheElder'}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_ensure_apply_for_update_called_idempotent(dont_sleep):
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info'])])
    module_args = {'use_rest': 'never'}
    assert not create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_ensure_apply_for_update_called_idempotent_node(dont_sleep):
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get', ZRR['cluster_image_info'])])
    module_args = {'use_rest': 'never', 'nodes': ['node_abc']}
    assert not create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_ensure_apply_for_update_called_with_validation(dont_sleep):
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-validate', ZRR['success']), ('ZAPI', 'cluster-image-update', ZRR['success']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-package-delete', ZRR['success'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder', 'validate_after_download': True}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_negative_download_error(dont_sleep):
    """ downloading software - error while downloading the image - first request """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = zapi_error_message('Error downloading cluster image package for abc.com')
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_download_progress_error(dont_sleep):
    """ downloading software - error while downloading the image - progress error """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = 'Error downloading package: failure_reason'
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_download_progress_error_no_status(dont_sleep):
    """ downloading software - error while downloading the image - progress error """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = 'Error downloading package: failure_reason'
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_download_progress_error_fetching_status(dont_sleep):
    """ downloading software - error while downloading the image - progress error """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = zapi_error_message('Error fetching cluster image package download progress for abc.com')
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_update_error_zapi(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-update', ZRR['error']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['error']), ('ZAPI', 'cluster-image-validate', ZRR['error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = zapi_error_message('Error updating cluster image for PlinyTheElder')
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_update_error(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-update', ZRR['success']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_error']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_error'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = 'Error updating image using ZAPI: overall_status: error.'
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_negative_update_error_timeout(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_running']), ('ZAPI', 'cluster-image-get-download-progress', ZRR['software_update_info_complete']), ('ZAPI', 'cluster-image-update', ZRR['success']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_error']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['software_update_info_running'])])
    module_args = {'use_rest': 'never', 'package_version': 'PlinyTheElder'}
    error = 'Timeout error updating image using ZAPI: overall_status: in_progress.  Should the timeout value be increased?  Current value is 1800 seconds.  The software update continues in background.'
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.has_netapp_lib')
def test_fail_netapp_lib_error(mock_has_netapp_lib):
    mock_has_netapp_lib.return_value = False
    module_args = {'use_rest': 'never'}
    assert 'Error: the python NetApp-Lib module is required.  Import error: None' == call_main(my_main, DEFAULT_ARGS, module_args, fail=True)['msg']

def test_fail_with_http():
    args = dict(DEFAULT_ARGS)
    args.pop('https')
    assert 'Error: https parameter must be True' == call_main(my_main, args, fail=True)['msg']

def test_is_update_required():
    """ update is required if nodes have different images, or version does not match """
    register_responses([('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info_mixed']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info']), ('ZAPI', 'cluster-image-get-iter', ZRR['cluster_image_info_mixed'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert not my_obj.is_update_required()
    assert my_obj.is_update_required()
    my_obj.parameters['package_version'] = 'PlinyTheElder'
    assert my_obj.is_update_required()
    assert my_obj.is_update_required()

def test_cluster_image_validate():
    """ check error, then check that reports are read correctly """
    register_responses([('ZAPI', 'cluster-image-validate', ZRR['error']), ('ZAPI', 'cluster-image-validate', ZRR['cluster_image_validation_report_list'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert my_obj.cluster_image_validate() == zapi_error_message('Error running cluster image validate')
    reports = my_obj.cluster_image_validate()
    assert 'required_action' in reports[0]
    assert 'action' in reports[0]['required_action']
    assert reports[0]['required_action']['action'] == 'some_action'
    assert reports[1]['required_action']['action'] == 'other_action'

def test_cluster_image_zapi_errors():
    """ ZAPi error on delete """
    register_responses([('ZAPI', 'cluster-image-get-iter', ZRR['error']), ('ZAPI', 'cluster-image-get', ZRR['error']), ('ZAPI', 'cluster-image-package-delete', ZRR['error']), ('ZAPI', 'cluster-image-package-local-get-iter', ZRR['error'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_get_versions, 'fail')['msg'] == zapi_error_message('Error fetching cluster image details: Fattire__9.3.0')
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_get_for_node, 'fail', 'node')['msg'] == zapi_error_message('Error fetching cluster image details for node')
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_package_delete, 'fail')['msg'] == zapi_error_message('Error deleting cluster image package for Fattire__9.3.0')
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_packages_get_zapi, 'fail')['msg'] == zapi_error_message('Error getting list of local packages')

def test_cluster_image_get_for_node_none_none():
    """ empty response on get """
    register_responses([('ZAPI', 'cluster-image-get', ZRR['success'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert my_obj.cluster_image_get_for_node('node') == (None, None)

def test_cluster_image_package_download():
    """ ZAPI error on download - package already exists"""
    register_responses([('ZAPI', 'cluster-image-package-download', ZRR['error']), ('ZAPI', 'cluster-image-package-download', ZRR['error_18408']), ('ZAPI', 'cluster-image-package-local-get-iter', ZRR['cluster_image_package_local_info']), ('ZAPI', 'cluster-image-package-download', ZRR['success'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_package_download, 'fail')['msg'] == zapi_error_message('Error downloading cluster image package for abc.com')
    assert my_obj.cluster_image_package_download()
    assert not my_obj.cluster_image_package_download()

def test_cluster_image_update_progress_get_error():
    """ ZAPI error on progress get """
    register_responses([('ZAPI', 'cluster-image-update-progress-info', ZRR['error']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['error']), ('ZAPI', 'cluster-image-update-progress-info', ZRR['error'])])
    module_args = {'use_rest': 'never'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_update_progress_get, 'fail', ignore_connection_error=False)['msg'] == zapi_error_message('Error fetching cluster image update progress details')
    assert my_obj.cluster_image_update_progress_get() == {}
    assert my_obj.cluster_image_update_progress_get(ignore_connection_error=True) == {}

def test_delete_package_zapi():
    register_responses([('ZAPI', 'cluster-image-package-local-get-iter', ZRR['cluster_image_package_local_info']), ('ZAPI', 'cluster-image-package-delete', ZRR['success']), ('ZAPI', 'cluster-image-package-local-get-iter', ZRR['no_records'])])
    module_args = {'use_rest': 'never', 'state': 'absent', 'package_version': 'Fattire__9.3.0'}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']
    assert not create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_ensure_apply_for_update_called(dont_sleep):
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success_with_job_uuid']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['generic_error']), ('GET', JOB_GET_API, SRR['job_generic_response_success']), ('PATCH', 'cluster/software', SRR['success_with_job_uuid']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['generic_error']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_success']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['cluster_software_state_completed']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('DELETE', 'cluster/software/packages/PlinyTheElder', SRR['success_with_job_uuid']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_success'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder'}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_ensure_apply_for_update_called_idempotent(dont_sleep):
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info'])])
    module_args = {'use_rest': 'always'}
    assert not create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_ensure_apply_for_update_called_with_validation(dont_sleep):
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['success']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('PATCH', 'cluster/software', SRR['success']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['cluster_software_state_completed']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('DELETE', 'cluster/software/packages/PlinyTheElder', SRR['success'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'validate_after_download': True}
    assert create_and_apply(my_module, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_download_idempotent_package_already_exist_pre(dont_sleep):
    """ downloading software - package already present before attempting download """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_pte']), ('GET', 'cluster/software', SRR['cluster_software_node_info'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'download_only': True}
    assert not call_main(my_main, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_download_idempotent_package_already_exist_post(dont_sleep):
    """ downloading software - package already present when attempting download """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['error_image_already_exists']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_pte'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'download_only': True}
    assert not call_main(my_main, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_download_already_in_progress(dont_sleep):
    """ downloading software - package already present when attempting download """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['error_download_in_progress']), ('GET', 'cluster/software/download', SRR['cluster_software_download_state_running']), ('GET', 'cluster/software/download', SRR['generic_error']), ('GET', 'cluster/software/download', SRR['generic_error']), ('GET', 'cluster/software/download', SRR['cluster_software_download_state_running']), ('GET', 'cluster/software/download', SRR['cluster_software_download_state_success'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'download_only': True}
    assert not call_main(my_main, DEFAULT_ARGS, module_args)['changed']

@patch('time.sleep')
def test_rest_negative_download_package_already_exist(dont_sleep):
    """ downloading software - error while downloading the image - first request """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['error_image_already_exists']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_ft'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'download_only': True}
    error = 'Error: another package with the same file name exists: found: Fattire__9.3.0'
    assert error in call_main(my_main, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_rest_negative_download_error(dont_sleep):
    """ downloading software - error while downloading the image - first request """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['generic_error'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder'}
    error = rest_error_message('Error downloading software', 'cluster/software/download', ' - current versions:')
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_rest_negative_download_progress_error(dont_sleep):
    """ downloading software - error while downloading the image - progress error """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success_with_job_uuid']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_running']), ('GET', JOB_GET_API, SRR['job_generic_response_failure'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder'}
    error = 'Error downloading software: job reported error: job reported failure, received'
    assert error in create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']

@patch('time.sleep')
def test_rest_negative_update_error_sync(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder'}
    error = rest_error_message('Error updating software', 'cluster/software')
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'validation results:' in msg
    assert "'issue': {'message': 'Cluster HA is not configured in the cluster.'}" in msg
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'validation results:' in msg
    assert 'validation results: Error fetching software information for validation_results:' in msg

@patch('time.sleep')
def test_rest_negative_update_error_waiting_for_state(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['success']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['success']), ('GET', 'cluster/software', SRR['cluster_software_state_in_progress']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'timeout': 240}
    error = rest_error_message('Error: unable to read image update state, using timeout 240.  Last error: Error fetching software information for state', 'cluster/software')
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'All errors:' in msg
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'timeout': 1800}
    error = rest_error_message('Error: unable to read image update state, using timeout 1800.  Last error: Error fetching software information for state', 'cluster/software')
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'All errors:' in msg

@patch('time.sleep')
def test_rest_negative_update_error_job_errors(dont_sleep):
    """ updating software - error while updating the image """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('POST', 'cluster/software/download', SRR['success']), ('PATCH', 'cluster/software', SRR['generic_error']), ('GET', 'cluster/software', SRR['generic_error'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder'}
    error = rest_error_message('Error updating software', 'cluster/software')
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'validation results:' in msg
    assert "'issue': {'message': 'Cluster HA is not configured in the cluster.'}" in msg
    msg = create_and_apply(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert error in msg
    assert 'validation results:' in msg
    assert 'validation results: Error fetching software information for validation_results:' in msg

def test_rest_is_update_required():
    """ update is required if nodes have different images, or version does not match """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info_mixed']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info_mixed'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert not my_obj.is_update_required()
    assert my_obj.is_update_required()
    my_obj.parameters['package_version'] = 'PlinyTheElder'
    assert my_obj.is_update_required()
    assert my_obj.is_update_required()

@patch('time.sleep')
def test_rest_cluster_image_validate(dont_sleep):
    """ check error, then check that reports are read correctly """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('PATCH', 'cluster/software', SRR['generic_error']), ('PATCH', 'cluster/software', SRR['success']), ('GET', 'cluster/software', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_validation_results'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert my_obj.cluster_image_validate() == rest_error_message('Error validating software', 'cluster/software')
    reports = my_obj.cluster_image_validate()
    assert 'action' in reports[0]
    assert 'issue' in reports[0]

def test_rest_cluster_image_errors():
    """ REST error on get and delete """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software', SRR['generic_error']), ('DELETE', 'cluster/software/packages/Fattire__9.3.0', SRR['generic_error'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_get_versions, 'fail')['msg'] == rest_error_message('Error fetching software information for nodes', 'cluster/software')
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_package_delete, 'fail')['msg'] == rest_error_message('Error deleting cluster software package for Fattire__9.3.0', 'cluster/software/packages/Fattire__9.3.0')

def test_rest_cluster_image_get_for_node_versions():
    """ getting nodes versions """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info']), ('GET', 'cluster/software', SRR['cluster_software_node_info'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert my_obj.cluster_image_get_rest('versions') == [('node1', 'Fattire__9.3.0'), ('node2', 'Fattire__9.3.0')]
    my_obj.parameters['nodes'] = ['node1']
    assert my_obj.cluster_image_get_rest('versions') == [('node1', 'Fattire__9.3.0')]
    my_obj.parameters['nodes'] = ['node2']
    assert my_obj.cluster_image_get_rest('versions') == [('node2', 'Fattire__9.3.0')]
    my_obj.parameters['nodes'] = ['node2', 'node3']
    error = 'Error: node not found in cluster: node3.'
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_get_rest, 'fail', 'versions')['msg'] == error
    my_obj.parameters['nodes'] = ['node4', 'node3']
    error = 'Error: nodes not found in cluster: node4, node3.'
    assert expect_and_capture_ansible_exception(my_obj.cluster_image_get_rest, 'fail', 'versions')['msg'] == error

def test_rest_negative_cluster_image_get_for_node_versions():
    """ getting nodes versions """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software', SRR['zero_records']), ('GET', 'cluster/software', SRR['cluster_software_validation_results'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    error = 'Error fetching software information for nodes: no record calling cluster/software'
    assert error in expect_and_capture_ansible_exception(my_obj.cluster_image_get_rest, 'fail', 'versions')['msg']
    error = "Unexpected results for what: versions, record: {'validation_results':"
    assert error in expect_and_capture_ansible_exception(my_obj.cluster_image_get_rest, 'fail', 'versions')['msg']

def test_rest_cluster_image_package_download():
    """ download error, download error indicating package exists, successful download """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('POST', 'cluster/software/download', SRR['generic_error']), ('POST', 'cluster/software/download', SRR['error_image_already_exists']), ('GET', 'cluster/software/packages', SRR['zero_records']), ('POST', 'cluster/software/download', SRR['success'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    error = rest_error_message('Error downloading software', 'cluster/software/download', " - current versions: ['not available with force_update']")
    assert error in expect_and_capture_ansible_exception(my_obj.download_software_rest, 'fail')['msg']
    error = 'Error: ONTAP reported package already exists, but no package found: '
    assert error in expect_and_capture_ansible_exception(my_obj.download_software_rest, 'fail')['msg']
    assert not my_obj.download_software_rest()

def test_rest_post_update_tasks():
    """ validate success and error messages """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('DELETE', 'cluster/software/packages/Fattire__9.3.0', SRR['success']), ('GET', 'cluster/software', SRR['cluster_software_validation_results']), ('GET', 'cluster/software', SRR['cluster_software_validation_results'])])
    module_args = {'use_rest': 'always'}
    my_obj = create_module(my_module, DEFAULT_ARGS, module_args)
    assert my_obj.post_update_tasks_rest('completed') == cluster_software_validation_results['validation_results']
    error = 'Timeout error updating image using REST: state: in_progress.'
    assert error in expect_and_capture_ansible_exception(my_obj.post_update_tasks_rest, 'fail', 'in_progress')['msg']
    error = 'Error updating image using REST: state: error_state.'
    assert error in expect_and_capture_ansible_exception(my_obj.post_update_tasks_rest, 'fail', 'error_state')['msg']

def test_rest_delete_package():
    """ deleting package """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_pte']), ('DELETE', 'cluster/software/packages/PlinyTheElder', SRR['success']), ('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_ft'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'state': 'absent'}
    assert call_main(my_main, DEFAULT_ARGS, module_args)['changed']
    assert not call_main(my_main, DEFAULT_ARGS, module_args)['changed']

def test_rest_negative_delete_package():
    """ deleting package """
    register_responses([('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['generic_error']), ('GET', 'cluster', SRR['is_rest_9_9_0']), ('GET', 'cluster/software/packages', SRR['cluster_software_package_info_pte']), ('DELETE', 'cluster/software/packages/PlinyTheElder', SRR['generic_error'])])
    module_args = {'use_rest': 'always', 'package_version': 'PlinyTheElder', 'state': 'absent'}
    error = rest_error_message('Error: unable to fetch local package list', 'cluster/software/packages')
    assert error in call_main(my_main, DEFAULT_ARGS, module_args, fail=True)['msg']
    error = rest_error_message('Error deleting cluster software package for PlinyTheElder', 'cluster/software/packages/PlinyTheElder')
    assert error in call_main(my_main, DEFAULT_ARGS, module_args, fail=True)['msg']

def test_rest_partially_supported_options():
    """ validate success and error messages """
    register_responses([('GET', 'cluster', SRR['is_rest_96']), ('GET', 'cluster', SRR['is_rest_9_8_0']), ('GET', 'cluster', SRR['is_rest_9_8_0']), ('GET', 'cluster', SRR['is_rest_9_8_0'])])
    module_args = {'use_rest': 'always'}
    error = 'Minimum version of ONTAP for stabilize_minutes is (9, 8)'
    assert error in create_module(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    assert create_module(my_module, DEFAULT_ARGS, module_args)
    module_args = {'use_rest': 'always', 'nodes': 'node1'}
    error = 'Minimum version of ONTAP for nodes is (9, 9)'
    assert error in create_module(my_module, DEFAULT_ARGS, module_args, fail=True)['msg']
    module_args = {'use_rest': 'auto', 'nodes': 'node1'}
    assert create_module(my_module, DEFAULT_ARGS, module_args)
    print_warnings
    assert_warning_was_raised('Falling back to ZAPI because of unsupported option(s) or option value(s) "nodes" in REST require (9, 9)')

def test_missing_arg():
    args = dict(DEFAULT_ARGS)
    args.pop('package_url')
    register_responses([('GET', 'cluster', SRR['is_rest_9_8_0']), ('GET', 'cluster/software/packages', SRR['zero_records'])])
    module_args = {'use_rest': 'always'}
    error = 'Error: packague_url is a required parameter to download the software package.'
    assert error in call_main(my_main, args, module_args, fail=True)['msg']