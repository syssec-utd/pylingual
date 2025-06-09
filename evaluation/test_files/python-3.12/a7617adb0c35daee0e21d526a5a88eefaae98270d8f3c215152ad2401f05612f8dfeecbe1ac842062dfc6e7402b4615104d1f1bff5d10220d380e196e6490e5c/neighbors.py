"""
This module contains Python wrappers for PAL k-nearest neighbors algorithms.

The following classes are available:
    * :class:`KNNClassifier`
    * :class:`KNNRegressor`
"""
import logging
import uuid
import numpy as np
import pandas as pd
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from deprecated import deprecated
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.ml_base import try_drop
from hana_ml.dataframe import quotename
from .sqlgen import trace_sql
from .pal_base import PALBase, create, ParameterTable, ListOfStrings, ListOfTuples, pal_param_register, require_pal_usable, execute_logged
from .utility import version_compare
from . import metrics
logger = logging.getLogger(__name__)

class _KNNBase(PALBase):
    """
    Base class for k-nearest-neighbor algorithm, be able to do classification and regression.
    """
    algorithm_map = {'brute_force': 0, 'kd_tree': 1, 'brure-force': 0, 'kd-tree': 1}
    func_map = {'classification': 0, 'regression': 1}
    voting_map = {'majority': 0, 'distance_weighted': 1, 'distance-weighted': 1}
    aggregate_map = {'average': 0, 'distance_weighted': 1, 'distance-weighted': 1}
    metric_map = {'manhattan': 1, 'euclidean': 2, 'minkowski': 3, 'chebyshev': 4, 'cosine': 6}
    resampling_map = {'classification': ['cv', 'cv_sha', 'cv_hyperband', 'stratified_cv', 'stratified_cv_sha', 'stratified_cv_hyperband', 'bootstrap', 'bootstrap_sha', 'bootstrap_hyperband', 'stratified_bootstrap', 'stratified_bootstrap_sha', 'stratified_bootstrap_hyperband'], 'regression': ['cv', 'cv_sha', 'cv_hyperband', 'bootstrap', 'bootstrap_sha', 'bootstrap_hyperband']}
    evaluation_map = {'classification': {'accuracy': 'ACCURACY', 'f1_score': 'F1_SCORE'}, 'regression': {'rmse': 'RMSE'}}
    search_strategy_map = {'grid': 'grid', 'random': 'random'}
    values_list = {'metric': 'DISTANCE_LEVEL', 'minkowski_power': 'MINKOWSKI_POWER', 'category_weights': 'CATEGORY_WEIGHTS', 'n_neighbors': 'K_NEAREST_NEIGHBOURS', 'voting_type': 'VOTING_TYPE', 'aggregate_type': 'AGGREGATE_TYPE'}
    range_list = ['minkowski_power', 'category_weights', 'n_neighbors']

    def __init__(self, n_neighbors=None, thread_ratio=None, functionality='classification', stat_info=True, voting_type=None, aggregate_type=None, metric=None, minkowski_power=None, category_weights=None, algorithm=None, resampling_method=None, evaluation_metric=None, fold_num=None, repeat_times=None, search_strategy=None, random_search_times=None, random_state=None, timeout=None, progress_indicator_id=None, param_values=None, param_range=None, min_resource_rate=None, reduction_rate=None, aggressive_elimination=None):
        if not hasattr(self, 'hanaml_parameters'):
            setattr(self, 'hanaml_parameters', pal_param_register())
        super(_KNNBase, self).__init__()
        self.pal_funcname = 'PAL_KNN'
        self.map_map = {'metric': self.metric_map, 'aggregate_type': self.aggregate_map, 'voting_type': self.voting_map}
        self.n_neighbors = self._arg('n_neighbors', n_neighbors, int)
        self.thread_ratio = self._arg('thread_ratio', thread_ratio, float)
        self.voting_type = self._arg('voting_type', voting_type, self.voting_map)
        self.aggregate_type = self._arg('aggregate_type', aggregate_type, self.aggregate_map)
        self.stat_info = self._arg('stat_info', stat_info, bool)
        self.metric = self._arg('metric', metric, self.metric_map)
        self.minkowski_power = self._arg('minkowski_power', minkowski_power, float)
        self.algorithm = self._arg('algorithm', algorithm, self.algorithm_map)
        self.category_weights = self._arg('category_weights', category_weights, float)
        self.resampling_method = self._arg('resampling_method', resampling_method, {x: x for x in self.resampling_map[functionality]})
        self.evaluation_metric = self._arg('evaluation_metric', evaluation_metric, self.evaluation_map[functionality])
        self.fold_num = self._arg('fold_num', fold_num, int, required='cv' in str(self.resampling_method))
        self.repeat_times = self._arg('repeat_times', repeat_times, int)
        self.search_strategy = self._arg('search_strategy', search_strategy, self.search_strategy_map, required='sha' in str(self.resampling_method))
        if 'hyperband' in str(self.resampling_method):
            self.search_strategy = 'random'
        self.random_search_times = self._arg('random_search_times', random_search_times, int, required=str(self.search_strategy) == 'random')
        self.random_state = self._arg('random_state', random_state, int)
        self.timeout = self._arg('timeout', timeout, int)
        self.progress_indicator_id = self._arg('progress_indicator_id', progress_indicator_id, str)
        if isinstance(param_range, dict):
            param_range = [(x, param_range[x]) for x in param_range]
        if isinstance(param_values, dict):
            param_values = [(x, param_values[x]) for x in param_values]
        self.param_values = self._arg('param_values', param_values, ListOfTuples)
        self.param_range = self._arg('param_range', param_range, ListOfTuples)
        self.min_resource_rate = self._arg('min_resource_rate', min_resource_rate, float)
        self.reduction_rate = self._arg('reduction_rate', reduction_rate, float)
        self.aggressive_elimination = self._arg('aggressive_elimination', aggressive_elimination, bool)
        self.functionality = self._arg('functionality', functionality, self.func_map)
        search_param_count = 0
        for param in (self.resampling_method, self.evaluation_metric):
            if param is not None:
                search_param_count += 1
        if search_param_count not in (0, 2):
            msg = "'resampling_method', and 'evaluation_metric' must be set together."
            logger.error(msg)
            raise ValueError(msg)
        if self.search_strategy is not None and self.resampling_method is None:
            msg = "'search_strategy' cannot be set if 'resampling_method' is not specified."
            logger.error(msg)
            raise ValueError(msg)
        if self.search_strategy == 'random' and self.random_search_times is None:
            msg = "'random_search_times' must be set when " + "'search_strategy' is set as random."
            logger.error(msg)
            raise ValueError(msg)
        if self.search_strategy is None:
            if self.param_values is not None:
                msg = 'Specifying the values of `{}` '.format(self.param_values[0][0]) + 'for non-parameter-search-strategy' + ' parameter selection is invalid.'
                logger.error(msg)
                raise ValueError(msg)
            if self.param_range is not None:
                msg = 'Specifying the range of `{}` for '.format(self.param_range[0][0]) + 'non-parameter-search-strategy parameter selection is invalid.'
                logger.error(msg)
                raise ValueError(msg)
        if self.search_strategy is not None:
            set_param_list = []
            if self.metric is not None:
                set_param_list.append('metric')
            if self.minkowski_power is not None:
                set_param_list.append('minkowski_power')
            if self.category_weights is not None:
                set_param_list.append('category_weights')
            if self.n_neighbors is not None:
                set_param_list.append('n_neighbors')
            if self.voting_type is not None:
                set_param_list.append('voting_type')
            if self.aggregate_type is not None:
                set_param_list.append('aggregate_type')
            if self.param_values is not None:
                for x in self.param_values:
                    if len(x) != 2:
                        msg = 'Each tuple that specifies the values of a parameter should' + ' contain exactly 2 elements: 1st is parameter name,' + ' 2nd is a list of valid values.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] not in self.values_list:
                        msg = 'Specifying the values of `{}` for '.format(x[0]) + 'parameter selection is invalid.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] in set_param_list:
                        msg = 'Parameter `{}` is invalid for '.format(x[0]) + 're-specification in parameter selection.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] == 'n_neighbors' and (not (isinstance(x[1], list) and all((isinstance(t, int) for t in x[1])))):
                        msg = 'Valid values of `{}` must be a list of int.'.format(x[0])
                        logger.error(msg)
                        raise TypeError(msg)
                    if x[0] in ('category_weights', 'minkowski_power') and (not (isinstance(x[1], list) and all((isinstance(t, (int, float)) for t in x[1])))):
                        msg = 'Valid values of `{}` must be a list of numericals.'.format(x[0])
                        logger.error(msg)
                        raise TypeError(msg)
                    if x[0] == 'aggregate_type' and self.functionality == self.func_map['classification']:
                        msg = "'aggregate_type' is not available for classification."
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] == 'voting_type' and self.functionality == self.func_map['regression']:
                        msg = "'voting_type' is not available for regression."
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] in ('metric', 'aggregate_type', 'voting_type') and (not (isinstance(x[1], list) and all((t in self.map_map[x[0]] for t in x[1])))):
                        msg = ' Some value in `{}` is not valid for `{}`.'.format(x[1], x[0])
                        logger.error(msg)
                        raise TypeError(msg)
                    set_param_list.append(x[0])
            if self.param_range is not None:
                rsz = [3] if self.search_strategy == 'grid' else [2, 3]
                for x in self.param_range:
                    if len(x) != 2:
                        msg = 'Each tuple that specifies the range of a parameter should contain' + ' exactly 2 elements: 1st is parameter name, 2nd is value range.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] not in self.range_list:
                        msg = 'Specifying the values of `{}` for '.format(x[0]) + 'parameter selection is invalid.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] in set_param_list:
                        msg = 'Parameter `{}` is invalid for '.format(x[0]) + 're-specification in parameter selection.'
                        logger.error(msg)
                        raise ValueError(msg)
                    if x[0] == 'n_neighbors' and (not (isinstance(x[1], list) and len(x[1]) in rsz and all((isinstance(t, int) for t in x[1])))):
                        msg = 'Valid values of `{}` must be a list of int.'.format(x[0])
                        logger.error(msg)
                        raise TypeError(msg)
                    if x[0] in ('category_weights', 'minkowski_power') and (not (isinstance(x[1], list) and len(x[1]) in rsz and all((isinstance(t, (int, float)) for t in x[1])))):
                        msg = 'Valid values of `{}` must be a list of numericals.'.format(x[0])
                        logger.error(msg)
                        raise TypeError(msg)
                    set_param_list.append(x[0])
        self.key = None
        self.features = None
        self.label = None
        self.attribute_num = None
        self.stats_ = None
        self.optim_param_ = None
        self.categorical_variable = None
        self.string_variable = None
        self.variable_weight = None
        self._training_set = None
        self.model_ = None

    def _check_variable_weight(self, variable_weight):
        self.variable_weight = self._arg('variable_weight', variable_weight, dict)
        for key, value in self.variable_weight.items():
            if not isinstance(key, str):
                msg = 'The key of variable_weight must be a string!'
                logger.error(msg)
                raise TypeError(msg)
            if not isinstance(value, (float, int)):
                msg = 'The value of variable_weight must be a float!'
                logger.error(msg)
                raise TypeError(msg)

    def _df_to_param_rows(self, df):
        new_tp = None
        if version_compare(pd.__version__, '1.2.0'):
            new_tp = [tuple(i.to_list()) for i in df.iloc]
        else:
            new_tp = list(zip(*[df[c_vals].values.tolist() for c_vals in df]))
        new_tp = [tuple([None if isinstance(x, float) and np.isnan(x) else x for x in y]) for y in new_tp]
        new_tp = [(x[0], int(x[1]) if x[1] is not None else None, x[2], x[3]) for x in new_tp]
        return new_tp

    @trace_sql
    def _fit(self, data, key=None, features=None, label=None, categorical_variable=None, string_variable=None, variable_weight=None):
        if not hasattr(self, 'hanaml_fit_params'):
            setattr(self, 'hanaml_fit_params', pal_param_register())
        conn = data.connection_context
        require_pal_usable(conn)
        index = data.index
        if isinstance(index, str) and isinstance(key, str):
            if index != key:
                msg = "Discrepancy between the designated key column '{}' ".format(key) + "and the designated index column '{}'.".format(index)
                logger.warning(msg)
        key = index if key is None else key
        self.key = self._arg('key', key, str, required=self.resampling_method is None)
        cols = data.columns
        if self.key is not None:
            cols.remove(self.key)
        self.label = self._arg('label', label, str)
        if label is None:
            self.label = cols[-1]
        if isinstance(features, str):
            features = [features]
        self.features = self._arg('features', features, ListOfStrings)
        if self.features is None:
            self.features = cols
            self.features.remove(self.label)
        if isinstance(categorical_variable, str):
            categorical_variable = [categorical_variable]
        self.categorical_variable = self._arg('categorical_variable', categorical_variable, ListOfStrings)
        if isinstance(string_variable, str):
            string_variable = [string_variable]
        self.string_variable = self._arg('string_variable', string_variable, ListOfStrings)
        if variable_weight is not None:
            self._check_variable_weight(variable_weight)
        if not data.dtypes([self.label])[0][1] in ('INT', 'DOUBLE') or (self.categorical_variable is not None and self.label in self.categorical_variable):
            if self.functionality == self.func_map['regression']:
                msg = 'The label column data must be numerical for regression.'
                logger.error(msg)
                raise ValueError(msg)
        if data.dtypes([self.label])[0][1] == 'DOUBLE' and self.functionality == self.func_map['classification']:
            msg = 'The label column data cannot be float for classification.'
            logger.error(msg)
            raise ValueError(msg)
        self.attribute_num = len(self.features)
        self._training_set = data[[self.key] + self.features + [self.label]]
        self.model_ = [self._training_set]
        if self.key is None:
            self._training_set = self._training_set.add_id('ID_ADD')
            self._training_set.set_index('ID_ADD')
        param_rows = [('K_NEAREST_NEIGHBOURS', self.n_neighbors, None, None), ('HAS_ID', self.key is not None, None, None), ('THREAD_RATIO', None, self.thread_ratio, None), ('ATTRIBUTE_NUM', self.attribute_num, None, None), ('FUNCTIONALITY', self.functionality, None, None), ('DEPENDENT_VARIABLE', None, None, self.label), ('DISTANCE_LEVEL', self.metric, None, None), ('MINKOWSKI_POWER', None, self.minkowski_power, None), ('CATEGORY_WEIGHTS', None, self.category_weights, None), ('METHOD', self.algorithm, None, None)]
        if self.functionality == self.func_map['classification']:
            param_rows.extend([('VOTING_TYPE', self.voting_type, None, None)])
            param_rows.extend([('CATEGORICAL_VARIABLE', None, None, label)])
        else:
            param_rows.extend([('AGGREGATE_TYPE', self.aggregate_type, None, None)])
        if self.categorical_variable is not None:
            param_rows.extend((('CATEGORICAL_VARIABLE', None, None, variable) for variable in self.categorical_variable))
        if self.string_variable is not None:
            param_rows.extend((('STRING_VARIABLE', None, None, variable) for variable in self.string_variable))
        if self.variable_weight is not None:
            param_rows.extend((('VARIABLE_WEIGHT', None, value, key) for key, value in self.variable_weight.items()))
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        param_tbl_name = '#PAL_KNN_PARAM_TBL_{}'.format(unique_id)
        param_tbl = ParameterTable(param_tbl_name).with_data(param_rows)
        create(conn, param_tbl)
        if self.resampling_method is not None and self.evaluation_metric is not None:
            param_arrs = [('RESAMPLING_METHOD', None, None, self.resampling_method), ('EVALUATION_METRIC', None, None, self.evaluation_metric), ('SEED', self.random_state, None, None), ('REPEAT_TIMES', self.repeat_times, None, None), ('PARAM_SEARCH_STRATEGY', None, None, self.search_strategy), ('FOLD_NUM', self.fold_num, None, None), ('RANDOM_SEARCH_TIMES', self.random_search_times, None, None), ('TIMEOUT', self.timeout, None, None), ('PROGRESS_INDICATOR_ID', None, None, self.progress_indicator_id), ('MIN_RESOURCE_RATE', None, self.min_resource_rate, None), ('REDUCTION_RATE', None, self.reduction_rate, None), ('AGGRESSIVE_ELIMINATION', self.aggressive_elimination, None, None)]
            if self.param_values is not None:
                for x in self.param_values:
                    value_str = x[1]
                    if isinstance(x[1][0], str):
                        value_str = [self.map_map[x[0]][val] for val in x[1]]
                    values = str(value_str).replace('[', '{').replace(']', '}')
                    param_arrs.extend([(self.values_list[x[0]] + '_VALUES', None, None, values)])
            if self.param_range is not None:
                for x in self.param_range:
                    range_ = str(x[1])
                    if len(x[1]) == 2 and self.search_strategy == 'random':
                        range_ = range_.replace(',', ',,')
                    param_arrs.extend([(self.values_list[x[0]] + '_RANGE', None, None, range_)])
            tables = ['STATISTICS', 'OPTIMAL_PARAM']
            tables = ['#PAL_KNN_{}_TBL_{}_{}'.format(tbl, self.id, unique_id) for tbl in tables]
            stats_tbl, optim_param_tbl = tables
            param_array = param_rows
            param_array.extend(param_arrs)
            try:
                self._call_pal_auto(conn, 'PAL_KNN_CV', self._training_set, ParameterTable().with_data(param_array), *tables)
            except dbapi.Error as db_err:
                logger.exception(str(db_err))
                try_drop(conn, tables)
                raise
            except pyodbc.Error as db_err:
                logger.exception(str(db_err.args[1]))
                try_drop(conn, tables)
                raise
            self.stats_ = conn.table(stats_tbl)
            self.optim_param_ = conn.table(optim_param_tbl)
            with conn.connection.cursor() as cur:
                sql_cmd = 'SELECT PARAM_NAME, INT_VALUE, DOUBLE_VALUE, ' + 'STRING_VALUE FROM {} INTO {}'.format(quotename(optim_param_tbl), quotename(param_tbl_name))
                execute_logged(cur, sql_cmd, conn.sql_tracer, conn)
        self.model_.append(conn.table(param_tbl_name))

    @trace_sql
    def _predict(self, data, key=None, features=None, interpret=False, sample_size=None, top_k_attributions=None, random_state=None):
        conn = data.connection_context
        if self.model_ is None:
            raise FitIncompleteError('Model not initialized. Perform a fit first.')
        index = data.index
        key = self._arg('key', key, str, required=not isinstance(index, str))
        if isinstance(index, str):
            if key is not None and index != key:
                msg = "Discrepancy between the designated key column '{}' ".format(key) + "and the designated index column '{}'.".format(index)
                logger.warning(msg)
        key = index if key is None else key
        cols = data.columns
        cols.remove(key)
        if isinstance(features, str):
            features = [features]
        features = self._arg('features', features, ListOfStrings)
        if features is None:
            features = cols
        training_cols = self.model_[0].columns
        training_cols.remove(training_cols[0])
        training_cols.remove(training_cols[-1])
        training_features = training_cols
        if not set(training_features) <= set(features):
            msg = 'Features in training data table is not recognized in prediction one.'
            logger.error(msg)
            raise ValueError(msg)
        attribute_num = len(features)
        if attribute_num != len(training_features):
            msg = "'Training dataset' has a different dimension from 'prediction dataset'."
            logger.error(msg)
            raise ValueError(msg)
        interpret = self._arg('interpret', interpret, bool)
        if interpret is None:
            interpret = False
        sample_size = self._arg('sample_size', sample_size, int)
        top_k_attributions = self._arg('top_k_attributions', top_k_attributions, int)
        random_state = self._arg('random_state', random_state, int)
        data_ = data[[key] + features]
        param_rows = [] if interpret is False else [('SAMPLESIZE', sample_size, None, None), ('TOP_K_ATTRIBUTIONS', top_k_attributions, None, None), ('SEED', random_state, None, None)]
        try:
            param_df = self.model_[1].collect()
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            raise
        new_tp = self._df_to_param_rows(param_df)
        param_rows.extend(new_tp)
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        tables = ['RESULT', 'STATISTICS']
        tables = ['#PAL_KNN_{}_TBL_{}_{}'.format(tbl, self.id, unique_id) for tbl in tables]
        res_tbl, stats_tbl = tables
        pal_proc = 'PAL_KNN_INTERPRET' if interpret is True else 'PAL_KNN'
        try:
            self._call_pal_auto(conn, pal_proc, self.model_[0], data_, ParameterTable().with_data(param_rows), res_tbl, stats_tbl)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, tables)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, tables)
            raise
        return (conn.table(tables[0]), conn.table(tables[1]))

