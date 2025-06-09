"""Test MIP sample info file"""
from pathlib import Path
import yaml
from cg.models.mip.mip_sample_info import MipBaseSampleInfo

def test_instantiate_mip_sampleinfo(sample_info_dna_raw: dict):
    """Tests sample info against a pydantic MipBaseSampleInfo"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert isinstance(sample_info_object, MipBaseSampleInfo)

def test_mip_sampleinfo(case_qc_sample_info_path: Path):
    """Test to parse the content of a real qc_sample_info file"""
    with open(case_qc_sample_info_path, 'r') as sample_info_handle:
        raw_sample_info = yaml.full_load(sample_info_handle)
    sample_info_object = MipBaseSampleInfo(**raw_sample_info)
    assert isinstance(sample_info_object, MipBaseSampleInfo)

def test_mip_sampleinfo_case_id(sample_info_dna_raw: dict):
    """Test case_id validator"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.case_id == 'yellowhog'

def test_mip_sampleinfo_case_id_with_family_id(sample_info_dna_raw: dict):
    """Test case_id validator"""
    sample_info_dna_raw.pop('case_id')
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.case_id == 'a_family_id'

def test_mip_sampleinfo_genome_build(sample_info_dna_raw: dict):
    """Test genome_build validator"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.genome_build == 'grch37'

def test_mip_sampleinfo_is_finished(sample_info_dna_raw: dict):
    """Test is_finished validator"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.is_finished

def test_mip_sampleinfo_is_finished(sample_info_dna_raw: dict):
    """Test is_finished validator"""
    sample_info_dna_raw['analysisrunstatus'] = 'not_finished'
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert not sample_info_object.is_finished

def test_mip_sampleinfo_rank_model_version(sample_info_dna_raw: dict):
    """Test rank_model_version validator"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.rank_model_version == 'v1.0'

def test_mip_sampleinfo_sv_rank_model_version(sample_info_dna_raw: dict):
    """Test sv_rank_model_version validator"""
    sample_info_object = MipBaseSampleInfo(**sample_info_dna_raw)
    assert sample_info_object.sv_rank_model_version == 'v1.2.0'