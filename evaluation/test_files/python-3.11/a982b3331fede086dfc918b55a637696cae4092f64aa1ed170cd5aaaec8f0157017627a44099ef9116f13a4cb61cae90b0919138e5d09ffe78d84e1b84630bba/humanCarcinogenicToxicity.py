from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.pesticideAI import impact_lookup_value
from . import MODEL
REQUIREMENTS = {'ImpactAssessment': {'cycle': {'@type': 'Cycle', 'completeness.pesticidesAntibiotics': 'True', 'inputs': [{'@type': 'Input', 'value': '', 'term.termType': 'pesticideAI'}]}}}
RETURNS = {'Indicator': {'value': ''}}
LOOKUPS = {'pesticideAI': '14DCBeqIndividualistHumanCarcinogenicToxicityReCiPe2016'}
TERM_ID = 'humanCarcinogenicToxicity'

def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    return indicator

def run(impact_assessment: dict):
    value = impact_lookup_value(MODEL, TERM_ID, impact_assessment, LOOKUPS['pesticideAI'])
    return None if value is None else _indicator(value)