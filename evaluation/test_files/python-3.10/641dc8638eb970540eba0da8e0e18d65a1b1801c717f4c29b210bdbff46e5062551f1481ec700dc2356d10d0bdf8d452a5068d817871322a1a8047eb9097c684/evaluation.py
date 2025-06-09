import json
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Mapping, Optional
import numpy as np

def _datetime_now_timestamp():
    """Wrapper to allow use as default factory for dataclass fields."""
    return datetime.now().timestamp()

@dataclass
class EvaluationSpecification(Mapping[str, Any]):
    configuration: dict = field(metadata={'Description': 'The configuration to be evaluated next.'})
    settings: dict = field(default_factory=dict, metadata={'Description': 'Additional settings like the fidelity or target task.'})
    optimizer_info: dict = field(default_factory=dict, metadata={'Description': 'Information about and for internal optimizer state.'})
    created_unixtime: float = field(default_factory=_datetime_now_timestamp, metadata={'Description': 'Creation time of the evaluation specificiation.'})
    context: Optional[Dict[str, Any]] = field(default=None, metadata={'Description': 'Contextual information is what you can determine but not ' + 'influence, like the environmental temperature.'})

    def keys(self):
        return self.__dataclass_fields__.keys()

    def create_evaluation(self, objectives: Dict[str, Optional[float]], constraints: Optional[Dict[str, Optional[float]]]=None, user_info: Optional[dict]=None, stacktrace: Optional[str]=None, finished_unixtime: Optional[float]=None):
        """Create a blackboxopt.Evaluation based on this evaluation specification.

        Args:
            objectives: For each objective name the respective value.
            constraints: For each constraint name the float value indicates how much the
                constraint was satisfied, with negative values implying a violated and
                positive values indicating a satisfied constraint.
            user_info: Miscellaneous information provided by the user.
            stacktrace: The stacktrace in case an unhandled exception occurred inside
                the evaluation function.
            finished_unixtime: Timestamp at completion of this evaluation. If none is
                provided, the current time is used.
        """
        evaluation = Evaluation(objectives=objectives, constraints=constraints, user_info=user_info, stacktrace=stacktrace, **self)
        if finished_unixtime is not None:
            evaluation.finished_unixtime = finished_unixtime
        return evaluation

    def __getitem__(self, key):
        if key not in self.__dataclass_fields__:
            raise KeyError(f"Only dataclass fields are accessible via __getitem__, '{key}' is not.")
        return deepcopy(getattr(self, key))

    def __iter__(self):
        return self.__dataclass_fields__.__iter__

    def __len__(self):
        return self.__dataclass_fields__.__len__

    def to_json(self, **json_dump_kwargs):
        return json.dumps(asdict(self), **json_dump_kwargs)

    def to_dict(self):
        return self.__dict__

@dataclass
class _EvaluationBase:
    """Helper dataclass to allow the Evaluation class to have attributes with defaults
    while still having attributes without default values. To make this happen, the
    non-default attributes need to be defined / inherited before the ones with defaults.

    Attributes:
        objectives: [description]

    Raises:
        ValueError: [description]
    """
    objectives: Dict[str, Optional[float]]

    def __post_init__(self):
        available_objective_values = np.array([o for o in self.objectives.values() if o is not None], dtype=float)
        if not np.isfinite(available_objective_values).all():
            raise ValueError(f'Objective values contain non-finite values: {self.objectives}\n' + 'Please use None to indicate missing objective evaluations.')

@dataclass
class Evaluation(EvaluationSpecification, _EvaluationBase):
    """An evaluated specification with a timestamp indicating the time of the
    evaluation, and a result dictionary for all objective values.

    NOTE: `NaN` is not allowed as an objective value, use `None` instead.
    """
    constraints: Optional[Dict[str, Optional[float]]] = field(default=None, metadata={'Description': 'For each constraint name the float value indicates ' + 'how much the constraint was satisfied, with negative values implying ' + 'a violated and positive values indicating a satisfied constraint.'})
    finished_unixtime: float = field(default_factory=_datetime_now_timestamp, metadata={'Description': 'Timestamp at completion of this evaluation.'})
    stacktrace: Optional[str] = field(default=None, metadata={'Description': 'The stacktrace in case an unhandled exception occurred ' + 'inside the evaluation function.'})
    user_info: Optional[dict] = field(default=None, metadata={'Description': 'Miscellaneous information provided by the user.'})

    def get_specification(self, reset_created_unixtime: bool=False) -> EvaluationSpecification:
        """Get the evaluation specifiation for which this result was evaluated."""
        eval_spec_kwargs = deepcopy(dict(configuration=self.configuration, settings=self.settings, optimizer_info=self.optimizer_info, context=self.context))
        if reset_created_unixtime:
            return EvaluationSpecification(created_unixtime=_datetime_now_timestamp(), **eval_spec_kwargs)
        return EvaluationSpecification(created_unixtime=self.created_unixtime, **eval_spec_kwargs)

    @property
    def any_objective_none(self) -> bool:
        return any([v is None for v in self.objectives.values()])

    @property
    def all_objectives_none(self) -> bool:
        return all([v is None for v in self.objectives.values()])