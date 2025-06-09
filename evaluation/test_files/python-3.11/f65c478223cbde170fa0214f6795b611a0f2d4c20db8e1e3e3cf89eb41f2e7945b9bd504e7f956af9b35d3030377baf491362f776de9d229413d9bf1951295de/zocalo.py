import copy
import json
import logging
import workflows.transport
from dls_utilpack.describe import describe
from dls_utilpack.explain import explain
from dls_utilpack.require import require
from dls_utilpack.thing import Thing
from dls_bxflow_api.bx_datafaces.bx_datafaces import bx_datafaces_get_default
from dls_bxflow_lib.base_aiohttp import BaseAiohttp
from dls_bxflow_lib.bx_jobs.bx_jobs import BxJobs
from dls_bxflow_lib.bx_jobs.states import States as BxJobStates
from dls_bxflow_lib.bx_launchers.constants import Queues
from dls_bxflow_run.bx_variables.bx_variables import BxVariables
logger = logging.getLogger(__name__)
thing_type = 'dls_bxflow_lib.bx_schedulers.zocalo'

class Zocalo(Thing, BaseAiohttp):
    """
    Object representing a registry which executes in zocalo.
    """

    def __init__(self, specification=None):
        Thing.__init__(self, thing_type, specification)
        BaseAiohttp.__init__(self, specification['server'])

    async def match(self):
        """ """
        records = await bx_datafaces_get_default().get_bx_jobs([BxJobStates.READY])
        logger.info('found %d %s bx_jobs' % (len(records), BxJobStates.READY))
        for record in records:
            await self.go(record)

    async def go(self, bx_job_record):
        bx_job_uuid = bx_job_record['uuid']
        bx_job = BxJobs().build_object(specification=bx_job_record['specification'], predefined_uuid=bx_job_uuid)
        await bx_job.fetch()
        variables = BxVariables()
        await variables.fetch(bx_job.uuid())
        variables_dict = {}
        for variable in variables.list():
            variables_dict[variable.trait('name')] = variable.trait('value')
        steps_dict = {}
        step_number = 0
        for bx_task in bx_job.bx_tasks.list():
            step_number += 1
            step_dict = {}
            step_dict['step_number'] = step_number
            step_dict['service'] = f"dls-bxflow bx_task {bx_task.label()} {bx_task.specification()['type']}"
            step_dict['queue'] = Queues.SUBMIT_ITASK
            step_dict['variables'] = {}
            step_dict['variables']['bx_launcher_payload'] = {}
            step_dict['variables']['bx_launcher_payload']['bx_job_uuid'] = bx_job_uuid
            step_dict['variables']['bx_launcher_payload']['bx_task_uuid'] = bx_task.uuid()
            step_dict['variables']['bx_launcher_payload']['bx_task_specification'] = copy.deepcopy(bx_task.specification())
            steps_dict[str(step_number)] = step_dict
        outputs = {}
        step_number = 0
        for bx_task in bx_job.bx_tasks.list():
            step_number += 1
            for dependency_bx_gate in bx_task.dependency_bx_gates.list():
                uuid = dependency_bx_gate.uuid()
                label = dependency_bx_gate.label()
                if uuid not in outputs:
                    outputs[uuid] = {}
                if label not in outputs[uuid]:
                    outputs[uuid][label] = []
                outputs[uuid][label].append(step_number)
        step_number = 0
        for bx_task in bx_job.bx_tasks.list():
            step_number += 1
            step_dict = steps_dict[str(step_number)]
            for controlled_bx_gate in bx_task.controlled_bx_gates.list():
                if controlled_bx_gate.uuid() in outputs:
                    step_dict['output'] = outputs[controlled_bx_gate.uuid()]
            step_dict.pop('step_number')
        steps_dict['start'] = [[1, []]]
        recipe_filename = self.specification()['recipe_filename']
        with open(f'{recipe_filename}', 'wt') as stream:
            json.dump(steps_dict, stream, indent=4)
        message = {'payload': [], 'recipe': steps_dict, 'recipe-path': [], 'recipe-pointer': 1}
        headers = {'workflows-recipe': 'True'}
        transport_factory = get_transport_factory(self.specification())
        self.__transport = transport_factory()
        self.__transport.connect()
        self.__transport.send(Queues.SUBMIT_ITASK, message=message, headers=headers)
        self.__transport.disconnect()
logger = logging.getLogger(__name__)

def get_transport_factory(specification):
    """"""
    thing_type = specification.get('type', 'unknown-thing-type')
    transport_factory = None
    try:
        type_specific_tbd = require('type_specific_tbd', specification, 'type_specific_tbd')
        transport_factory_specification = require('type_specific_tbd', type_specific_tbd, 'transport_factory')
        transport_mechanism = require('transport_factory_specification', transport_factory_specification, 'transport_mechanism')
        transport_factory = workflows.transport.lookup(transport_mechanism)
        logger.info(describe('transport_factory', transport_factory))
        if transport_mechanism == 'StompTransport':
            transport_factory.config['--stomp-host'] = require('transport_factory_specification', transport_factory_specification, 'stomp-host')
            transport_factory.config['--stomp-port'] = require('transport_factory_specification', transport_factory_specification, 'stomp-port')
        elif transport_mechanism == 'PikaTransport':
            transport_factory.config['--rabbit-host'] = require('transport_factory_specification', transport_factory_specification, 'rabbit-host')
            transport_factory.config['--rabbit-port'] = require('transport_factory_specification', transport_factory_specification, 'rabbit-port')
        else:
            raise RuntimeError(f'unrecognized transport_mechanism {transport_mechanism}')
    except Exception as exception:
        raise explain(exception, f'configuring {thing_type} transport factory')
    return transport_factory