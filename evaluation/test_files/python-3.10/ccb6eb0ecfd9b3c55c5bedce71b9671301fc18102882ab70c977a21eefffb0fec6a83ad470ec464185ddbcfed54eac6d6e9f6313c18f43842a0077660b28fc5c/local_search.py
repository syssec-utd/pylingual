import collections
import logging
import math
import random
import time
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Callable, Type, Sequence, TypeVar, Generic
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sensai.util.aggregation import RelativeFrequencyCounter
log = logging.getLogger(__name__)

class SATemperatureSchedule(ABC):
    """
    Describes how temperature changes as the annealing process goes on.
    The function maps a degree of completion (in the interval from 0 to 1) to a temperature value.
    """

    @abstractmethod
    def temperature(self, degreeOfCompletion):
        """
        Computes the temperature for a degree of completion in [0, 1]
        :param degreeOfCompletion: the degree to which the simulated annealing process has completed in [0, 1]
        :return: the temperature
        """
        pass

    def probability(self, degreeOfCompletion, costDelta):
        T = self.temperature(degreeOfCompletion)
        p = math.exp(-costDelta / T) if T > 0.0 else 0.0
        return (p, T)

    @abstractmethod
    def _getParams(self):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}{self._getParams()}'

class SATemperatureScheduleFixed(SATemperatureSchedule):
    """A schedule with a constant temperature"""

    def __init__(self, t):
        self.t = t

    def temperature(self, degreeOfCompletion):
        return self.t

    def _getParams(self):
        return {'fixedTemp': self.t}

class SATemperatureScheduleExponential(SATemperatureSchedule):
    """ A temperature schedule for simulated annealing where the temperature drops exponentially. """

    def __init__(self, t0, t1, exponentFactor):
        """
        :param t0: temperature at the beginning (degree of completion 0)
        :param t1: temperature at the end (degree of completion 1), which must be smaller than t0 and larger than 0
        :param exponentFactor: factor with which to multiply the exponent (the larger the factor, the faster the temperature drops)
        """
        super().__init__()
        if t1 > t0 or t0 <= 0:
            raise ValueError('Inadmissible temperatures given.')
        if exponentFactor < 1:
            raise ValueError('The exponent factor cannot be less than 1.')
        self.t0 = t0
        self.t1 = t1
        self.tDrop = t0 - t1
        self.exponentFactor = exponentFactor

    def temperature(self, degreeOfCompletion):
        return self.t0 - self.tDrop * (1.0 - math.exp(-self.exponentFactor * degreeOfCompletion))

    def _getParams(self):
        return {'t0': self.t0, 't1': self.t1, 'expFactor': self.exponentFactor}

def reverseSigmoid(degreeOfCompletion, v0, v1, steepness, midDegree=0.5):
    return v0 - (v0 - v1) / (1.0 + math.exp(-steepness * (degreeOfCompletion - midDegree)))

class SATemperatureScheduleReverseSigmoid(SATemperatureSchedule):
    """A temperature schedule for simulated annealing where the temperature drops in a reverse sigmoid curve (based on the logistic function)"""

    def __init__(self, t0, t1, steepness, midDegree=0.5):
        """
        :param t0: temperature at the beginning (degree of completion 0)
        :param t1: temperature at the end (degree of completion 1), which must be smaller than t0 and larger than 0
        :param steepness: Factor which roughly corresponds to the (negative) slope at the inflection point 0.5.
            For the sigmoid shape to be sufficiently pronounced, a value of at least 5 is recommended (the closer the value is to 1,
            the more the curve approaches a linear decay).
        :param midDegree: the degree of completion at which the function shall return the temperature (t0+t1)/2
        """
        super().__init__()
        if t1 > t0 or t0 <= 0:
            raise ValueError('Inadmissible temperatures given.')
        if midDegree < 0 or midDegree > 1:
            raise Exception('Mid-degree must be between 0 and 1')
        self.t0 = t0
        self.t1 = t1
        self.steepness = steepness
        self.midDegree = midDegree

    def temperature(self, degreeOfCompletion):
        return reverseSigmoid(degreeOfCompletion, self.t0, self.t1, self.steepness, self.midDegree)

    def _getParams(self):
        return {'t0': self.t0, 't1': self.t1, 'steepness': self.steepness, 'midDegree': self.midDegree}

