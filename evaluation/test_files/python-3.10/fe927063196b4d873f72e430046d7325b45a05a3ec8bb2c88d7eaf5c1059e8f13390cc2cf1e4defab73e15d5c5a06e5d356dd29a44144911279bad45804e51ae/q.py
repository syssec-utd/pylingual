import asyncio
from oap_rq.logger import logger
from oap_rq.sender import RedisQueue

class QBus:

    def __init__(self, redis, *, service='notify', queue='test'):
        self.queue = RedisQueue(redis, service=service, queue=queue)

    async def send(self, data, timeout=5):
        return await self.queue.send(data, timeout)

    async def consume(self, name, worker):
        logger.info({'message': 'Woker Starting ', 'name': name, 'worker_id': worker})
        async for f in self.queue.receive(worker):
            yield f

    def consumer(self, *, name: str, workers: int=1):

        def _process(function):

            def decorated(*args, **kwargs):
                logger.info({'message': 'Consumer', 'name': name, 'status': 'started'})
                tasks = [function(self.consume(name, worker), **kwargs) for worker in range(1, workers + 1)]

                async def inner():
                    task = [asyncio.create_task(f) for f in tasks]
                    return await asyncio.gather(*task)
                return inner()
            return decorated
        return _process