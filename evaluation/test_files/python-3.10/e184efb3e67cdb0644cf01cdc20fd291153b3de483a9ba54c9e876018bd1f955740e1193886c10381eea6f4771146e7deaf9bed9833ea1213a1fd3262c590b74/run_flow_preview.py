from typing import Any, Dict
import httpx
from ...client import Client
from ...models.run_flow_preview_json_body import RunFlowPreviewJsonBody
from ...types import Response

def _get_kwargs(*, client: Client, workspace: str, json_body: RunFlowPreviewJsonBody) -> Dict[str, Any]:
    url = '{}/w/{workspace}/jobs/run/preview_flow'.format(client.base_url, workspace=workspace)
    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()
    json_json_body = json_body.to_dict()
    return {'url': url, 'headers': headers, 'cookies': cookies, 'timeout': client.get_timeout(), 'json': json_json_body}

def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(status_code=response.status_code, content=response.content, headers=response.headers, parsed=None)

def sync_detailed(*, client: Client, workspace: str, json_body: RunFlowPreviewJsonBody) -> Response[None]:
    kwargs = _get_kwargs(client=client, workspace=workspace, json_body=json_body)
    response = httpx.post(**kwargs)
    return _build_response(response=response)

async def asyncio_detailed(*, client: Client, workspace: str, json_body: RunFlowPreviewJsonBody) -> Response[None]:
    kwargs = _get_kwargs(client=client, workspace=workspace, json_body=json_body)
    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)
    return _build_response(response=response)