class SATemperatureScheduleReverseSigmoidSymmetric(SATemperatureScheduleReverseSigmoid):
    """
    A variant of the logistic schedule with a reverse sigmoid shape, where the probability of acceptance for a given assumed positive
    cost delta is symmetric. "Symmetric" here means that half the schedule is to be above 0.5 and half of it below 0.5.
    """

    def __init__(self, t0, t1, steepness, costDeltaForSymmetry):
        """
        :param t0: temperature at the beginning (degree of completion 0)
        :param t1: temperature at the end (degree of completion 1), which must be smaller than t0 and larger than 0
        :param steepness: Factor which roughly corresponds to the (negative) slope at the inflection point 0.5.
            For the sigmoid shape to be sufficiently pronounced, a value of at least 8 is recommended (the closer the value is to 1,
            the more the curve approaches a linear decay).
        :param costDeltaForSymmetry: the (positive) cost delta value which the curve shall be "symmetric"
        """
        k = steepness
        cdelta = costDeltaForSymmetry
        midDegree = -(2 * math.log(-(13614799 * t0 - 19642003 * cdelta) / (13614799 * t1 - 19642003 * cdelta)) - k) / (2 * k)
        super().__init__(t0, t1, steepness, midDegree)

class SATemperatureSchedulePower(SATemperatureSchedule):
    """
    A temperature schedule for simulated annealing where the temperature drops with powers of the degree of completion d,
    i.e. the temperature drop is proportional to d to the power of e for a given exponent e.
    """

    def __init__(self, t0, t1, exponent):
        """
        :param t0: temperature at the beginning (degree of completion 0)
        :param t1: temperature at the end (degree of completion 1), which must be smaller than t0 and larger than 0
        :param exponent: the exponent of the power function
        """
        super().__init__()
        if t1 > t0 or t0 <= 0:
            raise ValueError('Inadmissible temperatures given.')
        self.t0 = t0
        self.t1 = t1
        self.tDrop = t0 - t1
        self.exponent = exponent

    def temperature(self, degreeOfCompletion):
        return self.t0 - self.tDrop * math.pow(degreeOfCompletion, self.exponent)

    def _getParams(self):
        return {'t0': self.t0, 't1': self.t1, 'exponent': self.exponent}

class SAProbabilityFunction(ABC):

    def __init__(self, **paramsDict):
        self.paramsDict = paramsDict

    def __str__(self):
        return f'{self.__class__.__name__}{self.paramsDict}'

    @abstractmethod
    def __call__(self, degreeOfCompletion):
        pass

class SAProbabilityFunctionLinear(SAProbabilityFunction):
    """A probability function where probabilities decay linearly"""

    def __init__(self, p0=1.0, p1=0.0):
        super().__init__(p0=p0, p1=p1)
        self.p0 = p0
        self.p1 = p1

    def __call__(self, degreeOfCompletion):
        return self.p0 - degreeOfCompletion * (self.p0 - self.p1)

class SAProbabilityFunctionReverseSigmoid(SAProbabilityFunction):
    """A probability function where probabilities decay in a reverse sigmoid shape"""

    def __init__(self, p0=1.0, p1=0.0, steepness=10):
        """
        :param p0: the probability at the beginning (degree of completion 0)
        :param p1: the probability at the end (degree of completion 1)
        :param steepness: the steepness of the sigmoid curve
        """
        super().__init__(p0=p0, p1=p1, steepness=steepness)
        self.p0 = p0
        self.p1 = p1
        self.steepness = steepness

    def __call__(self, degreeOfCompletion):
        return reverseSigmoid(degreeOfCompletion, self.p0, self.p1, self.steepness)

