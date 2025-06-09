import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ListChannelWithKeysResult', 'AwaitableListChannelWithKeysResult', 'list_channel_with_keys', 'list_channel_with_keys_output']

@pulumi.output_type
class ListChannelWithKeysResult:
    """
    The ARM channel of list channel with keys operation response.
    """

    def __init__(__self__, changed_time=None, entity_tag=None, etag=None, id=None, kind=None, location=None, name=None, properties=None, provisioning_state=None, resource=None, setting=None, sku=None, tags=None, type=None, zones=None):
        if changed_time and (not isinstance(changed_time, str)):
            raise TypeError("Expected argument 'changed_time' to be a str")
        pulumi.set(__self__, 'changed_time', changed_time)
        if entity_tag and (not isinstance(entity_tag, str)):
            raise TypeError("Expected argument 'entity_tag' to be a str")
        pulumi.set(__self__, 'entity_tag', entity_tag)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if resource and (not isinstance(resource, dict)):
            raise TypeError("Expected argument 'resource' to be a dict")
        pulumi.set(__self__, 'resource', resource)
        if setting and (not isinstance(setting, dict)):
            raise TypeError("Expected argument 'setting' to be a dict")
        pulumi.set(__self__, 'setting', setting)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if zones and (not isinstance(zones, list)):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, 'zones', zones)

    @property
    @pulumi.getter(name='changedTime')
    def changed_time(self) -> Optional[str]:
        """
        Changed time of the resource
        """
        return pulumi.get(self, 'changed_time')

    @property
    @pulumi.getter(name='entityTag')
    def entity_tag(self) -> Optional[str]:
        """
        Entity tag of the resource
        """
        return pulumi.get(self, 'entity_tag')

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Entity Tag
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Specifies the resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Required. Gets or sets the Kind of the resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> Any:
        """
        The set of properties specific to bot channel resource
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the resource
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def resource(self) -> Optional[Any]:
        """
        The set of properties specific to bot channel resource
        """
        return pulumi.get(self, 'resource')

    @property
    @pulumi.getter
    def setting(self) -> Optional['outputs.ChannelSettingsResponse']:
        """
        Channel settings
        """
        return pulumi.get(self, 'setting')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        Gets or sets the SKU of the resource.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        Entity zones
        """
        return pulumi.get(self, 'zones')

class AwaitableListChannelWithKeysResult(ListChannelWithKeysResult):

    def __await__(self):
        if False:
            yield self
        return ListChannelWithKeysResult(changed_time=self.changed_time, entity_tag=self.entity_tag, etag=self.etag, id=self.id, kind=self.kind, location=self.location, name=self.name, properties=self.properties, provisioning_state=self.provisioning_state, resource=self.resource, setting=self.setting, sku=self.sku, tags=self.tags, type=self.type, zones=self.zones)

def list_channel_with_keys(channel_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListChannelWithKeysResult:
    """
    The ARM channel of list channel with keys operation response.


    :param str channel_name: The name of the Channel resource.
    :param str resource_group_name: The name of the Bot resource group in the user subscription.
    :param str resource_name: The name of the Bot resource.
    """
    __args__ = dict()
    __args__['channelName'] = channel_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:botservice/v20210501preview:listChannelWithKeys', __args__, opts=opts, typ=ListChannelWithKeysResult).value
    return AwaitableListChannelWithKeysResult(changed_time=__ret__.changed_time, entity_tag=__ret__.entity_tag, etag=__ret__.etag, id=__ret__.id, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, provisioning_state=__ret__.provisioning_state, resource=__ret__.resource, setting=__ret__.setting, sku=__ret__.sku, tags=__ret__.tags, type=__ret__.type, zones=__ret__.zones)

@_utilities.lift_output_func(list_channel_with_keys)
def list_channel_with_keys_output(channel_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListChannelWithKeysResult]:
    """
    The ARM channel of list channel with keys operation response.


    :param str channel_name: The name of the Channel resource.
    :param str resource_group_name: The name of the Bot resource group in the user subscription.
    :param str resource_name: The name of the Bot resource.
    """
    ...