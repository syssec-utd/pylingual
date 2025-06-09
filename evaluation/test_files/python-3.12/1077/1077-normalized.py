def call(self, inputs):
    """Runs the model to generate a distribution `q(z_{1:T} | x_{1:T}, f)`.

    This generates a list of batched MultivariateNormalDiag
    distributions using the output of the recurrent model at each
    timestep to parameterize each distribution.

    Args:
      inputs: A tuple of a batch of intermediate representations of
        image frames across all timesteps of shape [..., batch_size,
        timesteps, dimensions], and a sample of the static latent
        variable `f` of shape [..., batch_size, latent_size].

    Returns:
      A batch of MultivariateNormalDiag distributions with event shape
      [latent_size], batch shape [broadcasted_shape, batch_size,
      timesteps], and sample shape [sample_shape, broadcasted_shape,
      batch_size, timesteps, latent_size], where `broadcasted_shape` is
      the broadcasted sampled shape between the inputs and static
      sample.
    """
    features, static_sample = inputs
    length = tf.shape(input=features)[-2]
    static_sample = static_sample[..., tf.newaxis, :] + tf.zeros([length, 1])
    sample_shape_static = tf.shape(input=static_sample)[:-3]
    sample_shape_inputs = tf.shape(input=features)[:-3]
    broadcast_shape_inputs = tf.concat((sample_shape_static, [1, 1, 1]), 0)
    broadcast_shape_static = tf.concat((sample_shape_inputs, [1, 1, 1]), 0)
    features = features + tf.zeros(broadcast_shape_inputs)
    static_sample = static_sample + tf.zeros(broadcast_shape_static)
    combined = tf.concat((features, static_sample), axis=-1)
    collapsed_shape = tf.concat(([-1], tf.shape(input=combined)[-2:]), axis=0)
    out = tf.reshape(combined, collapsed_shape)
    out = self.bilstm(out)
    out = self.rnn(out)
    expanded_shape = tf.concat((tf.shape(input=combined)[:-2], tf.shape(input=out)[1:]), axis=0)
    out = tf.reshape(out, expanded_shape)
    out = self.output_layer(out)
    loc = out[..., :self.latent_size]
    scale_diag = tf.nn.softplus(out[..., self.latent_size:]) + 1e-05
    return tfd.MultivariateNormalDiag(loc=loc, scale_diag=scale_diag)