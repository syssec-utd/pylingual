"""
Approximate the :class:`~moptipy.evaluation.ecdf.Ecdf` to reach certain goals.

The empirical cumulative distribution function (ECDF) for short illustrates
the fraction of runs that have reached a certain goal over time. Let's say
that you have performed 10 runs of a certain algorithm on a certain problem.
As goal quality, you could define the globally optimal solution quality.
For any point in time, the ECDF then shows how many of these runs have solved
the problem to this goal, to optimality.
Let's say the first run solves the problem after 100 FEs.
Then the ECDF is 0 until 99 FEs and at 100 FEs, it becomes 1/10.
The second fastest run solves the problem after 200 FEs.
The ECDF thus stays 0.1 until 199 FEs and at 200 FEs, it jumps to 0.2.
And so on.
This means that the value of the ECDF is always between 0 and 1.

1. Nikolaus Hansen, Anne Auger, Steffen Finck, Raymond Ros. *Real-Parameter
   Black-Box Optimization Benchmarking 2010: Experimental Setup.*
   Research Report RR-7215, INRIA. 2010. inria-00462481.
   https://hal.inria.fr/inria-00462481/document/
2. Dave Andrew Douglas Tompkins and Holger H. Hoos. UBCSAT: An Implementation
   and Experimentation Environment for SLS Algorithms for SAT and MAX-SAT. In
   *Revised Selected Papers from the Seventh International Conference on
   Theory and Applications of Satisfiability Testing (SAT'04),* May 10-13,
   2004, Vancouver, BC, Canada, pages 306-320. Lecture Notes in Computer
   Science (LNCS), volume 3542. Berlin, Germany: Springer-Verlag GmbH.
   ISBN: 3-540-27829-X. doi: https://doi.org/10.1007/11527695_24.
3. Holger H. Hoos and Thomas Stützle. Evaluating Las Vegas Algorithms -
   Pitfalls and Remedies. In Gregory F. Cooper and Serafín Moral, editors,
   *Proceedings of the 14th Conference on Uncertainty in Artificial
   Intelligence (UAI'98)*, July 24-26, 1998, Madison, WI, USA, pages 238-245.
   San Francisco, CA, USA: Morgan Kaufmann Publishers Inc.
   ISBN: 1-55860-555-X.
"""
from dataclasses import dataclass
from math import inf, isfinite
from typing import Any, Callable, Final, Iterable
import numpy as np
import moptipy.api.logging as lg
import moptipy.utils.nputils as npu
from moptipy.evaluation._utils import _get_reach_index
from moptipy.evaluation.base import F_NAME_NORMALIZED, F_NAME_SCALED, KEY_N, MultiRun2DData
from moptipy.evaluation.progress import Progress
from moptipy.utils.console import logger
from moptipy.utils.lang import Lang
from moptipy.utils.logger import COMMENT_CHAR, CSV_SEPARATOR, KEY_VALUE_SEPARATOR
from moptipy.utils.path import Path
from moptipy.utils.strings import num_to_str
from moptipy.utils.types import type_error
KEY_N_INSTS: Final[str] = f'{KEY_N}Insts'
KEY_F_NAME: Final[str] = 'fName'

