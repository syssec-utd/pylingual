"""File includes api to uploading data into Scout"""
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from housekeeper.store import models as hk_models
from sqlalchemy.orm import Query
from cg.apps.housekeeper.hk import HousekeeperAPI
from cg.apps.lims import LimsAPI
from cg.apps.madeline.api import MadelineAPI
from cg.apps.scout.scoutapi import ScoutAPI
from cg.constants import Pipeline
from cg.constants.constants import FileFormat
from cg.constants.sequencing import SequencingMethod
from cg.exc import CgDataError, HousekeeperBundleVersionMissingError
from cg.io.controller import WriteFile
from cg.meta.upload.scout.balsamic_config_builder import BalsamicConfigBuilder
from cg.meta.upload.scout.balsamic_umi_config_builder import BalsamicUmiConfigBuilder
from cg.meta.upload.scout.mip_config_builder import MipConfigBuilder
from cg.meta.upload.scout.rnafusion_config_builder import RnafusionConfigBuilder
from cg.meta.upload.scout.scout_config_builder import ScoutConfigBuilder
from cg.meta.workflow.analysis import AnalysisAPI
from cg.models.scout.scout_load_config import ScoutLoadConfig
from cg.store import Store, models
LOG = logging.getLogger(__name__)

class UploadScoutAPI:
    """Class that handles everything that has to do with uploading to Scout"""

    def __init__(self, hk_api: HousekeeperAPI, scout_api: ScoutAPI, lims_api: LimsAPI, analysis_api: AnalysisAPI, madeline_api: MadelineAPI, status_db: Store):
        self.housekeeper = hk_api
        self.scout = scout_api
        self.madeline_api = madeline_api
        self.mip_analysis_api = analysis_api
        self.lims = lims_api
        self.status_db = status_db

    def generate_config(self, analysis_obj: models.Analysis) -> ScoutLoadConfig:
        """Fetch data about an analysis to load Scout."""
        LOG.info('Generate scout load config')
        hk_version_obj: hk_models.Version = self.housekeeper.last_version(analysis_obj.family.internal_id)
        LOG.debug('Found housekeeper version %s', hk_version_obj.id)
        load_config: ScoutLoadConfig
        LOG.info('Found pipeline %s', analysis_obj.pipeline)
        config_builder = self.get_config_builder(analysis=analysis_obj, hk_version=hk_version_obj)
        config_builder.build_load_config()
        return config_builder.load_config

    @staticmethod
    def get_load_config_tag() -> str:
        """Get the hk tag for a scout load config"""
        return 'scout-load-config'

    @staticmethod
    def save_config_file(upload_config: ScoutLoadConfig, file_path: Path) -> None:
        """Save a scout load config file to <file_path>"""
        LOG.info('Save Scout load config to %s', file_path)
        WriteFile.write_file_from_content(content=upload_config.dict(exclude_none=True), file_format=FileFormat.YAML, file_path=file_path)

    def add_scout_config_to_hk(self, config_file_path: Path, case_id: str, delete: bool=False) -> hk_models.File:
        """Add scout load config to hk bundle"""
        LOG.info('Adding load config %s to housekeeper', config_file_path)
        tag_name: str = self.get_load_config_tag()
        version_obj: hk_models.Version = self.housekeeper.last_version(bundle=case_id)
        uploaded_config_file: Optional[hk_models.File] = self.housekeeper.fetch_file_from_version(version_obj=version_obj, tags={tag_name})
        if uploaded_config_file:
            LOG.info('Found config file: %s', uploaded_config_file)
            if not delete:
                raise FileExistsError('Upload config already exists')
            self.housekeeper.delete_file(uploaded_config_file.id)
        file_obj: hk_models.File = self.housekeeper.add_file(path=str(config_file_path), version_obj=version_obj, tags=tag_name)
        self.housekeeper.include_file(file_obj=file_obj, version_obj=version_obj)
        self.housekeeper.add_commit(file_obj)
        LOG.info('Added scout load config to housekeeper: %s', config_file_path)
        return file_obj

    def get_fusion_report(self, case_id: str, research: bool) -> Optional[hk_models.File]:
        """Get a fusion report for case in housekeeper

        Args:
            case_id     (string):       Case identifier
            research    (bool):         Research report
        Returns:
            File in housekeeper (Optional[hk_models.File])
        """
        tags = {'fusion'}
        if research:
            tags.add('research')
        else:
            tags.add('clinical')
        fusion_report: Optional[hk_models.File] = self.housekeeper.get_file_from_latest_version(bundle_name=case_id, tags=tags)
        return fusion_report

    def get_splice_junctions_bed(self, case_id: str, sample_id: str) -> Optional[hk_models.File]:
        """Get a splice junctions bed file for case in housekeeper

        Args:
            case_id     (string):       Case identifier
            sample_id   (string):       Sample identifier
        Returns:
            File in housekeeper (Optional[hk_models.File])
        """
        tags: {str} = {'junction', 'bed', sample_id}
        splice_junctions_bed: Optional[hk_models.File]
        try:
            splice_junctions_bed = self.housekeeper.get_file_from_latest_version(bundle_name=case_id, tags=tags)
        except HousekeeperBundleVersionMissingError:
            LOG.debug('Could not find bundle for case %s', case_id)
        return splice_junctions_bed

    def get_rna_coverage_bigwig(self, case_id: str, sample_id: str) -> Optional[hk_models.File]:
        """Get a rna coverage bigwig file for case in housekeeper

        Args:
            case_id     (string):       Case identifier
            sample_id   (string):       Sample identifier
        Returns:
            File in housekeeper (Optional[hk_models.File])
        """
        tags: {str} = {'coverage', 'bigwig', sample_id}
        rna_coverage_bigwig: Optional[hk_models.File] = self.housekeeper.get_file_from_latest_version(bundle_name=case_id, tags=tags)
        return rna_coverage_bigwig

    def upload_fusion_report_to_scout(self, dry_run: bool, case_id: str, research: bool=False, update: bool=False) -> None:
        """Upload fusion report file for a case to Scout.
        This can also be run as
        `housekeeper get file -V --tag fusion --tag pdf --tag clinical/research <case_id>`
        `scout load gene-fusion-report [-r] <case_id> <path/to/research_gene_fusion_report.pdf>`

        Args:
            dry_run     (bool):         Skip uploading
            case_id     (string):       Case identifier
            research    (bool):         Upload research report instead of clinical
            update      (bool):         Overwrite existing report
        Returns:
            Nothing
        """
        scout_api: ScoutAPI = self.scout
        status_db: Store = self.status_db
        report_type: str = 'Research' if research else 'Clinical'
        rna_case: models.Family = status_db.family(case_id)
        rna_dna_sample_case_map: Dict[str, Dict[str, list]] = self.create_rna_dna_sample_case_map(rna_case=rna_case)
        unique_dna_cases: Set[str] = set()
        fusion_report: Optional[hk_models.File] = self.get_fusion_report(case_id, research)
        if fusion_report is None:
            raise FileNotFoundError(f'{report_type} fusion report was not found in housekeeper for {case_id}')
        LOG.info(f'{report_type} fusion report {fusion_report.path} found')
        for rna_sample_id in rna_dna_sample_case_map:
            dna_cases: List[str]
            dna_sample_id, dna_cases = rna_dna_sample_case_map[rna_sample_id].popitem()
            unique_dna_cases.update(dna_cases)
        for dna_case_id in unique_dna_cases:
            LOG.info(f'Uploading {report_type} fusion report to scout for case {dna_case_id}')
            if dry_run:
                continue
            scout_api.upload_fusion_report(case_id=dna_case_id, report_path=fusion_report.full_path, research=research, update=update)
            LOG.info('Uploaded %s fusion report', report_type)
        LOG.info('Upload %s fusion report finished!', report_type)

    def upload_rna_coverage_bigwig_to_scout(self, case_id: str, dry_run: bool) -> None:
        """Upload rna_coverage_bigwig file for a case to Scout.
            This command can be executed as:
            `housekeeper get file -V --tag coverage --tag bigwig <sample_id>;`
            `scout update individual -c <case_id> -n <customer_sample_id> rna_coverage_bigwig
            <path/to/coverage_file.bigWig>;`

        Args:
            dry_run     (bool):         Skip uploading
            case_id     (string):       Case identifier
        Returns:
            Nothing
        """
        scout_api: ScoutAPI = self.scout
        status_db: Store = self.status_db
        rna_case = status_db.family(case_id)
        rna_dna_sample_case_map: Dict[str, Dict[str, list]] = self.create_rna_dna_sample_case_map(rna_case=rna_case)
        for rna_sample_id in rna_dna_sample_case_map:
            rna_coverage_bigwig: Optional[hk_models.File] = self.get_rna_coverage_bigwig(case_id=case_id, sample_id=rna_sample_id)
            if rna_coverage_bigwig is None:
                raise FileNotFoundError(f'No RNA coverage bigwig file was found in housekeeper for {rna_sample_id}')
            LOG.info(f'RNA coverage bigwig file {rna_coverage_bigwig.path} found')
            dna_sample_id: str
            dna_cases: List[str]
            dna_sample_id, dna_cases = rna_dna_sample_case_map[rna_sample_id].popitem()
            for dna_case_id in dna_cases:
                LOG.info(f'Uploading RNA coverage bigwig file for {dna_sample_id} in case {dna_case_id} in scout')
                if dry_run:
                    continue
                scout_api.upload_rna_coverage_bigwig(file_path=rna_coverage_bigwig.full_path, case_id=dna_case_id, customer_sample_id=dna_sample_id)
                LOG.info(f'Uploaded RNA coverage bigwig file for {dna_sample_id} in case {dna_case_id}')
        LOG.info('Upload RNA coverage bigwig file finished!')

    def upload_splice_junctions_bed_to_scout(self, dry_run: bool, case_id: str) -> None:
        """Upload splice_junctions_bed file for a case to Scout.
            This command can be executed as:
            `housekeeper get file -V --tag junction --tag bed <sample_id>;`
            `scout update individual -c <case_id> -n <customer_sample_id> splice_junctions_bed <path/to/junction_file.bed>;`

        Args:
            dry_run     (bool):         Skip uploading
            case_id     (string):       Case identifier
        Returns:
            Nothing
        """
        scout_api: ScoutAPI = self.scout
        status_db: Store = self.status_db
        rna_case: models.Family = status_db.family(case_id)
        rna_dna_sample_case_map: Dict[str, Dict[str, list]] = self.create_rna_dna_sample_case_map(rna_case=rna_case)
        for rna_sample_id in rna_dna_sample_case_map:
            splice_junctions_bed: Optional[hk_models.File] = self.get_splice_junctions_bed(case_id=case_id, sample_id=rna_sample_id)
            if splice_junctions_bed is None:
                raise FileNotFoundError(f'No splice junctions bed file was found in housekeeper for {rna_sample_id}')
            LOG.info(f'Splice junctions bed file {splice_junctions_bed.path} found')
            dna_sample_id: str
            dna_cases: List[str]
            dna_sample_id, dna_cases = rna_dna_sample_case_map[rna_sample_id].popitem()
            for dna_case_id in dna_cases:
                LOG.info(f'Uploading splice junctions bed file for sample {dna_sample_id} in case {dna_case_id} in scout')
                if dry_run:
                    continue
                scout_api.upload_splice_junctions_bed(file_path=splice_junctions_bed.full_path, case_id=dna_case_id, customer_sample_id=dna_sample_id)
                LOG.info(f'Uploaded splice junctions bed file {dna_sample_id} in case {dna_case_id}')
        LOG.info('Upload splice junctions bed file finished!')

    def upload_rna_junctions_to_scout(self, dry_run: bool, case_id: str) -> None:
        """Upload RNA junctions splice files to Scout.

        Args:
            dry_run     (bool):         Skip uploading
            case_id     (string):       RNA case identifier
        Returns:
            Nothing
        """
        self.upload_splice_junctions_bed_to_scout(dry_run=dry_run, case_id=case_id)
        self.upload_rna_coverage_bigwig_to_scout(case_id=case_id, dry_run=dry_run)

    @staticmethod
    def _get_sample(case: models.Family, subject_id: str) -> Optional[models.Sample]:
        """Get sample of a case for a subject_id.

        Args:
            case     (models.Family):               Case
            subject_id   (str):                     Subject id to search for
        Returns:
            matching sample (models.Sample)
        """
        link: models.FamilySample
        for link in case.links:
            sample: models.Sample = link.sample
            if sample.subject_id == subject_id:
                return sample

    def get_config_builder(self, analysis, hk_version) -> ScoutConfigBuilder:
        config_builders = {Pipeline.BALSAMIC: BalsamicConfigBuilder(hk_version_obj=hk_version, analysis_obj=analysis, lims_api=self.lims), Pipeline.BALSAMIC_UMI: BalsamicUmiConfigBuilder(hk_version_obj=hk_version, analysis_obj=analysis, lims_api=self.lims), Pipeline.MIP_DNA: MipConfigBuilder(hk_version_obj=hk_version, analysis_obj=analysis, mip_analysis_api=self.mip_analysis_api, lims_api=self.lims, madeline_api=self.madeline_api), Pipeline.MIP_RNA: MipConfigBuilder(hk_version_obj=hk_version, analysis_obj=analysis, mip_analysis_api=self.mip_analysis_api, lims_api=self.lims, madeline_api=self.madeline_api), Pipeline.RNAFUSION: RnafusionConfigBuilder(hk_version_obj=hk_version, analysis_obj=analysis, lims_api=self.lims)}
        return config_builders[analysis.pipeline]

    def create_rna_dna_sample_case_map(self, rna_case: models.Family) -> Dict[str, Dict[str, list]]:
        """Returns a nested dictionary for mapping an RNA sample to a DNA sample and its DNA cases based on
        subject_id. Example dictionary {rna_sample_id : {dna_sample_id : [dna_case1_id, dna_case2_id]}}.

        Args:
            rna_case                (models.Family):  RNA case identifier
        Case Returns:
            rna_dna_sample_case_map     (Dict):       rna-dna relationships, and related dna cases based on subject id
        """
        rna_dna_sample_case_map: Dict[str, Dict[str, list]] = {}
        for rna_case.link in rna_case.links:
            self._add_rna_sample(rna_sample=rna_case.link.sample, rna_dna_sample_case_map=rna_dna_sample_case_map)
        return rna_dna_sample_case_map

    def _add_rna_sample(self, rna_sample: models.Sample, rna_dna_sample_case_map: Dict[str, Dict[str, list]]) -> Dict[str, Dict[str, list]]:
        """Adds an RNA sample and its matching DNA sample, and cases."""
        dna_sample: models.Sample = self._link_rna_sample_to_dna_sample(rna_sample=rna_sample, rna_dna_sample_case_map=rna_dna_sample_case_map)
        self._add_dna_cases_to_dna_sample(dna_sample=dna_sample, rna_dna_sample_case_map=rna_dna_sample_case_map, rna_sample=rna_sample)
        return rna_dna_sample_case_map

    def _link_rna_sample_to_dna_sample(self, rna_sample: models.Sample, rna_dna_sample_case_map: Dict[str, Dict[str, list]]) -> models.Sample:
        if not rna_sample.subject_id:
            raise CgDataError(f'Failed on RNA sample {rna_sample.internal_id} as subject_id field is empty')
        subject_id_samples: Query = self.status_db.samples_by_subject_id(customer_id=rna_sample.customer.internal_id, subject_id=rna_sample.subject_id, is_tumour=rna_sample.is_tumour)
        subject_id_dna_samples = self._get_application_prep_category(subject_id_samples.all())
        if len(subject_id_dna_samples) != 1:
            raise CgDataError(f'Failed to upload files for RNA case: unexpected number of DNA sample matches for subject_id: {rna_sample.subject_id}. Number of matches: {len(subject_id_dna_samples)} ')
        rna_dna_sample_case_map[rna_sample.internal_id]: Dict[str, list] = {}
        sample: models.Sample
        for sample in subject_id_dna_samples:
            rna_dna_sample_case_map[rna_sample.internal_id][sample.name]: list = []
            return sample

    @staticmethod
    def _add_dna_cases_to_dna_sample(dna_sample: models.Sample, rna_dna_sample_case_map: Dict[str, Dict[str, list]], rna_sample: models.Sample) -> None:
        for dna_sample.link in dna_sample.links:
            case_object: models.Family = dna_sample.link.family
            if case_object.data_analysis in [Pipeline.MIP_DNA, Pipeline.BALSAMIC, Pipeline.BALSAMIC_UMI] and case_object.customer_id == rna_sample.customer_id:
                rna_dna_sample_case_map[rna_sample.internal_id][dna_sample.name].append(case_object.internal_id)

    @staticmethod
    def _get_application_prep_category(subject_id_samples: List[models.Sample]) -> List[Any]:
        """Filter a models.Sample list, returning DNA samples selected on their prep_category."""
        subject_id_dna_samples: List[models.Sample] = []
        for sample in subject_id_samples:
            if sample.application_version.application.prep_category in [SequencingMethod.WGS, SequencingMethod.TGS, SequencingMethod.WES]:
                subject_id_dna_samples.append(sample)
        return subject_id_dna_samples