import logging
from requests.models import Response
from msb_config import Config
from ._dataclasses import ApiRequestData, ApiResponseWrapper
from ._exceptions import ApiRequestExceptions

def make_api_request(request_data: ApiRequestData) -> ApiResponseWrapper:
    from requests import api, ConnectionError
    api_response = Response()
    try:
        request_parameters = request_data.get_request_parameters()
        api_response = api.request(**request_parameters)
    except ConnectionError as ce:
        if Config.is_local_env():
            logging.exception(ce)
        raise ApiRequestExceptions.ResourceNotFound
    except Exception as e:
        if Config.is_local_env():
            logging.exception(e)
        raise ApiRequestExceptions.InternalServerError
    return ApiResponseWrapper(api_response)