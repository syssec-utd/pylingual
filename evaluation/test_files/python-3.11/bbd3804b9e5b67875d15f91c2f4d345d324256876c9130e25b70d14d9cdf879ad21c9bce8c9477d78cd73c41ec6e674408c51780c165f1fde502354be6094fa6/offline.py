import warnings
import numpy as np
import jax.numpy as jnp
from jax.lax import while_loop
import brainpy.math as bm
from brainpy._src.math.object_transform.base import BrainPyObject
from brainpy.types import ArrayType
from .utils import Sigmoid, Regularization, L1Regularization, L1L2Regularization, L2Regularization, polynomial_features, normalize
__all__ = ['OfflineAlgorithm', 'LinearRegression', 'linear_regression', 'RidgeRegression', 'ridge_regression', 'LassoRegression', 'LogisticRegression', 'PolynomialRegression', 'PolynomialRidgeRegression', 'ElasticNetRegression', 'get_supported_offline_methods', 'register_offline_method']
name2func = dict()

class OfflineAlgorithm(BrainPyObject):
    """Base class for offline training algorithm."""

    def __init__(self, name=None):
        super(OfflineAlgorithm, self).__init__(name=name)

    def __call__(self, targets, inputs, outputs=None):
        """The training procedure.

    Parameters
    ----------
    targets: ArrayType
      The 2d target data with the shape of `(num_batch, num_output)`.
    inputs: ArrayType
      The 2d input data with the shape of `(num_batch, num_input)`.
    outputs: ArrayType
      The 2d output data with the shape of `(num_batch, num_output)`.

    Returns
    -------
    weight: ArrayType
      The weights after fit.
    """
        return self.call(targets, inputs, outputs)

    def call(self, targets, inputs, outputs=None) -> ArrayType:
        """The training procedure.

    Parameters
    ----------
    inputs: ArrayType
      The 3d input data with the shape of `(num_batch, num_time, num_input)`,
      or, the 2d input data with the shape of `(num_time, num_input)`.

    targets: ArrayType
      The 3d target data with the shape of `(num_batch, num_time, num_output)`,
      or the 2d target data with the shape of `(num_time, num_output)`.

    outputs: ArrayType
      The 3d output data with the shape of `(num_batch, num_time, num_output)`,
      or the 2d output data with the shape of `(num_time, num_output)`.

    Returns
    -------
    weight: ArrayType
      The weights after fit.
    """
        raise NotImplementedError('Must implement the __call__ function by the subclass itself.')

    def __repr__(self):
        return self.__class__.__name__

def _check_data_2d_atls(x):
    if x.ndim < 2:
        raise ValueError(f'Data must be a 2d tensor. But we got {x.ndim}d: {x.shape}.')
    if x.ndim != 2:
        return bm.flatten(x, end_dim=-2)
    else:
        return x

