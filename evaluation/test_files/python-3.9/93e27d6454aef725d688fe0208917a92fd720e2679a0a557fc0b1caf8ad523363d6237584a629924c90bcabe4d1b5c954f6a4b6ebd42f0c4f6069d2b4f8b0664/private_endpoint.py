import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['PrivateEndpointArgs', 'PrivateEndpoint']

@pulumi.input_type
class PrivateEndpointArgs:

    def __init__(__self__, *, compartment_id: pulumi.Input[str], display_name: pulumi.Input[str], subnet_id: pulumi.Input[str], vcn_id: pulumi.Input[str], defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, description: Optional[pulumi.Input[str]]=None, dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, is_used_with_configuration_source_provider: Optional[pulumi.Input[bool]]=None, nsg_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a PrivateEndpoint resource.
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        :param pulumi.Input[str] display_name: (Updatable) The private endpoint display name. Avoid entering confidential information.
        :param pulumi.Input[str] subnet_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        :param pulumi.Input[str] vcn_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] description: (Updatable) Description of the private endpoint. Avoid entering confidential information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_zones: (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[bool] is_used_with_configuration_source_provider: (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] nsg_id_lists: (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        """
        pulumi.set(__self__, 'compartment_id', compartment_id)
        pulumi.set(__self__, 'display_name', display_name)
        pulumi.set(__self__, 'subnet_id', subnet_id)
        pulumi.set(__self__, 'vcn_id', vcn_id)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if dns_zones is not None:
            pulumi.set(__self__, 'dns_zones', dns_zones)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if is_used_with_configuration_source_provider is not None:
            pulumi.set(__self__, 'is_used_with_configuration_source_provider', is_used_with_configuration_source_provider)
        if nsg_id_lists is not None:
            pulumi.set(__self__, 'nsg_id_lists', nsg_id_lists)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Input[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        (Updatable) The private endpoint display name. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='subnetId')
    def subnet_id(self) -> pulumi.Input[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        """
        return pulumi.get(self, 'subnet_id')

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'subnet_id', value)

    @property
    @pulumi.getter(name='vcnId')
    def vcn_id(self) -> pulumi.Input[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'vcn_id')

    @vcn_id.setter
    def vcn_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'vcn_id', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) Description of the private endpoint. Avoid entering confidential information.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='dnsZones')
    def dns_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        """
        return pulumi.get(self, 'dns_zones')

    @dns_zones.setter
    def dns_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'dns_zones', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='isUsedWithConfigurationSourceProvider')
    def is_used_with_configuration_source_provider(self) -> Optional[pulumi.Input[bool]]:
        """
        (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        """
        return pulumi.get(self, 'is_used_with_configuration_source_provider')

    @is_used_with_configuration_source_provider.setter
    def is_used_with_configuration_source_provider(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_used_with_configuration_source_provider', value)

    @property
    @pulumi.getter(name='nsgIdLists')
    def nsg_id_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        """
        return pulumi.get(self, 'nsg_id_lists')

    @nsg_id_lists.setter
    def nsg_id_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'nsg_id_lists', value)

