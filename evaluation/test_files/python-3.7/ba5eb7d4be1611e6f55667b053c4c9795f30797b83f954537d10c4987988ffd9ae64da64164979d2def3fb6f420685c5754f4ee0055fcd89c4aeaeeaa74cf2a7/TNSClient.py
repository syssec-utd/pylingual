import asyncio
import json
import sys
import traceback
from functools import partial
from typing import Dict
import aiohttp
import backoff
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientResponseError, ServerDisconnectedError
from .TNSToken import TNSToken

async def tns_post(session: ClientSession, semaphore: asyncio.Semaphore, method: str, token: TNSToken, data: dict, max_retries: int=10) -> dict:
    """
    post to TNS, asynchronously
    """
    async with semaphore:
        for _ in range(max_retries):
            with aiohttp.MultipartWriter('form-data') as mpwriter:
                p: aiohttp.Payload = aiohttp.StringPayload(token.api_key)
                p.set_content_disposition('form-data', name='api_key')
                mpwriter.append(p)
                p = aiohttp.JsonPayload(data)
                p.set_content_disposition('form-data', name='data')
                mpwriter.append(p)
                resp = await session.post('https://www.wis-tns.org/api/' + method, data=mpwriter)
            if resp.status == 429:
                wait = max((int(resp.headers.get('x-cone-rate-limit-reset', 0)) if method.endswith('search') else 0, int(resp.headers.get('x-rate-limit-reset', 0)), 1))
                await asyncio.sleep(wait)
                continue
            else:
                break
        resp.raise_for_status()
        return await resp.json()

class TNSClient:

    def __init__(self, token: TNSToken, timeout, maxParallelRequests, logger):
        self.token = token
        self.maxParallelRequests = maxParallelRequests
        self.logger = logger
        self.tns_post = backoff.on_exception(backoff.expo, (TimeoutError, ClientResponseError, ClientConnectorError, ClientConnectionError, ServerDisconnectedError), logger=None, giveup=self.is_permanent_error, on_giveup=self._on_giveup, on_backoff=self._on_backoff, max_time=timeout)(tns_post)

    def _on_backoff(self, details):
        (exc_typ, exc, _) = sys.exc_info()
        if exc is not None:
            exc = traceback.format_exception_only(exc_typ, exc)[-1].rstrip('\n')
        self.logger.warn('backoff', extra={'exc': exc, 'wait': details['wait'], 'tries': details['tries']})

    def _on_giveup(self, details):
        (exc_typ, exc, _) = sys.exc_info()
        if exc is not None:
            exc = traceback.format_exception_only(exc_typ, exc)[-1].rstrip('\n')
        self.logger.warn('gave up', extra={'exc': exc, 'tries': details['tries']})

    @staticmethod
    def is_permanent_error(exc):
        if isinstance(exc, ClientResponseError):
            return exc.code not in {500, 429}
        else:
            return False

    async def search(self, exclude=set(), **params):
        semaphore = asyncio.Semaphore(self.maxParallelRequests)
        async with ClientSession(headers={'User-Agent': 'tns_marker' + json.dumps({'tns_id': self.token.id, 'name': self.token.name, 'type': 'bot'})}) as session:
            search = partial(self.tns_post, session, semaphore, 'get/search', self.token)
            get = partial(self.tns_post, session, semaphore, 'get/object', self.token)
            response = await search(params)
            names = [item['objname'] for item in response['data']['reply']]
            tasks = [get({'objname': name}) for name in names if not (exclude and name in exclude)]
            self.logger.info('TNS search', extra={'params': params, 'results': len(names)})
            for fut in asyncio.as_completed(tasks):
                item = await fut
                yield item['data']['reply']

    async def get(self, session, semaphore, objname):
        return await self.tns_post(session, semaphore, 'get/object', self.apiKey, {'objname': objname})