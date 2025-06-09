"""Tests for RNA part of the scout upload API"""
import logging
from typing import Generator, List
import pytest
from _pytest.logging import LogCaptureFixture
from alchy import Query
from cg.apps.housekeeper.hk import HousekeeperAPI
from cg.constants import Pipeline
from cg.constants.sequencing import SequencingMethod
from cg.exc import CgDataError
from cg.meta.upload.scout.uploadscoutapi import UploadScoutAPI
from cg.store.models import Family, Sample
import cg.store as Store
from tests.store_helpers import StoreHelpers

def set_is_tumour_on_case(store: Store, case_id: str, is_tumour: bool):
    for link in store.get_case_by_internal_id(internal_id=case_id).links:
        link.sample.is_tumour = is_tumour

def get_subject_id_from_case(store: Store, case_id: str) -> str:
    for link in store.get_case_by_internal_id(internal_id=case_id).links:
        return link.sample.subject_id

def ensure_two_dna_tumour_matches(dna_case_id: str, another_sample_id: str, helpers: StoreHelpers, rna_case_id: str, rna_store: Store) -> None:
    """Ensures that we have one RNA case that has two matching DNA cases via subject id and tumour state."""
    set_is_tumour_on_case(store=rna_store, case_id=rna_case_id, is_tumour=True)
    subject_id: str = get_subject_id_from_case(store=rna_store, case_id=rna_case_id)
    set_is_tumour_on_case(store=rna_store, case_id=dna_case_id, is_tumour=True)
    dna_extra_case = helpers.ensure_case(store=rna_store, customer=rna_store.get_case_by_internal_id(dna_case_id).customer)
    another_sample_id = helpers.add_sample(store=rna_store, name=another_sample_id, subject_id=subject_id, is_tumour=True, application_tag=SequencingMethod.WGS, application_type=SequencingMethod.WGS)
    helpers.add_relationship(store=rna_store, sample=another_sample_id, case=dna_extra_case)
    rna_store.commit()

def ensure_extra_rna_case_match(another_rna_sample_id: str, helpers: StoreHelpers, rna_case_id: str, rna_store: Store) -> None:
    """Ensures that we have an extra RNA case that matches by subject_id the existing RNA case and DNA cases."""
    rna_extra_case = helpers.ensure_case(store=rna_store, data_analysis=Pipeline.MIP_RNA, customer=rna_store.get_case_by_internal_id(rna_case_id).customer)
    subject_id: str = get_subject_id_from_case(store=rna_store, case_id=rna_case_id)
    another_rna_sample_id = helpers.add_sample(store=rna_store, internal_id=another_rna_sample_id, subject_id=subject_id, is_tumour=False, application_type=SequencingMethod.WTS)
    helpers.add_relationship(store=rna_store, sample=another_rna_sample_id, case=rna_extra_case)

