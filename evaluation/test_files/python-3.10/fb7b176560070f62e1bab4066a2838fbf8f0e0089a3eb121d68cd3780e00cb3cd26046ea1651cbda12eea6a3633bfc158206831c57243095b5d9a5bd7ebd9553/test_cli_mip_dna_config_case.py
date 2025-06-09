""" Test the CLI for mip-dna config-case"""
import logging
from cg.cli.workflow.mip_dna.base import config_case

def test_cg_workflow_mip_dna_config_case_dry_run(cli_runner, caplog, case_id, mip_dna_context):
    """Test print the MIP DNA case config command to console."""
    caplog.set_level(logging.INFO)
    result = cli_runner.invoke(config_case, ['--dry-run', case_id], obj=mip_dna_context)
    assert result.exit_code == 0

def test_cg_workflow_mip_dna_config_case(cli_runner, caplog, case_id, mip_dna_context):
    """Test print the MIP dna case config command to file"""
    caplog.set_level(logging.INFO)
    result = cli_runner.invoke(config_case, [case_id], obj=mip_dna_context)
    assert result.exit_code == 0
    assert f'Config file saved to' in caplog.text

def test_cg_workflow_mip_dna_config_case_error(cli_runner, caplog, case_id, mip_dna_context):
    """Test wrong case id with MIP DNA case config command."""
    caplog.set_level(logging.INFO)
    result = cli_runner.invoke(config_case, ['not_a_case_id'], obj=mip_dna_context)
    assert result.exit_code == 1
    assert f'could not be found in Status DB' in caplog.text