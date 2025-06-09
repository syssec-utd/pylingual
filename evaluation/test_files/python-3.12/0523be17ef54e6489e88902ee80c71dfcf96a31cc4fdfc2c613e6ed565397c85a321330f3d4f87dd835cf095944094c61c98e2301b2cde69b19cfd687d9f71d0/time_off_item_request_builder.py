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
    from .......models import time_off
    from .......models.o_data_errors import o_data_error

class TimeOffItemRequestBuilder:
    """
    Provides operations to manage the timesOff property of the microsoft.graph.schedule entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new TimeOffItemRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/me/joinedTeams/{team%2Did}/schedule/timesOff/{timeOff%2Did}{?%24select}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def delete(self, request_configuration: Optional[TimeOffItemRequestBuilderDeleteRequestConfiguration]=None) -> bytes:
        """
        Delete navigation property timesOff for me
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_delete_request_information(request_configuration)
        from .......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        return await self.request_adapter.send_primitive_async(request_info, 'bytes', error_mapping)

    async def get(self, request_configuration: Optional[TimeOffItemRequestBuilderGetRequestConfiguration]=None) -> Optional[time_off.TimeOff]:
        """
        The instances of times off in the schedule.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[time_off.TimeOff]
        """
        request_info = self.to_get_request_information(request_configuration)
        from .......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .......models import time_off
        return await self.request_adapter.send_async(request_info, time_off.TimeOff, error_mapping)

    async def patch(self, body: Optional[time_off.TimeOff]=None, request_configuration: Optional[TimeOffItemRequestBuilderPatchRequestConfiguration]=None) -> Optional[time_off.TimeOff]:
        """
        Update the navigation property timesOff in me
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[time_off.TimeOff]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_patch_request_information(body, request_configuration)
        from .......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .......models import time_off
        return await self.request_adapter.send_async(request_info, time_off.TimeOff, error_mapping)

    def to_delete_request_information(self, request_configuration: Optional[TimeOffItemRequestBuilderDeleteRequestConfiguration]=None) -> RequestInformation:
        """
        Delete navigation property timesOff for me
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

    def to_get_request_information(self, request_configuration: Optional[TimeOffItemRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        The instances of times off in the schedule.
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

    def to_patch_request_information(self, body: Optional[time_off.TimeOff]=None, request_configuration: Optional[TimeOffItemRequestBuilderPatchRequestConfiguration]=None) -> RequestInformation:
        """
        Update the navigation property timesOff in me
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

    @dataclass
    class TimeOffItemRequestBuilderDeleteRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None

    @dataclass
    class TimeOffItemRequestBuilderGetQueryParameters:
        """
        The instances of times off in the schedule.
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
            if original_name == 'select':
                return '%24select'
            return original_name
        select: Optional[List[str]] = None

    @dataclass
    class TimeOffItemRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[TimeOffItemRequestBuilder.TimeOffItemRequestBuilderGetQueryParameters] = None

    @dataclass
    class TimeOffItemRequestBuilderPatchRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None