__author__ = 'yangjian'
'\n\n'
import copy
import math
import time
from collections import OrderedDict
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import get_scorer
from hypernets.core import set_random_state
from hypernets.experiment import Experiment
from hypernets.experiment.cfg import ExperimentCfg as cfg
from hypernets.tabular import get_tool_box
from hypernets.tabular.cache import cache
from hypernets.utils import logging, const, df_utils
logger = logging.get_logger(__name__)
DEFAULT_EVAL_SIZE = 0.3
GB = 1024 ** 3
DATA_ADAPTION_TARGET_CUML_ALIASES = {'cuml', 'cuda', 'cudf', 'gpu'}

def _set_log_level(log_level):
    logging.set_level(log_level)

def _generate_dataset_id(X_train, y_train, X_test, X_eval, y_eval):
    tb = get_tool_box(X_train, y_train, X_test, X_eval, y_eval)
    try:
        if hasattr(y_train, 'values'):
            y_train = y_train.values
        if hasattr(y_eval, 'values'):
            y_eval = y_eval.values
    except:
        pass
    sign = tb.data_hasher()([X_train, y_train, X_test, X_eval, y_eval])
    return sign

def _sample_by_classes(X, y, class_size, random_state=None, copy_data=True):
    if X is None or y is None:
        return (None, None)
    tb = get_tool_box(X, y)
    name_y = '__experiment_y_tmp__'
    df = X.copy() if copy_data else X
    df[name_y] = y
    uniques = set(tb.unique(y))
    parts = {c: df[df[name_y] == c] for c in uniques}
    dfs = [tb.train_test_split(part, train_size=class_size[c], random_state=random_state)[0] if c in class_size.keys() else part for (c, part) in parts.items()]
    df = tb.concat_df(dfs, repartition=True, random_state=random_state)
    if logger.is_info_enabled():
        logger.info(f'sample_by_classes: {tb.value_counts(df[name_y])}')
    y = df.pop(name_y)
    return (df, y)

class StepNames:
    DATA_ADAPTION = 'data_adaption'
    DATA_CLEAN = 'data_clean'
    FEATURE_GENERATION = 'feature_generation'
    MULITICOLLINEARITY_DETECTION = 'multicollinearity_detection'
    DRIFT_DETECTION = 'drift_detection'
    FEATURE_IMPORTANCE_SELECTION = 'feature_selection'
    SPACE_SEARCHING = 'space_searching'
    ENSEMBLE = 'ensemble'
    TRAINING = 'training'
    PSEUDO_LABELING = 'pseudo_labeling'
    FEATURE_RESELECTION = 'feature_reselection'
    FINAL_SEARCHING = 'two_stage_searching'
    FINAL_ENSEMBLE = 'final_ensemble'
    FINAL_TRAINING = 'final_train'

class ExperimentStep(BaseEstimator):
    STATUS_NONE = -1
    STATUS_SUCCESS = 0
    STATUS_FAILED = 1
    STATUS_SKIPPED = 2
    STATUS_RUNNING = 10

    def __init__(self, experiment, name):
        super(ExperimentStep, self).__init__()
        self.name = name
        self.experiment = experiment
        self.input_features_ = None
        self.status_ = self.STATUS_NONE
        self.start_time = None
        self.done_time = None

    def step_progress(self, *args, **kwargs):
        if self.experiment is not None:
            self.experiment.step_progress(*args, **kwargs)

    @property
    def task(self):
        return self.experiment.task if self.experiment is not None else None

    @property
    def elapsed_seconds(self):
        if self.start_time is not None:
            if self.done_time is not None:
                return self.done_time - self.start_time
            else:
                return time.time() - self.start_time
        else:
            return None

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        self.input_features_ = X_train.columns.to_list()
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def transform(self, X, y=None, **kwargs):
        raise NotImplemented()

    def is_transform_skipped(self):
        return False

    def get_fitted_params(self):
        return {'input_features': self.input_features_}

    @classmethod
    def _get_param_names(cls):
        params = super()._get_param_names()
        return filter(lambda x: x != 'experiment', params)

    def __getstate__(self):
        state = super().__getstate__()
        if 'experiment' in state.keys():
            state['experiment'] = None
        return state

    def _repr_df_(self):
        init_params = self.get_params()
        fitted_params = self.get_fitted_params()
        init_df = pd.Series(init_params, name='value').to_frame()
        init_df['kind'] = 'settings'
        fitted_df = pd.Series(fitted_params, name='value').to_frame()
        fitted_df['kind'] = 'fitted'
        df = pd.concat([init_df, fitted_df], axis=0)
        df['key'] = df.index
        df = df.set_index(['kind', 'key'])
        return df

    def _repr_html_(self):
        df = self._repr_df_()
        html = f'<h2>{self.name}</h2>{df._repr_html_()}'
        return html

class FeatureSelectStep(ExperimentStep):

    def __init__(self, experiment, name):
        super().__init__(experiment, name)
        self.selected_features_ = None

    def transform(self, X, y=None, **kwargs):
        if self.selected_features_ is not None:
            if logger.is_debug_enabled():
                msg = f'{self.name} transform from {len(X.columns.tolist())} to {len(self.selected_features_)} features'
                logger.debug(msg)
            X = X[self.selected_features_]
        return X

    def cache_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        if self.selected_features_ is not None:
            features = self.selected_features_
            X_train = X_train[features]
            if X_test is not None:
                X_test = X_test[features]
            if X_eval is not None:
                X_eval = X_eval[features]
            if logger.is_info_enabled():
                logger.info(f'{self.name} cache_transform: {len(X_train.columns)} columns kept.')
        elif logger.is_info_enabled():
            logger.info(f'{self.name} cache_transform: {len(X_train.columns)} columns kept (do nothing).')
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def is_transform_skipped(self):
        return self.selected_features_ is None

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'selected_features': self.selected_features, 'unselected_features': self.unselected_features}

    @property
    def selected_features(self):
        if self.input_features_ is None:
            raise ValueError('Not fitted.')
        r = self.selected_features_ if self.selected_features_ is not None else self.input_features_
        return copy.copy(r)

    @property
    def unselected_features(self):
        if self.input_features_ is None:
            raise ValueError('Not fitted.')
        if self.selected_features_ is None:
            unselected = []
        else:
            unselected = list(filter(lambda _: _ not in self.selected_features_, self.input_features_))
        return unselected

class DataAdaptionStep(FeatureSelectStep):

    def __init__(self, experiment, name, target=None, memory_limit=0.05, min_cols=0.3):
        assert isinstance(memory_limit, (int, float)) and memory_limit > 0
        super().__init__(experiment, name)
        self.target = target
        self.memory_limit = memory_limit
        self.min_cols = min_cols
        self.input_feature_importances_ = None

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        assert self.target is None or isinstance(X_train, pd.DataFrame), f'Only pandas/numpy data can be adapted to {self.target}'
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        (tb, tb_target) = self.get_tool_box_with_target(X_train, y_train, X_test, X_eval, y_eval)
        memory_usage = tb.memory_usage(X_train, y_train, X_test, X_eval, y_eval)
        if isinstance(self.memory_limit, float) and 0.0 < self.memory_limit < 1.0:
            if tb is tb_target:
                memory_free = tb.memory_free() + memory_usage
            else:
                memory_free = tb_target.memory_free()
            memory_limit = self.memory_limit * memory_free
        else:
            memory_limit = int(self.memory_limit)
        if logger.is_info_enabled():
            logger.info(f'{self.name} original data memory usage:{memory_usage / GB:.3f}, limit: {memory_limit / GB:.3f}GB')
        if memory_usage > memory_limit:
            exp = self.experiment
            exp.X_train = None
            exp.y_train = None
            exp.X_eval = None
            exp.y_eval = None
            exp.X_test = None
            if isinstance(self.min_cols, float) and 0.0 < self.min_cols < 1.0:
                min_cols = int(self.min_cols * X_train.shape[1])
            else:
                min_cols = int(self.min_cols)
            min_cols_limit = cfg.experiment_data_adaption_min_cols_limit
            if min_cols < min_cols_limit:
                min_cols = min(min_cols_limit, X_train.shape[1])
            frac = memory_limit / memory_usage
            if frac * X_train.shape[1] < min_cols:
                f = frac * X_train.shape[1] / min_cols
                (X_train, y_train, X_test, X_eval, y_eval) = self.compact_by_rows(X_train, y_train, X_test, X_eval, y_eval, f)
                tb.gc()
            if min_cols < X_train.shape[1]:
                memory_usage = tb.memory_usage(X_train, y_train, X_test, X_eval, y_eval)
                frac = memory_limit / memory_usage
                (X_train, y_train, X_test, X_eval, y_eval) = self.compact_by_columns(X_train, y_train, X_test, X_eval, y_eval, frac)
                tb.gc()
            if logger.is_info_enabled():
                memory_usage = tb.memory_usage(X_train, y_train, X_test, X_eval, y_eval)
                memory_free = tb.memory_free()
                logger.info(f'{self.name} adapted X_train:{tb.get_shape(X_train)}, X_test:{tb.get_shape(X_test, allow_none=True)}, X_eval:{tb.get_shape(X_eval, allow_none=True)}. memory usage: {memory_usage / GB:.3f}GB, memory free: {memory_free / GB:.3f}')
            exp.X_train = X_train
            exp.y_train = y_train
            exp.X_eval = X_eval
            exp.y_eval = y_eval
            exp.X_test = X_test
            self.selected_features_ = X_train.columns.to_list()
        else:
            self.selected_features_ = None
        if tb_target is not tb:
            logger.info(f'{self.name} adapt local data with {tb_target}')
            (X_train, y_train, X_test, X_eval, y_eval) = tb_target.from_local(X_train, y_train, X_test, X_eval, y_eval)
            tb.gc()
            tb_target.gc()
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_tool_box_with_target(self, *data):
        tb = get_tool_box(*data)
        if self.target is None:
            tb_target = tb
        elif isinstance(self.target, str) and self.target.lower() in DATA_ADAPTION_TARGET_CUML_ALIASES:
            import cudf
            tb_target = get_tool_box(cudf.DataFrame)
        else:
            tb_target = get_tool_box(self.target)
        return (tb, tb_target)

    def compact_by_rows(self, X_train, y_train, X_test, X_eval, y_eval, frac):
        (X_train, y_train) = self.sample(X_train, y_train, frac)
        if X_eval is not None:
            (X_eval, y_eval) = self.sample(X_eval, y_eval, frac)
        if X_test is not None:
            (X_test, _) = self.sample(X_test, None, frac)
        return (X_train, y_train, X_test, X_eval, y_eval)

    def compact_by_columns(self, X_train, y_train, X_test, X_eval, y_eval, frac):
        tb = get_tool_box(X_train, y_train, X_test, X_eval, y_eval)
        memory_usage = tb.memory_usage(X_train, y_train)
        memory_free = tb.memory_free()
        f_sample = memory_free / (memory_usage * 12)
        if f_sample < 1.0:
            logger.info(f'sample train data {f_sample} to calculate feature importances')
            (X, y) = self.sample(X_train, y_train, f_sample)
        else:
            (X, y) = (X_train, y_train)
        tf_cls = tb.transformers['FeatureImportancesSelectionTransformer']
        tf = tf_cls(task=self.task, strategy='number', number=frac)
        tf.fit(X, y)
        X_train = tf.transform(X_train)
        if X_eval is not None:
            X_eval = tf.transform(X_eval)
        if X_test is not None:
            X_test = tf.transform(X_test)
        self.input_feature_importances_ = tf.feature_importances_
        return (X_train, y_train, X_test, X_eval, y_eval)

    def sample(self, X, y, frac):
        tb = get_tool_box(X, y)
        options = {}
        task = self.task
        if y is not None and task == const.TASK_BINARY:
            vn = pd.Series(tb.value_counts(y)).sort_values()
            vn_sampled = (vn * frac).astype('int')
            delta = (min(vn.values[0], vn_sampled.values[1]) - vn_sampled.values[0]) // 4
            vn_sampled = vn_sampled + np.array([delta, -delta])
            sample_size = (vn_sampled / vn).to_dict()
            (X, y) = _sample_by_classes(X, y, class_size=sample_size, random_state=self.experiment.random_state, copy_data=False)
        else:
            if y is not None and task != const.TASK_REGRESSION:
                options['stratify'] = y
            (X, _, y, _) = tb.train_test_split(X, y, train_size=frac, **options)
        return (X, y)