class SAProbabilityFunctionConstant(SAProbabilityFunction):
    """A constant probability function (which returns the same probability for all degrees of completion)"""

    def __init__(self, p):
        super().__init__(p=p)
        self.p = p

    def __call__(self, degreeOfCompletion):
        return self.p

class SAProbabilitySchedule(SATemperatureSchedule):
    """
    A temperature schedule where temperatures are derived from a probability schedule that is to apply to a reference cost delta, which
    is either given or is computed from observed values (the latter resulting in an adaptive schedule).
    It converts a function that returns probabilities for degrees of completion into a corresponding temperature schedule.
    """

    def __init__(self, referenceCostDelta: Optional[float], probabilityFunction: SAProbabilityFunction):
        """
        Creates a temperature schedule for a reference cost delta (which can also be computed automatically from observed data)
        and probability function:
        The schedule will return temperatures such that for referenceCostDelta, the probability of acceptance of a move at
        degree of completion d in [0,1] will be probabilityFunction(d).

        :param referenceCostDelta: the (positive) cost delta for which the probability function is to apply;
            if None, adaptively determine it from the empirical mean
        :param probabilityFunction: a function which maps degrees of completion in [0,1] to probabilities in [0,1]
        """
        self.adaptive = referenceCostDelta is None
        self.referenceCostDelta = referenceCostDelta
        self.probabilityFunction = probabilityFunction
        self.paramsDict = {'refCostDelta': referenceCostDelta if referenceCostDelta is not None else 'adaptive', 'probabilityFunction': str(probabilityFunction)}
        self._costDeltaSum = 0
        self._costDeltaCount = 0

    def temperature(self, degreeOfCompletion):
        if self.adaptive and self._costDeltaCount == 0:
            raise Exception('Cannot generate a temperature from an adaptive schedule without any previous cost-delta samples')
        p = self.probabilityFunction(degreeOfCompletion)
        if p == 0.0:
            return 0
        else:
            return -self.referenceCostDelta / math.log(p)

    def probability(self, degreeOfCompletion, costDelta):
        if self.adaptive:
            self._costDeltaSum += costDelta
            self._costDeltaCount += 1
            self.referenceCostDelta = max(self._costDeltaSum / self._costDeltaCount, 1e-10)
        return super().probability(degreeOfCompletion, costDelta)

    def _getParams(self):
        return self.paramsDict

class SACostValue(ABC):
    """Representation of an immutable cost value"""

    @abstractmethod
    def value(self):
        """Returns the numeric cost value"""
        pass

    @abstractmethod
    def add(self, other) -> 'SACostValue':
        pass

class SACostValueNumeric(SACostValue):

    def __init__(self, scalar):
        self._value = scalar

    def __str__(self):
        return str(self.value())

    def value(self):
        return self._value

    def add(self, other: 'SACostValueNumeric') -> 'SACostValueNumeric':
        return SACostValueNumeric(self._value + other._value)

class SAState(ABC):
    """Represents the state/variable assignment during a simulated annealing process"""

    def __init__(self, r: random.Random):
        self.r = r
        self.cost = self.computeCostValue()

    @abstractmethod
    def computeCostValue(self) -> SACostValue:
        """Computes the costs of this state (from scratch)"""
        pass

    @abstractmethod
    def getStateRepresentation(self):
        """
        Returns a compact state representation (for the purpose of archiving a hitherto best result), which can later be
        applied via applyStateRepresentation.

        :return: a compact state representation of some sort
        """
        pass

    @abstractmethod
    def applyStateRepresentation(self, representation):
        """
        Applies the given state representation (as returned via `getStateRepresentation`) in order for the optimisation result to
        be obtained by the user.
        Note that the function does not necessarily need to change this state to reflect the representation, as its sole
        purpose is for the optimsation result to be obtainable thereafter (it is not used during the optimisation process as such).

        :param representation: a representation as returned by `getStateRepresentation`
        """
        pass
TSAState = TypeVar('TSAState', bound=SAState)

