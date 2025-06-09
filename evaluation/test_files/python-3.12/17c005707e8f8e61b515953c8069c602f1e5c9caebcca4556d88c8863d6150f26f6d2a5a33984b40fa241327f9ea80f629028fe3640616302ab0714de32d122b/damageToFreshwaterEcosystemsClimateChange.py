from hestia_earth.schema import IndicatorStatsDefinition
from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import impact_lookup_value
from . import MODEL
REQUIREMENTS = {'ImpactAssessment': {'emissionsResourceUse': [{'@type': 'Indicator', 'value': '', 'term.termType': 'emission'}]}}
RETURNS = {'Indicator': {'value': '', 'statsDefinition': 'modelled'}}
LOOKUPS = {'emission': 'pdfYearsAllEffects100YearsClimateChangeDamageToFreshwaterEcosystemsLCImpact'}
TERM_ID = 'damageToFreshwaterEcosystemsClimateChange'

def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator

def run(impact_assessment: dict):
    value = impact_lookup_value(MODEL, TERM_ID, impact_assessment, LOOKUPS['emission'])
    logRequirements(impact_assessment, model=MODEL, term=TERM_ID, value=value)
    logShouldRun(impact_assessment, MODEL, TERM_ID, True)
    return _indicator(value)