class DataCleanStep(FeatureSelectStep):

    def __init__(self, experiment, name, data_cleaner_args=None, cv=False, train_test_split_strategy=None):
        super().__init__(experiment, name)
        self.data_cleaner_args = data_cleaner_args if data_cleaner_args is not None else {}
        self.cv = cv
        self.train_test_split_strategy = train_test_split_strategy
        self.data_cleaner_ = get_tool_box(pd.DataFrame).data_cleaner(**self.data_cleaner_args)
        self.detector_ = None
        self.data_shapes_ = None

    @cache(arg_keys='X_train,y_train,X_test,X_eval,y_eval', strategy='transform', transformer='cache_transform', attrs_to_restore='input_features_,selected_features_,data_cleaner_,detector_')
    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        tb = get_tool_box(X_train)
        if self.cv and X_eval is not None and (y_eval is not None):
            logger.info(f'{self.name} cv enabled, so concat train data and eval data')
            X_train = tb.concat_df([X_train, X_eval], axis=0)
            y_train = tb.concat_df([y_train, y_eval], axis=0)
            X_eval = None
            y_eval = None
        data_cleaner = tb.data_cleaner(**self.data_cleaner_args)
        logger.info(f'{self.name} fit_transform with train data')
        (X_train, y_train) = data_cleaner.fit_transform(X_train, y_train)
        self.step_progress('fit_transform train set')
        if X_test is not None:
            logger.info(f'{self.name} transform test data')
            X_test = data_cleaner.transform(X_test)
            self.step_progress('transform X_test')
        if not self.cv:
            if X_eval is None or y_eval is None:
                eval_size = self.experiment.eval_size
                random_state = self.experiment.random_state
                if self.train_test_split_strategy == 'adversarial_validation' and X_test is not None:
                    logger.debug('DriftDetector.train_test_split')
                    detector = tb.drift_detector(random_state=random_state)
                    detector.fit(X_train, X_test)
                    self.detector_ = detector
                    (X_train, X_eval, y_train, y_eval) = detector.train_test_split(X_train, y_train, test_size=eval_size)
                elif self.task == const.TASK_REGRESSION:
                    (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_train, y_train, test_size=eval_size, random_state=random_state)
                else:
                    (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_train, y_train, test_size=eval_size, random_state=random_state, stratify=y_train)
                if self.task != const.TASK_REGRESSION:
                    y_train_uniques = tb.unique(y_train)
                    y_eval_uniques = tb.unique(y_eval)
                    if y_train_uniques != y_eval_uniques:
                        vn_train = tb.value_counts(y_train)
                        vn_eval = tb.value_counts(y_eval)
                        raise ValueError(f'The classes of `y_train` and `y_eval` must be equal, try to increase eval_size.your y_train [{len(y_train)}] :{vn_train} , y_eval [{len(y_eval)}] : {vn_eval}')
                self.step_progress('split into train set and eval set')
            else:
                (X_eval, y_eval) = data_cleaner.transform(X_eval, y_eval)
                self.step_progress('transform eval set')
        selected_features = X_train.columns.to_list()
        data_shapes = {'X_train.shape': tb.get_shape(X_train), 'y_train.shape': tb.get_shape(y_train), 'X_eval.shape': None if X_eval is None else tb.get_shape(X_eval), 'y_eval.shape': None if y_eval is None else tb.get_shape(y_eval), 'X_test.shape': None if X_test is None else tb.get_shape(X_test)}
        logger.info(f'{self.name} keep {len(selected_features)} columns')
        self.selected_features_ = selected_features
        self.data_cleaner_ = data_cleaner
        self.data_shapes_ = data_shapes
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_params(self, deep=True):
        params = super(DataCleanStep, self).get_params()
        params['data_cleaner_args'] = self.data_cleaner_.get_params()
        return params

    def cache_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        tb = get_tool_box(X_train)
        if self.cv and X_eval is not None and (y_eval is not None):
            logger.info(f'{self.name} cv enabled, so concat train data and eval data')
            X_train = tb.concat_df([X_train, X_eval], axis=0)
            y_train = tb.concat_df([y_train, y_eval], axis=0)
            X_eval = None
            y_eval = None
        data_cleaner = self.data_cleaner_
        logger.info(f'{self.name} transform train data')
        (X_train, y_train) = data_cleaner.transform(X_train, y_train)
        self.step_progress('fit_transform train set')
        if X_test is not None:
            logger.info(f'{self.name} transform test data')
            X_test = data_cleaner.transform(X_test)
            self.step_progress('transform X_test')
        if not self.cv:
            if X_eval is None or y_eval is None:
                eval_size = self.experiment.eval_size
                random_state = self.experiment.random_state
                if self.train_test_split_strategy == 'adversarial_validation' and X_test is not None:
                    logger.debug('DriftDetector.train_test_split')
                    detector = self.detector_
                    (X_train, X_eval, y_train, y_eval) = detector.train_test_split(X_train, y_train, test_size=eval_size)
                elif self.task == const.TASK_REGRESSION:
                    (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_train, y_train, test_size=eval_size, random_state=random_state)
                else:
                    (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_train, y_train, test_size=eval_size, random_state=random_state, stratify=y_train)
                if self.task != const.TASK_REGRESSION:
                    y_train_uniques = tb.unique(y_train)
                    y_eval_uniques = tb.unique(y_eval)
                    if y_train_uniques != y_eval_uniques:
                        vn_train = tb.value_counts(y_train)
                        vn_eval = tb.value_counts(y_eval)
                        raise ValueError(f'The classes of `y_train` and `y_eval` must be equal, try to increase eval_size.your y_train [{len(y_train)}] :{vn_train} , y_eval [{len(y_eval)}] : {vn_eval}')
                self.step_progress('split into train set and eval set')
            else:
                (X_eval, y_eval) = data_cleaner.transform(X_eval, y_eval)
                self.step_progress('transform eval set')
        selected_features = self.selected_features_
        data_shapes = {'X_train.shape': tb.get_shape(X_train), 'y_train.shape': tb.get_shape(y_train), 'X_eval.shape': tb.get_shape(X_eval, allow_none=True), 'y_eval.shape': tb.get_shape(y_eval, allow_none=True), 'X_test.shape': tb.get_shape(X_test, allow_none=True)}
        logger.info(f'{self.name} keep {len(selected_features)} columns')
        self.data_shapes_ = data_shapes
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def transform(self, X, y=None, **kwargs):
        return self.data_cleaner_.transform(X, None, **kwargs)

    def get_fitted_params(self):
        dc = self.data_cleaner_

        def get_reason(c):
            if dc is None:
                return 'unknown'
            if dc.dropped_constant_columns_ is not None and c in dc.dropped_constant_columns_:
                return 'constant'
            elif dc.dropped_idness_columns_ is not None and c in dc.dropped_idness_columns_:
                return 'idness'
            elif dc.dropped_duplicated_columns_ is not None and c in dc.dropped_duplicated_columns_:
                return 'duplicated'
            else:
                return 'others'
        params = super().get_fitted_params()
        data_shapes = self.data_shapes_ if self.data_shapes_ is not None else {}
        unselected_features = params.get('unselected_features', [])
        if dc is not None and unselected_features is not None:
            unselected_reason = {f: get_reason(f) for f in unselected_features}
        else:
            unselected_reason = None
        return {**params, **data_shapes, 'unselected_reason': unselected_reason}

    def as_local(self):
        if hasattr(self.data_cleaner_, 'as_local'):
            target = copy.copy(self)
            target.data_cleaner_ = self.data_cleaner_.as_local()
            return target
        else:
            return self

