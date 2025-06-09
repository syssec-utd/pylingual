def bind_parameter(binding_key, value):
    """Binds the parameter value specified by `binding_key` to `value`.

  The `binding_key` argument should either be a string of the form
  `maybe/scope/optional.module.names.configurable_name.parameter_name`, or a
  list or tuple of `(scope, selector, parameter_name)`, where `selector`
  corresponds to `optional.module.names.configurable_name`. Once this function
  has been called, subsequent calls (in the specified scope) to the specified
  configurable function will have `value` supplied to their `parameter_name`
  parameter.

  Example:

      @configurable('fully_connected_network')
      def network_fn(num_layers=5, units_per_layer=1024):
         ...

      def main(_):
        config.bind_parameter('fully_connected_network.num_layers', 3)
        network_fn()  # Called with num_layers == 3, not the default of 5.

  Args:
    binding_key: The parameter whose value should be set. This can either be a
      string, or a tuple of the form `(scope, selector, parameter)`.
    value: The desired value.

  Raises:
    RuntimeError: If the config is locked.
    ValueError: If no function can be found matching the configurable name
      specified by `binding_key`, or if the specified parameter name is
      blacklisted or not in the function's whitelist (if present).
  """
    if config_is_locked():
        raise RuntimeError('Attempted to modify locked Gin config.')
    pbk = ParsedBindingKey(binding_key)
    fn_dict = _CONFIG.setdefault(pbk.config_key, {})
    fn_dict[pbk.arg_name] = value