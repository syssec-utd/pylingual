import json
from unittest.mock import patch
from tests.utils import fixtures_path
from hestia_earth.validation.validators.transformation import validate_previous_transformation, validate_first_transformation_fields, validate_first_transformation_input, validate_transformation_excretaManagement, validate_linked_emission, validate_excreta_inputs_products
class_path = 'hestia_earth.validation.validators.transformation'
fixtures_folder = f'{fixtures_path}/transformation'

def test_validate_previous_transformation_valid():
    assert validate_previous_transformation([]) is True
    with open(f'{fixtures_folder}/previousTransformationTerm/valid.json') as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) is True

def test_validate_previous_transformation_invalid():
    with open(f'{fixtures_folder}/previousTransformationTerm/invalid-wrong-order.json') as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {'level': 'error', 'dataPath': '.transformations[1].previousTransformationTerm', 'message': 'must point to a previous transformation in the list'}
    with open(f'{fixtures_folder}/previousTransformationTerm/invalid-no-previous.json') as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {'level': 'error', 'dataPath': '.transformations[1].previousTransformationTerm', 'message': 'must point to a previous transformation in the list'}
    with open(f'{fixtures_folder}/previousTransformationTerm/invalid-product-input.json') as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {'level': 'error', 'dataPath': '.transformations[1].inputs[0].value', 'message': 'must be equal to previous product multiplied by the share'}

def test_validate_first_transformation_fields_valid():
    assert validate_first_transformation_fields([]) is True
    with open(f'{fixtures_folder}/first-transformation-fields/valid.json') as f:
        data = json.load(f)
    assert validate_first_transformation_fields(data.get('nodes')) is True

def test_validate_first_transformation_fields_invalid():
    with open(f'{fixtures_folder}/first-transformation-fields/invalid.json') as f:
        data = json.load(f)
    assert validate_first_transformation_fields(data.get('nodes')) == {'level': 'error', 'dataPath': '.transformations[0].previousTransformationTerm', 'message': 'must not be set on the first transformation'}

def validate_first_transformation_input_valid():
    assert validate_first_transformation_input({}, []) is True
    with open(f'{fixtures_folder}/first-transformation-input/valid.json') as f:
        cycle = json.load(f)
    assert validate_first_transformation_fields(cycle, cycle.get('transformations')) is True

def test_validate_first_transformation_input_invalid():
    with open(f'{fixtures_folder}/first-transformation-input/invalid.json') as f:
        cycle = json.load(f)
    assert validate_first_transformation_input(cycle, cycle.get('transformations')) == {'level': 'error', 'dataPath': '.transformations[0]', 'message': 'at least one Input must be a Product of the Cycle'}

def test_validate_transformation_excretaManagement_valid():
    assert validate_transformation_excretaManagement([])
    with open(f'{fixtures_folder}/excretaManagement/valid.json') as f:
        data = json.load(f)
    assert validate_transformation_excretaManagement(data.get('nodes')) is True

def test_validate_transformation_excretaManagement_invalid():
    with open(f'{fixtures_folder}/excretaManagement/invalid.json') as f:
        data = json.load(f)
    assert validate_transformation_excretaManagement(data.get('nodes')) == {'level': 'error', 'dataPath': '.transformations[0].practices', 'message': 'an excreta input is required when using an excretaManagement practice'}

def test_validate_linked_emission_valid():
    assert validate_linked_emission({}, 'transformations') is True
    with open(f'{fixtures_folder}/linked-emission/valid.json') as f:
        data = json.load(f)
    assert validate_linked_emission(data, 'transformations') is True

def test_validate_linked_emission_invalid():
    with open(f'{fixtures_folder}/linked-emission/invalid.json') as f:
        data = json.load(f)
    assert validate_linked_emission(data, 'transformations') == {'level': 'warning', 'dataPath': '.transformations[0].emissions[0]', 'message': 'should be linked to an emission in the Cycle', 'params': {'term': {'@type': 'Term', '@id': 'ch4ToAirEntericFermentation', 'termType': 'emission'}}}

def test_validate_excreta_inputs_products_valid():
    assert validate_excreta_inputs_products([]) is True
    with open(f'{fixtures_folder}/inputs-products/valid.json') as f:
        data = json.load(f)
    assert validate_excreta_inputs_products(data) is True

def fake_download_excreta(term_id: str, *args):
    return {'processedExcretaKgVs': {}, 'excretaBeefCattleExceptFeedlotFedKgMass': {'subClassOf': [{}]}}[term_id]

@patch(f'{class_path}.download_hestia', side_effect=fake_download_excreta)
def test_validate_excreta_inputs_products_invalid(*args):
    with open(f'{fixtures_folder}/inputs-products/invalid.json') as f:
        data = json.load(f)
    assert validate_excreta_inputs_products(data) == {'level': 'error', 'dataPath': '.transformations[0].products[1]', 'message': 'must be included as an Input', 'params': {'term': {'@type': 'Term', '@id': 'excretaBeefCattleExceptFeedlotFedKgMass', 'termType': 'excreta'}, 'expected': ['excretaDairyCattle']}}