"""
Implements a T-Net: T-learner for CATE based on a dense NN
"""
from typing import Any, Callable, List, Tuple
import jax.numpy as jnp
import numpy as onp
from jax import grad, jit, random
from jax.example_libraries import optimizers
import catenets.logger as log
from catenets.models.constants import DEFAULT_AVG_OBJECTIVE, DEFAULT_BATCH_SIZE, DEFAULT_LAYERS_OUT, DEFAULT_LAYERS_R, DEFAULT_N_ITER, DEFAULT_N_ITER_MIN, DEFAULT_N_ITER_PRINT, DEFAULT_NONLIN, DEFAULT_PATIENCE, DEFAULT_PENALTY_L2, DEFAULT_SEED, DEFAULT_STEP_SIZE, DEFAULT_UNITS_OUT, DEFAULT_UNITS_R, DEFAULT_VAL_SPLIT, LARGE_VAL
from catenets.models.jax.base import BaseCATENet, OutputHead, train_output_net_only
from catenets.models.jax.model_utils import check_shape_1d_data, heads_l2_penalty, make_val_split

class TNet(BaseCATENet):
    """
    TNet class -- two separate functions learned for each Potential Outcome function

    Parameters
    ----------
    binary_y: bool, default False
        Whether the outcome is binary
    n_layers_out: int
        Number of hypothesis layers (n_layers_out x n_units_out + 1 x Dense layer)
    n_units_out: int
        Number of hidden units in each hypothesis layer
    n_layers_r: int
        Number of representation layers before hypothesis layers (distinction between
        hypothesis layers and representation layers is made to match TARNet & SNets)
    n_units_r: int
        Number of hidden units in each representation layer
    penalty_l2: float
        l2 (ridge) penalty
    step_size: float
        learning rate for optimizer
    n_iter: int
        Maximum number of iterations
    batch_size: int
        Batch size
    val_split_prop: float
        Proportion of samples used for validation split (can be 0)
    early_stopping: bool, default True
        Whether to use early stopping
    patience: int
        Number of iterations to wait before early stopping after decrease in validation loss
    n_iter_min: int
        Minimum number of iterations to go through before starting early stopping
    n_iter_print: int
        Number of iterations after which to print updates
    seed: int
        Seed used
    train_separate: bool, default True
        Whether to train the two output heads completely separately or whether to regularize
        their difference
    penalty_diff: float
        l2-penalty for regularizing the difference between output heads. used only if
        train_separate=False
    nonlin: string, default 'elu'
        Nonlinearity to use in NN
    """

    def __init__(self, binary_y: bool=False, n_layers_out: int=DEFAULT_LAYERS_OUT, n_units_out: int=DEFAULT_UNITS_OUT, n_layers_r: int=DEFAULT_LAYERS_R, n_units_r: int=DEFAULT_UNITS_R, penalty_l2: float=DEFAULT_PENALTY_L2, step_size: float=DEFAULT_STEP_SIZE, n_iter: int=DEFAULT_N_ITER, batch_size: int=DEFAULT_BATCH_SIZE, val_split_prop: float=DEFAULT_VAL_SPLIT, early_stopping: bool=True, patience: int=DEFAULT_PATIENCE, n_iter_min: int=DEFAULT_N_ITER_MIN, n_iter_print: int=DEFAULT_N_ITER_PRINT, seed: int=DEFAULT_SEED, train_separate: bool=True, penalty_diff: float=DEFAULT_PENALTY_L2, nonlin: str=DEFAULT_NONLIN) -> None:
        self.binary_y = binary_y
        self.n_layers_out = n_layers_out
        self.n_units_out = n_units_out
        self.n_layers_r = n_layers_r
        self.n_units_r = n_units_r
        self.penalty_l2 = penalty_l2
        self.step_size = step_size
        self.n_iter = n_iter
        self.batch_size = batch_size
        self.val_split_prop = val_split_prop
        self.early_stopping = early_stopping
        self.patience = patience
        self.n_iter_min = n_iter_min
        self.n_iter_print = n_iter_print
        self.seed = seed
        self.train_separate = train_separate
        self.penalty_diff = penalty_diff
        self.nonlin = nonlin

    def _get_predict_function(self) -> Callable:
        return predict_t_net

    def _get_train_function(self) -> Callable:
        return train_tnet