class SAOperator(Generic[TSAState]):
    """
    An operator which, when applied with appropriately chosen parameters, can transform a state into another
    state during simulated annealing
    """

    def __init__(self, state: TSAState):
        """
        :param state: the state to which the operator is applied
        """
        self.state = state

    def applyCostChange(self, costDelta: SACostValue):
        """
        Applies the cost change to the state given at construction

        :param costDelta: the cost change to apply
        """
        self.state.cost = self.state.cost.add(costDelta)

    @abstractmethod
    def applyStateChange(self, *params):
        """
        Applies the operator to the state, i.e. it makes the changes to the state only
        (and does not update the associated costs)

        :param params: the parameters with which the operator is to be applied
        :return:
        """
        pass

    def apply(self, params: Tuple, costDelta: SACostValue):
        """
        Applies the operator to the state given at construction, changing the state and updating the costs appropriately

        :param params: the parameters with which the operator is to be applied
        :param costDelta: the cost change that results from the application
        :return:
        """
        self.applyCostChange(costDelta)
        self.applyStateChange(*params)

    @abstractmethod
    def costDelta(self, *params) -> SACostValue:
        """
        Computes the cost change that would apply when applying this operator with the given parameters

        :param params: an arbitrary list of parameters (specific to the concrete operator)
        :return:
        """
        pass

    @abstractmethod
    def chooseParams(self) -> Optional[Tuple[Tuple, Optional[SACostValue]]]:
        """
        Chooses parameters for the application of the operator (e.g. randomly or greedily).

        :return: a tuple (params, costValue) or None if no suitable parameters are found, where params is the list of chosen
            parameters and costValue is either an instance of CostValue or None if the costs have not been computed.
        """
        pass

