import logging
from os import environ, path
from typing import TYPE_CHECKING, Any, Dict, Tuple, Optional, Set, cast
from logging import Logger
from abc import abstractmethod
from json import dumps as jsondumps, loads as jsonloads
from jinja2 import Template
from locust.exception import StopUser
from locust.user.users import User
from locust.user.task import LOCUST_STATE_RUNNING
from locust.env import Environment
from grizzly.types import GrizzlyResponse, RequestType, ScenarioState
from ...tasks import RequestTask
from ...utils import merge_dicts
from . import FileRequests
if TYPE_CHECKING:
    from ...context import GrizzlyContextScenario

class GrizzlyUser(User):
    _context_root: str
    _context: Dict[str, Any] = {'variables': {}}
    _scenario: 'GrizzlyContextScenario'
    _scenario_state: Optional[ScenarioState]
    __dependencies__: Set[str] = set()
    logger: Logger
    weight: int = 1
    host: str

    def __init__(self, environment: Environment, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        super().__init__(environment, *args, **kwargs)
        self._context_root = environ.get('GRIZZLY_CONTEXT_ROOT', '.')
        self._context = merge_dicts({}, GrizzlyUser._context)
        self.logger = logging.getLogger(f'{self.__class__.__name__}/{id(self)}')
        self._scenario_state = None
        assert self.host is not None, f'{self.__class__.__name__} must have host set'

    @property
    def scenario_state(self) -> Optional[ScenarioState]:
        return self._scenario_state

    @scenario_state.setter
    def scenario_state(self, value: ScenarioState) -> None:
        old_state = self._scenario_state
        if old_state != value:
            self._scenario_state = value
            self.logger.debug(f'scenario state={old_state} -> {value}')

    def stop(self, force: bool=False) -> bool:
        if not force:
            self.logger.debug('stop scenarios before stopping user')
            self.scenario_state = ScenarioState.STOPPING
            self._state = LOCUST_STATE_RUNNING
            return False
        else:
            return cast(bool, super().stop(force=force))

    @abstractmethod
    def request(self, request: RequestTask) -> GrizzlyResponse:
        raise NotImplementedError(f'{self.__class__.__name__} has not implemented request')

    def render(self, request: RequestTask) -> Tuple[str, str, Optional[str], Optional[Dict[str, str]], Optional[Dict[str, str]]]:
        scenario_name = f'{request.scenario.identifier} {request.name}'
        try:
            payload: Optional[str] = None
            name = Template(request.name).render(**self.context_variables)
            scenario_name = f'{request.scenario.identifier} {name}'
            endpoint = Template(request.endpoint).render(**self.context_variables)
            arguments: Optional[Dict[str, str]] = None
            metadata: Optional[Dict[str, str]] = None
            if request.template is not None:
                payload = request.template.render(**self.context_variables)
                file = path.join(self._context_root, 'requests', payload)
                if path.isfile(file):
                    if not isinstance(self, FileRequests):
                        with open(file, 'r') as fd:
                            payload = fd.read()
                        if '{{' in payload and '}}' in payload:
                            payload = Template(payload).render(**self.context_variables)
                    else:
                        file_name = path.basename(payload)
                        if not endpoint.endswith(file_name):
                            endpoint = f'{endpoint}/{file_name}'
            if request.arguments is not None:
                arguments_json = jsondumps(request.arguments)
                rendered_json = Template(arguments_json).render(**self.context_variables)
                arguments = jsonloads(rendered_json)
            if request.metadata is not None:
                metadata_json = jsondumps(request.metadata)
                rendered_metadata = Template(metadata_json).render(**self.context_variables)
                metadata = jsonloads(rendered_metadata)
            return (name, endpoint, payload, arguments, metadata)
        except Exception as exception:
            self.logger.error(f'exception={exception!r}, request.name={request.name!r}, request.endpoint={request.endpoint!r}, self.context_variables={self.context_variables!r}, request.arguments={request.arguments!r}, request.metadata={request.metadata!r}', exc_info=True)
            self.environment.events.request.fire(request_type=RequestType.from_method(request.method), name=scenario_name, response_time=0, response_length=0, context=self._context, exception=exception)
            raise StopUser()

    def context(self) -> Dict[str, Any]:
        return self._context

    def add_context(self, context: Dict[str, Any]) -> None:
        self._context = merge_dicts(self._context, context)

    def set_context_variable(self, variable: str, value: Any) -> None:
        old_value = self._context['variables'].get(variable, None)
        self._context['variables'][variable] = value
        self.logger.debug(f'context variable={variable!r}, value={old_value} -> {value}')

    @property
    def context_variables(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], self._context.get('variables', {}))