class TransformerAdaptorStep(ExperimentStep):

    def __init__(self, experiment, name, transformer_creator, **kwargs):
        assert transformer_creator is not None
        self.transformer_creator = transformer_creator
        self.transformer_kwargs = kwargs
        super(TransformerAdaptorStep, self).__init__(experiment, name)
        self.transformer_ = None

    @cache(arg_keys='X_train, y_train, X_test, X_eval, y_eval', strategy='transform', transformer='cache_transform', attrs_to_restore='input_features_,transformer_kwargs,transformer_')
    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        logger.info(f'{self.name} fit')
        init_kwargs = self.transformer_kwargs.copy()
        if 'task' in init_kwargs.keys():
            init_kwargs['task'] = self.task
        transformer = self.transformer_creator(**init_kwargs)
        transformer.fit(X_train, y_train, **kwargs)
        self.transformer_ = transformer
        return self.cache_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval, **kwargs)

    def cache_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        logger.info(f'{self.name} cache_transform')
        transformer = self.transformer_
        X_train = transformer.transform(X_train)
        if X_eval is not None:
            X_eval = transformer.transform(X_eval, y_eval)
        if X_test is not None:
            X_test = transformer.transform(X_test)
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def transform(self, X, y=None, **kwargs):
        logger.info(f'{self.name} transform')
        if y is None:
            return self.transformer_.transform(X)
        else:
            return self.transformer_.transform(X, y)

    def __getattribute__(self, item):
        try:
            return super(TransformerAdaptorStep, self).__getattribute__(item)
        except AttributeError as e:
            transformer_kwargs = self.transformer_kwargs
            if item in transformer_kwargs.keys():
                return transformer_kwargs[item]
            else:
                raise e

    def __dir__(self):
        transformer_kwargs = self.transformer_kwargs
        return set(super(TransformerAdaptorStep, self).__dir__()).union(set(transformer_kwargs.keys()))

class FeatureGenerationStep(TransformerAdaptorStep):

    def __init__(self, experiment, name, trans_primitives=None, continuous_cols=None, datetime_cols=None, categories_cols=None, latlong_cols=None, text_cols=None, max_depth=1, feature_selection_args=None):
        drop_cols = []
        if text_cols is not None:
            drop_cols += list(text_cols)
        if latlong_cols is not None:
            drop_cols += list(latlong_cols)
        super(FeatureGenerationStep, self).__init__(experiment, name, self._creator, trans_primitives=trans_primitives, fix_input=True, continuous_cols=continuous_cols, datetime_cols=datetime_cols, categories_cols=categories_cols, latlong_cols=latlong_cols, text_cols=text_cols, drop_cols=drop_cols if len(drop_cols) > 0 else None, max_depth=max_depth, feature_selection_args=feature_selection_args, task=None)

    def _creator(self, **kwargs):
        gen_cls = get_tool_box(self.experiment.X_train).transformers['FeatureGenerationTransformer']
        return gen_cls(**kwargs)

    def get_fitted_params(self):
        t = self.transformer_
        return {**super(FeatureGenerationStep, self).get_fitted_params(), 'trans_primitives': t.trans_primitives if t is not None else None, 'output_feature_names': t.transformed_feature_names_ if t is not None else None}

    def is_transform_skipped(self):
        t = self.transformer_
        return t is None or t.transformed_feature_names_ == self.input_features_

class MulticollinearityDetectStep(FeatureSelectStep):

    def __init__(self, experiment, name):
        super().__init__(experiment, name)
        self.feature_clusters_ = None

    @cache(arg_keys='X_train', strategy='transform', transformer='cache_transform', attrs_to_restore='input_features_,selected_features_,feature_clusters_')
    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        detector = get_tool_box(X_train).collinearity_detector()
        (feature_clusters_, remained, dropped) = detector.detect(X_train)
        self.step_progress('calc correlation')
        if dropped:
            self.selected_features_ = remained
            X_train = X_train[self.selected_features_]
            if X_eval is not None:
                X_eval = X_eval[self.selected_features_]
            if X_test is not None:
                X_test = X_test[self.selected_features_]
            self.step_progress('drop features')
        else:
            self.selected_features_ = None
        self.feature_clusters_ = feature_clusters_
        logger.info(f'{self.name} drop {len(dropped)} columns, {len(remained)} kept')
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'feature_clusters': self.feature_clusters_}

class DriftDetectStep(FeatureSelectStep):

    def __init__(self, experiment, name, remove_shift_variable, variable_shift_threshold, threshold, remove_size, min_features, num_folds):
        super().__init__(experiment, name)
        self.remove_shift_variable = remove_shift_variable
        self.variable_shift_threshold = variable_shift_threshold
        self.threshold = threshold
        self.remove_size = remove_size if 1.0 > remove_size > 0 else 0.1
        self.min_features = min_features if min_features > 1 else 10
        self.num_folds = num_folds if num_folds > 1 else 5
        self.history_ = None
        self.scores_ = None

    @cache(arg_keys='X_train,X_test', strategy='transform', transformer='cache_transform', attrs_to_restore='input_features_,selected_features_,history_,scores_')
    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        if X_test is not None:
            selector = get_tool_box(X_train, X_test).feature_selector_with_drift_detection(remove_shift_variable=self.remove_shift_variable, variable_shift_threshold=self.variable_shift_threshold, auc_threshold=self.threshold, min_features=self.min_features, remove_size=self.remove_size, cv=self.num_folds, random_state=self.experiment.random_state)
            (features, history, scores) = selector.select(X_train, X_test)
            dropped = set(X_train.columns.to_list()) - set(features)
            if dropped:
                self.selected_features_ = features
                X_train = X_train[features]
                X_test = X_test[features]
                if X_eval is not None:
                    X_eval = X_eval[features]
            else:
                self.selected_features_ = None
            self.history_ = history
            self.scores_ = scores
            logger.info(f'{self.name} drop {len(dropped)} columns, {len(features)} kept')
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'history': self.history_, 'scores': self.scores_}

class FeatureImportanceSelectionStep(FeatureSelectStep):

    def __init__(self, experiment, name, strategy, threshold, quantile, number):
        super(FeatureImportanceSelectionStep, self).__init__(experiment, name)
        tb = get_tool_box(pd.DataFrame)
        (strategy, threshold, quantile, number) = tb.detect_strategy_of_feature_selection_by_importance(strategy, threshold=threshold, quantile=quantile, number=number)
        self.strategy = strategy
        self.threshold = threshold
        self.quantile = quantile
        self.number = number
        self.importances_ = None

    @cache(arg_keys='X_train,y_train', strategy='transform', transformer='cache_transform', attrs_to_restore='input_features_,selected_features_,importances_')
    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        tb = get_tool_box(X_train, y_train)
        preprocessor = tb.general_preprocessor(X_train)
        estimator = tb.general_estimator(X_train, y_train, task=self.task)
        estimator.fit(preprocessor.fit_transform(X_train, y_train), y_train)
        importances = estimator.feature_importances_
        self.step_progress('training general estimator')
        (selected, unselected) = tb.select_feature_by_importance(importances, strategy=self.strategy, threshold=self.threshold, quantile=self.quantile, number=self.number)
        features = X_train.columns.to_list()
        selected_features = [features[i] for i in selected]
        unselected_features = [features[i] for i in unselected]
        self.step_progress('select by importances')
        if unselected_features:
            X_train = X_train[selected_features]
            if X_eval is not None:
                X_eval = X_eval[selected_features]
            if X_test is not None:
                X_test = X_test[selected_features]
        self.step_progress('drop features')
        logger.info(f'{self.name} drop {len(unselected_features)} columns, {len(selected_features)} kept')
        self.selected_features_ = selected_features if len(unselected_features) > 0 else None
        self.importances_ = importances
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'importances': self.importances_}

