def _as_tensor(x, name, dtype):
    """Convenience to convert to `Tensor` or leave as `None`."""
    return None if x is None else tf.convert_to_tensor(value=x, name=name, dtype=dtype)