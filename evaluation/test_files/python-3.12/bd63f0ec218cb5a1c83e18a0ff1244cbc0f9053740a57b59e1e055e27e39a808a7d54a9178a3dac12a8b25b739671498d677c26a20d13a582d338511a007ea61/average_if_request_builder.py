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
    from . import average_if_post_request_body
    from ........models import workbook_function_result
    from ........models.o_data_errors import o_data_error

class AverageIfRequestBuilder:
    """
    Provides operations to call the averageIf method.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new AverageIfRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/drives/{drive%2Did}/items/{driveItem%2Did}/workbook/functions/averageIf'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def post(self, body: Optional[average_if_post_request_body.AverageIfPostRequestBody]=None, request_configuration: Optional[AverageIfRequestBuilderPostRequestConfiguration]=None) -> Optional[workbook_function_result.WorkbookFunctionResult]:
        """
        Invoke action averageIf
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[workbook_function_result.WorkbookFunctionResult]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_post_request_information(body, request_configuration)
        from ........models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ........models import workbook_function_result
        return await self.request_adapter.send_async(request_info, workbook_function_result.WorkbookFunctionResult, error_mapping)

    def to_post_request_information(self, body: Optional[average_if_post_request_body.AverageIfPostRequestBody]=None, request_configuration: Optional[AverageIfRequestBuilderPostRequestConfiguration]=None) -> RequestInformation:
        """
        Invoke action averageIf
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

    @dataclass
    class AverageIfRequestBuilderPostRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None