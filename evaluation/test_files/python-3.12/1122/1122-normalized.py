def _reparameterize_sample(self, x):
    """Adds reparameterization (pathwise) gradients to samples of the mixture.

    Implicit reparameterization gradients are
       dx/dphi = -(d transform(x, phi) / dx)^-1 * d transform(x, phi) / dphi,
    where transform(x, phi) is distributional transform that removes all
    parameters from samples x.

    We implement them by replacing x with
      -stop_gradient(d transform(x, phi) / dx)^-1 * transform(x, phi)]
    for the backward pass (gradient computation).
    The derivative of this quantity w.r.t. phi is then the implicit
    reparameterization gradient.
    Note that this replaces the gradients w.r.t. both the mixture
    distribution parameters and components distributions parameters.

    Limitations:
      1. Fundamental: components must be fully reparameterized.
      2. Distributional transform is currently only implemented for
        factorized components.
      3. Distributional transform currently only works for known rank of the
        batch tensor.

    Arguments:
      x: Sample of mixture distribution

    Returns:
      Tensor with same value as x, but with reparameterization gradients
    """
    x = tf.stop_gradient(x)
    x_2d_shape = [-1, self._event_size]

    def reshaped_distributional_transform(x_2d):
        return tf.reshape(self._distributional_transform(tf.reshape(x_2d, tf.shape(input=x))), x_2d_shape)
    transform_2d, jacobian = _value_and_batch_jacobian(reshaped_distributional_transform, tf.reshape(x, x_2d_shape))
    transform_2d = _prevent_2nd_derivative(transform_2d)
    surrogate_x_2d = -tf.linalg.triangular_solve(tf.stop_gradient(jacobian), tf.expand_dims(transform_2d, axis=-1), lower=True)
    surrogate_x = tf.reshape(surrogate_x_2d, tf.shape(input=x))
    return x + (surrogate_x - tf.stop_gradient(surrogate_x))