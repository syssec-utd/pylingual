from __future__ import annotations
from dataclasses import dataclass
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.response_handler import ResponseHandler
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .....models import unified_role_definition
    from .....models.o_data_errors import o_data_error
    from .inherits_permissions_from import inherits_permissions_from_request_builder
    from .inherits_permissions_from.item import unified_role_definition_item_request_builder

class UnifiedRoleDefinitionItemRequestBuilder:
    """
    Provides operations to manage the roleDefinitions property of the microsoft.graph.rbacApplication entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new UnifiedRoleDefinitionItemRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/roleManagement/entitlementManagement/roleDefinitions/{unifiedRoleDefinition%2Did}{?%24select,%24expand}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def delete(self, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderDeleteRequestConfiguration]=None) -> bytes:
        """
        Delete navigation property roleDefinitions for roleManagement
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_delete_request_information(request_configuration)
        from .....models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        return await self.request_adapter.send_primitive_async(request_info, 'bytes', error_mapping)

    async def get(self, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderGetRequestConfiguration]=None) -> Optional[unified_role_definition.UnifiedRoleDefinition]:
        """
        Resource representing the roles allowed by RBAC providers and the permissions assigned to the roles.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[unified_role_definition.UnifiedRoleDefinition]
        """
        request_info = self.to_get_request_information(request_configuration)
        from .....models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .....models import unified_role_definition
        return await self.request_adapter.send_async(request_info, unified_role_definition.UnifiedRoleDefinition, error_mapping)

    def inherits_permissions_from_by_id(self, id: str) -> UnifiedRoleDefinitionItemRequestBuilder:
        """
        Provides operations to manage the inheritsPermissionsFrom property of the microsoft.graph.unifiedRoleDefinition entity.
        Args:
            id: Unique identifier of the item
        Returns: UnifiedRoleDefinitionItemRequestBuilder
        """
        if id is None:
            raise Exception('id cannot be undefined')
        from .inherits_permissions_from.item import unified_role_definition_item_request_builder
        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params['unifiedRoleDefinition%2Did1'] = id
        return UnifiedRoleDefinitionItemRequestBuilder(self.request_adapter, url_tpl_params)

    async def patch(self, body: Optional[unified_role_definition.UnifiedRoleDefinition]=None, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderPatchRequestConfiguration]=None) -> Optional[unified_role_definition.UnifiedRoleDefinition]:
        """
        Update the navigation property roleDefinitions in roleManagement
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[unified_role_definition.UnifiedRoleDefinition]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_patch_request_information(body, request_configuration)
        from .....models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .....models import unified_role_definition
        return await self.request_adapter.send_async(request_info, unified_role_definition.UnifiedRoleDefinition, error_mapping)

    def to_delete_request_information(self, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderDeleteRequestConfiguration]=None) -> RequestInformation:
        """
        Delete navigation property roleDefinitions for roleManagement
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.DELETE
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        return request_info

    def to_get_request_information(self, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        Resource representing the roles allowed by RBAC providers and the permissions assigned to the roles.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers['Accept'] = ['application/json']
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info

    def to_patch_request_information(self, body: Optional[unified_role_definition.UnifiedRoleDefinition]=None, request_configuration: Optional[UnifiedRoleDefinitionItemRequestBuilderPatchRequestConfiguration]=None) -> RequestInformation:
        """
        Update the navigation property roleDefinitions in roleManagement
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.PATCH
        request_info.headers['Accept'] = ['application/json']
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.set_content_from_parsable(self.request_adapter, 'application/json', body)
        return request_info

    @property
    def inherits_permissions_from(self) -> inherits_permissions_from_request_builder.InheritsPermissionsFromRequestBuilder:
        """
        Provides operations to manage the inheritsPermissionsFrom property of the microsoft.graph.unifiedRoleDefinition entity.
        """
        from .inherits_permissions_from import inherits_permissions_from_request_builder
        return inherits_permissions_from_request_builder.InheritsPermissionsFromRequestBuilder(self.request_adapter, self.path_parameters)

    @dataclass
    class UnifiedRoleDefinitionItemRequestBuilderDeleteRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None

    @dataclass
    class UnifiedRoleDefinitionItemRequestBuilderGetQueryParameters:
        """
        Resource representing the roles allowed by RBAC providers and the permissions assigned to the roles.
        """

        def get_query_parameter(self, original_name: Optional[str]=None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            Args:
                originalName: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise Exception('original_name cannot be undefined')
            if original_name == 'expand':
                return '%24expand'
            if original_name == 'select':
                return '%24select'
            return original_name
        expand: Optional[List[str]] = None
        select: Optional[List[str]] = None

    @dataclass
    class UnifiedRoleDefinitionItemRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[UnifiedRoleDefinitionItemRequestBuilder.UnifiedRoleDefinitionItemRequestBuilderGetQueryParameters] = None

    @dataclass
    class UnifiedRoleDefinitionItemRequestBuilderPatchRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None