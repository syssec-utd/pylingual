"""Test for properties."""
import numpy as np
import pytest
from gt4sd.properties import PROPERTY_PREDICTOR_FACTORY, PropertyPredictorRegistry
from gt4sd.properties.molecules import MOLECULE_PROPERTY_PREDICTOR_FACTORY
from gt4sd.properties.molecules.core import SimilaritySeed
from gt4sd.properties.proteins import PROTEIN_PROPERTY_PREDICTOR_FACTORY
from gt4sd.properties.proteins.core import Charge
protein = 'KFLIYQMECSTMIFGL'
molecule = 'C1=CC(=CC(=C1)Br)CN'
seed = 'CCO'
target = 'drd2'
ground_truths = {'length': 16, 'protein_weight': 1924.36, 'boman_index': -0.534375, 'aliphaticity': 97.5, 'hydrophobicity': 0.5625, 'charge': -0.071, 'charge_density': -3.6895383400195386e-05, 'isoelectric_point': 6.125, 'aromaticity': 0.1875, 'instability': 36.8375, 'plogp': 0.25130060815905964, 'molecular_weight': 186.05199999999996, 'lipinski': 1, 'esol': -2.6649954522215555, 'scscore': 4.391860681753299, 'sas': 1.6564993918409403, 'bertz': 197.86256853719752, 'tpsa': 26.02, 'logp': 1.9078, 'qed': 0.7116306772337652, 'number_of_h_acceptors': 1, 'number_of_atoms': 17, 'number_of_h_donors': 1, 'number_of_aromatic_rings': 1, 'number_of_rings': 1, 'number_of_large_rings': 0, 'number_of_rotatable_bonds': 1, 'is_scaffold': 0, 'number_of_heterocycles': 0, 'number_of_stereocenters': 0}
molecule_further_ground_truths = {'activity_against_target': 0.0049787821116125345, 'similarity_seed': 0.03333333333333333}
protein_further_ground_truths = {'charge': 1.123}
artifact_model_data = {'tox21': {'parameters': {'algorithm_version': 'v0'}, 'ground_truth': [6.422001024475321e-05, 0.00028556393226608634, 0.0027144483756273985, 0.03775344416499138, 0.000604992441367358, 0.00027705798856914043, 0.10752066224813461, 0.5733309388160706, 0.001268531079404056, 0.10181115567684174, 0.8995946049690247, 0.1677667647600174]}, 'organtox': {'parameters': {'algorithm_version': 'v0', 'site': 'Heart', 'toxicity_type': 'all'}, 'ground_truth': [0.06142323836684227, 0.07934761792421341]}}

@pytest.mark.parametrize('property_key', [property_key for property_key in ground_truths.keys()])
def test_property(property_key):
    (property_class, parameters_class) = PROPERTY_PREDICTOR_FACTORY[property_key]
    function = property_class(parameters_class())
    sample = protein if property_key in PROTEIN_PROPERTY_PREDICTOR_FACTORY else molecule
    assert np.isclose(function(sample), ground_truths[property_key], atol=0.01)

def test_similarity_seed():
    (property_class, parameters_class) = MOLECULE_PROPERTY_PREDICTOR_FACTORY['similarity_seed']
    function = property_class(parameters_class(smiles=seed))
    assert np.isclose(function(molecule), molecule_further_ground_truths['similarity_seed'], atol=0.01)

def test_activity_against_target():
    (property_class, parameters_class) = MOLECULE_PROPERTY_PREDICTOR_FACTORY['activity_against_target']
    function = property_class(parameters_class(target=target))
    assert np.isclose(function(molecule), molecule_further_ground_truths['activity_against_target'], atol=0.01)

def test_charge_with_arguments():
    (property_class, parameters_class) = PROTEIN_PROPERTY_PREDICTOR_FACTORY['charge']
    function = property_class(parameters_class(amide=True, ph=5.0))
    assert np.isclose(function(protein), protein_further_ground_truths['charge'], atol=0.01)

@pytest.mark.parametrize('property_key', [property_key for property_key in artifact_model_data.keys()])
def test_artifact_models(property_key):
    (property_class, parameters_class) = PROPERTY_PREDICTOR_FACTORY[property_key]
    function = property_class(parameters_class(**artifact_model_data[property_key]['parameters']))
    sample = protein if property_key in PROTEIN_PROPERTY_PREDICTOR_FACTORY else molecule
    assert all(np.isclose(function(sample), artifact_model_data[property_key]['ground_truth'], atol=0.01))

def test_property_predictor_registry():
    predictor = PropertyPredictorRegistry.get_property_predictor('similarity_seed', {'smiles': seed})
    assert isinstance(predictor, SimilaritySeed)
    assert np.isclose(predictor(molecule), molecule_further_ground_truths['similarity_seed'])
    predictor = PropertyPredictorRegistry.get_property_predictor('charge', {'amide': 'True', 'ph': 5.0})
    assert isinstance(predictor, Charge)
    assert np.isclose(predictor(protein), protein_further_ground_truths['charge'])
    assert len(PropertyPredictorRegistry.list_available()) == len(PROTEIN_PROPERTY_PREDICTOR_FACTORY) + len(MOLECULE_PROPERTY_PREDICTOR_FACTORY)