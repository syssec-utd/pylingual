REQUIREMENTS = {'Cycle': {'inputs': [{'@type': 'Input', 'term.units': 'kg', 'term.termType': ['crop', 'animalProduct', 'other'], 'properties': [{'@type': 'Property', 'value': '', 'term.@id': 'energyContentHigherHeatingValue'}]}], 'products': [{'@type': 'Product', 'term.termType': 'animalProduct', 'optional': {'properties': [{'@type': 'Property', 'value': '', 'term.@id': ['processingConversionLiveweightToCarcassWeight', 'processingConversionLiveweightToDressedCarcassWeight', 'processingConversionCarcassWeightToReadyToCookWeight', 'processingConversionDressedCarcassWeightToReadyToCookWeight']}]}}]}}
RETURNS = {'Practice': [{'value': '', 'statsDefinition': 'modelled'}]}
LOOKUPS = {'crop-property': 'energyContentHigherHeatingValue'}
TERM_ID = 'feedConversionRatioCarbon'

def run(cycle: dict, feed: float):
    return feed * 0.021