class RegressionAlgorithm(OfflineAlgorithm):
    """ Base regression model. Models the relationship between a scalar dependent variable y and the independent
  variables X.

  Parameters
  ----------
  max_iter: int
    The number of training iterations the algorithm will tune the weights for.
  learning_rate: float
    The step length that will be used when updating the weights.
  """

    def __init__(self, max_iter: int=None, learning_rate: float=None, regularizer: Regularization=None, name: str=None):
        super(RegressionAlgorithm, self).__init__(name=name)
        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.regularizer = regularizer

    def initialize(self, *args, **kwargs):
        pass

    def init_weights(self, n_features, n_out):
        """ Initialize weights randomly [-1/N, 1/N] """
        limit = 1 / np.sqrt(n_features)
        return bm.random.uniform(-limit, limit, (n_features, n_out))

    def gradient_descent_solve(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        w = self.init_weights(inputs.shape[1], targets.shape[1])

        def cond_fun(a):
            i, par_old, par_new = a
            return jnp.logical_and(jnp.logical_not(jnp.allclose(par_old, par_new)), i < self.max_iter).value

        def body_fun(a):
            i, _, par_new = a
            y_pred = inputs.dot(par_new)
            grad_w = jnp.dot(inputs.T, -(targets - y_pred)) + self.regularizer.grad(par_new)
            par_new2 = par_new - self.learning_rate * grad_w
            return (i + 1, par_new, par_new2)
        r = while_loop(cond_fun, body_fun, (0, w - 1e-08, w))
        return r[-1]

    def predict(self, W, X):
        return jnp.dot(X, W)

class LinearRegression(RegressionAlgorithm):
    """Training algorithm of least-square regression.

  Parameters
  ----------
  name: str
    The name of the algorithm.
  """

    def __init__(self, name: str=None, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=False):
        super(LinearRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate, regularizer=Regularization(0.0))
        self.gradient_descent = gradient_descent

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        if self.gradient_descent:
            return self.gradient_descent_solve(targets, inputs)
        else:
            weights = jnp.linalg.lstsq(inputs, targets)
            return weights[0]
linear_regression = LinearRegression()
name2func['linear'] = LinearRegression
name2func['lstsq'] = LinearRegression

class RidgeRegression(RegressionAlgorithm):
    """Training algorithm of ridge regression.

  Parameters
  ----------
  alpha: float
    The regularization coefficient.

    .. versionadded:: 2.2.0

  beta: float
    The regularization coefficient.

    .. deprecated:: 2.2.0
       Please use `alpha` to set regularization factor.

  name: str
    The name of the algorithm.
  """

    def __init__(self, alpha: float=1e-07, beta: float=None, name: str=None, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=False):
        if beta is not None:
            warnings.warn(f"Please use 'alpha' to set regularization factor. 'beta' has been deprecated since version 2.2.0.", UserWarning)
            alpha = beta
        super(RidgeRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate, regularizer=L2Regularization(alpha=alpha))
        self.gradient_descent = gradient_descent

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        if self.gradient_descent:
            return self.gradient_descent_solve(targets, inputs)
        else:
            temp = inputs.T @ inputs
            if self.regularizer.alpha > 0.0:
                temp += self.regularizer.alpha * jnp.eye(inputs.shape[-1])
            weights = jnp.linalg.pinv(temp) @ (inputs.T @ targets)
            return weights

    def __repr__(self):
        return f'{self.__class__.__name__}(beta={self.regularizer.alpha})'
ridge_regression = RidgeRegression()
name2func['ridge'] = RidgeRegression

class LassoRegression(RegressionAlgorithm):
    """Lasso regression method for offline training.

  Parameters
  ----------
  alpha: float
    Constant that multiplies the L1 term. Defaults to 1.0.
    `alpha = 0` is equivalent to an ordinary least square.
  max_iter: int
    The maximum number of iterations.
  degree: int
    The degree of the polynomial that the independent variable X will be transformed to.
  name: str
    The name of the algorithm.
  """

    def __init__(self, alpha: float=1.0, degree: int=2, add_bias: bool=False, name: str=None, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=True):
        super(LassoRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate, regularizer=L1Regularization(alpha=alpha))
        self.gradient_descent = gradient_descent
        self.add_bias = add_bias
        assert gradient_descent
        self.degree = degree

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        inputs = normalize(polynomial_features(inputs, degree=self.degree, add_bias=self.add_bias))
        return super(LassoRegression, self).gradient_descent_solve(targets, inputs)

    def predict(self, W, X):
        X = _check_data_2d_atls(bm.as_jax(X))
        X = normalize(polynomial_features(X, degree=self.degree, add_bias=self.add_bias))
        return super(LassoRegression, self).predict(W, X)
name2func['lasso'] = LassoRegression

class LogisticRegression(RegressionAlgorithm):
    """Logistic regression method for offline training.

  Parameters
  ----------
  learning_rate: float
      The step length that will be taken when following the negative gradient during
      training.
  gradient_descent: boolean
    True or false depending on if gradient descent should be used when training. If
    false then we use batch optimization by least squares.
  max_iter: int
    The number of iteration to optimize the parameters.
  name: str
    The name of the algorithm.
  """

    def __init__(self, learning_rate: float=0.1, gradient_descent: bool=True, max_iter: int=4000, name: str=None):
        super(LogisticRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate)
        self.gradient_descent = gradient_descent
        self.sigmoid = Sigmoid()

    def call(self, targets, inputs, outputs=None) -> ArrayType:
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        if targets.shape[-1] != 1:
            raise ValueError(f'Target must be a scalar, but got multiple variables: {targets.shape}. ')
        targets = targets.flatten()
        param = self.init_weights(inputs.shape[1], targets.shape[1])

        def cond_fun(a):
            i, par_old, par_new = a
            return jnp.logical_and(jnp.logical_not(jnp.allclose(par_old, par_new)), i < self.max_iter).value

        def body_fun(a):
            i, par_old, par_new = a
            y_pred = self.sigmoid(inputs.dot(par_new))
            if self.gradient_descent:
                par_new2 = par_new - self.learning_rate * (y_pred - targets).dot(inputs)
            else:
                gradient = self.sigmoid.grad(inputs.dot(par_new))
                diag_grad = bm.zeros((gradient.size, gradient.size))
                diag = bm.arange(gradient.size)
                diag_grad[diag, diag] = gradient
                par_new2 = jnp.linalg.pinv(inputs.T.dot(diag_grad).dot(inputs)).dot(inputs.T).dot(diag_grad.dot(inputs).dot(par_new) + targets - y_pred)
            return (i + 1, par_new, par_new2)
        r = while_loop(cond_fun, body_fun, (0, param + 1.0, param))
        return r[-1]

    def predict(self, W, X):
        return self.sigmoid(X @ W)
name2func['logistic'] = LogisticRegression

class PolynomialRegression(LinearRegression):

    def __init__(self, degree: int=2, name: str=None, add_bias: bool=False, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=True):
        super(PolynomialRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate, gradient_descent=gradient_descent)
        self.degree = degree
        self.add_bias = add_bias

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        inputs = polynomial_features(inputs, degree=self.degree, add_bias=self.add_bias)
        return super(PolynomialRegression, self).call(targets, inputs)

    def predict(self, W, X):
        X = _check_data_2d_atls(bm.as_jax(X))
        X = polynomial_features(X, degree=self.degree, add_bias=self.add_bias)
        return super(PolynomialRegression, self).predict(W, X)
name2func['polynomial'] = PolynomialRegression

class PolynomialRidgeRegression(RidgeRegression):

    def __init__(self, alpha: float=1.0, degree: int=2, name: str=None, add_bias: bool=False, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=True):
        super(PolynomialRidgeRegression, self).__init__(alpha=alpha, name=name, max_iter=max_iter, learning_rate=learning_rate, gradient_descent=gradient_descent)
        self.degree = degree
        self.add_bias = add_bias

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        inputs = polynomial_features(inputs, degree=self.degree, add_bias=self.add_bias)
        return super(PolynomialRidgeRegression, self).call(targets, inputs)

    def predict(self, W, X):
        X = _check_data_2d_atls(bm.as_jax(X))
        X = polynomial_features(X, degree=self.degree, add_bias=self.add_bias)
        return super(PolynomialRidgeRegression, self).predict(W, X)
name2func['polynomial_ridge'] = PolynomialRidgeRegression

class ElasticNetRegression(RegressionAlgorithm):
    """

  Parameters:
  -----------
  degree: int
      The degree of the polynomial that the independent variable X will be transformed to.
  reg_factor: float
      The factor that will determine the amount of regularization and feature
      shrinkage.
  l1_ration: float
      Weighs the contribution of l1 and l2 regularization.
  n_iterations: float
      The number of training iterations the algorithm will tune the weights for.
  learning_rate: float
      The step length that will be used when updating the weights.
  """

    def __init__(self, alpha: float=1.0, degree: int=2, l1_ratio: float=0.5, name: str=None, add_bias: bool=False, max_iter: int=1000, learning_rate: float=0.001, gradient_descent: bool=True):
        super(ElasticNetRegression, self).__init__(name=name, max_iter=max_iter, learning_rate=learning_rate, regularizer=L1L2Regularization(alpha=alpha, l1_ratio=l1_ratio))
        self.degree = degree
        self.add_bias = add_bias
        self.gradient_descent = gradient_descent
        assert gradient_descent

    def call(self, targets, inputs, outputs=None):
        inputs = _check_data_2d_atls(bm.as_jax(inputs))
        targets = _check_data_2d_atls(bm.as_jax(targets))
        inputs = normalize(polynomial_features(inputs, degree=self.degree))
        return super(ElasticNetRegression, self).gradient_descent_solve(targets, inputs)

    def predict(self, W, X):
        X = _check_data_2d_atls(bm.as_jax(X))
        X = normalize(polynomial_features(X, degree=self.degree, add_bias=self.add_bias))
        return super(ElasticNetRegression, self).predict(W, X)
name2func['elastic_net'] = ElasticNetRegression

def get_supported_offline_methods():
    """Get all supported offline training methods."""
    return tuple(name2func.keys())

def register_offline_method(name: str, method: OfflineAlgorithm):
    """Register a new offline learning method.

  Parameters
  ----------
  name: str
    The method name.
  method: OfflineAlgorithm
    The function method.
  """
    if name in name2func:
        raise ValueError(f'"{name}" has been registered in offline training methods.')
    if not isinstance(method, OfflineAlgorithm):
        raise ValueError(f'"method" must be an instance {OfflineAlgorithm.__name__}, but we got {type(method)}')
    name2func[name] = method

def get(name: str) -> OfflineAlgorithm:
    """Get the training function according to the training method name."""
    if name not in name2func:
        raise ValueError(f'All offline methods are: {get_supported_offline_methods()}.\nBut we got {name}.')
    return name2func[name]