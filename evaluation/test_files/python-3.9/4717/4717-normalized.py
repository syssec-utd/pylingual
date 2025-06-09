def finalize():
    """A function that should be called after parsing all Gin config files.

  Calling this function allows registered "finalize hooks" to inspect (and
  potentially modify) the Gin config, to provide additional functionality. Hooks
  should not modify the configuration object they receive directly; instead,
  they should return a dictionary mapping Gin binding keys to (new or updated)
  values. This way, all hooks see the config as originally parsed.

  Raises:
    RuntimeError: If the config is already locked.
    ValueError: If two or more hooks attempt to modify or introduce bindings for
      the same key. Since it is difficult to control the order in which hooks
      are registered, allowing this could yield unpredictable behavior.
  """
    if config_is_locked():
        raise RuntimeError('Finalize called twice (config already locked).')
    bindings = {}
    for hook in _FINALIZE_HOOKS:
        new_bindings = hook(_CONFIG)
        if new_bindings is not None:
            for (key, value) in six.iteritems(new_bindings):
                pbk = ParsedBindingKey(key)
                if pbk in bindings:
                    err_str = 'Received conflicting updates when running {}.'
                    raise ValueError(err_str.format(hook))
                bindings[pbk] = value
    for (pbk, value) in six.iteritems(bindings):
        bind_parameter(pbk, value)
    _set_config_is_locked(True)