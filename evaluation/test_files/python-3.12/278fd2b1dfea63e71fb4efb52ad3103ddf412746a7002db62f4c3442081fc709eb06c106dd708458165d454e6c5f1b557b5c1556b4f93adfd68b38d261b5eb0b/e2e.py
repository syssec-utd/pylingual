from wazy.mlp import NaiveBlock
import haiku as hk
from .mlp import EnsembleBlock
from .seq import SeqpropBlock
from .utils import differentiable_jax_unirep, seq2useq, transform_var, ALPHABET
import jax.numpy as jnp
import jax

def model_reduce(out):
    mu = jnp.mean(out[..., 0], axis=0)
    var = jnp.mean(transform_var(out[..., 1]) + out[..., 0] ** 2, axis=0) - mu ** 2
    epi_var = jnp.std(out[..., 0], axis=0) ** 2
    return (mu, var, epi_var)

def tree_transpose(list_of_trees):
    """Convert a list of trees of identical structure into a single tree of arrays."""
    return jax.tree_util.tree_map(lambda *xs: jnp.array(xs), *list_of_trees)

class EnsembleModel:

    def __init__(self, config):

        def full_model_forward(x, training=True):
            e = EnsembleBlock(config)
            return e(x, training)

        def model_forward(x, training=False):
            x_dim = tuple([1 for i in range(x.ndim)])
            s = jnp.tile(x, (config.model_number, *x_dim))
            mean, var, epi_var = model_reduce(full_model_forward(s, training=training))
            return (mean, var, epi_var)

        def model_uncertainty_eval(x, training=False):
            x_dim = tuple([1 for i in range(x.ndim)])
            s = jnp.tile(x, (config.model_number, *x_dim))
            out = full_model_forward(s, training=training)
            epistemic = jnp.std(out[..., 0], axis=0)
            aleatoric = jnp.mean(jax.nn.softplus(out[..., 1]) + 1e-06, axis=0)
            return (epistemic, aleatoric)

        def seq_forward(x):
            s = seq_only(x)
            if config.pretrained:
                us = seq2useq(s)
                u = differentiable_jax_unirep(us)
            else:
                u = s.flatten()
            mean, var, epi_var = model_forward(u, training=False)
            return (mean, var)

        def seq_only(x):
            s = SeqpropBlock()(x)
            return s
        self.infer_t = hk.transform(model_forward)
        self.train_t = hk.transform(full_model_forward)
        self.seq_t = hk.transform(seq_forward)
        self.var_t = hk.transform(model_uncertainty_eval)
        self.seq_only_t = hk.transform(seq_only)

    def seq_apply(self, params, key, x):
        """Apply the seqprop model by merging the sequence and trainable parameters"""
        mp = hk.data_structures.merge(params, x[1])
        return self.seq_t.apply(mp, key, x[0])

    def seq_only_apply(self, params, key, x):
        """Apply the seqprop model by merging the sequence and trainable parameters. Only returns sequence"""
        mp = hk.data_structures.merge(params, x[1])
        return self.seq_only_t.apply(mp, key, x[0])

    def seq_partition(self, params):
        """Extract the seqprop parameters from the parameters"""
        return hk.data_structures.partition(lambda m, *_: 'seqprop' in m, params)[0]

    def random_seqs(self, key, batch_size, params, length, start_seq=None):
        """Generate a batch of tuples of sequences and seqprop r,b parameters

        The params should contain the seqprop block. All others will be ignored.
        """
        if start_seq is None:
            start_seq = jnp.zeros((length, len(ALPHABET)), dtype=jnp.float32)
        start_seq = jnp.pad(start_seq[None], ((0, batch_size - 1), (0, 0), (0, 0)))
        sp = self.seq_partition(params)
        return (0.1 * (start_seq + jax.random.normal(key, shape=(batch_size, length, len(ALPHABET)))), tree_transpose([jax.tree_util.tree_map(lambda x: x, sp) for _ in range(batch_size)]))

def build_naive_e2e():

    def naive_model_forward(x):
        e = NaiveBlock()
        return e(x)

    def seq_forward(x):
        s = SeqpropBlock()(x)
        us = seq2useq(s)
        u = differentiable_jax_unirep(us)
        out = naive_model_forward(u)
        return out
    naive_model_forward_t = hk.transform(naive_model_forward)
    naive_seq_t = hk.transform(seq_forward)
    return (naive_model_forward_t, naive_seq_t)