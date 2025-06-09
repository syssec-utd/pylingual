import asyncio
import logging
import time
import traceback
from string import Template
from connect.client import AsyncConnectClient
from connect.client.models import AsyncCollection, AsyncResource
from connect.eaas.core.enums import ResultType
from connect.eaas.core.proto import Task, TaskOutput
from connect.eaas.core.responses import ProcessingResponse
from connect.eaas.runner.managers.base import TasksManagerBase
logger = logging.getLogger(__name__)

class BackgroundTasksManager(TasksManagerBase):

    def get_method_name(self, task_data, argument):
        return self.handler.events[task_data.input.event_type]['method']

    async def get_argument(self, task_data):
        """
        Get the request object through the Connect public API
        related to the task that need processing.
        """
        client = self.client
        if task_data.options.api_key:
            client = AsyncConnectClient(task_data.options.api_key, endpoint=self.config.get_api_url(), use_specs=False, default_headers=self.config.get_user_agent())
        definition = self.config.event_definitions[task_data.input.event_type]
        supported_statuses = self.handler.events[task_data.input.event_type]['statuses']
        rql_filter = Template(definition.api_collection_filter).substitute({'_statuses_': f"({','.join(supported_statuses)})", '_object_id_': task_data.input.object_id})
        collection = AsyncCollection(client, definition.api_collection_endpoint)
        if await collection.filter(rql_filter).count() == 0:
            logger.info(f'Send skip response for {task_data.options.task_id} since the current request status is not supported.')
            self.send_skip_response(task_data, f"The request status does not match the supported statuses: {','.join(supported_statuses)}.")
            return
        url = definition.api_resource_endpoint.format(pk=task_data.input.object_id)
        resource = AsyncResource(client, url)
        return await resource.get()

    async def build_response(self, task_data, future):
        """
        Wait for a background task to be completed and then build the task result message.
        """
        result_message = Task(**task_data.dict())
        result = None
        try:
            begin_ts = time.monotonic()
            result = await asyncio.wait_for(future, timeout=self.config.get_timeout('background'))
            result_message.output = TaskOutput(result=result.status)
            result_message.output.runtime = time.monotonic() - begin_ts
            logger.info(f'background task {task_data.options.task_id} result: {result.status}, took: {result_message.output.runtime}')
            if result.status in (ResultType.SKIP, ResultType.FAIL):
                result_message.output.message = result.output
            if result.status == ResultType.RESCHEDULE:
                result_message.output.countdown = result.countdown
        except Exception as e:
            self.log_exception(task_data, e)
            result_message.output = TaskOutput(result=ResultType.RETRY)
            result_message.output.message = traceback.format_exc()[:4000]
        return result_message

    def send_skip_response(self, data, output):
        future = asyncio.Future()
        future.set_result(ProcessingResponse.skip(output))
        asyncio.create_task(self.enqueue_result(data, future))