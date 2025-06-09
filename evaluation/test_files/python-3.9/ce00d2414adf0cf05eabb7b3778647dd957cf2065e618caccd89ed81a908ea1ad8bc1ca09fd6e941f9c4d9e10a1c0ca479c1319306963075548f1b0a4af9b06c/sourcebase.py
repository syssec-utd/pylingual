__author__ = 'Myron Walker'
__copyright__ = 'Copyright 2023, Myron W Walker'
__credits__ = []
__version__ = '1.0.0'
__maintainer__ = 'Myron Walker'
__email__ = 'myron.walker@gmail.com'
__status__ = 'Development'
__license__ = 'MIT'
from typing import Callable, Type
import inspect

class SourceBase:

    def __init__(self, source_func: Callable, query_func: Callable, resource_type: Type, constaints: dict):
        self._source_func = source_func
        self._query_func = query_func
        self._resource_type = resource_type
        self._constraints = constaints
        self._subscriptions = None
        return

    @property
    def constraints(self):
        return self._constraints

    @property
    def module_name(self) -> str:
        return self._source_func.__module__

    @property
    def query_function(self) -> Callable:
        return self._query_func

    @property
    def resource_type(self) -> Type:
        return self._resource_type

    @property
    def source_function(self) -> Callable:
        return self._source_func

    @property
    def source_signature(self) -> inspect.Signature:
        return inspect.signature(self._source_func)

    @property
    def source_id(self) -> str:
        source = self._source_func
        idstr = '{}#{}'.format(source.__module__, source.__name__)
        return idstr

    @property
    def subscriptions(self):
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, val):
        self._subscriptions = val
        return