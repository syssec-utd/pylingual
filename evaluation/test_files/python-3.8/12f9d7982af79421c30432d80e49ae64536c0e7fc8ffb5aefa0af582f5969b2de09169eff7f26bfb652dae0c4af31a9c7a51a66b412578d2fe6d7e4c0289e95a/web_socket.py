from gs2.core import *
from .request import *
from .result import *

class Gs2VersionWebSocketClient(web_socket.AbstractGs2WebSocketClient):

    def _describe_namespaces(self, request: DescribeNamespacesRequest, callback: Callable[[AsyncResult[DescribeNamespacesResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='describeNamespaces', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.page_token is not None:
            body['pageToken'] = request.page_token
        if request.limit is not None:
            body['limit'] = request.limit
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DescribeNamespacesResult, callback=callback, body=body))

    def describe_namespaces(self, request: DescribeNamespacesRequest) -> DescribeNamespacesResult:
        async_result = []
        with timeout(30):
            self._describe_namespaces(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def describe_namespaces_async(self, request: DescribeNamespacesRequest) -> DescribeNamespacesResult:
        async_result = []
        self._describe_namespaces(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _create_namespace(self, request: CreateNamespaceRequest, callback: Callable[[AsyncResult[CreateNamespaceResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='createNamespace', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.name is not None:
            body['name'] = request.name
        if request.description is not None:
            body['description'] = request.description
        if request.assume_user_id is not None:
            body['assumeUserId'] = request.assume_user_id
        if request.accept_version_script is not None:
            body['acceptVersionScript'] = request.accept_version_script.to_dict()
        if request.check_version_trigger_script_id is not None:
            body['checkVersionTriggerScriptId'] = request.check_version_trigger_script_id
        if request.log_setting is not None:
            body['logSetting'] = request.log_setting.to_dict()
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=CreateNamespaceResult, callback=callback, body=body))

    def create_namespace(self, request: CreateNamespaceRequest) -> CreateNamespaceResult:
        async_result = []
        with timeout(30):
            self._create_namespace(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def create_namespace_async(self, request: CreateNamespaceRequest) -> CreateNamespaceResult:
        async_result = []
        self._create_namespace(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_namespace_status(self, request: GetNamespaceStatusRequest, callback: Callable[[AsyncResult[GetNamespaceStatusResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='getNamespaceStatus', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetNamespaceStatusResult, callback=callback, body=body))

    def get_namespace_status(self, request: GetNamespaceStatusRequest) -> GetNamespaceStatusResult:
        async_result = []
        with timeout(30):
            self._get_namespace_status(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_namespace_status_async(self, request: GetNamespaceStatusRequest) -> GetNamespaceStatusResult:
        async_result = []
        self._get_namespace_status(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_namespace(self, request: GetNamespaceRequest, callback: Callable[[AsyncResult[GetNamespaceResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='getNamespace', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetNamespaceResult, callback=callback, body=body))

    def get_namespace(self, request: GetNamespaceRequest) -> GetNamespaceResult:
        async_result = []
        with timeout(30):
            self._get_namespace(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_namespace_async(self, request: GetNamespaceRequest) -> GetNamespaceResult:
        async_result = []
        self._get_namespace(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _update_namespace(self, request: UpdateNamespaceRequest, callback: Callable[[AsyncResult[UpdateNamespaceResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='updateNamespace', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.description is not None:
            body['description'] = request.description
        if request.assume_user_id is not None:
            body['assumeUserId'] = request.assume_user_id
        if request.accept_version_script is not None:
            body['acceptVersionScript'] = request.accept_version_script.to_dict()
        if request.check_version_trigger_script_id is not None:
            body['checkVersionTriggerScriptId'] = request.check_version_trigger_script_id
        if request.log_setting is not None:
            body['logSetting'] = request.log_setting.to_dict()
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=UpdateNamespaceResult, callback=callback, body=body))

    def update_namespace(self, request: UpdateNamespaceRequest) -> UpdateNamespaceResult:
        async_result = []
        with timeout(30):
            self._update_namespace(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def update_namespace_async(self, request: UpdateNamespaceRequest) -> UpdateNamespaceResult:
        async_result = []
        self._update_namespace(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _delete_namespace(self, request: DeleteNamespaceRequest, callback: Callable[[AsyncResult[DeleteNamespaceResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='namespace', function='deleteNamespace', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DeleteNamespaceResult, callback=callback, body=body))

    def delete_namespace(self, request: DeleteNamespaceRequest) -> DeleteNamespaceResult:
        async_result = []
        with timeout(30):
            self._delete_namespace(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def delete_namespace_async(self, request: DeleteNamespaceRequest) -> DeleteNamespaceResult:
        async_result = []
        self._delete_namespace(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _describe_version_model_masters(self, request: DescribeVersionModelMastersRequest, callback: Callable[[AsyncResult[DescribeVersionModelMastersResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModelMaster', function='describeVersionModelMasters', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.page_token is not None:
            body['pageToken'] = request.page_token
        if request.limit is not None:
            body['limit'] = request.limit
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DescribeVersionModelMastersResult, callback=callback, body=body))

    def describe_version_model_masters(self, request: DescribeVersionModelMastersRequest) -> DescribeVersionModelMastersResult:
        async_result = []
        with timeout(30):
            self._describe_version_model_masters(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def describe_version_model_masters_async(self, request: DescribeVersionModelMastersRequest) -> DescribeVersionModelMastersResult:
        async_result = []
        self._describe_version_model_masters(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _create_version_model_master(self, request: CreateVersionModelMasterRequest, callback: Callable[[AsyncResult[CreateVersionModelMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModelMaster', function='createVersionModelMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.name is not None:
            body['name'] = request.name
        if request.description is not None:
            body['description'] = request.description
        if request.metadata is not None:
            body['metadata'] = request.metadata
        if request.warning_version is not None:
            body['warningVersion'] = request.warning_version.to_dict()
        if request.error_version is not None:
            body['errorVersion'] = request.error_version.to_dict()
        if request.scope is not None:
            body['scope'] = request.scope
        if request.current_version is not None:
            body['currentVersion'] = request.current_version.to_dict()
        if request.need_signature is not None:
            body['needSignature'] = request.need_signature
        if request.signature_key_id is not None:
            body['signatureKeyId'] = request.signature_key_id
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=CreateVersionModelMasterResult, callback=callback, body=body))

    def create_version_model_master(self, request: CreateVersionModelMasterRequest) -> CreateVersionModelMasterResult:
        async_result = []
        with timeout(30):
            self._create_version_model_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def create_version_model_master_async(self, request: CreateVersionModelMasterRequest) -> CreateVersionModelMasterResult:
        async_result = []
        self._create_version_model_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_version_model_master(self, request: GetVersionModelMasterRequest, callback: Callable[[AsyncResult[GetVersionModelMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModelMaster', function='getVersionModelMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetVersionModelMasterResult, callback=callback, body=body))

    def get_version_model_master(self, request: GetVersionModelMasterRequest) -> GetVersionModelMasterResult:
        async_result = []
        with timeout(30):
            self._get_version_model_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_version_model_master_async(self, request: GetVersionModelMasterRequest) -> GetVersionModelMasterResult:
        async_result = []
        self._get_version_model_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _update_version_model_master(self, request: UpdateVersionModelMasterRequest, callback: Callable[[AsyncResult[UpdateVersionModelMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModelMaster', function='updateVersionModelMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.description is not None:
            body['description'] = request.description
        if request.metadata is not None:
            body['metadata'] = request.metadata
        if request.warning_version is not None:
            body['warningVersion'] = request.warning_version.to_dict()
        if request.error_version is not None:
            body['errorVersion'] = request.error_version.to_dict()
        if request.scope is not None:
            body['scope'] = request.scope
        if request.current_version is not None:
            body['currentVersion'] = request.current_version.to_dict()
        if request.need_signature is not None:
            body['needSignature'] = request.need_signature
        if request.signature_key_id is not None:
            body['signatureKeyId'] = request.signature_key_id
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=UpdateVersionModelMasterResult, callback=callback, body=body))

    def update_version_model_master(self, request: UpdateVersionModelMasterRequest) -> UpdateVersionModelMasterResult:
        async_result = []
        with timeout(30):
            self._update_version_model_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def update_version_model_master_async(self, request: UpdateVersionModelMasterRequest) -> UpdateVersionModelMasterResult:
        async_result = []
        self._update_version_model_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _delete_version_model_master(self, request: DeleteVersionModelMasterRequest, callback: Callable[[AsyncResult[DeleteVersionModelMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModelMaster', function='deleteVersionModelMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DeleteVersionModelMasterResult, callback=callback, body=body))

    def delete_version_model_master(self, request: DeleteVersionModelMasterRequest) -> DeleteVersionModelMasterResult:
        async_result = []
        with timeout(30):
            self._delete_version_model_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def delete_version_model_master_async(self, request: DeleteVersionModelMasterRequest) -> DeleteVersionModelMasterResult:
        async_result = []
        self._delete_version_model_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _describe_version_models(self, request: DescribeVersionModelsRequest, callback: Callable[[AsyncResult[DescribeVersionModelsResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModel', function='describeVersionModels', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DescribeVersionModelsResult, callback=callback, body=body))

    def describe_version_models(self, request: DescribeVersionModelsRequest) -> DescribeVersionModelsResult:
        async_result = []
        with timeout(30):
            self._describe_version_models(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def describe_version_models_async(self, request: DescribeVersionModelsRequest) -> DescribeVersionModelsResult:
        async_result = []
        self._describe_version_models(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_version_model(self, request: GetVersionModelRequest, callback: Callable[[AsyncResult[GetVersionModelResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='versionModel', function='getVersionModel', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetVersionModelResult, callback=callback, body=body))

    def get_version_model(self, request: GetVersionModelRequest) -> GetVersionModelResult:
        async_result = []
        with timeout(30):
            self._get_version_model(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_version_model_async(self, request: GetVersionModelRequest) -> GetVersionModelResult:
        async_result = []
        self._get_version_model(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _describe_accept_versions(self, request: DescribeAcceptVersionsRequest, callback: Callable[[AsyncResult[DescribeAcceptVersionsResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='describeAcceptVersions', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.access_token is not None:
            body['accessToken'] = request.access_token
        if request.page_token is not None:
            body['pageToken'] = request.page_token
        if request.limit is not None:
            body['limit'] = request.limit
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.access_token:
            body['xGs2AccessToken'] = request.access_token
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DescribeAcceptVersionsResult, callback=callback, body=body))

    def describe_accept_versions(self, request: DescribeAcceptVersionsRequest) -> DescribeAcceptVersionsResult:
        async_result = []
        with timeout(30):
            self._describe_accept_versions(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def describe_accept_versions_async(self, request: DescribeAcceptVersionsRequest) -> DescribeAcceptVersionsResult:
        async_result = []
        self._describe_accept_versions(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _describe_accept_versions_by_user_id(self, request: DescribeAcceptVersionsByUserIdRequest, callback: Callable[[AsyncResult[DescribeAcceptVersionsByUserIdResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='describeAcceptVersionsByUserId', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.user_id is not None:
            body['userId'] = request.user_id
        if request.page_token is not None:
            body['pageToken'] = request.page_token
        if request.limit is not None:
            body['limit'] = request.limit
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DescribeAcceptVersionsByUserIdResult, callback=callback, body=body))

    def describe_accept_versions_by_user_id(self, request: DescribeAcceptVersionsByUserIdRequest) -> DescribeAcceptVersionsByUserIdResult:
        async_result = []
        with timeout(30):
            self._describe_accept_versions_by_user_id(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def describe_accept_versions_by_user_id_async(self, request: DescribeAcceptVersionsByUserIdRequest) -> DescribeAcceptVersionsByUserIdResult:
        async_result = []
        self._describe_accept_versions_by_user_id(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _accept(self, request: AcceptRequest, callback: Callable[[AsyncResult[AcceptResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='accept', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.access_token is not None:
            body['accessToken'] = request.access_token
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.access_token:
            body['xGs2AccessToken'] = request.access_token
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=AcceptResult, callback=callback, body=body))

    def accept(self, request: AcceptRequest) -> AcceptResult:
        async_result = []
        with timeout(30):
            self._accept(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def accept_async(self, request: AcceptRequest) -> AcceptResult:
        async_result = []
        self._accept(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _accept_by_user_id(self, request: AcceptByUserIdRequest, callback: Callable[[AsyncResult[AcceptByUserIdResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='acceptByUserId', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.user_id is not None:
            body['userId'] = request.user_id
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=AcceptByUserIdResult, callback=callback, body=body))

    def accept_by_user_id(self, request: AcceptByUserIdRequest) -> AcceptByUserIdResult:
        async_result = []
        with timeout(30):
            self._accept_by_user_id(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def accept_by_user_id_async(self, request: AcceptByUserIdRequest) -> AcceptByUserIdResult:
        async_result = []
        self._accept_by_user_id(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_accept_version(self, request: GetAcceptVersionRequest, callback: Callable[[AsyncResult[GetAcceptVersionResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='getAcceptVersion', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.access_token is not None:
            body['accessToken'] = request.access_token
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.access_token:
            body['xGs2AccessToken'] = request.access_token
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetAcceptVersionResult, callback=callback, body=body))

    def get_accept_version(self, request: GetAcceptVersionRequest) -> GetAcceptVersionResult:
        async_result = []
        with timeout(30):
            self._get_accept_version(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_accept_version_async(self, request: GetAcceptVersionRequest) -> GetAcceptVersionResult:
        async_result = []
        self._get_accept_version(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_accept_version_by_user_id(self, request: GetAcceptVersionByUserIdRequest, callback: Callable[[AsyncResult[GetAcceptVersionByUserIdResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='getAcceptVersionByUserId', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.user_id is not None:
            body['userId'] = request.user_id
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetAcceptVersionByUserIdResult, callback=callback, body=body))

    def get_accept_version_by_user_id(self, request: GetAcceptVersionByUserIdRequest) -> GetAcceptVersionByUserIdResult:
        async_result = []
        with timeout(30):
            self._get_accept_version_by_user_id(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_accept_version_by_user_id_async(self, request: GetAcceptVersionByUserIdRequest) -> GetAcceptVersionByUserIdResult:
        async_result = []
        self._get_accept_version_by_user_id(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _delete_accept_version(self, request: DeleteAcceptVersionRequest, callback: Callable[[AsyncResult[DeleteAcceptVersionResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='deleteAcceptVersion', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.access_token is not None:
            body['accessToken'] = request.access_token
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.access_token:
            body['xGs2AccessToken'] = request.access_token
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DeleteAcceptVersionResult, callback=callback, body=body))

    def delete_accept_version(self, request: DeleteAcceptVersionRequest) -> DeleteAcceptVersionResult:
        async_result = []
        with timeout(30):
            self._delete_accept_version(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def delete_accept_version_async(self, request: DeleteAcceptVersionRequest) -> DeleteAcceptVersionResult:
        async_result = []
        self._delete_accept_version(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _delete_accept_version_by_user_id(self, request: DeleteAcceptVersionByUserIdRequest, callback: Callable[[AsyncResult[DeleteAcceptVersionByUserIdResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='acceptVersion', function='deleteAcceptVersionByUserId', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.user_id is not None:
            body['userId'] = request.user_id
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=DeleteAcceptVersionByUserIdResult, callback=callback, body=body))

    def delete_accept_version_by_user_id(self, request: DeleteAcceptVersionByUserIdRequest) -> DeleteAcceptVersionByUserIdResult:
        async_result = []
        with timeout(30):
            self._delete_accept_version_by_user_id(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def delete_accept_version_by_user_id_async(self, request: DeleteAcceptVersionByUserIdRequest) -> DeleteAcceptVersionByUserIdResult:
        async_result = []
        self._delete_accept_version_by_user_id(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _check_version(self, request: CheckVersionRequest, callback: Callable[[AsyncResult[CheckVersionResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='checker', function='checkVersion', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.access_token is not None:
            body['accessToken'] = request.access_token
        if request.target_versions is not None:
            body['targetVersions'] = [item.to_dict() for item in request.target_versions]
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.access_token:
            body['xGs2AccessToken'] = request.access_token
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=CheckVersionResult, callback=callback, body=body))

    def check_version(self, request: CheckVersionRequest) -> CheckVersionResult:
        async_result = []
        with timeout(30):
            self._check_version(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def check_version_async(self, request: CheckVersionRequest) -> CheckVersionResult:
        async_result = []
        self._check_version(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _check_version_by_user_id(self, request: CheckVersionByUserIdRequest, callback: Callable[[AsyncResult[CheckVersionByUserIdResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='checker', function='checkVersionByUserId', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.user_id is not None:
            body['userId'] = request.user_id
        if request.target_versions is not None:
            body['targetVersions'] = [item.to_dict() for item in request.target_versions]
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        if request.duplication_avoider:
            body['xGs2DuplicationAvoider'] = request.duplication_avoider
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=CheckVersionByUserIdResult, callback=callback, body=body))

    def check_version_by_user_id(self, request: CheckVersionByUserIdRequest) -> CheckVersionByUserIdResult:
        async_result = []
        with timeout(30):
            self._check_version_by_user_id(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def check_version_by_user_id_async(self, request: CheckVersionByUserIdRequest) -> CheckVersionByUserIdResult:
        async_result = []
        self._check_version_by_user_id(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _calculate_signature(self, request: CalculateSignatureRequest, callback: Callable[[AsyncResult[CalculateSignatureResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='checker', function='calculateSignature', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.version_name is not None:
            body['versionName'] = request.version_name
        if request.version is not None:
            body['version'] = request.version.to_dict()
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=CalculateSignatureResult, callback=callback, body=body))

    def calculate_signature(self, request: CalculateSignatureRequest) -> CalculateSignatureResult:
        async_result = []
        with timeout(30):
            self._calculate_signature(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def calculate_signature_async(self, request: CalculateSignatureRequest) -> CalculateSignatureResult:
        async_result = []
        self._calculate_signature(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _export_master(self, request: ExportMasterRequest, callback: Callable[[AsyncResult[ExportMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='currentVersionMaster', function='exportMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=ExportMasterResult, callback=callback, body=body))

    def export_master(self, request: ExportMasterRequest) -> ExportMasterResult:
        async_result = []
        with timeout(30):
            self._export_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def export_master_async(self, request: ExportMasterRequest) -> ExportMasterResult:
        async_result = []
        self._export_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _get_current_version_master(self, request: GetCurrentVersionMasterRequest, callback: Callable[[AsyncResult[GetCurrentVersionMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='currentVersionMaster', function='getCurrentVersionMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=GetCurrentVersionMasterResult, callback=callback, body=body))

    def get_current_version_master(self, request: GetCurrentVersionMasterRequest) -> GetCurrentVersionMasterResult:
        async_result = []
        with timeout(30):
            self._get_current_version_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def get_current_version_master_async(self, request: GetCurrentVersionMasterRequest) -> GetCurrentVersionMasterResult:
        async_result = []
        self._get_current_version_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _update_current_version_master(self, request: UpdateCurrentVersionMasterRequest, callback: Callable[[AsyncResult[UpdateCurrentVersionMasterResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='currentVersionMaster', function='updateCurrentVersionMaster', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.settings is not None:
            body['settings'] = request.settings
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=UpdateCurrentVersionMasterResult, callback=callback, body=body))

    def update_current_version_master(self, request: UpdateCurrentVersionMasterRequest) -> UpdateCurrentVersionMasterResult:
        async_result = []
        with timeout(30):
            self._update_current_version_master(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def update_current_version_master_async(self, request: UpdateCurrentVersionMasterRequest) -> UpdateCurrentVersionMasterResult:
        async_result = []
        self._update_current_version_master(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    def _update_current_version_master_from_git_hub(self, request: UpdateCurrentVersionMasterFromGitHubRequest, callback: Callable[[AsyncResult[UpdateCurrentVersionMasterFromGitHubResult]], None]):
        import uuid
        request_id = str(uuid.uuid4())
        body = self._create_metadata(service='version', component='currentVersionMaster', function='updateCurrentVersionMasterFromGitHub', request_id=request_id)
        if request.context_stack:
            body['contextStack'] = str(request.context_stack)
        if request.namespace_name is not None:
            body['namespaceName'] = request.namespace_name
        if request.checkout_setting is not None:
            body['checkoutSetting'] = request.checkout_setting.to_dict()
        if request.request_id:
            body['xGs2RequestId'] = request.request_id
        self.session.send(web_socket.NetworkJob(request_id=request_id, result_type=UpdateCurrentVersionMasterFromGitHubResult, callback=callback, body=body))

    def update_current_version_master_from_git_hub(self, request: UpdateCurrentVersionMasterFromGitHubRequest) -> UpdateCurrentVersionMasterFromGitHubResult:
        async_result = []
        with timeout(30):
            self._update_current_version_master_from_git_hub(request, lambda result: async_result.append(result))
        with timeout(30):
            while not async_result:
                time.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result

    async def update_current_version_master_from_git_hub_async(self, request: UpdateCurrentVersionMasterFromGitHubRequest) -> UpdateCurrentVersionMasterFromGitHubResult:
        async_result = []
        self._update_current_version_master_from_git_hub(request, lambda result: async_result.append(result))
        import asyncio
        with timeout(30):
            while not async_result:
                await asyncio.sleep(0.01)
        if async_result[0].error:
            raise async_result[0].error
        return async_result[0].result