class PermutationImportanceSelectionStep(FeatureSelectStep):

    def __init__(self, experiment, name, scorer, estimator_size, strategy, threshold, quantile, number):
        assert scorer is not None
        super().__init__(experiment, name)
        (strategy, threshold, quantile, number) = get_tool_box(pd.DataFrame).detect_strategy_of_feature_selection_by_importance(strategy, threshold=threshold, quantile=quantile, number=number)
        self.scorer = scorer
        self.estimator_size = estimator_size
        self.strategy = strategy
        self.threshold = threshold
        self.quantile = quantile
        self.number = number
        self.importances_ = None

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        best_trials = hyper_model.get_top_trials(self.estimator_size)
        estimators = [hyper_model.load_estimator(trial.model_file) for trial in best_trials]
        self.step_progress('load estimators')
        (X, y) = (X_train, y_train) if X_eval is None or y_eval is None else (X_eval, y_eval)
        tb = get_tool_box(X, y)
        importances = tb.permutation_importance_batch(estimators, X, y, self.scorer, n_repeats=5, random_state=self.experiment.random_state)
        (selected, unselected) = tb.select_feature_by_importance(importances.importances_mean, strategy=self.strategy, threshold=self.threshold, quantile=self.quantile, number=self.number)
        if len(selected) > 0:
            selected_features = [importances.columns[i] for i in selected]
            unselected_features = [importances.columns[i] for i in unselected]
        else:
            msg = f'{self.name}: All features will be dropped with importance:{importances.importances_mean}, so drop nothing. Change settings and try again pls.'
            logger.warning(msg)
            selected_features = importances.columns
            unselected_features = []
        self.step_progress('calc importance')
        if unselected_features:
            X_train = X_train[selected_features]
            if X_eval is not None:
                X_eval = X_eval[selected_features]
            if X_test is not None:
                X_test = X_test[selected_features]
        self.step_progress('drop features')
        logger.info(f'{self.name} drop {len(unselected_features)} columns, {len(selected_features)} kept')
        self.selected_features_ = selected_features if len(unselected_features) > 0 else None
        self.importances_ = importances
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'importances': self.importances_}

class SpaceSearchStep(ExperimentStep):

    def __init__(self, experiment, name, cv=False, num_folds=3):
        super().__init__(experiment, name)
        self.cv = cv
        self.num_folds = num_folds
        self.dataset_id = None
        self.model = None
        self.history_ = None
        self.best_reward_ = None

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        dataset_id = _generate_dataset_id(X_train, y_train, X_test, X_eval, y_eval)
        fitted_step = self.experiment.find_step(lambda s: isinstance(s, SpaceSearchStep) and s.dataset_id == dataset_id, until_step_name=self.name)
        if fitted_step is None:
            model = self.search(X_train.copy(), y_train.copy(), X_test=X_test.copy() if X_test is not None else None, X_eval=X_eval.copy() if X_eval is not None else None, y_eval=y_eval.copy() if y_eval is not None else None, dataset_id=dataset_id, **kwargs)
            if model.get_best_trial() is None or model.get_best_trial().reward == 0:
                raise RuntimeError('Not found available trial, change experiment settings and try again pls.')
            self.dataset_id = dataset_id
            self.model = model
            self.history_ = model.history
            self.best_reward_ = model.get_best_trial().reward
        else:
            logger.info(f'reuse fitted step: {fitted_step.name}')
            self.status_ = self.STATUS_SKIPPED
            self.from_fitted_step(fitted_step)
        logger.info(f'{self.name} best_reward: {self.best_reward_}')
        return (self.model, X_train, y_train, X_test, X_eval, y_eval)

    def search(self, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        if X_eval is not None:
            kwargs['eval_set'] = (X_eval, y_eval)
        model = copy.deepcopy(self.experiment.hyper_model)
        es = self.find_early_stopping_callback(model.callbacks)
        if es is not None and es.time_limit is not None and (es.time_limit > 0):
            es.time_limit = self.estimate_time_limit(es.time_limit)
        model.search(X_train, y_train, X_eval, y_eval, cv=self.cv, num_folds=self.num_folds, **kwargs)
        return model

    def from_fitted_step(self, fitted_step):
        self.dataset_id = fitted_step.dataset_id
        self.model = fitted_step.model
        self.history_ = fitted_step.history_
        self.best_reward_ = fitted_step.best_reward_

    @staticmethod
    def find_early_stopping_callback(cbs):
        from hypernets.core.callbacks import EarlyStoppingCallback
        assert isinstance(cbs, (tuple, list))
        for cb in cbs:
            if isinstance(cb, EarlyStoppingCallback):
                return cb
        return None

    def estimate_time_limit(self, total_time_limit):
        all_steps = self.experiment.steps
        my_index = -1
        search_total = 0
        search_ran = 0
        search_elapsed_seconds = 0
        nosearch_total = 0
        nosearch_ran = 0
        nosearch_elapsed_seconds = 0
        for step in all_steps:
            if isinstance(step, SpaceSearchStep):
                if step.name == self.name:
                    my_index = search_total
                search_total += 1
                if my_index < 0:
                    search_ran += 1
                    search_elapsed_seconds += step.elapsed_seconds
            else:
                nosearch_total += 1
                if my_index < 0:
                    nosearch_ran += 1
                    nosearch_elapsed_seconds += step.elapsed_seconds
        if nosearch_ran < nosearch_total - 1:
            nosearch_total_seconds = (nosearch_ran + 1) / nosearch_total * nosearch_elapsed_seconds
        else:
            nosearch_total_seconds = nosearch_elapsed_seconds
        search_total_seconds = total_time_limit - nosearch_total_seconds
        time_limit = search_total_seconds - search_elapsed_seconds
        if my_index < search_total - 1:
            time_limit /= search_total - my_index
        if time_limit < total_time_limit * 0.2:
            time_limit = total_time_limit * 0.2
        return time_limit

    def transform(self, X, y=None, **kwargs):
        return X

    def is_transform_skipped(self):
        return True

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'best_reward': self.best_reward_, 'history': self.history_}

