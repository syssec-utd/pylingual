def only_module(*modules):
    """
        This will exclude all modules from the traceback except these "modules"
    :param modules: list of modules to report in traceback
    :return:        None
    """
    modules = (modules and isinstance(modules[0], list)) and modules[0] or modules
    for module in modules:
        if not module in ONLY_MODULES:
            ONLY_MODULES.append(module)
    traceback.extract_tb = _new_extract_tb