class SAChain(Generic[TSAState]):
    """Manages the progression of one state during simulated annealing"""
    log = log.getChild(__qualname__)

    def __init__(self, stateFactory: Callable[[random.Random], TSAState], schedule: SATemperatureSchedule, opsAndWeights: Sequence[Tuple[Callable[[TSAState], SAOperator[TSAState]], float]], randomSeed, collectStats=False):
        self.schedule = schedule
        self.r = random.Random(randomSeed)
        self.state = stateFactory(self.r)
        self.collectStats = collectStats
        (operators, weights) = zip(*opsAndWeights)
        (cumWeights, s) = ([], 0)
        for weight in weights:
            s += weight
            cumWeights.append(s)
        self.ops = [cons(self.state) for cons in operators]
        self.opCumWeights = cumWeights
        self.stepsTaken = 0
        self.countNoneParams = 0
        self.countBestUpdates = -1
        self.bestCost = None
        self.bestStateRepr = None
        self.loggedSeries = collections.defaultdict(lambda : [])
        self._updateBestState()
        if self.collectStats:
            self.operatorInapplicabilityCounters = {}
            for op in self.ops:
                self.operatorInapplicabilityCounters[op] = RelativeFrequencyCounter()

    def _updateBestState(self):
        cost = self.state.cost
        if self.bestCost is None or cost.value() < self.bestCost.value():
            self.bestCost = cost
            self.bestStateRepr = self.state.getStateRepresentation()
            self.countBestUpdates += 1

    def step(self, degreeOfCompletion):
        r = self.r
        op = r.choices(self.ops, cum_weights=self.opCumWeights, k=1)[0]
        paramChoice = op.chooseParams()
        if paramChoice is None:
            self.countNoneParams += 1
        else:
            (params, costChange) = paramChoice
            if costChange is None:
                costChange = op.costDelta(*params)
            if costChange.value() < 0:
                makeMove = True
            else:
                costChangeValue = costChange.value()
                (p, T) = self.schedule.probability(degreeOfCompletion, costChangeValue)
                makeMove = r.random() <= p
                self.log.debug(f'p: {p}, T: {T}, costDelta: {costChangeValue}, move: {makeMove}')
                if self.collectStats:
                    self.loggedSeries['temperatures'].append(T)
                    self.loggedSeries['probabilities'].append(p)
            if makeMove:
                op.apply(params, costChange)
                self._updateBestState()
            if self.collectStats:
                self.loggedSeries['costDeltas'].append(costChange.value())
        if self.collectStats:
            self.loggedSeries['bestCostValues'].append(self.bestCost.value())
            self.loggedSeries['costValues'].append(self.state.cost.value())
            self.operatorInapplicabilityCounters[op].count(paramChoice is None)
        self.stepsTaken += 1
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug(f'Step {self.stepsTaken}: cost={self.state.cost}; best cost={self.bestCost}')

    def logStats(self):
        if self.collectStats:
            stats = {'useless moves total (None params)': f'{self.countNoneParams}/{self.stepsTaken}'}
            for (op, counter) in self.operatorInapplicabilityCounters.items():
                stats[f'useless moves of {op}'] = str(counter)
            loggedCostDeltas = self.loggedSeries['costDeltas']
            if loggedCostDeltas:
                stats['mean cost delta'] = f'{np.mean(loggedCostDeltas):.3f} +- {np.std(loggedCostDeltas):.3f}'
                absCostDeltas = np.abs(loggedCostDeltas)
                stats['mean absolute cost delta'] = f'{np.mean(absCostDeltas):.3f} +- {np.std(absCostDeltas):.3f}'
                positiveCostDeltas = [cd for cd in loggedCostDeltas if cd > 0]
                if positiveCostDeltas:
                    stats['positive cost delta'] = f'mean={np.mean(positiveCostDeltas):.3f} +- {np.std(positiveCostDeltas):.3f}, max={np.max(positiveCostDeltas):.3f}'
            statsJoin = '\n    '
            self.log.info(f"Stats: {statsJoin.join([key + ': ' + value for (key, value) in stats.items()])}")
        self.log.info(f'Best solution has {self.bestCost} after {self.countBestUpdates} updates of best state')

    def applyBestState(self):
        """Applies the best state representation found in this chain to the chain's state"""
        self.state.applyStateRepresentation(self.bestStateRepr)
        self.state.cost = self.bestCost

    def plotSeries(self, seriesName):
        """
        Plots one of the logged series

        :param seriesName: the name of the series (see getSeries)
        """
        series = self.getSeries(seriesName)
        plt.figure()
        series.plot(title=seriesName)

    def getSeries(self, seriesName):
        """
        Gets one of the logged series (for collectStats==True)

        :param seriesName: name of the series: one of "temperatures", "probabilities", "costDeltas", "bestCostValues", "costValues
        """
        if not self.collectStats:
            raise Exception('No stats were collected')
        if seriesName not in self.loggedSeries:
            raise Exception('Unknown series')
        return pd.Series(self.loggedSeries[seriesName])

