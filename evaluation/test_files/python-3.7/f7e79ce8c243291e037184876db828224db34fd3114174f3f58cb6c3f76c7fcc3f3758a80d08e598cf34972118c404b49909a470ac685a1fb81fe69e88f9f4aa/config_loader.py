import os
from typing import Dict
from pesto.cli import PROCESSING_FACTORY_PATH
from pesto.cli.core.build_config import BuildConfig
from pesto.cli.core.pesto_files import PestoFiles
from pesto.cli.core.profile_loader import ProfileLoader
from pesto.cli.core.utils import PESTO_LOG
from pesto.common.utils import load_json, validate_json
from pesto.version import PESTO_VERSION
SCHEMA_PATH = os.path.join(PROCESSING_FACTORY_PATH, 'pesto/cli/resources/schema')

class ConfigLoader(object):

    @staticmethod
    def load(build_config: BuildConfig):
        root_path = os.path.join(build_config.algorithm_path, 'pesto')
        loader = ProfileLoader(root_path, build_config.profiles)
        configs = {_: loader.load(_.value) for _ in PestoFiles.required()}
        configs.update({PestoFiles.service: ConfigLoader._describe(configs), PestoFiles.version: ConfigLoader._version(configs), PestoFiles.build: build_config.to_dict()})
        return configs

    @staticmethod
    def _version(configs: Dict) -> dict:
        PESTO_LOG.info('********** generate version.json **********')
        return {'version': configs[PestoFiles.description]['version'], **configs[PestoFiles.version], '__packaging': 'packaged with PESTO v{}'.format(PESTO_VERSION)}

    @staticmethod
    def _describe(configs: Dict) -> dict:
        PESTO_LOG.info('********** generate service.json **********')
        definitions = load_json(SCHEMA_PATH, 'definitions.json')
        description = {**configs[PestoFiles.description], 'config': configs[PestoFiles.config_schema], 'input': {**configs[PestoFiles.input_schema], 'definitions': definitions}, 'output': {**configs[PestoFiles.output_schema], 'definitions': definitions}}
        service_schema = load_json(SCHEMA_PATH, 'service_schema.json')
        validate_json(description, service_schema)
        return description