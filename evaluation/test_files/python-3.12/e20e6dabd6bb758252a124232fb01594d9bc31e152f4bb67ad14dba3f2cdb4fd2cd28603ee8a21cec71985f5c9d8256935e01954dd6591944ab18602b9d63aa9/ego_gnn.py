from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
'EgoGraph based GNN model.'
try:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()
except ImportError:
    import tensorflow as tf
from graphlearn.python.nn.tf.config import conf
from graphlearn.python.nn.tf.module import Module

class EgoGNN(Module):
    """ Represents `EgoGraph` based GNN models.

  Args:
    layers: A list, each element is an `EgoLayer`.
    bn_func: Batch normalization function for hidden layers' output. Default is
      None, which means batch normalization will not be performed.
    act_func: Activation function for hidden layers' output. 
      Default is tf.nn.relu.
    dropout: Dropout rate for hidden layers' output. Default is 0.0, which
      means dropout will not be performed. The optional value is a float.
  """

    def __init__(self, layers, bn_func=None, act_func=tf.nn.relu, dropout=0.0, **kwargs):
        super(EgoGNN, self).__init__()
        self.layers = layers
        self.bn_func = bn_func
        self.active_func = act_func
        self.dropout = dropout

    def forward(self, graph):
        """ Update node embeddings through the given ego layers.

    h^{i} is a list, 0 <= i <= n, where n is len(layers).
    h^{i} = [ h_{0}^{i}, h_{1}^{i}, h_{2}^{i}, ... , h_{n - i}^{i} ]

    For 3 layers, we need nodes and 3-hop neighbors in the graph object.
      h^{0} = [ h_{0}^{0}, h_{1}^{0}, h_{2}^{0}, h_{3}^{0} ]
      h^{1} = [ h_{0}^{1}, h_{1}^{1}, h_{2}^{1} ]
      h^{2} = [ h_{0}^{2}, h_{1}^{2} ]
      h^{3} = [ h_{0}^{3} ]

    For initialization,
      h_{0}^{0} = graph.src
      h_{1}^{0} = graph.hop_node{1}
      h_{2}^{0} = graph.hop_node{2}
      h_{3}^{0} = graph.hop_node{3}

    Then we apply h^{i} = layer_{i}(h^{i-1}), and h_{0}^{3} is the final returned value.

    Args:
      graph: an `EgoGraph` object.

    Return:
      A tensor with shape [batch_size, output_dim], where `output_dim` is the
      same with layers[-1].
    """
        graph = graph.transform()
        h = [graph.src]
        for i in range(len(self.layers)):
            h.append(graph.hop_node(i))
        hops = graph.nbr_nums
        for i in range(len(self.layers) - 1):
            current_hops = hops if i == 0 else hops[:-i]
            h = self.layers[i].forward(h, current_hops)
            H = []
            for x in h:
                if self.bn_func is not None:
                    x = self.bn_func(x)
                if self.active_func is not None:
                    x = self.active_func(x)
                if self.dropout and conf.training:
                    x = tf.nn.dropout(x, keep_prob=1 - self.dropout)
                H.append(x)
            h = H
        h = self.layers[-1].forward(h, [hops[0]])
        assert len(h) == 1
        return h[0]