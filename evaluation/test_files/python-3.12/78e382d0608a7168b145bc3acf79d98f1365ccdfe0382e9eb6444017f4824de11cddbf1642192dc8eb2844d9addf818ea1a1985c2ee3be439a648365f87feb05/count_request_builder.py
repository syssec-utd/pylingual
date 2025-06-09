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
    from .............models.o_data_errors import o_data_error

class CountRequestBuilder:
    """
    Provides operations to count the resources in the collection.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new CountRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/sites/{site%2Did}/termStores/{store%2Did}/groups/{group%2Did}/sets/{set%2Did}/terms/{term%2Did}/children/$count{?%24search,%24filter}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def get(self, request_configuration: Optional[CountRequestBuilderGetRequestConfiguration]=None) -> Optional[int]:
        """
        Get the number of the resource
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[int]
        """
        request_info = self.to_get_request_information(request_configuration)
        from .............models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        return await self.request_adapter.send_primitive_async(request_info, 'int', error_mapping)

    def to_get_request_information(self, request_configuration: Optional[CountRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        Get the number of the resource
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers['Accept'] = ['text/plain']
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info

    @dataclass
    class CountRequestBuilderGetQueryParameters:
        """
        Get the number of the resource
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
            if original_name == 'filter':
                return '%24filter'
            if original_name == 'search':
                return '%24search'
            return original_name
        filter: Optional[str] = None
        search: Optional[str] = None

    @dataclass
    class CountRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[CountRequestBuilder.CountRequestBuilderGetQueryParameters] = None