class SpaceSearchWithDownSampleStep(SpaceSearchStep):

    def __init__(self, experiment, name, cv=False, num_folds=3, size=None, max_trials=None, time_limit=None):
        assert size is None or isinstance(size, (int, float, dict))
        assert time_limit is None or isinstance(time_limit, (int, float))
        assert max_trials is None or isinstance(max_trials, int)
        super().__init__(experiment, name, cv=cv, num_folds=num_folds)
        self.size = size
        self.max_trials = max_trials
        self.time_limit = time_limit
        self.down_sample_model = None

    def search(self, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        key_max_trials = 'max_trials'
        model0 = copy.deepcopy(self.experiment.hyper_model)
        kwargs0 = kwargs.copy()
        (X_train_sampled, y_train_sampled, X_eval_sampled, y_eval_sampled) = self.down_sample(X_train, y_train, X_eval, y_eval)
        if X_eval_sampled is not None:
            kwargs0['eval_set'] = (X_eval_sampled, y_eval_sampled)
        if self.max_trials is not None:
            kwargs0[key_max_trials] = self.max_trials
        elif key_max_trials in kwargs.keys():
            kwargs0[key_max_trials] *= 3
        es0 = self.find_early_stopping_callback(model0.callbacks)
        time_limit = 0
        if es0 is not None:
            if es0.time_limit is not None and es0.time_limit > 0:
                time_limit = self.estimate_time_limit(es0.time_limit)
                if self.time_limit is not None:
                    es0.time_limit = min(self.time_limit, time_limit / 2)
                else:
                    es0.time_limit = math.ceil(time_limit / 3)
            if isinstance(es0.max_no_improvement_trials, int) and isinstance(kwargs.get(key_max_trials), int) and (kwargs[key_max_trials] > 0):
                es0.max_no_improvement_trials *= kwargs0[key_max_trials] / kwargs[key_max_trials]
                es0.max_no_improvement_trials = math.ceil(es0.max_no_improvement_trials)
        if logger.is_info_enabled():
            logger.info(f'search with down sampled data, max_trails={kwargs0.get(key_max_trials)}, {es0}')
        model0.search(X_train_sampled, y_train_sampled, X_eval_sampled, y_eval_sampled, cv=self.cv, num_folds=self.num_folds, **kwargs0)
        if model0.get_best_trial() is None or model0.get_best_trial().reward == 0:
            raise RuntimeError('Not found available trial, change experiment settings and try again pls.')
        self.down_sample_model = model0
        playback = self.create_playback_searcher(model0.history)
        if X_eval is not None:
            kwargs['eval_set'] = (X_eval, y_eval)
        model = copy.deepcopy(self.experiment.hyper_model)
        es = self.find_early_stopping_callback(model.callbacks)
        if es is not None and es.time_limit is not None and (es.time_limit > 0):
            elapsed = self.elapsed_seconds
            if time_limit - elapsed > 0:
                es.time_limit = math.ceil(time_limit - elapsed)
            else:
                es.time_limit = math.ceil(time_limit * 0.3)
            es.max_no_improvement_trials = 0
        model.searcher = playback
        model.discriminator = None
        if isinstance(kwargs.get(key_max_trials), int) and kwargs[key_max_trials] > len(playback.samples):
            kwargs[key_max_trials] = len(playback.samples)
        if logger.is_info_enabled():
            logger.info(f'playback with full data, max_trails={kwargs.get(key_max_trials)}, {es}')
        model.search(X_train, y_train, X_eval, y_eval, cv=self.cv, num_folds=self.num_folds, **kwargs)
        return model

    def down_sample(self, X_train, y_train, X_eval, y_eval):
        size = self.size if self.size else 0.1
        task = self.task
        random_state = self.experiment.random_state
        options = {}
        if isinstance(size, dict):
            assert task in {const.TASK_BINARY, const.TASK_MULTICLASS}
            (X_train_sampled, y_train_sampled) = _sample_by_classes(X_train, y_train, size, random_state)
            (X_eval_sampled, y_eval_sampled) = _sample_by_classes(X_eval, y_eval, size, random_state)
        else:
            if task in {const.TASK_BINARY, const.TASK_MULTICLASS} and isinstance(X_train, pd.DataFrame):
                options['stratify'] = y_train
            tb = get_tool_box(X_train, y_train)
            (X_train_sampled, _, y_train_sampled, _) = tb.train_test_split(X_train, y_train, train_size=size, random_state=random_state, **options)
            if X_eval is not None:
                if task in {const.TASK_BINARY, const.TASK_MULTICLASS} and isinstance(X_eval, pd.DataFrame):
                    options['stratify'] = y_eval
                (X_eval_sampled, _, y_eval_sampled, _) = tb.train_test_split(X_eval, y_eval, train_size=size, random_state=random_state, **options)
            else:
                (X_eval_sampled, y_eval_sampled) = (None, None)
        return (X_train_sampled, y_train_sampled, X_eval_sampled, y_eval_sampled)

    @staticmethod
    def create_playback_searcher(history):
        from hypernets.searchers import PlaybackSearcher
        playback = PlaybackSearcher(history, reverse=False)
        return playback

    def from_fitted_step(self, fitted_step):
        super().from_fitted_step(fitted_step)
        self.down_sample_model = fitted_step.down_sample_model

class EstimatorBuilderStep(ExperimentStep):

    def __init__(self, experiment, name):
        super().__init__(experiment, name)
        self.dataset_id = None
        self.estimator_ = None

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        dataset_id = _generate_dataset_id(X_train, y_train, X_test, X_eval, y_eval)
        fitted_step = self.experiment.find_step(lambda s: isinstance(s, EstimatorBuilderStep) and s.dataset_id == dataset_id, until_step_name=self.name)
        if fitted_step is None:
            estimator = self.build_estimator(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval, **kwargs)
            logger.info(f'built estimator: {estimator}')
        else:
            logger.info(f'reuse fitted step: {fitted_step.name}')
            self.status_ = self.STATUS_SKIPPED
            estimator = fitted_step.estimator_
        self.dataset_id = dataset_id
        self.estimator_ = estimator
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    def build_estimator(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        raise NotImplementedError()

    def transform(self, X, y=None, **kwargs):
        return X

    def is_transform_skipped(self):
        return True

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'estimator': self.estimator_}

class EnsembleStep(EstimatorBuilderStep):

    def __init__(self, experiment, name, scorer=None, ensemble_size=7):
        assert ensemble_size > 1
        super().__init__(experiment, name)
        self.scorer = scorer if scorer is not None else get_scorer('neg_log_loss')
        self.ensemble_size = ensemble_size

    def select_trials(self, hyper_model):
        """
        select trails to ensemble from hyper_model (and it's history)
        """
        best_trials = hyper_model.get_top_trials(self.ensemble_size)
        return best_trials

    def build_estimator(self, hyper_model, X_train, y_train, X_eval=None, y_eval=None, **kwargs):
        trials = self.select_trials(hyper_model)
        estimators = [hyper_model.load_estimator(trial.model_file) for trial in trials]
        ensemble = self.get_ensemble(estimators, X_train, y_train)
        if all(['oof' in trial.memo.keys() for trial in trials]):
            logger.info('ensemble with oofs')
            oofs = self.get_ensemble_predictions(trials, ensemble)
            assert oofs is not None
            if hasattr(oofs, 'shape'):
                tb = get_tool_box(y_train, oofs)
                (y_, oofs_) = tb.select_valid_oof(y_train, oofs)
                ensemble.fit(None, y_, oofs_)
            else:
                ensemble.fit(None, y_train, oofs)
        elif X_eval is not None and y_eval is not None:
            ensemble.fit(X_eval, y_eval)
        else:
            ensemble.fit(X_train, y_train)
        return ensemble

    def get_ensemble(self, estimators, X_train, y_train):
        tb = get_tool_box(X_train, y_train)
        return tb.greedy_ensemble(self.task, estimators, scoring=self.scorer, ensemble_size=self.ensemble_size)

    def get_ensemble_predictions(self, trials, ensemble):
        np_ = ensemble.np
        oofs = None
        for (i, trial) in enumerate(trials):
            if 'oof' in trial.memo.keys():
                oof = trial.memo['oof']
                if oofs is None:
                    if len(oof.shape) == 1:
                        oofs = np_.zeros((oof.shape[0], len(trials)), dtype=np_.float64)
                    else:
                        oofs = np_.zeros((oof.shape[0], len(trials), oof.shape[-1]), dtype=np_.float64)
                oofs[:, i] = oof
        return oofs

class DaskEnsembleStep(EnsembleStep):

    def get_ensemble_predictions(self, trials, ensemble):
        if type(ensemble).__name__.lower().find('dask') >= 0:
            oofs = [trial.memo.get('oof') for trial in trials]
            return oofs if any([oof is not None for oof in oofs]) else None
        return super().get_ensemble_predictions(trials, ensemble)

class FinalTrainStep(EstimatorBuilderStep):

    def __init__(self, experiment, name, retrain_on_wholedata=False):
        super().__init__(experiment, name)
        self.retrain_on_wholedata = retrain_on_wholedata

    def build_estimator(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        if self.retrain_on_wholedata:
            trial = hyper_model.get_best_trial()
            tb = get_tool_box(X_train, X_eval)
            X_all = tb.concat_df([X_train, X_eval], axis=0)
            y_all = tb.concat_df([y_train, y_eval], axis=0)
            estimator = hyper_model.final_train(trial.space_sample, X_all, y_all, **kwargs)
        else:
            estimator = hyper_model.load_estimator(hyper_model.get_best_trial().model_file)
        return estimator

class PseudoLabelStep(ExperimentStep):

    def __init__(self, experiment, name, estimator_builder_name, strategy=None, proba_threshold=None, proba_quantile=None, sample_number=None, resplit=False):
        super().__init__(experiment, name)
        pl = get_tool_box(pd.DataFrame).pseudo_labeling(strategy=strategy)
        (strategy, proba_threshold, proba_quantile, sample_number) = pl.detect_strategy(strategy, threshold=proba_threshold, quantile=proba_quantile, number=sample_number)
        self.estimator_builder_name = estimator_builder_name
        self.strategy = strategy
        self.proba_threshold = proba_threshold
        self.proba_quantile = proba_quantile
        self.sample_number = sample_number
        self.resplit = resplit
        self.plot_sample_size = 3000
        self.test_proba_ = None
        self.pseudo_label_stat_ = None

    def transform(self, X, y=None, **kwargs):
        return X

    def is_transform_skipped(self):
        return True

    def fit_transform(self, hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, **kwargs):
        assert self.task in [const.TASK_BINARY, const.TASK_MULTICLASS] and X_test is not None
        super().fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval)
        estimator_builder_step = self.experiment.get_step(self.estimator_builder_name)
        assert estimator_builder_step is not None and estimator_builder_step.estimator_ is not None
        estimator = estimator_builder_step.estimator_
        pl = get_tool_box(X_test).pseudo_labeling(strategy=self.strategy, threshold=self.proba_threshold, quantile=self.proba_quantile, number=self.sample_number)
        proba = estimator.predict_proba(X_test)
        classes = estimator.classes_
        (X_pseudo, y_pseudo) = pl.select(X_test, classes, proba)
        pseudo_label_stat = self.stat_pseudo_label(y_pseudo, classes)
        test_proba = get_tool_box(proba).to_local(proba)[0]
        if len(test_proba) > self.plot_sample_size:
            (test_proba, _) = get_tool_box(test_proba).train_test_split(test_proba, train_size=self.plot_sample_size, random_state=self.experiment.random_state)
        if X_pseudo is not None:
            (X_train, y_train, X_eval, y_eval) = self.merge_pseudo_label(X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo)
        self.test_proba_ = test_proba
        self.pseudo_label_stat_ = pseudo_label_stat
        return (hyper_model, X_train, y_train, X_test, X_eval, y_eval)

    @staticmethod
    def stat_pseudo_label(y_pseudo, classes):
        stat = OrderedDict()
        value_counts = get_tool_box(y_pseudo).value_counts(y_pseudo)
        for c in classes:
            stat[c] = value_counts.get(c, 0)
        return stat

    def merge_pseudo_label(self, X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo, **kwargs):
        tb = get_tool_box(X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo)
        if self.resplit:
            x_list = [X_train, X_pseudo]
            y_list = [y_train, pd.Series(y_pseudo)]
            if X_eval is not None and y_eval is not None:
                x_list.append(X_eval)
                y_list.append(y_eval)
            X_mix = tb.concat_df(x_list, axis=0, ignore_index=True)
            y_mix = tb.concat_df(y_list, axis=0, ignore_index=True)
            if y_mix.dtype != y_train.dtype:
                y_mix = y_mix.astype(y_train.dtype)
            if self.task == const.TASK_REGRESSION:
                stratify = None
            else:
                stratify = y_mix
            eval_size = self.experiment.eval_size
            (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_mix, y_mix, test_size=eval_size, random_state=self.experiment.random_state, stratify=stratify)
        else:
            X_train = tb.concat_df([X_train, X_pseudo], axis=0)
            y_train = tb.concat_df([y_train, y_pseudo], axis=0)
        return (X_train, y_train, X_eval, y_eval)

    def get_fitted_params(self):
        return {**super().get_fitted_params(), 'test_proba': self.test_proba_, 'pseudo_label_stat': self.pseudo_label_stat_}

class DaskPseudoLabelStep(PseudoLabelStep):

    def merge_pseudo_label(self, X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo, **kwargs):
        tb = get_tool_box(X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo)
        if not (hasattr(tb, 'exist_dask_object') and tb.exist_dask_object(X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo)):
            return super().merge_pseudo_label(X_train, y_train, X_eval, y_eval, X_pseudo, y_pseudo, **kwargs)
        if self.resplit:
            x_list = [X_train, X_pseudo]
            y_list = [y_train, y_pseudo]
            if X_eval is not None and y_eval is not None:
                x_list.append(X_eval)
                y_list.append(y_eval)
            X_mix = tb.concat_df(x_list, axis=0)
            y_mix = tb.concat_df(y_list, axis=0)
            X_mix = tb.concat_df([X_mix, y_mix], axis=1).reset_index(drop=True)
            y_mix = X_mix.pop(y_mix.name)
            eval_size = self.experiment.eval_size
            (X_train, X_eval, y_train, y_eval) = tb.train_test_split(X_mix, y_mix, test_size=eval_size, random_state=self.experiment.random_state)
        else:
            X_train = tb.concat_df([X_train, X_pseudo], axis=0)
            y_train = tb.concat_df([y_train, y_pseudo], axis=0)
            X_train = tb.concat_df([X_train, y_train], axis=1)
            y_train = X_train.pop(y_train.name)
        return (X_train, y_train, X_eval, y_eval)

class SteppedExperiment(Experiment):

    def __init__(self, steps, *args, **kwargs):
        assert isinstance(steps, (tuple, list)) and all([isinstance(step, ExperimentStep) for step in steps])
        super(SteppedExperiment, self).__init__(*args, **kwargs)
        if logger.is_info_enabled():
            names = [step.name for step in steps]
            logger.info(f'create experiment with {names}, random_state={self.random_state}')
        self.steps = steps
        self.hyper_model_ = None

    def train(self, hyper_model, X_train, y_train, X_test, X_eval=None, y_eval=None, **kwargs):
        from_step = self.get_step_index(kwargs.pop('from_step', None), 0)
        to_step = self.get_step_index(kwargs.pop('to_step', None), len(self.steps) - 1)
        assert from_step <= to_step
        for (i, step) in enumerate(self.steps):
            if i > to_step:
                break
            assert step.status_ != ExperimentStep.STATUS_RUNNING
            tb = get_tool_box(X_train, y_train, X_test, X_eval, y_eval)
            tb.gc()
            if logger.is_info_enabled():
                u = tb.memory_usage(X_train, y_train, X_test, X_eval, y_eval)
                f = tb.memory_free()
                logger.info(f'{tb.__name__} data memory usage: {u / GB:.3f}, free={f / GB:.3f}')
            if X_test is not None and X_train.columns.to_list() != X_test.columns.to_list():
                logger.warning(f'X_train{X_train.columns.to_list()} and X_test{X_test.columns.to_list()} have different columns before {step.name}, try fix it.')
                X_test = X_test[X_train.columns]
            if X_eval is not None and X_train.columns.to_list() != X_eval.columns.to_list():
                logger.warning(f'X_train{X_train.columns.to_list()} and X_eval{X_eval.columns.to_list()} have different columns before {step.name}, try fix it.')
                X_eval = X_eval[X_train.columns]
            (X_train, y_train, X_test, X_eval, y_eval) = [v.persist() if hasattr(v, 'persist') else v for v in (X_train, y_train, X_test, X_eval, y_eval)]
            if i >= from_step or step.status_ == ExperimentStep.STATUS_NONE:
                logger.info(f'fit_transform {step.name} with columns: {X_train.columns.to_list()}')
                step.status_ = ExperimentStep.STATUS_RUNNING
                self.step_start(step.name)
                try:
                    step.start_time = time.time()
                    (hyper_model, X_train, y_train, X_test, X_eval, y_eval) = step.fit_transform(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval, **kwargs)
                    if step.status_ == ExperimentStep.STATUS_RUNNING:
                        step.status_ = ExperimentStep.STATUS_SUCCESS
                    self.step_end(output=step.get_fitted_params())
                except Exception as e:
                    if step.status_ == ExperimentStep.STATUS_RUNNING:
                        step.status_ = ExperimentStep.STATUS_FAILED
                    self.step_break(error=e)
                    raise e
                finally:
                    step.done_time = time.time()
            elif not step.is_transform_skipped():
                logger.info(f'transform {step.name} with columns: {X_train.columns.to_list()}')
                X_train = step.transform(X_train, y_train)
                if X_test is not None:
                    X_test = step.transform(X_test)
                if X_eval is not None:
                    X_eval = step.transform(X_eval, y_eval)
        estimator = self.to_estimator(X_train, y_train, X_test, X_eval, y_eval, self.steps) if to_step == len(self.steps) - 1 else None
        self.hyper_model_ = hyper_model
        return estimator

    def get_step(self, name):
        for step in self.steps:
            if step.name == name:
                return step
        raise ValueError(f'Not found step "{name}"')

    def find_step(self, fn, until_step_name=None, index=False):
        for (i, step) in enumerate(self.steps):
            if step.name == until_step_name:
                break
            if fn(step):
                return i if index else step
        return None

    def get_step_index(self, name_or_index, default):
        assert name_or_index is None or isinstance(name_or_index, (int, str))
        if isinstance(name_or_index, str):
            step_names = [s.name for s in self.steps]
            assert name_or_index in step_names
            return step_names.index(name_or_index)
        elif isinstance(name_or_index, int):
            assert 0 <= name_or_index < len(self.steps)
            return name_or_index
        else:
            return default

    @staticmethod
    def to_estimator(X_train, y_train, X_test, X_eval, y_eval, steps):
        last_step = steps[-1]
        assert getattr(last_step, 'estimator_', None) is not None
        pipeline_steps = [(step.name, step) for step in steps if not step.is_transform_skipped()]
        if len(pipeline_steps) > 0:
            tb = get_tool_box(X_train, y_train, X_test, X_eval, y_eval)
            pipeline_steps += [('estimator', last_step.estimator_)]
            estimator = tb.transformers['Pipeline'](pipeline_steps)
            if logger.is_info_enabled():
                names = [step[0] for step in pipeline_steps]
                logger.info(f'trained experiment pipeline: {names}')
        else:
            estimator = last_step.estimator_
            if logger.is_info_enabled():
                logger.info(f'trained experiment estimator:\n{estimator}')
        return estimator

class CompeteExperiment(SteppedExperiment):
    """
    A powerful experiment strategy for AutoML with a set of advanced features.

    There are still many challenges in the machine learning modeling process for tabular data, such as imbalanced data,
    data drift, poor generalization ability, etc.  This challenges cannot be completely solved by pipeline search,
    so we introduced in HyperNets a more powerful tool is `CompeteExperiment`. `CompeteExperiment` is composed of a series
    of steps and *Pipeline Search* is just one step. It also includes advanced steps such as data cleaning,
    data drift handling, two-stage search, ensemble etc.
    """

    def __init__(self, hyper_model, X_train, y_train, X_eval=None, y_eval=None, X_test=None, eval_size=DEFAULT_EVAL_SIZE, train_test_split_strategy=None, cv=None, num_folds=3, task=None, id=None, callbacks=None, random_state=None, scorer=None, data_adaption=None, data_adaption_target=None, data_adaption_memory_limit=0.05, data_adaption_min_cols=0.3, data_cleaner_args=None, feature_generation=False, feature_generation_trans_primitives=None, feature_generation_max_depth=1, feature_generation_categories_cols=None, feature_generation_continuous_cols=None, feature_generation_datetime_cols=None, feature_generation_latlong_cols=None, feature_generation_text_cols=None, collinearity_detection=False, drift_detection=True, drift_detection_remove_shift_variable=True, drift_detection_variable_shift_threshold=0.7, drift_detection_threshold=0.7, drift_detection_remove_size=0.1, drift_detection_min_features=10, drift_detection_num_folds=5, feature_selection=False, feature_selection_strategy=None, feature_selection_threshold=None, feature_selection_quantile=None, feature_selection_number=None, down_sample_search=None, down_sample_search_size=None, down_sample_search_time_limit=None, down_sample_search_max_trials=None, ensemble_size=20, feature_reselection=False, feature_reselection_estimator_size=10, feature_reselection_strategy=None, feature_reselection_threshold=1e-05, feature_reselection_quantile=None, feature_reselection_number=None, pseudo_labeling=False, pseudo_labeling_strategy=None, pseudo_labeling_proba_threshold=None, pseudo_labeling_proba_quantile=None, pseudo_labeling_sample_number=None, pseudo_labeling_resplit=False, retrain_on_wholedata=False, log_level=None, **kwargs):
        """
        Parameters
        ----------
        hyper_model : hypernets.model.HyperModel
            A `HyperModel` instance
        X_train : Pandas or Dask DataFrame
            Feature data for training
        y_train : Pandas or Dask Series
            Target values for training
        X_eval : (Pandas or Dask DataFrame) or None
            (default=None), Feature data for evaluation
        y_eval : (Pandas or Dask Series) or None, (default=None)
            Target values for evaluation
        X_test : (Pandas or Dask Series) or None, (default=None)
            Unseen data without target values for semi-supervised learning
        eval_size : float or int, (default=None)
            Only valid when ``X_eval`` or ``y_eval`` is None. If float, should be between 0.0 and 1.0 and represent
            the proportion of the dataset to include in the eval split. If int, represents the absolute number of
            test samples. If None, the value is set to the complement of the train size.
        train_test_split_strategy : *'adversarial_validation'* or None, (default=None)
            Only valid when ``X_eval`` or ``y_eval`` is None. If None, use eval_size to split the dataset,
            otherwise use adversarial validation approach.
        cv : bool, (default=True if X_eval is None, False if X_eval is not None)
            If True, use cross-validation instead of evaluation set reward to guide the search process
        num_folds : int, (default=3)
            Number of cross-validated folds, only valid when cv is true
        task : str or None, (default=None)
            Task type(*binary*, *multiclass* or *regression*).
            If None, inference the type of task automatically
        callbacks : list of callback functions or None, (default=None)
            List of callback functions that are applied at each experiment step. See `hypernets.experiment.ExperimentCallback`
            for more information.
        random_state : int or RandomState instance, (default=None)
            Controls the shuffling applied to the data before applying the split
        scorer : str, callable or None, (default=None)
            Scorer to used for feature importance evaluation and ensemble. It can be a single string
            (see [get_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.get_scorer.html))
            or a callable (see [make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html)).
            Will be inferred from *hyper_model.reward_metric* if it's None.
        data_adaption: bool, (default True for Pandas/Cuml data types)
            Whether to enable data adaption. Support Pandas/Cuml data types only.
        data_adaption_target: None or str or dataframe type, (default None)
            Whether to run the next steps. 'cuml' or 'cuda', adapt training data into cuml datatypes and run next steps on nvidia GPU Devices.
            None, not change the training data types.
        data_adaption_memory_limit: int or float, (default 0.05)
            If float, should be between 0.0 and 1.0 and represent the proportion of the system free memory.
            If int, represents the absolute byte number of memory.
        data_adaption_min_cols: int or float, (default 0.3)
            If float, should be between 0.0 and 1.0 and represent the proportion of the original dataframe column number.
            If int, represents the absolute column number.
        data_cleaner_args : dict, (default None)
            Dictionary of parameters to initialize the `DataCleaner` instance. If None, `DataCleaner` will be initialized
            with default values.
        feature_generation : bool (default False),
            Whether to enable feature generation.
        feature_generation_trans_primitives: list (default None)
            FeatureTools transform primitives list.
        feature_generation_categories_cols: list (default None),
            Column names to generate new features as FeatureTools Categorical variables.
        feature_generation_continuous_cols: list (default detected from X_train),
            Column names to generate new features as FeatureTools Numeric variables.
        feature_generation_datetime_cols: list (default detected from X_train),
            Column names to generate new features as FeatureTools Datetime variables.
        feature_generation_latlong_cols: list (default None),
            Column names to generate new features as FeatureTools LatLong variables.
        feature_generation_text_cols: list (default None),
            Column names to generate new features as FeatureTools Text(NaturalLanguage) variables.
        collinearity_detection :  bool, (default=False)
            Whether to clear multicollinearity features
        drift_detection : bool,(default=True)
            Whether to enable data drift detection and processing. Only valid when *X_test* is provided. Concept drift
            in the input data is one of the main challenges. Over time, it will worsen the performance of model on new
            data. We introduce an adversarial validation approach to concept drift problems. This approach will detect
            concept drift and identify the drifted features and process them automatically.
        drift_detection_remove_shift_variable : bool, (default=True)
        drift_detection_variable_shift_threshold : float, (default=0.7)
        drift_detection_threshold : float, (default=0.7)
        drift_detection_remove_size : float, (default=0.1)
        drift_detection_min_features : int, (default=10)
        drift_detection_num_folds : int, (default=5)
        feature_selection: bool, (default=False)
            Whether to select features by *feature_importances_*.
        feature_selection_strategy : str, (default='threshold')
            Strategy to select features(*threshold*, *number* or *quantile*).
        feature_selection_threshold : float, (default=0.1)
            Confidence threshold of feature_importance. Only valid when *feature_selection_strategy* is 'threshold'.
        feature_selection_quantile:
            Confidence quantile of feature_importance. Only valid when *feature_selection_strategy* is 'quantile'.
        feature_selection_number:
            Expected feature number to keep. Only valid when *feature_selection_strategy* is 'number'.
        feature_reselection : bool, (default=True)
            Whether to enable two stage feature selection with permutation importance.
        feature_reselection_estimator_size : int, (default=10)
            The number of estimator to evaluate feature importance. Only valid when *feature_reselection* is True.
        feature_reselection_strategy : str, (default='threshold')
            Strategy to reselect features(*threshold*, *number* or *quantile*).
        feature_reselection_threshold : float, (default=1e-5)
            Confidence threshold of the mean permutation importance. Only valid when *feature_reselection_strategy* is 'threshold'.
        feature_reselection_quantile:
            Confidence quantile of feature_importance. Only valid when *feature_reselection_strategy* is 'quantile'.
        feature_reselection_number:
            Expected feature number to keep. Only valid when *feature_reselection_strategy* is 'number'.
        down_sample_search : bool, (default None),
            Whether to enable down sample search.
        down_sample_search_size : float, (default 0.1)
            The sample size to extract from train_data.
        down_sample_search_time_limit : int, (default None)
            The maximum seconds to run with down sampled data.
        down_sample_search_max_trials : int, (default 3*experiment's *max_trials* argument)
            The maximum trial number to run with down sampled data.
        ensemble_size : int, (default=20)
            The number of estimator to ensemble. During the AutoML process, a lot of models will be generated with different
            preprocessing pipelines, different models, and different hyperparameters. Usually selecting some of the models
            that perform well to ensemble can obtain better generalization ability than just selecting the single best model.
        pseudo_labeling : bool, (default=False)
            Whether to enable pseudo labeling. Pseudo labeling is a semi-supervised learning technique, instead of manually
            labeling the unlabelled data, we give approximate labels on the basis of the labelled data. Pseudo-labeling can
            sometimes improve the generalization capabilities of the model.
        pseudo_labeling_strategy : str, (default='threshold')
            Strategy to sample pseudo labeling data(*threshold*, *number* or *quantile*).
        pseudo_labeling_proba_threshold : float, (default=0.8)
            Confidence threshold of pseudo-label samples. Only valid when *pseudo_labeling_strategy* is 'threshold'.
        pseudo_labeling_proba_quantile:
            Confidence quantile of pseudo-label samples. Only valid when *pseudo_labeling_strategy* is 'quantile'.
        pseudo_labeling_sample_number:
            Expected number to sample per class. Only valid when *pseudo_labeling_strategy* is 'number'.
        pseudo_labeling_resplit : bool, (default=False)
            Whether to re-split the training set and evaluation set after adding pseudo-labeled data. If False, the
            pseudo-labeled data is only appended to the training set. Only valid when *pseudo_labeling* is True.
        retrain_on_wholedata : bool, (default=False)
            Whether to retrain the model with whole data after the search is completed.
        log_level : int, str, or None (default=None),
            Level of logging, possible values:
                -logging.CRITICAL
                -logging.FATAL
                -logging.ERROR
                -logging.WARNING
                -logging.WARN
                -logging.INFO
                -logging.DEBUG
                -logging.NOTSET
        kwargs :

        """
        if random_state is None:
            random_state = np.random.randint(0, 65535)
        set_random_state(random_state)
        if cv is None:
            cv = X_eval is None
        tb = get_tool_box(X_train, y_train)
        if task is None:
            dc_nan_chars = data_cleaner_args.get('nan_chars') if data_cleaner_args is not None else None
            if isinstance(dc_nan_chars, str):
                dc_nan_chars = [dc_nan_chars]
            (task, _) = tb.infer_task_type(y_train, excludes=dc_nan_chars if dc_nan_chars is not None else None)
        if scorer is None:
            scorer = tb.metrics.metric_to_scoring(hyper_model.reward_metric, task=task, pos_label=kwargs.get('pos_label'))
        if collinearity_detection:
            try:
                tb.collinearity_detector()
            except NotImplementedError:
                raise NotImplementedError('collinearity_detection is not supported for your data')
        if feature_generation:
            if 'FeatureGenerationTransformer' not in tb.transformers.keys():
                raise NotImplementedError('feature_generation is not supported for your data')
            if data_cleaner_args is None:
                data_cleaner_args = {}
            cs = tb.column_selector
            reserve_columns = data_cleaner_args.get('reserve_columns')
            reserve_columns = list(reserve_columns) if reserve_columns is not None else []
            if feature_generation_datetime_cols is None:
                feature_generation_datetime_cols = tb.column_selector.column_all_datetime(X_train)
                logger.info(f'detected datetime columns: {feature_generation_datetime_cols}')
            if feature_generation_latlong_cols is None:
                feature_generation_latlong_cols = cs.column_latlong(X_train)
                logger.info(f'detected latlong columns: {feature_generation_latlong_cols}')
            if feature_generation_text_cols is None:
                feature_generation_text_cols = cs.column_text(X_train)
                logger.info(f'detected text columns: {feature_generation_text_cols}')
            for cols in (feature_generation_categories_cols, feature_generation_continuous_cols, feature_generation_datetime_cols, feature_generation_latlong_cols, feature_generation_text_cols):
                if cols is not None and len(cols) > 0:
                    reserve_columns += list(cols)
            data_cleaner_args['reserve_columns'] = reserve_columns
        steps = []
        two_stage = False
        creators = self.get_creators(hyper_model, X_train, y_train, X_test=X_test, X_eval=X_eval, y_eval=y_eval, down_sample_search=down_sample_search)
        if data_adaption is None:
            data_adaption = tb.__name__.lower().find('dask') < 0
        if data_adaption:
            if tb.__name__.lower().find('dask') >= 0:
                raise ValueError('Data adaption dose not support dask data types now.')
            creator = creators[StepNames.DATA_ADAPTION]
            steps.append(creator(self, StepNames.DATA_ADAPTION, target=data_adaption_target, memory_limit=data_adaption_memory_limit, min_cols=data_adaption_min_cols))
        creator = creators[StepNames.DATA_CLEAN]
        steps.append(creator(self, StepNames.DATA_CLEAN, data_cleaner_args=data_cleaner_args, cv=cv, train_test_split_strategy=train_test_split_strategy))
        if feature_generation:
            creator = creators[StepNames.FEATURE_GENERATION]
            steps.append(creator(self, StepNames.FEATURE_GENERATION, trans_primitives=feature_generation_trans_primitives, max_depth=feature_generation_max_depth, continuous_cols=feature_generation_continuous_cols, datetime_cols=feature_generation_datetime_cols, categories_cols=feature_generation_categories_cols, latlong_cols=feature_generation_latlong_cols, text_cols=feature_generation_text_cols))
        if collinearity_detection:
            creator = creators[StepNames.MULITICOLLINEARITY_DETECTION]
            steps.append(creator(self, StepNames.MULITICOLLINEARITY_DETECTION))
        if drift_detection and X_test is not None:
            creator = creators[StepNames.DRIFT_DETECTION]
            steps.append(creator(self, StepNames.DRIFT_DETECTION, remove_shift_variable=drift_detection_remove_shift_variable, variable_shift_threshold=drift_detection_variable_shift_threshold, threshold=drift_detection_threshold, remove_size=drift_detection_remove_size, min_features=drift_detection_min_features, num_folds=drift_detection_num_folds))
        if feature_selection:
            creator = creators[StepNames.FEATURE_IMPORTANCE_SELECTION]
            steps.append(creator(self, StepNames.FEATURE_IMPORTANCE_SELECTION, strategy=feature_selection_strategy, threshold=feature_selection_threshold, quantile=feature_selection_quantile, number=feature_selection_number))
        creator = creators[StepNames.SPACE_SEARCHING]
        if down_sample_search:
            steps.append(creator(self, StepNames.SPACE_SEARCHING, cv=cv, num_folds=num_folds, size=down_sample_search_size, max_trials=down_sample_search_max_trials, time_limit=down_sample_search_time_limit))
        else:
            steps.append(creator(self, StepNames.SPACE_SEARCHING, cv=cv, num_folds=num_folds))
        if pseudo_labeling and X_test is not None and (task in [const.TASK_BINARY, const.TASK_MULTICLASS]):
            if ensemble_size is not None and ensemble_size > 1:
                creator = creators[StepNames.ENSEMBLE]
                estimator_builder = creator(self, StepNames.ENSEMBLE, scorer=scorer, ensemble_size=ensemble_size)
            else:
                creator = creators[StepNames.TRAINING]
                estimator_builder = creator(self, StepNames.TRAINING, retrain_on_wholedata=retrain_on_wholedata)
            steps.append(estimator_builder)
            creator = creators[StepNames.PSEUDO_LABELING]
            steps.append(creator(self, StepNames.PSEUDO_LABELING, estimator_builder_name=estimator_builder.name, strategy=pseudo_labeling_strategy, proba_threshold=pseudo_labeling_proba_threshold, proba_quantile=pseudo_labeling_proba_quantile, sample_number=pseudo_labeling_sample_number, resplit=pseudo_labeling_resplit))
            two_stage = True
        if feature_reselection:
            creator = creators[StepNames.FEATURE_RESELECTION]
            steps.append(creator(self, StepNames.FEATURE_RESELECTION, scorer=scorer, estimator_size=feature_reselection_estimator_size, strategy=feature_reselection_strategy, threshold=feature_reselection_threshold, quantile=feature_reselection_quantile, number=feature_reselection_number))
            two_stage = True
        if two_stage:
            creator = creators[StepNames.FINAL_SEARCHING]
            if down_sample_search:
                steps.append(creator(self, StepNames.FINAL_SEARCHING, cv=cv, num_folds=num_folds, size=down_sample_search_size, max_trials=down_sample_search_max_trials, time_limit=down_sample_search_time_limit))
            else:
                steps.append(creator(self, StepNames.FINAL_SEARCHING, cv=cv, num_folds=num_folds))
        if ensemble_size is not None and ensemble_size > 1:
            creator = creators[StepNames.FINAL_ENSEMBLE]
            last_step = creator(self, StepNames.FINAL_ENSEMBLE, scorer=scorer, ensemble_size=ensemble_size)
        else:
            creator = creators[StepNames.FINAL_TRAINING]
            last_step = creator(self, StepNames.FINAL_TRAINING, retrain_on_wholedata=retrain_on_wholedata)
        steps.append(last_step)
        import warnings
        warnings.filterwarnings('ignore')
        if log_level is not None:
            _set_log_level(log_level)
        self.run_kwargs = kwargs
        self.evaluation_ = None
        super(CompeteExperiment, self).__init__(steps, hyper_model, X_train, y_train, X_eval=X_eval, y_eval=y_eval, X_test=X_test, eval_size=eval_size, task=task, id=id, callbacks=callbacks, random_state=random_state)

    @staticmethod
    def get_creators(hyper_model, X_train, y_train, X_test=None, X_eval=None, y_eval=None, down_sample_search=False):
        mapping = {StepNames.DATA_ADAPTION: DataAdaptionStep, StepNames.DATA_CLEAN: DataCleanStep, StepNames.FEATURE_GENERATION: FeatureGenerationStep, StepNames.MULITICOLLINEARITY_DETECTION: MulticollinearityDetectStep, StepNames.DRIFT_DETECTION: DriftDetectStep, StepNames.FEATURE_IMPORTANCE_SELECTION: FeatureImportanceSelectionStep, StepNames.SPACE_SEARCHING: SpaceSearchWithDownSampleStep if down_sample_search else SpaceSearchStep, StepNames.ENSEMBLE: EnsembleStep, StepNames.TRAINING: FinalTrainStep, StepNames.FEATURE_RESELECTION: PermutationImportanceSelectionStep, StepNames.PSEUDO_LABELING: PseudoLabelStep, StepNames.FINAL_SEARCHING: SpaceSearchWithDownSampleStep if down_sample_search else SpaceSearchStep, StepNames.FINAL_ENSEMBLE: EnsembleStep, StepNames.FINAL_TRAINING: FinalTrainStep}
        tb = get_tool_box(X_train, y_train, X_test, X_eval, y_eval)
        if hasattr(tb, 'exist_dask_object') and tb.exist_dask_object(X_train, y_train, X_test, X_eval, y_eval):
            mapping[StepNames.ENSEMBLE] = DaskEnsembleStep
            mapping[StepNames.FINAL_ENSEMBLE] = DaskEnsembleStep
            mapping[StepNames.PSEUDO_LABELING] = DaskPseudoLabelStep
        return mapping

    def get_data_character(self):
        data_character = super(CompeteExperiment, self).get_data_character()
        x_types = df_utils.get_x_data_character(self.X_train, self.get_step)
        data_character.update(x_types)
        return data_character

    def run(self, **kwargs):
        run_kwargs = {**self.run_kwargs, **kwargs}
        return super().run(**run_kwargs)

    def to_estimator(self, X_train, y_train, X_test, X_eval, y_eval, steps):
        estimator = super().to_estimator(X_train, y_train, X_test, X_eval, y_eval, steps)
        first_step = steps[0]
        if isinstance(first_step, DataAdaptionStep):
            if str(first_step.target).lower() in DATA_ADAPTION_TARGET_CUML_ALIASES and isinstance(self.X_train, pd.DataFrame) and hasattr(estimator, 'as_local'):
                estimator = estimator.as_local()
        return estimator

    def _repr_html_(self):
        try:
            from hboard_widget.widget import ExperimentSummary
            from IPython.display import display
            display(ExperimentSummary(self))
        except:
            return self.__repr__()

def evaluate_oofs(hyper_model, ensemble_estimator, y_train, metrics):
    from hypernets.tabular.lifelong_learning import select_valid_oof
    from hypernets.tabular.metrics import calc_score
    trials = hyper_model.get_top_trials(ensemble_estimator.ensemble_size)
    if all(['oof' in trial.memo.keys() for trial in trials]):
        oofs = None
        for (i, trial) in enumerate(trials):
            if 'oof' in trial.memo.keys():
                oof = trial.memo['oof']
                if oofs is None:
                    if len(oof.shape) == 1:
                        oofs = np.zeros((oof.shape[0], len(trials)), dtype=np.float64)
                    else:
                        oofs = np.zeros((oof.shape[0], len(trials), oof.shape[-1]), dtype=np.float64)
                oofs[:, i] = oof
        (y_, oofs_) = select_valid_oof(y_train, oofs)
        proba = ensemble_estimator.predictions2predict_proba(oofs_)
        pred = ensemble_estimator.predictions2predict(oofs_)
        scores = calc_score(y_, pred, proba, metrics)
        return scores
    else:
        print('No oof data')
        return None