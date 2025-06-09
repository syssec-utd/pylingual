from hestia_earth.schema import EmissionMethodTier, TermTermType, EmissionStatsDefinition
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value
from hestia_earth.utils.model import find_primary_product, filter_list_term_type
from hestia_earth.utils.tools import safe_parse_float
from hestia_earth.models.log import logRequirements, debugMissingLookup, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.input import total_excreta_tan
from . import MODEL
REQUIREMENTS = {'Cycle': {'inputs': [{'@type': 'Input', 'value': '', 'term.termType': 'excreta', 'properties': [{'@type': 'Property', 'value': '', 'term.@id': 'totalAmmoniacalNitrogenContentAsN'}]}], 'practices': [{'@type': 'Practice', 'value': '', 'term.termType': 'excretaManagement'}]}}
LOOKUPS = {'excretaManagement-excreta-NH3_EF_2019': 'primary product @id'}
RETURNS = {'Emission': [{'value': '', 'methodTier': 'tier 2', 'statsDefinition': 'modelled'}]}
TERM_ID = 'nh3ToAirExcreta'
TIER = EmissionMethodTier.TIER_2.value

def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission

def get_nh3_factor(termType: str, practices: list, lookup_col: str):
    practices = filter_list_term_type(practices, TermTermType.EXCRETAMANAGEMENT)
    practice_id = practices[0].get('term', {}).get('@id') if len(practices) > 0 else None
    lookup_name = f'excretaManagement-{termType}-NH3_EF_2019.csv'
    lookup = download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', practice_id, column_name(lookup_col))
    debugMissingLookup(lookup_name, 'termid', practice_id, lookup_col, value, model=MODEL, term=TERM_ID)
    return safe_parse_float(value, None)

def _run(excretaKgTAN: float, NH3_N_EF: float):
    value = (NH3_N_EF or 0) * excretaKgTAN * get_atomic_conversion(Units.KG_NH3, Units.TO_N)
    return [_emission(value)]

def _should_run(cycle: dict):
    primary_product = find_primary_product(cycle) or {}
    product_id = primary_product.get('term', {}).get('@id')
    termType = primary_product.get('term', {}).get('termType')
    excretaKgTAN = total_excreta_tan(cycle.get('inputs', []))
    NH3_N_EF = get_nh3_factor(termType, cycle.get('practices', []), product_id) if product_id else None
    logRequirements(cycle, model=MODEL, term=TERM_ID, excretaKgTAN=excretaKgTAN, NH3_N_EF=NH3_N_EF)
    should_run = all([excretaKgTAN, NH3_N_EF is not None])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return (should_run, excretaKgTAN, NH3_N_EF)

def run(cycle: dict):
    should_run, excretaKgTAN, NH3_N_EF = _should_run(cycle)
    return _run(excretaKgTAN, NH3_N_EF) if should_run else []