import importlib
import os
import re
import sys
from inspect import isclass
from pathlib import Path
from typing import Dict, Union, Callable, ClassVar
from tepe.core.base_task import BaseTask
task_dict = {}

def register_config(task_name: str=None):
    """Register a task config in task_dict.

    Example:
        >>> @register_config()
        >>> class YOLOv5Config:
        >>>     pass

        >>> @register_config(task_name='yolox')
        >>> class YOLOXConfig:
        >>>     pass

    Args:
        task_name (str | None): The task name to be registered. If not
            specified, the class name will be used.
    """

    def _register(cls):
        name = task_name
        if task_name is None:
            name = cls.__name__
            s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', name)
            name = re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower().replace('_config', '')
        task_dict[name] = cls
        return cls
    return _register

def get_task(name: str) -> BaseTask:
    """
    Get task instance according to task name or task file.
    Args:
        name: task name or task file

    Returns:
        task config instance
    """
    return get_task_cls(name)()

def get_task_cls(name: str) -> ClassVar[BaseTask]:
    """
    Get task class according to task name or task file.
    Args:
        name: task name or task file

    Returns:
        task config class
    """
    if Path(name).suffix == '.py':
        if not os.path.exists(name):
            raise FileNotFoundError('{} is not found.'.format(name))
        task_file = name
    else:
        task_file_list = _get_task_file_list()
        task_file = task_file_list.get(name)
        assert task_file is not None, f'{name} is not in task list'
    task_cls = _find_task_obj(task_file)
    assert task_cls is not None, ImportError(f'Task object is not found in {name}.')
    return task_cls

def print_tasks() -> None:
    """
    Print tasks list.
    """
    task_file_list = _get_task_file_list()
    print('\n'.join(['{:20s} {}'.format(k, v) for (k, v) in task_file_list.items()]))

def _find_task_obj(task_file: str) -> Union[None, Callable]:
    """
    Find task class in task file.
    Args:
        task_file: Absolute path of task config.

    Returns:
        task class
    """
    task_cls = None
    task_dir = os.path.abspath(os.path.dirname(task_file))
    sys.path.append(task_dir)
    module_name = os.path.basename(task_file).split('.')[0]
    current_module = importlib.import_module(module_name)
    for (obj_name, obj) in current_module.__dict__.items():
        if not isclass(obj):
            continue
        if obj_name.startswith('_'):
            continue
        if issubclass(obj, BaseTask) and obj_name != 'BaseTask':
            task_cls = obj
    sys.path.remove(task_dir)
    return task_cls

def _get_task_file_list() -> Dict:
    """
    Get task files list.
    Returns:
        Dict {task_name: task_file}
    """
    task_list = {}
    from tepe import tasks
    tasks_dir = os.path.dirname(tasks.__file__)
    for task_name in os.listdir(tasks_dir):
        if task_name.startswith('_') and (not os.path.isdir(os.path.join(tasks_dir, task_name))):
            continue
        task_file = os.path.join(tasks_dir, task_name, 'task.py')
        if task_name not in task_list and os.path.exists(task_file):
            task_list[task_name] = task_file
    return task_list