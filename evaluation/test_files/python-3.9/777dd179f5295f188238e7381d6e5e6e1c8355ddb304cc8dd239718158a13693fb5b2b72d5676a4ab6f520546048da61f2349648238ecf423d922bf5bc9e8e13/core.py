"""Bases classes and core code used across multiple algorithms."""
from __future__ import annotations
import collections
import logging
import os
import shutil
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from time import time
from typing import Any, Callable, ClassVar, Dict, Generic, Iterable, Iterator, Optional, Set, Type, TypeVar, Union
from ..configuration import GT4SDConfiguration, get_algorithm_subdirectories_in_cache, get_algorithm_subdirectories_with_s3, get_cached_algorithm_path, sync_algorithm_with_s3, upload_to_s3
from ..exceptions import GT4SDTimeoutError, InvalidItem, S3SyncError, SamplingError
from ..training_pipelines.core import TrainingPipelineArguments
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
gt4sd_configuration_instance = GT4SDConfiguration.get_instance()
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')
Targeted = Callable[[T], Iterable[Any]]
Untargeted = Callable[[], Iterable[Any]]
Predictor = Callable[[Any], Any]

class GeneratorAlgorithm(ABC, Generic[S, T]):
    """Interface for automated generation via an :class:`AlgorithmConfiguration`."""
    generator: Union[Untargeted, Targeted[T]]
    target: Optional[T]
    max_runtime: int = gt4sd_configuration_instance.gt4sd_max_runtime
    max_samples: int = gt4sd_configuration_instance.gt4sd_max_number_of_samples
    generate: Untargeted

    def __init__(self, configuration: AlgorithmConfiguration[S, T], target: Optional[T]=None):
        """Targeted or untargeted generation.

        Args:
            configuration: application specific helper that allows to setup the
                generator.
            target: context or condition for the generation. Defaults to None.
        """
        logger.info(f'runnning {self.__class__.__name__} with configuration={configuration}')
        generator = self.get_generator(configuration, target)
        setattr(self, 'generate', self._setup_untargeted_generator(configuration=configuration, generator=generator, target=target))

    @abstractmethod
    def get_generator(self, configuration: AlgorithmConfiguration[S, T], target: Optional[T]) -> Union[Untargeted, Targeted[T]]:
        """Set up the detail implementation using the configuration.

        Note:
            This is the major method to implement in child classes, it is called
            at instantiation of the GeneratorAlgorithm and must return a callable:

            - Either :obj:`Untargeted`: the callable is taking no arguements,
              and target has to be :obj:`None`.
            - Or :obj:`Targeted`: the callable with the target (but not :obj:`None`).

        Args:
            configuration: application specific helper that allows to setup the
                generator.
            target: context or condition for the generation. Defaults to None.

        Returns:
            generator, the detail implementation used for generation.
            If the target is None, the generator is assumed to be untargeted.
        """

    def timeout(self, item_set: Set, detail: str, error: TimeoutError) -> None:
        """Throws a timeout exception if applicable, otherwise returns
            items gracefully.

        Args:
            item_set: Set of items generated thus far.
            detail: context or condition for the generation.
            error: An error instance, child class of `TimeoutError` either
                `GT4SDTimeoutError` or `SamplingError`.

        Raises:
            TimeoutError: If no items were sampled so far.
        """
        if len(item_set) == 0:
            logger.error(detail + 'Exiting now!')
            raise error(title='No samples generated', detail=detail)
        logger.warning(detail + f'Returning {len(item_set)} instead of {self.number_of_items} items!')

    def _setup_untargeted_generator(self, configuration: AlgorithmConfiguration[S, T], generator: Union[Untargeted, Targeted[T]], target: Optional[T]=None) -> Untargeted:
        """Targeted or untargeted generation.

        Args:
            configuration: application specific helper that allows to setup the
                generator.
            generator: the detail implementation used for generation.
                If the target is None, the generator is assumed to be untargeted.
            target: context or condition for the generation. Defaults to None.
        """
        self.configuration = configuration
        self.target = target
        self.generator = generator
        if target is None:
            return self.generator
        else:
            return partial(self.generator, self.target)

    def sample(self, number_of_items: int=100) -> Iterator[S]:
        """Generate a number of unique and valid items.

        Filters duplicate items and iterates batches of generated items to reach
        the desired number of samples, but the number of yielded items is not
        guaranteed:
        In case the generate method does not create new samples for
        GT4SD_MAX_NUMBER_OF_STUCK_CALLS times, it will terminate the
        sampling process.

        Args:
            number_of_items: number of items to generate.
                Defaults to 100.

        Raises:
            SamplingError: when requesting too many items.
            GT4SDTimeoutError: when the algorithm takes longer than the allowed time limit.
                Or when no items were yielded (i.e., if not generating samples for many
                consecutive calls).

        Yields:
            the items.
        """
        self.number_of_items = number_of_items
        if number_of_items > self.max_samples:
            detail = f'{number_of_items} is too many items to generate, must be under {self.max_samples + 1} samples.'
            self.timeout(set(), detail=detail, error=SamplingError)
        item_set: Set = set()
        stuck_counter = 0
        item_set_length = 0
        start = time()
        while True:
            if time() - start > self.max_runtime:
                detail = f'Sampling took longer than maximal runtime ({self.max_runtime} seconds). '
                self.timeout(item_set, detail=detail, error=GT4SDTimeoutError)
                return
            generated_items = self.generate()
            for (index, item) in enumerate(generated_items):
                try:
                    valid_item = self.configuration.validate_item(item)
                    if not isinstance(item, collections.Hashable):
                        yield valid_item
                        item_set.add(str(index))
                    elif item in item_set:
                        continue
                    else:
                        yield valid_item
                        item_set.add(item)
                    if len(item_set) == number_of_items:
                        return
                except InvalidItem as error:
                    logger.debug(f'item {item} could not be validated, raising {error.title}: {error.detail}')
                    continue
            if len(item_set) == item_set_length:
                stuck_counter += 1
            else:
                stuck_counter = 0
            if stuck_counter >= gt4sd_configuration_instance.gt4sd_max_number_of_stuck_calls:
                prefix = 'No' if len(item_set) == 0 else 'No new'
                detail = f'{prefix} samples generated for more than {gt4sd_configuration_instance.gt4sd_max_number_of_stuck_calls} cycles. '
                self.timeout(item_set, detail=detail, error=GT4SDTimeoutError)
                return
            item_set_length = len(item_set)

    def validate_configuration(self, configuration: AlgorithmConfiguration) -> AlgorithmConfiguration:
        """Overload to validate the a configuration for the algorithm.

        Args:
            configuration: the algorithm configuration.

        Raises:
            InvalidAlgorithmConfiguration: in case the configuration for the algorithm is invalid.

        Returns:
            the validated configuration.
        """
        logger.info('no parameters validation')
        return configuration

