import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetReplicationNetworkMappingResult', 'AwaitableGetReplicationNetworkMappingResult', 'get_replication_network_mapping', 'get_replication_network_mapping_output']

@pulumi.output_type
class GetReplicationNetworkMappingResult:
    """
    Network Mapping model. Ideally it should have been possible to inherit this class from prev version in InheritedModels as long as there is no difference in structure or method signature. Since there were no base Models for certain fields and methods viz NetworkMappingProperties and Load with required return type, the class has been introduced in its entirety with references to base models to facilitate extensions in subsequent versions.
    """

    def __init__(__self__, id=None, location=None, name=None, properties=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource Location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.NetworkMappingPropertiesResponse':
        """
        The Network Mapping Properties.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, 'type')

class AwaitableGetReplicationNetworkMappingResult(GetReplicationNetworkMappingResult):

    def __await__(self):
        if False:
            yield self
        return GetReplicationNetworkMappingResult(id=self.id, location=self.location, name=self.name, properties=self.properties, type=self.type)

def get_replication_network_mapping(fabric_name: Optional[str]=None, network_mapping_name: Optional[str]=None, network_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetReplicationNetworkMappingResult:
    """
    Gets the details of an ASR network mapping.


    :param str fabric_name: Primary fabric name.
    :param str network_mapping_name: Network mapping name.
    :param str network_name: Primary network name.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    """
    __args__ = dict()
    __args__['fabricName'] = fabric_name
    __args__['networkMappingName'] = network_mapping_name
    __args__['networkName'] = network_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:recoveryservices/v20210801:getReplicationNetworkMapping', __args__, opts=opts, typ=GetReplicationNetworkMappingResult).value
    return AwaitableGetReplicationNetworkMappingResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, type=__ret__.type)

@_utilities.lift_output_func(get_replication_network_mapping)
def get_replication_network_mapping_output(fabric_name: Optional[pulumi.Input[str]]=None, network_mapping_name: Optional[pulumi.Input[str]]=None, network_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetReplicationNetworkMappingResult]:
    """
    Gets the details of an ASR network mapping.


    :param str fabric_name: Primary fabric name.
    :param str network_mapping_name: Network mapping name.
    :param str network_name: Primary network name.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    """
    ...