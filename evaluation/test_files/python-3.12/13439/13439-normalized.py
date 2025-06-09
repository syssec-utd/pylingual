def get_dot_target_name_safe(version=None, module=None):
    """
  Returns the current version/module in -dot- notation which is used by `target:` parameters.
  If there is no current version or module then None is returned.
  """
    version = version or get_current_version_name_safe()
    module = module or get_current_module_name_safe()
    if version and module:
        return '-dot-'.join((version, module))
    return None