__all__ = ['expect_not_an_experiment', 'join_paths', 'verify_type', 'RunType']
from typing import Union
from neptune import Run
from neptune.common.experiments import LegacyExperiment as Experiment
from neptune.exceptions import NeptuneLegacyIncompatibilityException
from neptune.handler import Handler
from neptune.internal.utils import verify_type
from neptune.internal.utils.paths import join_paths

def expect_not_an_experiment(run: Run):
    if isinstance(run, Experiment):
        raise NeptuneLegacyIncompatibilityException()
RunType = Union[Run, Handler]