class SimulatedAnnealing(Generic[TSAState]):
    """
    The simulated annealing algorithm for discrete optimisation (cost minimisation)
    """
    log = log.getChild(__qualname__)

    def __init__(self, scheduleFactory: Callable[[], SATemperatureSchedule], opsAndWeights: Sequence[Tuple[Callable[[TSAState], SAOperator[TSAState]], float]], maxSteps: int=None, duration: float=None, randomSeed=42, collectStats=False):
        """
        :param scheduleFactory: a factory for the creation of the temperature schedule for the annealing process
        :param opsAndWeights: a list of operator factories with associated weights, where weights are to indicate the (non-normalised) probability of choosing the associated operator
        :param maxSteps: the number of steps for which to run the optimisation; may be None (if not given, duration must be provided)
        :param duration: the duration, in seconds, for which to run the optimisation; may be None (if not given, maxSteps must be provided)
        :param randomSeed: the random seed to use for all random choices
        :param collectStats: flag indicating whether to collect additional statics which will be logged
        """
        if maxSteps is not None and maxSteps <= 0:
            raise ValueError('The number of iterations should be greater than 0.')
        if maxSteps is None and duration is None or (maxSteps is not None and duration is not None):
            raise ValueError('Exactly one of {maxSteps, duration} must be specified.')
        if duration is not None and duration <= 0:
            raise ValueError('Duration must be greater than 0 if provided')
        self.scheduleFactory = scheduleFactory
        self.maxSteps = maxSteps
        self.duration = duration
        self.randomSeed = randomSeed
        self.opsAndWeights = opsAndWeights
        self.collectStats = collectStats
        self._chain = None

    def optimise(self, stateFactory: Callable[[random.Random], TSAState]) -> TSAState:
        """
        Applies the annealing process, starting with a state created via the given factory.

        :param stateFactory: the factory with which to create the (initial) state
        :return: the state with the least-cost representation found during the optimisation applied
        """
        chain = SAChain(stateFactory, self.scheduleFactory(), opsAndWeights=self.opsAndWeights, randomSeed=self.randomSeed, collectStats=self.collectStats)
        self.log.info(f"Running simulated annealing with {len(self.opsAndWeights)} operators for {('%d steps' % self.maxSteps if self.maxSteps is not None else '%d seconds' % self.duration)} ...")
        startTime = time.time()
        while True:
            timeElapsed = time.time() - startTime
            if self.maxSteps is not None and chain.stepsTaken >= self.maxSteps or (self.duration is not None and timeElapsed >= self.duration):
                break
            if self.maxSteps is not None:
                degreeOfCompletion = chain.stepsTaken / self.maxSteps
            else:
                degreeOfCompletion = timeElapsed / self.duration
            chain.step(degreeOfCompletion)
        self.log.info(f'Simulated annealing completed after {time.time() - startTime:.1f} seconds, {chain.stepsTaken} steps')
        chain.logStats()
        chain.applyBestState()
        if self.collectStats:
            self._chain = chain
        return chain.state

    def getChain(self) -> Optional[SAChain[TSAState]]:
        """
        Gets the chain used by the most recently completed application (optimise call) of this object
        for the case where stats collection was enabled; the chain then contains relevant series and may be used
        to generate plots. If stats collection was not enabled, returns None.
        """
        return self._chain

