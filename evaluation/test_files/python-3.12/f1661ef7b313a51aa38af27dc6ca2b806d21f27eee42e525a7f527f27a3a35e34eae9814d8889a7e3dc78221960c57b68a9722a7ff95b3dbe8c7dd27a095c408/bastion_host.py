import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['BastionHostArgs', 'BastionHost']

@pulumi.input_type
class BastionHostArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], bastion_host_name: Optional[pulumi.Input[str]]=None, disable_copy_paste: Optional[pulumi.Input[bool]]=None, dns_name: Optional[pulumi.Input[str]]=None, enable_file_copy: Optional[pulumi.Input[bool]]=None, enable_ip_connect: Optional[pulumi.Input[bool]]=None, enable_shareable_link: Optional[pulumi.Input[bool]]=None, enable_tunneling: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['BastionHostIPConfigurationArgs']]]]=None, location: Optional[pulumi.Input[str]]=None, scale_units: Optional[pulumi.Input[int]]=None, sku: Optional[pulumi.Input['SkuArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a BastionHost resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] bastion_host_name: The name of the Bastion Host.
        :param pulumi.Input[bool] disable_copy_paste: Enable/Disable Copy/Paste feature of the Bastion Host resource.
        :param pulumi.Input[str] dns_name: FQDN for the endpoint on which bastion host is accessible.
        :param pulumi.Input[bool] enable_file_copy: Enable/Disable File Copy feature of the Bastion Host resource.
        :param pulumi.Input[bool] enable_ip_connect: Enable/Disable IP Connect feature of the Bastion Host resource.
        :param pulumi.Input[bool] enable_shareable_link: Enable/Disable Shareable Link of the Bastion Host resource.
        :param pulumi.Input[bool] enable_tunneling: Enable/Disable Tunneling feature of the Bastion Host resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['BastionHostIPConfigurationArgs']]] ip_configurations: IP configuration of the Bastion Host resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[int] scale_units: The scale units for the Bastion Host resource.
        :param pulumi.Input['SkuArgs'] sku: The sku of this Bastion Host.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if bastion_host_name is not None:
            pulumi.set(__self__, 'bastion_host_name', bastion_host_name)
        if disable_copy_paste is None:
            disable_copy_paste = False
        if disable_copy_paste is not None:
            pulumi.set(__self__, 'disable_copy_paste', disable_copy_paste)
        if dns_name is not None:
            pulumi.set(__self__, 'dns_name', dns_name)
        if enable_file_copy is None:
            enable_file_copy = False
        if enable_file_copy is not None:
            pulumi.set(__self__, 'enable_file_copy', enable_file_copy)
        if enable_ip_connect is None:
            enable_ip_connect = False
        if enable_ip_connect is not None:
            pulumi.set(__self__, 'enable_ip_connect', enable_ip_connect)
        if enable_shareable_link is None:
            enable_shareable_link = False
        if enable_shareable_link is not None:
            pulumi.set(__self__, 'enable_shareable_link', enable_shareable_link)
        if enable_tunneling is None:
            enable_tunneling = False
        if enable_tunneling is not None:
            pulumi.set(__self__, 'enable_tunneling', enable_tunneling)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if ip_configurations is not None:
            pulumi.set(__self__, 'ip_configurations', ip_configurations)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if scale_units is not None:
            pulumi.set(__self__, 'scale_units', scale_units)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='bastionHostName')
    def bastion_host_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Bastion Host.
        """
        return pulumi.get(self, 'bastion_host_name')

    @bastion_host_name.setter
    def bastion_host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'bastion_host_name', value)

    @property
    @pulumi.getter(name='disableCopyPaste')
    def disable_copy_paste(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/Disable Copy/Paste feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'disable_copy_paste')

    @disable_copy_paste.setter
    def disable_copy_paste(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'disable_copy_paste', value)

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> Optional[pulumi.Input[str]]:
        """
        FQDN for the endpoint on which bastion host is accessible.
        """
        return pulumi.get(self, 'dns_name')

    @dns_name.setter
    def dns_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dns_name', value)

    @property
    @pulumi.getter(name='enableFileCopy')
    def enable_file_copy(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/Disable File Copy feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_file_copy')

    @enable_file_copy.setter
    def enable_file_copy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_file_copy', value)

    @property
    @pulumi.getter(name='enableIpConnect')
    def enable_ip_connect(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/Disable IP Connect feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_ip_connect')

    @enable_ip_connect.setter
    def enable_ip_connect(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_ip_connect', value)

    @property
    @pulumi.getter(name='enableShareableLink')
    def enable_shareable_link(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/Disable Shareable Link of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_shareable_link')

    @enable_shareable_link.setter
    def enable_shareable_link(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_shareable_link', value)

    @property
    @pulumi.getter(name='enableTunneling')
    def enable_tunneling(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/Disable Tunneling feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_tunneling')

    @enable_tunneling.setter
    def enable_tunneling(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_tunneling', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter(name='ipConfigurations')
    def ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BastionHostIPConfigurationArgs']]]]:
        """
        IP configuration of the Bastion Host resource.
        """
        return pulumi.get(self, 'ip_configurations')

    @ip_configurations.setter
    def ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BastionHostIPConfigurationArgs']]]]):
        pulumi.set(self, 'ip_configurations', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='scaleUnits')
    def scale_units(self) -> Optional[pulumi.Input[int]]:
        """
        The scale units for the Bastion Host resource.
        """
        return pulumi.get(self, 'scale_units')

    @scale_units.setter
    def scale_units(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'scale_units', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The sku of this Bastion Host.
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class BastionHost(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, bastion_host_name: Optional[pulumi.Input[str]]=None, disable_copy_paste: Optional[pulumi.Input[bool]]=None, dns_name: Optional[pulumi.Input[str]]=None, enable_file_copy: Optional[pulumi.Input[bool]]=None, enable_ip_connect: Optional[pulumi.Input[bool]]=None, enable_shareable_link: Optional[pulumi.Input[bool]]=None, enable_tunneling: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BastionHostIPConfigurationArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scale_units: Optional[pulumi.Input[int]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Bastion Host resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bastion_host_name: The name of the Bastion Host.
        :param pulumi.Input[bool] disable_copy_paste: Enable/Disable Copy/Paste feature of the Bastion Host resource.
        :param pulumi.Input[str] dns_name: FQDN for the endpoint on which bastion host is accessible.
        :param pulumi.Input[bool] enable_file_copy: Enable/Disable File Copy feature of the Bastion Host resource.
        :param pulumi.Input[bool] enable_ip_connect: Enable/Disable IP Connect feature of the Bastion Host resource.
        :param pulumi.Input[bool] enable_shareable_link: Enable/Disable Shareable Link of the Bastion Host resource.
        :param pulumi.Input[bool] enable_tunneling: Enable/Disable Tunneling feature of the Bastion Host resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BastionHostIPConfigurationArgs']]]] ip_configurations: IP configuration of the Bastion Host resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[int] scale_units: The scale units for the Bastion Host resource.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of this Bastion Host.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: BastionHostArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Bastion Host resource.

        :param str resource_name: The name of the resource.
        :param BastionHostArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BastionHostArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, bastion_host_name: Optional[pulumi.Input[str]]=None, disable_copy_paste: Optional[pulumi.Input[bool]]=None, dns_name: Optional[pulumi.Input[str]]=None, enable_file_copy: Optional[pulumi.Input[bool]]=None, enable_ip_connect: Optional[pulumi.Input[bool]]=None, enable_shareable_link: Optional[pulumi.Input[bool]]=None, enable_tunneling: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BastionHostIPConfigurationArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scale_units: Optional[pulumi.Input[int]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BastionHostArgs.__new__(BastionHostArgs)
            __props__.__dict__['bastion_host_name'] = bastion_host_name
            if disable_copy_paste is None:
                disable_copy_paste = False
            __props__.__dict__['disable_copy_paste'] = disable_copy_paste
            __props__.__dict__['dns_name'] = dns_name
            if enable_file_copy is None:
                enable_file_copy = False
            __props__.__dict__['enable_file_copy'] = enable_file_copy
            if enable_ip_connect is None:
                enable_ip_connect = False
            __props__.__dict__['enable_ip_connect'] = enable_ip_connect
            if enable_shareable_link is None:
                enable_shareable_link = False
            __props__.__dict__['enable_shareable_link'] = enable_shareable_link
            if enable_tunneling is None:
                enable_tunneling = False
            __props__.__dict__['enable_tunneling'] = enable_tunneling
            __props__.__dict__['id'] = id
            __props__.__dict__['ip_configurations'] = ip_configurations
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['scale_units'] = scale_units
            __props__.__dict__['sku'] = sku
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:BastionHost'), pulumi.Alias(type_='azure-native:network/v20190401:BastionHost'), pulumi.Alias(type_='azure-native:network/v20190601:BastionHost'), pulumi.Alias(type_='azure-native:network/v20190701:BastionHost'), pulumi.Alias(type_='azure-native:network/v20190801:BastionHost'), pulumi.Alias(type_='azure-native:network/v20190901:BastionHost'), pulumi.Alias(type_='azure-native:network/v20191101:BastionHost'), pulumi.Alias(type_='azure-native:network/v20191201:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200301:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200401:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200501:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200601:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200701:BastionHost'), pulumi.Alias(type_='azure-native:network/v20200801:BastionHost'), pulumi.Alias(type_='azure-native:network/v20201101:BastionHost'), pulumi.Alias(type_='azure-native:network/v20210201:BastionHost'), pulumi.Alias(type_='azure-native:network/v20210301:BastionHost'), pulumi.Alias(type_='azure-native:network/v20210801:BastionHost'), pulumi.Alias(type_='azure-native:network/v20220101:BastionHost'), pulumi.Alias(type_='azure-native:network/v20220501:BastionHost'), pulumi.Alias(type_='azure-native:network/v20220701:BastionHost'), pulumi.Alias(type_='azure-native:network/v20220901:BastionHost')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BastionHost, __self__).__init__('azure-native:network/v20210501:BastionHost', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'BastionHost':
        """
        Get an existing BastionHost resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = BastionHostArgs.__new__(BastionHostArgs)
        __props__.__dict__['disable_copy_paste'] = None
        __props__.__dict__['dns_name'] = None
        __props__.__dict__['enable_file_copy'] = None
        __props__.__dict__['enable_ip_connect'] = None
        __props__.__dict__['enable_shareable_link'] = None
        __props__.__dict__['enable_tunneling'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['ip_configurations'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['scale_units'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return BastionHost(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='disableCopyPaste')
    def disable_copy_paste(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable/Disable Copy/Paste feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'disable_copy_paste')

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> pulumi.Output[Optional[str]]:
        """
        FQDN for the endpoint on which bastion host is accessible.
        """
        return pulumi.get(self, 'dns_name')

    @property
    @pulumi.getter(name='enableFileCopy')
    def enable_file_copy(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable/Disable File Copy feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_file_copy')

    @property
    @pulumi.getter(name='enableIpConnect')
    def enable_ip_connect(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable/Disable IP Connect feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_ip_connect')

    @property
    @pulumi.getter(name='enableShareableLink')
    def enable_shareable_link(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable/Disable Shareable Link of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_shareable_link')

    @property
    @pulumi.getter(name='enableTunneling')
    def enable_tunneling(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable/Disable Tunneling feature of the Bastion Host resource.
        """
        return pulumi.get(self, 'enable_tunneling')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='ipConfigurations')
    def ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.BastionHostIPConfigurationResponse']]]:
        """
        IP configuration of the Bastion Host resource.
        """
        return pulumi.get(self, 'ip_configurations')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the bastion host resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='scaleUnits')
    def scale_units(self) -> pulumi.Output[Optional[int]]:
        """
        The scale units for the Bastion Host resource.
        """
        return pulumi.get(self, 'scale_units')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of this Bastion Host.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')