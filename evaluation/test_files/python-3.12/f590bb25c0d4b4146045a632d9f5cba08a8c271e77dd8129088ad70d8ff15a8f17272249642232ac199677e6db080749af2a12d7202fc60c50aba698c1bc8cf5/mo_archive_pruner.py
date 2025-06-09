"""Functions for testing multi-objective archive pruners."""
from typing import Final, List, Iterable, Optional, Callable
import numpy as np
from numpy.random import Generator, default_rng
from moptipy.api.mo_archive import MOArchivePruner, check_mo_archive_pruner, MORecord
from moptipy.api.mo_problem import MOProblem
from moptipy.mock.mo_problem import MockMOProblem
from moptipy.tests.component import validate_component
from moptipy.utils.nputils import DEFAULT_NUMERICAL
from moptipy.utils.types import type_error

def __run_single_test(pruner_factory: Callable[[MOProblem], MOArchivePruner], random: Generator, dim: int, dt: np.dtype) -> bool:
    """
    Run a single test.

    :param pruner_factory: the factory for creating pruners
    :param random: the random number generator
    :param dim: the dimension
    :param dt: the data type
    :returns: `True` if a test was run, `False` if we need to try again
    """
    mop: Final[MockMOProblem] = MockMOProblem.for_dtype(dim, dt)
    if not isinstance(mop, MockMOProblem):
        raise type_error(mop, 'new mock problem', MockMOProblem)
    tag: Final[str] = f'bla{random.integers(100)}'
    pruner = pruner_factory(mop)
    if not isinstance(pruner, MOArchivePruner):
        raise type_error(pruner, 'pruner', MOArchivePruner)
    check_mo_archive_pruner(pruner)
    validate_component(pruner)
    alen = int(random.integers(2, 10))
    if not isinstance(alen, int):
        raise type_error(alen, 'alen', int)
    amax = int(random.integers(1, alen + 1))
    if not isinstance(amax, int):
        raise type_error(amax, 'amax', int)
    if not 0 < amax <= alen <= 10:
        raise ValueError(f'invalid amax={amax} and alen={alen}.')
    dim_mode = [False]
    if dim > 1:
        dim_mode.append(True)
    for use_collapse in dim_mode:
        archive: List[MORecord] = []
        archivec: List[MORecord] = []
        collapse_dim: int = -1
        if use_collapse:
            collapse_dim = random.integers(dim)
        max_samples: int = 10000
        for _ in range(alen):
            needed: bool = True
            rec: Optional[MORecord] = None
            fs: Optional[np.ndarray] = None
            while needed:
                max_samples -= 1
                if max_samples <= 0:
                    return False
                fs = np.empty(dim, dt)
                if not isinstance(fs, np.ndarray):
                    raise type_error(fs, 'fs', np.ndarray)
                if len(fs) != dim:
                    raise ValueError(f'len(fs)={len(fs)}!=dim={dim}')
                mop.sample(fs)
                rec = MORecord(tag, fs)
                if not isinstance(rec, MORecord):
                    raise type_error(rec, 'rec', MORecord)
                needed = False
                for z in archive:
                    fs2 = z.fs
                    if np.array_equal(fs, fs2):
                        needed = True
                        break
            if rec is None or fs is None:
                raise ValueError('huh?')
            archive.append(rec)
            rec2 = MORecord(tag, fs.copy())
            if rec.x != rec2.x or not np.array_equal(rec2.fs, rec.fs):
                raise ValueError(f'{rec} != {rec2}')
            archivec.append(rec2)
        if not isinstance(archive, List):
            raise type_error(archive, 'archive', List)
        if not isinstance(archivec, List):
            raise type_error(archivec, 'archivec', List)
        thelen: int = len(archive)
        if not isinstance(thelen, int):
            raise type_error(thelen, 'len(archive)', int)
        if thelen != alen:
            raise ValueError(f'{alen} != len(archive)={len(archive)}?')
        if use_collapse:
            collapse_value = archive[random.integers(alen)].fs[collapse_dim]
            for rec in archive:
                rec.fs[collapse_dim] = collapse_value
            for rec in archivec:
                rec.fs[collapse_dim] = collapse_value
        pruner.prune(archive, amax, len(archive))
        thelen = len(archive)
        if not isinstance(thelen, int):
            raise type_error(thelen, 'len(archive)', int)
        if thelen != alen:
            raise ValueError(f'pruning messed up archive len: {alen} != len(archive)={len(archive)}?')
        for ii, a in enumerate(archive):
            if not isinstance(a, MORecord):
                raise type_error(a, f'archive[{ii}]', MORecord)
            for j in range(ii):
                if archive[j] is a:
                    raise ValueError(f'record {a} appears at indexes {ii} and {j}!')
            if a.x != tag:
                raise ValueError(f"a.x={a.x}!='{tag}'")
            if not isinstance(a.fs, np.ndarray):
                raise type_error(a.fs, 'a.fs', np.ndarray)
            if not use_collapse:
                for idx, b in enumerate(archivec):
                    if np.array_equal(a.fs, b.fs):
                        if a.x != b.x:
                            raise ValueError(f'a.fs={a.fs}==b.fs, but a.x={a.x}!=b.x={b.x}')
                        del archivec[idx]
                        break
    return True

def validate_mo_archive_pruner(pruner_factory: Callable[[MOProblem], MOArchivePruner], dimensions: Iterable[int], dtypes: Iterable[np.dtype]=DEFAULT_NUMERICAL) -> None:
    """
    Check whether an object is a moptipy multi-objective optimization pruner.

    This method checks whether the class is correct and whether the pruning
    follows the general contract: Interesting records in the list to be pruned
    are moved to the front, the ones to discard are moved to the back. No
    record is lost and none is duplicated.

    :param pruner_factory: the creator for the multi-objective archive pruner
        to test
    :param dimensions: the dimensions to simulate
    :param dtypes: the dtypes to test on
    :raises ValueError: if `mo_problem` is not a valid
        :class:`~moptipy.api.mo_problem.MOProblem`
    :raises TypeError: if values of the wrong types are encountered
    """
    if not callable(pruner_factory):
        raise type_error(pruner_factory, 'pruner_factory', call=True)
    if not isinstance(dimensions, Iterable):
        raise type_error(dimensions, 'dimensions', Iterable)
    if not isinstance(dtypes, Iterable):
        raise type_error(dtypes, 'dtypes', Iterable)
    nothing: bool = True
    random: Final[Generator] = default_rng()
    for dim in dimensions:
        if not isinstance(dim, int):
            raise type_error(dim, 'dimensions[i]', int)
        nothing = False
        for dt in dtypes:
            if not isinstance(dt, np.dtype):
                raise type_error(dt, 'dt', np.dtype)
            while not __run_single_test(pruner_factory, random, dim, dt):
                pass
    if nothing:
        raise ValueError('dimensions are empty!')