import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetHierarchySettingResult', 'AwaitableGetHierarchySettingResult', 'get_hierarchy_setting', 'get_hierarchy_setting_output']

@pulumi.output_type
class GetHierarchySettingResult:
    """
    Settings defined at the Management Group scope.
    """

    def __init__(__self__, default_management_group=None, id=None, name=None, require_authorization_for_group_creation=None, tenant_id=None, type=None):
        if default_management_group and (not isinstance(default_management_group, str)):
            raise TypeError("Expected argument 'default_management_group' to be a str")
        pulumi.set(__self__, 'default_management_group', default_management_group)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if require_authorization_for_group_creation and (not isinstance(require_authorization_for_group_creation, bool)):
            raise TypeError("Expected argument 'require_authorization_for_group_creation' to be a bool")
        pulumi.set(__self__, 'require_authorization_for_group_creation', require_authorization_for_group_creation)
        if tenant_id and (not isinstance(tenant_id, str)):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, 'tenant_id', tenant_id)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='defaultManagementGroup')
    def default_management_group(self) -> Optional[str]:
        """
        Settings that sets the default Management Group under which new subscriptions get added in this tenant. For example, /providers/Microsoft.Management/managementGroups/defaultGroup
        """
        return pulumi.get(self, 'default_management_group')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The fully qualified ID for the settings object.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000/settings/default.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the object. In this case, default.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='requireAuthorizationForGroupCreation')
    def require_authorization_for_group_creation(self) -> Optional[bool]:
        """
        Indicates whether RBAC access is required upon group creation under the root Management Group. If set to true, user will require Microsoft.Management/managementGroups/write action on the root Management Group scope in order to create new Groups directly under the root. This will prevent new users from creating new Management Groups, unless they are given access.
        """
        return pulumi.get(self, 'require_authorization_for_group_creation')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> Optional[str]:
        """
        The AAD Tenant ID associated with the hierarchy settings. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.  For example, Microsoft.Management/managementGroups/settings.
        """
        return pulumi.get(self, 'type')

class AwaitableGetHierarchySettingResult(GetHierarchySettingResult):

    def __await__(self):
        if False:
            yield self
        return GetHierarchySettingResult(default_management_group=self.default_management_group, id=self.id, name=self.name, require_authorization_for_group_creation=self.require_authorization_for_group_creation, tenant_id=self.tenant_id, type=self.type)

def get_hierarchy_setting(group_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetHierarchySettingResult:
    """
    Gets the hierarchy settings defined at the Management Group level. Settings can only be set on the root Management Group of the hierarchy.


    :param str group_id: Management Group ID.
    """
    __args__ = dict()
    __args__['groupId'] = group_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:management/v20201001:getHierarchySetting', __args__, opts=opts, typ=GetHierarchySettingResult).value
    return AwaitableGetHierarchySettingResult(default_management_group=__ret__.default_management_group, id=__ret__.id, name=__ret__.name, require_authorization_for_group_creation=__ret__.require_authorization_for_group_creation, tenant_id=__ret__.tenant_id, type=__ret__.type)

@_utilities.lift_output_func(get_hierarchy_setting)
def get_hierarchy_setting_output(group_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetHierarchySettingResult]:
    """
    Gets the hierarchy settings defined at the Management Group level. Settings can only be set on the root Management Group of the hierarchy.


    :param str group_id: Management Group ID.
    """
    ...