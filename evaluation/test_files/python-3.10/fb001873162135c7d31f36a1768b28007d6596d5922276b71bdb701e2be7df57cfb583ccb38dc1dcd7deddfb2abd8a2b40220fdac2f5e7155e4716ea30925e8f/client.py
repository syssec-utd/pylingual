from Tea.core import TeaCore
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

class Client(OpenApiClient):
    """
    *    """

    def __init__(self, config: open_api_models.Config):
        super().__init__(config)
        self._endpoint_rule = ''
        if UtilClient.empty(self._endpoint):
            self._endpoint = 'api.dingtalk.com'

    def batch_get_form_data_by_id_list(self, request: dingtalkyida__1__0_models.BatchGetFormDataByIdListRequest) -> dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchGetFormDataByIdListHeaders()
        return self.batch_get_form_data_by_id_list_with_options(request, headers, runtime)

    async def batch_get_form_data_by_id_list_async(self, request: dingtalkyida__1__0_models.BatchGetFormDataByIdListRequest) -> dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchGetFormDataByIdListHeaders()
        return await self.batch_get_form_data_by_id_list_with_options_async(request, headers, runtime)

    def batch_get_form_data_by_id_list_with_options(self, request: dingtalkyida__1__0_models.BatchGetFormDataByIdListRequest, headers: dingtalkyida__1__0_models.BatchGetFormDataByIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.need_form_instance_value):
            body['needFormInstanceValue'] = request.need_form_instance_value
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse(), self.do_roarequest('BatchGetFormDataByIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/ids/query', 'json', req, runtime))

    async def batch_get_form_data_by_id_list_with_options_async(self, request: dingtalkyida__1__0_models.BatchGetFormDataByIdListRequest, headers: dingtalkyida__1__0_models.BatchGetFormDataByIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.need_form_instance_value):
            body['needFormInstanceValue'] = request.need_form_instance_value
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchGetFormDataByIdListResponse(), await self.do_roarequest_async('BatchGetFormDataByIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/ids/query', 'json', req, runtime))

    def batch_removal_by_form_instance_id_list(self, request: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest) -> dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders()
        return self.batch_removal_by_form_instance_id_list_with_options(request, headers, runtime)

    async def batch_removal_by_form_instance_id_list_async(self, request: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest) -> dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders()
        return await self.batch_removal_by_form_instance_id_list_with_options_async(request, headers, runtime)

    def batch_removal_by_form_instance_id_list_with_options(self, request: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest, headers: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.execute_expression):
            body['executeExpression'] = request.execute_expression
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse(), self.do_roarequest('BatchRemovalByFormInstanceIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/batchRemove', 'none', req, runtime))

    async def batch_removal_by_form_instance_id_list_with_options_async(self, request: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListRequest, headers: dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.execute_expression):
            body['executeExpression'] = request.execute_expression
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchRemovalByFormInstanceIdListResponse(), await self.do_roarequest_async('BatchRemovalByFormInstanceIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/batchRemove', 'none', req, runtime))

    def batch_save_form_data(self, request: dingtalkyida__1__0_models.BatchSaveFormDataRequest) -> dingtalkyida__1__0_models.BatchSaveFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchSaveFormDataHeaders()
        return self.batch_save_form_data_with_options(request, headers, runtime)

    async def batch_save_form_data_async(self, request: dingtalkyida__1__0_models.BatchSaveFormDataRequest) -> dingtalkyida__1__0_models.BatchSaveFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchSaveFormDataHeaders()
        return await self.batch_save_form_data_with_options_async(request, headers, runtime)

    def batch_save_form_data_with_options(self, request: dingtalkyida__1__0_models.BatchSaveFormDataRequest, headers: dingtalkyida__1__0_models.BatchSaveFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchSaveFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_data_json_list):
            body['formDataJsonList'] = request.form_data_json_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.keep_running_after_exception):
            body['keepRunningAfterException'] = request.keep_running_after_exception
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchSaveFormDataResponse(), self.do_roarequest('BatchSaveFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/batchSave', 'json', req, runtime))

    async def batch_save_form_data_with_options_async(self, request: dingtalkyida__1__0_models.BatchSaveFormDataRequest, headers: dingtalkyida__1__0_models.BatchSaveFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchSaveFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_data_json_list):
            body['formDataJsonList'] = request.form_data_json_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.keep_running_after_exception):
            body['keepRunningAfterException'] = request.keep_running_after_exception
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchSaveFormDataResponse(), await self.do_roarequest_async('BatchSaveFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/batchSave', 'json', req, runtime))

    def batch_update_form_data_by_instance_id(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders()
        return self.batch_update_form_data_by_instance_id_with_options(request, headers, runtime)

    async def batch_update_form_data_by_instance_id_async(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders()
        return await self.batch_update_form_data_by_instance_id_with_options_async(request, headers, runtime)

    def batch_update_form_data_by_instance_id_with_options(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest, headers: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.ignore_empty):
            body['ignoreEmpty'] = request.ignore_empty
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.use_latest_form_schema_version):
            body['useLatestFormSchemaVersion'] = request.use_latest_form_schema_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse(), self.do_roarequest('BatchUpdateFormDataByInstanceId', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances/components', 'json', req, runtime))

    async def batch_update_form_data_by_instance_id_with_options_async(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdRequest, headers: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.ignore_empty):
            body['ignoreEmpty'] = request.ignore_empty
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.use_latest_form_schema_version):
            body['useLatestFormSchemaVersion'] = request.use_latest_form_schema_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceIdResponse(), await self.do_roarequest_async('BatchUpdateFormDataByInstanceId', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances/components', 'json', req, runtime))

    def batch_update_form_data_by_instance_map(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapRequest) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapHeaders()
        return self.batch_update_form_data_by_instance_map_with_options(request, headers, runtime)

    async def batch_update_form_data_by_instance_map_async(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapRequest) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapHeaders()
        return await self.batch_update_form_data_by_instance_map_with_options_async(request, headers, runtime)

    def batch_update_form_data_by_instance_map_with_options(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapRequest, headers: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.ignore_empty):
            body['ignoreEmpty'] = request.ignore_empty
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json_map):
            body['updateFormDataJsonMap'] = request.update_form_data_json_map
        if not UtilClient.is_unset(request.use_latest_form_schema_version):
            body['useLatestFormSchemaVersion'] = request.use_latest_form_schema_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse(), self.do_roarequest('BatchUpdateFormDataByInstanceMap', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances/datas', 'json', req, runtime))

    async def batch_update_form_data_by_instance_map_with_options_async(self, request: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapRequest, headers: dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.asynchronous_execution):
            body['asynchronousExecution'] = request.asynchronous_execution
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.ignore_empty):
            body['ignoreEmpty'] = request.ignore_empty
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json_map):
            body['updateFormDataJsonMap'] = request.update_form_data_json_map
        if not UtilClient.is_unset(request.use_latest_form_schema_version):
            body['useLatestFormSchemaVersion'] = request.use_latest_form_schema_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BatchUpdateFormDataByInstanceMapResponse(), await self.do_roarequest_async('BatchUpdateFormDataByInstanceMap', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances/datas', 'json', req, runtime))

    def buy_authorization_order(self, request: dingtalkyida__1__0_models.BuyAuthorizationOrderRequest) -> dingtalkyida__1__0_models.BuyAuthorizationOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BuyAuthorizationOrderHeaders()
        return self.buy_authorization_order_with_options(request, headers, runtime)

    async def buy_authorization_order_async(self, request: dingtalkyida__1__0_models.BuyAuthorizationOrderRequest) -> dingtalkyida__1__0_models.BuyAuthorizationOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BuyAuthorizationOrderHeaders()
        return await self.buy_authorization_order_with_options_async(request, headers, runtime)

    def buy_authorization_order_with_options(self, request: dingtalkyida__1__0_models.BuyAuthorizationOrderRequest, headers: dingtalkyida__1__0_models.BuyAuthorizationOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BuyAuthorizationOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BuyAuthorizationOrderResponse(), self.do_roarequest('BuyAuthorizationOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/appAuthorizations/order', 'json', req, runtime))

    async def buy_authorization_order_with_options_async(self, request: dingtalkyida__1__0_models.BuyAuthorizationOrderRequest, headers: dingtalkyida__1__0_models.BuyAuthorizationOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BuyAuthorizationOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BuyAuthorizationOrderResponse(), await self.do_roarequest_async('BuyAuthorizationOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/appAuthorizations/order', 'json', req, runtime))

    def buy_fresh_order(self, request: dingtalkyida__1__0_models.BuyFreshOrderRequest) -> dingtalkyida__1__0_models.BuyFreshOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BuyFreshOrderHeaders()
        return self.buy_fresh_order_with_options(request, headers, runtime)

    async def buy_fresh_order_async(self, request: dingtalkyida__1__0_models.BuyFreshOrderRequest) -> dingtalkyida__1__0_models.BuyFreshOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.BuyFreshOrderHeaders()
        return await self.buy_fresh_order_with_options_async(request, headers, runtime)

    def buy_fresh_order_with_options(self, request: dingtalkyida__1__0_models.BuyFreshOrderRequest, headers: dingtalkyida__1__0_models.BuyFreshOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BuyFreshOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BuyFreshOrderResponse(), self.do_roarequest('BuyFreshOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/freshOrders', 'json', req, runtime))

    async def buy_fresh_order_with_options_async(self, request: dingtalkyida__1__0_models.BuyFreshOrderRequest, headers: dingtalkyida__1__0_models.BuyFreshOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.BuyFreshOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.BuyFreshOrderResponse(), await self.do_roarequest_async('BuyFreshOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/freshOrders', 'json', req, runtime))

    def check_cloud_account_status(self, caller_uid: str, request: dingtalkyida__1__0_models.CheckCloudAccountStatusRequest) -> dingtalkyida__1__0_models.CheckCloudAccountStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.CheckCloudAccountStatusHeaders()
        return self.check_cloud_account_status_with_options(caller_uid, request, headers, runtime)

    async def check_cloud_account_status_async(self, caller_uid: str, request: dingtalkyida__1__0_models.CheckCloudAccountStatusRequest) -> dingtalkyida__1__0_models.CheckCloudAccountStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.CheckCloudAccountStatusHeaders()
        return await self.check_cloud_account_status_with_options_async(caller_uid, request, headers, runtime)

    def check_cloud_account_status_with_options(self, caller_uid: str, request: dingtalkyida__1__0_models.CheckCloudAccountStatusRequest, headers: dingtalkyida__1__0_models.CheckCloudAccountStatusHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.CheckCloudAccountStatusResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.CheckCloudAccountStatusResponse(), self.do_roarequest('CheckCloudAccountStatus', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/cloudAccountStatus/{caller_uid}', 'json', req, runtime))

    async def check_cloud_account_status_with_options_async(self, caller_uid: str, request: dingtalkyida__1__0_models.CheckCloudAccountStatusRequest, headers: dingtalkyida__1__0_models.CheckCloudAccountStatusHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.CheckCloudAccountStatusResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.CheckCloudAccountStatusResponse(), await self.do_roarequest_async('CheckCloudAccountStatus', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/cloudAccountStatus/{caller_uid}', 'json', req, runtime))

    def create_or_update_form_data(self, request: dingtalkyida__1__0_models.CreateOrUpdateFormDataRequest) -> dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.CreateOrUpdateFormDataHeaders()
        return self.create_or_update_form_data_with_options(request, headers, runtime)

    async def create_or_update_form_data_async(self, request: dingtalkyida__1__0_models.CreateOrUpdateFormDataRequest) -> dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.CreateOrUpdateFormDataHeaders()
        return await self.create_or_update_form_data_with_options_async(request, headers, runtime)

    def create_or_update_form_data_with_options(self, request: dingtalkyida__1__0_models.CreateOrUpdateFormDataRequest, headers: dingtalkyida__1__0_models.CreateOrUpdateFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse(), self.do_roarequest('CreateOrUpdateFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/insertOrUpdate', 'json', req, runtime))

    async def create_or_update_form_data_with_options_async(self, request: dingtalkyida__1__0_models.CreateOrUpdateFormDataRequest, headers: dingtalkyida__1__0_models.CreateOrUpdateFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.no_execute_expression):
            body['noExecuteExpression'] = request.no_execute_expression
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.CreateOrUpdateFormDataResponse(), await self.do_roarequest_async('CreateOrUpdateFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/insertOrUpdate', 'json', req, runtime))

    def delete_form_data(self, request: dingtalkyida__1__0_models.DeleteFormDataRequest) -> dingtalkyida__1__0_models.DeleteFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteFormDataHeaders()
        return self.delete_form_data_with_options(request, headers, runtime)

    async def delete_form_data_async(self, request: dingtalkyida__1__0_models.DeleteFormDataRequest) -> dingtalkyida__1__0_models.DeleteFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteFormDataHeaders()
        return await self.delete_form_data_with_options_async(request, headers, runtime)

    def delete_form_data_with_options(self, request: dingtalkyida__1__0_models.DeleteFormDataRequest, headers: dingtalkyida__1__0_models.DeleteFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteFormDataResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id):
            query['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteFormDataResponse(), self.do_roarequest('DeleteFormData', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/forms/instances', 'none', req, runtime))

    async def delete_form_data_with_options_async(self, request: dingtalkyida__1__0_models.DeleteFormDataRequest, headers: dingtalkyida__1__0_models.DeleteFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteFormDataResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id):
            query['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteFormDataResponse(), await self.do_roarequest_async('DeleteFormData', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/forms/instances', 'none', req, runtime))

    def delete_instance(self, request: dingtalkyida__1__0_models.DeleteInstanceRequest) -> dingtalkyida__1__0_models.DeleteInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteInstanceHeaders()
        return self.delete_instance_with_options(request, headers, runtime)

    async def delete_instance_async(self, request: dingtalkyida__1__0_models.DeleteInstanceRequest) -> dingtalkyida__1__0_models.DeleteInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteInstanceHeaders()
        return await self.delete_instance_with_options_async(request, headers, runtime)

    def delete_instance_with_options(self, request: dingtalkyida__1__0_models.DeleteInstanceRequest, headers: dingtalkyida__1__0_models.DeleteInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteInstanceResponse(), self.do_roarequest('DeleteInstance', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/processes/instances', 'none', req, runtime))

    async def delete_instance_with_options_async(self, request: dingtalkyida__1__0_models.DeleteInstanceRequest, headers: dingtalkyida__1__0_models.DeleteInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteInstanceResponse(), await self.do_roarequest_async('DeleteInstance', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/processes/instances', 'none', req, runtime))

    def delete_sequence(self, request: dingtalkyida__1__0_models.DeleteSequenceRequest) -> dingtalkyida__1__0_models.DeleteSequenceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteSequenceHeaders()
        return self.delete_sequence_with_options(request, headers, runtime)

    async def delete_sequence_async(self, request: dingtalkyida__1__0_models.DeleteSequenceRequest) -> dingtalkyida__1__0_models.DeleteSequenceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeleteSequenceHeaders()
        return await self.delete_sequence_with_options_async(request, headers, runtime)

    def delete_sequence_with_options(self, request: dingtalkyida__1__0_models.DeleteSequenceRequest, headers: dingtalkyida__1__0_models.DeleteSequenceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteSequenceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.sequence):
            query['sequence'] = request.sequence
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteSequenceResponse(), self.do_roarequest('DeleteSequence', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/forms/deleteSequence', 'none', req, runtime))

    async def delete_sequence_with_options_async(self, request: dingtalkyida__1__0_models.DeleteSequenceRequest, headers: dingtalkyida__1__0_models.DeleteSequenceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeleteSequenceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.sequence):
            query['sequence'] = request.sequence
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeleteSequenceResponse(), await self.do_roarequest_async('DeleteSequence', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/forms/deleteSequence', 'none', req, runtime))

    def deploy_function_callback(self, request: dingtalkyida__1__0_models.DeployFunctionCallbackRequest) -> dingtalkyida__1__0_models.DeployFunctionCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeployFunctionCallbackHeaders()
        return self.deploy_function_callback_with_options(request, headers, runtime)

    async def deploy_function_callback_async(self, request: dingtalkyida__1__0_models.DeployFunctionCallbackRequest) -> dingtalkyida__1__0_models.DeployFunctionCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.DeployFunctionCallbackHeaders()
        return await self.deploy_function_callback_with_options_async(request, headers, runtime)

    def deploy_function_callback_with_options(self, request: dingtalkyida__1__0_models.DeployFunctionCallbackRequest, headers: dingtalkyida__1__0_models.DeployFunctionCallbackHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeployFunctionCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['appId'] = request.app_id
        if not UtilClient.is_unset(request.custom_domain):
            body['customDomain'] = request.custom_domain
        if not UtilClient.is_unset(request.deploy_stage):
            body['deployStage'] = request.deploy_stage
        if not UtilClient.is_unset(request.gate_way_app_key):
            body['gateWayAppKey'] = request.gate_way_app_key
        if not UtilClient.is_unset(request.gate_way_app_secret):
            body['gateWayAppSecret'] = request.gate_way_app_secret
        if not UtilClient.is_unset(request.gate_way_domain):
            body['gateWayDomain'] = request.gate_way_domain
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeployFunctionCallbackResponse(), self.do_roarequest('DeployFunctionCallback', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/functionComputeConnectors/completeDeployments/notify', 'json', req, runtime))

    async def deploy_function_callback_with_options_async(self, request: dingtalkyida__1__0_models.DeployFunctionCallbackRequest, headers: dingtalkyida__1__0_models.DeployFunctionCallbackHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.DeployFunctionCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_id):
            body['appId'] = request.app_id
        if not UtilClient.is_unset(request.custom_domain):
            body['customDomain'] = request.custom_domain
        if not UtilClient.is_unset(request.deploy_stage):
            body['deployStage'] = request.deploy_stage
        if not UtilClient.is_unset(request.gate_way_app_key):
            body['gateWayAppKey'] = request.gate_way_app_key
        if not UtilClient.is_unset(request.gate_way_app_secret):
            body['gateWayAppSecret'] = request.gate_way_app_secret
        if not UtilClient.is_unset(request.gate_way_domain):
            body['gateWayDomain'] = request.gate_way_domain
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.DeployFunctionCallbackResponse(), await self.do_roarequest_async('DeployFunctionCallback', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/functionComputeConnectors/completeDeployments/notify', 'json', req, runtime))

    def execute_batch_task(self, request: dingtalkyida__1__0_models.ExecuteBatchTaskRequest) -> dingtalkyida__1__0_models.ExecuteBatchTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteBatchTaskHeaders()
        return self.execute_batch_task_with_options(request, headers, runtime)

    async def execute_batch_task_async(self, request: dingtalkyida__1__0_models.ExecuteBatchTaskRequest) -> dingtalkyida__1__0_models.ExecuteBatchTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteBatchTaskHeaders()
        return await self.execute_batch_task_with_options_async(request, headers, runtime)

    def execute_batch_task_with_options(self, request: dingtalkyida__1__0_models.ExecuteBatchTaskRequest, headers: dingtalkyida__1__0_models.ExecuteBatchTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteBatchTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_information_list):
            body['taskInformationList'] = request.task_information_list
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteBatchTaskResponse(), self.do_roarequest('ExecuteBatchTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/batches/execute', 'json', req, runtime))

    async def execute_batch_task_with_options_async(self, request: dingtalkyida__1__0_models.ExecuteBatchTaskRequest, headers: dingtalkyida__1__0_models.ExecuteBatchTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteBatchTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_information_list):
            body['taskInformationList'] = request.task_information_list
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteBatchTaskResponse(), await self.do_roarequest_async('ExecuteBatchTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/batches/execute', 'json', req, runtime))

    def execute_custom_api(self, request: dingtalkyida__1__0_models.ExecuteCustomApiRequest) -> dingtalkyida__1__0_models.ExecuteCustomApiResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteCustomApiHeaders()
        return self.execute_custom_api_with_options(request, headers, runtime)

    async def execute_custom_api_async(self, request: dingtalkyida__1__0_models.ExecuteCustomApiRequest) -> dingtalkyida__1__0_models.ExecuteCustomApiResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteCustomApiHeaders()
        return await self.execute_custom_api_with_options_async(request, headers, runtime)

    def execute_custom_api_with_options(self, request: dingtalkyida__1__0_models.ExecuteCustomApiRequest, headers: dingtalkyida__1__0_models.ExecuteCustomApiHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteCustomApiResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.data):
            query['data'] = request.data
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.service_id):
            query['serviceId'] = request.service_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteCustomApiResponse(), self.do_roarequest('ExecuteCustomApi', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/customApi/execute', 'json', req, runtime))

    async def execute_custom_api_with_options_async(self, request: dingtalkyida__1__0_models.ExecuteCustomApiRequest, headers: dingtalkyida__1__0_models.ExecuteCustomApiHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteCustomApiResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.data):
            query['data'] = request.data
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.service_id):
            query['serviceId'] = request.service_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteCustomApiResponse(), await self.do_roarequest_async('ExecuteCustomApi', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/customApi/execute', 'json', req, runtime))

    def execute_platform_task(self, request: dingtalkyida__1__0_models.ExecutePlatformTaskRequest) -> dingtalkyida__1__0_models.ExecutePlatformTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecutePlatformTaskHeaders()
        return self.execute_platform_task_with_options(request, headers, runtime)

    async def execute_platform_task_async(self, request: dingtalkyida__1__0_models.ExecutePlatformTaskRequest) -> dingtalkyida__1__0_models.ExecutePlatformTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecutePlatformTaskHeaders()
        return await self.execute_platform_task_with_options_async(request, headers, runtime)

    def execute_platform_task_with_options(self, request: dingtalkyida__1__0_models.ExecutePlatformTaskRequest, headers: dingtalkyida__1__0_models.ExecutePlatformTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecutePlatformTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.no_execute_expressions):
            body['noExecuteExpressions'] = request.no_execute_expressions
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecutePlatformTaskResponse(), self.do_roarequest('ExecutePlatformTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/platformTasks/execute', 'none', req, runtime))

    async def execute_platform_task_with_options_async(self, request: dingtalkyida__1__0_models.ExecutePlatformTaskRequest, headers: dingtalkyida__1__0_models.ExecutePlatformTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecutePlatformTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.no_execute_expressions):
            body['noExecuteExpressions'] = request.no_execute_expressions
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecutePlatformTaskResponse(), await self.do_roarequest_async('ExecutePlatformTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/platformTasks/execute', 'none', req, runtime))

    def execute_task(self, request: dingtalkyida__1__0_models.ExecuteTaskRequest) -> dingtalkyida__1__0_models.ExecuteTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteTaskHeaders()
        return self.execute_task_with_options(request, headers, runtime)

    async def execute_task_async(self, request: dingtalkyida__1__0_models.ExecuteTaskRequest) -> dingtalkyida__1__0_models.ExecuteTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExecuteTaskHeaders()
        return await self.execute_task_with_options_async(request, headers, runtime)

    def execute_task_with_options(self, request: dingtalkyida__1__0_models.ExecuteTaskRequest, headers: dingtalkyida__1__0_models.ExecuteTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.digital_sign_url):
            body['digitalSignUrl'] = request.digital_sign_url
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.no_execute_expressions):
            body['noExecuteExpressions'] = request.no_execute_expressions
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteTaskResponse(), self.do_roarequest('ExecuteTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/execute', 'none', req, runtime))

    async def execute_task_with_options_async(self, request: dingtalkyida__1__0_models.ExecuteTaskRequest, headers: dingtalkyida__1__0_models.ExecuteTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExecuteTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.digital_sign_url):
            body['digitalSignUrl'] = request.digital_sign_url
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.no_execute_expressions):
            body['noExecuteExpressions'] = request.no_execute_expressions
        if not UtilClient.is_unset(request.out_result):
            body['outResult'] = request.out_result
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExecuteTaskResponse(), await self.do_roarequest_async('ExecuteTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/execute', 'none', req, runtime))

    def expire_commodity(self, request: dingtalkyida__1__0_models.ExpireCommodityRequest) -> dingtalkyida__1__0_models.ExpireCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExpireCommodityHeaders()
        return self.expire_commodity_with_options(request, headers, runtime)

    async def expire_commodity_async(self, request: dingtalkyida__1__0_models.ExpireCommodityRequest) -> dingtalkyida__1__0_models.ExpireCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ExpireCommodityHeaders()
        return await self.expire_commodity_with_options_async(request, headers, runtime)

    def expire_commodity_with_options(self, request: dingtalkyida__1__0_models.ExpireCommodityRequest, headers: dingtalkyida__1__0_models.ExpireCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExpireCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExpireCommodityResponse(), self.do_roarequest('ExpireCommodity', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/appAuth/commodities/expire', 'json', req, runtime))

    async def expire_commodity_with_options_async(self, request: dingtalkyida__1__0_models.ExpireCommodityRequest, headers: dingtalkyida__1__0_models.ExpireCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ExpireCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ExpireCommodityResponse(), await self.do_roarequest_async('ExpireCommodity', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/appAuth/commodities/expire', 'json', req, runtime))

    def get_activation_code_by_caller_union_id(self, caller_uid: str, request: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdRequest) -> dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdHeaders()
        return self.get_activation_code_by_caller_union_id_with_options(caller_uid, request, headers, runtime)

    async def get_activation_code_by_caller_union_id_async(self, caller_uid: str, request: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdRequest) -> dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdHeaders()
        return await self.get_activation_code_by_caller_union_id_with_options_async(caller_uid, request, headers, runtime)

    def get_activation_code_by_caller_union_id_with_options(self, caller_uid: str, request: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdRequest, headers: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse(), self.do_roarequest('GetActivationCodeByCallerUnionId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applications/activationCodes/{caller_uid}', 'json', req, runtime))

    async def get_activation_code_by_caller_union_id_with_options_async(self, caller_uid: str, request: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdRequest, headers: dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivationCodeByCallerUnionIdResponse(), await self.do_roarequest_async('GetActivationCodeByCallerUnionId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applications/activationCodes/{caller_uid}', 'json', req, runtime))

    def get_activity_button_list(self, app_type: str, process_code: str, activity_id: str, request: dingtalkyida__1__0_models.GetActivityButtonListRequest) -> dingtalkyida__1__0_models.GetActivityButtonListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivityButtonListHeaders()
        return self.get_activity_button_list_with_options(app_type, process_code, activity_id, request, headers, runtime)

    async def get_activity_button_list_async(self, app_type: str, process_code: str, activity_id: str, request: dingtalkyida__1__0_models.GetActivityButtonListRequest) -> dingtalkyida__1__0_models.GetActivityButtonListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivityButtonListHeaders()
        return await self.get_activity_button_list_with_options_async(app_type, process_code, activity_id, request, headers, runtime)

    def get_activity_button_list_with_options(self, app_type: str, process_code: str, activity_id: str, request: dingtalkyida__1__0_models.GetActivityButtonListRequest, headers: dingtalkyida__1__0_models.GetActivityButtonListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivityButtonListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        process_code = OpenApiUtilClient.get_encode_param(process_code)
        activity_id = OpenApiUtilClient.get_encode_param(activity_id)
        query = {}
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivityButtonListResponse(), self.do_roarequest('GetActivityButtonList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processDefinitions/buttons/{app_type}/{process_code}/{activity_id}', 'json', req, runtime))

    async def get_activity_button_list_with_options_async(self, app_type: str, process_code: str, activity_id: str, request: dingtalkyida__1__0_models.GetActivityButtonListRequest, headers: dingtalkyida__1__0_models.GetActivityButtonListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivityButtonListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        process_code = OpenApiUtilClient.get_encode_param(process_code)
        activity_id = OpenApiUtilClient.get_encode_param(activity_id)
        query = {}
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivityButtonListResponse(), await self.do_roarequest_async('GetActivityButtonList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processDefinitions/buttons/{app_type}/{process_code}/{activity_id}', 'json', req, runtime))

    def get_activity_list(self, request: dingtalkyida__1__0_models.GetActivityListRequest) -> dingtalkyida__1__0_models.GetActivityListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivityListHeaders()
        return self.get_activity_list_with_options(request, headers, runtime)

    async def get_activity_list_async(self, request: dingtalkyida__1__0_models.GetActivityListRequest) -> dingtalkyida__1__0_models.GetActivityListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetActivityListHeaders()
        return await self.get_activity_list_with_options_async(request, headers, runtime)

    def get_activity_list_with_options(self, request: dingtalkyida__1__0_models.GetActivityListRequest, headers: dingtalkyida__1__0_models.GetActivityListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivityListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_code):
            query['processCode'] = request.process_code
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivityListResponse(), self.do_roarequest('GetActivityList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/activities', 'json', req, runtime))

    async def get_activity_list_with_options_async(self, request: dingtalkyida__1__0_models.GetActivityListRequest, headers: dingtalkyida__1__0_models.GetActivityListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetActivityListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_code):
            query['processCode'] = request.process_code
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetActivityListResponse(), await self.do_roarequest_async('GetActivityList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/activities', 'json', req, runtime))

    def get_application_authorization_service_platform_resource(self, request: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceRequest) -> dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceHeaders()
        return self.get_application_authorization_service_platform_resource_with_options(request, headers, runtime)

    async def get_application_authorization_service_platform_resource_async(self, request: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceRequest) -> dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceHeaders()
        return await self.get_application_authorization_service_platform_resource_with_options_async(request, headers, runtime)

    def get_application_authorization_service_platform_resource_with_options(self, request: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceRequest, headers: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse(), self.do_roarequest('GetApplicationAuthorizationServicePlatformResource', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/authorization/platformResources', 'json', req, runtime))

    async def get_application_authorization_service_platform_resource_with_options_async(self, request: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceRequest, headers: dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetApplicationAuthorizationServicePlatformResourceResponse(), await self.do_roarequest_async('GetApplicationAuthorizationServicePlatformResource', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/authorization/platformResources', 'json', req, runtime))

    def get_corp_accomplishment_tasks(self, corp_id: str, user_id: str, request: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksRequest) -> dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpAccomplishmentTasksHeaders()
        return self.get_corp_accomplishment_tasks_with_options(corp_id, user_id, request, headers, runtime)

    async def get_corp_accomplishment_tasks_async(self, corp_id: str, user_id: str, request: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksRequest) -> dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpAccomplishmentTasksHeaders()
        return await self.get_corp_accomplishment_tasks_with_options_async(corp_id, user_id, request, headers, runtime)

    def get_corp_accomplishment_tasks_with_options(self, corp_id: str, user_id: str, request: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksRequest, headers: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse:
        UtilClient.validate_model(request)
        corp_id = OpenApiUtilClient.get_encode_param(corp_id)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse(), self.do_roarequest('GetCorpAccomplishmentTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/completedTasks/{corp_id}/{user_id}', 'json', req, runtime))

    async def get_corp_accomplishment_tasks_with_options_async(self, corp_id: str, user_id: str, request: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksRequest, headers: dingtalkyida__1__0_models.GetCorpAccomplishmentTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse:
        UtilClient.validate_model(request)
        corp_id = OpenApiUtilClient.get_encode_param(corp_id)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpAccomplishmentTasksResponse(), await self.do_roarequest_async('GetCorpAccomplishmentTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/completedTasks/{corp_id}/{user_id}', 'json', req, runtime))

    def get_corp_level_by_account_id(self, request: dingtalkyida__1__0_models.GetCorpLevelByAccountIdRequest) -> dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpLevelByAccountIdHeaders()
        return self.get_corp_level_by_account_id_with_options(request, headers, runtime)

    async def get_corp_level_by_account_id_async(self, request: dingtalkyida__1__0_models.GetCorpLevelByAccountIdRequest) -> dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpLevelByAccountIdHeaders()
        return await self.get_corp_level_by_account_id_with_options_async(request, headers, runtime)

    def get_corp_level_by_account_id_with_options(self, request: dingtalkyida__1__0_models.GetCorpLevelByAccountIdRequest, headers: dingtalkyida__1__0_models.GetCorpLevelByAccountIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.account_id):
            query['accountId'] = request.account_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse(), self.do_roarequest('GetCorpLevelByAccountId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/corpLevel', 'json', req, runtime))

    async def get_corp_level_by_account_id_with_options_async(self, request: dingtalkyida__1__0_models.GetCorpLevelByAccountIdRequest, headers: dingtalkyida__1__0_models.GetCorpLevelByAccountIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.account_id):
            query['accountId'] = request.account_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpLevelByAccountIdResponse(), await self.do_roarequest_async('GetCorpLevelByAccountId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/corpLevel', 'json', req, runtime))

    def get_corp_tasks(self, request: dingtalkyida__1__0_models.GetCorpTasksRequest) -> dingtalkyida__1__0_models.GetCorpTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpTasksHeaders()
        return self.get_corp_tasks_with_options(request, headers, runtime)

    async def get_corp_tasks_async(self, request: dingtalkyida__1__0_models.GetCorpTasksRequest) -> dingtalkyida__1__0_models.GetCorpTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetCorpTasksHeaders()
        return await self.get_corp_tasks_with_options_async(request, headers, runtime)

    def get_corp_tasks_with_options(self, request: dingtalkyida__1__0_models.GetCorpTasksRequest, headers: dingtalkyida__1__0_models.GetCorpTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpTasksResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpTasksResponse(), self.do_roarequest('GetCorpTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/corpTasks', 'json', req, runtime))

    async def get_corp_tasks_with_options_async(self, request: dingtalkyida__1__0_models.GetCorpTasksRequest, headers: dingtalkyida__1__0_models.GetCorpTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetCorpTasksResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetCorpTasksResponse(), await self.do_roarequest_async('GetCorpTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/corpTasks', 'json', req, runtime))

    def get_field_def_by_uuid(self, request: dingtalkyida__1__0_models.GetFieldDefByUuidRequest) -> dingtalkyida__1__0_models.GetFieldDefByUuidResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFieldDefByUuidHeaders()
        return self.get_field_def_by_uuid_with_options(request, headers, runtime)

    async def get_field_def_by_uuid_async(self, request: dingtalkyida__1__0_models.GetFieldDefByUuidRequest) -> dingtalkyida__1__0_models.GetFieldDefByUuidResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFieldDefByUuidHeaders()
        return await self.get_field_def_by_uuid_with_options_async(request, headers, runtime)

    def get_field_def_by_uuid_with_options(self, request: dingtalkyida__1__0_models.GetFieldDefByUuidRequest, headers: dingtalkyida__1__0_models.GetFieldDefByUuidHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFieldDefByUuidResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFieldDefByUuidResponse(), self.do_roarequest('GetFieldDefByUuid', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/formFields', 'json', req, runtime))

    async def get_field_def_by_uuid_with_options_async(self, request: dingtalkyida__1__0_models.GetFieldDefByUuidRequest, headers: dingtalkyida__1__0_models.GetFieldDefByUuidHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFieldDefByUuidResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFieldDefByUuidResponse(), await self.do_roarequest_async('GetFieldDefByUuid', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/formFields', 'json', req, runtime))

    def get_form_component_definition_list(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.GetFormComponentDefinitionListRequest) -> dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormComponentDefinitionListHeaders()
        return self.get_form_component_definition_list_with_options(app_type, form_uuid, request, headers, runtime)

    async def get_form_component_definition_list_async(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.GetFormComponentDefinitionListRequest) -> dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormComponentDefinitionListHeaders()
        return await self.get_form_component_definition_list_with_options_async(app_type, form_uuid, request, headers, runtime)

    def get_form_component_definition_list_with_options(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.GetFormComponentDefinitionListRequest, headers: dingtalkyida__1__0_models.GetFormComponentDefinitionListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        form_uuid = OpenApiUtilClient.get_encode_param(form_uuid)
        query = {}
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse(), self.do_roarequest('GetFormComponentDefinitionList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/definitions/{app_type}/{form_uuid}', 'json', req, runtime))

    async def get_form_component_definition_list_with_options_async(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.GetFormComponentDefinitionListRequest, headers: dingtalkyida__1__0_models.GetFormComponentDefinitionListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        form_uuid = OpenApiUtilClient.get_encode_param(form_uuid)
        query = {}
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormComponentDefinitionListResponse(), await self.do_roarequest_async('GetFormComponentDefinitionList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/definitions/{app_type}/{form_uuid}', 'json', req, runtime))

    def get_form_data_by_id(self, id: str, request: dingtalkyida__1__0_models.GetFormDataByIDRequest) -> dingtalkyida__1__0_models.GetFormDataByIDResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormDataByIDHeaders()
        return self.get_form_data_by_idwith_options(id, request, headers, runtime)

    async def get_form_data_by_id_async(self, id: str, request: dingtalkyida__1__0_models.GetFormDataByIDRequest) -> dingtalkyida__1__0_models.GetFormDataByIDResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormDataByIDHeaders()
        return await self.get_form_data_by_idwith_options_async(id, request, headers, runtime)

    def get_form_data_by_idwith_options(self, id: str, request: dingtalkyida__1__0_models.GetFormDataByIDRequest, headers: dingtalkyida__1__0_models.GetFormDataByIDHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormDataByIDResponse:
        UtilClient.validate_model(request)
        id = OpenApiUtilClient.get_encode_param(id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormDataByIDResponse(), self.do_roarequest('GetFormDataByID', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/instances/{id}', 'json', req, runtime))

    async def get_form_data_by_idwith_options_async(self, id: str, request: dingtalkyida__1__0_models.GetFormDataByIDRequest, headers: dingtalkyida__1__0_models.GetFormDataByIDHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormDataByIDResponse:
        UtilClient.validate_model(request)
        id = OpenApiUtilClient.get_encode_param(id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormDataByIDResponse(), await self.do_roarequest_async('GetFormDataByID', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/instances/{id}', 'json', req, runtime))

    def get_form_list_in_app(self, request: dingtalkyida__1__0_models.GetFormListInAppRequest) -> dingtalkyida__1__0_models.GetFormListInAppResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormListInAppHeaders()
        return self.get_form_list_in_app_with_options(request, headers, runtime)

    async def get_form_list_in_app_async(self, request: dingtalkyida__1__0_models.GetFormListInAppRequest) -> dingtalkyida__1__0_models.GetFormListInAppResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetFormListInAppHeaders()
        return await self.get_form_list_in_app_with_options_async(request, headers, runtime)

    def get_form_list_in_app_with_options(self, request: dingtalkyida__1__0_models.GetFormListInAppRequest, headers: dingtalkyida__1__0_models.GetFormListInAppHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormListInAppResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_types):
            query['formTypes'] = request.form_types
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormListInAppResponse(), self.do_roarequest('GetFormListInApp', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms', 'json', req, runtime))

    async def get_form_list_in_app_with_options_async(self, request: dingtalkyida__1__0_models.GetFormListInAppRequest, headers: dingtalkyida__1__0_models.GetFormListInAppHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetFormListInAppResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_types):
            query['formTypes'] = request.form_types
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetFormListInAppResponse(), await self.do_roarequest_async('GetFormListInApp', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms', 'json', req, runtime))

    def get_instance_by_id(self, id: str, request: dingtalkyida__1__0_models.GetInstanceByIdRequest) -> dingtalkyida__1__0_models.GetInstanceByIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstanceByIdHeaders()
        return self.get_instance_by_id_with_options(id, request, headers, runtime)

    async def get_instance_by_id_async(self, id: str, request: dingtalkyida__1__0_models.GetInstanceByIdRequest) -> dingtalkyida__1__0_models.GetInstanceByIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstanceByIdHeaders()
        return await self.get_instance_by_id_with_options_async(id, request, headers, runtime)

    def get_instance_by_id_with_options(self, id: str, request: dingtalkyida__1__0_models.GetInstanceByIdRequest, headers: dingtalkyida__1__0_models.GetInstanceByIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstanceByIdResponse:
        UtilClient.validate_model(request)
        id = OpenApiUtilClient.get_encode_param(id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstanceByIdResponse(), self.do_roarequest('GetInstanceById', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/instancesInfos/{id}', 'json', req, runtime))

    async def get_instance_by_id_with_options_async(self, id: str, request: dingtalkyida__1__0_models.GetInstanceByIdRequest, headers: dingtalkyida__1__0_models.GetInstanceByIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstanceByIdResponse:
        UtilClient.validate_model(request)
        id = OpenApiUtilClient.get_encode_param(id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstanceByIdResponse(), await self.do_roarequest_async('GetInstanceById', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/instancesInfos/{id}', 'json', req, runtime))

    def get_instance_id_list(self, request: dingtalkyida__1__0_models.GetInstanceIdListRequest) -> dingtalkyida__1__0_models.GetInstanceIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstanceIdListHeaders()
        return self.get_instance_id_list_with_options(request, headers, runtime)

    async def get_instance_id_list_async(self, request: dingtalkyida__1__0_models.GetInstanceIdListRequest) -> dingtalkyida__1__0_models.GetInstanceIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstanceIdListHeaders()
        return await self.get_instance_id_list_with_options_async(request, headers, runtime)

    def get_instance_id_list_with_options(self, request: dingtalkyida__1__0_models.GetInstanceIdListRequest, headers: dingtalkyida__1__0_models.GetInstanceIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstanceIdListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.approved_result):
            body['approvedResult'] = request.approved_result
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.instance_status):
            body['instanceStatus'] = request.instance_status
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstanceIdListResponse(), self.do_roarequest('GetInstanceIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instanceIds', 'json', req, runtime))

    async def get_instance_id_list_with_options_async(self, request: dingtalkyida__1__0_models.GetInstanceIdListRequest, headers: dingtalkyida__1__0_models.GetInstanceIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstanceIdListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.approved_result):
            body['approvedResult'] = request.approved_result
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.instance_status):
            body['instanceStatus'] = request.instance_status
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstanceIdListResponse(), await self.do_roarequest_async('GetInstanceIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instanceIds', 'json', req, runtime))

    def get_instances(self, request: dingtalkyida__1__0_models.GetInstancesRequest) -> dingtalkyida__1__0_models.GetInstancesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstancesHeaders()
        return self.get_instances_with_options(request, headers, runtime)

    async def get_instances_async(self, request: dingtalkyida__1__0_models.GetInstancesRequest) -> dingtalkyida__1__0_models.GetInstancesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstancesHeaders()
        return await self.get_instances_with_options_async(request, headers, runtime)

    def get_instances_with_options(self, request: dingtalkyida__1__0_models.GetInstancesRequest, headers: dingtalkyida__1__0_models.GetInstancesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstancesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.approved_result):
            body['approvedResult'] = request.approved_result
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.instance_status):
            body['instanceStatus'] = request.instance_status
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstancesResponse(), self.do_roarequest('GetInstances', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instances', 'json', req, runtime))

    async def get_instances_with_options_async(self, request: dingtalkyida__1__0_models.GetInstancesRequest, headers: dingtalkyida__1__0_models.GetInstancesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstancesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.approved_result):
            body['approvedResult'] = request.approved_result
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.instance_status):
            body['instanceStatus'] = request.instance_status
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstancesResponse(), await self.do_roarequest_async('GetInstances', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instances', 'json', req, runtime))

    def get_instances_by_id_list(self, request: dingtalkyida__1__0_models.GetInstancesByIdListRequest) -> dingtalkyida__1__0_models.GetInstancesByIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstancesByIdListHeaders()
        return self.get_instances_by_id_list_with_options(request, headers, runtime)

    async def get_instances_by_id_list_async(self, request: dingtalkyida__1__0_models.GetInstancesByIdListRequest) -> dingtalkyida__1__0_models.GetInstancesByIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetInstancesByIdListHeaders()
        return await self.get_instances_by_id_list_with_options_async(request, headers, runtime)

    def get_instances_by_id_list_with_options(self, request: dingtalkyida__1__0_models.GetInstancesByIdListRequest, headers: dingtalkyida__1__0_models.GetInstancesByIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstancesByIdListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_ids):
            query['processInstanceIds'] = request.process_instance_ids
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstancesByIdListResponse(), self.do_roarequest('GetInstancesByIdList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/instances/searchWithIds', 'json', req, runtime))

    async def get_instances_by_id_list_with_options_async(self, request: dingtalkyida__1__0_models.GetInstancesByIdListRequest, headers: dingtalkyida__1__0_models.GetInstancesByIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetInstancesByIdListResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_ids):
            query['processInstanceIds'] = request.process_instance_ids
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetInstancesByIdListResponse(), await self.do_roarequest_async('GetInstancesByIdList', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/instances/searchWithIds', 'json', req, runtime))

    def get_me_corp_submission(self, user_id: str, request: dingtalkyida__1__0_models.GetMeCorpSubmissionRequest) -> dingtalkyida__1__0_models.GetMeCorpSubmissionResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetMeCorpSubmissionHeaders()
        return self.get_me_corp_submission_with_options(user_id, request, headers, runtime)

    async def get_me_corp_submission_async(self, user_id: str, request: dingtalkyida__1__0_models.GetMeCorpSubmissionRequest) -> dingtalkyida__1__0_models.GetMeCorpSubmissionResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetMeCorpSubmissionHeaders()
        return await self.get_me_corp_submission_with_options_async(user_id, request, headers, runtime)

    def get_me_corp_submission_with_options(self, user_id: str, request: dingtalkyida__1__0_models.GetMeCorpSubmissionRequest, headers: dingtalkyida__1__0_models.GetMeCorpSubmissionHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetMeCorpSubmissionResponse:
        UtilClient.validate_model(request)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetMeCorpSubmissionResponse(), self.do_roarequest('GetMeCorpSubmission', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/myCorpSubmission/{user_id}', 'json', req, runtime))

    async def get_me_corp_submission_with_options_async(self, user_id: str, request: dingtalkyida__1__0_models.GetMeCorpSubmissionRequest, headers: dingtalkyida__1__0_models.GetMeCorpSubmissionHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetMeCorpSubmissionResponse:
        UtilClient.validate_model(request)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetMeCorpSubmissionResponse(), await self.do_roarequest_async('GetMeCorpSubmission', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/myCorpSubmission/{user_id}', 'json', req, runtime))

    def get_notify_me(self, user_id: str, request: dingtalkyida__1__0_models.GetNotifyMeRequest) -> dingtalkyida__1__0_models.GetNotifyMeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetNotifyMeHeaders()
        return self.get_notify_me_with_options(user_id, request, headers, runtime)

    async def get_notify_me_async(self, user_id: str, request: dingtalkyida__1__0_models.GetNotifyMeRequest) -> dingtalkyida__1__0_models.GetNotifyMeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetNotifyMeHeaders()
        return await self.get_notify_me_with_options_async(user_id, request, headers, runtime)

    def get_notify_me_with_options(self, user_id: str, request: dingtalkyida__1__0_models.GetNotifyMeRequest, headers: dingtalkyida__1__0_models.GetNotifyMeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetNotifyMeResponse:
        UtilClient.validate_model(request)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.instance_create_from_time_gmt):
            query['instanceCreateFromTimeGMT'] = request.instance_create_from_time_gmt
        if not UtilClient.is_unset(request.instance_create_to_time_gmt):
            query['instanceCreateToTimeGMT'] = request.instance_create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetNotifyMeResponse(), self.do_roarequest('GetNotifyMe', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/corpNotifications/{user_id}', 'json', req, runtime))

    async def get_notify_me_with_options_async(self, user_id: str, request: dingtalkyida__1__0_models.GetNotifyMeRequest, headers: dingtalkyida__1__0_models.GetNotifyMeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetNotifyMeResponse:
        UtilClient.validate_model(request)
        user_id = OpenApiUtilClient.get_encode_param(user_id)
        query = {}
        if not UtilClient.is_unset(request.app_types):
            query['appTypes'] = request.app_types
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.instance_create_from_time_gmt):
            query['instanceCreateFromTimeGMT'] = request.instance_create_from_time_gmt
        if not UtilClient.is_unset(request.instance_create_to_time_gmt):
            query['instanceCreateToTimeGMT'] = request.instance_create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetNotifyMeResponse(), await self.do_roarequest_async('GetNotifyMe', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/corpNotifications/{user_id}', 'json', req, runtime))

    def get_open_url(self, app_type: str, request: dingtalkyida__1__0_models.GetOpenUrlRequest) -> dingtalkyida__1__0_models.GetOpenUrlResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetOpenUrlHeaders()
        return self.get_open_url_with_options(app_type, request, headers, runtime)

    async def get_open_url_async(self, app_type: str, request: dingtalkyida__1__0_models.GetOpenUrlRequest) -> dingtalkyida__1__0_models.GetOpenUrlResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetOpenUrlHeaders()
        return await self.get_open_url_with_options_async(app_type, request, headers, runtime)

    def get_open_url_with_options(self, app_type: str, request: dingtalkyida__1__0_models.GetOpenUrlRequest, headers: dingtalkyida__1__0_models.GetOpenUrlHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetOpenUrlResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        query = {}
        if not UtilClient.is_unset(request.file_url):
            query['fileUrl'] = request.file_url
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.timeout):
            query['timeout'] = request.timeout
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetOpenUrlResponse(), self.do_roarequest('GetOpenUrl', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/temporaryUrls/{app_type}', 'json', req, runtime))

    async def get_open_url_with_options_async(self, app_type: str, request: dingtalkyida__1__0_models.GetOpenUrlRequest, headers: dingtalkyida__1__0_models.GetOpenUrlHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetOpenUrlResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        query = {}
        if not UtilClient.is_unset(request.file_url):
            query['fileUrl'] = request.file_url
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.timeout):
            query['timeout'] = request.timeout
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetOpenUrlResponse(), await self.do_roarequest_async('GetOpenUrl', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/temporaryUrls/{app_type}', 'json', req, runtime))

    def get_operation_records(self, request: dingtalkyida__1__0_models.GetOperationRecordsRequest) -> dingtalkyida__1__0_models.GetOperationRecordsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetOperationRecordsHeaders()
        return self.get_operation_records_with_options(request, headers, runtime)

    async def get_operation_records_async(self, request: dingtalkyida__1__0_models.GetOperationRecordsRequest) -> dingtalkyida__1__0_models.GetOperationRecordsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetOperationRecordsHeaders()
        return await self.get_operation_records_with_options_async(request, headers, runtime)

    def get_operation_records_with_options(self, request: dingtalkyida__1__0_models.GetOperationRecordsRequest, headers: dingtalkyida__1__0_models.GetOperationRecordsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetOperationRecordsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetOperationRecordsResponse(), self.do_roarequest('GetOperationRecords', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/operationRecords', 'json', req, runtime))

    async def get_operation_records_with_options_async(self, request: dingtalkyida__1__0_models.GetOperationRecordsRequest, headers: dingtalkyida__1__0_models.GetOperationRecordsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetOperationRecordsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetOperationRecordsResponse(), await self.do_roarequest_async('GetOperationRecords', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/operationRecords', 'json', req, runtime))

    def get_platform_resource(self, request: dingtalkyida__1__0_models.GetPlatformResourceRequest) -> dingtalkyida__1__0_models.GetPlatformResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPlatformResourceHeaders()
        return self.get_platform_resource_with_options(request, headers, runtime)

    async def get_platform_resource_async(self, request: dingtalkyida__1__0_models.GetPlatformResourceRequest) -> dingtalkyida__1__0_models.GetPlatformResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPlatformResourceHeaders()
        return await self.get_platform_resource_with_options_async(request, headers, runtime)

    def get_platform_resource_with_options(self, request: dingtalkyida__1__0_models.GetPlatformResourceRequest, headers: dingtalkyida__1__0_models.GetPlatformResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPlatformResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPlatformResourceResponse(), self.do_roarequest('GetPlatformResource', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/platformResources', 'json', req, runtime))

    async def get_platform_resource_with_options_async(self, request: dingtalkyida__1__0_models.GetPlatformResourceRequest, headers: dingtalkyida__1__0_models.GetPlatformResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPlatformResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPlatformResourceResponse(), await self.do_roarequest_async('GetPlatformResource', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/platformResources', 'json', req, runtime))

    def get_print_app_info(self, request: dingtalkyida__1__0_models.GetPrintAppInfoRequest) -> dingtalkyida__1__0_models.GetPrintAppInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPrintAppInfoHeaders()
        return self.get_print_app_info_with_options(request, headers, runtime)

    async def get_print_app_info_async(self, request: dingtalkyida__1__0_models.GetPrintAppInfoRequest) -> dingtalkyida__1__0_models.GetPrintAppInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPrintAppInfoHeaders()
        return await self.get_print_app_info_with_options_async(request, headers, runtime)

    def get_print_app_info_with_options(self, request: dingtalkyida__1__0_models.GetPrintAppInfoRequest, headers: dingtalkyida__1__0_models.GetPrintAppInfoHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPrintAppInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name_like):
            query['nameLike'] = request.name_like
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPrintAppInfoResponse(), self.do_roarequest('GetPrintAppInfo', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/printTemplates/printAppInfos', 'json', req, runtime))

    async def get_print_app_info_with_options_async(self, request: dingtalkyida__1__0_models.GetPrintAppInfoRequest, headers: dingtalkyida__1__0_models.GetPrintAppInfoHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPrintAppInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name_like):
            query['nameLike'] = request.name_like
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPrintAppInfoResponse(), await self.do_roarequest_async('GetPrintAppInfo', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/printTemplates/printAppInfos', 'json', req, runtime))

    def get_print_dictionary(self, request: dingtalkyida__1__0_models.GetPrintDictionaryRequest) -> dingtalkyida__1__0_models.GetPrintDictionaryResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPrintDictionaryHeaders()
        return self.get_print_dictionary_with_options(request, headers, runtime)

    async def get_print_dictionary_async(self, request: dingtalkyida__1__0_models.GetPrintDictionaryRequest) -> dingtalkyida__1__0_models.GetPrintDictionaryResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetPrintDictionaryHeaders()
        return await self.get_print_dictionary_with_options_async(request, headers, runtime)

    def get_print_dictionary_with_options(self, request: dingtalkyida__1__0_models.GetPrintDictionaryRequest, headers: dingtalkyida__1__0_models.GetPrintDictionaryHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPrintDictionaryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPrintDictionaryResponse(), self.do_roarequest('GetPrintDictionary', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/printTemplates/printDictionaries', 'json', req, runtime))

    async def get_print_dictionary_with_options_async(self, request: dingtalkyida__1__0_models.GetPrintDictionaryRequest, headers: dingtalkyida__1__0_models.GetPrintDictionaryHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetPrintDictionaryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetPrintDictionaryResponse(), await self.do_roarequest_async('GetPrintDictionary', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/printTemplates/printDictionaries', 'json', req, runtime))

    def get_process_definition(self, process_instance_id: str, request: dingtalkyida__1__0_models.GetProcessDefinitionRequest) -> dingtalkyida__1__0_models.GetProcessDefinitionResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetProcessDefinitionHeaders()
        return self.get_process_definition_with_options(process_instance_id, request, headers, runtime)

    async def get_process_definition_async(self, process_instance_id: str, request: dingtalkyida__1__0_models.GetProcessDefinitionRequest) -> dingtalkyida__1__0_models.GetProcessDefinitionResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetProcessDefinitionHeaders()
        return await self.get_process_definition_with_options_async(process_instance_id, request, headers, runtime)

    def get_process_definition_with_options(self, process_instance_id: str, request: dingtalkyida__1__0_models.GetProcessDefinitionRequest, headers: dingtalkyida__1__0_models.GetProcessDefinitionHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetProcessDefinitionResponse:
        UtilClient.validate_model(request)
        process_instance_id = OpenApiUtilClient.get_encode_param(process_instance_id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.group_id):
            query['groupId'] = request.group_id
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.name_space):
            query['nameSpace'] = request.name_space
        if not UtilClient.is_unset(request.order_number):
            query['orderNumber'] = request.order_number
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.system_type):
            query['systemType'] = request.system_type
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetProcessDefinitionResponse(), self.do_roarequest('GetProcessDefinition', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/definitions/{process_instance_id}', 'json', req, runtime))

    async def get_process_definition_with_options_async(self, process_instance_id: str, request: dingtalkyida__1__0_models.GetProcessDefinitionRequest, headers: dingtalkyida__1__0_models.GetProcessDefinitionHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetProcessDefinitionResponse:
        UtilClient.validate_model(request)
        process_instance_id = OpenApiUtilClient.get_encode_param(process_instance_id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.group_id):
            query['groupId'] = request.group_id
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.name_space):
            query['nameSpace'] = request.name_space
        if not UtilClient.is_unset(request.order_number):
            query['orderNumber'] = request.order_number
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.system_type):
            query['systemType'] = request.system_type
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetProcessDefinitionResponse(), await self.do_roarequest_async('GetProcessDefinition', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/definitions/{process_instance_id}', 'json', req, runtime))

    def get_running_task_list(self, request: dingtalkyida__1__0_models.GetRunningTaskListRequest) -> dingtalkyida__1__0_models.GetRunningTaskListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetRunningTaskListHeaders()
        return self.get_running_task_list_with_options(request, headers, runtime)

    async def get_running_task_list_async(self, request: dingtalkyida__1__0_models.GetRunningTaskListRequest) -> dingtalkyida__1__0_models.GetRunningTaskListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetRunningTaskListHeaders()
        return await self.get_running_task_list_with_options_async(request, headers, runtime)

    def get_running_task_list_with_options(self, request: dingtalkyida__1__0_models.GetRunningTaskListRequest, headers: dingtalkyida__1__0_models.GetRunningTaskListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetRunningTaskListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.process_instance_id_list):
            body['processInstanceIdList'] = request.process_instance_id_list
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_corp_id):
            body['userCorpId'] = request.user_corp_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetRunningTaskListResponse(), self.do_roarequest('GetRunningTaskList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/runningTasks/query', 'json', req, runtime))

    async def get_running_task_list_with_options_async(self, request: dingtalkyida__1__0_models.GetRunningTaskListRequest, headers: dingtalkyida__1__0_models.GetRunningTaskListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetRunningTaskListResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.process_instance_id_list):
            body['processInstanceIdList'] = request.process_instance_id_list
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_corp_id):
            body['userCorpId'] = request.user_corp_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetRunningTaskListResponse(), await self.do_roarequest_async('GetRunningTaskList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/runningTasks/query', 'json', req, runtime))

    def get_running_tasks(self, request: dingtalkyida__1__0_models.GetRunningTasksRequest) -> dingtalkyida__1__0_models.GetRunningTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetRunningTasksHeaders()
        return self.get_running_tasks_with_options(request, headers, runtime)

    async def get_running_tasks_async(self, request: dingtalkyida__1__0_models.GetRunningTasksRequest) -> dingtalkyida__1__0_models.GetRunningTasksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetRunningTasksHeaders()
        return await self.get_running_tasks_with_options_async(request, headers, runtime)

    def get_running_tasks_with_options(self, request: dingtalkyida__1__0_models.GetRunningTasksRequest, headers: dingtalkyida__1__0_models.GetRunningTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetRunningTasksResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetRunningTasksResponse(), self.do_roarequest('GetRunningTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/tasks/getRunningTasks', 'json', req, runtime))

    async def get_running_tasks_with_options_async(self, request: dingtalkyida__1__0_models.GetRunningTasksRequest, headers: dingtalkyida__1__0_models.GetRunningTasksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetRunningTasksResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetRunningTasksResponse(), await self.do_roarequest_async('GetRunningTasks', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/processes/tasks/getRunningTasks', 'json', req, runtime))

    def get_sale_user_info_by_user_id(self, request: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdRequest) -> dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetSaleUserInfoByUserIdHeaders()
        return self.get_sale_user_info_by_user_id_with_options(request, headers, runtime)

    async def get_sale_user_info_by_user_id_async(self, request: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdRequest) -> dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetSaleUserInfoByUserIdHeaders()
        return await self.get_sale_user_info_by_user_id_with_options_async(request, headers, runtime)

    def get_sale_user_info_by_user_id_with_options(self, request: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdRequest, headers: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.namespace):
            query['namespace'] = request.namespace
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse(), self.do_roarequest('GetSaleUserInfoByUserId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/saleUserInfo', 'json', req, runtime))

    async def get_sale_user_info_by_user_id_with_options_async(self, request: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdRequest, headers: dingtalkyida__1__0_models.GetSaleUserInfoByUserIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.namespace):
            query['namespace'] = request.namespace
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetSaleUserInfoByUserIdResponse(), await self.do_roarequest_async('GetSaleUserInfoByUserId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/saleUserInfo', 'json', req, runtime))

    def get_task_copies(self, request: dingtalkyida__1__0_models.GetTaskCopiesRequest) -> dingtalkyida__1__0_models.GetTaskCopiesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetTaskCopiesHeaders()
        return self.get_task_copies_with_options(request, headers, runtime)

    async def get_task_copies_async(self, request: dingtalkyida__1__0_models.GetTaskCopiesRequest) -> dingtalkyida__1__0_models.GetTaskCopiesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.GetTaskCopiesHeaders()
        return await self.get_task_copies_with_options_async(request, headers, runtime)

    def get_task_copies_with_options(self, request: dingtalkyida__1__0_models.GetTaskCopiesRequest, headers: dingtalkyida__1__0_models.GetTaskCopiesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetTaskCopiesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetTaskCopiesResponse(), self.do_roarequest('GetTaskCopies', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/taskCopies', 'json', req, runtime))

    async def get_task_copies_with_options_async(self, request: dingtalkyida__1__0_models.GetTaskCopiesRequest, headers: dingtalkyida__1__0_models.GetTaskCopiesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.GetTaskCopiesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            query['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            query['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.process_codes):
            query['processCodes'] = request.process_codes
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.GetTaskCopiesResponse(), await self.do_roarequest_async('GetTaskCopies', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/tasks/taskCopies', 'json', req, runtime))

    def list_application(self, request: dingtalkyida__1__0_models.ListApplicationRequest) -> dingtalkyida__1__0_models.ListApplicationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationHeaders()
        return self.list_application_with_options(request, headers, runtime)

    async def list_application_async(self, request: dingtalkyida__1__0_models.ListApplicationRequest) -> dingtalkyida__1__0_models.ListApplicationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationHeaders()
        return await self.list_application_with_options_async(request, headers, runtime)

    def list_application_with_options(self, request: dingtalkyida__1__0_models.ListApplicationRequest, headers: dingtalkyida__1__0_models.ListApplicationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_filter):
            query['appFilter'] = request.app_filter
        if not UtilClient.is_unset(request.app_name_search_keyword):
            query['appNameSearchKeyword'] = request.app_name_search_keyword
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationResponse(), self.do_roarequest('ListApplication', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/organizations/applications', 'json', req, runtime))

    async def list_application_with_options_async(self, request: dingtalkyida__1__0_models.ListApplicationRequest, headers: dingtalkyida__1__0_models.ListApplicationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_filter):
            query['appFilter'] = request.app_filter
        if not UtilClient.is_unset(request.app_name_search_keyword):
            query['appNameSearchKeyword'] = request.app_name_search_keyword
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationResponse(), await self.do_roarequest_async('ListApplication', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/organizations/applications', 'json', req, runtime))

    def list_application_authorization_service_application_information(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationRequest) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationHeaders()
        return self.list_application_authorization_service_application_information_with_options(instance_id, request, headers, runtime)

    async def list_application_authorization_service_application_information_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationRequest) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationHeaders()
        return await self.list_application_authorization_service_application_information_with_options_async(instance_id, request, headers, runtime)

    def list_application_authorization_service_application_information_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            query['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse(), self.do_roarequest('ListApplicationAuthorizationServiceApplicationInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/authorizations/applicationInfos/{instance_id}', 'json', req, runtime))

    async def list_application_authorization_service_application_information_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            query['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationAuthorizationServiceApplicationInformationResponse(), await self.do_roarequest_async('ListApplicationAuthorizationServiceApplicationInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/authorizations/applicationInfos/{instance_id}', 'json', req, runtime))

    def list_application_authorization_service_connector_information(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationRequest) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationHeaders()
        return self.list_application_authorization_service_connector_information_with_options(instance_id, request, headers, runtime)

    async def list_application_authorization_service_connector_information_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationRequest) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationHeaders()
        return await self.list_application_authorization_service_connector_information_with_options_async(instance_id, request, headers, runtime)

    def list_application_authorization_service_connector_information_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse(), self.do_roarequest('ListApplicationAuthorizationServiceConnectorInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applicationAuthorizations/plugs/{instance_id}', 'json', req, runtime))

    async def list_application_authorization_service_connector_information_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationAuthorizationServiceConnectorInformationResponse(), await self.do_roarequest_async('ListApplicationAuthorizationServiceConnectorInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applicationAuthorizations/plugs/{instance_id}', 'json', req, runtime))

    def list_application_information(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationInformationRequest) -> dingtalkyida__1__0_models.ListApplicationInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationInformationHeaders()
        return self.list_application_information_with_options(instance_id, request, headers, runtime)

    async def list_application_information_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationInformationRequest) -> dingtalkyida__1__0_models.ListApplicationInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListApplicationInformationHeaders()
        return await self.list_application_information_with_options_async(instance_id, request, headers, runtime)

    def list_application_information_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationInformationResponse(), self.do_roarequest('ListApplicationInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/infos/{instance_id}', 'json', req, runtime))

    async def list_application_information_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListApplicationInformationRequest, headers: dingtalkyida__1__0_models.ListApplicationInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListApplicationInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListApplicationInformationResponse(), await self.do_roarequest_async('ListApplicationInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/infos/{instance_id}', 'json', req, runtime))

    def list_commodity(self, request: dingtalkyida__1__0_models.ListCommodityRequest) -> dingtalkyida__1__0_models.ListCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListCommodityHeaders()
        return self.list_commodity_with_options(request, headers, runtime)

    async def list_commodity_async(self, request: dingtalkyida__1__0_models.ListCommodityRequest) -> dingtalkyida__1__0_models.ListCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListCommodityHeaders()
        return await self.list_commodity_with_options_async(request, headers, runtime)

    def list_commodity_with_options(self, request: dingtalkyida__1__0_models.ListCommodityRequest, headers: dingtalkyida__1__0_models.ListCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListCommodityResponse(), self.do_roarequest('ListCommodity', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/appAuth/commodities', 'json', req, runtime))

    async def list_commodity_with_options_async(self, request: dingtalkyida__1__0_models.ListCommodityRequest, headers: dingtalkyida__1__0_models.ListCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListCommodityResponse(), await self.do_roarequest_async('ListCommodity', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/appAuth/commodities', 'json', req, runtime))

    def list_connector_information(self, instance_id: str, request: dingtalkyida__1__0_models.ListConnectorInformationRequest) -> dingtalkyida__1__0_models.ListConnectorInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListConnectorInformationHeaders()
        return self.list_connector_information_with_options(instance_id, request, headers, runtime)

    async def list_connector_information_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListConnectorInformationRequest) -> dingtalkyida__1__0_models.ListConnectorInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListConnectorInformationHeaders()
        return await self.list_connector_information_with_options_async(instance_id, request, headers, runtime)

    def list_connector_information_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ListConnectorInformationRequest, headers: dingtalkyida__1__0_models.ListConnectorInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListConnectorInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListConnectorInformationResponse(), self.do_roarequest('ListConnectorInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/plugins/infos/{instance_id}', 'json', req, runtime))

    async def list_connector_information_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ListConnectorInformationRequest, headers: dingtalkyida__1__0_models.ListConnectorInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListConnectorInformationResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListConnectorInformationResponse(), await self.do_roarequest_async('ListConnectorInformation', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/plugins/infos/{instance_id}', 'json', req, runtime))

    def list_form_remarks(self, request: dingtalkyida__1__0_models.ListFormRemarksRequest) -> dingtalkyida__1__0_models.ListFormRemarksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListFormRemarksHeaders()
        return self.list_form_remarks_with_options(request, headers, runtime)

    async def list_form_remarks_async(self, request: dingtalkyida__1__0_models.ListFormRemarksRequest) -> dingtalkyida__1__0_models.ListFormRemarksResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListFormRemarksHeaders()
        return await self.list_form_remarks_with_options_async(request, headers, runtime)

    def list_form_remarks_with_options(self, request: dingtalkyida__1__0_models.ListFormRemarksRequest, headers: dingtalkyida__1__0_models.ListFormRemarksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListFormRemarksResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListFormRemarksResponse(), self.do_roarequest('ListFormRemarks', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/remarks/query', 'json', req, runtime))

    async def list_form_remarks_with_options_async(self, request: dingtalkyida__1__0_models.ListFormRemarksRequest, headers: dingtalkyida__1__0_models.ListFormRemarksHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListFormRemarksResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListFormRemarksResponse(), await self.do_roarequest_async('ListFormRemarks', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/remarks/query', 'json', req, runtime))

    def list_navigation_by_form_type(self, request: dingtalkyida__1__0_models.ListNavigationByFormTypeRequest) -> dingtalkyida__1__0_models.ListNavigationByFormTypeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListNavigationByFormTypeHeaders()
        return self.list_navigation_by_form_type_with_options(request, headers, runtime)

    async def list_navigation_by_form_type_async(self, request: dingtalkyida__1__0_models.ListNavigationByFormTypeRequest) -> dingtalkyida__1__0_models.ListNavigationByFormTypeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListNavigationByFormTypeHeaders()
        return await self.list_navigation_by_form_type_with_options_async(request, headers, runtime)

    def list_navigation_by_form_type_with_options(self, request: dingtalkyida__1__0_models.ListNavigationByFormTypeRequest, headers: dingtalkyida__1__0_models.ListNavigationByFormTypeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListNavigationByFormTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_type):
            query['formType'] = request.form_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListNavigationByFormTypeResponse(), self.do_roarequest('ListNavigationByFormType', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/navigations', 'json', req, runtime))

    async def list_navigation_by_form_type_with_options_async(self, request: dingtalkyida__1__0_models.ListNavigationByFormTypeRequest, headers: dingtalkyida__1__0_models.ListNavigationByFormTypeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListNavigationByFormTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_type):
            query['formType'] = request.form_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListNavigationByFormTypeResponse(), await self.do_roarequest_async('ListNavigationByFormType', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/navigations', 'json', req, runtime))

    def list_operation_logs(self, request: dingtalkyida__1__0_models.ListOperationLogsRequest) -> dingtalkyida__1__0_models.ListOperationLogsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListOperationLogsHeaders()
        return self.list_operation_logs_with_options(request, headers, runtime)

    async def list_operation_logs_async(self, request: dingtalkyida__1__0_models.ListOperationLogsRequest) -> dingtalkyida__1__0_models.ListOperationLogsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListOperationLogsHeaders()
        return await self.list_operation_logs_with_options_async(request, headers, runtime)

    def list_operation_logs_with_options(self, request: dingtalkyida__1__0_models.ListOperationLogsRequest, headers: dingtalkyida__1__0_models.ListOperationLogsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListOperationLogsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListOperationLogsResponse(), self.do_roarequest('ListOperationLogs', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/operationsLogs/query', 'json', req, runtime))

    async def list_operation_logs_with_options_async(self, request: dingtalkyida__1__0_models.ListOperationLogsRequest, headers: dingtalkyida__1__0_models.ListOperationLogsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListOperationLogsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id_list):
            body['formInstanceIdList'] = request.form_instance_id_list
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListOperationLogsResponse(), await self.do_roarequest_async('ListOperationLogs', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/operationsLogs/query', 'json', req, runtime))

    def list_table_data_by_form_instance_id_table_id(self, form_instance_id: str, request: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdRequest) -> dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdHeaders()
        return self.list_table_data_by_form_instance_id_table_id_with_options(form_instance_id, request, headers, runtime)

    async def list_table_data_by_form_instance_id_table_id_async(self, form_instance_id: str, request: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdRequest) -> dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdHeaders()
        return await self.list_table_data_by_form_instance_id_table_id_with_options_async(form_instance_id, request, headers, runtime)

    def list_table_data_by_form_instance_id_table_id_with_options(self, form_instance_id: str, request: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdRequest, headers: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse:
        UtilClient.validate_model(request)
        form_instance_id = OpenApiUtilClient.get_encode_param(form_instance_id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.table_field_id):
            query['tableFieldId'] = request.table_field_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse(), self.do_roarequest('ListTableDataByFormInstanceIdTableId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/innerTables/{form_instance_id}', 'json', req, runtime))

    async def list_table_data_by_form_instance_id_table_id_with_options_async(self, form_instance_id: str, request: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdRequest, headers: dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse:
        UtilClient.validate_model(request)
        form_instance_id = OpenApiUtilClient.get_encode_param(form_instance_id)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.table_field_id):
            query['tableFieldId'] = request.table_field_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ListTableDataByFormInstanceIdTableIdResponse(), await self.do_roarequest_async('ListTableDataByFormInstanceIdTableId', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/forms/innerTables/{form_instance_id}', 'json', req, runtime))

    def login_code_gen(self, request: dingtalkyida__1__0_models.LoginCodeGenRequest) -> dingtalkyida__1__0_models.LoginCodeGenResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.LoginCodeGenHeaders()
        return self.login_code_gen_with_options(request, headers, runtime)

    async def login_code_gen_async(self, request: dingtalkyida__1__0_models.LoginCodeGenRequest) -> dingtalkyida__1__0_models.LoginCodeGenResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.LoginCodeGenHeaders()
        return await self.login_code_gen_with_options_async(request, headers, runtime)

    def login_code_gen_with_options(self, request: dingtalkyida__1__0_models.LoginCodeGenRequest, headers: dingtalkyida__1__0_models.LoginCodeGenHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.LoginCodeGenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.LoginCodeGenResponse(), self.do_roarequest('LoginCodeGen', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/authorizations/loginCodes', 'json', req, runtime))

    async def login_code_gen_with_options_async(self, request: dingtalkyida__1__0_models.LoginCodeGenRequest, headers: dingtalkyida__1__0_models.LoginCodeGenHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.LoginCodeGenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.LoginCodeGenResponse(), await self.do_roarequest_async('LoginCodeGen', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/authorizations/loginCodes', 'json', req, runtime))

    def notify_authorization_result(self, request: dingtalkyida__1__0_models.NotifyAuthorizationResultRequest) -> dingtalkyida__1__0_models.NotifyAuthorizationResultResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.NotifyAuthorizationResultHeaders()
        return self.notify_authorization_result_with_options(request, headers, runtime)

    async def notify_authorization_result_async(self, request: dingtalkyida__1__0_models.NotifyAuthorizationResultRequest) -> dingtalkyida__1__0_models.NotifyAuthorizationResultResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.NotifyAuthorizationResultHeaders()
        return await self.notify_authorization_result_with_options_async(request, headers, runtime)

    def notify_authorization_result_with_options(self, request: dingtalkyida__1__0_models.NotifyAuthorizationResultRequest, headers: dingtalkyida__1__0_models.NotifyAuthorizationResultHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.NotifyAuthorizationResultResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_uid):
            body['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.NotifyAuthorizationResultResponse(), self.do_roarequest('NotifyAuthorizationResult', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/authorizationResults/notify', 'json', req, runtime))

    async def notify_authorization_result_with_options_async(self, request: dingtalkyida__1__0_models.NotifyAuthorizationResultRequest, headers: dingtalkyida__1__0_models.NotifyAuthorizationResultHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.NotifyAuthorizationResultResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.begin_time_gmt):
            body['beginTimeGMT'] = request.begin_time_gmt
        if not UtilClient.is_unset(request.caller_uid):
            body['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.charge_type):
            body['chargeType'] = request.charge_type
        if not UtilClient.is_unset(request.commerce_type):
            body['commerceType'] = request.commerce_type
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_name):
            body['instanceName'] = request.instance_name
        if not UtilClient.is_unset(request.produce_code):
            body['produceCode'] = request.produce_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.NotifyAuthorizationResultResponse(), await self.do_roarequest_async('NotifyAuthorizationResult', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/authorizationResults/notify', 'json', req, runtime))

    def page_form_base_infos(self, request: dingtalkyida__1__0_models.PageFormBaseInfosRequest) -> dingtalkyida__1__0_models.PageFormBaseInfosResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.PageFormBaseInfosHeaders()
        return self.page_form_base_infos_with_options(request, headers, runtime)

    async def page_form_base_infos_async(self, request: dingtalkyida__1__0_models.PageFormBaseInfosRequest) -> dingtalkyida__1__0_models.PageFormBaseInfosResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.PageFormBaseInfosHeaders()
        return await self.page_form_base_infos_with_options_async(request, headers, runtime)

    def page_form_base_infos_with_options(self, request: dingtalkyida__1__0_models.PageFormBaseInfosRequest, headers: dingtalkyida__1__0_models.PageFormBaseInfosHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.PageFormBaseInfosResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_key):
            body['appKey'] = request.app_key
        if not UtilClient.is_unset(request.form_type_list):
            body['formTypeList'] = request.form_type_list
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.page_index):
            body['pageIndex'] = request.page_index
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.PageFormBaseInfosResponse(), self.do_roarequest('PageFormBaseInfos', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/forms/query', 'json', req, runtime))

    async def page_form_base_infos_with_options_async(self, request: dingtalkyida__1__0_models.PageFormBaseInfosRequest, headers: dingtalkyida__1__0_models.PageFormBaseInfosHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.PageFormBaseInfosResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_key):
            body['appKey'] = request.app_key
        if not UtilClient.is_unset(request.form_type_list):
            body['formTypeList'] = request.form_type_list
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.page_index):
            body['pageIndex'] = request.page_index
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.PageFormBaseInfosResponse(), await self.do_roarequest_async('PageFormBaseInfos', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/forms/query', 'json', req, runtime))

    def query_service_record(self, request: dingtalkyida__1__0_models.QueryServiceRecordRequest) -> dingtalkyida__1__0_models.QueryServiceRecordResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.QueryServiceRecordHeaders()
        return self.query_service_record_with_options(request, headers, runtime)

    async def query_service_record_async(self, request: dingtalkyida__1__0_models.QueryServiceRecordRequest) -> dingtalkyida__1__0_models.QueryServiceRecordResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.QueryServiceRecordHeaders()
        return await self.query_service_record_with_options_async(request, headers, runtime)

    def query_service_record_with_options(self, request: dingtalkyida__1__0_models.QueryServiceRecordRequest, headers: dingtalkyida__1__0_models.QueryServiceRecordHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.QueryServiceRecordResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.hook_type):
            query['hookType'] = request.hook_type
        if not UtilClient.is_unset(request.hook_uuid):
            query['hookUuid'] = request.hook_uuid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.invoke_after_date_gmt):
            query['invokeAfterDateGMT'] = request.invoke_after_date_gmt
        if not UtilClient.is_unset(request.invoke_before_date_gmt):
            query['invokeBeforeDateGMT'] = request.invoke_before_date_gmt
        if not UtilClient.is_unset(request.invoke_status):
            query['invokeStatus'] = request.invoke_status
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.request_url):
            query['requestUrl'] = request.request_url
        if not UtilClient.is_unset(request.source_uuid):
            query['sourceUuid'] = request.source_uuid
        if not UtilClient.is_unset(request.success):
            query['success'] = request.success
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.QueryServiceRecordResponse(), self.do_roarequest('QueryServiceRecord', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/services/invocationRecords', 'json', req, runtime))

    async def query_service_record_with_options_async(self, request: dingtalkyida__1__0_models.QueryServiceRecordRequest, headers: dingtalkyida__1__0_models.QueryServiceRecordHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.QueryServiceRecordResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_uuid):
            query['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.hook_type):
            query['hookType'] = request.hook_type
        if not UtilClient.is_unset(request.hook_uuid):
            query['hookUuid'] = request.hook_uuid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        if not UtilClient.is_unset(request.invoke_after_date_gmt):
            query['invokeAfterDateGMT'] = request.invoke_after_date_gmt
        if not UtilClient.is_unset(request.invoke_before_date_gmt):
            query['invokeBeforeDateGMT'] = request.invoke_before_date_gmt
        if not UtilClient.is_unset(request.invoke_status):
            query['invokeStatus'] = request.invoke_status
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.request_url):
            query['requestUrl'] = request.request_url
        if not UtilClient.is_unset(request.source_uuid):
            query['sourceUuid'] = request.source_uuid
        if not UtilClient.is_unset(request.success):
            query['success'] = request.success
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.QueryServiceRecordResponse(), await self.do_roarequest_async('QueryServiceRecord', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/services/invocationRecords', 'json', req, runtime))

    def redirect_task(self, request: dingtalkyida__1__0_models.RedirectTaskRequest) -> dingtalkyida__1__0_models.RedirectTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RedirectTaskHeaders()
        return self.redirect_task_with_options(request, headers, runtime)

    async def redirect_task_async(self, request: dingtalkyida__1__0_models.RedirectTaskRequest) -> dingtalkyida__1__0_models.RedirectTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RedirectTaskHeaders()
        return await self.redirect_task_with_options_async(request, headers, runtime)

    def redirect_task_with_options(self, request: dingtalkyida__1__0_models.RedirectTaskRequest, headers: dingtalkyida__1__0_models.RedirectTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RedirectTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.by_manager):
            body['byManager'] = request.by_manager
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.now_action_executor_id):
            body['nowActionExecutorId'] = request.now_action_executor_id
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RedirectTaskResponse(), self.do_roarequest('RedirectTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/redirect', 'none', req, runtime))

    async def redirect_task_with_options_async(self, request: dingtalkyida__1__0_models.RedirectTaskRequest, headers: dingtalkyida__1__0_models.RedirectTaskHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RedirectTaskResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.by_manager):
            body['byManager'] = request.by_manager
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.now_action_executor_id):
            body['nowActionExecutorId'] = request.now_action_executor_id
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.task_id):
            body['taskId'] = request.task_id
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RedirectTaskResponse(), await self.do_roarequest_async('RedirectTask', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/tasks/redirect', 'none', req, runtime))

    def refund_commodity(self, request: dingtalkyida__1__0_models.RefundCommodityRequest) -> dingtalkyida__1__0_models.RefundCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RefundCommodityHeaders()
        return self.refund_commodity_with_options(request, headers, runtime)

    async def refund_commodity_async(self, request: dingtalkyida__1__0_models.RefundCommodityRequest) -> dingtalkyida__1__0_models.RefundCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RefundCommodityHeaders()
        return await self.refund_commodity_with_options_async(request, headers, runtime)

    def refund_commodity_with_options(self, request: dingtalkyida__1__0_models.RefundCommodityRequest, headers: dingtalkyida__1__0_models.RefundCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RefundCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.RefundCommodityResponse(), self.do_roarequest('RefundCommodity', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/appAuth/commodities/refund', 'json', req, runtime))

    async def refund_commodity_with_options_async(self, request: dingtalkyida__1__0_models.RefundCommodityRequest, headers: dingtalkyida__1__0_models.RefundCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RefundCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.RefundCommodityResponse(), await self.do_roarequest_async('RefundCommodity', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/appAuth/commodities/refund', 'json', req, runtime))

    def register_accounts(self, request: dingtalkyida__1__0_models.RegisterAccountsRequest) -> dingtalkyida__1__0_models.RegisterAccountsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RegisterAccountsHeaders()
        return self.register_accounts_with_options(request, headers, runtime)

    async def register_accounts_async(self, request: dingtalkyida__1__0_models.RegisterAccountsRequest) -> dingtalkyida__1__0_models.RegisterAccountsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RegisterAccountsHeaders()
        return await self.register_accounts_with_options_async(request, headers, runtime)

    def register_accounts_with_options(self, request: dingtalkyida__1__0_models.RegisterAccountsRequest, headers: dingtalkyida__1__0_models.RegisterAccountsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RegisterAccountsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.active_code):
            body['activeCode'] = request.active_code
        if not UtilClient.is_unset(request.corp_id):
            body['corpId'] = request.corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RegisterAccountsResponse(), self.do_roarequest('RegisterAccounts', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/applicationAuthorizations/accounts/register', 'json', req, runtime))

    async def register_accounts_with_options_async(self, request: dingtalkyida__1__0_models.RegisterAccountsRequest, headers: dingtalkyida__1__0_models.RegisterAccountsHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RegisterAccountsResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.active_code):
            body['activeCode'] = request.active_code
        if not UtilClient.is_unset(request.corp_id):
            body['corpId'] = request.corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RegisterAccountsResponse(), await self.do_roarequest_async('RegisterAccounts', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/applicationAuthorizations/accounts/register', 'json', req, runtime))

    def release_commodity(self, request: dingtalkyida__1__0_models.ReleaseCommodityRequest) -> dingtalkyida__1__0_models.ReleaseCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ReleaseCommodityHeaders()
        return self.release_commodity_with_options(request, headers, runtime)

    async def release_commodity_async(self, request: dingtalkyida__1__0_models.ReleaseCommodityRequest) -> dingtalkyida__1__0_models.ReleaseCommodityResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ReleaseCommodityHeaders()
        return await self.release_commodity_with_options_async(request, headers, runtime)

    def release_commodity_with_options(self, request: dingtalkyida__1__0_models.ReleaseCommodityRequest, headers: dingtalkyida__1__0_models.ReleaseCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ReleaseCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ReleaseCommodityResponse(), self.do_roarequest('ReleaseCommodity', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/appAuth/commodities/release', 'json', req, runtime))

    async def release_commodity_with_options_async(self, request: dingtalkyida__1__0_models.ReleaseCommodityRequest, headers: dingtalkyida__1__0_models.ReleaseCommodityHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ReleaseCommodityResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ReleaseCommodityResponse(), await self.do_roarequest_async('ReleaseCommodity', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/appAuth/commodities/release', 'json', req, runtime))

    def remove_tenant_resource(self, caller_uid: str, request: dingtalkyida__1__0_models.RemoveTenantResourceRequest) -> dingtalkyida__1__0_models.RemoveTenantResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RemoveTenantResourceHeaders()
        return self.remove_tenant_resource_with_options(caller_uid, request, headers, runtime)

    async def remove_tenant_resource_async(self, caller_uid: str, request: dingtalkyida__1__0_models.RemoveTenantResourceRequest) -> dingtalkyida__1__0_models.RemoveTenantResourceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RemoveTenantResourceHeaders()
        return await self.remove_tenant_resource_with_options_async(caller_uid, request, headers, runtime)

    def remove_tenant_resource_with_options(self, caller_uid: str, request: dingtalkyida__1__0_models.RemoveTenantResourceRequest, headers: dingtalkyida__1__0_models.RemoveTenantResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RemoveTenantResourceResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.RemoveTenantResourceResponse(), self.do_roarequest('RemoveTenantResource', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/applications/tenantRelatedResources/{caller_uid}', 'json', req, runtime))

    async def remove_tenant_resource_with_options_async(self, caller_uid: str, request: dingtalkyida__1__0_models.RemoveTenantResourceRequest, headers: dingtalkyida__1__0_models.RemoveTenantResourceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RemoveTenantResourceResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.RemoveTenantResourceResponse(), await self.do_roarequest_async('RemoveTenantResource', 'yida_1.0', 'HTTP', 'DELETE', 'AK', f'/v1.0/yida/applications/tenantRelatedResources/{caller_uid}', 'json', req, runtime))

    def render_batch_callback(self, request: dingtalkyida__1__0_models.RenderBatchCallbackRequest) -> dingtalkyida__1__0_models.RenderBatchCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenderBatchCallbackHeaders()
        return self.render_batch_callback_with_options(request, headers, runtime)

    async def render_batch_callback_async(self, request: dingtalkyida__1__0_models.RenderBatchCallbackRequest) -> dingtalkyida__1__0_models.RenderBatchCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenderBatchCallbackHeaders()
        return await self.render_batch_callback_with_options_async(request, headers, runtime)

    def render_batch_callback_with_options(self, request: dingtalkyida__1__0_models.RenderBatchCallbackRequest, headers: dingtalkyida__1__0_models.RenderBatchCallbackHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenderBatchCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.corp_id):
            body['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.file_size):
            body['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.namespace):
            body['namespace'] = request.namespace
        if not UtilClient.is_unset(request.oss_url):
            body['ossUrl'] = request.oss_url
        if not UtilClient.is_unset(request.sequence_id):
            body['sequenceId'] = request.sequence_id
        if not UtilClient.is_unset(request.source):
            body['source'] = request.source
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.time_zone):
            body['timeZone'] = request.time_zone
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenderBatchCallbackResponse(), self.do_roarequest('RenderBatchCallback', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/printings/callbacks/batch', 'none', req, runtime))

    async def render_batch_callback_with_options_async(self, request: dingtalkyida__1__0_models.RenderBatchCallbackRequest, headers: dingtalkyida__1__0_models.RenderBatchCallbackHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenderBatchCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.corp_id):
            body['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.file_size):
            body['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.namespace):
            body['namespace'] = request.namespace
        if not UtilClient.is_unset(request.oss_url):
            body['ossUrl'] = request.oss_url
        if not UtilClient.is_unset(request.sequence_id):
            body['sequenceId'] = request.sequence_id
        if not UtilClient.is_unset(request.source):
            body['source'] = request.source
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.time_zone):
            body['timeZone'] = request.time_zone
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenderBatchCallbackResponse(), await self.do_roarequest_async('RenderBatchCallback', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/printings/callbacks/batch', 'none', req, runtime))

    def renew_application_authorization_service_order(self, request: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderRequest) -> dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderHeaders()
        return self.renew_application_authorization_service_order_with_options(request, headers, runtime)

    async def renew_application_authorization_service_order_async(self, request: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderRequest) -> dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderHeaders()
        return await self.renew_application_authorization_service_order_with_options_async(request, headers, runtime)

    def renew_application_authorization_service_order_with_options(self, request: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderRequest, headers: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse(), self.do_roarequest('RenewApplicationAuthorizationServiceOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/applicationAuthorizations/orders/renew', 'json', req, runtime))

    async def renew_application_authorization_service_order_with_options_async(self, request: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderRequest, headers: dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenewApplicationAuthorizationServiceOrderResponse(), await self.do_roarequest_async('RenewApplicationAuthorizationServiceOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/applicationAuthorizations/orders/renew', 'json', req, runtime))

    def renew_tenant_order(self, request: dingtalkyida__1__0_models.RenewTenantOrderRequest) -> dingtalkyida__1__0_models.RenewTenantOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenewTenantOrderHeaders()
        return self.renew_tenant_order_with_options(request, headers, runtime)

    async def renew_tenant_order_async(self, request: dingtalkyida__1__0_models.RenewTenantOrderRequest) -> dingtalkyida__1__0_models.RenewTenantOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.RenewTenantOrderHeaders()
        return await self.renew_tenant_order_with_options_async(request, headers, runtime)

    def renew_tenant_order_with_options(self, request: dingtalkyida__1__0_models.RenewTenantOrderRequest, headers: dingtalkyida__1__0_models.RenewTenantOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenewTenantOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenewTenantOrderResponse(), self.do_roarequest('RenewTenantOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/tenants/reorder', 'json', req, runtime))

    async def renew_tenant_order_with_options_async(self, request: dingtalkyida__1__0_models.RenewTenantOrderRequest, headers: dingtalkyida__1__0_models.RenewTenantOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.RenewTenantOrderResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.end_time_gmt):
            body['endTimeGMT'] = request.end_time_gmt
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.RenewTenantOrderResponse(), await self.do_roarequest_async('RenewTenantOrder', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/tenants/reorder', 'json', req, runtime))

    def save_form_data(self, request: dingtalkyida__1__0_models.SaveFormDataRequest) -> dingtalkyida__1__0_models.SaveFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SaveFormDataHeaders()
        return self.save_form_data_with_options(request, headers, runtime)

    async def save_form_data_async(self, request: dingtalkyida__1__0_models.SaveFormDataRequest) -> dingtalkyida__1__0_models.SaveFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SaveFormDataHeaders()
        return await self.save_form_data_with_options_async(request, headers, runtime)

    def save_form_data_with_options(self, request: dingtalkyida__1__0_models.SaveFormDataRequest, headers: dingtalkyida__1__0_models.SaveFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SaveFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SaveFormDataResponse(), self.do_roarequest('SaveFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances', 'json', req, runtime))

    async def save_form_data_with_options_async(self, request: dingtalkyida__1__0_models.SaveFormDataRequest, headers: dingtalkyida__1__0_models.SaveFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SaveFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SaveFormDataResponse(), await self.do_roarequest_async('SaveFormData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances', 'json', req, runtime))

    def save_form_remark(self, request: dingtalkyida__1__0_models.SaveFormRemarkRequest) -> dingtalkyida__1__0_models.SaveFormRemarkResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SaveFormRemarkHeaders()
        return self.save_form_remark_with_options(request, headers, runtime)

    async def save_form_remark_async(self, request: dingtalkyida__1__0_models.SaveFormRemarkRequest) -> dingtalkyida__1__0_models.SaveFormRemarkResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SaveFormRemarkHeaders()
        return await self.save_form_remark_with_options_async(request, headers, runtime)

    def save_form_remark_with_options(self, request: dingtalkyida__1__0_models.SaveFormRemarkRequest, headers: dingtalkyida__1__0_models.SaveFormRemarkHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SaveFormRemarkResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.at_user_id):
            body['atUserId'] = request.at_user_id
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.form_instance_id):
            body['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.reply_id):
            body['replyId'] = request.reply_id
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SaveFormRemarkResponse(), self.do_roarequest('SaveFormRemark', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/remarks', 'json', req, runtime))

    async def save_form_remark_with_options_async(self, request: dingtalkyida__1__0_models.SaveFormRemarkRequest, headers: dingtalkyida__1__0_models.SaveFormRemarkHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SaveFormRemarkResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.at_user_id):
            body['atUserId'] = request.at_user_id
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.form_instance_id):
            body['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.reply_id):
            body['replyId'] = request.reply_id
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SaveFormRemarkResponse(), await self.do_roarequest_async('SaveFormRemark', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/remarks', 'json', req, runtime))

    def save_print_tpl_detail_info(self, request: dingtalkyida__1__0_models.SavePrintTplDetailInfoRequest) -> dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SavePrintTplDetailInfoHeaders()
        return self.save_print_tpl_detail_info_with_options(request, headers, runtime)

    async def save_print_tpl_detail_info_async(self, request: dingtalkyida__1__0_models.SavePrintTplDetailInfoRequest) -> dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SavePrintTplDetailInfoHeaders()
        return await self.save_print_tpl_detail_info_with_options_async(request, headers, runtime)

    def save_print_tpl_detail_info_with_options(self, request: dingtalkyida__1__0_models.SavePrintTplDetailInfoRequest, headers: dingtalkyida__1__0_models.SavePrintTplDetailInfoHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.description):
            body['description'] = request.description
        if not UtilClient.is_unset(request.file_name_config):
            body['fileNameConfig'] = request.file_name_config
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.form_version):
            body['formVersion'] = request.form_version
        if not UtilClient.is_unset(request.setting):
            body['setting'] = request.setting
        if not UtilClient.is_unset(request.template_id):
            body['templateId'] = request.template_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.vm):
            body['vm'] = request.vm
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse(), self.do_roarequest('SavePrintTplDetailInfo', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/printTemplates/printTplDetailInfos', 'json', req, runtime))

    async def save_print_tpl_detail_info_with_options_async(self, request: dingtalkyida__1__0_models.SavePrintTplDetailInfoRequest, headers: dingtalkyida__1__0_models.SavePrintTplDetailInfoHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.description):
            body['description'] = request.description
        if not UtilClient.is_unset(request.file_name_config):
            body['fileNameConfig'] = request.file_name_config
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.form_version):
            body['formVersion'] = request.form_version
        if not UtilClient.is_unset(request.setting):
            body['setting'] = request.setting
        if not UtilClient.is_unset(request.template_id):
            body['templateId'] = request.template_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.vm):
            body['vm'] = request.vm
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SavePrintTplDetailInfoResponse(), await self.do_roarequest_async('SavePrintTplDetailInfo', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/printTemplates/printTplDetailInfos', 'json', req, runtime))

    def search_activation_code(self, request: dingtalkyida__1__0_models.SearchActivationCodeRequest) -> dingtalkyida__1__0_models.SearchActivationCodeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchActivationCodeHeaders()
        return self.search_activation_code_with_options(request, headers, runtime)

    async def search_activation_code_async(self, request: dingtalkyida__1__0_models.SearchActivationCodeRequest) -> dingtalkyida__1__0_models.SearchActivationCodeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchActivationCodeHeaders()
        return await self.search_activation_code_with_options_async(request, headers, runtime)

    def search_activation_code_with_options(self, request: dingtalkyida__1__0_models.SearchActivationCodeRequest, headers: dingtalkyida__1__0_models.SearchActivationCodeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchActivationCodeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchActivationCodeResponse(), self.do_roarequest('SearchActivationCode', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/activationCode/information', 'json', req, runtime))

    async def search_activation_code_with_options_async(self, request: dingtalkyida__1__0_models.SearchActivationCodeRequest, headers: dingtalkyida__1__0_models.SearchActivationCodeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchActivationCodeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchActivationCodeResponse(), await self.do_roarequest_async('SearchActivationCode', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/activationCode/information', 'json', req, runtime))

    def search_employee_field_values(self, request: dingtalkyida__1__0_models.SearchEmployeeFieldValuesRequest) -> dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchEmployeeFieldValuesHeaders()
        return self.search_employee_field_values_with_options(request, headers, runtime)

    async def search_employee_field_values_async(self, request: dingtalkyida__1__0_models.SearchEmployeeFieldValuesRequest) -> dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchEmployeeFieldValuesHeaders()
        return await self.search_employee_field_values_with_options_async(request, headers, runtime)

    def search_employee_field_values_with_options(self, request: dingtalkyida__1__0_models.SearchEmployeeFieldValuesRequest, headers: dingtalkyida__1__0_models.SearchEmployeeFieldValuesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.target_field_json):
            body['targetFieldJson'] = request.target_field_json
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse(), self.do_roarequest('SearchEmployeeFieldValues', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/employeeFields', 'json', req, runtime))

    async def search_employee_field_values_with_options_async(self, request: dingtalkyida__1__0_models.SearchEmployeeFieldValuesRequest, headers: dingtalkyida__1__0_models.SearchEmployeeFieldValuesHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.target_field_json):
            body['targetFieldJson'] = request.target_field_json
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchEmployeeFieldValuesResponse(), await self.do_roarequest_async('SearchEmployeeFieldValues', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/employeeFields', 'json', req, runtime))

    def search_form_data_id_list(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.SearchFormDataIdListRequest) -> dingtalkyida__1__0_models.SearchFormDataIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataIdListHeaders()
        return self.search_form_data_id_list_with_options(app_type, form_uuid, request, headers, runtime)

    async def search_form_data_id_list_async(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.SearchFormDataIdListRequest) -> dingtalkyida__1__0_models.SearchFormDataIdListResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataIdListHeaders()
        return await self.search_form_data_id_list_with_options_async(app_type, form_uuid, request, headers, runtime)

    def search_form_data_id_list_with_options(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.SearchFormDataIdListRequest, headers: dingtalkyida__1__0_models.SearchFormDataIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataIdListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        form_uuid = OpenApiUtilClient.get_encode_param(form_uuid)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataIdListResponse(), self.do_roarequest('SearchFormDataIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/ids/{app_type}/{form_uuid}', 'json', req, runtime))

    async def search_form_data_id_list_with_options_async(self, app_type: str, form_uuid: str, request: dingtalkyida__1__0_models.SearchFormDataIdListRequest, headers: dingtalkyida__1__0_models.SearchFormDataIdListHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataIdListResponse:
        UtilClient.validate_model(request)
        app_type = OpenApiUtilClient.get_encode_param(app_type)
        form_uuid = OpenApiUtilClient.get_encode_param(form_uuid)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        body = {}
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query), body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataIdListResponse(), await self.do_roarequest_async('SearchFormDataIdList', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/ids/{app_type}/{form_uuid}', 'json', req, runtime))

    def search_form_data_removal_table_data(self, request: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataRequest) -> dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataRemovalTableDataHeaders()
        return self.search_form_data_removal_table_data_with_options(request, headers, runtime)

    async def search_form_data_removal_table_data_async(self, request: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataRequest) -> dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataRemovalTableDataHeaders()
        return await self.search_form_data_removal_table_data_with_options_async(request, headers, runtime)

    def search_form_data_removal_table_data_with_options(self, request: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataRequest, headers: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse(), self.do_roarequest('SearchFormDataRemovalTableData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/query', 'json', req, runtime))

    async def search_form_data_removal_table_data_with_options_async(self, request: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataRequest, headers: dingtalkyida__1__0_models.SearchFormDataRemovalTableDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataRemovalTableDataResponse(), await self.do_roarequest_async('SearchFormDataRemovalTableData', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/query', 'json', req, runtime))

    def search_form_data_second_generation(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationRequest) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataSecondGenerationHeaders()
        return self.search_form_data_second_generation_with_options(request, headers, runtime)

    async def search_form_data_second_generation_async(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationRequest) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataSecondGenerationHeaders()
        return await self.search_form_data_second_generation_with_options_async(request, headers, runtime)

    def search_form_data_second_generation_with_options(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationRequest, headers: dingtalkyida__1__0_models.SearchFormDataSecondGenerationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse(), self.do_roarequest('SearchFormDataSecondGeneration', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/advances/queryAll', 'json', req, runtime))

    async def search_form_data_second_generation_with_options_async(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationRequest, headers: dingtalkyida__1__0_models.SearchFormDataSecondGenerationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataSecondGenerationResponse(), await self.do_roarequest_async('SearchFormDataSecondGeneration', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/advances/queryAll', 'json', req, runtime))

    def search_form_data_second_generation_no_table_field(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldRequest) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldHeaders()
        return self.search_form_data_second_generation_no_table_field_with_options(request, headers, runtime)

    async def search_form_data_second_generation_no_table_field_async(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldRequest) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldHeaders()
        return await self.search_form_data_second_generation_no_table_field_with_options_async(request, headers, runtime)

    def search_form_data_second_generation_no_table_field_with_options(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldRequest, headers: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse(), self.do_roarequest('SearchFormDataSecondGenerationNoTableField', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/advances/query', 'json', req, runtime))

    async def search_form_data_second_generation_no_table_field_with_options_async(self, request: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldRequest, headers: dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.order_config_json):
            body['orderConfigJson'] = request.order_config_json
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_number):
            body['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_condition):
            body['searchCondition'] = request.search_condition
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDataSecondGenerationNoTableFieldResponse(), await self.do_roarequest_async('SearchFormDataSecondGenerationNoTableField', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/advances/query', 'json', req, runtime))

    def search_form_datas(self, request: dingtalkyida__1__0_models.SearchFormDatasRequest) -> dingtalkyida__1__0_models.SearchFormDatasResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDatasHeaders()
        return self.search_form_datas_with_options(request, headers, runtime)

    async def search_form_datas_async(self, request: dingtalkyida__1__0_models.SearchFormDatasRequest) -> dingtalkyida__1__0_models.SearchFormDatasResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.SearchFormDatasHeaders()
        return await self.search_form_datas_with_options_async(request, headers, runtime)

    def search_form_datas_with_options(self, request: dingtalkyida__1__0_models.SearchFormDatasRequest, headers: dingtalkyida__1__0_models.SearchFormDatasHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDatasResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.current_page):
            body['currentPage'] = request.current_page
        if not UtilClient.is_unset(request.dynamic_order):
            body['dynamicOrder'] = request.dynamic_order
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDatasResponse(), self.do_roarequest('SearchFormDatas', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/search', 'json', req, runtime))

    async def search_form_datas_with_options_async(self, request: dingtalkyida__1__0_models.SearchFormDatasRequest, headers: dingtalkyida__1__0_models.SearchFormDatasHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.SearchFormDatasResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.create_from_time_gmt):
            body['createFromTimeGMT'] = request.create_from_time_gmt
        if not UtilClient.is_unset(request.create_to_time_gmt):
            body['createToTimeGMT'] = request.create_to_time_gmt
        if not UtilClient.is_unset(request.current_page):
            body['currentPage'] = request.current_page
        if not UtilClient.is_unset(request.dynamic_order):
            body['dynamicOrder'] = request.dynamic_order
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.modified_from_time_gmt):
            body['modifiedFromTimeGMT'] = request.modified_from_time_gmt
        if not UtilClient.is_unset(request.modified_to_time_gmt):
            body['modifiedToTimeGMT'] = request.modified_to_time_gmt
        if not UtilClient.is_unset(request.originator_id):
            body['originatorId'] = request.originator_id
        if not UtilClient.is_unset(request.page_size):
            body['pageSize'] = request.page_size
        if not UtilClient.is_unset(request.search_field_json):
            body['searchFieldJson'] = request.search_field_json
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.SearchFormDatasResponse(), await self.do_roarequest_async('SearchFormDatas', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/forms/instances/search', 'json', req, runtime))

    def start_instance(self, request: dingtalkyida__1__0_models.StartInstanceRequest) -> dingtalkyida__1__0_models.StartInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.StartInstanceHeaders()
        return self.start_instance_with_options(request, headers, runtime)

    async def start_instance_async(self, request: dingtalkyida__1__0_models.StartInstanceRequest) -> dingtalkyida__1__0_models.StartInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.StartInstanceHeaders()
        return await self.start_instance_with_options_async(request, headers, runtime)

    def start_instance_with_options(self, request: dingtalkyida__1__0_models.StartInstanceRequest, headers: dingtalkyida__1__0_models.StartInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.StartInstanceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.department_id):
            body['departmentId'] = request.department_id
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.process_code):
            body['processCode'] = request.process_code
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.StartInstanceResponse(), self.do_roarequest('StartInstance', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instances/start', 'json', req, runtime))

    async def start_instance_with_options_async(self, request: dingtalkyida__1__0_models.StartInstanceRequest, headers: dingtalkyida__1__0_models.StartInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.StartInstanceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.department_id):
            body['departmentId'] = request.department_id
        if not UtilClient.is_unset(request.form_data_json):
            body['formDataJson'] = request.form_data_json
        if not UtilClient.is_unset(request.form_uuid):
            body['formUuid'] = request.form_uuid
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.process_code):
            body['processCode'] = request.process_code
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.StartInstanceResponse(), await self.do_roarequest_async('StartInstance', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/processes/instances/start', 'json', req, runtime))

    def terminate_cloud_authorization(self, request: dingtalkyida__1__0_models.TerminateCloudAuthorizationRequest) -> dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.TerminateCloudAuthorizationHeaders()
        return self.terminate_cloud_authorization_with_options(request, headers, runtime)

    async def terminate_cloud_authorization_async(self, request: dingtalkyida__1__0_models.TerminateCloudAuthorizationRequest) -> dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.TerminateCloudAuthorizationHeaders()
        return await self.terminate_cloud_authorization_with_options_async(request, headers, runtime)

    def terminate_cloud_authorization_with_options(self, request: dingtalkyida__1__0_models.TerminateCloudAuthorizationRequest, headers: dingtalkyida__1__0_models.TerminateCloudAuthorizationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse(), self.do_roarequest('TerminateCloudAuthorization', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/cloudAuthorizations/terminate', 'json', req, runtime))

    async def terminate_cloud_authorization_with_options_async(self, request: dingtalkyida__1__0_models.TerminateCloudAuthorizationRequest, headers: dingtalkyida__1__0_models.TerminateCloudAuthorizationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.instance_id):
            body['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.TerminateCloudAuthorizationResponse(), await self.do_roarequest_async('TerminateCloudAuthorization', 'yida_1.0', 'HTTP', 'POST', 'AK', f'/v1.0/yida/apps/cloudAuthorizations/terminate', 'json', req, runtime))

    def terminate_instance(self, request: dingtalkyida__1__0_models.TerminateInstanceRequest) -> dingtalkyida__1__0_models.TerminateInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.TerminateInstanceHeaders()
        return self.terminate_instance_with_options(request, headers, runtime)

    async def terminate_instance_async(self, request: dingtalkyida__1__0_models.TerminateInstanceRequest) -> dingtalkyida__1__0_models.TerminateInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.TerminateInstanceHeaders()
        return await self.terminate_instance_with_options_async(request, headers, runtime)

    def terminate_instance_with_options(self, request: dingtalkyida__1__0_models.TerminateInstanceRequest, headers: dingtalkyida__1__0_models.TerminateInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.TerminateInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.TerminateInstanceResponse(), self.do_roarequest('TerminateInstance', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/processes/instances/terminate', 'none', req, runtime))

    async def terminate_instance_with_options_async(self, request: dingtalkyida__1__0_models.TerminateInstanceRequest, headers: dingtalkyida__1__0_models.TerminateInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.TerminateInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_type):
            query['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            query['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            query['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.TerminateInstanceResponse(), await self.do_roarequest_async('TerminateInstance', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/processes/instances/terminate', 'none', req, runtime))

    def update_cloud_account_information(self, request: dingtalkyida__1__0_models.UpdateCloudAccountInformationRequest) -> dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateCloudAccountInformationHeaders()
        return self.update_cloud_account_information_with_options(request, headers, runtime)

    async def update_cloud_account_information_async(self, request: dingtalkyida__1__0_models.UpdateCloudAccountInformationRequest) -> dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateCloudAccountInformationHeaders()
        return await self.update_cloud_account_information_with_options_async(request, headers, runtime)

    def update_cloud_account_information_with_options(self, request: dingtalkyida__1__0_models.UpdateCloudAccountInformationRequest, headers: dingtalkyida__1__0_models.UpdateCloudAccountInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse(), self.do_roarequest('UpdateCloudAccountInformation', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/apps/cloudAccountInfos', 'json', req, runtime))

    async def update_cloud_account_information_with_options_async(self, request: dingtalkyida__1__0_models.UpdateCloudAccountInformationRequest, headers: dingtalkyida__1__0_models.UpdateCloudAccountInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateCloudAccountInformationResponse(), await self.do_roarequest_async('UpdateCloudAccountInformation', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/apps/cloudAccountInfos', 'json', req, runtime))

    def update_form_data(self, request: dingtalkyida__1__0_models.UpdateFormDataRequest) -> dingtalkyida__1__0_models.UpdateFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateFormDataHeaders()
        return self.update_form_data_with_options(request, headers, runtime)

    async def update_form_data_async(self, request: dingtalkyida__1__0_models.UpdateFormDataRequest) -> dingtalkyida__1__0_models.UpdateFormDataResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateFormDataHeaders()
        return await self.update_form_data_with_options_async(request, headers, runtime)

    def update_form_data_with_options(self, request: dingtalkyida__1__0_models.UpdateFormDataRequest, headers: dingtalkyida__1__0_models.UpdateFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id):
            body['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.use_latest_version):
            body['useLatestVersion'] = request.use_latest_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateFormDataResponse(), self.do_roarequest('UpdateFormData', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances', 'none', req, runtime))

    async def update_form_data_with_options_async(self, request: dingtalkyida__1__0_models.UpdateFormDataRequest, headers: dingtalkyida__1__0_models.UpdateFormDataHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateFormDataResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.form_instance_id):
            body['formInstanceId'] = request.form_instance_id
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.use_latest_version):
            body['useLatestVersion'] = request.use_latest_version
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateFormDataResponse(), await self.do_roarequest_async('UpdateFormData', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/instances', 'none', req, runtime))

    def update_instance(self, request: dingtalkyida__1__0_models.UpdateInstanceRequest) -> dingtalkyida__1__0_models.UpdateInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateInstanceHeaders()
        return self.update_instance_with_options(request, headers, runtime)

    async def update_instance_async(self, request: dingtalkyida__1__0_models.UpdateInstanceRequest) -> dingtalkyida__1__0_models.UpdateInstanceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateInstanceHeaders()
        return await self.update_instance_with_options_async(request, headers, runtime)

    def update_instance_with_options(self, request: dingtalkyida__1__0_models.UpdateInstanceRequest, headers: dingtalkyida__1__0_models.UpdateInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateInstanceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateInstanceResponse(), self.do_roarequest('UpdateInstance', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/processes/instances', 'none', req, runtime))

    async def update_instance_with_options_async(self, request: dingtalkyida__1__0_models.UpdateInstanceRequest, headers: dingtalkyida__1__0_models.UpdateInstanceHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateInstanceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.process_instance_id):
            body['processInstanceId'] = request.process_instance_id
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.update_form_data_json):
            body['updateFormDataJson'] = request.update_form_data_json
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateInstanceResponse(), await self.do_roarequest_async('UpdateInstance', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/processes/instances', 'none', req, runtime))

    def update_status(self, request: dingtalkyida__1__0_models.UpdateStatusRequest) -> dingtalkyida__1__0_models.UpdateStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateStatusHeaders()
        return self.update_status_with_options(request, headers, runtime)

    async def update_status_async(self, request: dingtalkyida__1__0_models.UpdateStatusRequest) -> dingtalkyida__1__0_models.UpdateStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpdateStatusHeaders()
        return await self.update_status_with_options_async(request, headers, runtime)

    def update_status_with_options(self, request: dingtalkyida__1__0_models.UpdateStatusRequest, headers: dingtalkyida__1__0_models.UpdateStatusHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateStatusResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.error_lines):
            body['errorLines'] = request.error_lines
        if not UtilClient.is_unset(request.import_sequence):
            body['importSequence'] = request.import_sequence
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateStatusResponse(), self.do_roarequest('UpdateStatus', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/status', 'none', req, runtime))

    async def update_status_with_options_async(self, request: dingtalkyida__1__0_models.UpdateStatusRequest, headers: dingtalkyida__1__0_models.UpdateStatusHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpdateStatusResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.app_type):
            body['appType'] = request.app_type
        if not UtilClient.is_unset(request.error_lines):
            body['errorLines'] = request.error_lines
        if not UtilClient.is_unset(request.import_sequence):
            body['importSequence'] = request.import_sequence
        if not UtilClient.is_unset(request.language):
            body['language'] = request.language
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.system_token):
            body['systemToken'] = request.system_token
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpdateStatusResponse(), await self.do_roarequest_async('UpdateStatus', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/forms/status', 'none', req, runtime))

    def upgrade_tenant_information(self, request: dingtalkyida__1__0_models.UpgradeTenantInformationRequest) -> dingtalkyida__1__0_models.UpgradeTenantInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpgradeTenantInformationHeaders()
        return self.upgrade_tenant_information_with_options(request, headers, runtime)

    async def upgrade_tenant_information_async(self, request: dingtalkyida__1__0_models.UpgradeTenantInformationRequest) -> dingtalkyida__1__0_models.UpgradeTenantInformationResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.UpgradeTenantInformationHeaders()
        return await self.upgrade_tenant_information_with_options_async(request, headers, runtime)

    def upgrade_tenant_information_with_options(self, request: dingtalkyida__1__0_models.UpgradeTenantInformationRequest, headers: dingtalkyida__1__0_models.UpgradeTenantInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpgradeTenantInformationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpgradeTenantInformationResponse(), self.do_roarequest('UpgradeTenantInformation', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/apps/tenantInfos', 'json', req, runtime))

    async def upgrade_tenant_information_with_options_async(self, request: dingtalkyida__1__0_models.UpgradeTenantInformationRequest, headers: dingtalkyida__1__0_models.UpgradeTenantInformationHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.UpgradeTenantInformationResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.access_key):
            body['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.account_number):
            body['accountNumber'] = request.account_number
        if not UtilClient.is_unset(request.caller_union_id):
            body['callerUnionId'] = request.caller_union_id
        if not UtilClient.is_unset(request.commodity_type):
            body['commodityType'] = request.commodity_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, body=OpenApiUtilClient.parse_to_map(body))
        return TeaCore.from_map(dingtalkyida__1__0_models.UpgradeTenantInformationResponse(), await self.do_roarequest_async('UpgradeTenantInformation', 'yida_1.0', 'HTTP', 'PUT', 'AK', f'/v1.0/yida/apps/tenantInfos', 'json', req, runtime))

    def validate_application_authorization_order(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderRequest) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderHeaders()
        return self.validate_application_authorization_order_with_options(instance_id, request, headers, runtime)

    async def validate_application_authorization_order_async(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderRequest) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderHeaders()
        return await self.validate_application_authorization_order_with_options_async(instance_id, request, headers, runtime)

    def validate_application_authorization_order_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderRequest, headers: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            query['callerUnionId'] = request.caller_union_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse(), self.do_roarequest('ValidateApplicationAuthorizationOrder', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applicationOrderUpdateAuthorizations/{instance_id}', 'json', req, runtime))

    async def validate_application_authorization_order_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderRequest, headers: dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_union_id):
            query['callerUnionId'] = request.caller_union_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationAuthorizationOrderResponse(), await self.do_roarequest_async('ValidateApplicationAuthorizationOrder', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applicationOrderUpdateAuthorizations/{instance_id}', 'json', req, runtime))

    def validate_application_authorization_service_order(self, caller_uid: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderRequest) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderHeaders()
        return self.validate_application_authorization_service_order_with_options(caller_uid, request, headers, runtime)

    async def validate_application_authorization_service_order_async(self, caller_uid: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderRequest) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderHeaders()
        return await self.validate_application_authorization_service_order_with_options_async(caller_uid, request, headers, runtime)

    def validate_application_authorization_service_order_with_options(self, caller_uid: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderRequest, headers: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse(), self.do_roarequest('ValidateApplicationAuthorizationServiceOrder', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/appsAuthorizations/freshOrderInfoReviews/{caller_uid}', 'json', req, runtime))

    async def validate_application_authorization_service_order_with_options_async(self, caller_uid: str, request: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderRequest, headers: dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse:
        UtilClient.validate_model(request)
        caller_uid = OpenApiUtilClient.get_encode_param(caller_uid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationAuthorizationServiceOrderResponse(), await self.do_roarequest_async('ValidateApplicationAuthorizationServiceOrder', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/appsAuthorizations/freshOrderInfoReviews/{caller_uid}', 'json', req, runtime))

    def validate_application_service_order_upgrade(self, caller_unionid: str, request: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeRequest) -> dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeHeaders()
        return self.validate_application_service_order_upgrade_with_options(caller_unionid, request, headers, runtime)

    async def validate_application_service_order_upgrade_async(self, caller_unionid: str, request: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeRequest) -> dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeHeaders()
        return await self.validate_application_service_order_upgrade_with_options_async(caller_unionid, request, headers, runtime)

    def validate_application_service_order_upgrade_with_options(self, caller_unionid: str, request: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeRequest, headers: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse:
        UtilClient.validate_model(request)
        caller_unionid = OpenApiUtilClient.get_encode_param(caller_unionid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse(), self.do_roarequest('ValidateApplicationServiceOrderUpgrade', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applications/orderValidations/{caller_unionid}', 'json', req, runtime))

    async def validate_application_service_order_upgrade_with_options_async(self, caller_unionid: str, request: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeRequest, headers: dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse:
        UtilClient.validate_model(request)
        caller_unionid = OpenApiUtilClient.get_encode_param(caller_unionid)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateApplicationServiceOrderUpgradeResponse(), await self.do_roarequest_async('ValidateApplicationServiceOrderUpgrade', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/applications/orderValidations/{caller_unionid}', 'json', req, runtime))

    def validate_order_buy(self, request: dingtalkyida__1__0_models.ValidateOrderBuyRequest) -> dingtalkyida__1__0_models.ValidateOrderBuyResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderBuyHeaders()
        return self.validate_order_buy_with_options(request, headers, runtime)

    async def validate_order_buy_async(self, request: dingtalkyida__1__0_models.ValidateOrderBuyRequest) -> dingtalkyida__1__0_models.ValidateOrderBuyResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderBuyHeaders()
        return await self.validate_order_buy_with_options_async(request, headers, runtime)

    def validate_order_buy_with_options(self, request: dingtalkyida__1__0_models.ValidateOrderBuyRequest, headers: dingtalkyida__1__0_models.ValidateOrderBuyHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderBuyResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderBuyResponse(), self.do_roarequest('ValidateOrderBuy', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/orderBuy/validate', 'json', req, runtime))

    async def validate_order_buy_with_options_async(self, request: dingtalkyida__1__0_models.ValidateOrderBuyRequest, headers: dingtalkyida__1__0_models.ValidateOrderBuyHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderBuyResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderBuyResponse(), await self.do_roarequest_async('ValidateOrderBuy', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/orderBuy/validate', 'json', req, runtime))

    def validate_order_update(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateOrderUpdateRequest) -> dingtalkyida__1__0_models.ValidateOrderUpdateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderUpdateHeaders()
        return self.validate_order_update_with_options(instance_id, request, headers, runtime)

    async def validate_order_update_async(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateOrderUpdateRequest) -> dingtalkyida__1__0_models.ValidateOrderUpdateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderUpdateHeaders()
        return await self.validate_order_update_with_options_async(instance_id, request, headers, runtime)

    def validate_order_update_with_options(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateOrderUpdateRequest, headers: dingtalkyida__1__0_models.ValidateOrderUpdateHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderUpdateResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderUpdateResponse(), self.do_roarequest('ValidateOrderUpdate', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/orders/renewalReviews/{instance_id}', 'json', req, runtime))

    async def validate_order_update_with_options_async(self, instance_id: str, request: dingtalkyida__1__0_models.ValidateOrderUpdateRequest, headers: dingtalkyida__1__0_models.ValidateOrderUpdateHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderUpdateResponse:
        UtilClient.validate_model(request)
        instance_id = OpenApiUtilClient.get_encode_param(instance_id)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderUpdateResponse(), await self.do_roarequest_async('ValidateOrderUpdate', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/orders/renewalReviews/{instance_id}', 'json', req, runtime))

    def validate_order_upgrade(self, request: dingtalkyida__1__0_models.ValidateOrderUpgradeRequest) -> dingtalkyida__1__0_models.ValidateOrderUpgradeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderUpgradeHeaders()
        return self.validate_order_upgrade_with_options(request, headers, runtime)

    async def validate_order_upgrade_async(self, request: dingtalkyida__1__0_models.ValidateOrderUpgradeRequest) -> dingtalkyida__1__0_models.ValidateOrderUpgradeResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkyida__1__0_models.ValidateOrderUpgradeHeaders()
        return await self.validate_order_upgrade_with_options_async(request, headers, runtime)

    def validate_order_upgrade_with_options(self, request: dingtalkyida__1__0_models.ValidateOrderUpgradeRequest, headers: dingtalkyida__1__0_models.ValidateOrderUpgradeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderUpgradeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderUpgradeResponse(), self.do_roarequest('ValidateOrderUpgrade', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/orderUpgrade/validate', 'json', req, runtime))

    async def validate_order_upgrade_with_options_async(self, request: dingtalkyida__1__0_models.ValidateOrderUpgradeRequest, headers: dingtalkyida__1__0_models.ValidateOrderUpgradeHeaders, runtime: util_models.RuntimeOptions) -> dingtalkyida__1__0_models.ValidateOrderUpgradeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.access_key):
            query['accessKey'] = request.access_key
        if not UtilClient.is_unset(request.caller_uid):
            query['callerUid'] = request.caller_uid
        if not UtilClient.is_unset(request.instance_id):
            query['instanceId'] = request.instance_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(headers=real_headers, query=OpenApiUtilClient.query(query))
        return TeaCore.from_map(dingtalkyida__1__0_models.ValidateOrderUpgradeResponse(), await self.do_roarequest_async('ValidateOrderUpgrade', 'yida_1.0', 'HTTP', 'GET', 'AK', f'/v1.0/yida/apps/orderUpgrade/validate', 'json', req, runtime))