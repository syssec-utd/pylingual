"""Base AutoML class."""
import logging
import os
from copy import copy
from typing import Any, Callable, Tuple, cast, Union
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from lightautoml.dataset.base import RolesDict
from lightautoml.reader.base import RolesDict
from lightautoml.utils.logging import set_stdout_level, verbosity_to_loglevel
from lightautoml.utils.timer import PipelineTimer
from pyspark.ml import PipelineModel, Transformer
from pyspark.sql.session import SparkSession
from .blend import SparkBlender, SparkBestModelSelector
from ..dataset.base import SparkDataset, PersistenceLevel, PersistenceManager
from ..dataset.persistence import PlainCachePersistenceManager
from ..pipelines.base import TransformerInputOutputRoles
from ..pipelines.features.base import SparkPipelineModel
from ..pipelines.ml.base import SparkMLPipeline
from ..reader.base import SparkToSparkReader
from ..utils import ColumnsSelectorTransformer, SparkDataFrame
from ..validation.base import SparkBaseTrainValidIterator
from ..validation.iterators import SparkFoldsIterator, SparkHoldoutIterator, SparkDummyIterator
logger = logging.getLogger(__name__)
ReadableIntoSparkDf = Union[str, SparkDataFrame]

class SparkAutoML(TransformerInputOutputRoles):
    """Class for compile full pipeline of AutoML task.

    AutoML steps:

        - Read, analyze data and get inner
          :class:`~lightautoml.dataset.base.LAMLDataset` from input
          dataset: performed by reader.
        - Create validation scheme.
        - Compute passed ml pipelines from levels.
          Each element of levels is list
          of :class:`~lightautoml.pipelines.ml.base.MLPipelines`
          prediction from current level are passed to next level
          pipelines as features.
        - Time monitoring - check if we have enough time to calc new pipeline.
        - Blend last level models and prune useless pipelines
          to speedup inference: performed by blender.
        - Returns prediction on validation data.
          If crossvalidation scheme is used,
          out-of-fold prediction will returned.
          If validation data is passed
          it will return prediction on validation dataset.
          In case of cv scheme when some point of train data
          never was used as validation (ex. timeout exceeded
          or custom cv iterator like
          :class:`~lightautoml.validation.np_iterators.TimeSeriesIterator`
          was used) NaN for this point will be returned.

    Example:
        Common usecase - create custom pipelines or presets.

        >>> reader = SparkToSparkReader()
        >>> pipe = SparkMLPipeline([SparkMLAlgo()])
        >>> levels = [[pipe]]
        >>> automl = SparkAutoML(reader, levels, )
        >>> automl.fit_predict(data, roles={'target': 'TARGET'})

    """

    def __init__(self, reader: Optional[SparkToSparkReader]=None, levels: Optional[Sequence[Sequence[SparkMLPipeline]]]=None, timer: Optional[PipelineTimer]=None, blender: Optional[SparkBlender]=None, skip_conn: bool=False, return_all_predictions: bool=False):
        """

        Args:
            reader: Instance of Reader class object that
              creates :class:`~lightautoml.dataset.base.LAMLDataset`
              from input data.
            levels: List of list
              of :class:`~lightautoml.pipelines.ml..base.MLPipelines`.
            timer: Timer instance of
              :class:`~lightautoml.utils.timer.PipelineTimer`.
              Default - unlimited timer.
            blender: Instance of Blender.
              Default - :class:`~lightautoml.automl.blend.BestModelSelector`.
            skip_conn: True if we should pass first level
              input features to next levels.

        Note:
            There are several verbosity levels:

                - `0`: No messages.
                - `1`: Warnings.
                - `2`: Info.
                - `3`: Debug.

        """
        super().__init__()
        self.levels: Optional[Sequence[Sequence[SparkMLPipeline]]] = None
        self._transformer = None
        self._input_roles: Optional[RolesDict] = None
        self._output_roles: Optional[RolesDict] = None
        self._service_columns: Optional[List[str]] = None
        self._persistence_manager: Optional[PersistenceManager] = None
        if reader and levels:
            self._initialize(reader, levels, timer, blender, skip_conn, return_all_predictions)

    @property
    def input_roles(self) -> Optional[RolesDict]:
        return self._input_roles

    @property
    def output_roles(self) -> Optional[RolesDict]:
        return self._output_roles

    @property
    def persistence_manager(self) -> Optional[PersistenceManager]:
        return self._persistence_manager

    def transformer(self, return_all_predictions: bool=False, add_array_attrs: bool=True, **reader_args) -> SparkPipelineModel:
        if not return_all_predictions:
            blender = [self.blender.transformer()]
            output_roles = self.blender.output_roles
        else:
            blender = []
            output_roles = {**(ml_pipe.output_roles for ml_pipe in self.levels[-1])}
        sel_tr = ColumnsSelectorTransformer(name='SparkAutoML', input_cols=[SparkDataset.ID_COLUMN] + list(output_roles.keys()), optional_cols=[self.reader.target_col] if self.reader.target_col else [])
        stages = [self.reader.transformer(add_array_attrs=add_array_attrs, **reader_args), *(ml_pipe.transformer() for level in self.levels for ml_pipe in level), *blender, sel_tr]
        return SparkPipelineModel(stages, input_roles=self.input_roles, output_roles=output_roles)

    def _initialize(self, reader: SparkToSparkReader, levels: Sequence[Sequence[SparkMLPipeline]], timer: Optional[PipelineTimer]=None, blender: Optional[SparkBlender]=None, skip_conn: bool=False, return_all_predictions: bool=False):
        """Same as __init__. Exists for delayed initialization in presets.

        Args:
            reader: Instance of Reader class object that
              creates :class:`~lightautoml.dataset.base.LAMLDataset`
              from input data.
            levels: List of list
              of :class:`~lightautoml.pipelines.ml..base.MLPipelines`.
            timer: Timer instance of
              :class:`~lightautoml.utils.timer.PipelineTimer`.
              Default - unlimited timer.
            blender: Instance of Blender.
              Default - :class:`~lightautoml.automl.blend.BestModelSelector`.
            skip_conn: True if we should pass first level
              input features to next levels.
            return_all_predictions: True if we should return all predictions from last
              level models.

        """
        assert len(levels) > 0, 'At least 1 level should be defined'
        self.timer = timer
        if timer is None:
            self.timer = PipelineTimer()
        self.reader = reader
        self._levels = levels
        self.blender = blender
        if blender is None:
            self.blender = SparkBestModelSelector()
        for i, lvl in enumerate(self._levels):
            for j, pipe in enumerate(lvl):
                pipe.upd_model_names('Lvl_{0}_Pipe_{1}'.format(i, j))
        self.skip_conn = skip_conn
        self.return_all_predictions = return_all_predictions

    def fit_predict(self, train_data: Any, roles: dict, train_features: Optional[Sequence[str]]=None, cv_iter: Optional[Iterable]=None, valid_data: Optional[Any]=None, valid_features: Optional[Sequence[str]]=None, verbose: int=0, persistence_manager: Optional[PersistenceManager]=None) -> SparkDataset:
        """Fit on input data and make prediction on validation part.

        Args:
            train_data: Dataset to train.
            roles: Roles dict.
            train_features: Optional features names,
              if cannot be inferred from train_data.
            cv_iter: Custom cv iterator. For example,
              :class:`~lightautoml.validation.np_iterators.TimeSeriesIterator`.
            valid_data: Optional validation dataset.
            valid_features: Optional validation dataset
              features if can't be inferred from `valid_data`.
            verbose: controls verbosity

        Returns:
            Predicted values.

        """
        set_stdout_level(verbosity_to_loglevel(verbose))
        self.timer.start()
        self._persistence_manager = persistence_manager or PlainCachePersistenceManager()
        train_dataset = self.reader.fit_read(train_data, train_features, roles, persistence_manager=self._persistence_manager)
        train_dataset = train_dataset.persist(level=PersistenceLevel.REGULAR)
        assert len(self._levels) <= 1 or train_dataset.folds is not None, 'Not possible to fit more than 1 level without cv folds'
        assert len(self._levels) <= 1 or valid_data is None, 'Not possible to fit more than 1 level with holdout validation'
        if valid_data:
            valid_dataset = self.reader.read(valid_data, valid_features, add_array_attrs=True).persist(PersistenceLevel.READER)
        else:
            valid_dataset = None
        train_valid = self._create_validation_iterator(train_dataset, valid_dataset, None, cv_iter=cv_iter)
        pipes: List[SparkMLPipeline] = []
        self.levels = []
        level_ds: Optional[SparkDataset] = None
        for leven_number, level in enumerate(self._levels, 1):
            pipes = []
            flg_last_level = leven_number == len(self._levels)
            logger.info(f'Layer \x1b[1m{leven_number}\x1b[0m train process start. Time left {self.timer.time_left:.2f} secs')
            all_pipes_predictions: List[SparkDataset] = []
            with train_valid.frozen() as frozen_train_valid:
                for k, ml_pipe in enumerate(level):
                    pipe_predictions = cast(SparkDataset, ml_pipe.fit_predict(frozen_train_valid)).persist(level=PersistenceLevel.CHECKPOINT, force=True)
                    all_pipes_predictions.append(pipe_predictions)
                    pipes.append(ml_pipe)
                    logger.info('Time left {:.2f} secs\n'.format(self.timer.time_left))
                    if self.timer.time_limit_exceeded():
                        logger.info('Time limit exceeded. Last level models will be blended and unused pipelines will be pruned.\n')
                        flg_last_level = True
                        break
                    elif self.timer.child_out_of_time:
                        logger.info('Time limit exceeded in one of the tasks. AutoML will blend level {0} models.\n'.format(leven_number))
                        flg_last_level = True
            logger.info('\x1b[1mLayer {} training completed.\x1b[0m\n'.format(leven_number))
            level_ds_name = f'all_piped_predictions_level_{leven_number}'
            if flg_last_level:
                level_ds = SparkDataset.concatenate(all_pipes_predictions, name=level_ds_name)
                train_valid.unpersist()
                break
            self.levels.append(pipes)
            level = [train_valid.get_validation_data(), *all_pipes_predictions] if self.skip_conn else all_pipes_predictions
            name = f'{level_ds_name}_skip_conn' if self.skip_conn else level_ds_name
            level_ds = SparkDataset.concatenate(level, name=name)
            train_valid.unpersist(skip_val=self.skip_conn)
            train_valid = self._create_validation_iterator(level_ds, None, n_folds=None, cv_iter=None)
        blended_prediction, last_pipes = self.blender.fit_predict(level_ds, pipes)
        self.levels.append(last_pipes)
        del self._levels
        oof_pred = level_ds if self.return_all_predictions else blended_prediction
        self._input_roles = copy(train_dataset.roles)
        self._output_roles = copy(oof_pred.roles)
        self._service_columns = train_dataset.service_columns
        return oof_pred

    def predict(self, data: ReadableIntoSparkDf, return_all_predictions: Optional[bool]=None, add_reader_attrs: bool=False, persistence_manager: Optional[PersistenceManager]=None) -> SparkDataset:
        """Get dataset with predictions.

        Almost same as :meth:`lightautoml.automl.base.AutoML.predict`
        on new dataset, with additional features.

        Additional features - working with different data formats.
        Supported now:

            - Path to ``.csv``, ``.parquet``, ``.feather`` files.
            - :class:`~numpy.ndarray`, or dict of :class:`~numpy.ndarray`. For example,
              ``{'data': X...}``. In this case roles are optional,
              but `train_features` and `valid_features` required.
            - :class:`pandas.DataFrame`.

        Parallel inference - you can pass ``n_jobs`` to speedup
        prediction (requires more RAM).
        Batch_inference - you can pass ``batch_size``
        to decrease RAM usage (may be longer).

        Args:
            data: Dataset to perform inference.
            features_names: Optional features names,
              if cannot be inferred from `train_data`.
            return_all_predictions: if True,
              returns all model predictions from last level
            add_reader_attrs: if True,
              the reader's attributes will be added to the SparkDataset

        Returns:
            Dataset with predictions.

        """
        persistence_manager = persistence_manager or PlainCachePersistenceManager()
        transformer = self.transformer(return_all_predictions=return_all_predictions, add_array_attrs=add_reader_attrs)
        data = self._read_data(data)
        predictions = transformer.transform(data)
        sds = SparkDataset(data=predictions, roles=copy(transformer.get_output_roles()), task=self.reader.task, persistence_manager=persistence_manager, target=self.reader.target_col)
        return sds

    def collect_used_feats(self) -> List[str]:
        """Get feats that automl uses on inference.

        Returns:
            Features names list.

        """
        used_feats = set()
        for lvl in self.levels:
            for pipe in lvl:
                used_feats.update(pipe.used_features)
        used_feats = list(used_feats)
        return used_feats

    def collect_model_stats(self) -> Dict[str, int]:
        """Collect info about models in automl.

        Returns:
            Dict with models and its runtime numbers.

        """
        model_stats = {}
        for lvl in self.levels:
            for pipe in lvl:
                for ml_algo in pipe.ml_algos:
                    model_stats[ml_algo.name] = len(ml_algo.models)
        return model_stats

    def _create_validation_iterator(self, train: SparkDataset, valid: Optional[SparkDataset], n_folds: Optional[int], cv_iter: Optional[Callable]) -> SparkBaseTrainValidIterator:
        train = train.persist(level=PersistenceLevel.REGULAR)
        if valid:
            valid = valid.persist(level=PersistenceLevel.REGULAR)
            iterator = SparkHoldoutIterator(train, valid)
        elif cv_iter:
            raise NotImplementedError('Not supported now')
        elif train.folds:
            iterator = SparkFoldsIterator(train, n_folds)
        else:
            iterator = SparkDummyIterator(train)
        logger.info(f'Using train valid iterator of type: {type(iterator)}')
        return iterator

    def _get_service_columns(self) -> List[str]:
        return self._service_columns

    def _build_transformer(self, no_reader: bool=False, return_all_predictions: bool=False) -> Tuple[Transformer, RolesDict]:
        stages = []
        if not no_reader:
            stages.append(self.reader.transformer(add_array_attrs=True))
        ml_pipes = [ml_pipe.transformer() for level in self.levels for ml_pipe in level]
        stages.extend(ml_pipes)
        if not return_all_predictions:
            stages.append(self.blender.transformer())
            output_roles = self.blender.output_roles
        else:
            output_roles = dict()
            for ml_pipe in self.levels[-1]:
                output_roles.update(ml_pipe.output_roles)
        sel_tr = ColumnsSelectorTransformer(name='SparkAutoML', input_cols=[SparkDataset.ID_COLUMN] + list(output_roles.keys()), optional_cols=[self.reader.target_col] if self.reader.target_col else [])
        stages.append(sel_tr)
        automl_transformer = PipelineModel(stages=stages)
        return (automl_transformer, output_roles)

    def _read_data(self, data: ReadableIntoSparkDf, features: Optional[List[str]]=None) -> SparkDataFrame:
        """Get :class:`~pyspark.sql.DataFrame` from different data formats.

        Note:
            Supported now data formats:

                - Path to ``.csv``, ``.parquet``, ``.feather`` files.
                - :class:`~numpy.ndarray`, or dict of :class:`~numpy.ndarray`.
                  For example, ``{'data': X...}``. In this case,
                  roles are optional, but `train_features`
                  and `valid_features` required.
                - :class:`pandas.DataFrame`.

        Args:
            data: Readable to DataFrame data.
            features_names: Optional features names if ``numpy.ndarray``.
            n_jobs: Number of processes to read file.
            read_csv_params: Params to read csv file.

        Returns:
            Tuple with read data and new roles mapping.

        """
        spark = SparkSession.getActiveSession()
        if isinstance(data, SparkDataFrame):
            out_sdf = data
        elif isinstance(data, str):
            path = cast(str, data)
            if path.endswith('.parquet'):
                out_sdf = spark.read.parquet(path)
            elif path.endswith('.csv'):
                csv_params = self._get_read_csv_params()
                out_sdf = spark.read.csv(path, **csv_params)
            else:
                raise ValueError(f'Unsupported data format: {os.path.splitext(path)[1]}')
        else:
            raise ValueError('Input data format is not supported')
        out_sdf = out_sdf.select(*features) if features is not None else out_sdf
        return out_sdf

    def _get_read_csv_params(self) -> Dict:
        return {}