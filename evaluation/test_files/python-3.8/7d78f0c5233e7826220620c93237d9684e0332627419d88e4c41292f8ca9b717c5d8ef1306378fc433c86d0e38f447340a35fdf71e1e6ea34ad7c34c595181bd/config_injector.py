import logging
from typing import Optional
from _pytest.main import Session
from overhave.entities import IFeatureExtractor, OverhaveFileSettings, StepPrefixesModel
from overhave.test_execution import PytestRunner, StepCollector
logger = logging.getLogger(__name__)

class BaseConfigInjectorException(Exception):
    """Base exception for :class:`ConfigInjector`."""

class NullableEntitiesError(BaseConfigInjectorException):
    """Excepion for situation with unresolved entities."""

class ConfigInjector:
    """Special class to operate with pytest entites, for example get data and patch objects."""

    def __init__(self) -> None:
        self._file_settings: Optional[OverhaveFileSettings] = None
        self._step_collector: Optional[StepCollector] = None
        self._test_runner: Optional[PytestRunner] = None
        self._feature_extractor: Optional[IFeatureExtractor] = None
        self._current_type: Optional[str] = None
        self._initialized = False

    @staticmethod
    def patch_pytestbdd_prefixes(custom_step_prefixes: Optional[StepPrefixesModel]) -> None:
        """Def for patch pytestbdd STEP_PREFIXES."""
        if custom_step_prefixes is not None:
            step_prefixes = custom_step_prefixes.extend_defaults()
            logger.debug('Successfully extended pytest-bdd step prefixes with custom prefixes:\n%s', step_prefixes)

    def supplement_components(self, file_settings: OverhaveFileSettings, step_collector: StepCollector, test_runner: PytestRunner, feature_extractor: IFeatureExtractor) -> None:
        """Def for dynamical supplement of settings on-the-fly (strictly after PyTest configuring)."""
        self._file_settings = file_settings
        self._step_collector = step_collector
        self._test_runner = test_runner
        self._feature_extractor = feature_extractor

    def collect_configs(self) -> None:
        """Special def for pytest run in collect-only mode. Collects pytestbdd steps and other config data."""
        if self._feature_extractor is None or self._test_runner is None or self._file_settings is None:
            raise NullableEntitiesError('Could not collect configuration for injection!')
        if not self._initialized:
            logger.info('Started initialization process...')
            for feature_type in self._feature_extractor.feature_types:
                self._current_type = feature_type
                self._test_runner.collect_only(fixture_file=self._file_settings.fixtures_dir / self._file_settings.fixtures_file_template_mask.format(feature_type=feature_type))
            self._current_type = None
            logger.info('Successfully initialized.')
            self._initialized = True

    @property
    def _inside_collecting(self) -> bool:
        return self._current_type is not None and (not self._initialized)

    def _load_from_session(self, session: Session) -> None:
        """Loads pytestbdd steps and other config data from pytest Session."""
        if self._step_collector is None:
            raise NullableEntitiesError
        if self._inside_collecting:
            self._step_collector.collect_steps(session=session, feature_type=self._current_type)

    def adapt(self, session: Session) -> None:
        """Main def for data loading from pytest Session and enrichment of pytest configs."""
        if self._inside_collecting:
            self._load_from_session(session)