class PredictorAlgorithm(ABC, Generic[S, T]):
    """Interface for automated prediction via an :class:`AlgorithmConfiguration`."""
    max_runtime: int = gt4sd_configuration_instance.gt4sd_max_runtime

    def __init__(self, configuration: AlgorithmConfiguration[S, T]):
        """Targeted or untargeted generation.

        Args:
            configuration: application specific helper that allows to setup the
                generator.
        """
        logger.info(f'runnning {self.__class__.__name__} with configuration={configuration}')
        self.configuration = configuration
        self.predictor = self.get_predictor(configuration)

    def get_predictor(self, configuration: AlgorithmConfiguration[S, T]) -> Predictor:
        """Set up the predictive model from the configuration. This is called at
            instantiation of the PredictorAlgorithm and must return a callable.

        Returns:
            predictor, a callable that takes an item and returns a prediction.
        """
        logger.info('ensure artifacts for the application are present.')
        self.local_artifacts = configuration.ensure_artifacts()
        model: Predictor = self.get_model(self.local_artifacts)
        return model

    @abstractmethod
    def get_model(self, resources_path: str) -> Predictor:
        """
        Restore the model from a local path.

        Note:
            This is the major method to implement in child classes, it is called
            at instantiation of the PredictorAlgorithm and must return a callable:

        Args:
            resources_path: local path to the downloaded artifacts.

        Returns:
            Predictor (callable)
        """
        raise NotImplementedError('Not implemented in baseclass.')

    def predict(self, input: Any) -> Any:
        """Perform a prediction for an input.
        Args:
            input: the input for the predictive model

        Raises:
            TimeoutError: when the walltime limit is hit.

        Returns:
            the prediction.
        """
        try:
            predicted = self.predictor(input)
        except TimeoutError:
            detail = f'Predicting took longer than maximum ({self.max_runtime} seconds).'
            logger.warning(detail + ' Exiting now!')
        except Exception:
            raise Exception(f'{self.__class__.__name__} failed with {input}')
        return predicted

    def __call__(self, input: Any) -> Any:
        """Alias for `self.predict`."""
        return self.predict(input)

