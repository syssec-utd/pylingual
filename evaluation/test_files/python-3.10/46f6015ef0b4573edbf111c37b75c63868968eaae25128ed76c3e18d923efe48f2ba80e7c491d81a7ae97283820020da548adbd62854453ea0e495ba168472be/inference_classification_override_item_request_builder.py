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
    from ......models import inference_classification_override
    from ......models.o_data_errors import o_data_error

class InferenceClassificationOverrideItemRequestBuilder:
    """
    Provides operations to manage the overrides property of the microsoft.graph.inferenceClassification entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new InferenceClassificationOverrideItemRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/users/{user%2Did}/inferenceClassification/overrides/{inferenceClassificationOverride%2Did}{?%24select}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def delete(self, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderDeleteRequestConfiguration]=None) -> bytes:
        """
        Delete navigation property overrides for users
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_delete_request_information(request_configuration)
        from ......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        return await self.request_adapter.send_primitive_async(request_info, 'bytes', error_mapping)

    async def get(self, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderGetRequestConfiguration]=None) -> Optional[inference_classification_override.InferenceClassificationOverride]:
        """
        A set of overrides for a user to always classify messages from specific senders in certain ways: focused, or other. Read-only. Nullable.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[inference_classification_override.InferenceClassificationOverride]
        """
        request_info = self.to_get_request_information(request_configuration)
        from ......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ......models import inference_classification_override
        return await self.request_adapter.send_async(request_info, inference_classification_override.InferenceClassificationOverride, error_mapping)

    async def patch(self, body: Optional[inference_classification_override.InferenceClassificationOverride]=None, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderPatchRequestConfiguration]=None) -> Optional[inference_classification_override.InferenceClassificationOverride]:
        """
        Update the navigation property overrides in users
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[inference_classification_override.InferenceClassificationOverride]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_patch_request_information(body, request_configuration)
        from ......models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from ......models import inference_classification_override
        return await self.request_adapter.send_async(request_info, inference_classification_override.InferenceClassificationOverride, error_mapping)

    def to_delete_request_information(self, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderDeleteRequestConfiguration]=None) -> RequestInformation:
        """
        Delete navigation property overrides for users
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

    def to_get_request_information(self, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        A set of overrides for a user to always classify messages from specific senders in certain ways: focused, or other. Read-only. Nullable.
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

    def to_patch_request_information(self, body: Optional[inference_classification_override.InferenceClassificationOverride]=None, request_configuration: Optional[InferenceClassificationOverrideItemRequestBuilderPatchRequestConfiguration]=None) -> RequestInformation:
        """
        Update the navigation property overrides in users
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
    class InferenceClassificationOverrideItemRequestBuilderDeleteRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None

    @dataclass
    class InferenceClassificationOverrideItemRequestBuilderGetQueryParameters:
        """
        A set of overrides for a user to always classify messages from specific senders in certain ways: focused, or other. Read-only. Nullable.
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
    class InferenceClassificationOverrideItemRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[InferenceClassificationOverrideItemRequestBuilder.InferenceClassificationOverrideItemRequestBuilderGetQueryParameters] = None

    @dataclass
    class InferenceClassificationOverrideItemRequestBuilderPatchRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None