class KNNClassifier(_KNNBase):
    """
    K-Nearest Neighbor (KNN) is a memory-based classification or regression method
    with no explicit training phase. It assumes similar instances
    should have similar labels or values.

    Parameters
    ----------

    n_neighbors : int, optional
        Number of nearest neighbors (k).

        Default to 1.
    thread_ratio : float, optional
        Specifies the ratio of total number of threads that can be used by this function.

        The range of this parameter is from 0 to 1, where 0 means only using 1 thread, and
        1 means using at most all the currently available threads.

        Values outside this range are ignored and this function heuristically determines the number of threads to use.

        Default to 0.0.
    voting_type : {'majority', 'distance-weighted'}, optional
        Voting type.

        Default to 'distance-weighted'.
    stat_info : bool, optional
        Indicate if statistic information will be stored into the STATISTIC table.

        Only valid when model evaluation/parameter selection is not activated.

        Default to True.
    metric : {'manhattan', 'euclidean', 'minkowski', 'chebyshev', 'cosine'}, optional
        Ways to compute the distance between data points.

        Defaults to 'euclidean'.
    minkowski_power : float, optional
        When ``metric`` is set to 'minkowski', this parameter controls the value of power.

        Only valid when ``metric`` is set as 'minkowski'.

        Defaults to 3.0.
    category_weights : float, optional
        Represents the weight of category attributes.

        Default to 0.707.
    algorithm : {'brute-force', 'kd-tree'}, optional
        Algorithm used to compute the nearest neighbors.

        Defaults to 'brute-force'.
    factor_num : int, optional
        The factorization dimensionality.

        Default to 4.
    random_state : int, optional
        Specifies the seed for random number generator.

          - 0: Uses the current time as the seed.
          - Others: Uses the specified value as the seed.

        Default to 0.

    resampling_method : str, optional
        Specifies the resampling method for model evaluation or parameter selection:

          - 'cv'
          - 'cv_sha'
          - 'cv_hyperband'
          - 'stratified_cv'
          - 'stratified_cv_sha'
          - 'stratified_cv_hyperband'
          - 'bootstrap'
          - 'bootstrap_sha'
          - 'bootstrap_hyperband'
          - 'stratified_bootstrap'
          - 'stratified_bootstrap_sha'
          - 'stratified_bootstrap_hyperband'

        If no value is specified for this parameter, neither model evaluation
        nor parameter selection is activated.

        No default value.

        .. note::
            Resampling methods that end with 'sha' or 'hyperband' are used for
            parameter selection only, not for model evaluation.

    evaluation_metric : {'accuracy', 'f1_score'}, optional
        Specifies the evaluation metric for model evaluation or parameter selection.

        If not specified, neither model evaluation nor parameter selection is activated.

        No default value.
    fold_num : int, optional
        Specifies the fold number for the cross validation method.

        Mandatory and valid only when ``resampling_method`` is set to one of the following values:
        'cv', 'cv_sha', 'cv_hyperband', 'stratified_cv', 'stratified_cv_sha', 'stratified_cv_hyperband'.

        No default value.
    repeat_times : int, optional
        Specifies the number of repeat times for resampling.

        Default to 1.
    search_strategy : {'random', 'grid'}, optional
        The search strategy for parameters.

        Mandatory if ``resampling_method`` is specified and ends with 'sha'.

        Defaults to 'random' and cannot be changed if ``resampling_method`` is specified and
        ends with 'hyperband'; otherwise no default value, and parameter selection
        cannot be carried out if not specified.

    random_search_times : int, optional
        Specifies the number of times to randomly select candidate parameters for selection.

        Mandatory and valid when ``search_strategy`` is set to 'random'.

        No default value.
    timeout : int, optional
        Specifies maximum running time for model evaluation or parameter selection, in seconds.

        No timeout when 0 is specified.

        Default to 0.
    progress_indicator_id : str, optional
        Sets an ID of progress indicator for model evaluation or parameter selection.

        No progress indicator is active if no value is provided.

        No default value.
    param_values : dict or ListOfTuples, optional

        Specifies values of parameters to be selected.

        Input should be a dict, or a list of tuples of two elements, with key/1st element
        being the target parameter name,
        and value/2nd element being the a list of values for selection.

        Only valid when parameter selection is activated.

        Valid Parameter names include:        ``metric``, ``minkowski_power``, ``category_weights``,
        ``n_neighbors``, ``voting_type``.

        No default value.
    param_range : dict or ListOfTuples, optional

        Specifies ranges of parameters to be selected.

        Input should be a dict, or a list of tuples of two elements, with key/1st element
        the name of the target parameter,
        while value/2nd element being a list that specifies the range of parameters with the
        following format: [start, step, end] or [start, end].

        Only valid when parameter selection is activated.

        Valid parameter names include: ``minkowski_power``, ``category_weights``, ``n_neighbors``.

        No default value.
    min_resource_rate : float, optional
        Specifies the minimum resource rate that should be used in SHA or Hyperband iteration.

        Valid only when ``resampling_method`` takes one of the following values:
        'cv_sha', 'stratified_cv_sha', 'bootstrap_sha', 'stratified_bootstrap_sha',
        'cv_hyperband', 'stratified_cv_hyperband', 'bootstrap_hyperband',
        'stratified_bootstrap_hyperband'.

        Defaults to 0.0.
    reduction_rate : float, optional
        Specifies reduction rate in SHA or Hyperband method.

        For each round, the available parameter candidate size will be divided by value of this parameter.
        Thus valid value for this parameter must be greater than 1.0

        Valid only when ``resampling_method`` is set to one of the following values:
        'cv_sha', 'stratified_cv_sha', 'bootstrap_sha', 'stratified_bootstrap_sha',
        'cv_hyperband', 'stratified_cv_hyperband', 'bootstrap_hyperband',
        'stratified_bootstrap_hyperband'.

        Defaults to 3.0.

    aggressive_elimination : bool, optional
        Specifies whether to apply aggressive elimination while using SHA method.

        Aggressive elimination happens when the data size and parameters size to be searched does not match
        and there are still bunch of parameters to be searched while data size reaches its upper limits.
        If aggressive elimination is applied, lower bound of limit of data size will be used multiple times
        first to reduce number of parameters.

        Valid only when ``resampling_method`` is set to one of the following:
        'cv_sha', 'stratified_cv_sha', 'bootstrap_sha', 'stratified_bootstrap_sha'.

        Defaults to True.

    Attributes
    ----------
    _training_set : DataFrame
        Input training data with structured column arrangement.
        If model evaluation or parameter selection is not enabled, the first column must be the
        ID column, followed by feature columns.

    Examples
    --------
    Input dataframe for classification training:

    >>> df_class_train.collect()
       ID  X1      X2 X3  TYPE
    0   0   2     1.0  A     1
    1   1   3    10.0  A    10
    2   2   3    10.0  B    10
    3   3   3    10.0  C     1
    4   4   1  1000.0  C     1
    5   5   1  1000.0  A    10
    6   6   1  1000.0  B    99
    7   7   1   999.0  A    99
    8   8   1   999.0  B    10
    9   9   1  1000.0  C    10

    Creating KNNClassifier instance:

    >>> knn  = KNNClassifier(thread_ratio=1, algorithm='kd_tree',
                             n_neighbors=3, voting_type='majority')

    Performing fit() on given dataframe:

    >>> knn.fit(self.df_class_train, key='ID', label='TYPE')

    Performing predict() on given predicting dataframe:

    Input prediction dataframe:

    >>> df_class_predict.collect()
       ID  X1       X2 X3
    0   0   2      1.0  A
    1   1   1     10.0  C
    2   2   1     11.0  B
    3   3   3  15000.0  C
    4   4   2   1000.0  C
    5   5   1   1001.0  A
    6   6   1    999.0  A
    7   7   3    999.0  B

    >>> res, stats = knn.predict(df_class_predict, key='ID', categorical_variable='X1')

    >>> res.collect()
       ID TARGET
    0   0     10
    1   1     10
    2   2     10
    3   3      1
    4   4      1
    5   5      1
    6   6     10
    7   7     99

    >>> stats.collect().head(10)
        TEST_ID  K  TRAIN_ID      DISTANCE
    0         0  1         0      0.000000
    1         0  2         1      9.999849
    2         0  3         2     10.414000
    3         1  1         3      0.999849
    4         1  2         1      1.414000
    5         1  3         2      1.414000
    6         2  1         2      1.999849
    7         2  2         1      2.414000
    8         2  3         3      2.414000
    9         3  1         4  14000.999849
    """

    def __init__(self, n_neighbors=None, thread_ratio=None, stat_info=None, voting_type=None, metric=None, minkowski_power=None, category_weights=None, algorithm=None, resampling_method=None, evaluation_metric=None, fold_num=None, repeat_times=None, search_strategy=None, random_search_times=None, random_state=None, timeout=None, progress_indicator_id=None, param_values=None, param_range=None, min_resource_rate=None, reduction_rate=None, aggressive_elimination=None):
        setattr(self, 'hanaml_parameters', pal_param_register())
        super(KNNClassifier, self).__init__(functionality='classification', n_neighbors=n_neighbors, thread_ratio=thread_ratio, stat_info=stat_info, voting_type=voting_type, metric=metric, minkowski_power=minkowski_power, category_weights=category_weights, algorithm=algorithm, resampling_method=resampling_method, evaluation_metric=evaluation_metric, fold_num=fold_num, repeat_times=repeat_times, search_strategy=search_strategy, random_search_times=random_search_times, random_state=random_state, timeout=timeout, progress_indicator_id=progress_indicator_id, param_values=param_values, param_range=param_range, min_resource_rate=min_resource_rate, reduction_rate=reduction_rate, aggressive_elimination=aggressive_elimination)

    def fit(self, data, key=None, features=None, label=None, categorical_variable=None, string_variable=None, variable_weight=None):
        """
        Build the KNNClassifier training dataset with the input dataframe.
        Assign key, features, and label column.

        Parameters
        ----------
        data : DataFrame
            Data to be fit.
        key : str, optional
            Name of the ID column.

            Required if parameter selection/model evaluation is not activated, unless
            ``data`` is indexed by a single column(the column name will be the default value
            of ``key``).

            If ``key`` is not provided when activating parameter-selection/model-evaluation, then:

                - if ``data`` is indexed by a single column, then ``key`` defaults
                  to that index column;
                - otherwise, it is assumed that ``data`` contains no ID column.

        features : str/ListOfStrings, optional
            Name of the feature columns.
        label : str, optional
            Specifies the dependent variable.

            Default to last column name.

        categorical_variable : str or list of str, optional
            Indicates whether or not a column data is actually corresponding to a category variable
            even the data type of this column is INTEGER.

            By default, VARCHAR or NVARCHAR is category variable, and INTEGER or DOUBLE is continuous variable.

            Defaults to None.

        string_variable : str or list of str, optional
            Indicates a string column storing not categorical data.
            Levenshtein distance is used to calculate similarity between two strings.
            Ignored if it is not a string column.

            Defaults to None.

        variable_weight : dict, optional
            Specifies the weight of a variable participating in distance calculation.
            The value must be greater or equal to 0. Defaults to 1 for variables not specified.

            Defaults to None.

        Returns
        -------
        KNNClassifier

            A fitted object.

        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        self._fit(data=data, key=key, features=features, label=label, categorical_variable=categorical_variable, string_variable=string_variable, variable_weight=variable_weight)
        return self

    def predict(self, data, key=None, features=None, interpret=False, sample_size=None, top_k_attributions=None, random_state=None):
        """
        Prediction for the input data with the training dataset.
        Training data set must be constructed through the fit function first.

        Parameters
        ----------
        data : DataFrame
            Prediction data.

        key : str, optional
            Name of the ID column.

            Mandatory if ``data`` is not indexed, or the index of ``data`` contains multiple columns.

            Defaults to the single index column of ``data`` if not provided.

        features : str/ListOfStrings, optional
            Name of the feature columns.

        interpret : int, optional
            Specifies whether or not to interpret the prediction results.

            Defaults to False(i.e. not to interpret the prediction results).

        sample_size : int, optional
            Specifies the number of sampled combinations of features.

                - 0 : Heuristically determined by algorithm
                - Others : The specified sample size

            Defaults to 0.

        top_k_attributions : int, optional
            Specifies the number of features with highest attributions to output.

            Defaults to 10.

        random_state : int, optional
            Specifies the seed for random number generator when sampling the combination of features.

                - 0 : User current time as seed
                - Others : The actual seed

            Defaults to 0.

        Returns
        -------
        DataFrame
            KNN predict results. Structured as follows:

              - ID: Prediction data ID.
              - TARGET: Predicted label.
              - REASON_CODE: interpretation of of result. This column is available only if
                ``interpret`` is True.

            KNN prediction statistics information. Structured as follows:

              - TEST\\_ + ID column name of prediction data: Prediction data ID.
              - K: K number.
              - TRAIN\\_ + ID column name of training data: Train data ID.
              - DISTANCE: Distance.
        """
        return super(KNNClassifier, self)._predict(data=data, key=key, features=features, interpret=interpret, sample_size=sample_size, top_k_attributions=top_k_attributions, random_state=random_state)

class KNNRegressor(_KNNBase):
    """
    K-Nearest Neighbor (KNN) is a memory-based classification or regression method
    with no explicit training phase. It assumes similar instances
    should have similar labels or values.

    Parameters
    ----------

    n_neighbors : int, optional
        Number of nearest neighbors (k).

        Default to 1.
    thread_ratio : float, optional
        Specifies the ratio of total number of threads that can be used by this function.

        The range of this parameter is from 0 to 1, where 0 means only using 1 thread, and
        1 means using at most all the currently available threads.

        Values outside this range are ignored and this function heuristically determines the number of threads to use.

        Default to 0.0.
    aggregate_type : {'average', 'distance-weighted'}, optional
        Aggregate type.

        Default to 'distance-weighted'.
    stat_info : bool, optional
        Indicate if statistic information will be stored into the STATISTIC table.

        Only valid when model evaluation/parameter selection is not activated.

        Default to True.
    metric : {'manhattan', 'euclidean', 'minkowski', 'chebyshev'}, optional
        Ways to compute the distance between data points.

        Defaults to 'euclidean'.
    minkowski_power : float, optional
        When Minkowski is used for ``metric``, this parameter controls the value of power.

        Only valid when ``metric`` is set as 'minkowski'.

        Defaults to 3.0.
    category_weights : float, optional
        Represents the weight of category attributes.

        Default to 0.707.
    algorithm : {'brute-force', 'kd-tree'}, optional
        Algorithm used to compute the nearest neighbors.

        Defaults to 'brute-force'.
    factor_num : int, optional
        The factorization dimensionality.

        Default to 4.
    random_state : int, optional
        Specifies the seed for random number generator.

          - 0: Uses the current time as the seed.
          - Others: Uses the specified value as the seed.

        Default to 0.
    resampling_method : str, optional
        Specifies the resampling method for model evaluation or parameter selection:

          - 'cv'
          - 'cv_sha'
          - 'cv_hyperband'
          - 'bootstrap'
          - 'bootstrap_sha'
          - 'bootstrap_hyperband'

        If not specified, neither model evaluation nor parameters selection is activated.

        No default value.

        .. note::
            Resampling methods that end with 'sha' or 'hyperband' are used for
            parameter selection only, not for model evaluation.
    evaluation_metric : {'rmse'}, optional
        Specifies the evaluation metric for model evaluation or parameter selection.

        If not specified, neither model evaluation nor parameter selection is activated.

        No default value.
    fold_num : int, optional
        Specifies the fold number for the cross validation method.

        Mandatory and valid only when ``resampling_method`` is set to 'cv', 'cv_sha' or
        'cv_hyperband'.

        No default value.
    repeat_times : int, optional
        Specifies the number of repeat times for resampling.

        Default to 1.
    search_strategy : {'random', 'grid'}, optional
        The search strategy for parameters.

        Mandatory if ``resampling_method`` is specified and ends with 'sha'.

        Defaults to 'random' and cannot be changed if ``resampling_method`` is specified and
        ends with 'hyperband'; otherwise no default value, and parameter selection
        cannot be carried out if not specified.
    random_search_times : int, optional
        Specifies the number of times to randomly select candidate parameters for selection.

        Mandatory and valid when ``search_strategy`` is set to 'random'.

        No default value.
    timeout : int, optional
        Specifies maximum running time for model evaluation or parameter selection, in seconds.

        No timeout when 0 is specified.

        Default to 0.
    progress_indicator_id : str, optional
        Sets an ID of progress indicator for model evaluation or parameter selection.

        No progress indicator is active if no value is provided.

        No default value.
    param_values : ListOfTuples, optional

        Specifies values of parameters to be selected.

        Input should be a dict, or a list of size-two tuples, with key/1st element
        being the target parameter name,
        and value/2nd element being the a list of valued for selection.

        Valid only when parameter selection is activated.

        Valid Parameter names include: 'metric', 'minkowski_power', 'category_weights',
                                      'n_neighbors', 'aggregate_type'.

        No default value.
    param_range : ListOfTuples, optional
        Specifies ranges of parameters to be selected.

        Input should be a dict, or a list of size-two tuples, with key/1st element
        being the name of the target parameter,
        and value/2nd element being a list that specifies the range of parameters with
        [start, step, end] or [start, end].

        Valid only when parameter selection is activated.

        Valid parameter names include: 'minkowski_power', 'category_weights', 'n_neighbors'.

        No default value.
    min_resource_rate : float, optional
        Specifies the minimum resource rate that should be used in SHA or Hyperband iteration.

        Valid only when ``resampling_method`` takes one of the following values:
        'cv_sha', 'bootstrap_sha', 'cv_hyperband', 'bootstrap_hyperband'.

        Defaults to 0.0.

    reduction_rate : float, optional
        Specifies reduction rate in SHA or Hyperband method.

        For each round, the available parameter candidate size will be divided by value of this parameter.
        Thus valid value for this parameter must be greater than 1.0

        Valid only when ``resampling_method`` is set to one of the following values:
        'cv_sha', 'bootstrap_sha', 'cv_hyperband', 'bootstrap_hyperband'.

        Defaults to 3.0.

    aggressive_elimination : bool, optional
        Specifies whether to apply aggressive elimination while using SHA method.

        Aggressive elimination happens when the data size and parameters size to be searched does not match
        and there are still bunch of parameters to be searched while data size reaches its upper limits.
        If aggressive elimination is applied, lower bound of limit of data size will be used multiple times
        first to reduce number of parameters.

        Valid only when ``resampling_method`` is set to 'cv_sha' or 'bootstrap_sha'.

    Attributes
    ----------
    _training_set : DataFrame
        Input training data with structured column arrangement.
        If model evaluation or parameter selection is not enabled, the first column must be the
        ID column, following by feature columns.

    Examples
    --------
    Input dataframe for regression training:

    >>> df_regr_train.collect()
        ID  X1      X2 X3 VALUE
    0   0   2     1.0  A      1
    1   1   3    10.0  A     10
    2   2   3    10.0  B     10
    3   3   3    10.0  C      1
    4   4   1  1000.0  C      1
    5   5   1  1000.0  A     10
    6   6   1  1000.0  B     99
    7   7   1   999.0  A     99
    8   8   1   999.0  B     10
    9   9   1  1000.0  C     10

    Creating KNNRegressor instance:

    >>> knn  = KNNRegressor(thread_ratio=1, algorithm='kd_tree',
                            n_neighbors=3, aggregate_type='average')

    Performing fit() on given dataframe:

    >>> knn.fit(df_regr_train, key='ID', categorical_variable='X1', label='VALUE')

    Performing predict() on given predicting dataframe:

    Input prediction dataframe:

    >>> df_class_predict.collect()
       ID  X1       X2 X3
    0   0   2      1.0  A
    1   1   1     10.0  C
    2   2   1     11.0  B
    3   3   3  15000.0  C
    4   4   2   1000.0  C
    5   5   1   1001.0  A
    6   6   1    999.0  A
    7   7   3    999.0  B

    >>> res, stats = knn.predict(self.df_class_predict, key='ID', categorical_variable='X1')

    >>> res.collect()
        ID              TARGET
    0   0                   7
    1   1                   7
    2   2                   7
    3   3  36.666666666666664
    4   4  36.666666666666664
    5   5  36.666666666666664
    6   6  39.666666666666664
    7   7   69.33333333333333

    >>> stats.collect().head(10)
        TEST_ID  K  TRAIN_ID      DISTANCE
    0         0  1         0      0.000000
    1         0  2         1      9.999849
    2         0  3         2     10.414000
    3         1  1         3      0.999849
    4         1  2         1      1.414000
    5         1  3         2      1.414000
    6         2  1         2      1.999849
    7         2  2         1      2.414000
    8         2  3         3      2.414000
    9         3  1         4  14000.999849
    """

    def __init__(self, n_neighbors=None, thread_ratio=None, stat_info=None, aggregate_type=None, metric=None, minkowski_power=None, category_weights=None, algorithm=None, resampling_method=None, evaluation_metric=None, fold_num=None, repeat_times=None, search_strategy=None, random_search_times=None, random_state=None, timeout=None, progress_indicator_id=None, param_values=None, param_range=None, min_resource_rate=None, reduction_rate=None, aggressive_elimination=None):
        setattr(self, 'hanaml_parameters', pal_param_register())
        super(KNNRegressor, self).__init__(functionality='regression', n_neighbors=n_neighbors, thread_ratio=thread_ratio, stat_info=stat_info, aggregate_type=aggregate_type, metric=metric, minkowski_power=minkowski_power, category_weights=category_weights, algorithm=algorithm, resampling_method=resampling_method, evaluation_metric=evaluation_metric, fold_num=fold_num, repeat_times=repeat_times, search_strategy=search_strategy, random_search_times=random_search_times, random_state=random_state, timeout=timeout, progress_indicator_id=progress_indicator_id, param_values=param_values, param_range=param_range, min_resource_rate=min_resource_rate, reduction_rate=reduction_rate, aggressive_elimination=aggressive_elimination)

    def fit(self, data, key=None, features=None, label=None, categorical_variable=None, string_variable=None, variable_weight=None):
        """
        Build the KNNRegrssor training dataset with the input dataframe.
        Assign key, features, and label column.

        Parameters
        ----------
        data : DataFrame
            Data to be fit.
        key : str, optional
            Name of the ID column.

            Required if parameter selection/model evaluation is not activated, unless
            ``data`` is indexed by a single column(the column name will be the default value
            of ``key``).

            If ``key`` is not provided when activating parameter-selection/model-evaluation, then:

                - if ``data`` is indexed by a single column, then ``key`` defaults
                  to that index column;
                - otherwise, it is assumed that ``data`` contains no ID column.

        features : str/ListOfStrings, optional
            Name of the feature columns.
        label : str, optional
            Specifies the dependent variable.

            Default to last column name.
        categorical_variable : str or list of str, optional
            Indicates whether or not a column data is actually corresponding to a category variable even the data type of this column is INTEGER.

            By default, VARCHAR or NVARCHAR is category variable, and INTEGER or DOUBLE is continuous variable.

            Defaults to None.
        string_variable : str or list of str, optional
            Indicates a string column storing not categorical data.

            Levenshtein distance is used to calculate similarity between two strings.

            Ignored if it is not a string column.

            Defaults to None.
        variable_weight : dict, optional
            Specifies the weight of a variable participating in distance calculation.

            The value must be greater or equal to 0. Defaults to 1 for variables not specified.

            Defaults to None.

        Returns
        ---------
        KNNRegressor
            A fitted object.
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        self._fit(data=data, key=key, features=features, label=label, categorical_variable=categorical_variable, string_variable=string_variable, variable_weight=variable_weight)
        return self

    def predict(self, data, key=None, features=None, interpret=False, sample_size=None, top_k_attributions=None, random_state=None):
        """
        Prediction for the input data with the training dataset. Training data set must be
        constructed through the fit function first.

        Parameters
        ----------
        data : DataFrame
            Prediction data.
        key : str, optional
            Name of the ID column.

            Mandatory if ``data`` is not indexed, or the index of ``data`` contains multiple columns.

            Defaults to the single index column of ``data`` if not provided.

        features : str/ListOfStrings, optional
            Name of the feature columns.

        interpret : int, optional
            Specifies whether or not to interpret the prediction results.

            Defaults to False(i.e. not to interpret the prediction results).

        sample_size : int, optional
            Specifies the number of sampled combinations of features.

                - 0 : Heuristically determined by algorithm
                - Others : The specified sample size

            Defaults to 0.

        top_k_attributions : int, optional
            Specifies the number of features with highest attributions to output.

            Defaults to 10.

        random_state : int, optional
            Specifies the seed for random number generator when sampling the combination of features.

                - 0 : User current time as seed
                - Others : The actual seed

            Defaults to 0.

        Returns
        -------
        DataFrame
            KNN predict results. Structured as following:

                - ID: Prediction data ID.
                - TARGET: Predicted value.
                - REASON_CODE: interpretation of of result. This column is available only if
                  ``interpret`` is True.

            KNN prediction statistics information. Structured as following:

                - TEST\\_ + ID column name of prediction data: Prediction data ID.
                - K: K number.
                - TRAIN\\_ + ID column name of training data: Train data ID.
                - DISTANCE: Distance.
        """
        return super(KNNRegressor, self)._predict(data=data, key=key, features=features, interpret=interpret, sample_size=sample_size, top_k_attributions=top_k_attributions, random_state=random_state)

