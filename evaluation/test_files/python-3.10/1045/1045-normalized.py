def factored_joint_mvn(distributions):
    """Combine MultivariateNormals into a factored joint distribution.

   Given a list of multivariate normal distributions
   `dist[i] = Normal(loc[i], scale[i])`, construct the joint
   distribution given by concatenating independent samples from these
   distributions. This is multivariate normal with mean vector given by the
   concatenation of the component mean vectors, and block-diagonal covariance
   matrix in which the blocks are the component covariances.

   Note that for computational efficiency, multivariate normals are represented
   by a 'scale' (factored covariance) linear operator rather than the full
   covariance matrix.

  Args:
    distributions: Python `iterable` of MultivariateNormal distribution
      instances (e.g., `tfd.MultivariateNormalDiag`,
      `tfd.MultivariateNormalTriL`, etc.). These must be broadcastable to a
      consistent batch shape, but may have different event shapes
      (i.e., defined over spaces of different dimension).

  Returns:
    joint_distribution: An instance of `tfd.MultivariateNormalLinearOperator`
      representing the joint distribution constructed by concatenating
      an independent sample from each input distributions.
  """
    graph_parents = [tensor for distribution in distributions for tensor in distribution._graph_parents]
    with tf.compat.v1.name_scope('factored_joint_mvn', values=graph_parents):
        dtype = tf.debugging.assert_same_float_dtype(distributions)
        broadcast_ones = tf.ones(broadcast_batch_shape(distributions), dtype=dtype)[..., tf.newaxis]
        return MultivariateNormalLinearOperator(loc=tf.concat([mvn.mean() * broadcast_ones for mvn in distributions], axis=-1), scale=tfl.LinearOperatorBlockDiag([mvn.scale for mvn in distributions], is_square=True))