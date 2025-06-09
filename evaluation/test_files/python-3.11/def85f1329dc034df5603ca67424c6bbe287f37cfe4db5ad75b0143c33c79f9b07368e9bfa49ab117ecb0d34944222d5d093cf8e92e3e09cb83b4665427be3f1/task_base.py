"""
celery自定义任务基类
"""
from celery import Task
from yyxx_game_pkg.xtrace.helper import get_current_trace_id

class TaskCustomBase(Task):

    def __init__(self):
        self._task_type = 'TaskBase'

    def on_success(self, retval, task_id, args, kwargs):
        trace_id = get_current_trace_id()
        print(f"[trace_id: {trace_id}]<{self._task_type}> on_success: {task_id}, kwargs:{kwargs.get('schedule_name')}, statistic_id:{kwargs.get('statistic_id')}, svr_id_slice_size:{(len(kwargs.get('server_ids', [])),)}, sdate:{kwargs.get('sdate')}, edate:{kwargs.get('edate')}")
        return super(TaskCustomBase, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        trace_id = get_current_trace_id()
        print(f'[trace_id: {trace_id}]<{self._task_type}> on_failure, reason:{exc}, task_id:{task_id}, args:{args}, kwargs:{kwargs}')
        return super(TaskCustomBase, self).on_failure(exc, task_id, args, kwargs, einfo)