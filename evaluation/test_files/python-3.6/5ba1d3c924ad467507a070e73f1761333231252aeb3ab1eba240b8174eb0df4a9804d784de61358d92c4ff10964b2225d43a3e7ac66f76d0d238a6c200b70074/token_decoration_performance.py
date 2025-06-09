"""
    This file is part of PM4Py (More Info: https://pm4py.fit.fraunhofer.de).

    PM4Py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PM4Py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PM4Py.  If not, see <https://www.gnu.org/licenses/>.
"""
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.statistics.variants.log import get as variants_get
from pm4py.visualization.petri_net.common import visualize
from pm4py.visualization.petri_net.util import performance_map
from pm4py.util import exec_utils, xes_constants
from enum import Enum
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TIMESTAMP_KEY
from pm4py.objects.petri_net.obj import PetriNet, Marking
from typing import Optional, Dict, Any, Union, Tuple
from pm4py.objects.log.obj import EventLog, EventStream
import graphviz

class Parameters(Enum):
    FORMAT = 'format'
    DEBUG = 'debug'
    RANKDIR = 'set_rankdir'
    ACTIVITY_KEY = PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = PARAMETER_CONSTANT_TIMESTAMP_KEY
    AGGREGATION_MEASURE = 'aggregationMeasure'
    FONT_SIZE = 'font_size'
    STAT_LOCALE = 'stat_locale'

def get_decorations(log, net, initial_marking, final_marking, parameters=None, measure='frequency', ht_perf_method='last'):
    """
    Calculate decorations in order to annotate the Petri net

    Parameters
    -----------
    log
        Trace log
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    parameters
        Parameters associated to the algorithm
    measure
        Measure to represent on the process model (frequency/performance)
    ht_perf_method
        Method to use in order to annotate hidden transitions (performance value could be put on the last possible
        point (last) or in the first possible point (first)

    Returns
    ------------
    decorations
        Decorations to put on the process model
    """
    if parameters is None:
        parameters = {}
    aggregation_measure = exec_utils.get_param_value(Parameters.AGGREGATION_MEASURE, parameters, None)
    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes_constants.DEFAULT_NAME_KEY)
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes_constants.DEFAULT_TIMESTAMP_KEY)
    stat_locale = exec_utils.get_param_value(Parameters.STAT_LOCALE, parameters, {})
    variants_idx = variants_get.get_variants_from_log_trace_idx(log, parameters=parameters)
    variants = variants_get.convert_variants_trace_idx_to_trace_obj(log, variants_idx)
    parameters_tr = {token_replay.Variants.TOKEN_REPLAY.value.Parameters.ACTIVITY_KEY: activity_key, token_replay.Variants.TOKEN_REPLAY.value.Parameters.VARIANTS: variants}
    aligned_traces = token_replay.apply(log, net, initial_marking, final_marking, parameters=parameters_tr)
    element_statistics = performance_map.single_element_statistics(log, net, initial_marking, aligned_traces, variants_idx, activity_key=activity_key, timestamp_key=timestamp_key, ht_perf_method=ht_perf_method)
    aggregated_statistics = performance_map.aggregate_statistics(element_statistics, measure=measure, aggregation_measure=aggregation_measure, stat_locale=stat_locale)
    return aggregated_statistics

def apply(net: PetriNet, initial_marking: Marking, final_marking: Marking, log: EventLog=None, aggregated_statistics=None, parameters: Optional[Dict[Union[str, Parameters], Any]]=None) -> graphviz.Digraph:
    """
    Apply method for Petri net visualization (it calls the graphviz_visualization
    method) adding performance representation obtained by token replay

    Parameters
    -----------
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    log
        (Optional) log
    aggregated_statistics
        Dictionary containing the frequency statistics
    parameters
        Algorithm parameters (including the activity key used during the replay, and the timestamp key)

    Returns
    -----------
    viz
        Graph object
    """
    if aggregated_statistics is None:
        if log is not None:
            aggregated_statistics = get_decorations(log, net, initial_marking, final_marking, parameters=parameters, measure='performance')
    return visualize.apply(net, initial_marking, final_marking, parameters=parameters, decorations=aggregated_statistics)