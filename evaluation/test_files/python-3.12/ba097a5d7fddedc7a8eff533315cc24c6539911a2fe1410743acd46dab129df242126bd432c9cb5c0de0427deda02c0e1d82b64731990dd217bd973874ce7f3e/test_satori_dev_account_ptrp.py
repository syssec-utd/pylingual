import json
import os
import pathlib
from typing import Set
import pytest
from aws_ptrp import AwsPtrp
from aws_ptrp.iam.iam_roles import IAMRole
from aws_ptrp.services import ServiceResourceType, register_service_action_by_name, register_service_action_type_by_name, register_service_resource_by_name, register_service_resource_type_by_name
from aws_ptrp.services.assume_role.assume_role_actions import AssumeRoleAction
from aws_ptrp.services.assume_role.assume_role_service import ROLE_TRUST_SERVICE_NAME, AssumeRoleService
from aws_ptrp.services.federated_user.federated_user_actions import FederatedUserAction
from aws_ptrp.services.federated_user.federated_user_resources import FederatedUserResource
from aws_ptrp.services.federated_user.federated_user_service import FEDERATED_USER_SERVICE_NAME, FederatedUserService
from aws_ptrp.services.s3.bucket import S3Bucket
from aws_ptrp.services.s3.s3_actions import S3Action
from aws_ptrp.services.s3.s3_service import S3_SERVICE_NAME, S3Service
from serde.json import to_json
from authz_analyzer.datastores.aws.analyzer.exporter import AWSAuthzAnalyzerExporter
from authz_analyzer.utils.logger import get_logger
from authz_analyzer.writers.base_writers import OutputFormat
from authz_analyzer.writers.get_writers import get_writer
from tests.tests_datastores.aws.aws_ptrp.utils.aws_ptrp_load_from_dict import load_aws_ptrp_from_dict
AWS_AUTHZ_ANALYZER_SATORI_DEV_JSON_FILE = pathlib.Path().joinpath(os.path.dirname(__file__), 'satori_dev_account_ptrp.json')
AWS_AUTHZ_ANALYZER_SATORI_DEV_RESULT_JSON_FILE = pathlib.Path().joinpath(os.path.dirname(__file__), 'satori_dev_account_ptrp_result.json')

@pytest.fixture
def register_services_for_deserialize_from_file():
    register_service_action_by_name(S3_SERVICE_NAME, S3Action)
    register_service_resource_by_name(S3_SERVICE_NAME, S3Bucket)
    register_service_action_by_name(ROLE_TRUST_SERVICE_NAME, AssumeRoleAction)
    register_service_resource_by_name(ROLE_TRUST_SERVICE_NAME, IAMRole)
    register_service_action_by_name(FEDERATED_USER_SERVICE_NAME, FederatedUserAction)
    register_service_resource_by_name(FEDERATED_USER_SERVICE_NAME, FederatedUserResource)
    register_service_action_type_by_name(S3_SERVICE_NAME, S3Service)
    register_service_resource_type_by_name(S3_SERVICE_NAME, S3Service)
    register_service_action_type_by_name(ROLE_TRUST_SERVICE_NAME, AssumeRoleService)
    register_service_resource_type_by_name(ROLE_TRUST_SERVICE_NAME, AssumeRoleService)
    register_service_action_type_by_name(FEDERATED_USER_SERVICE_NAME, FederatedUserService)
    register_service_resource_type_by_name(FEDERATED_USER_SERVICE_NAME, FederatedUserService)

@pytest.mark.skipif(not os.environ.get('AUTHZ_SATORI_DEV_ACCOUNT_TEST'), reason='not really a test, just pull latest satori dev account config and write it to file')
def test_aws_ptrp_with_s3_write_satori_dev_account():
    target_account_id = '105246067165'
    additional_account_ids = set(['982269985744'])
    role_name = 'SatoriScanner'
    external_id = '766c940d1ce1bb63ee41ec1e64a5ddb820285ced'
    ptrp = AwsPtrp.load_from_role(get_logger(False), role_name, external_id, set([S3Service()]), target_account_id, additional_account_ids)
    ptrp_json = to_json(ptrp)
    with open(AWS_AUTHZ_ANALYZER_SATORI_DEV_JSON_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(ptrp_json)

@pytest.mark.skipif(not os.environ.get('AUTHZ_SATORI_DEV_ACCOUNT_TEST'), reason='not really a test, just pull latest satori dev account config and write it to file')
def test_aws_ptrp_resolve_permissions_satori_dev_json_file(register_services_for_deserialize_from_file):
    with open(AWS_AUTHZ_ANALYZER_SATORI_DEV_JSON_FILE, 'r', encoding='utf-8') as file:
        ptrp_json_from_file = json.load(file)
        resource_service_types_to_load: Set[ServiceResourceType] = set([AssumeRoleService(), FederatedUserService(), S3Service()])
        ptrp: AwsPtrp = load_aws_ptrp_from_dict(ptrp_json_from_file['iam_entities'], ptrp_json_from_file['target_account_resources'], resource_service_types_to_load)
        writer = get_writer(AWS_AUTHZ_ANALYZER_SATORI_DEV_RESULT_JSON_FILE, OutputFormat.MULTI_JSON)
        exporter = AWSAuthzAnalyzerExporter(writer)
        ptrp.resolve_permissions(get_logger(False), exporter.export_entry_from_ptrp_line)