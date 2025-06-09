import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetReferenceDataSetResult', 'AwaitableGetReferenceDataSetResult', 'get_reference_data_set', 'get_reference_data_set_output']
warnings.warn('Version 2018-08-15-preview will be removed in v2 of the provider.', DeprecationWarning)

@pulumi.output_type
class GetReferenceDataSetResult:
    """
    A reference data set provides metadata about the events in an environment. Metadata in the reference data set will be joined with events as they are read from event sources. The metadata that makes up the reference data set is uploaded or modified through the Time Series Insights data plane APIs.
    """

    def __init__(__self__, creation_time=None, data_string_comparison_behavior=None, id=None, key_properties=None, location=None, name=None, provisioning_state=None, tags=None, type=None):
        if creation_time and (not isinstance(creation_time, str)):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, 'creation_time', creation_time)
        if data_string_comparison_behavior and (not isinstance(data_string_comparison_behavior, str)):
            raise TypeError("Expected argument 'data_string_comparison_behavior' to be a str")
        pulumi.set(__self__, 'data_string_comparison_behavior', data_string_comparison_behavior)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if key_properties and (not isinstance(key_properties, list)):
            raise TypeError("Expected argument 'key_properties' to be a list")
        pulumi.set(__self__, 'key_properties', key_properties)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='creationTime')
    def creation_time(self) -> str:
        """
        The time the resource was created.
        """
        return pulumi.get(self, 'creation_time')

    @property
    @pulumi.getter(name='dataStringComparisonBehavior')
    def data_string_comparison_behavior(self) -> Optional[str]:
        """
        The reference data set key comparison behavior can be set using this property. By default, the value is 'Ordinal' - which means case sensitive key comparison will be performed while joining reference data with events or while adding new reference data. When 'OrdinalIgnoreCase' is set, case insensitive comparison will be used.
        """
        return pulumi.get(self, 'data_string_comparison_behavior')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='keyProperties')
    def key_properties(self) -> Sequence['outputs.ReferenceDataSetKeyPropertyResponse']:
        """
        The list of key properties for the reference data set.
        """
        return pulumi.get(self, 'key_properties')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

class AwaitableGetReferenceDataSetResult(GetReferenceDataSetResult):

    def __await__(self):
        if False:
            yield self
        return GetReferenceDataSetResult(creation_time=self.creation_time, data_string_comparison_behavior=self.data_string_comparison_behavior, id=self.id, key_properties=self.key_properties, location=self.location, name=self.name, provisioning_state=self.provisioning_state, tags=self.tags, type=self.type)

def get_reference_data_set(environment_name: Optional[str]=None, reference_data_set_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetReferenceDataSetResult:
    """
    Gets the reference data set with the specified name in the specified environment.


    :param str environment_name: The name of the Time Series Insights environment associated with the specified resource group.
    :param str reference_data_set_name: The name of the Time Series Insights reference data set associated with the specified environment.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    pulumi.log.warn('get_reference_data_set is deprecated: Version 2018-08-15-preview will be removed in v2 of the provider.')
    __args__ = dict()
    __args__['environmentName'] = environment_name
    __args__['referenceDataSetName'] = reference_data_set_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:timeseriesinsights/v20180815preview:getReferenceDataSet', __args__, opts=opts, typ=GetReferenceDataSetResult).value
    return AwaitableGetReferenceDataSetResult(creation_time=__ret__.creation_time, data_string_comparison_behavior=__ret__.data_string_comparison_behavior, id=__ret__.id, key_properties=__ret__.key_properties, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_reference_data_set)
def get_reference_data_set_output(environment_name: Optional[pulumi.Input[str]]=None, reference_data_set_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetReferenceDataSetResult]:
    """
    Gets the reference data set with the specified name in the specified environment.


    :param str environment_name: The name of the Time Series Insights environment associated with the specified resource group.
    :param str reference_data_set_name: The name of the Time Series Insights reference data set associated with the specified environment.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    pulumi.log.warn('get_reference_data_set is deprecated: Version 2018-08-15-preview will be removed in v2 of the provider.')
    ...