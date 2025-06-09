def touchstone_options(obj):
    """
    Validate if an object is an :ref:`TouchstoneOptions` pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises: RuntimeError (Argument \\`*[argument_name]*\\` is not valid). The
     token \\*[argument_name]\\* is replaced by the name of the argument the
     contract is attached to

    :rtype: None
    """
    if not isinstance(obj, dict) or (isinstance(obj, dict) and sorted(obj.keys()) != sorted(['units', 'ptype', 'pformat', 'z0'])):
        raise ValueError(pexdoc.pcontracts.get_exdesc())
    if not (obj['units'].lower() in ['ghz', 'mhz', 'khz', 'hz'] and obj['ptype'].lower() in ['s', 'y', 'z', 'h', 'g'] and (obj['pformat'].lower() in ['db', 'ma', 'ri']) and isinstance(obj['z0'], float) and (obj['z0'] >= 0)):
        raise ValueError(pexdoc.pcontracts.get_exdesc())