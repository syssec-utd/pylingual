def get_template_field(env, fullname):
    """
    Gets template fields for specific operator class.

    :param fullname: Full path to operator class.
        For example: ``airflow.contrib.operators.gcp_vision_operator.CloudVisionProductSetCreateOperator``
    :return: List of template field
    :rtype: list[str]
    """
    modname, classname = fullname.rsplit('.', 1)
    try:
        with mock(env.config.autodoc_mock_imports):
            mod = import_module(modname)
    except ImportError:
        raise RoleException('Error loading %s module.' % (modname,))
    clazz = getattr(mod, classname)
    if not clazz:
        raise RoleException('Error finding %s class in %s module.' % (classname, modname))
    template_fields = getattr(clazz, 'template_fields')
    if not template_fields:
        raise RoleException('Could not find the template fields for %s class in %s module.' % (classname, modname))
    return list(template_fields)