def test_upload_rna_junctions_to_scout(caplog: Generator[LogCaptureFixture, None, None], mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report and junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    upload_scout_api.upload_rna_junctions_to_scout(case_id=rna_case_id, dry_run=True)
    assert 'Upload splice junctions bed file finished!' in caplog.text
    assert 'Upload RNA coverage bigwig file finished!' in caplog.text

def test_upload_splice_junctions_bed_to_scout(caplog: Generator[LogCaptureFixture, None, None], dna_sample_son_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    upload_scout_api.upload_splice_junctions_bed_to_scout(case_id=rna_case_id, dry_run=True)
    assert 'Upload splice junctions bed file finished!' in caplog.text
    dna_customer_sample_name: str = rna_store.get_sample_by_internal_id(internal_id=dna_sample_son_id).name
    assert dna_customer_sample_name in caplog.text

def test_upload_rna_coverage_bigwig_to_scout(caplog: Generator[LogCaptureFixture, None, None], dna_sample_son_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's bigWig file for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    upload_scout_api.upload_rna_coverage_bigwig_to_scout(case_id=rna_case_id, dry_run=True)
    assert 'Upload RNA coverage bigwig file finished!' in caplog.text
    dna_customer_sample_name: str = rna_store.get_sample_by_internal_id(internal_id=dna_sample_son_id).name
    assert dna_customer_sample_name in caplog.text

def test_upload_clinical_rna_fusion_report_to_scout(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, dna_sample_son_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's clinical fusion report and junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    upload_scout_api.upload_fusion_report_to_scout(case_id=rna_case_id, dry_run=True)
    assert 'Upload Clinical fusion report finished!' in caplog.text
    assert dna_case_id in caplog.text
    dna_customer_sample_name: str = rna_store.get_sample_by_internal_id(internal_id=dna_sample_son_id).name
    assert dna_customer_sample_name not in caplog.text

def test_upload_research_rna_fusion_report_to_scout(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, dna_sample_son_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report and junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    upload_scout_api.upload_fusion_report_to_scout(case_id=rna_case_id, dry_run=True, research=True)
    assert 'Upload Research fusion report finished!' in caplog.text
    assert dna_case_id in caplog.text
    dna_customer_sample_name: str = rna_store.get_sample_by_internal_id(internal_id=dna_sample_son_id).name
    assert dna_customer_sample_name not in caplog.text

def test_upload_rna_fusion_report_to_scout_no_subject_id(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report"""
    for link in rna_store.get_case_by_internal_id(rna_case_id).links:
        link.sample.subject_id = ''
    for link in rna_store.get_case_by_internal_id(dna_case_id).links:
        link.sample.subject_id = ''
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_fusion_report_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_rna_coverage_bigwig_to_scout_no_subject_id(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report and junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    for link in rna_store.get_case_by_internal_id(rna_case_id).links:
        link.sample.subject_id = ''
    for link in rna_store.get_case_by_internal_id(dna_case_id).links:
        link.sample.subject_id = ''
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_rna_coverage_bigwig_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_splice_junctions_bed_to_scout_no_subject_id(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's junction splice files for all samples can be loaded via a cg CLI
    command into an already existing DNA case"""
    for link in rna_store.get_case_by_internal_id(rna_case_id).links:
        link.sample.subject_id = ''
    for link in rna_store.get_case_by_internal_id(dna_case_id).links:
        link.sample.subject_id = ''
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_splice_junctions_bed_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_rna_fusion_report_to_scout_tumour_non_matching(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that an RNA case's gene fusion report is not uploaded if the is_tumour is not matching"""
    set_is_tumour_on_case(store=rna_store, case_id=rna_case_id, is_tumour=True)
    set_is_tumour_on_case(store=rna_store, case_id=dna_case_id, is_tumour=False)
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_fusion_report_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_rna_coverage_bigwig_to_scout_tumour_non_matching(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report and junction splice files for all samples is not uploaded if the is_tumour is not matching"""
    set_is_tumour_on_case(store=rna_store, case_id=rna_case_id, is_tumour=True)
    set_is_tumour_on_case(store=rna_store, case_id=dna_case_id, is_tumour=False)
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_rna_coverage_bigwig_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_splice_junctions_bed_to_scout_tumour_non_matching(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's junction splice files for all samples is not uploaded if the is_tumour is not matching"""
    set_is_tumour_on_case(store=rna_store, case_id=rna_case_id, is_tumour=True)
    set_is_tumour_on_case(store=rna_store, case_id=dna_case_id, is_tumour=False)
    rna_store.commit()
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_splice_junctions_bed_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_rna_fusion_report_to_scout_tumour_multiple_matches(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, another_sample_id: str, helpers: StoreHelpers, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that an RNA case's gene fusion report is not uploaded if the is_tumour has too many DNA-matches"""
    ensure_two_dna_tumour_matches(dna_case_id, another_sample_id, helpers, rna_case_id, rna_store)
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_fusion_report_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_rna_coverage_bigwig_to_scout_tumour_multiple_matches(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, another_sample_id: str, helpers: StoreHelpers, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's gene fusion report and junction splice files for all samples is not uploaded if the RNA-sample has too many DNA-matches"""
    ensure_two_dna_tumour_matches(dna_case_id, another_sample_id, helpers, rna_case_id, rna_store)
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_rna_coverage_bigwig_to_scout(case_id=rna_case_id, dry_run=True)

def test_upload_splice_junctions_bed_to_scout_tumour_multiple_matches(caplog: Generator[LogCaptureFixture, None, None], dna_case_id: str, another_sample_id: str, helpers: StoreHelpers, mip_rna_analysis_hk_api: HousekeeperAPI, rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that A RNA case's junction splice files for all samples is not uploaded if the RNA-sample has too many DNA-matches"""
    ensure_two_dna_tumour_matches(dna_case_id, another_sample_id, helpers, rna_case_id, rna_store)
    upload_scout_api.status_db = rna_store
    caplog.set_level(logging.INFO)
    with pytest.raises(CgDataError):
        upload_scout_api.upload_splice_junctions_bed_to_scout(case_id=rna_case_id, dry_run=True)

def test_get_application_prep_category(another_rna_sample_id: str, dna_sample_son_id: str, helpers: StoreHelpers, rna_case_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that RNA samples are removed when filtering sample list by pipeline"""
    ensure_extra_rna_case_match(another_rna_sample_id, helpers, rna_case_id, rna_store)
    upload_scout_api.status_db = rna_store
    dna_sample: Sample = rna_store.get_sample_by_internal_id(dna_sample_son_id)
    another_rna_sample_id: Sample = rna_store.get_sample_by_internal_id(another_rna_sample_id)
    all_son_rna_dna_samples: List[Sample] = [dna_sample, another_rna_sample_id]
    only_son_dna_samples = upload_scout_api._get_application_prep_category(all_son_rna_dna_samples)
    nr_of_subject_id_samples: int = len(all_son_rna_dna_samples)
    nr_of_subject_id_dna_samples: int = len([only_son_dna_samples])
    assert nr_of_subject_id_samples == 2
    assert nr_of_subject_id_dna_samples == 1

def test_create_rna_dna_sample_case_map(rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that the create_rna_dna_sample_case_map returns a nested dictionary."""
    rna_case: Family = rna_store.get_case_by_internal_id(internal_id=rna_case_id)
    rna_dna_case_map: dict = upload_scout_api.create_rna_dna_sample_case_map(rna_case=rna_case)
    assert all((isinstance(items, dict) for items in rna_dna_case_map.values()))

def test_add_rna_sample(rna_case_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test that for a given RNA case the RNA samples are added to the rna_dna_case_map."""
    rna_case: Family = rna_store.get_case_by_internal_id(internal_id=rna_case_id)
    rna_sample_list: List[Sample] = rna_store.get_samples_by_name_pattern(name_pattern='rna')
    rna_dna_case_map: dict = upload_scout_api.create_rna_dna_sample_case_map(rna_case=rna_case)
    for key in rna_sample_list:
        assert key.internal_id in list(rna_dna_case_map.keys())

def test_link_rna_sample_to_dna_sample(dna_sample_son_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test for a given RNA sample, the associated DNA sample name matches and is present in rna_dna_case_map."""
    rna_sample: Sample = rna_store.get_sample_by_internal_id(rna_sample_son_id)
    rna_dna_case_map: dict = {}
    upload_scout_api._add_rna_sample(rna_sample=rna_sample, rna_dna_sample_case_map=rna_dna_case_map)
    assert rna_sample_son_id in rna_dna_case_map
    dna_samples: dict = rna_dna_case_map[rna_sample.internal_id]
    assert dna_sample_son_id in dna_samples

def test_add_dna_cases_to_dna_sample(dna_case_id: str, dna_sample_son_id: str, rna_sample_son_id: str, rna_store: Store, upload_scout_api: UploadScoutAPI):
    """Test for a given RNA sample, the DNA case name matches to the case name of the DNA sample in rna_dna_case_map."""
    rna_sample: Sample = rna_store.get_sample_by_internal_id(rna_sample_son_id)
    dna_sample: Sample = rna_store.get_sample_by_internal_id(dna_sample_son_id)
    dna_case: Family = rna_store.get_case_by_internal_id(internal_id=dna_case_id)
    rna_dna_case_map: dict = {}
    upload_scout_api._add_rna_sample(rna_sample=rna_sample, rna_dna_sample_case_map=rna_dna_case_map)
    case_names: list = rna_dna_case_map[rna_sample.internal_id][dna_sample.name]
    assert dna_case.internal_id in case_names