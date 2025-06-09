import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['LoadBalancerArgs', 'LoadBalancer']

@pulumi.input_type
class LoadBalancerArgs:

    def __init__(__self__, *, address_type: pulumi.Input[str], load_balancer_billing_config: pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs'], load_balancer_edition: pulumi.Input[str], load_balancer_name: pulumi.Input[str], vpc_id: pulumi.Input[str], zone_mappings: pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]], access_log_config: Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]=None, address_allocated_mode: Optional[pulumi.Input[str]]=None, address_ip_version: Optional[pulumi.Input[str]]=None, deletion_protection_enabled: Optional[pulumi.Input[bool]]=None, dry_run: Optional[pulumi.Input[bool]]=None, modification_protection_config: Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]=None, resource_group_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None):
        """
        The set of arguments for constructing a LoadBalancer resource.
        :param pulumi.Input[str] address_type: The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        :param pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs'] load_balancer_billing_config: The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        :param pulumi.Input[str] load_balancer_edition: The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        :param pulumi.Input[str] load_balancer_name: The name of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]] zone_mappings: The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        :param pulumi.Input['LoadBalancerAccessLogConfigArgs'] access_log_config: The Access Logging Configuration Structure. See the following `Block access_log_config`.
        :param pulumi.Input[str] address_allocated_mode: The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        :param pulumi.Input[str] address_ip_version: The IP version. Valid values: `Ipv4`, `DualStack`.
        :param pulumi.Input[bool] deletion_protection_enabled: The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck the API request. Valid values: `true` and `false`.
        :param pulumi.Input['LoadBalancerModificationProtectionConfigArgs'] modification_protection_config: Modify the Protection Configuration. See the following `Block modification_protection_config`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, 'address_type', address_type)
        pulumi.set(__self__, 'load_balancer_billing_config', load_balancer_billing_config)
        pulumi.set(__self__, 'load_balancer_edition', load_balancer_edition)
        pulumi.set(__self__, 'load_balancer_name', load_balancer_name)
        pulumi.set(__self__, 'vpc_id', vpc_id)
        pulumi.set(__self__, 'zone_mappings', zone_mappings)
        if access_log_config is not None:
            pulumi.set(__self__, 'access_log_config', access_log_config)
        if address_allocated_mode is not None:
            pulumi.set(__self__, 'address_allocated_mode', address_allocated_mode)
        if address_ip_version is not None:
            pulumi.set(__self__, 'address_ip_version', address_ip_version)
        if deletion_protection_enabled is not None:
            pulumi.set(__self__, 'deletion_protection_enabled', deletion_protection_enabled)
        if dry_run is not None:
            pulumi.set(__self__, 'dry_run', dry_run)
        if modification_protection_config is not None:
            pulumi.set(__self__, 'modification_protection_config', modification_protection_config)
        if resource_group_id is not None:
            pulumi.set(__self__, 'resource_group_id', resource_group_id)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='addressType')
    def address_type(self) -> pulumi.Input[str]:
        """
        The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        """
        return pulumi.get(self, 'address_type')

    @address_type.setter
    def address_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'address_type', value)

    @property
    @pulumi.getter(name='loadBalancerBillingConfig')
    def load_balancer_billing_config(self) -> pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs']:
        """
        The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        """
        return pulumi.get(self, 'load_balancer_billing_config')

    @load_balancer_billing_config.setter
    def load_balancer_billing_config(self, value: pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs']):
        pulumi.set(self, 'load_balancer_billing_config', value)

    @property
    @pulumi.getter(name='loadBalancerEdition')
    def load_balancer_edition(self) -> pulumi.Input[str]:
        """
        The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        """
        return pulumi.get(self, 'load_balancer_edition')

    @load_balancer_edition.setter
    def load_balancer_edition(self, value: pulumi.Input[str]):
        pulumi.set(self, 'load_balancer_edition', value)

    @property
    @pulumi.getter(name='loadBalancerName')
    def load_balancer_name(self) -> pulumi.Input[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'load_balancer_name')

    @load_balancer_name.setter
    def load_balancer_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'load_balancer_name', value)

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        """
        return pulumi.get(self, 'vpc_id')

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'vpc_id', value)

    @property
    @pulumi.getter(name='zoneMappings')
    def zone_mappings(self) -> pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]]:
        """
        The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        return pulumi.get(self, 'zone_mappings')

    @zone_mappings.setter
    def zone_mappings(self, value: pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]]):
        pulumi.set(self, 'zone_mappings', value)

    @property
    @pulumi.getter(name='accessLogConfig')
    def access_log_config(self) -> Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]:
        """
        The Access Logging Configuration Structure. See the following `Block access_log_config`.
        """
        return pulumi.get(self, 'access_log_config')

    @access_log_config.setter
    def access_log_config(self, value: Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]):
        pulumi.set(self, 'access_log_config', value)

    @property
    @pulumi.getter(name='addressAllocatedMode')
    def address_allocated_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        """
        return pulumi.get(self, 'address_allocated_mode')

    @address_allocated_mode.setter
    def address_allocated_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_allocated_mode', value)

    @property
    @pulumi.getter(name='addressIpVersion')
    def address_ip_version(self) -> Optional[pulumi.Input[str]]:
        """
        The IP version. Valid values: `Ipv4`, `DualStack`.
        """
        return pulumi.get(self, 'address_ip_version')

    @address_ip_version.setter
    def address_ip_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_ip_version', value)

    @property
    @pulumi.getter(name='deletionProtectionEnabled')
    def deletion_protection_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        """
        return pulumi.get(self, 'deletion_protection_enabled')

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'deletion_protection_enabled', value)

    @property
    @pulumi.getter(name='dryRun')
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to precheck the API request. Valid values: `true` and `false`.
        """
        return pulumi.get(self, 'dry_run')

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'dry_run', value)

    @property
    @pulumi.getter(name='modificationProtectionConfig')
    def modification_protection_config(self) -> Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]:
        """
        Modify the Protection Configuration. See the following `Block modification_protection_config`.
        """
        return pulumi.get(self, 'modification_protection_config')

    @modification_protection_config.setter
    def modification_protection_config(self, value: Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]):
        pulumi.set(self, 'modification_protection_config', value)

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, 'resource_group_id')

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_id', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'tags', value)

