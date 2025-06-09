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
    from ....models import directory_object_collection_response
    from ....models.o_data_errors import o_data_error
    from .count import count_request_builder
    from .graph_application import graph_application_request_builder
    from .graph_app_role_assignment import graph_app_role_assignment_request_builder
    from .graph_endpoint import graph_endpoint_request_builder
    from .graph_group import graph_group_request_builder
    from .graph_service_principal import graph_service_principal_request_builder

class OwnedObjectsRequestBuilder:
    """
    Provides operations to manage the ownedObjects property of the microsoft.graph.servicePrincipal entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new OwnedObjectsRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/servicePrincipals/{servicePrincipal%2Did}/ownedObjects{?%24top,%24skip,%24search,%24filter,%24count,%24orderby,%24select,%24expand}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def get(self, request_configuration: Optional[OwnedObjectsRequestBuilderGetRequestConfiguration]=None) -> Optional[directory_object_collection_response.DirectoryObjectCollectionResponse]:
        """
        Directory objects that are owned by this service principal. Read-only. Nullable. Supports $expand and $filter (/$count eq 0, /$count ne 0, /$count eq 1, /$count ne 1).
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[directory_object_collection_response.DirectoryObjectCollectionResponse]
        """
        request_info = self.to_get_request_information(request_configuration)
        from ....models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ....models import directory_object_collection_response
        return await self.request_adapter.send_async(request_info, directory_object_collection_response.DirectoryObjectCollectionResponse, error_mapping)

    def to_get_request_information(self, request_configuration: Optional[OwnedObjectsRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        Directory objects that are owned by this service principal. Read-only. Nullable. Supports $expand and $filter (/$count eq 0, /$count ne 0, /$count eq 1, /$count ne 1).
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

    @property
    def count(self) -> count_request_builder.CountRequestBuilder:
        """
        Provides operations to count the resources in the collection.
        """
        from .count import count_request_builder
        return count_request_builder.CountRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def graph_application(self) -> graph_application_request_builder.GraphApplicationRequestBuilder:
        """
        Casts the previous resource to application.
        """
        from .graph_application import graph_application_request_builder
        return graph_application_request_builder.GraphApplicationRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def graph_app_role_assignment(self) -> graph_app_role_assignment_request_builder.GraphAppRoleAssignmentRequestBuilder:
        """
        Casts the previous resource to appRoleAssignment.
        """
        from .graph_app_role_assignment import graph_app_role_assignment_request_builder
        return graph_app_role_assignment_request_builder.GraphAppRoleAssignmentRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def graph_endpoint(self) -> graph_endpoint_request_builder.GraphEndpointRequestBuilder:
        """
        Casts the previous resource to endpoint.
        """
        from .graph_endpoint import graph_endpoint_request_builder
        return graph_endpoint_request_builder.GraphEndpointRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def graph_group(self) -> graph_group_request_builder.GraphGroupRequestBuilder:
        """
        Casts the previous resource to group.
        """
        from .graph_group import graph_group_request_builder
        return graph_group_request_builder.GraphGroupRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def graph_service_principal(self) -> graph_service_principal_request_builder.GraphServicePrincipalRequestBuilder:
        """
        Casts the previous resource to servicePrincipal.
        """
        from .graph_service_principal import graph_service_principal_request_builder
        return graph_service_principal_request_builder.GraphServicePrincipalRequestBuilder(self.request_adapter, self.path_parameters)

    @dataclass
    class OwnedObjectsRequestBuilderGetQueryParameters:
        """
        Directory objects that are owned by this service principal. Read-only. Nullable. Supports $expand and $filter (/$count eq 0, /$count ne 0, /$count eq 1, /$count ne 1).
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
            if original_name == 'count':
                return '%24count'
            if original_name == 'expand':
                return '%24expand'
            if original_name == 'filter':
                return '%24filter'
            if original_name == 'orderby':
                return '%24orderby'
            if original_name == 'search':
                return '%24search'
            if original_name == 'select':
                return '%24select'
            if original_name == 'skip':
                return '%24skip'
            if original_name == 'top':
                return '%24top'
            return original_name
        count: Optional[bool] = None
        expand: Optional[List[str]] = None
        filter: Optional[str] = None
        orderby: Optional[List[str]] = None
        search: Optional[str] = None
        select: Optional[List[str]] = None
        skip: Optional[int] = None
        top: Optional[int] = None

    @dataclass
    class OwnedObjectsRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[OwnedObjectsRequestBuilder.OwnedObjectsRequestBuilderGetQueryParameters] = None