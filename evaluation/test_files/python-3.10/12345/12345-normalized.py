def add(self, task_id, backend, category, backend_args, archiving_cfg=None, scheduling_cfg=None):
    """Add a task to the registry.

        This method adds task using `task_id` as identifier. If a task
        with the same identifier already exists on the registry, a
        `AlreadyExistsError` exception will be raised.

        :param task_id: identifier of the task to add
        :param backend: backend used to fetch data from the repository
        :param category: category of the items to fetch
        :param backend_args: dictionary of arguments required to run the backend
        :param archiving_cfg: archiving config for the task, if needed
        :param scheduling_cfg: scheduling config for the task, if needed

        :returns: the new task added to the registry

        :raises AlreadyExistsError: raised when the given task identifier
            exists on the registry
        """
    self._rwlock.writer_acquire()
    if task_id in self._tasks:
        self._rwlock.writer_release()
        raise AlreadyExistsError(element=str(task_id))
    task = Task(task_id, backend, category, backend_args, archiving_cfg=archiving_cfg, scheduling_cfg=scheduling_cfg)
    self._tasks[task_id] = task
    self._rwlock.writer_release()
    logger.debug('Task %s added to the registry', str(task_id))
    return task