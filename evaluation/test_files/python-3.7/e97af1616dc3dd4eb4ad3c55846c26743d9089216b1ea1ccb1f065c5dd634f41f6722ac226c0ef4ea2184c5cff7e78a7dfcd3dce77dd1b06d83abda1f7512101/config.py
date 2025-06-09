from grid2op.Reward import RedispReward
from grid2op.Rules import DefaultRules
from grid2op.Chronics import Multifolder
from grid2op.Chronics import GridStateFromFileWithForecastsWithMaintenance
from grid2op.Backend import PandaPowerBackend
try:
    from grid2op.l2rpn_utils import ActionWCCI2020, ObservationWCCI2020
except ImportError:
    from grid2op.Action import TopologyAndDispatchAction
    from grid2op.Observation import CompleteObservation
    import warnings
    warnings.warn('The grid2op version you are trying to use is too old for this environment. Please upgrade it.')
    ActionWCCI2020 = TopologyAndDispatchAction
    ObservationWCCI2020 = CompleteObservation
config = {'backend': PandaPowerBackend, 'action_class': ActionWCCI2020, 'observation_class': ObservationWCCI2020, 'reward_class': RedispReward, 'gamerules_class': DefaultRules, 'chronics_class': Multifolder, 'grid_value_class': GridStateFromFileWithForecastsWithMaintenance, 'volagecontroler_class': None, 'names_chronics_to_grid': {}, 'thermal_limits': [43.3, 205.2, 341.2, 204.0, 601.4, 347.1, 319.6, 301.4, 330.3, 274.1, 307.4, 172.3, 354.3, 127.9, 174.9, 152.6, 81.8, 204.3, 561.5, 561.5, 98.7, 179.8, 193.4, 239.9, 164.8, 100.4, 125.7, 278.2, 274.0, 89.9, 352.1, 157.1, 124.4, 154.6, 86.1, 106.7, 148.5, 129.6, 136.1, 86.0, 313.2, 198.5, 599.1, 206.8, 233.7, 395.8, 516.7, 656.4, 583.0, 583.0, 263.1, 222.6, 322.8, 340.6, 305.2, 360.1, 395.8, 274.2, 605.5]}