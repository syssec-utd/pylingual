import logging
import os
import queue
import threading
from time import sleep, time
from typing import Any, Dict
import attr
from dbnd._core.current import in_tracking_run, is_orchestration_run
from dbnd._core.errors.base import DatabandWebserverNotReachableError
from dbnd._core.errors.errors_utils import log_exception
from dbnd._core.log.external_exception_logging import log_exception_to_server
from dbnd._core.tracking.backends.abstract_tracking_store import is_state_call
from dbnd._core.tracking.backends.channels.abstract_channel import TrackingChannel
from dbnd._core.tracking.backends.channels.tracking_web_channel import TrackingWebChannel
from dbnd._core.tracking.backends.tracking_store_composite import try_run_handler
from dbnd._vendor.pendulum import utcnow
logger = logging.getLogger(__name__)
_TERMINATOR = object()

class TrackingAsyncWebChannelBackgroundWorker(object):

    def __init__(self, item_processing_handler, skip_processing_callback):
        self.item_processing_handler = item_processing_handler
        self.skip_processing_callback = skip_processing_callback
        self._lock = None
        self._queue = None
        self._thread = None
        self._thread_for_pid = None

    @property
    def queue(self):
        if self._queue is None:
            self._queue = queue.Queue()
        return self._queue

    @property
    def lock(self):
        if self._lock is None:
            self._lock = threading.Lock()
        return self._lock

    @property
    def is_alive(self) -> bool:
        if self._thread_for_pid != os.getpid():
            return False
        if not self._thread:
            return False
        return self._thread.is_alive()

    def start(self) -> None:
        with self.lock:
            if not self.is_alive:
                self._thread = threading.Thread(target=self._thread_worker, daemon=True, name='dbnd.TrackingAsyncWebChannelBackgroundWorker')
                self._thread.start()
                self._thread_for_pid = os.getpid()

    def flush(self, timeout) -> None:
        logger.debug('background worker got flush request')
        with self.lock:
            if self.is_alive:
                self.queue.put(_TERMINATOR)
                self._wait_flush(timeout)
                self._thread = None
                self._thread_for_pid = None
                self._lock = None
                self._queue = None

    def _wait_flush(self, timeout: float) -> None:
        initial_timeout = min(0.1, timeout)
        if not self._timed_queue_join(initial_timeout):
            logger.debug('%d event(s) pending on flush', self.get_qsize())
            if not self._timed_queue_join(timeout - initial_timeout):
                raise TimeoutError('Flush timed out and dropped some events', self.get_qsize(), timeout)

    def _timed_queue_join(self, timeout: float) -> bool:
        deadline = time() + timeout
        self.queue.all_tasks_done.acquire()
        try:
            while self.queue.unfinished_tasks:
                delay = deadline - time()
                if delay <= 0:
                    return False
                self.queue.all_tasks_done.wait(timeout=delay)
            return True
        finally:
            self.queue.all_tasks_done.release()

    def _thread_worker(self) -> None:
        failed_on_previous_iteration = False
        while True:
            item = self.queue.get()
            try:
                if item is _TERMINATOR:
                    break
                if not failed_on_previous_iteration:
                    self.item_processing_handler(item)
                else:
                    self.skip_processing_callback(item)
            except Exception as e:
                failed_on_previous_iteration = True
                err_msg = 'TrackingAsyncWebChannelBackgroundWorker will skip processing next events'
                log_exception(err_msg, e, logger)
            finally:
                self.queue.task_done()
            sleep(0)

    def _ensure_thread(self) -> None:
        if not self.is_alive:
            self.start()

    def submit(self, item: Any) -> None:
        self._ensure_thread()
        self.queue.put(item)

    def get_qsize(self) -> int:
        return self._queue.qsize() + 1

@attr.s
class AsyncWebChannelQueueItem(object):
    name: str = attr.ib()
    data: Dict[str, Any] = attr.ib()
    is_orchestration_run: str = attr.ib()
    stop_tracking_on_failure: str = attr.ib()

class TrackingAsyncWebChannel(TrackingChannel):
    """Json API client implementation with non-blocking calls."""

    def __init__(self, max_retries, remove_failed_store, tracker_raise_on_error, is_verbose, databand_api_client, *args, **kwargs):
        super(TrackingAsyncWebChannel, self).__init__(*args, **kwargs)
        self.web_channel = TrackingWebChannel(databand_api_client)
        self._background_worker = TrackingAsyncWebChannelBackgroundWorker(item_processing_handler=self._background_worker_item_handler, skip_processing_callback=self._background_worker_skip_processing_callback)
        self._max_retries = max_retries
        self._remove_failed_store = remove_failed_store
        self._tracker_raise_on_error = tracker_raise_on_error
        self._is_verbose = is_verbose
        self._log_fn = logger.info if self._is_verbose else logger.debug
        self._shutting_down = False
        self._start_time = utcnow()

    def _handle(self, name, data):
        if self._shutting_down:
            raise RuntimeError('TrackingAsyncWebChannel is invoked during flush')
        stop_tracking_on_failure = self._remove_failed_store or (in_tracking_run() and is_state_call(name))
        item = AsyncWebChannelQueueItem(name=name, data=data, is_orchestration_run=is_orchestration_run(), stop_tracking_on_failure=stop_tracking_on_failure)
        self._background_worker.submit(item=item)

    def _background_worker_item_handler(self, item: AsyncWebChannelQueueItem):
        try:
            tries = self._max_retries if is_state_call(item.name) else 1
            self._log_fn('TrackingAsyncWebChannel.thread_worker processing %s', item.name)
            try_run_handler(tries, self.web_channel, item.name, {'data': item.data})
            self._log_fn('TrackingAsyncWebChannel.thread_worker completed %s', item.name)
        except Exception as exc:
            log_exception_to_server()
            logger.warning('Exception in TrackingAsyncWebChannel in background worker', exc_info=True)
            if item.stop_tracking_on_failure:
                raise exc
            if isinstance(exc, DatabandWebserverNotReachableError):
                if in_tracking_run():
                    logger.warning(str(exc))
                if item.is_orchestration_run:
                    exc.show_exc_info = False
                if self._tracker_raise_on_error:
                    raise exc

    def _background_worker_skip_processing_callback(self, item: AsyncWebChannelQueueItem):
        self._log_fn('TrackingAsyncWebChannel skips %s tracking event due to a previous failure', item.name)

    def flush(self):
        if not self._background_worker.is_alive:
            return
        tracking_duration = (utcnow() - self._start_time).in_seconds()
        flush_limit = min(max(tracking_duration * 0.1, 5 * 60), 30 * 60)
        logger.info('Waiting %ss for TrackingAsyncWebChannel to complete async tasks...', flush_limit)
        self._shutting_down = True
        try:
            self._background_worker.flush(flush_limit)
            self.web_channel.flush()
            logger.info('TrackingAsyncWebChannel completed all tasks')
        except TimeoutError as e:
            err_msg = f'TrackingAsyncWebChannel flush exceeded {flush_limit}s timeout'
            log_exception(err_msg, e, logger)
        finally:
            self._shutting_down = False

    def is_ready(self):
        return self.web_channel.is_ready() and (not self._shutting_down)

    def __str__(self):
        return 'AsyncWeb'