@pulumi.input_type
class _LoadBalancerState:

    def __init__(__self__, *, access_log_config: Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]=None, address_allocated_mode: Optional[pulumi.Input[str]]=None, address_ip_version: Optional[pulumi.Input[str]]=None, address_type: Optional[pulumi.Input[str]]=None, deletion_protection_enabled: Optional[pulumi.Input[bool]]=None, dns_name: Optional[pulumi.Input[str]]=None, dry_run: Optional[pulumi.Input[bool]]=None, load_balancer_billing_config: Optional[pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs']]=None, load_balancer_edition: Optional[pulumi.Input[str]]=None, load_balancer_name: Optional[pulumi.Input[str]]=None, modification_protection_config: Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]=None, resource_group_id: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, vpc_id: Optional[pulumi.Input[str]]=None, zone_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]]]=None):
        """
        Input properties used for looking up and filtering LoadBalancer resources.
        :param pulumi.Input['LoadBalancerAccessLogConfigArgs'] access_log_config: The Access Logging Configuration Structure. See the following `Block access_log_config`.
        :param pulumi.Input[str] address_allocated_mode: The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        :param pulumi.Input[str] address_ip_version: The IP version. Valid values: `Ipv4`, `DualStack`.
        :param pulumi.Input[str] address_type: The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        :param pulumi.Input[bool] deletion_protection_enabled: The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        :param pulumi.Input[str] dns_name: The domain name of the ALB instance. **NOTE:** Available in v1.158.0+.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck the API request. Valid values: `true` and `false`.
        :param pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs'] load_balancer_billing_config: The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        :param pulumi.Input[str] load_balancer_edition: The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        :param pulumi.Input[str] load_balancer_name: The name of the resource.
        :param pulumi.Input['LoadBalancerModificationProtectionConfigArgs'] modification_protection_config: Modify the Protection Configuration. See the following `Block modification_protection_config`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[str] status: Specifies whether to enable the configuration read-only mode for the ALB instance. Valid values: `NonProtection` and `ConsoleProtection`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]] zone_mappings: The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        if access_log_config is not None:
            pulumi.set(__self__, 'access_log_config', access_log_config)
        if address_allocated_mode is not None:
            pulumi.set(__self__, 'address_allocated_mode', address_allocated_mode)
        if address_ip_version is not None:
            pulumi.set(__self__, 'address_ip_version', address_ip_version)
        if address_type is not None:
            pulumi.set(__self__, 'address_type', address_type)
        if deletion_protection_enabled is not None:
            pulumi.set(__self__, 'deletion_protection_enabled', deletion_protection_enabled)
        if dns_name is not None:
            pulumi.set(__self__, 'dns_name', dns_name)
        if dry_run is not None:
            pulumi.set(__self__, 'dry_run', dry_run)
        if load_balancer_billing_config is not None:
            pulumi.set(__self__, 'load_balancer_billing_config', load_balancer_billing_config)
        if load_balancer_edition is not None:
            pulumi.set(__self__, 'load_balancer_edition', load_balancer_edition)
        if load_balancer_name is not None:
            pulumi.set(__self__, 'load_balancer_name', load_balancer_name)
        if modification_protection_config is not None:
            pulumi.set(__self__, 'modification_protection_config', modification_protection_config)
        if resource_group_id is not None:
            pulumi.set(__self__, 'resource_group_id', resource_group_id)
        if status is not None:
            pulumi.set(__self__, 'status', status)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if vpc_id is not None:
            pulumi.set(__self__, 'vpc_id', vpc_id)
        if zone_mappings is not None:
            pulumi.set(__self__, 'zone_mappings', zone_mappings)

    @property
    @pulumi.getter(name='accessLogConfig')
    def access_log_config(self) -> Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]:
        """
        The Access Logging Configuration Structure. See the following `Block access_log_config`.
        """
        return pulumi.get(self, 'access_log_config')

    @access_log_config.setter
    def access_log_config(self, value: Optional[pulumi.Input['LoadBalancerAccessLogConfigArgs']]):
        pulumi.set(self, 'access_log_config', value)

    @property
    @pulumi.getter(name='addressAllocatedMode')
    def address_allocated_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        """
        return pulumi.get(self, 'address_allocated_mode')

    @address_allocated_mode.setter
    def address_allocated_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_allocated_mode', value)

    @property
    @pulumi.getter(name='addressIpVersion')
    def address_ip_version(self) -> Optional[pulumi.Input[str]]:
        """
        The IP version. Valid values: `Ipv4`, `DualStack`.
        """
        return pulumi.get(self, 'address_ip_version')

    @address_ip_version.setter
    def address_ip_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_ip_version', value)

    @property
    @pulumi.getter(name='addressType')
    def address_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        """
        return pulumi.get(self, 'address_type')

    @address_type.setter
    def address_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_type', value)

    @property
    @pulumi.getter(name='deletionProtectionEnabled')
    def deletion_protection_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        """
        return pulumi.get(self, 'deletion_protection_enabled')

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'deletion_protection_enabled', value)

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name of the ALB instance. **NOTE:** Available in v1.158.0+.
        """
        return pulumi.get(self, 'dns_name')

    @dns_name.setter
    def dns_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dns_name', value)

    @property
    @pulumi.getter(name='dryRun')
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to precheck the API request. Valid values: `true` and `false`.
        """
        return pulumi.get(self, 'dry_run')

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'dry_run', value)

    @property
    @pulumi.getter(name='loadBalancerBillingConfig')
    def load_balancer_billing_config(self) -> Optional[pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs']]:
        """
        The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        """
        return pulumi.get(self, 'load_balancer_billing_config')

    @load_balancer_billing_config.setter
    def load_balancer_billing_config(self, value: Optional[pulumi.Input['LoadBalancerLoadBalancerBillingConfigArgs']]):
        pulumi.set(self, 'load_balancer_billing_config', value)

    @property
    @pulumi.getter(name='loadBalancerEdition')
    def load_balancer_edition(self) -> Optional[pulumi.Input[str]]:
        """
        The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        """
        return pulumi.get(self, 'load_balancer_edition')

    @load_balancer_edition.setter
    def load_balancer_edition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'load_balancer_edition', value)

    @property
    @pulumi.getter(name='loadBalancerName')
    def load_balancer_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'load_balancer_name')

    @load_balancer_name.setter
    def load_balancer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'load_balancer_name', value)

    @property
    @pulumi.getter(name='modificationProtectionConfig')
    def modification_protection_config(self) -> Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]:
        """
        Modify the Protection Configuration. See the following `Block modification_protection_config`.
        """
        return pulumi.get(self, 'modification_protection_config')

    @modification_protection_config.setter
    def modification_protection_config(self, value: Optional[pulumi.Input['LoadBalancerModificationProtectionConfigArgs']]):
        pulumi.set(self, 'modification_protection_config', value)

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, 'resource_group_id')

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_id', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to enable the configuration read-only mode for the ALB instance. Valid values: `NonProtection` and `ConsoleProtection`.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'status', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        """
        return pulumi.get(self, 'vpc_id')

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vpc_id', value)

    @property
    @pulumi.getter(name='zoneMappings')
    def zone_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]]]:
        """
        The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        return pulumi.get(self, 'zone_mappings')

    @zone_mappings.setter
    def zone_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerZoneMappingArgs']]]]):
        pulumi.set(self, 'zone_mappings', value)

class LoadBalancer(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, access_log_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerAccessLogConfigArgs']]]=None, address_allocated_mode: Optional[pulumi.Input[str]]=None, address_ip_version: Optional[pulumi.Input[str]]=None, address_type: Optional[pulumi.Input[str]]=None, deletion_protection_enabled: Optional[pulumi.Input[bool]]=None, dry_run: Optional[pulumi.Input[bool]]=None, load_balancer_billing_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerLoadBalancerBillingConfigArgs']]]=None, load_balancer_edition: Optional[pulumi.Input[str]]=None, load_balancer_name: Optional[pulumi.Input[str]]=None, modification_protection_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerModificationProtectionConfigArgs']]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, vpc_id: Optional[pulumi.Input[str]]=None, zone_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerZoneMappingArgs']]]]]=None, __props__=None):
        """
        Provides a ALB Load Balancer resource.

        For information about ALB Load Balancer and how to use it, see [What is Load Balancer](https://www.alibabacloud.com/help/doc-detail/197341.htm).

        > **NOTE:** Available in v1.132.0+.

        ## Import

        ALB Load Balancer can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:alb/loadBalancer:LoadBalancer example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['LoadBalancerAccessLogConfigArgs']] access_log_config: The Access Logging Configuration Structure. See the following `Block access_log_config`.
        :param pulumi.Input[str] address_allocated_mode: The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        :param pulumi.Input[str] address_ip_version: The IP version. Valid values: `Ipv4`, `DualStack`.
        :param pulumi.Input[str] address_type: The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        :param pulumi.Input[bool] deletion_protection_enabled: The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck the API request. Valid values: `true` and `false`.
        :param pulumi.Input[pulumi.InputType['LoadBalancerLoadBalancerBillingConfigArgs']] load_balancer_billing_config: The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        :param pulumi.Input[str] load_balancer_edition: The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        :param pulumi.Input[str] load_balancer_name: The name of the resource.
        :param pulumi.Input[pulumi.InputType['LoadBalancerModificationProtectionConfigArgs']] modification_protection_config: Modify the Protection Configuration. See the following `Block modification_protection_config`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerZoneMappingArgs']]]] zone_mappings: The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: LoadBalancerArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a ALB Load Balancer resource.

        For information about ALB Load Balancer and how to use it, see [What is Load Balancer](https://www.alibabacloud.com/help/doc-detail/197341.htm).

        > **NOTE:** Available in v1.132.0+.

        ## Import

        ALB Load Balancer can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:alb/loadBalancer:LoadBalancer example <id>
        ```

        :param str resource_name: The name of the resource.
        :param LoadBalancerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, access_log_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerAccessLogConfigArgs']]]=None, address_allocated_mode: Optional[pulumi.Input[str]]=None, address_ip_version: Optional[pulumi.Input[str]]=None, address_type: Optional[pulumi.Input[str]]=None, deletion_protection_enabled: Optional[pulumi.Input[bool]]=None, dry_run: Optional[pulumi.Input[bool]]=None, load_balancer_billing_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerLoadBalancerBillingConfigArgs']]]=None, load_balancer_edition: Optional[pulumi.Input[str]]=None, load_balancer_name: Optional[pulumi.Input[str]]=None, modification_protection_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerModificationProtectionConfigArgs']]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, vpc_id: Optional[pulumi.Input[str]]=None, zone_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerZoneMappingArgs']]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancerArgs.__new__(LoadBalancerArgs)
            __props__.__dict__['access_log_config'] = access_log_config
            __props__.__dict__['address_allocated_mode'] = address_allocated_mode
            __props__.__dict__['address_ip_version'] = address_ip_version
            if address_type is None and (not opts.urn):
                raise TypeError("Missing required property 'address_type'")
            __props__.__dict__['address_type'] = address_type
            __props__.__dict__['deletion_protection_enabled'] = deletion_protection_enabled
            __props__.__dict__['dry_run'] = dry_run
            if load_balancer_billing_config is None and (not opts.urn):
                raise TypeError("Missing required property 'load_balancer_billing_config'")
            __props__.__dict__['load_balancer_billing_config'] = load_balancer_billing_config
            if load_balancer_edition is None and (not opts.urn):
                raise TypeError("Missing required property 'load_balancer_edition'")
            __props__.__dict__['load_balancer_edition'] = load_balancer_edition
            if load_balancer_name is None and (not opts.urn):
                raise TypeError("Missing required property 'load_balancer_name'")
            __props__.__dict__['load_balancer_name'] = load_balancer_name
            __props__.__dict__['modification_protection_config'] = modification_protection_config
            __props__.__dict__['resource_group_id'] = resource_group_id
            __props__.__dict__['tags'] = tags
            if vpc_id is None and (not opts.urn):
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__['vpc_id'] = vpc_id
            if zone_mappings is None and (not opts.urn):
                raise TypeError("Missing required property 'zone_mappings'")
            __props__.__dict__['zone_mappings'] = zone_mappings
            __props__.__dict__['dns_name'] = None
            __props__.__dict__['status'] = None
        super(LoadBalancer, __self__).__init__('alicloud:alb/loadBalancer:LoadBalancer', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, access_log_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerAccessLogConfigArgs']]]=None, address_allocated_mode: Optional[pulumi.Input[str]]=None, address_ip_version: Optional[pulumi.Input[str]]=None, address_type: Optional[pulumi.Input[str]]=None, deletion_protection_enabled: Optional[pulumi.Input[bool]]=None, dns_name: Optional[pulumi.Input[str]]=None, dry_run: Optional[pulumi.Input[bool]]=None, load_balancer_billing_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerLoadBalancerBillingConfigArgs']]]=None, load_balancer_edition: Optional[pulumi.Input[str]]=None, load_balancer_name: Optional[pulumi.Input[str]]=None, modification_protection_config: Optional[pulumi.Input[pulumi.InputType['LoadBalancerModificationProtectionConfigArgs']]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, vpc_id: Optional[pulumi.Input[str]]=None, zone_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerZoneMappingArgs']]]]]=None) -> 'LoadBalancer':
        """
        Get an existing LoadBalancer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['LoadBalancerAccessLogConfigArgs']] access_log_config: The Access Logging Configuration Structure. See the following `Block access_log_config`.
        :param pulumi.Input[str] address_allocated_mode: The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        :param pulumi.Input[str] address_ip_version: The IP version. Valid values: `Ipv4`, `DualStack`.
        :param pulumi.Input[str] address_type: The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        :param pulumi.Input[bool] deletion_protection_enabled: The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        :param pulumi.Input[str] dns_name: The domain name of the ALB instance. **NOTE:** Available in v1.158.0+.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck the API request. Valid values: `true` and `false`.
        :param pulumi.Input[pulumi.InputType['LoadBalancerLoadBalancerBillingConfigArgs']] load_balancer_billing_config: The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        :param pulumi.Input[str] load_balancer_edition: The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        :param pulumi.Input[str] load_balancer_name: The name of the resource.
        :param pulumi.Input[pulumi.InputType['LoadBalancerModificationProtectionConfigArgs']] modification_protection_config: Modify the Protection Configuration. See the following `Block modification_protection_config`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[str] status: Specifies whether to enable the configuration read-only mode for the ALB instance. Valid values: `NonProtection` and `ConsoleProtection`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerZoneMappingArgs']]]] zone_mappings: The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _LoadBalancerState.__new__(_LoadBalancerState)
        __props__.__dict__['access_log_config'] = access_log_config
        __props__.__dict__['address_allocated_mode'] = address_allocated_mode
        __props__.__dict__['address_ip_version'] = address_ip_version
        __props__.__dict__['address_type'] = address_type
        __props__.__dict__['deletion_protection_enabled'] = deletion_protection_enabled
        __props__.__dict__['dns_name'] = dns_name
        __props__.__dict__['dry_run'] = dry_run
        __props__.__dict__['load_balancer_billing_config'] = load_balancer_billing_config
        __props__.__dict__['load_balancer_edition'] = load_balancer_edition
        __props__.__dict__['load_balancer_name'] = load_balancer_name
        __props__.__dict__['modification_protection_config'] = modification_protection_config
        __props__.__dict__['resource_group_id'] = resource_group_id
        __props__.__dict__['status'] = status
        __props__.__dict__['tags'] = tags
        __props__.__dict__['vpc_id'] = vpc_id
        __props__.__dict__['zone_mappings'] = zone_mappings
        return LoadBalancer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='accessLogConfig')
    def access_log_config(self) -> pulumi.Output[Optional['outputs.LoadBalancerAccessLogConfig']]:
        """
        The Access Logging Configuration Structure. See the following `Block access_log_config`.
        """
        return pulumi.get(self, 'access_log_config')

    @property
    @pulumi.getter(name='addressAllocatedMode')
    def address_allocated_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The method in which IP addresses are assigned. Valid values: `Fixed` and `Dynamic`. Default value: `Dynamic`.
        """
        return pulumi.get(self, 'address_allocated_mode')

    @property
    @pulumi.getter(name='addressIpVersion')
    def address_ip_version(self) -> pulumi.Output[str]:
        """
        The IP version. Valid values: `Ipv4`, `DualStack`.
        """
        return pulumi.get(self, 'address_ip_version')

    @property
    @pulumi.getter(name='addressType')
    def address_type(self) -> pulumi.Output[str]:
        """
        The type of IP address that the ALB instance uses to provide services. Valid values: `Intranet`, `Internet`. **NOTE:** From version 1.193.1, `address_type` can be modified.
        """
        return pulumi.get(self, 'address_type')

    @property
    @pulumi.getter(name='deletionProtectionEnabled')
    def deletion_protection_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The deletion protection enabled. Valid values: `true` and `false`. Default value: `false`.
        """
        return pulumi.get(self, 'deletion_protection_enabled')

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> pulumi.Output[str]:
        """
        The domain name of the ALB instance. **NOTE:** Available in v1.158.0+.
        """
        return pulumi.get(self, 'dns_name')

    @property
    @pulumi.getter(name='dryRun')
    def dry_run(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to precheck the API request. Valid values: `true` and `false`.
        """
        return pulumi.get(self, 'dry_run')

    @property
    @pulumi.getter(name='loadBalancerBillingConfig')
    def load_balancer_billing_config(self) -> pulumi.Output['outputs.LoadBalancerLoadBalancerBillingConfig']:
        """
        The configuration of the billing method. See the following `Block load_balancer_billing_config`.
        """
        return pulumi.get(self, 'load_balancer_billing_config')

    @property
    @pulumi.getter(name='loadBalancerEdition')
    def load_balancer_edition(self) -> pulumi.Output[str]:
        """
        The edition of the ALB instance. Different editions have different limits and billing methods. Valid values: `Basic`, `Standard` and `StandardWithWaf`(Available in v1.193.1+).
        """
        return pulumi.get(self, 'load_balancer_edition')

    @property
    @pulumi.getter(name='loadBalancerName')
    def load_balancer_name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'load_balancer_name')

    @property
    @pulumi.getter(name='modificationProtectionConfig')
    def modification_protection_config(self) -> pulumi.Output['outputs.LoadBalancerModificationProtectionConfig']:
        """
        Modify the Protection Configuration. See the following `Block modification_protection_config`.
        """
        return pulumi.get(self, 'modification_protection_config')

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, 'resource_group_id')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Specifies whether to enable the configuration read-only mode for the ALB instance. Valid values: `NonProtection` and `ConsoleProtection`.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the virtual private cloud (VPC) where the ALB instance is deployed.
        """
        return pulumi.get(self, 'vpc_id')

    @property
    @pulumi.getter(name='zoneMappings')
    def zone_mappings(self) -> pulumi.Output[Sequence['outputs.LoadBalancerZoneMapping']]:
        """
        The zones and vSwitches. You must specify at least two zones. See the following `Block zone_mappings`.
        """
        return pulumi.get(self, 'zone_mappings')