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
    from ......models import user
    from ......models.o_data_errors import o_data_error

class GraphUserRequestBuilder:
    """
    Casts the previous resource to user.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new GraphUserRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/contacts/{orgContact%2Did}/directReports/{directoryObject%2Did}/graph.user{?%24select,%24expand}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def get(self, request_configuration: Optional[GraphUserRequestBuilderGetRequestConfiguration]=None) -> Optional[user.User]:
        """
        Get the item of type microsoft.graph.directoryObject as microsoft.graph.user
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[user.User]
        """
        request_info = self.to_get_request_information(request_configuration)
        from ......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ......models import user
        return await self.request_adapter.send_async(request_info, user.User, error_mapping)

    def to_get_request_information(self, request_configuration: Optional[GraphUserRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        Get the item of type microsoft.graph.directoryObject as microsoft.graph.user
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

    @dataclass
    class GraphUserRequestBuilderGetQueryParameters:
        """
        Get the item of type microsoft.graph.directoryObject as microsoft.graph.user
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
    class GraphUserRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[GraphUserRequestBuilder.GraphUserRequestBuilderGetQueryParameters] = None