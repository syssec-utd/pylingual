import logging
import attr
from pobptrace.internal import compat
from pobptrace.internal import periodic
from pobptrace.internal.utils import attr as attr_utils
from pobptrace.profiling import _traceback
from pobptrace.profiling import exporter
LOG = logging.getLogger(__name__)

@attr.s
class Scheduler(periodic.PeriodicService):
    """Schedule export of recorded data."""
    recorder = attr.ib()
    exporters = attr.ib()
    before_flush = attr.ib(default=None, eq=False)
    _interval = attr.ib(factory=attr_utils.from_env('POBP_PROFILING_UPLOAD_INTERVAL', 60.0, float))
    _configured_interval = attr.ib(init=False)
    _last_export = attr.ib(init=False, default=None, eq=False)

    def __attrs_post_init__(self):
        self._configured_interval = self.interval

    def _start_service(self):
        """Start the scheduler."""
        LOG.debug('Starting scheduler')
        super(Scheduler, self)._start_service()
        self._last_export = compat.time_ns()
        LOG.debug('Scheduler started')

    def flush(self):
        """Flush events from recorder to exporters."""
        LOG.debug('Flushing events')
        if self.before_flush is not None:
            try:
                self.before_flush()
            except Exception:
                LOG.error('Scheduler before_flush hook failed', exc_info=True)
        if self.exporters:
            events = self.recorder.reset()
            start = self._last_export
            self._last_export = compat.time_ns()
            for exp in self.exporters:
                try:
                    exp.export(events, start, self._last_export)
                except exporter.ExportError as e:
                    LOG.error('Unable to export profile: %s. Ignoring.', _traceback.format_exception(e))
                except Exception:
                    LOG.exception('Unexpected error while exporting events. Please report this bug to https://github.com/DataDog/dd-trace-py/issues')

    def periodic(self):
        start_time = compat.monotonic()
        try:
            self.flush()
        finally:
            self.interval = max(0, self._configured_interval - (compat.monotonic() - start_time))