class ParallelTempering(Generic[TSAState]):
    """
    The parallel tempering algorithm for discrete optimisation (cost minimisation)
    """
    log = log.getChild(__qualname__)

    def __init__(self, numChains, opsAndWeights: Sequence[Tuple[Callable[[TSAState], SAOperator[TSAState]], float]], schedule: SATemperatureSchedule=None, probabilityFunction: SAProbabilityFunction=None, maxSteps: int=None, duration: float=None, randomSeed=42, logCostProgression=False):
        """
        Creates a parallel tempering optimiser with the given number of chains and operators for each chain.
        To determine the schedule to use for each chain, either schedule or probabilityFunction must be provided.
        It is usually more robust to use adaptive schedules and therefore to provide probabilityFunction.

        :param numChains: the number of parallel chains
        :param opsAndWeights: a list of operators with associated weights (which are to indicate the non-normalised probability of chosing the associated operator)
        :param schedule: the temperature schedule from which numChains temperatures of chains are drawn (using equidistant degrees of completion); if None, must provide probabilityFunction
        :param probabilityFunction: the probability function from which numChains probabilities for adaptive probability schedules, each using a constant probability, are to be drawn; if None, must provide schedule
        :param maxSteps: the number of steps for which to run the optimisation; may be None (if not given, duration must be provided)
        :param duration: the duration, in seconds, for which to run the optimisation; may be None (if not given, maxSteps must be provided)
        :param randomSeed: the random seed to use for all random choices
        :param logCostProgression: whether to log cost progression of all chains (such that it can be plotted after the fact via plotCostProgression)
        """
        if maxSteps is not None and maxSteps <= 0:
            raise ValueError('The number of iterations should be greater than 0.')
        if maxSteps is None and duration is None or (maxSteps is not None and duration is not None):
            raise ValueError('Exactly one of {maxSteps, duration} must be specified.')
        if duration is not None and duration <= 0:
            raise ValueError('duration should be greater than 0 if provided.')
        if numChains < 2:
            raise ValueError('Number of chains must be at least 2.')
        if schedule is None and probabilityFunction is None or (schedule is not None and probabilityFunction is not None):
            raise ValueError('Exactly one of {schedule, probabilityFunction} must be given')
        self.maxSteps = maxSteps
        self.duration = duration
        self.randomSeed = randomSeed
        self.numChains = numChains
        self.baseSchedule = schedule
        self.baseProbabilityFunction = probabilityFunction
        self.opsAndWeights = opsAndWeights
        self.logCostProgression = logCostProgression
        self._costProgressions = None
        self._scheduleParamStrings = None

    def _createSchedules(self):
        degreeStep = 1.0 / (self.numChains - 1)
        degreesOfCompletion = [i * degreeStep for i in range(self.numChains)]
        if self.baseSchedule is not None:
            temperatures = [self.baseSchedule.temperature(d) for d in degreesOfCompletion]
            self._scheduleParamStrings = ['T=%.2f' % t for t in temperatures]
            return [SATemperatureScheduleFixed(t) for t in temperatures]
        else:
            probabilities = [self.baseProbabilityFunction(d) for d in degreesOfCompletion]
            self._scheduleParamStrings = ['p=%.3f' % p for p in probabilities]
            return [SAProbabilitySchedule(None, SAProbabilityFunctionConstant(p)) for p in probabilities]

    def optimise(self, stateFactory: Callable[[random.Random], SAState]) -> SAState:
        """
        Applies the optimisation process, starting, in each chain, with a state created via the given factory.

        :param stateFactory: the factory with which to create the states for all chains
        :return: the state with the least-cost representation found during the optimisation (among all parallel chains) applied
        """
        self.log.info(f"Running parallel tempering with {self.numChains} chains, {len(self.opsAndWeights)} operators for {('%d steps' % self.maxSteps if self.maxSteps is not None else '%d seconds' % self.duration)} ...")
        r = random.Random(self.randomSeed)
        chains = []
        costProgressions = []
        for (i, schedule) in enumerate(self._createSchedules(), start=1):
            self.log.info(f'Chain {i} uses {schedule}')
            chains.append(SAChain(stateFactory, schedule, opsAndWeights=self.opsAndWeights, randomSeed=r.randint(0, 1000)))
            costProgressions.append([])
        startTime = time.time()
        step = 0
        numChainSwaps = 0
        while True:
            timeElapsed = time.time() - startTime
            if self.maxSteps is not None and step > self.maxSteps or (self.duration is not None and timeElapsed > self.duration):
                break
            degreeOfCompletion = step / self.maxSteps if self.maxSteps is not None else timeElapsed / self.duration
            for chain in chains:
                chain.step(degreeOfCompletion)
            for idxHighTempChain in range(0, self.numChains - 1):
                idxLowTempChain = idxHighTempChain + 1
                highTempChain = chains[idxHighTempChain]
                lowTempChain = chains[idxLowTempChain]
                if highTempChain.state.cost.value() < lowTempChain.state.cost.value():
                    (highTempChain.schedule, lowTempChain.schedule) = (lowTempChain.schedule, highTempChain.schedule)
                    chains[idxLowTempChain] = highTempChain
                    chains[idxHighTempChain] = lowTempChain
                    numChainSwaps += 1
            if self.logCostProgression:
                for (idxChain, chain) in enumerate(chains):
                    costProgressions[idxChain].append(chain.state.cost.value())
            step += 1
        self.log.info(f'Number of chain swaps: {numChainSwaps}')
        if self.logCostProgression:
            self._costProgressions = costProgressions
        bestChainIdx = int(np.argmin([chain.bestCost.value() for chain in chains]))
        chains[bestChainIdx].applyBestState()
        return chains[bestChainIdx].state

    def plotCostProgression(self):
        if not self.logCostProgression or self._costProgressions is None:
            raise Exception('No cost progression was logged')
        series = {}
        for (scheduleParamStr, costProgression) in zip(self._scheduleParamStrings, self._costProgressions):
            series[scheduleParamStr] = costProgression
        plt.figure()
        pd.DataFrame(series).plot()