@dataclass
class AlgorithmConfiguration(Generic[S, T]):
    """Algorithm parameter definitions and implementation setup.

    The signature of this class constructor (given by the instance attributes) is used
    for the REST API and needs to be serializable.

    Child classes will add additional instance attributes to configure their respective
    algorithms. This will require setting default values for all of the attributes defined
    here.
    However, the values for :attr:`algorithm_name` and :attr:`algorithm_application`
    are set the registering decorator.

    This strict setup has the following desired effects:

    - Ease child implementation. For example::

        from typing import ClassVar

        from gt4sd.algorithms.registry import ApplicationsRegistry
        from gt4sd.algorithms.core import AlgorithmConfiguration

        @ApplicationsRegistry.register_algorithm_application(ChildOfGeneratorAlgorithm)
        class ConfigurationForChildOfGeneratorAlgorithm(AlgorithmConfiguration):
            algorithm_type: ClassVar[str] = 'generation'
            domain: ClassVar[str] = 'materials'
            algorithm_version: str = 'version3.14'
            actual_parameter: float = 1.61

            # no __init__ definition required


    2. Retrieve the algorithm and configuration easily (via the four class attributes)
    from the :class:`ApplicationsRegistry<gt4sd.algorithms.registry.ApplicationsRegistry>`.
    For example::

       from gt4sd.algorithms.registry import ApplicationsRegistry

       application = ApplicationsRegistry.get_application(
            algorithm_type='generation',
            domain='materials',
            algorithm_name='ChildOfGeneratorAlgorithm',
            algorithm_application='ConfigurationForChildOfGeneratorAlgorithm',
        )
        Algorithm = application.algorithm_class
        Configuration = application.configuration_class

    3. An effortless validation at instantiation via :mod:`pydantic`.

    4. An effortless mapping to artifacts on s3, see :meth:`ensure_artifacts`.

    Todo:
        show how to register a configuration manually (in case it applies to multiple
        algorithms and/or applications)

    """
    algorithm_type: ClassVar[str]
    domain: ClassVar[str]
    algorithm_name: ClassVar[str]
    algorithm_application: ClassVar[str]
    algorithm_version: str = ''

    def get_target_description(self) -> Optional[Dict[str, str]]:
        """Get description of the target for generation.

        Returns:
            target description, returns None in case no target is used.
        """
        return {'title': 'Target for generation', 'type': 'object', 'description': 'Optional target for generation.'}

    def to_dict(self) -> Dict[str, Any]:
        """Represent the configuration as a dictionary.

        Returns:
            description of the configuration with parameters description.
        """
        base_configuration_fields_set = set(AlgorithmConfiguration.__dataclass_fields__.keys())
        application_configuration_dict = dict(description=self.__doc__)
        for (name, base_description) in self.__pydantic_model__.schema()['properties'].items():
            if name not in base_configuration_fields_set:
                description = dict(getattr(self.__dataclass_fields__[name], 'metadata', {}))
                description.update(base_description)
                if 'default' in description:
                    description['optional'] = True
                else:
                    description['optional'] = False
                application_configuration_dict[name] = description
        return application_configuration_dict

    def validate_item(self, item: Any) -> S:
        """Overload to validate an item.

        Args:
            item: validate an item.

        Raises:
            InvalidItem: in case the item can not be validated.

        Returns:
            S: the validated item.
        """
        return item

    @classmethod
    def get_application_prefix(cls) -> str:
        """Get prefix up to the specific application.

        Returns:
            the application prefix.
        """
        return os.path.join(cls.algorithm_type, cls.algorithm_name, cls.algorithm_application)

    @classmethod
    def list_versions(cls) -> Set[str]:
        """Get possible algorithm versions.

        S3 is searched as well as the local cache is searched for matching versions.

        Returns:
            viable values as :attr:`algorithm_version` for the environment.
        """
        prefix = cls.get_application_prefix()
        try:
            versions = get_algorithm_subdirectories_with_s3(prefix)
        except (KeyError, S3SyncError) as error:
            logger.info(f'searching S3 raised {error.__class__.__name__}, using local cache only.')
            logger.debug(error)
            versions = set()
        versions = versions.union(get_algorithm_subdirectories_in_cache(prefix))
        return versions

    @classmethod
    def list_remote_versions(cls, prefix) -> Set[str]:
        """Get possible algorithm versions on s3.
           Before uploading an artifact on S3, we need to check that
           a particular version is not already present and overwrite by mistake.
           If the final set is empty we can then upload the folder artifact.
           If the final set is not empty, we need to check that the specific version
           of interest is not present.

        only S3 is searched (not the local cache) for matching versions.

        Returns:
            viable values as :attr:`algorithm_version` for the environment.
        """
        if not prefix:
            prefix = cls.get_application_prefix()
        try:
            versions = get_algorithm_subdirectories_with_s3(prefix)
        except (KeyError, S3SyncError) as error:
            logger.info(f'searching S3 raised {error.__class__.__name__}. This means that no versions are available on S3.')
            logger.debug(error)
            versions = set()
        return versions

    @classmethod
    def get_filepath_mappings_for_training_pipeline_arguments(cls, training_pipeline_arguments: TrainingPipelineArguments) -> Dict[str, str]:
        """Ger filepath mappings for the given training pipeline arguments.

        Args:
            training_pipeline_arguments: training pipeline arguments.

        Raises:
            ValueError: in case no mapping is available.

        Returns:
            a mapping between artifacts' files and training pipeline's output files.
        """
        raise ValueError(f'{cls.__name__} artifacts not mapped for {training_pipeline_arguments}')

    @classmethod
    def save_version_from_training_pipeline_arguments_postprocess(cls, training_pipeline_arguments: TrainingPipelineArguments):
        """Postprocess after saving.

        Args:
            training_pipeline_arguments: training pipeline arguments.
        """
        pass

    @classmethod
    def save_version_from_training_pipeline_arguments(cls, training_pipeline_arguments: TrainingPipelineArguments, target_version: str, source_version: Optional[str]=None) -> None:
        """Save a version using training pipeline arguments.

        Args:
            training_pipeline_arguments: training pipeline arguments.
            target_version: target version used to save the model in the cache.
            source_version: source version to use for missing artifacts.
                Defaults to None, a.k.a., use the default version.
        """
        filepaths_mapping: Dict[str, str] = {}
        try:
            filepaths_mapping = cls.get_filepath_mappings_for_training_pipeline_arguments(training_pipeline_arguments=training_pipeline_arguments)
        except ValueError:
            logger.info(f'{cls.__name__} can not save a version based on {training_pipeline_arguments}')
        if len(filepaths_mapping) > 0:
            if source_version is None:
                source_version = cls.algorithm_version
            source_missing_path = cls.ensure_artifacts_for_version(source_version)
            target_path = os.path.join(get_cached_algorithm_path(), cls.get_application_prefix(), target_version)
            filepaths_mapping = {filename: source_filepath if os.path.exists(source_filepath) else os.path.join(source_missing_path, filename) for (filename, source_filepath) in filepaths_mapping.items()}
            logger.info(f'Saving artifacts into {target_path}...')
            try:
                os.makedirs(target_path)
            except OSError:
                logger.warning(f'Artifacts already existing in {target_path}, overwriting them...')
                os.makedirs(target_path, exist_ok=True)
            for (target_filename, source_filepath) in filepaths_mapping.items():
                target_filepath = os.path.join(target_path, target_filename)
                logger.info(f'Saving artifact {source_filepath} into {target_filepath}...')
                shutil.copyfile(source_filepath, target_filepath)
            cls.save_version_from_training_pipeline_arguments_postprocess(training_pipeline_arguments)
            logger.info(f'Artifacts saving completed into {target_path}')

    @classmethod
    def upload_version_from_training_pipeline_arguments_postprocess(cls, training_pipeline_arguments: TrainingPipelineArguments):
        """Postprocess after uploading. Not implemented yet.

        Args:
            training_pipeline_arguments: training pipeline arguments.
        """
        pass

    @classmethod
    def upload_version_from_training_pipeline_arguments(cls, training_pipeline_arguments: TrainingPipelineArguments, target_version: str, source_version: Optional[str]=None) -> None:
        """Upload a version using training pipeline arguments.

        Args:
            training_pipeline_arguments: training pipeline arguments.
            target_version: target version used to save the model in s3.
            source_version: source version to use for missing artifacts.
                Defaults to None, a.k.a., use the default version.
        """
        filepaths_mapping: Dict[str, str] = {}
        try:
            filepaths_mapping = cls.get_filepath_mappings_for_training_pipeline_arguments(training_pipeline_arguments=training_pipeline_arguments)
        except ValueError:
            logger.info(f'{cls.__name__} can not save a version based on {training_pipeline_arguments}')
        if len(filepaths_mapping) > 0:
            if source_version is None:
                source_version = cls.algorithm_version
            source_missing_path = cls.ensure_artifacts_for_version(source_version)
            prefix = cls.get_application_prefix()
            versions = cls.list_remote_versions(prefix)
            if target_version not in versions:
                logger.info(f'There is no version {target_version} in S3, starting upload...')
            else:
                logger.info(f'Version {target_version} already exists in S3, skipping upload...')
                return
            filepaths_mapping = {filename: source_filepath if os.path.exists(source_filepath) else os.path.join(source_missing_path, filename) for (filename, source_filepath) in filepaths_mapping.items()}
            logger.info(f'Uploading artifacts into {os.path.join(prefix, target_version)}...')
            try:
                for (target_filename, source_filepath) in filepaths_mapping.items():
                    target_filepath = os.path.join(prefix, target_version, target_filename)
                    upload_to_s3(target_filepath, source_filepath)
                    logger.info(f'Upload artifact {source_filepath} into {target_filepath}...')
            except S3SyncError:
                logger.warning('Problem with upload...')
                return
            logger.info(f'Artifacts uploading completed into {os.path.join(prefix, target_version)}')

    @classmethod
    def ensure_artifacts_for_version(cls, algorithm_version: str) -> str:
        """The artifacts matching the path defined by class attributes and the given version are downloaded.

        That is all objects under ``algorithm_type/algorithm_name/algorithm_application/algorithm_version``
        in the bucket are downloaded.

        Args:
            algorithm_version: version of the algorithm to ensure artifacts for.

        Returns:
            the common local path of the matching artifacts.
        """
        prefix = os.path.join(cls.get_application_prefix(), algorithm_version)
        try:
            local_path = sync_algorithm_with_s3(prefix)
        except (KeyError, S3SyncError) as error:
            logger.info(f'searching S3 raised {error.__class__.__name__}, using local cache only.')
            logger.debug(error)
            local_path = get_cached_algorithm_path(prefix)
            if not os.path.isdir(local_path):
                raise OSError(f'artifacts directory {local_path} does not exist locally, and syncing with s3 failed: {error}')
        return local_path

    def ensure_artifacts(self) -> str:
        """The artifacts matching the path defined by class attributes are downloaded.

        That is all objects under ``algorithm_type/algorithm_name/algorithm_application/algorithm_version``
        in the bucket are downloaded.

        Returns:
            the common local path of the matching artifacts.
        """
        return self.ensure_artifacts_for_version(self.algorithm_version)

