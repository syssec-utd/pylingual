import asyncio
import select
import signal
from asyncio import Task, CancelledError
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from typing import Optional
from ..registry import MultiModelRegistry
from ..utils import install_uvloop_event_loop, schedule_with_callback
from ..logging import configure_logger
from ..settings import Settings
from ..metrics import configure_metrics, model_context
from ..env import Environment
from .messages import ModelRequestMessage, ModelUpdateType, ModelUpdateMessage, ModelResponseMessage
from .utils import terminate_queue, END_OF_QUEUE
from .logging import logger
from .errors import WorkerError
IGNORED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]

def _noop():
    pass

class Worker(Process):

    def __init__(self, settings: Settings, responses: Queue, env: Optional[Environment]=None):
        super().__init__()
        self._settings = settings
        self._responses = responses
        self._requests: Queue[ModelRequestMessage] = Queue()
        self._model_updates: Queue[ModelUpdateMessage] = Queue()
        self._env = env
        self.__executor = None

    @property
    def _executor(self):
        """
        Helper property to initialise a threadpool executor on demand.
        This is required to avoid having to pickle the executor object into a
        separate process.
        """
        if self.__executor is None:
            self.__executor = ThreadPoolExecutor()
        return self.__executor

    def run(self):
        ctx = nullcontext()
        if self._env:
            ctx = self._env
        with ctx:
            install_uvloop_event_loop()
            configure_logger(self._settings)
            configure_metrics(self._settings)
            self._ignore_signals()
            asyncio.run(self.coro_run())

    def _ignore_signals(self):
        """
        Uvloop will try to propagate the main process' signals to the
        underlying workers.
        However, this would just kill off the workers without any cleaning.
        To avoid this, and be able to properly shut them down, we forcefully
        ignore the signals coming from the main parent process.
        """
        loop = asyncio.get_event_loop()
        for sign in IGNORED_SIGNALS:
            loop.add_signal_handler(sign, _noop)

    def __inner_init__(self):
        """
        Internal __init__ method that needs to run within the worker process.
        """
        self._model_registry = MultiModelRegistry()
        self._active = True

    async def coro_run(self):
        self.__inner_init__()
        loop = asyncio.get_event_loop()
        while self._active:
            readable = await loop.run_in_executor(self._executor, self._select)
            for r in readable:
                if r is self._requests._reader:
                    request = self._requests.get()
                    schedule_with_callback(self._process_request(request), self._handle_response)
                elif r is self._model_updates._reader:
                    model_update = self._model_updates.get()
                    if model_update is END_OF_QUEUE:
                        self._active = False
                        return
                    schedule_with_callback(self._process_model_update(model_update), self._handle_response)

    def _select(self):
        (readable, _, _) = select.select([self._requests._reader, self._model_updates._reader], [], [])
        return readable

    async def _process_request(self, request) -> ModelResponseMessage:
        try:
            model = await self._model_registry.get_model(request.model_name, request.model_version)
            method = getattr(model, request.method_name)
            with model_context(model.settings):
                return_value = await method(*request.method_args, **request.method_kwargs)
            return ModelResponseMessage(id=request.id, return_value=return_value)
        except (Exception, CancelledError) as e:
            logger.exception(f"An error occurred calling method '{request.method_name}' from model '{request.model_name}'.")
            worker_error = WorkerError(e)
            return ModelResponseMessage(id=request.id, exception=worker_error)

    def _handle_response(self, process_task: Task):
        response_message = process_task.result()
        self._responses.put(response_message)

    async def _process_model_update(self, update: ModelUpdateMessage) -> ModelResponseMessage:
        try:
            model_settings = update.model_settings
            if update.update_type == ModelUpdateType.Load:
                await self._model_registry.load(model_settings)
            elif update.update_type == ModelUpdateType.Unload:
                await self._model_registry.unload_version(model_settings.name, model_settings.version)
            else:
                logger.warning('Unknown model update message with type ', update.update_type)
            return ModelResponseMessage(id=update.id)
        except (Exception, CancelledError) as e:
            logger.exception(f"An error occurred processing a model update of type '{update.update_type.name}'.")
            worker_error = WorkerError(e)
            return ModelResponseMessage(id=update.id, exception=worker_error)

    def send_request(self, request_message: ModelRequestMessage):
        """
        Send an inference request message to the worker.
        Note that this method should be both multiprocess- and thread-safe.
        """
        self._requests.put(request_message)

    def send_update(self, model_update: ModelUpdateMessage):
        """
        Send a model update to the worker.
        Note that this method should be both multiprocess- and thread-safe.
        """
        self._model_updates.put(model_update)

    async def stop(self):
        """
        Close the worker's main loop.
        Note that this method should be both multiprocess- and thread-safe.
        """
        await terminate_queue(self._model_updates)
        self._model_updates.close()
        self._requests.close()
        self._executor.shutdown()