@deprecated('This method is deprecated. Please use KNNClassifier and KNNRegressor instead.')
class KNN(PALBase):
    """
    K-Nearest Neighbor(KNN) model that handles classification problems.

    Parameters
    ----------

    n_neighbors : int, optional
        Number of nearest neighbors.

        Defaults to 1.
    thread_ratio : float, optional
        Controls the proportion of available threads to use.

        The value range is from 0 to 1, where 0 indicates
        a single thread, and 1 indicates up to all available threads.

        Values between 0 and 1 will use up to that percentage of available
        threads.

        Values outside this range tell PAL to heuristically determine
        the number of threads to use.

        Defaults to 0.
    voting_type : {'majority', 'distance-weighted'}, optional
        Method used to vote for the most frequent label of the K
        nearest neighbors.

        Defaults to 'distance-weighted'.
    stat_info : bool, optional
        Controls whether to return a statistic information table containing
        the distance between each point in the prediction set and its
        k nearest neighbors in the training set.

        If true, the table will be returned.

        Defaults to True.
    metric : {'manhattan', 'euclidean', 'minkowski', 'chebyshev'}, optional
        Ways to compute the distance between data points.

        Defaults to 'euclidean'.
    minkowski_power : float, optional
        When Minkowski is used for ``metric``, this parameter controls the value
        of power.

        Only valid when ``metric`` is 'minkowski'.

        Defaults to 3.0.
    algorithm : {'brute-force', 'kd-tree'}, optional
        Algorithm used to compute the nearest neighbors.

        Defaults to 'brute-force'.

    Examples
    --------
    Training data:

    >>> df.collect()
       ID      X1      X2  TYPE
    0   0     1.0     1.0     2
    1   1    10.0    10.0     3
    2   2    10.0    11.0     3
    3   3    10.0    10.0     3
    4   4  1000.0  1000.0     1
    5   5  1000.0  1001.0     1
    6   6  1000.0   999.0     1
    7   7   999.0   999.0     1
    8   8   999.0  1000.0     1
    9   9  1000.0  1000.0     1

    Create KNN instance and call fit:

    >>> knn = KNN(n_neighbors=3, voting_type='majority',
    ...           thread_ratio=0.1, stat_info=False)
    >>> knn.fit(df, 'ID', features=['X1', 'X2'], label='TYPE')
    >>> pred_df = connection_context.table("PAL_KNN_CLASSDATA_TBL")

    Call predict:

    >>> res, stat = knn.predict(pred_df, "ID")
    >>> res.collect()
       ID  TYPE
    0   0     3
    1   1     3
    2   2     3
    3   3     1
    4   4     1
    5   5     1
    6   6     1
    7   7     1
    """
    voting_map = {'majority': 0, 'distance-weighted': 1}
    metric_map = {'manhattan': 1, 'euclidean': 2, 'minkowski': 3, 'chebyshev': 4}
    algorithm_map = {'brute-force': 0, 'kd-tree': 1}

    def __init__(self, n_neighbors=None, thread_ratio=None, voting_type=None, stat_info=True, metric=None, minkowski_power=None, algorithm=None):
        setattr(self, 'hanaml_parameters', pal_param_register())
        super(KNN, self).__init__()
        self.n_neighbors = self._arg('n_neighbors', n_neighbors, int)
        self.thread_ratio = self._arg('thread_ratio', thread_ratio, float)
        self.voting_type = self._arg('voting_type', voting_type, self.voting_map)
        self.stat_info = self._arg('stat_info', stat_info, bool)
        self.metric = self._arg('metric', metric, self.metric_map)
        self.minkowski_power = self._arg('minkowski_power', minkowski_power, float)
        if self.metric != 3 and minkowski_power is not None:
            msg = 'Minkowski_power will only be valid if distance metric is Minkowski.'
            logger.error(msg)
            raise ValueError(msg)
        self.algorithm = self._arg('algorithm', algorithm, self.algorithm_map)

    @trace_sql
    def fit(self, data, key, features=None, label=None):
        """
        Fit the model when given training set.

        Parameters
        ----------
        data : DataFrame
            DataFrame containing the data.
        key : str
            Name of the ID column.
        features : list of str, optional
            Names of the feature columns.

            If not provided, it defaults to all the non-ID and non-label columns in ``data``.
        label : str, optional
            Name of the label column.

            If not provided, it defaults to the last column in ``data``.
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        key = self._arg('key', key, str, True)
        features = self._arg('features', features, ListOfStrings)
        label = self._arg('label', label, str)
        col_left = data.columns
        col_left.remove(key)
        if label is None:
            label = col_left[-1]
        col_left.remove(label)
        if features is None:
            features = col_left
        training_data = data[[key] + [label] + features]
        self._training_set = training_data

    @trace_sql
    def predict(self, data, key, features=None):
        """
        Predict the class labels for the provided data

        Parameters
        ----------
        data : DataFrame
            DataFrame containing the data.
        key : str
            Name of the ID column.
        features : list of str, optional
            Names of the feature columns.

            If ``features`` is not provided, it defaults to all
            the non-ID columns.

        Returns
        -------
        DataFrame
            Predicted result, structured as follows:

              - ID column, with same name and type as ``data`` 's ID column.
              - Label column, with same name and type as training data's label
                column.

        DataFrame
            The distance between each point in ``data`` and its k nearest
            neighbors in the training set.
            Only returned if ``stat_info`` is True.
            Structured as follows:

              - TEST\\_ + ``data`` 's ID name, with same type as ``data`` 's ID column,
                query data ID.
              - K, type INTEGER, K number.
              - TRAIN\\_ + training data's ID name, with same type as training
                data's ID column, neighbor point's ID.
              - DISTANCE, type DOUBLE, distance.
        """
        conn = data.connection_context
        if not hasattr(self, '_training_set'):
            raise FitIncompleteError('Model not initialized. Perform a fit first.')
        key = self._arg('key', key, str, True)
        features = self._arg('features', features, ListOfStrings)
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        col_left = data.columns
        col_left.remove(key)
        if features is None:
            features = col_left
        features_train = self._training_set.columns[2:]
        if len(features_train) != len(features):
            msg = 'The number of features must be the same for both training data and ' + 'prediction data.'
            logger.error(msg)
            raise ValueError(msg)
        data_ = data[[key] + features]
        param_array = [('K_NEAREST_NEIGHBOURS', self.n_neighbors, None, None), ('THREAD_RATIO', None, self.thread_ratio, None), ('ATTRIBUTE_NUM', len(features), None, None), ('VOTING_TYPE', self.voting_type, None, None), ('STAT_INFO', self.stat_info, None, None), ('DISTANCE_LEVEL', self.metric, None, None), ('MINKOWSKI_POWER', None, self.minkowski_power, None), ('METHOD', self.algorithm, None, None)]
        result_tbl = '#KNN_PREDICT_RESULT_TBL_{}_{}'.format(self.id, unique_id)
        stat_tbl = '#KNN_PREDICT_STAT_TBL_{}_{}'.format(self.id, unique_id)
        tables = [result_tbl, stat_tbl]
        try:
            self._call_pal_auto(conn, 'PAL_KNN', self._training_set, data_, ParameterTable().with_data(param_array), *tables)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, tables)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, tables)
            raise
        if self.stat_info:
            return (conn.table(result_tbl), conn.table(stat_tbl))
        return conn.table(result_tbl)

    def score(self, data, key, features=None, label=None):
        """
        Return a scalar accuracy value after comparing the predicted
        and original label.

        Parameters
        ----------
        data : DataFrame
            DataFrame containing the data.
        key : str
            Name of the ID column.
        features : list of str, optional
            Names of the feature columns.

            If ``features`` is not provided, it defaults to all
            the non-ID and non-label columns.
        label : str, optional
            Name of the label column.

            If ``label`` is not provided, it defaults to the last column.

        Returns
        -------
        accuracy : float
            Scalar accuracy value after comparing the predicted label and
            original label.
        """
        if not hasattr(self, '_training_set'):
            raise FitIncompleteError('Model not initialized. Perform a fit first.')
        key = self._arg('key', key, str, True)
        features = self._arg('features', features, ListOfStrings)
        label = self._arg('label', label, str)
        cols_left = data.columns
        cols_left.remove(key)
        if label is None:
            label = cols_left[-1]
        cols_left.remove(label)
        if features is None:
            features = cols_left
        if self.stat_info:
            prediction, _ = self.predict(data=data, key=key, features=features)
        else:
            prediction = self.predict(data=data, key=key, features=features)
        prediction = prediction.select(key, 'TARGET').rename_columns(['ID_P', 'PREDICTION'])
        actual = data.select(key, label).rename_columns(['ID_A', 'ACTUAL'])
        joined = actual.join(prediction, 'ID_P=ID_A').select('ACTUAL', 'PREDICTION')
        return metrics.accuracy_score(joined, label_true='ACTUAL', label_pred='PREDICTION')