def fetch_celery_task_state(celery_task):
    """
    Fetch and return the state of the given celery task. The scope of this function is
    global so that it can be called by subprocesses in the pool.

    :param celery_task: a tuple of the Celery task key and the async Celery object used
        to fetch the task's state
    :type celery_task: tuple(str, celery.result.AsyncResult)
    :return: a tuple of the Celery task key and the Celery state of the task
    :rtype: tuple[str, str]
    """
    try:
        with timeout(seconds=2):
            res = (celery_task[0], celery_task[1].state)
    except Exception as e:
        exception_traceback = 'Celery Task ID: {}\n{}'.format(celery_task[0], traceback.format_exc())
        res = ExceptionWithTraceback(e, exception_traceback)
    return res