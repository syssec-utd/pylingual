import asyncio
import logging
import os
import re
import socket
import time
from contextlib import closing
from typing import Any, Dict
from dls_utilpack.callsign import callsign
from dls_utilpack.explain import EXCEPTION_CAUSE_CHAIN_MARKER, EXCEPTION_CAUSE_CHAIN_PREFIX
from dls_utilpack.require import require
from dls_utilpack.thing import Thing
from dls_bxflow_api.exceptions import NotFound, NotSet
from dls_bxflow_api.remex import Clusters as RemexClusters
from dls_bxflow_api.remex import Keywords as RemexKeywords
from dls_bxflow_run.bx_gates.bx_gates import BxGates
from dls_bxflow_run.bx_gates.constants import Labels as BxGateLabels
from dls_bxflow_run.bx_tasks.constants import ExtractionErrorLinesMessages
from dls_bxflow_run.bx_variables.bx_variables import BxVariables
logger = logging.getLogger(__name__)

class Base(Thing):
    """ """

    def __init__(self, thing_type, specification=None, predefined_uuid=None):
        Thing.__init__(self, thing_type, specification, predefined_uuid=predefined_uuid)
        self.__label = require('%s specification' % thing_type, specification, 'label')
        remex_hints = require(f'{thing_type} specification', specification, RemexKeywords.HINTS)
        if not isinstance(remex_hints, dict):
            raise RuntimeError(f'{thing_type} specification {RemexKeywords.HINTS} is not a dictionary')
        remex_clusters = require(f'{thing_type} specification {RemexKeywords.HINTS}', remex_hints, RemexKeywords.CLUSTER)
        if not isinstance(remex_clusters, list):
            remex_clusters = [remex_clusters]
        for remex_cluster in remex_clusters:
            RemexClusters.validate(remex_cluster)
        self.__directory = specification.get('directory')
        self.__bx_job_uuid = specification.get('bx_job_uuid')
        self.__variables = BxVariables()
        self.__controlled_bx_gates = BxGates()
        self.__dependency_bx_gates = BxGates()
        self.__success_bx_gate = self.__controlled_bx_gates.build_object({'type': 'dls_bxflow_lib.bx_gates.standard', 'label': BxGateLabels.SUCCESS})
        self.__controlled_bx_gates.add(self.__success_bx_gate)
        self.__failure_bx_gate = self.__controlled_bx_gates.build_object({'type': 'dls_bxflow_lib.bx_gates.standard', 'label': BxGateLabels.FAILURE})
        self.__controlled_bx_gates.add(self.__failure_bx_gate)

    def label(self):
        return self.__label

    def set_directory(self, directory):
        self.__directory = directory

    def get_directory(self):
        if self.__directory is None:
            raise NotSet(f'{callsign(self)} directory has not been set')
        return self.__directory

    def bx_job_uuid(self, bx_job_uuid=None):
        if bx_job_uuid is not None:
            self.__bx_job_uuid = bx_job_uuid
        return self.__bx_job_uuid

    def _get_bx_variables(self):
        return self.__variables

    def _set_bx_variables(self, variables):
        self.__variables = variables

    def _del_variables(self):
        del self.__variables
    variables = property(fget=_get_bx_variables, fset=_set_bx_variables, fdel=_del_variables, doc='The variables property.')

    def _get_success_bx_gate(self):
        return self.__success_bx_gate
    success_bx_gate = property(fget=_get_success_bx_gate, doc='The success bx_gate property.')

    def _get_failure_bx_gate(self):
        return self.__failure_bx_gate
    failure_bx_gate = property(fget=_get_failure_bx_gate, doc='The failure bx_gate property.')

    def _get_controlled_bx_gates(self):
        return self.__controlled_bx_gates

    def _set_controlled_bx_gates(self, controlled_bx_gates):
        self.__controlled_bx_gates = controlled_bx_gates

    def _del_controlled_bx_gates(self):
        del self.__controlled_bx_gates
    controlled_bx_gates = property(fget=_get_controlled_bx_gates, fset=_set_controlled_bx_gates, fdel=_del_controlled_bx_gates, doc='The controlled_bx_gates property.')

    def _get_dependency_bx_gates(self):
        return self.__dependency_bx_gates

    def _set_dependency_bx_gates(self, dependency_bx_gates):
        self.__dependency_bx_gates = dependency_bx_gates

    def _del_dependency_bx_gates(self):
        del self.__dependency_bx_gates
    dependency_bx_gates = property(fget=_get_dependency_bx_gates, fset=_set_dependency_bx_gates, fdel=_del_dependency_bx_gates, doc='The dependency_bx_gates property.')

    def add_dependency_bx_gate(self, bx_gate):
        self.dependency_bx_gates.add(bx_gate)

    async def register(self, bx_job_uuid):
        self.__controlled_bx_gates.register(bx_job_uuid, self.uuid())

    def propose_artefact(self, artefact):
        """
        Write the artefact request into the runtime directory for later sending to the catalog.
        """
        with open('.bxflow/artefacts.txt', 'a') as stream:
            stream.write(f'{artefact}\n')

    def extract_error_lines_from_dls_logformatter(self):
        """
        Get task post-run fields after the task finished running.
        """
        error_lines = []
        runtime_directory = self.get_directory()
        stderr_filename = f'{runtime_directory}/stderr.txt'
        if os.path.exists(stderr_filename):
            lines = None
            try:
                with open(stderr_filename, 'r') as stream:
                    lines = stream.readlines(32768)
            except Exception as exception:
                s = str(exception)
                s = s.replace(stderr_filename, '')
                s = s.replace("''", '')
                s = s.replace('""', '')
                s = s.rstrip(': ')
                error_lines.append(f'{ExtractionErrorLinesMessages.PROBLEM_READING} {stderr_filename}: {s}')
            if lines is not None:
                if len(lines) == 0:
                    error_lines.append(f'{stderr_filename} {ExtractionErrorLinesMessages.EXISTS_BUT_IS_EMPTY}')
                elif len(lines) > 1 and EXCEPTION_CAUSE_CHAIN_MARKER in lines[0]:
                    for i in range(1, 10):
                        if not lines[i].startswith(EXCEPTION_CAUSE_CHAIN_PREFIX):
                            break
                        error_lines.append(lines[i][len(EXCEPTION_CAUSE_CHAIN_PREFIX):].rstrip())
                else:
                    line = re.sub('[ ]+', ' ', lines[0].rstrip())
                    parts = line.split(' ')
                    if len(parts) > 9:
                        error_lines.append(' '.join(parts[9:]))
                    else:
                        error_lines.append(lines[0].strip())
                        if len(lines) > 1 and lines[1].startswith('see '):
                            error_lines.append(lines[1].strip())
        else:
            error_lines.append(f'{stderr_filename} {ExtractionErrorLinesMessages.DOES_NOT_EXIST}')
        return error_lines

    def _find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    async def prepare_pairstream_publisher(self):
        from dls_pairstream_lib.pairstream import new_WriterInterface
        hostname = socket.gethostname()
        port = self._find_free_port()
        producer_configuration = {'class_name': 'dls::pairstream::zmq_pushpull', 'endpoint': f'tcp://*:{port}', 'should_block': True, 'send_timeout_milliseconds': 2000}
        self.__pairstream_publisher = new_WriterInterface(producer_configuration)
        self.__pairstream_publisher.activate()
        consumer_endpoint = f'tcp://{hostname}:{port}'
        logger.info(f'pairstream consumer_endpoint is {consumer_endpoint}')
        bx_variables = BxVariables()
        bx_variables.add(f'{self.label()}.pairstream_consumer_endpoint', consumer_endpoint)
        await bx_variables.register(self.bx_job_uuid())

    async def prepare_pairstream_consumer(self, publisher_label: str):
        bx_variables = BxVariables()
        from dls_pairstream_lib.pairstream import new_ReaderInterface
        name = f'{publisher_label}.pairstream_consumer_endpoint'
        timeout = 5.0
        naptime = 0.5
        time0 = time.time()
        while True:
            await bx_variables.fetch(self.bx_job_uuid())
            try:
                bx_variable = bx_variables.find(name, trait_name='name')
                break
            except NotFound:
                pass
            if time.time() > time0 + timeout:
                raise RuntimeError(f'did not find bx_variable {name} within timeout {timeout} seconds')
            await asyncio.sleep(naptime)
        consumer_configuration = {'class_name': 'dls::pairstream::zmq_pushpull', 'endpoint': bx_variable.trait('value')}
        self.__pairstream_consumer = new_ReaderInterface(consumer_configuration)
        self.__pairstream_consumer.activate()

    def publish_pairstream(self, meta: Dict, data: Any):
        self.__pairstream_publisher.write(meta, data)

    def consume_pairstream(self, meta: Dict, data: Any):
        self.__pairstream_consumer.read(meta, data)