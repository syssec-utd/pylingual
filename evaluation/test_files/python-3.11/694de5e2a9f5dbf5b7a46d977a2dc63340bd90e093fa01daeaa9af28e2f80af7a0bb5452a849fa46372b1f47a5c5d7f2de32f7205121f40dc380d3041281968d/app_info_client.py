import asyncio
import logging
from ..core.base_client import BaseClient
logger = logging.getLogger(__name__)

class AppInfoClient(BaseClient):

    def __init__(self, url, session=None, identity=None):
        super(AppInfoClient, self).__init__(url, session, identity)

    async def __get_info(self):
        url = f'/atlas_engine/api/v1/info'
        result = await self.do_get(url)
        return result

    def get_info(self):

        async def run_loop():
            result = await self.__get_info()
            return result
        logger.info(f"Connection to atlas engine at url '{self._url}'.")
        logger.info(f'Get info of the atlas engine.')
        loop = asyncio.new_event_loop()
        task = run_loop()
        result = loop.run_until_complete(task)
        loop.close()
        return result

    async def __get_authority(self):
        url = f'/atlas_engine/api/v1/authority'
        result = await self.do_get(url)
        return result

    def get_authority(self):

        async def run_loop():
            result = await self.__get_authority()
            return result
        logger.info(f"Connection to atlas engine at url '{self._url}'.")
        logger.info(f'Get info of the authority of the atlas engine.')
        loop = asyncio.new_event_loop()
        task = run_loop()
        result = loop.run_until_complete(task)
        loop.close()
        return result