def train_tnet(X: jnp.ndarray, y: jnp.ndarray, w: jnp.ndarray, binary_y: bool=False, n_layers_out: int=DEFAULT_LAYERS_OUT, n_units_out: int=DEFAULT_UNITS_OUT, n_layers_r: int=DEFAULT_LAYERS_R, n_units_r: int=DEFAULT_UNITS_R, penalty_l2: float=DEFAULT_PENALTY_L2, step_size: float=DEFAULT_STEP_SIZE, n_iter: int=DEFAULT_N_ITER, batch_size: int=DEFAULT_BATCH_SIZE, val_split_prop: float=DEFAULT_VAL_SPLIT, early_stopping: bool=True, patience: int=DEFAULT_PATIENCE, n_iter_min: int=DEFAULT_N_ITER_MIN, n_iter_print: int=DEFAULT_N_ITER_PRINT, seed: int=DEFAULT_SEED, return_val_loss: bool=False, train_separate: bool=True, penalty_diff: float=DEFAULT_PENALTY_L2, nonlin: str=DEFAULT_NONLIN, avg_objective: bool=DEFAULT_AVG_OBJECTIVE) -> Any:
    if len(w.shape) > 1:
        w = w.reshape((len(w),))
    if train_separate:
        log.debug('Training PO_0 Net')
        out_0 = train_output_net_only(X[w == 0], y[w == 0], binary_y=binary_y, n_layers_out=n_layers_out, n_units_out=n_units_out, n_layers_r=n_layers_r, n_units_r=n_units_r, penalty_l2=penalty_l2, step_size=step_size, n_iter=n_iter, batch_size=batch_size, val_split_prop=val_split_prop, early_stopping=early_stopping, patience=patience, n_iter_min=n_iter_min, n_iter_print=n_iter_print, seed=seed, return_val_loss=return_val_loss, nonlin=nonlin, avg_objective=avg_objective)
        log.debug('Training PO_1 Net')
        out_1 = train_output_net_only(X[w == 1], y[w == 1], binary_y=binary_y, n_layers_out=n_layers_out, n_units_out=n_units_out, n_layers_r=n_layers_r, n_units_r=n_units_r, penalty_l2=penalty_l2, step_size=step_size, n_iter=n_iter, batch_size=batch_size, val_split_prop=val_split_prop, early_stopping=early_stopping, patience=patience, n_iter_min=n_iter_min, n_iter_print=n_iter_print, seed=seed, return_val_loss=return_val_loss, nonlin=nonlin, avg_objective=avg_objective)
        if return_val_loss:
            params_0, predict_fun_0, loss_0 = out_0
            params_1, predict_fun_1, loss_1 = out_1
            return ((params_0, params_1), (predict_fun_0, predict_fun_1), loss_1 + loss_0)
        params_0, predict_fun_0 = out_0
        params_1, predict_fun_1 = out_1
    else:
        params, predict_fun = _train_tnet_jointly(X, y, w, binary_y=binary_y, n_layers_out=n_layers_out, n_units_out=n_units_out, n_layers_r=n_layers_r, n_units_r=n_units_r, penalty_l2=penalty_l2, step_size=step_size, n_iter=n_iter, batch_size=batch_size, val_split_prop=val_split_prop, early_stopping=early_stopping, patience=patience, n_iter_min=n_iter_min, n_iter_print=n_iter_print, seed=seed, return_val_loss=return_val_loss, penalty_diff=penalty_diff, nonlin=nonlin)
        params_0, params_1 = (params[0], params[1])
        predict_fun_0, predict_fun_1 = (predict_fun, predict_fun)
    return ((params_0, params_1), (predict_fun_0, predict_fun_1))

def predict_t_net(X: jnp.ndarray, trained_params: dict, predict_funs: list, return_po: bool=False, return_prop: bool=False) -> jnp.ndarray:
    if return_prop:
        raise NotImplementedError('TNet does not implement a propensity model.')
    params_0, params_1 = trained_params
    predict_fun_0, predict_fun_1 = predict_funs
    mu_0 = predict_fun_0(params_0, X)
    mu_1 = predict_fun_1(params_1, X)
    if return_po:
        return (mu_1 - mu_0, mu_0, mu_1)
    else:
        return mu_1 - mu_0

