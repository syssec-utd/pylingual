from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import xgboost as xgb
from matplotlib.figure import Figure
from slickml.regression._xgboost import XGBoostRegressor
from slickml.utils import Colors, check_var
from slickml.visualization import plot_xgb_cv_results

@dataclass
class XGBoostCVRegressor(XGBoostRegressor):
    """XGBoost CV Regressor.

    This is wrapper using ``XGBoostRegressor`` to train a XGBoost [xgboost-api]_ model with using the optimum
    number of boosting rounds from the inputs. It used ``xgboost.cv()`` model with n-folds
    cross-validation and train model based on the best number of boosting round to avoid over-fitting.

    Parameters
    ----------
    num_boost_round : int, optional
        Number of boosting rounds to fit a model, by default 200

    n_splits : int, optional
        Number of folds for cross-validation, by default 4

    metrics : str, optional
        Metrics to be tracked at cross-validation fitting time with possible values of ``"rmse"``,
        ``"rmsle"``, ``"mae"``. Note this is different than `eval_metric` that needs to be passed to
        `params` dict, by default "rmse"

    early_stopping_rounds : int, optional
        The criterion to early abort the ``xgboost.cv()`` phase if the test metric is not improved,
        by default 20

    random_state : int, optional
        Random seed number, by default 1367

    shuffle : bool, optional
        Whether to shuffle data to have the ability of building stratified folds in ``xgboost.cv()``,
        by default True

    sparse_matrix : bool, optional
        Whether to convert the input features to sparse matrix with csr format or not. This would
        increase the speed of feature selection for relatively large/sparse datasets. Consequently,
        this would actually act like an un-optimize solution for dense feature matrix. Additionally,
        this feature cannot be used along with ``scale_mean=True`` standardizing the feature matrix
        to have a mean value of zeros would turn the feature matrix into a dense matrix. Therefore,
        by default our API banned this feature, by default False

    scale_mean : bool, optional
        Whether to standarize the feauture matrix to have a mean value of zero per feature (center
        the features before scaling). As laid out in ``sparse_matrix``, ``scale_mean=False`` when
        using ``sparse_matrix=True``, since centering the feature matrix would decrease the sparsity
        and in practice it does not make any sense to use sparse matrix method and it would make
        it worse. The ``StandardScaler`` object can be accessed via ``cls.scaler_`` if ``scale_mean`` or
        ``scale_strd`` is used unless it is ``None``, by default False

    scale_std : bool, optional
        Whether to scale the feauture matrix to have unit variance (or equivalently, unit standard
        deviation) per feature. The ``StandardScaler`` object can be accessed via ``cls.scaler_``
        if ``scale_mean`` or ``scale_strd`` is used unless it is ``None``, by default False

    importance_type : str, optional
        Importance type of ``xgboost.train()`` with possible values ``"weight"``, ``"gain"``,
        ``"total_gain"``, ``"cover"``, ``"total_cover"``, by default "total_gain"

    params : Dict[str, Union[str, float, int]], optional
        Set of parameters required for fitting a Booster, by default {"eval_metric": "rmse",
        "tree_method": "hist", "objective": "reg:squarederror", "learning_rate": 0.05,
        "max_depth": 2, "min_child_weight": 1, "gamma": 0.0, "reg_alpha": 0.0, "reg_lambda": 1.0,
        "subsample": 0.9, "max_delta_step": 1, "verbosity": 0, "nthread": 4}
        Other options for objective: ``"reg:logistic"``, ``"reg:squaredlogerror"``

    verbose : bool, optional
        Whether to log the final results of ``xgboost.cv()``, by default True

    callbacks : bool, optional
        Whether to logging standard deviation of metrics on train data and track the early stopping
        criterion, by default False

    Methods
    -------
    fit(X_train, y_train)
        Fits a ``XGBoost.Booster`` to input training data. Proper ``dtrain_`` matrix based on chosen
        options i.e. ``sparse_matrix``, ``scale_mean``, ``scale_std`` is being created based on the
        passed ``X_train`` and ``y_train``

    predict(X_test, y_test)
        Returns prediction target values

    get_cv_results()
        Returns the mean value of the metrics in ``n_splits`` cross-validation for each boosting round

    get_params()
        Returns final set of train parameters. The default set of parameters will be updated with
        the new ones that passed to ``params``

    get_default_params()
        Returns the default set of train parameters. The default set of parameters will be used when
        ``params=None``

    get_feature_importance()
        Returns the feature importance of the trained booster based on the given ``importance_type``

    get_shap_explainer()
        Returns the ``shap.TreeExplainer``

    plot_cv_results()
        Visualizes cross-validation results

    plot_shap_summary()
        Visualizes Shapley values summary plot

    plot_shap_waterfall()
        Visualizes Shapley values waterfall plot

    Attributes
    ----------
    cv_results_ : pd.DataFrame
        The mean value of the metrics in ``n_splits`` cross-validation for each boosting round

    feature_importance_ : pd.DataFrame
        Features importance based on the given ``importance_type``

    scaler_ : StandardScaler, optional
        Standardization object when ``scale_mean=True`` or ``scale_std=True`` unless it is ``None``

    X_train_ : pd.DataFrame
        Fitted and Transformed features when ``scale_mean=True`` or ``scale_std=True``. In other case, it will
        be the same as the passed ``X_train`` features

    X_test_ : pd.DataFrame
        Transformed features when ``scale_mean=True`` or ``scale_std=True`` using `clf.scaler_` that
        has be fitted on ``X_train`` and ``y_train`` data. In other case, it will be the same as the
        passed ``X_train`` features

    dtrain_ : xgb.DMatrix
        Training data matrix via ``xgboost.DMatrix(clf.X_train_, clf.y_train)``

    dtest_ : xgb.DMatrix
        Testing data matrix via ``xgboost.DMatrix(clf.X_test_, clf.y_test)`` or
        ``xgboost.DMatrix(clf.X_test_, None)`` when ``y_test`` is not available in inference

    shap_values_train_ : np.ndarray
        Shapley values from ``TreeExplainer`` using ``X_train_``

    shap_values_test_ : np.ndarray
        Shapley values from ``TreeExplainer`` using ``X_test_``

    shap_explainer_ : shap.TreeExplainer
        Shap TreeExplainer object

    model_ : xgboost.Booster
        XGBoost Booster object

    See Also
    --------
    :class:`slickml.regression.XGBoostRegressor`

    References
    ----------
    .. [callback-api] https://xgboost.readthedocs.io/en/latest/python/python_api.html#callback-api
    .. [linestyles-api] https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
    """
    num_boost_round: Optional[int] = 200
    n_splits: Optional[int] = 4
    metrics: Optional[str] = 'rmse'
    early_stopping_rounds: Optional[int] = 20
    random_state: Optional[int] = 1367
    shuffle: Optional[bool] = True
    sparse_matrix: Optional[bool] = False
    scale_mean: Optional[bool] = False
    scale_std: Optional[bool] = False
    importance_type: Optional[str] = 'total_gain'
    params: Optional[Dict] = None
    verbose: Optional[bool] = True
    callbacks: Optional[bool] = False

    def __post_init__(self) -> None:
        super().__post_init__()
        check_var(self.n_splits, var_name='n_splits', dtypes=int)
        check_var(self.metrics, var_name='metrics', dtypes=str, values=('rmse', 'rmsle', 'mae'))
        check_var(self.early_stopping_rounds, var_name='early_stopping_rounds', dtypes=int)
        check_var(self.random_state, var_name='random_state', dtypes=int)
        check_var(self.shuffle, var_name='shuffle', dtypes=bool)
        check_var(self.verbose, var_name='verbose', dtypes=bool)
        check_var(self.callbacks, var_name='callbacks', dtypes=bool)
        self._callbacks()

    def fit(self, X_train: Union[pd.DataFrame, np.ndarray], y_train: Union[List[float], np.ndarray, pd.Series]) -> None:
        """Fits a ``XGBoost.Booster`` to input training data based on the best number of boostring round.

        Parameters
        ----------
        X_train : Union[pd.DataFrame, np.ndarray]
            Input data for training (features)

        y_train : Union[List[float], np.ndarray, pd.Series]
            Input ground truth for training (targets)

        See Also
        --------
        :meth:`xgboost.cv()`
        :meth:`xgboost.train()`

        Returns
        -------
        None
        """
        self.dtrain_ = self._dtrain(X_train=X_train, y_train=y_train)
        self.cv_results_ = self._cv()
        if self.verbose:
            self._verbose_log()
        self.model_ = self._model()
        self.feature_importance_ = self._imp_to_df()
        return None

    def get_cv_results(self) -> pd.DataFrame:
        """Returns cross-validiation results.

        Returns
        -------
        pd.DataFrame
        """
        return self.cv_results_

    def plot_cv_results(self, figsize: Optional[Tuple[Union[int, float], Union[int, float]]]=(8, 5), linestyle: Optional[str]='--', train_label: Optional[str]='Train', test_label: Optional[str]='Test', train_color: Optional[str]='navy', train_std_color: Optional[str]='#B3C3F3', test_color: Optional[str]='purple', test_std_color: Optional[str]='#D0AAF3', save_path: Optional[str]=None, display_plot: Optional[bool]=False, return_fig: Optional[bool]=False) -> Optional[Figure]:
        """Visualizes the cross-validation results and evolution of metrics through number of boosting rounds.

        Parameters
        ----------
        cv_results : pd.DataFrame
            Cross-validation results

        figsize : Tuple[Union[int, float], Union[int, float]], optional
            Figure size, by default (8, 5)

        linestyle : str, optional
            Style of lines [linestyles-api]_, by default "--"

        train_label : str, optional
            Label in the figure legend for the train line, by default "Train"

        test_label : str, optional
            Label in the figure legend for the test line, by default "Test"

        train_color : str, optional
            Color of the training line, by default "navy"

        train_std_color : str, optional
            Color of the edge color of the training std bars, by default "#B3C3F3"

        test_color : str, optional
            Color of the testing line, by default "purple"

        test_std_color : str, optional
            Color of the edge color of the testing std bars, by default "#D0AAF3"

        save_path : str, optional
            The full or relative path to save the plot including the image format such as
            "myplot.png" or "../../myplot.pdf", by default None

        display_plot : bool, optional
            Whether to show the plot, by default False

        return_fig : bool, optional
            Whether to return figure object, by default False

        Returns
        -------
        Figure, optional
        """
        return plot_xgb_cv_results(cv_results=self.cv_results_, figsize=figsize, linestyle=linestyle, train_label=train_label, test_label=test_label, train_color=train_color, train_std_color=train_std_color, test_color=test_color, test_std_color=test_std_color, save_path=save_path, display_plot=display_plot, return_fig=return_fig)

    def _cv(self) -> pd.DataFrame:
        """Returns the XGBoost cv_results based on the best number of boosting rounds.

        Returns
        -------
        pd.DataFrame
        """
        return xgb.cv(params=self.params, dtrain=self.dtrain_, num_boost_round=self.num_boost_round, nfold=self.n_splits, metrics=self.metrics, early_stopping_rounds=self.early_stopping_rounds, seed=self.random_state, shuffle=self.shuffle, callbacks=self.callbacks, as_pandas=True)

    def _model(self) -> xgb.Booster:
        """Fits a ``XGBoost.Booster`` based on the best number of boosting round on ``dtrain_`` matrix.

        Returns
        -------
        xgb.Booster
        """
        return xgb.train(params=self.params, dtrain=self.dtrain_, num_boost_round=len(self.cv_results_) - 1)

    def _callbacks(self) -> None:
        """Returns a list of callbacks.

        The implemented callbacks are including ``xgboost.callback.EvaluationMonitor`` and
        ``xgboost.callback.EarlyStopping`` [callback-api]_.

        Returns
        -------
        None
        """
        if self.callbacks:
            self.callbacks = [xgb.callback.EvaluationMonitor(rank=0, period=1, show_stdv=True), xgb.callback.EarlyStopping(rounds=self.early_stopping_rounds)]
        else:
            self.callbacks = None
        return None

    def _verbose_log(self) -> None:
        """Logs n-folds cross-validation results.

        Returns
        -------
        None
        """
        print(str(Colors.BOLD) + '*-* ' + str(Colors.GREEN) + f'Best Boosting Round = {len(self.cv_results_) - 1}' + str(Colors.END) + str(Colors.BOLD) + ' -*- ' + str(Colors.F_Red) + f'{self.n_splits}-Folds CV {self.metrics.upper()}: ' + str(Colors.END) + str(Colors.BOLD) + str(Colors.B_Blue) + f'Train = {self.cv_results_.iloc[-1][0]:.3f}' + ' +/- ' + f'{self.cv_results_.iloc[-1][1]:.3f}' + str(Colors.END) + str(Colors.BOLD) + ' -*- ' + str(Colors.B_Magenta) + f'Test = {self.cv_results_.iloc[-1][2]:.3f}' + ' +/- ' + f'{self.cv_results_.iloc[-1][3]:.3f}' + str(Colors.END) + str(Colors.BOLD) + ' *-*')