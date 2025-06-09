async def start_master(self):
    """Actually start crawling."""
    for url in self.start_urls:
        request_ins = self.request(url=url, callback=self.parse, metadata=self.metadata)
        self.request_queue.put_nowait(self.handle_request(request_ins))
    workers = [asyncio.ensure_future(self.start_worker()) for i in range(self.worker_numbers)]
    for worker in workers:
        self.logger.info(f'Worker started: {id(worker)}')
    await self.request_queue.join()
    if not self.is_async_start:
        await self.stop(SIGINT)
    else:
        await self._cancel_tasks()