"""CLI support to create config and/or start RNAFUSION."""
import logging
from pathlib import Path
import click
from pydantic import ValidationError
from cg.apps.housekeeper.hk import HousekeeperAPI
from cg.cli.workflow.commands import ARGUMENT_CASE_ID, resolve_compression
from cg.cli.workflow.nextflow.options import OPTION_CONFIG, OPTION_LOG, OPTION_PARAMS_FILE, OPTION_PROFILE, OPTION_REVISION, OPTION_STUB, OPTION_TOWER, OPTION_USE_NEXTFLOW, OPTION_WORKDIR
from cg.cli.workflow.rnafusion.options import OPTION_FROM_START, OPTION_REFERENCES, OPTION_STRANDEDNESS
from cg.cli.workflow.tower.options import OPTION_COMPUTE_ENV
from cg.constants import EXIT_FAIL, EXIT_SUCCESS
from cg.constants.constants import DRY_RUN, CaseActions, MetaApis
from cg.constants.tb import AnalysisStatus
from cg.exc import CgError, DecompressionNeededError, MetricsQCError
from cg.meta.workflow.analysis import AnalysisAPI
from cg.meta.workflow.nextflow_common import NextflowAnalysisAPI
from cg.meta.workflow.rnafusion import RnafusionAnalysisAPI
from cg.models.cg_config import CGConfig
from cg.store import Store
LOG = logging.getLogger(__name__)

@click.group(invoke_without_command=True)
@click.pass_context
def rnafusion(context: click.Context) -> None:
    """nf-core/rnafusion analysis workflow."""
    AnalysisAPI.get_help(context)
    context.obj.meta_apis[MetaApis.ANALYSIS_API] = RnafusionAnalysisAPI(config=context.obj)
rnafusion.add_command(resolve_compression)

@rnafusion.command('config-case')
@ARGUMENT_CASE_ID
@OPTION_STRANDEDNESS
@OPTION_REFERENCES
@DRY_RUN
@click.pass_obj
def config_case(context: CGConfig, case_id: str, strandedness: str, genomes_base: Path, dry_run: bool) -> None:
    """Create sample sheet file for RNAFUSION analysis for a given CASE_ID."""
    analysis_api: RnafusionAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]
    LOG.info(f'Creating sample sheet file for {case_id}.')
    analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
    try:
        analysis_api.config_case(case_id=case_id, strandedness=strandedness, genomes_base=genomes_base, dry_run=dry_run)
    except CgError as error:
        LOG.error(f'Could not create sample sheet: {error}')
        raise click.Abort() from error

@rnafusion.command('run')
@ARGUMENT_CASE_ID
@OPTION_LOG
@OPTION_WORKDIR
@OPTION_FROM_START
@OPTION_PROFILE
@OPTION_TOWER
@OPTION_STUB
@OPTION_CONFIG
@OPTION_PARAMS_FILE
@OPTION_REVISION
@OPTION_COMPUTE_ENV
@OPTION_USE_NEXTFLOW
@DRY_RUN
@click.pass_obj
def run(context: CGConfig, case_id: str, log: str, work_dir: str, from_start: bool, profile: str, with_tower: bool, stub: bool, config: str, params_file: str, revision: str, compute_env: str, use_nextflow: bool, dry_run: bool) -> None:
    """Run rnafusion analysis for given CASE ID."""
    analysis_api: RnafusionAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]
    analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
    command_args = {'log': NextflowAnalysisAPI.get_log_path(case_id=case_id, pipeline=analysis_api.pipeline, root_dir=analysis_api.root_dir, log=log), 'work-dir': NextflowAnalysisAPI.get_workdir_path(case_id=case_id, root_dir=analysis_api.root_dir, work_dir=work_dir), 'resume': not from_start, 'profile': analysis_api.get_profile(profile=profile), 'with-tower': with_tower, 'stub': stub, 'config': NextflowAnalysisAPI.get_nextflow_config_path(nextflow_config=config), 'params-file': NextflowAnalysisAPI.get_params_file_path(case_id=case_id, root_dir=analysis_api.root_dir, params_file=params_file), 'name': case_id, 'compute-env': compute_env or analysis_api.compute_env, 'revision': revision or analysis_api.revision, 'wait': 'SUBMITTED'}
    try:
        analysis_api.verify_case_config_file_exists(case_id=case_id, dry_run=dry_run)
        analysis_api.check_analysis_ongoing(case_id)
        LOG.info(f'Running RNAFUSION analysis for {case_id}')
        analysis_api.run_analysis(case_id=case_id, command_args=command_args, use_nextflow=use_nextflow, dry_run=dry_run)
        analysis_api.set_statusdb_action(case_id=case_id, action=CaseActions.RUNNING, dry_run=dry_run)
    except (CgError, ValueError) as error:
        LOG.error(f'Could not run analysis: {error}')
        raise click.Abort() from error
    except Exception as error:
        LOG.error(f'Could not run analysis: {error}')
        raise click.Abort() from error
    if not dry_run:
        analysis_api.add_pending_trailblazer_analysis(case_id=case_id)

