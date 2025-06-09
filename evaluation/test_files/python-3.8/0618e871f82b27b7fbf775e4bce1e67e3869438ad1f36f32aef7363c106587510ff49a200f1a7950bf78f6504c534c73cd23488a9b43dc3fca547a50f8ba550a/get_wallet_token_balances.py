import json
from .api_instance import get_api_instance
import typing
from openapi_evm_api.paths.address_erc20.get import RequestQueryParams, RequestPathParams

def get_wallet_token_balances(api_key: str, params: typing.Union[RequestQueryParams, RequestPathParams]):
    api_instance = get_api_instance(api_key)
    query_params = {k: v for (k, v) in params.items() if k in RequestQueryParams.__annotations__.keys()}
    path_params = {k: v for (k, v) in params.items() if k in RequestPathParams.__annotations__.keys()}
    api_response = api_instance.get_wallet_token_balances(query_params=query_params, path_params=path_params, accept_content_types='application/json; charset=utf-8', skip_deserialization=True)
    return json.loads(api_response.response.data)