def make_decoder(base_depth, activation, input_size, output_shape):
    """Creates the decoder function.

  Args:
    base_depth: Layer base depth in decoder net.
    activation: Activation function in hidden layers.
    input_size: The flattened latent input shape as an int.
    output_shape: The output image shape as a list.

  Returns:
    decoder: A `callable` mapping a `Tensor` of encodings to a
      `tfd.Distribution` instance over images.
  """
    deconv = functools.partial(tf.keras.layers.Conv2DTranspose, padding='SAME', activation=activation)
    conv = functools.partial(tf.keras.layers.Conv2D, padding='SAME', activation=activation)
    decoder_net = tf.keras.Sequential([tf.keras.layers.Reshape((1, 1, input_size)), deconv(2 * base_depth, 7, padding='VALID'), deconv(2 * base_depth, 5), deconv(2 * base_depth, 5, 2), deconv(base_depth, 5), deconv(base_depth, 5, 2), deconv(base_depth, 5), conv(output_shape[-1], 5, activation=None), tf.keras.layers.Reshape(output_shape)])

    def decoder(codes):
        """Builds a distribution over images given codes.

    Args:
      codes: A `Tensor` representing the inputs to be decoded, of shape `[...,
        code_size]`.

    Returns:
      decoder_distribution: A multivariate `Bernoulli` distribution.
    """
        logits = decoder_net(codes)
        return tfd.Independent(tfd.Bernoulli(logits=logits), reinterpreted_batch_ndims=len(output_shape), name='decoder_distribution')
    return decoder