@pulumi.input_type
class _PrivateEndpointState:

    def __init__(__self__, *, compartment_id: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, is_used_with_configuration_source_provider: Optional[pulumi.Input[bool]]=None, nsg_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, source_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, state: Optional[pulumi.Input[str]]=None, subnet_id: Optional[pulumi.Input[str]]=None, time_created: Optional[pulumi.Input[str]]=None, vcn_id: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering PrivateEndpoint resources.
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] description: (Updatable) Description of the private endpoint. Avoid entering confidential information.
        :param pulumi.Input[str] display_name: (Updatable) The private endpoint display name. Avoid entering confidential information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_zones: (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[bool] is_used_with_configuration_source_provider: (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] nsg_id_lists: (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ips: The source IPs which resource manager service will use to connect to customer's network. Automatically assigned by Resource Manager Service.
        :param pulumi.Input[str] state: The current lifecycle state of the private endpoint.
        :param pulumi.Input[str] subnet_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        :param pulumi.Input[str] time_created: The date and time at which the private endpoint was created. Format is defined by RFC3339. Example: `2020-11-25T21:10:29.600Z`
        :param pulumi.Input[str] vcn_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        if compartment_id is not None:
            pulumi.set(__self__, 'compartment_id', compartment_id)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if dns_zones is not None:
            pulumi.set(__self__, 'dns_zones', dns_zones)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if is_used_with_configuration_source_provider is not None:
            pulumi.set(__self__, 'is_used_with_configuration_source_provider', is_used_with_configuration_source_provider)
        if nsg_id_lists is not None:
            pulumi.set(__self__, 'nsg_id_lists', nsg_id_lists)
        if source_ips is not None:
            pulumi.set(__self__, 'source_ips', source_ips)
        if state is not None:
            pulumi.set(__self__, 'state', state)
        if subnet_id is not None:
            pulumi.set(__self__, 'subnet_id', subnet_id)
        if time_created is not None:
            pulumi.set(__self__, 'time_created', time_created)
        if vcn_id is not None:
            pulumi.set(__self__, 'vcn_id', vcn_id)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) Description of the private endpoint. Avoid entering confidential information.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The private endpoint display name. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='dnsZones')
    def dns_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        """
        return pulumi.get(self, 'dns_zones')

    @dns_zones.setter
    def dns_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'dns_zones', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='isUsedWithConfigurationSourceProvider')
    def is_used_with_configuration_source_provider(self) -> Optional[pulumi.Input[bool]]:
        """
        (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        """
        return pulumi.get(self, 'is_used_with_configuration_source_provider')

    @is_used_with_configuration_source_provider.setter
    def is_used_with_configuration_source_provider(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_used_with_configuration_source_provider', value)

    @property
    @pulumi.getter(name='nsgIdLists')
    def nsg_id_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        """
        return pulumi.get(self, 'nsg_id_lists')

    @nsg_id_lists.setter
    def nsg_id_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'nsg_id_lists', value)

    @property
    @pulumi.getter(name='sourceIps')
    def source_ips(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The source IPs which resource manager service will use to connect to customer's network. Automatically assigned by Resource Manager Service.
        """
        return pulumi.get(self, 'source_ips')

    @source_ips.setter
    def source_ips(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'source_ips', value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current lifecycle state of the private endpoint.
        """
        return pulumi.get(self, 'state')

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'state', value)

    @property
    @pulumi.getter(name='subnetId')
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        """
        return pulumi.get(self, 'subnet_id')

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnet_id', value)

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time at which the private endpoint was created. Format is defined by RFC3339. Example: `2020-11-25T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_created')

    @time_created.setter
    def time_created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'time_created', value)

    @property
    @pulumi.getter(name='vcnId')
    def vcn_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'vcn_id')

    @vcn_id.setter
    def vcn_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vcn_id', value)

class PrivateEndpoint(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, compartment_id: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, is_used_with_configuration_source_provider: Optional[pulumi.Input[bool]]=None, nsg_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, subnet_id: Optional[pulumi.Input[str]]=None, vcn_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        This resource provides the Private Endpoint resource in Oracle Cloud Infrastructure Resource Manager service.

        Creates a a private endpoint in the specified compartment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_private_endpoint = oci.resource_manager.PrivateEndpoint("testPrivateEndpoint",
            compartment_id=var["compartment_id"],
            display_name=var["private_endpoint_display_name"],
            subnet_id=oci_core_subnet["test_subnet"]["id"],
            vcn_id=oci_core_vcn["test_vcn"]["id"],
            defined_tags={
                "Operations.CostCenter": "42",
            },
            description=var["private_endpoint_description"],
            dns_zones=var["private_endpoint_dns_zones"],
            freeform_tags={
                "Department": "Finance",
            },
            is_used_with_configuration_source_provider=var["private_endpoint_is_used_with_configuration_source_provider"],
            nsg_id_lists=var["private_endpoint_nsg_id_list"])
        ```

        ## Import

        PrivateEndpoints can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:ResourceManager/privateEndpoint:PrivateEndpoint test_private_endpoint "id"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] description: (Updatable) Description of the private endpoint. Avoid entering confidential information.
        :param pulumi.Input[str] display_name: (Updatable) The private endpoint display name. Avoid entering confidential information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_zones: (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[bool] is_used_with_configuration_source_provider: (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] nsg_id_lists: (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        :param pulumi.Input[str] subnet_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        :param pulumi.Input[str] vcn_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PrivateEndpointArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        This resource provides the Private Endpoint resource in Oracle Cloud Infrastructure Resource Manager service.

        Creates a a private endpoint in the specified compartment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_private_endpoint = oci.resource_manager.PrivateEndpoint("testPrivateEndpoint",
            compartment_id=var["compartment_id"],
            display_name=var["private_endpoint_display_name"],
            subnet_id=oci_core_subnet["test_subnet"]["id"],
            vcn_id=oci_core_vcn["test_vcn"]["id"],
            defined_tags={
                "Operations.CostCenter": "42",
            },
            description=var["private_endpoint_description"],
            dns_zones=var["private_endpoint_dns_zones"],
            freeform_tags={
                "Department": "Finance",
            },
            is_used_with_configuration_source_provider=var["private_endpoint_is_used_with_configuration_source_provider"],
            nsg_id_lists=var["private_endpoint_nsg_id_list"])
        ```

        ## Import

        PrivateEndpoints can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:ResourceManager/privateEndpoint:PrivateEndpoint test_private_endpoint "id"
        ```

        :param str resource_name: The name of the resource.
        :param PrivateEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(PrivateEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, compartment_id: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, is_used_with_configuration_source_provider: Optional[pulumi.Input[bool]]=None, nsg_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, subnet_id: Optional[pulumi.Input[str]]=None, vcn_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateEndpointArgs.__new__(PrivateEndpointArgs)
            if compartment_id is None and (not opts.urn):
                raise TypeError("Missing required property 'compartment_id'")
            __props__.__dict__['compartment_id'] = compartment_id
            __props__.__dict__['defined_tags'] = defined_tags
            __props__.__dict__['description'] = description
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['dns_zones'] = dns_zones
            __props__.__dict__['freeform_tags'] = freeform_tags
            __props__.__dict__['is_used_with_configuration_source_provider'] = is_used_with_configuration_source_provider
            __props__.__dict__['nsg_id_lists'] = nsg_id_lists
            if subnet_id is None and (not opts.urn):
                raise TypeError("Missing required property 'subnet_id'")
            __props__.__dict__['subnet_id'] = subnet_id
            if vcn_id is None and (not opts.urn):
                raise TypeError("Missing required property 'vcn_id'")
            __props__.__dict__['vcn_id'] = vcn_id
            __props__.__dict__['source_ips'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['time_created'] = None
        super(PrivateEndpoint, __self__).__init__('oci:ResourceManager/privateEndpoint:PrivateEndpoint', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, compartment_id: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, is_used_with_configuration_source_provider: Optional[pulumi.Input[bool]]=None, nsg_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, source_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, state: Optional[pulumi.Input[str]]=None, subnet_id: Optional[pulumi.Input[str]]=None, time_created: Optional[pulumi.Input[str]]=None, vcn_id: Optional[pulumi.Input[str]]=None) -> 'PrivateEndpoint':
        """
        Get an existing PrivateEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] description: (Updatable) Description of the private endpoint. Avoid entering confidential information.
        :param pulumi.Input[str] display_name: (Updatable) The private endpoint display name. Avoid entering confidential information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_zones: (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[bool] is_used_with_configuration_source_provider: (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] nsg_id_lists: (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ips: The source IPs which resource manager service will use to connect to customer's network. Automatically assigned by Resource Manager Service.
        :param pulumi.Input[str] state: The current lifecycle state of the private endpoint.
        :param pulumi.Input[str] subnet_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        :param pulumi.Input[str] time_created: The date and time at which the private endpoint was created. Format is defined by RFC3339. Example: `2020-11-25T21:10:29.600Z`
        :param pulumi.Input[str] vcn_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _PrivateEndpointState.__new__(_PrivateEndpointState)
        __props__.__dict__['compartment_id'] = compartment_id
        __props__.__dict__['defined_tags'] = defined_tags
        __props__.__dict__['description'] = description
        __props__.__dict__['display_name'] = display_name
        __props__.__dict__['dns_zones'] = dns_zones
        __props__.__dict__['freeform_tags'] = freeform_tags
        __props__.__dict__['is_used_with_configuration_source_provider'] = is_used_with_configuration_source_provider
        __props__.__dict__['nsg_id_lists'] = nsg_id_lists
        __props__.__dict__['source_ips'] = source_ips
        __props__.__dict__['state'] = state
        __props__.__dict__['subnet_id'] = subnet_id
        __props__.__dict__['time_created'] = time_created
        __props__.__dict__['vcn_id'] = vcn_id
        return PrivateEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing this private endpoint details.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        (Updatable) Description of the private endpoint. Avoid entering confidential information.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        (Updatable) The private endpoint display name. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='dnsZones')
    def dns_zones(self) -> pulumi.Output[Sequence[str]]:
        """
        (Updatable) DNS Proxy forwards any DNS FQDN queries over into the consumer DNS resolver if the DNS FQDN is included in the dns zones list otherwise it goes to service provider VCN resolver.
        """
        return pulumi.get(self, 'dns_zones')

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Free-form tags associated with the resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @property
    @pulumi.getter(name='isUsedWithConfigurationSourceProvider')
    def is_used_with_configuration_source_provider(self) -> pulumi.Output[bool]:
        """
        (Updatable) When `true`, allows the private endpoint to be used with a configuration source provider.
        """
        return pulumi.get(self, 'is_used_with_configuration_source_provider')

    @property
    @pulumi.getter(name='nsgIdLists')
    def nsg_id_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        (Updatable) An array of network security group (NSG) [OCIDs](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) for the private endpoint. Order does not matter.
        """
        return pulumi.get(self, 'nsg_id_lists')

    @property
    @pulumi.getter(name='sourceIps')
    def source_ips(self) -> pulumi.Output[Sequence[str]]:
        """
        The source IPs which resource manager service will use to connect to customer's network. Automatically assigned by Resource Manager Service.
        """
        return pulumi.get(self, 'source_ips')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current lifecycle state of the private endpoint.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='subnetId')
    def subnet_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the subnet within the VCN for the private endpoint.
        """
        return pulumi.get(self, 'subnet_id')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> pulumi.Output[str]:
        """
        The date and time at which the private endpoint was created. Format is defined by RFC3339. Example: `2020-11-25T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='vcnId')
    def vcn_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the VCN for the private endpoint.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'vcn_id')