def _train_tnet_jointly(X: jnp.ndarray, y: jnp.ndarray, w: jnp.ndarray, binary_y: bool=False, n_layers_out: int=DEFAULT_LAYERS_OUT, n_units_out: int=DEFAULT_UNITS_OUT, n_layers_r: int=DEFAULT_LAYERS_R, n_units_r: int=DEFAULT_UNITS_R, penalty_l2: float=DEFAULT_PENALTY_L2, step_size: float=DEFAULT_STEP_SIZE, n_iter: int=DEFAULT_N_ITER, batch_size: int=DEFAULT_BATCH_SIZE, val_split_prop: float=DEFAULT_VAL_SPLIT, early_stopping: bool=True, patience: int=DEFAULT_PATIENCE, n_iter_min: int=DEFAULT_N_ITER_MIN, n_iter_print: int=DEFAULT_N_ITER_PRINT, seed: int=DEFAULT_SEED, return_val_loss: bool=False, same_init: bool=True, penalty_diff: float=DEFAULT_PENALTY_L2, nonlin: str=DEFAULT_NONLIN, avg_objective: bool=DEFAULT_AVG_OBJECTIVE) -> jnp.ndarray:
    y, w = (check_shape_1d_data(y), check_shape_1d_data(w))
    d = X.shape[1]
    input_shape = (-1, d)
    rng_key = random.PRNGKey(seed)
    onp.random.seed(seed)
    X, y, w, X_val, y_val, w_val, val_string = make_val_split(X, y, w, val_split_prop=val_split_prop, seed=seed)
    n = X.shape[0]
    init_fun_head, predict_fun_head = OutputHead(n_layers_out=n_layers_out, n_units_out=n_units_out, binary_y=binary_y, n_layers_r=n_layers_r, n_units_r=n_units_r, nonlin=nonlin)
    if not binary_y:

        def loss_head(params: List, batch: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray]) -> jnp.ndarray:
            inputs, targets, weights = batch
            preds = predict_fun_head(params, inputs)
            return jnp.sum(weights * (preds - targets) ** 2)
    else:

        def loss_head(params: List, batch: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray]) -> jnp.ndarray:
            inputs, targets, weights = batch
            preds = predict_fun_head(params, inputs)
            return -jnp.sum(weights * (targets * jnp.log(preds) + (1 - targets) * jnp.log(1 - preds)))

    @jit
    def loss_tnet(params: List, batch: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray], penalty_l2: float, penalty_diff: float) -> jnp.ndarray:
        X, y, w = batch
        loss_0 = loss_head(params[0], (X, y, 1 - w))
        loss_1 = loss_head(params[1], (X, y, w))
        weightsq_head = heads_l2_penalty(params[0], params[1], n_layers_r + n_layers_out, True, penalty_l2, penalty_diff)
        if not avg_objective:
            return loss_0 + loss_1 + 0.5 * weightsq_head
        else:
            n_batch = y.shape[0]
            return (loss_0 + loss_1) / n_batch + 0.5 * weightsq_head
    opt_init, opt_update, get_params = optimizers.adam(step_size=step_size)

    @jit
    def update(i: int, state: dict, batch: jnp.ndarray, penalty_l2: float, penalty_diff: float) -> jnp.ndarray:
        params = get_params(state)
        return opt_update(i, grad(loss_tnet)(params, batch, penalty_l2, penalty_diff), state)
    if same_init:
        _, init_head = init_fun_head(rng_key, input_shape)
        init_params = [init_head, init_head]
    else:
        rng_key, rng_key_2 = random.split(rng_key)
        _, init_head_0 = init_fun_head(rng_key, input_shape)
        _, init_head_1 = init_fun_head(rng_key_2, input_shape)
        init_params = [init_head_0, init_head_1]
    opt_state = opt_init(init_params)
    batch_size = batch_size if batch_size < n else n
    n_batches = int(onp.round(n / batch_size)) if batch_size < n else 1
    train_indices = onp.arange(n)
    l_best = LARGE_VAL
    p_curr = 0
    for i in range(n_iter):
        onp.random.shuffle(train_indices)
        for b in range(n_batches):
            idx_next = train_indices[b * batch_size:min((b + 1) * batch_size, n - 1)]
            next_batch = (X[idx_next, :], y[idx_next, :], w[idx_next])
            opt_state = update(i * n_batches + b, opt_state, next_batch, penalty_l2, penalty_diff)
        if i % n_iter_print == 0 or early_stopping:
            params_curr = get_params(opt_state)
            l_curr = loss_tnet(params_curr, (X_val, y_val, w_val), penalty_l2, penalty_diff)
        if i % n_iter_print == 0:
            log.debug(f'Epoch: {i}, current {val_string} loss {l_curr}')
        if early_stopping and (i + 1) * n_batches > n_iter_min:
            if l_curr < l_best:
                l_best = l_curr
                p_curr = 0
                params_best = params_curr
            else:
                if onp.isnan(l_curr):
                    return (params_best, predict_fun_head)
                p_curr = p_curr + 1
            if p_curr > patience:
                if return_val_loss:
                    l_final = loss_tnet(params_curr, (X_val, y_val, w_val), 0, 0)
                    return (params_curr, predict_fun_head, l_final)
                return (params_curr, predict_fun_head)
    trained_params = get_params(opt_state)
    if return_val_loss:
        l_final = loss_tnet(get_params(opt_state), (X_val, y_val, w_val), 0, 0)
        return (trained_params, predict_fun_head, l_final)
    return (trained_params, predict_fun_head)