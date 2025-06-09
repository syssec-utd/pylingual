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
from pm4py.util.business_hours import BusinessHours
from pm4py.objects.log.util import sorting
from pm4py.util import constants
from pm4py.util import xes_constants as xes
from pm4py.objects.log.obj import EventLog, Trace, Event
from copy import copy
from enum import Enum
from pm4py.util import exec_utils

class Parameters(Enum):
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY
    TRANSITION_KEY = constants.PARAMETER_CONSTANT_TRANSITION_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    LIFECYCLE_INSTANCE_KEY = 'pm4py:param:lifecycle:instance:key'
    BUSINESS_HOURS = 'business_hours'
    WORKTIMING = 'worktiming'
    WEEKENDS = 'weekends'
    WORKCALENDAR = 'workcalendar'

def to_interval(log, parameters=None):
    """
    Converts a log to interval format (e.g. an event has two timestamps)
    from lifecycle format (an event has only a timestamp, and a transition lifecycle)

    Parameters
    -------------
    log
        Log (expressed in the lifecycle format)
    parameters
        Possible parameters of the method (activity, timestamp key, start timestamp key, transition ...)

    Returns
    -------------
    log
        Interval event log
    """
    if parameters is None:
        parameters = {}
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes.DEFAULT_TIMESTAMP_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, xes.DEFAULT_START_TIMESTAMP_KEY)
    transition_key = exec_utils.get_param_value(Parameters.TRANSITION_KEY, parameters, xes.DEFAULT_TRANSITION_KEY)
    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes.DEFAULT_NAME_KEY)
    lifecycle_instance_key = exec_utils.get_param_value(Parameters.LIFECYCLE_INSTANCE_KEY, parameters, xes.DEFAULT_INSTANCE_KEY)
    business_hours = exec_utils.get_param_value(Parameters.BUSINESS_HOURS, parameters, False)
    worktiming = exec_utils.get_param_value(Parameters.WORKTIMING, parameters, [7, 17])
    weekends = exec_utils.get_param_value(Parameters.WEEKENDS, parameters, [6, 7])
    if log is not None and len(log) > 0:
        if 'PM4PY_TYPE' in log.attributes and log.attributes['PM4PY_TYPE'] == 'interval':
            return log
        if log[0] is not None and len(log[0]) > 0:
            first_event = log[0][0]
            if start_timestamp_key in first_event:
                return log
        new_log = EventLog(attributes=copy(log.attributes), extensions=copy(log.extensions), classifiers=copy(log.classifiers), omni_present=copy(log.omni_present), properties=copy(log.properties))
        new_log.attributes['PM4PY_TYPE'] = 'interval'
        new_log.properties[constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY] = xes.DEFAULT_START_TIMESTAMP_KEY
        for trace in log:
            new_trace = Trace()
            for attr in trace.attributes:
                new_trace.attributes[attr] = trace.attributes[attr]
            activities_start = {}
            for event in trace:
                activity = event[activity_key]
                instance = event[lifecycle_instance_key] if lifecycle_instance_key in event else None
                activity = (activity, instance)
                transition = event[transition_key] if transition_key in event else 'complete'
                timestamp = event[timestamp_key]
                if transition.lower() == 'start':
                    if activity not in activities_start:
                        activities_start[activity] = list()
                    activities_start[activity].append(event)
                elif transition.lower() == 'complete':
                    start_event = None
                    start_timestamp = event[timestamp_key]
                    if activity in activities_start and len(activities_start[activity]) > 0:
                        start_event = activities_start[activity].pop(0)
                        start_timestamp = start_event[timestamp_key]
                    new_event = Event()
                    for attr in event:
                        if not attr == timestamp_key and (not attr == transition_key):
                            new_event[attr] = event[attr]
                    if start_event is not None:
                        for attr in start_event:
                            if not attr == timestamp_key and (not attr == transition_key):
                                new_event['@@startevent_' + attr] = start_event[attr]
                    new_event[start_timestamp_key] = start_timestamp
                    new_event[timestamp_key] = timestamp
                    new_event['@@duration'] = (timestamp - start_timestamp).total_seconds()
                    if business_hours:
                        bh = BusinessHours(start_timestamp.replace(tzinfo=None), timestamp.replace(tzinfo=None), worktiming=worktiming, weekends=weekends)
                        new_event['@@approx_bh_duration'] = bh.getseconds()
                    new_trace.append(new_event)
            new_trace = sorting.sort_timestamp_trace(new_trace, start_timestamp_key)
            new_log.append(new_trace)
        return new_log
    return log

