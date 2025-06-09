from threading import Thread
import time
from types import FrameType
from typing import Any
from typing import Dict
from typing import Optional
from uuid import uuid4
import attr
from ddtrace.context import Context
from ddtrace.debugging._probe.model import ConditionalProbe
from ddtrace.internal.compat import ExcInfoType
from ddtrace.internal.logger import get_logger
log = get_logger(__name__)

class ConditionEvaluationError(Exception):
    """Thrown when an error occurs while evaluating a probe condition."""

@attr.s
class Snapshot(object):
    """Raw snapshot.

    Used to collect the minimum amount of information from a firing probe.
    """
    probe = attr.ib(type=ConditionalProbe)
    frame = attr.ib(type=FrameType)
    thread = attr.ib(type=Thread)
    exc_info = attr.ib(type=ExcInfoType)
    context = attr.ib(type=Optional[Context])
    entry_capture = attr.ib(type=Optional[dict], default=None)
    return_capture = attr.ib(type=Optional[dict], default=None)
    duration = attr.ib(type=Optional[int], default=None)
    timestamp = attr.ib(type=float, factory=time.time)
    snapshot_id = attr.ib(type=str, init=False, factory=lambda : str(uuid4()))

    def evaluate(self, _locals=None):
        """Evaluate the probe condition against the collected frame."""
        condition = self.probe.condition
        if condition is None:
            return True
        try:
            return bool(condition(_locals or self.frame.f_locals))
        except Exception as e:
            raise ConditionEvaluationError(e)