class ConfigurablePropertyAlgorithmConfiguration(AlgorithmConfiguration):
    """A configurable AlgorithmConfiguration to be used by the properties submodule."""
    module: str = 'properties'

    def __init__(self, domain: str, algorithm_name: str, algorithm_application: str, algorithm_version: str='v0', algorithm_type: str='prediction'):
        """
        Args:
            domain: submodule of properties where the model resides.
            algorithm_version: name of the predictive model, e.g., `MCA`.
            algorithm_application: application of the algorithm, e.g., dataset it was
                trained on, like `Tox21`.
            algorithm_version: version of the algorithm, defaults to `v0`.
            algorithm_type: type of the algorithm. This should be `prediction`.
        """
        self.algorithm_type = algorithm_type
        self.domain = domain
        self.algorithm_name = algorithm_name
        self.algorithm_application = algorithm_application
        self.algorithm_version = algorithm_version

    def get_application_prefix(self) -> str:
        """Get prefix up to the specific application.

        NOTE: Unlike the parent method this uses the assgined attributes since it's
        configurable.

        Returns:
            the application prefix.
        """
        return os.path.join(self.domain, self.algorithm_name, self.algorithm_application)

    def ensure_artifacts_for_version(self, algorithm_version: str) -> str:
        """The artifacts matching the path defined by class attributes and the given version are downloaded.

        NOTE: Unlike the parent method this uses the assigned attributes since it's
        configurable.

        That is all objects under ``algorithm_type/algorithm_name/algorithm_application/algorithm_version``
        in the bucket are downloaded.

        Args:
            algorithm_version: version of the algorithm to ensure artifacts for.

        Returns:
            the common local path of the matching artifacts.
        """
        prefix = os.path.join(self.get_application_prefix(), algorithm_version)
        try:
            local_path = sync_algorithm_with_s3(prefix, module=self.module)
        except (KeyError, S3SyncError) as error:
            logger.info(f'searching S3 raised {error.__class__.__name__}, using local cache only.')
            logger.debug(error)
            local_path = get_cached_algorithm_path(prefix, module=self.module)
            if not os.path.isdir(local_path):
                raise OSError(f'artifacts directory {local_path} does not exist locally, and syncing with s3 failed: {error}')
        return local_path

    def list_versions(self) -> Set[str]:
        """Get possible algorithm versions.

        NOTE: Unlike the parent method this uses the assigned attributes since it's
        configurable.

        S3 is searched as well as the local cache is searched for matching versions.

        Returns:
            viable values as :attr:`algorithm_version` for the environment.
        """
        prefix = self.get_application_prefix()
        try:
            versions = get_algorithm_subdirectories_with_s3(prefix, module=self.module)
        except (KeyError, S3SyncError) as error:
            logger.info(f'searching S3 raised {error.__class__.__name__}, using local cache only.')
            logger.debug(error)
            versions = set()
        versions = versions.union(get_algorithm_subdirectories_in_cache(prefix, module=self.module))
        return versions

