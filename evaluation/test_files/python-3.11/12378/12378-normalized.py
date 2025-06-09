def _build_job_arguments(task):
    """Build the set of arguments required for running a job"""
    job_args = {}
    job_args['qitems'] = Q_STORAGE_ITEMS
    job_args['task_id'] = task.task_id
    job_args['backend'] = task.backend
    backend_args = copy.deepcopy(task.backend_args)
    if 'next_from_date' in backend_args:
        backend_args['from_date'] = backend_args.pop('next_from_date')
    if 'next_offset' in backend_args:
        backend_args['offset'] = backend_args.pop('next_offset')
    job_args['backend_args'] = backend_args
    job_args['category'] = task.category
    archiving_cfg = task.archiving_cfg
    job_args['archive_args'] = archiving_cfg.to_dict() if archiving_cfg else None
    sched_cfg = task.scheduling_cfg
    job_args['max_retries'] = sched_cfg.max_retries if sched_cfg else MAX_JOB_RETRIES
    return job_args