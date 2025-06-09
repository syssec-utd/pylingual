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
    from .........models import attachment, attachment_collection_response
    from .........models.o_data_errors import o_data_error
    from .count import count_request_builder
    from .create_upload_session import create_upload_session_request_builder

class AttachmentsRequestBuilder:
    """
    Provides operations to manage the attachments property of the microsoft.graph.event entity.
    """

    def __init__(self, request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]]=None) -> None:
        """
        Instantiates a new AttachmentsRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception('path_parameters cannot be undefined')
        if request_adapter is None:
            raise Exception('request_adapter cannot be undefined')
        self.url_template: str = '{+baseurl}/me/calendars/{calendar%2Did}/events/{event%2Did}/instances/{event%2Did1}/attachments{?%24top,%24skip,%24filter,%24count,%24orderby,%24select,%24expand}'
        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter

    async def get(self, request_configuration: Optional[AttachmentsRequestBuilderGetRequestConfiguration]=None) -> Optional[attachment_collection_response.AttachmentCollectionResponse]:
        """
        Retrieve a list of attachment objects attached to an event.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[attachment_collection_response.AttachmentCollectionResponse]
        """
        request_info = self.to_get_request_information(request_configuration)
        from .........models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .........models import attachment_collection_response
        return await self.request_adapter.send_async(request_info, attachment_collection_response.AttachmentCollectionResponse, error_mapping)

    async def post(self, body: Optional[attachment.Attachment]=None, request_configuration: Optional[AttachmentsRequestBuilderPostRequestConfiguration]=None) -> Optional[attachment.Attachment]:
        """
        Use this API to add an attachment to an existing event. This operation limits the size of the attachment you can add to under 3 MB. If an organizer adds an attachment to a meeting event, the organizer can subsequently update the event to send the attachment and update the event for each attendee as well.
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[attachment.Attachment]
        """
        if body is None:
            raise Exception('body cannot be undefined')
        request_info = self.to_post_request_information(body, request_configuration)
        from .........models.o_data_errors import o_data_error
        error_mapping: Dict[str, ParsableFactory] = {'4XX': o_data_error.ODataError, '5XX': o_data_error.ODataError}
        if not self.request_adapter:
            raise Exception('Http core is null')
        from .........models import attachment
        return await self.request_adapter.send_async(request_info, attachment.Attachment, error_mapping)

    def to_get_request_information(self, request_configuration: Optional[AttachmentsRequestBuilderGetRequestConfiguration]=None) -> RequestInformation:
        """
        Retrieve a list of attachment objects attached to an event.
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

    def to_post_request_information(self, body: Optional[attachment.Attachment]=None, request_configuration: Optional[AttachmentsRequestBuilderPostRequestConfiguration]=None) -> RequestInformation:
        """
        Use this API to add an attachment to an existing event. This operation limits the size of the attachment you can add to under 3 MB. If an organizer adds an attachment to a meeting event, the organizer can subsequently update the event to send the attachment and update the event for each attendee as well.
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

    @property
    def create_upload_session(self) -> create_upload_session_request_builder.CreateUploadSessionRequestBuilder:
        """
        Provides operations to call the createUploadSession method.
        """
        from .create_upload_session import create_upload_session_request_builder
        return create_upload_session_request_builder.CreateUploadSessionRequestBuilder(self.request_adapter, self.path_parameters)

    @dataclass
    class AttachmentsRequestBuilderGetQueryParameters:
        """
        Retrieve a list of attachment objects attached to an event.
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
        select: Optional[List[str]] = None
        skip: Optional[int] = None
        top: Optional[int] = None

    @dataclass
    class AttachmentsRequestBuilderGetRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None
        query_parameters: Optional[AttachmentsRequestBuilder.AttachmentsRequestBuilderGetQueryParameters] = None

    @dataclass
    class AttachmentsRequestBuilderPostRequestConfiguration:
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        headers: Optional[Dict[str, Union[str, List[str]]]] = None
        options: Optional[List[RequestOption]] = None