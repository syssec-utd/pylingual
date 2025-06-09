from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from mayan.apps.navigation.classes import Link
from .icons import icon_setting_namespace_detail, icon_setting_namespace_list, icon_setting_edit
from .permissions import permission_settings_edit, permission_settings_view

def condition_local_storage_enabled(context, resolved_object):
    return not settings.COMMON_DISABLE_LOCAL_STORAGE
link_setting_namespace_list = Link(icon=icon_setting_namespace_list, permissions=(permission_settings_view,), text=_('Settings'), view='settings:setting_namespace_list')
link_setting_namespace_detail = Link(args='resolved_object.name', icon=icon_setting_namespace_detail, permissions=(permission_settings_view,), text=_('Settings'), view='settings:setting_namespace_detail')
link_namespace_root_list = Link(icon=icon_setting_namespace_list, permissions=(permission_settings_view,), text=_('Namespaces'), view='settings:setting_namespace_list')
link_setting_edit = Link(args='resolved_object.global_name', condition=condition_local_storage_enabled, icon=icon_setting_edit, permissions=(permission_settings_edit,), text=_('Edit'), view='settings:setting_edit_view')