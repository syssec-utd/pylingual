def import_project_sitetree_modules():
    """Imports sitetrees modules from packages (apps).
    Returns a list of submodules.

    :rtype: list
    """
    from django.conf import settings as django_settings
    submodules = []
    for app in django_settings.INSTALLED_APPS:
        module = import_app_sitetree_module(app)
        if module is not None:
            submodules.append(module)
    return submodules