def get_configuration_class_with_attributes(klass: Type[AlgorithmConfiguration]) -> Type[AlgorithmConfiguration]:
    """Get AlgorithmConfiguration with set attributes.

    Args:
        klass: a class to be used to extract attributes from.

    Returns:
        a class with the attributes set.
    """
    configuration_class = deepcopy(AlgorithmConfiguration)
    setattr(configuration_class, 'algorithm_type', klass.algorithm_type)
    setattr(configuration_class, 'algorithm_name', klass.algorithm_name)
    setattr(configuration_class, 'algorithm_application', klass.__name__)
    setattr(configuration_class, 'algorithm_version', klass.algorithm_version)
    return configuration_class

class PropertyPredictor(ABC, Generic[S, U]):
    """TODO: Might be deprecated in future release."""

    def __init__(self, context: U) -> None:
        """Property predictor to investigate items.

        Args:
            context: the context in which a property of an item can be
                computed or checked is very application specific.
        """
        logger.warning('This class will be deprecated in a future release.')
        self.context = context

    @abstractmethod
    def satisfies(self, item: S) -> bool:
        """Check whether an item satisfies given requirements.

        Args:
            item: the item to check.

        Returns:
            bool:
        """

    def compute(self, item: S) -> Any:
        """Compute some metric/property on an item.

        Args:
            item: the item to compute a metric on.

        Returns:
            Any: the computed metric/property.
        """