def to_lifecycle(log, parameters=None):
    """
    Converts a log from interval format (e.g. an event has two timestamps)
    to lifecycle format (an event has only a timestamp, and a transition lifecycle)

    Parameters
    -------------
    log
        Log (expressed in the interval format)
    parameters
        Possible parameters of the method (activity, timestamp key, start timestamp key, transition ...)

    Returns
    -------------
    log
        Lifecycle event log
    """
    if parameters is None:
        parameters = {}
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes.DEFAULT_TIMESTAMP_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, xes.DEFAULT_START_TIMESTAMP_KEY)
    transition_key = exec_utils.get_param_value(Parameters.TRANSITION_KEY, parameters, xes.DEFAULT_TRANSITION_KEY)
    if log is not None and len(log) > 0:
        if 'PM4PY_TYPE' in log.attributes and log.attributes['PM4PY_TYPE'] == 'lifecycle':
            return log
        if log[0] is not None and len(log[0]) > 0:
            first_event = log[0][0]
            if transition_key in first_event:
                return log
        new_log = EventLog(attributes=copy(log.attributes), extensions=copy(log.extensions), classifiers=copy(log.classifiers), omni_present=copy(log.omni_present), properties=copy(log.properties))
        new_log.attributes['PM4PY_TYPE'] = 'lifecycle'
        for trace in log:
            new_trace = Trace()
            for attr in trace.attributes:
                new_trace.attributes[attr] = trace.attributes[attr]
            list_events = []
            for index, event in enumerate(trace):
                new_event_start = Event()
                new_event_complete = Event()
                for attr in event:
                    if not attr == timestamp_key and (not attr == start_timestamp_key):
                        new_event_start[attr] = event[attr]
                        new_event_complete[attr] = event[attr]
                new_event_start[timestamp_key] = event[start_timestamp_key]
                new_event_start[transition_key] = 'start'
                new_event_start['@@custom_lif_id'] = 0
                new_event_start['@@origin_ev_idx'] = index
                new_event_complete[timestamp_key] = event[timestamp_key]
                new_event_complete[transition_key] = 'complete'
                new_event_complete['@@custom_lif_id'] = 1
                new_event_complete['@@origin_ev_idx'] = index
                list_events.append(new_event_start)
                list_events.append(new_event_complete)
            list_events = sorted(list_events, key=lambda x: (x[timestamp_key], x['@@origin_ev_idx'], x['@@custom_lif_id']))
            for ev in list_events:
                new_trace.append(ev)
            new_log.append(new_trace)
        return new_log
    return log

def assign_lead_cycle_time(log, parameters=None):
    """
    Assigns the lead and cycle time to an interval log

    Parameters
    -------------
    log
        Interval log
    parameters
        Parameters of the algorithm, including: start_timestamp_key, timestamp_key, worktiming, weekends
    """
    if parameters is None:
        parameters = {}
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, xes.DEFAULT_TIMESTAMP_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, xes.DEFAULT_START_TIMESTAMP_KEY)
    worktiming = exec_utils.get_param_value(Parameters.WORKTIMING, parameters, [7, 17])
    weekends = exec_utils.get_param_value(Parameters.WEEKENDS, parameters, [6, 7])
    interval_log = to_interval(log, parameters=parameters)
    for trace in interval_log:
        approx_partial_lead_time = 0
        approx_partial_cycle_time = 0
        approx_wasted_time = 0
        max_et = None
        max_et_seconds = 0
        for i in range(len(trace)):
            this_wasted_time = 0
            st = trace[i][start_timestamp_key]
            st_seconds = st.timestamp()
            et = trace[i][timestamp_key]
            et_seconds = et.timestamp()
            if max_et_seconds > 0 and st_seconds > max_et_seconds:
                bh_unworked = BusinessHours(max_et.replace(tzinfo=None), st.replace(tzinfo=None), worktiming=worktiming, weekends=weekends)
                unworked_sec = bh_unworked.getseconds()
                approx_partial_lead_time = approx_partial_lead_time + unworked_sec
                approx_wasted_time = approx_wasted_time + unworked_sec
                this_wasted_time = unworked_sec
            if st_seconds > max_et_seconds:
                bh = BusinessHours(st.replace(tzinfo=None), et.replace(tzinfo=None), worktiming=worktiming, weekends=weekends)
                approx_bh_duration = bh.getseconds()
                approx_partial_cycle_time = approx_partial_cycle_time + approx_bh_duration
                approx_partial_lead_time = approx_partial_lead_time + approx_bh_duration
            elif st_seconds < max_et_seconds and et_seconds > max_et_seconds:
                bh = BusinessHours(max_et.replace(tzinfo=None), et.replace(tzinfo=None), worktiming=worktiming, weekends=weekends)
                approx_bh_duration = bh.getseconds()
                approx_partial_cycle_time = approx_partial_cycle_time + approx_bh_duration
                approx_partial_lead_time = approx_partial_lead_time + approx_bh_duration
            if et_seconds > max_et_seconds:
                max_et_seconds = et_seconds
                max_et = et
            ratio_cycle_lead_time = 1
            if approx_partial_lead_time > 0:
                ratio_cycle_lead_time = approx_partial_cycle_time / approx_partial_lead_time
            trace[i]['@@approx_bh_partial_cycle_time'] = approx_partial_cycle_time
            trace[i]['@@approx_bh_partial_lead_time'] = approx_partial_lead_time
            trace[i]['@@approx_bh_overall_wasted_time'] = approx_wasted_time
            trace[i]['@@approx_bh_this_wasted_time'] = this_wasted_time
            trace[i]['@approx_bh_ratio_cycle_lead_time'] = ratio_cycle_lead_time
    return interval_log