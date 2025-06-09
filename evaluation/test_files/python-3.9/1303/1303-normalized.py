def prepare_args(model_matrix, response, model_coefficients, predicted_linear_response, offset, name=None):
    """Helper to `fit` which sanitizes input args.

  Args:
    model_matrix: (Batch of) `float`-like, matrix-shaped `Tensor` where each row
      represents a sample's features.
    response: (Batch of) vector-shaped `Tensor` where each element represents a
      sample's observed response (to the corresponding row of features). Must
      have same `dtype` as `model_matrix`.
    model_coefficients: Optional (batch of) vector-shaped `Tensor` representing
      the model coefficients, one for each column in `model_matrix`. Must have
      same `dtype` as `model_matrix`.
      Default value: `tf.zeros(tf.shape(model_matrix)[-1], model_matrix.dtype)`.
    predicted_linear_response: Optional `Tensor` with `shape`, `dtype` matching
      `response`; represents `offset` shifted initial linear predictions based
      on current `model_coefficients`.
      Default value: `offset` if `model_coefficients is None`, and
      `tf.linalg.matvec(model_matrix, model_coefficients_start) + offset`
      otherwise.
    offset: Optional `Tensor` with `shape`, `dtype` matching `response`;
      represents constant shift applied to `predicted_linear_response`.
      Default value: `None` (i.e., `tf.zeros_like(response)`).
    name: Python `str` used as name prefix to ops created by this function.
      Default value: `"prepare_args"`.

  Returns:
    model_matrix: A `Tensor` with `shape`, `dtype` and values of the
      `model_matrix` argument.
    response: A `Tensor` with `shape`, `dtype` and values of the
      `response` argument.
    model_coefficients_start: A `Tensor` with `shape`, `dtype` and
      values of the `model_coefficients_start` argument if specified.
      A (batch of) vector-shaped `Tensors` with `dtype` matching `model_matrix`
      containing the default starting point otherwise.
    predicted_linear_response:  A `Tensor` with `shape`, `dtype` and
      values of the `predicted_linear_response` argument if specified.
      A `Tensor` with `shape`, `dtype` matching `response` containing the
      default value otherwise.
    offset: A `Tensor` with `shape`, `dtype` and values of the `offset` argument
      if specified or `None` otherwise.
  """
    graph_deps = [model_matrix, response, model_coefficients, predicted_linear_response, offset]
    with tf.compat.v1.name_scope(name, 'prepare_args', graph_deps):
        dtype = dtype_util.common_dtype(graph_deps, np.float32)
        model_matrix = tf.convert_to_tensor(value=model_matrix, dtype=dtype, name='model_matrix')
        if offset is not None:
            offset = tf.convert_to_tensor(value=offset, dtype=dtype, name='offset')
        response = tf.convert_to_tensor(value=response, dtype=dtype, name='response')
        use_default_model_coefficients = model_coefficients is None
        if use_default_model_coefficients:
            batch_shape = tf.shape(input=model_matrix)[:-2]
            num_columns = tf.shape(input=model_matrix)[-1]
            model_coefficients = tf.zeros(shape=tf.concat([batch_shape, [num_columns]], axis=0), dtype=dtype, name='model_coefficients')
        else:
            model_coefficients = tf.convert_to_tensor(value=model_coefficients, dtype=dtype, name='model_coefficients')
        if predicted_linear_response is None:
            if use_default_model_coefficients:
                if offset is None:
                    predicted_linear_response = tf.zeros_like(response, dtype, name='predicted_linear_response')
                else:
                    predicted_linear_response = tf.broadcast_to(offset, tf.shape(input=response), name='predicted_linear_response')
            else:
                predicted_linear_response = calculate_linear_predictor(model_matrix, model_coefficients, offset)
        else:
            predicted_linear_response = tf.convert_to_tensor(value=predicted_linear_response, dtype=dtype, name='predicted_linear_response')
    return [model_matrix, response, model_coefficients, predicted_linear_response, offset]