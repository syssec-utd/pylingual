import abc
from os.path import abspath
from os.path import isfile
from os.path import normcase
from os.path import normpath
from os.path import sep
from os.path import splitdrive
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
import attr
import six
from ddtrace.internal.logger import get_logger
from ddtrace.internal.module import _resolve
from ddtrace.internal.rate_limiter import BudgetRateLimiterWithJitter as RateLimiter
from ddtrace.internal.utils.cache import cached
log = get_logger(__name__)

@cached()
def _resolve_source_file(path):
    """Resolve the source path for the given path.

    This recursively strips parent directories until it finds a file that
    exists according to sys.path.
    """
    npath = abspath(normpath(normcase(path)))
    if isfile(npath):
        return npath
    _, relpath = splitdrive(npath)
    while relpath:
        resolved_path = _resolve(relpath)
        if resolved_path is not None:
            return abspath(resolved_path)
        _, _, relpath = relpath.partition(sep)
    return None

@attr.s(hash=True)
class Probe(six.with_metaclass(abc.ABCMeta)):
    probe_id = attr.ib(type=str)
    tags = attr.ib(type=dict, factory=dict, eq=False)
    active = attr.ib(type=bool, default=True, eq=False)
    rate = attr.ib(type=float, default=1.0, eq=False)
    limiter = attr.ib(type=RateLimiter, init=False, repr=False, eq=False)

    def __attrs_post_init__(self):
        self.limiter = RateLimiter(limit_rate=self.rate, tau=1.0 / self.rate if self.rate else 1.0, on_exceed=lambda: log.warning('Rate limit exceeeded for %r', self), call_once=True, raise_on_exceed=False)

    def activate(self):
        """Activate the probe."""
        self.active = True

    def deactivate(self):
        """Deactivate the probe."""
        self.active = False

@attr.s
class ConditionalProbe(Probe):
    """Conditional probe.

    If the condition is ``None``, then this is equivalent to a non-conditional
    probe.
    """
    condition = attr.ib(type=Optional[Callable[[Dict[str, Any]], Any]], default=None)

@attr.s
class LineProbe(ConditionalProbe):
    source_file = attr.ib(type=Optional[str], default=None, converter=_resolve_source_file)
    line = attr.ib(type=Optional[int], default=None)

@attr.s
class FunctionProbe(ConditionalProbe):
    module = attr.ib(type=Optional[str], default=None)
    func_qname = attr.ib(type=Optional[str], default=None)

class MetricProbeKind(object):
    COUNTER = 'COUNT'
    GAUGE = 'GAUGE'
    HISTOGRAM = 'HISTOGRAM'
    DISTRIBUTION = 'DISTRIBUTION'

@attr.s
class MetricProbe(LineProbe):
    kind = attr.ib(type=Optional[str], default=None)
    name = attr.ib(type=Optional[str], default=None)
    value = attr.ib(type=Optional[Callable[[Dict[str, Any]], Any]], default=None)