"""
CLI module to calculate dilution volumes from Concentration udf

For an explanation of the sample volume calculation and setting of the QG flag, see
AM-document 1243 Method - Preparing Plate for Genotyping, section 3.3.2 Preparing the plate
"""
import logging
import sys
from typing import List, Optional
import click
from genologics.entities import Artifact
from pydantic import BaseModel, validator
from cg_lims.exceptions import LimsError
from cg_lims.get.artifacts import get_artifacts
LOG = logging.getLogger(__name__)
FINAL_CONCENTRATION = 4
MINIMUM_TOTAL_VOLUME = 15
QC_FAILED = 'FAILED'
QC_PASSED = 'PASSED'
STANDARD_SAMPLE_VOLUME = 3

class MafVolumes(BaseModel):
    """Pydantic model for calculating MAF volumes based on the sample concentration"""
    sample_concentration: float
    sample_volume: Optional[float]
    final_volume: Optional[float]
    water_volume: Optional[float]
    qc_flag: Optional[str]

    @validator('sample_concentration', always=True)
    def set_sample_concentration(cls, v, values):
        """Set sample concentration and handle low or missing concentration"""
        if v < FINAL_CONCENTRATION:
            message = 'Too low or missing concentration'
            LOG.error(message)
            raise ValueError(message)
        return v

    @validator('sample_volume', always=True)
    def set_sample_volume(cls, v, values):
        """Calculate the sample volume. For an explanation about how sample volumes are
        determined for various sample concentration ranges, refer to AM document 1243 Method -
        Preparing Plate for Genotyping, section 3.3.2"""
        sample_concentration = values.get('sample_concentration')
        if sample_concentration < 20:
            return MINIMUM_TOTAL_VOLUME * FINAL_CONCENTRATION / sample_concentration
        elif 20 <= sample_concentration < 244:
            return 3
        elif 244 <= sample_concentration < 364:
            return 2
        elif 364 <= sample_concentration < 724:
            return 1
        elif 724 <= sample_concentration < 1444:
            return 0.5
        else:
            message = 'Sample concentration not in valid range'
            LOG.error(message)
            raise ValueError(message)

    @validator('water_volume', always=True)
    def set_water_volume(cls, v, values):
        """Calculate the water volume for a sample"""
        return values.get('final_volume') - values.get('sample_volume')

    @validator('final_volume', always=True)
    def set_final_volume(cls, v, values):
        """Calculates the final volume for a sample"""
        return values.get('sample_volume') * values.get('sample_concentration') / FINAL_CONCENTRATION

    @validator('qc_flag', always=True)
    def set_qc_flag(cls, v, values):
        """Set the QC flag on a sample"""
        if values.get('sample_volume') == STANDARD_SAMPLE_VOLUME:
            return QC_PASSED
        else:
            return QC_FAILED

def calculate_volume(artifacts: List[Artifact]) -> None:
    """Determines the final volume, water volume, and sample volume"""
    failed_artifacts = []
    for artifact in artifacts:
        try:
            volumes = MafVolumes(sample_concentration=artifact.udf.get('Concentration'))
            artifact.qc_flag = volumes.qc_flag
            artifact.udf['Final Volume (uL)'] = volumes.final_volume
            artifact.udf['Volume H2O (ul)'] = volumes.water_volume
            artifact.udf['Volume of sample (ul)'] = volumes.sample_volume
            artifact.put()
        except Exception:
            LOG.warning(f'Could not calculate sample volume for sample {artifact.id}.')
            failed_artifacts.append(artifact)
            continue
    if failed_artifacts:
        raise LimsError(f'MAF volume calculations failed for {len(failed_artifacts)} samples, {len(artifacts) - len(failed_artifacts)} updates successful. ')

@click.command()
@click.pass_context
def maf_calculate_volume(context: click.Context):
    """Calculate dilution volumes based on the Concentration udf"""
    LOG.info(f'Running {context.command_path} with params: {context.params}')
    process = context.obj['process']
    try:
        artifacts: List[Artifact] = get_artifacts(process=process, input=False)
        calculate_volume(artifacts=artifacts)
        message = 'MAF volumes have been calculated.'
        LOG.info(message)
        click.echo(message)
    except LimsError as e:
        LOG.error(e.message)
        sys.exit(e.message)