def _value(self, dtype=None, name=None, as_ref=False):
    """Get the value returned by `tf.convert_to_tensor(distribution)`.

  Note: this function may mutate the distribution instance state by caching
  the concretized `Tensor` value.

  Args:
    dtype: Must return a `Tensor` with the given `dtype` if specified.
    name: If the conversion function creates a new `Tensor`, it should use the
      given `name` if specified.
    as_ref: `as_ref` is true, the function must return a `Tensor` reference,
      such as a `Variable`.
  Returns:
    concretized_distribution_value: `Tensor` identical to
    `tf.convert_to_tensor(distribution)`.

  #### Examples

  ```python
  tfd = tfp.distributions
  x = tfd.Normal(0.5, 1).set_tensor_conversion(tfd.Distribution.mean)

  x._value()
  # ==> tf.convert_to_tensor(x) ==> 0.5

  x._value() + 2
  # ==> tf.convert_to_tensor(x) + 2. ==> 2.5

  x + 2
  # ==> tf.convert_to_tensor(x) + 2. ==> 2.5
  ```

  """
    if as_ref:
        raise NotImplementedError('Cannot convert a `Distribution` to a reference (e.g., `tf.Variable`).')
    if self._concrete_value is None:
        if self._convert_to_tensor_fn is None:
            raise NotImplementedError('Failed to convert object of type {} to Tensor. Contents: {}. Call `distribution.set_tensor_conversion(lambda self: ...)` to enable `tf.convert_to_tensor` capability. For example: `x = tfd.Normal(0,1).set_tensor_conversion(tfd.Distribution.mean)` results in `tf.convert_to_tensor(x)` being identical to `x.mean()`.'.format(type(self), self))
        with self._name_scope('value'):
            self._concrete_value = self._convert_to_tensor_fn(self) if callable(self._convert_to_tensor_fn) else self._convert_to_tensor_fn
            if not tf.is_tensor(self._concrete_value):
                self._concrete_value = tfd._convert_to_tensor(value=self._concrete_value, name=name or 'concrete_value', dtype=dtype, dtype_hint=self.dtype)
    return self._concrete_value