@rnafusion.command('start')
@ARGUMENT_CASE_ID
@OPTION_LOG
@OPTION_WORKDIR
@OPTION_PROFILE
@OPTION_TOWER
@OPTION_STUB
@OPTION_CONFIG
@OPTION_PARAMS_FILE
@OPTION_REVISION
@OPTION_COMPUTE_ENV
@OPTION_USE_NEXTFLOW
@OPTION_REFERENCES
@DRY_RUN
@click.pass_context
def start(context: CGConfig, case_id: str, log: str, work_dir: str, profile: str, with_tower: bool, stub: bool, config: str, params_file: str, revision: str, compute_env: str, use_nextflow: bool, genomes_base: Path, dry_run: bool) -> None:
    """Start full workflow for CASE ID."""
    LOG.info(f'Starting analysis for {case_id}')
    try:
        context.invoke(resolve_compression, case_id=case_id, dry_run=dry_run)
    except DecompressionNeededError as error:
        LOG.error(error)
        raise click.Abort() from error
    context.invoke(config_case, case_id=case_id, genomes_base=genomes_base, dry_run=dry_run)
    context.invoke(run, case_id=case_id, log=log, work_dir=work_dir, from_start=True, profile=profile, with_tower=with_tower, stub=stub, config=config, params_file=params_file, revision=revision, compute_env=compute_env, use_nextflow=use_nextflow, dry_run=dry_run)

@rnafusion.command('start-available')
@DRY_RUN
@click.pass_context
def start_available(context: click.Context, dry_run: bool=False) -> None:
    """Start full workflow for all cases ready for analysis."""
    analysis_api: AnalysisAPI = context.obj.meta_apis[MetaApis.ANALYSIS_API]
    exit_code: int = EXIT_SUCCESS
    for case_obj in analysis_api.get_cases_to_analyze():
        try:
            context.invoke(start, case_id=case_obj.internal_id, dry_run=dry_run)
        except CgError as error:
            LOG.error(error)
            exit_code = EXIT_FAIL
        except Exception as error:
            LOG.error(f'Unspecified error occurred: {error}')
            exit_code = EXIT_FAIL
    if exit_code:
        raise click.Abort

@rnafusion.command('metrics-deliver')
@ARGUMENT_CASE_ID
@DRY_RUN
@click.pass_obj
def metrics_deliver(context: CGConfig, case_id: str, dry_run: bool) -> None:
    """Create and validate a metrics deliverables file for given case id.
    If QC metrics are met it sets the status in Trailblazer to complete.
    If failed, it sets it as failed and adds a comment with information of the failed metrics."""
    analysis_api: RnafusionAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]
    try:
        analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
    except CgError as error:
        raise click.Abort() from error
    if not analysis_api.trailblazer_api.is_latest_analysis_qc(case_id=case_id):
        raise click.Abort()
    analysis_api.write_metrics_deliverables(case_id=case_id, dry_run=dry_run)
    if dry_run:
        LOG.info('Dry-run: QC metrics validation would be performed.')
        return
    try:
        LOG.info('Validating QC metrics.')
        analysis_api.validate_qc_metrics(case_id=case_id)
    except MetricsQCError as error:
        LOG.error(f'QC metrics failed for {case_id}')
        analysis_api.trailblazer_api.set_analysis_status(case_id=case_id, status=AnalysisStatus.FAILED)
        analysis_api.trailblazer_api.add_comment(case_id=case_id, comment=str(error))
        raise click.Abort() from error
    except CgError as error:
        LOG.error(f'Could not create metrics deliverables file: {error}')
        analysis_api.trailblazer_api.set_analysis_status(case_id=case_id, status=AnalysisStatus.ERROR)
        raise click.Abort() from error
    analysis_api.trailblazer_api.set_analysis_status(case_id=case_id, status=AnalysisStatus.COMPLETED)

