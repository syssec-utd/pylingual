""" Check if the unit has a dimension that matches pressure"""
from timeseer import AnalysisInput, AnalysisResult
from timeseer.analysis.utils.unit_dimension_match import unit_not_matching_dimension
_CHECK_NAME = 'pressure unit dimension'
_EVENT_FRAME_NAME = 'Unit not matching pressure'
META = {'checks': [{'name': _CHECK_NAME, 'event_frames': [_EVENT_FRAME_NAME], 'data_type': 'bool'}], 'conditions': [{'min_series': 1, 'min_data_points': 1}], 'signature': 'univariate'}

def run(analysis_input: AnalysisInput) -> AnalysisResult:
    parameters = {}
    parameters['value'] = '[pressure]'
    analysis_input.parameters = parameters
    analysis_result = unit_not_matching_dimension.run(analysis_input)
    event_frames = []
    for event_frame in analysis_result.event_frames:
        event_frame.type = _EVENT_FRAME_NAME
        event_frames.append(event_frame)
    analysis_result.event_frames = event_frames
    return analysis_result