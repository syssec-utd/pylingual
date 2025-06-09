def _machine_eps(dtype):
    """Returns the machine epsilon for the supplied dtype."""
    if isinstance(dtype, tf.DType):
        dtype = dtype.as_numpy_dtype()
    return np.finfo(dtype).eps