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
    from ........models import single_value_legacy_extended_property, single_value_legacy_extended_property_collection_response
    from ........models.o_data_errors import o_data_error
    from .count import count_request_builder

class SingleValueExtendedPropertiesRequestBuilder:
    """
    Provides operations to manage the singleValueExtendedProperties property of the microsoft.graph.post entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new SingleValueExtendedPropertiesRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/groups/{group%2Did}/threads/{conversationThread%2Did}/posts/{post%2Did}/singleValueExtendedProperties{?%24top,%24skip,%24search,%24filter,%24count,%24orderby,%24select,%24expand}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def get(self, request_configuration: Optional[SingleValueExtendedPropertiesRequestBuilderGetRequestConfiguration]=None) -> Optional[single_value_legacy_extended_property_collection_response.SingleValueLegacyExtendedPropertyCollectionResponse]:
        """
        The collection of single-value extended properties defined for the post. Read-only. Nullable.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[single_value_legacy_extended_property_collection_response.SingleValueLegacyExtendedPropertyCollectionResponse]
        """
        request_info = self.to_get_request_information(request_configuration)
        from ........models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ........models import single_value_legacy_extended_property_collection_response
        return await self.request_adapter.send_async(request_info, single_value_legacy_extended_property_collection_response.SingleValueLegacyExtendedPropertyCollectionResponse, error_mapping)

    async def post(self, body: Optional[single_value_legacy_extended_property.SingleValueLegacyExtendedProperty]=None, request_configuration: Optional[SingleValueExtendedPropertiesRequestBuilderPostRequestConfiguration]=None) -> Optional[single_value_legacy_extended_property.SingleValueLegacyExtendedProperty]:
        """
        Create new navigation property to singleValueExtendedProperties for groups
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[single_value_legacy_extended_property.SingleValueLegacyExtendedProperty]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_post_request_information(body, request_configuration)
        from ........models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ........models import single_value_legacy_extended_property
        return await self.request_adapter.send_async(request_info, single_value_legacy_extended_property.SingleValueLegacyExtendedProperty, error_mapping)

    def to_get_request_information(self, request_configuration: Optional[SingleValueExtendedPropertiesRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        The collection of single-value extended properties defined for the post. Read-only. Nullable.
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

    def to_post_request_information(self, body: Optional[single_value_legacy_extended_property.SingleValueLegacyExtendedProperty]=None, request_configuration: Optional[SingleValueExtendedPropertiesRequestBuilderPostRequestConfiguration]=None) -> RequestInformation:
        """
        Create new navigation property to singleValueExtendedProperties for groups
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
        request_info.http_method = Method.POST
        request_info.headers['Accept'] = ['application/json']
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.set_content_from_parsable(self.request_adapter, 'application/json', body)
        return request_info

    @property
    def count(self) -> count_request_builder.CountRequestBuilder:
        """
        Provides operations to count the resources in the collection.
        """
        from .count import count_request_builder
        return count_request_builder.CountRequestBuilder(self.request_adapter, self.path_parameters)

    @dataclass
    class SingleValueExtendedPropertiesRequestBuilderGetQueryParameters:
        """
        The collection of single-value extended properties defined for the post. Read-only. Nullable.
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
    class SingleValueExtendedPropertiesRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[SingleValueExtendedPropertiesRequestBuilder.SingleValueExtendedPropertiesRequestBuilderGetQueryParameters] = None

    @dataclass
    class SingleValueExtendedPropertiesRequestBuilderPostRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None