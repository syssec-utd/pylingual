def run(self, job: Job) -> Future[Result]:
    """ return values of execute are set as result of the task
        returned by ensure_future(), obtainable via task.result()
        """
    if not self.watcher_ready:
        self.log.error(f'child watcher unattached when executing {job}')
        job.cancel('unattached watcher')
    elif not self.can_execute(job):
        self.log.error('invalid execution job: {}'.format(job))
        job.cancel('invalid')
    else:
        self.log.debug('executing {}'.format(job))
        task = asyncio.ensure_future(self._execute(job), loop=self.loop)
        task.add_done_callback(job.finish)
        task.add_done_callback(L(self.job_done)(job, _))
        self.current[job.client] = job
    return job.status