@dataclass(frozen=True, init=False, order=True)
class Ecdf(MultiRun2DData):
    """The ECDF data."""
    ecdf: np.ndarray
    n_insts: int
    goal_f: int | float | None

    def __init__(self, algorithm: str | None, n: int, n_insts: int, time_unit: str, f_name: str, goal_f: int | float | None, ecdf: np.ndarray):
        """
        Create the ECDF function.

        :param algorithm: the algorithm name, if all runs are with the same
            algorithm
        :param n: the total number of runs
        :param n_insts: the total number of instances
        :param time_unit: the time unit
        :param f_name: the objective dimension name
        :param goal_f: the goal value, or `None` if different goals were used
            for different instances
        :param numpy.ndarray ecdf: the ert-ecdf matrix
        """
        super().__init__(algorithm, None, n, time_unit, f_name)
        if not isinstance(n_insts, int):
            raise type_error(n_insts, 'n_insts', int)
        if n_insts < 1 or n_insts > self.n:
            raise ValueError(f'n_insts must be > 0 and < n_runs ({self.n}), but got {n_insts}.')
        object.__setattr__(self, 'n_insts', n_insts)
        if goal_f is not None:
            if not isinstance(goal_f, (int, float)):
                raise type_error(goal_f, 'goal_f', (int, float))
            if not isfinite(goal_f):
                raise ValueError(f'Invalid goal_f {goal_f}.')
        object.__setattr__(self, 'goal_f', goal_f)
        if not isinstance(ecdf, np.ndarray):
            raise type_error(ecdf, 'ecdf', np.ndarray)
        ecdf.flags.writeable = False
        time: Final[np.ndarray] = ecdf[:, 0]
        ll = time.size
        if ll < 2:
            raise ValueError(f'Must have at least two points in ecdf curve , but encountered {ll}.')
        if not npu.is_all_finite(time[:-1]):
            raise ValueError(f'Non-last Ert-based time-values must be finite, but encountered {time}.')
        if np.any(time[1:] <= time[:-1]):
            raise ValueError(f'Time data must be strictly increasing,but encountered {time}.')
        prb: Final[np.ndarray] = ecdf[:, 1]
        if not npu.is_all_finite(prb):
            raise ValueError(f'All ECDF values must be finite, but encountered {prb}.')
        if ll > 2 and np.any(prb[1:-1] <= prb[:-2]):
            raise ValueError(f'ECDF data must be strictly increasing,but encountered {prb}.')
        if prb[0] < 0:
            raise ValueError(f'First ECDF element cannot be {prb[0]}.')
        if prb[ll - 1] > 1:
            raise ValueError(f'Last ECDF element cannot be {prb[ll - 1]}.')
        object.__setattr__(self, 'ecdf', ecdf)

    def time_label(self) -> str:
        """
        Get the time label for x-axes.

        :return: the time key
        """
        return Lang.translate(self.time_unit)

    def _time_key(self) -> str:
        """
        Get the time key.

        :return: the time key
        """
        return self.time_unit

    def to_csv(self, file: str, put_header: bool=True) -> Path:
        """
        Store a :class:`Ecdf` record in a CSV file.

        :param file: the file to generate
        :param put_header: should we put a header with meta-data?
        :return: the fully resolved file name
        """
        path: Final[Path] = Path.path(file)
        logger(f'Writing ECDF to CSV file {path!r}.')
        with path.open_for_write() as out:
            sep: Final[str] = CSV_SEPARATOR
            if put_header:
                kv: Final[str] = KEY_VALUE_SEPARATOR
                cmt: Final[str] = COMMENT_CHAR
                if self.algorithm is not None:
                    out.write(f'{cmt} {lg.KEY_ALGORITHM}{kv}{self.algorithm}\n')
                out.write(f'{cmt} {KEY_N}{kv}{self.n}\n')
                out.write(f'{cmt} {KEY_N_INSTS}{kv}{self.n_insts}\n')
                out.write(f'{cmt} {KEY_F_NAME}{kv}{self.f_name}\n')
                if self.goal_f is not None:
                    out.write(f'{cmt} {lg.KEY_GOAL_F}{kv}{self.goal_f}\n')
            out.write(f'{self._time_key()}{sep}ecdf\n')
            for v in self.ecdf:
                out.write(f'{num_to_str(v[0])}{sep}{num_to_str(v[1])}\n')
        logger(f'Done writing ECDF to CSV file {path!r}.')
        path.enforce_file()
        return path

    @staticmethod
    def _compute_times(source: list[Progress], goal: int | float) -> list[float]:
        """
        Compute the times for the given goals.

        :param source: the source array
        :param goal: the goal value
        :return: a list of times
        """
        ret = []
        for pr in source:
            idx = _get_reach_index(pr.f, goal)
            if idx <= 0:
                continue
            ret.append(pr.time[pr.time.size - idx])
        return ret

    @staticmethod
    def _get_div(n: int, n_insts: int) -> int:
        """
        Get the divisor.

        :param n: the number of runs
        :param n_insts: the number of instances
        :return: the divisor
        """
        del n_insts
        return n

    @classmethod
    def create(cls: type['Ecdf'], source: Iterable[Progress], goal_f: int | float | Callable | None=None, use_default_goal_f: bool=True) -> 'Ecdf':
        """
        Create one single Ecdf record from an iterable of Progress records.

        :param source: the set of progress instances
        :param goal_f: the goal objective value
        :param use_default_goal_f: should we use the default lower bounds as
            goals?
        :return: the Ecdf record
        :rtype: Ecdf
        """
        if not isinstance(source, Iterable):
            raise type_error(source, 'source', Iterable)
        algorithm: str | None = None
        time_unit: str | None = None
        f_name: str | None = None
        inst_runs: dict[str, list[Progress]] = {}
        n: int = 0
        for progress in source:
            if not isinstance(progress, Progress):
                raise type_error(progress, 'progress', Progress)
            if n <= 0:
                algorithm = progress.algorithm
                time_unit = progress.time_unit
                f_name = progress.f_name
            else:
                if algorithm != progress.algorithm:
                    algorithm = None
                if time_unit != progress.time_unit:
                    raise ValueError(f'Cannot mix time units {time_unit} and {progress.time_unit}.')
                if f_name != progress.f_name:
                    raise ValueError(f'Cannot mix f-names {f_name} and {progress.f_name}.')
            n += 1
            if progress.instance in inst_runs:
                inst_runs[progress.instance].append(progress)
            else:
                inst_runs[progress.instance] = [progress]
        del source
        if n <= 0:
            raise ValueError('Did not encounter any progress information.')
        n_insts: Final[int] = len(inst_runs)
        if n_insts <= 0 or n_insts > n:
            raise ValueError('Huh?.')
        times: list[float] = []
        goal: int | float | None
        same_goal_f: int | float | None = None
        first: bool = True
        for instance, pl in inst_runs.items():
            goal = None
            if isinstance(goal_f, (int, float)):
                goal = goal_f
            elif callable(goal_f):
                goal = goal_f(instance)
            if goal is None and use_default_goal_f:
                if f_name == F_NAME_SCALED:
                    goal = 1
                elif f_name == F_NAME_NORMALIZED:
                    goal = 0
                else:
                    goal = pl[0].f_standard
                    for pp in pl:
                        if goal != pp.f_standard:
                            raise ValueError(f'Inconsistent goals: {goal} and {pp.f_standard}')
            if not isinstance(goal, (int, float)):
                raise type_error(goal, 'goal', (int, float))
            if first:
                same_goal_f = goal
            elif goal != same_goal_f:
                same_goal_f = None
            res = cls._compute_times(pl, goal)
            for t in res:
                if isfinite(t):
                    if t < 0:
                        raise ValueError(f'Invalid ert {t}.')
                    times.append(t)
                elif not t >= inf:
                    raise ValueError(f'Invalid ert {t}.')
        del inst_runs
        if len(times) <= 0:
            return cls(algorithm, n, n_insts, time_unit, f_name, same_goal_f, np.array([[0, 0], [inf, 0]]))
        times.sort()
        time: list[float] = [0]
        ecdf: list[float] = [0]
        success: int = 0
        div: Final[int] = cls._get_div(n, n_insts)
        ll: int = 0
        for t in times:
            success += 1
            if t > time[ll]:
                time.append(t)
                ecdf.append(success / div)
                ll += 1
            else:
                ecdf[ll] = success / div
        time.append(inf)
        ecdf.append(ecdf[ll])
        return cls(algorithm, n, n_insts, time_unit, f_name, same_goal_f, np.column_stack((np.array(time), np.array(ecdf))))

    @classmethod
    def from_progresses(cls: type['Ecdf'], source: Iterable[Progress], consumer: Callable[['Ecdf'], Any], f_goal: int | float | Callable | Iterable[int | float | Callable]=None, join_all_algorithms: bool=False) -> None:
        """
        Compute one or multiple ECDFs from a stream of end results.

        :param source: the set of progress instances
        :param f_goal: one or multiple goal values
        :param consumer: the destination to which the new records will be
            passed, can be the `append` method of a :class:`list`
        :param join_all_algorithms: should the Ert-Ecdf be aggregated over all
            algorithms
        """
        if not isinstance(source, Iterable):
            raise type_error(source, 'source', Iterable)
        if not callable(consumer):
            raise type_error(consumer, 'consumer', call=True)
        if not isinstance(join_all_algorithms, bool):
            raise type_error(join_all_algorithms, 'join_all_algorithms', bool)
        if not isinstance(f_goal, Iterable):
            f_goal = [f_goal]
        sorter: dict[str, list[Progress]] = {}
        for er in source:
            if not isinstance(er, Progress):
                raise type_error(er, 'progress', Progress)
            key = er.algorithm
            if key in sorter:
                lst = sorter[key]
            else:
                lst = []
                sorter[key] = lst
            lst.append(er)
        if len(sorter) <= 0:
            raise ValueError('source must not be empty')
        keyz = list(sorter.keys())
        keyz.sort()
        for goal in f_goal:
            use_default_goal = goal is None
            for key in keyz:
                consumer(cls.create(sorter[key], goal, use_default_goal))

def get_goal(ecdf: Ecdf) -> int | float | None:
    """
    Get the goal value from the given ecdf instance.

    :param Ecdf ecdf: the ecdf instance
    :return: the goal value
    """
    return ecdf.goal_f

def goal_to_str(goal_f: int | float | None) -> str:
    """
    Transform a goal to a string.

    :param goal_f: the goal value
    :return: the string representation
    """
    return 'undefined' if goal_f is None else f'goal: ≤{num_to_str(goal_f)}'