@rnafusion.command('report-deliver')
@ARGUMENT_CASE_ID
@DRY_RUN
@click.pass_obj
def report_deliver(context: CGConfig, case_id: str, dry_run: bool) -> None:
    """Create a housekeeper deliverables file for given CASE ID."""
    analysis_api: RnafusionAnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]
    try:
        analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
        analysis_api.trailblazer_api.is_latest_analysis_completed(case_id=case_id)
        if not dry_run:
            analysis_api.report_deliver(case_id=case_id)
        else:
            LOG.info('Dry-run')
    except CgError as error:
        LOG.error(f'Could not create report file: {error}')
        raise click.Abort()
    except Exception as error:
        LOG.error(f'Could not create report file: {error}')
        raise click.Abort()

@rnafusion.command('store-housekeeper')
@ARGUMENT_CASE_ID
@DRY_RUN
@click.pass_obj
def store_housekeeper(context: CGConfig, case_id: str, dry_run: bool) -> None:
    """Store a finished RNAFUSION analysis in Housekeeper and StatusDB."""
    analysis_api: AnalysisAPI = context.meta_apis[MetaApis.ANALYSIS_API]
    housekeeper_api: HousekeeperAPI = context.housekeeper_api
    status_db: Store = context.status_db
    try:
        analysis_api.status_db.verify_case_exists(case_internal_id=case_id)
        analysis_api.trailblazer_api.is_latest_analysis_completed(case_id=case_id)
        analysis_api.verify_deliverables_file_exists(case_id=case_id)
        analysis_api.upload_bundle_housekeeper(case_id=case_id, dry_run=dry_run)
        analysis_api.upload_bundle_statusdb(case_id=case_id, dry_run=dry_run)
        analysis_api.set_statusdb_action(case_id=case_id, action=None, dry_run=dry_run)
    except ValidationError as error:
        LOG.warning('Deliverables file is malformed')
        raise error
    except CgError as error:
        LOG.error(f'Could not store bundle in Housekeeper and StatusDB: {error}')
        raise click.Abort()
    except Exception as error:
        LOG.error(f'Could not store bundle in Housekeeper and StatusDB: {error}!')
        housekeeper_api.rollback()
        status_db.session.rollback()
        raise click.Abort()

@rnafusion.command('store')
@ARGUMENT_CASE_ID
@DRY_RUN
@click.pass_context
def store(context: click.Context, case_id: str, dry_run: bool) -> None:
    """Generate deliverables files for a case and store in Housekeeper if they
    pass QC metrics checks."""
    LOG.info('Generating metrics file and performing QC checks for %s', case_id)
    context.invoke(metrics_deliver, case_id=case_id, dry_run=dry_run)
    LOG.info(f'Storing analysis for {case_id}')
    context.invoke(report_deliver, case_id=case_id, dry_run=dry_run)
    context.invoke(store_housekeeper, case_id=case_id, dry_run=dry_run)

@rnafusion.command('store-available')
@DRY_RUN
@click.pass_context
def store_available(context: click.Context, dry_run: bool) -> None:
    """Store bundles for all finished RNAFUSION analyses in Housekeeper."""
    analysis_api: AnalysisAPI = context.obj.meta_apis[MetaApis.ANALYSIS_API]
    exit_code: int = EXIT_SUCCESS
    for case_obj in analysis_api.get_cases_to_qc():
        LOG.info('Storing RNAFUSION deliverables for %s', case_obj.internal_id)
        try:
            context.invoke(store, case_id=case_obj.internal_id, dry_run=dry_run)
        except Exception as error:
            LOG.error(f'Error storing {case_obj.internal_id}: {error}')
            exit_code: int = EXIT_FAIL
    if exit_code:
        raise click.Abort