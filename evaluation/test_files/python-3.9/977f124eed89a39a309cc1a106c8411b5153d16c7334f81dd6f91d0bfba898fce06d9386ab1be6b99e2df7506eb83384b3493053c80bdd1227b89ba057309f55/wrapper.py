"""
モデル作成時に用いるクラスなどの定義
"""
from typing import Union
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator, clone
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.utils.validation import check_is_fitted
from ..utils import get_logger
logger = get_logger(__name__)
scaler = {True: StandardScaler, 'standard': StandardScaler, 'minmax': MinMaxScaler}

def get_scalar_by_name(name: Union[None, str]) -> Union[None, StandardScaler]:
    if name is None:
        return None
    try:
        return scaler.get(name, None)()
    except TypeError:
        raise ValueError('{} is not defined. must be {}'.format(name, ','.join(map(str, scaler.keys()))))

class UtilityTransform(TransformerMixin, BaseEstimator):
    """
    sklearn transformer にログスケール変換の処理を追加した transformer
    """

    def __init__(self, log: bool=False, scaling: Union[None, str]=None):
        super(UtilityTransform, self).__init__()
        self.log = log
        self.scaling = scaling
        self.threshold = 1e-10

    def fit(self, X, y=None):
        self.scalar_ = get_scalar_by_name(self.scaling)
        if self.scaling is not None and self.scalar_ is None:
            raise ValueError('{} is not a valid scaling name. Must be one of the following name '.format(self.scaling) + ', '.join(map(str, scaler.keys())))
        if self.log and np.sum(X < 0) > 0:
            raise ValueError('In Log-scalar, you must input value over zero')
        self.is_one_dim_ = len(X.shape) == 1
        if self.log:
            X = np.log1p(X + self.threshold)
        if self.scalar_ is not None:
            logger.debug('fit scaling {}'.format(self.scalar_))
            if self.is_one_dim_:
                X = X.reshape(-1, 1)
            self.scalar_ = self.scalar_.fit(X, y=y)
        return self

    def transform(self, X):
        check_is_fitted(self, 'is_one_dim_')
        if self.scalar_:
            check_is_fitted(self.scalar_)
        if self.log:
            X = np.log1p(X + self.threshold)
        if self.scalar_:
            if self.is_one_dim_:
                X = X.reshape(-1, 1)
            X = self.scalar_.transform(X)
            if self.is_one_dim_:
                X = X.reshape(-1)
        return X

    def inverse_transform(self, X):
        check_is_fitted(self, 'is_one_dim_')
        if self.scalar_:
            if self.is_one_dim_:
                X = X.reshape(-1, 1)
            X = self.scalar_.inverse_transform(X)
            if self.is_one_dim_:
                X = X.reshape(-1)
        if self.log:
            X = np.expm1(X) - self.threshold
        return X

class PrePostProcessModel(BaseEstimator):
    """Custom Scikit-Learn Estimator

    [note] this class should be replaced by pileline class. (future work)
    """

    def __init__(self, instance: BaseEstimator, input_scaling=None, input_logscale=False, target_scaling=None, target_logscale=False):
        """


        Args:
            instance:
                main model instance.
            input_scaling:
                scaling name apply to feature `X` before input to instance
            input_logscale:
                set True, feature `X` convert to logscale
            target_scaling:
                scaling name apply to target `y` before instance
            target_logscale:
                set True, target `y` convert to logscale
        """
        self.input_scaling = input_logscale
        self.input_logscale = input_logscale
        self.target_scaling = target_logscale
        self.target_logscale = target_logscale
        self.input_transformer = UtilityTransform(input_logscale, input_scaling)
        self.target_transformer = UtilityTransform(target_logscale, target_scaling)
        self.instance = instance
        super(PrePostProcessModel, self).__init__()

    def fit(self, x_train, y_train, **kwargs):
        clf = clone(self.instance)
        (x, y) = self._before_fit(x_train, y_train)
        self.fitted_model_ = clf.fit(x, y=y, **kwargs)
        return self

    def predict(self, x, prob=False):
        check_is_fitted(self, 'fitted_model_')
        x = self._before_predict(x)
        if prob:
            try:
                pred = self.fitted_model_.predict_proba(x)
            except AttributeError as e:
                logger.warning(e)
                pred = self.fitted_model_.predict(x)
        else:
            pred = self.fitted_model_.predict(x)
        pred = self.target_transformer.inverse_transform(pred)
        return pred

    def get_params(self, deep=True):
        params = super(PrePostProcessModel, self).get_params(deep=False)
        if not deep:
            return params
        params.update({'instance': {'class': str(type(self.instance)), 'params': self.instance.get_params(deep=True)}, 'input_transformer': self.input_transformer.get_params(deep=True), 'target_transformer': self.target_transformer.get_params(deep=True)})
        return params

    def _before_fit(self, x_train, y_train):
        x = self.input_transformer.fit_transform(x_train)
        y = self.target_transformer.fit_transform(y_train)
        return (x, y)

    def _before_predict(self, x):
        """
        予測モデルに投入する前の前処理を行う

        Args:
            x: 変換前の特長

        Returns:
            変換後の特徴.
        """
        return self.input_transformer.transform(x)