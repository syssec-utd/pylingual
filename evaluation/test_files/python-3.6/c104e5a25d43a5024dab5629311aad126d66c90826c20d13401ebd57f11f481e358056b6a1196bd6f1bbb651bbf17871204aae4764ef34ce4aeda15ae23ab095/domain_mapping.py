import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['DomainMappingArgs', 'DomainMapping']

@pulumi.input_type
class DomainMappingArgs:

    def __init__(__self__, *, app_id: pulumi.Input[str], id: Optional[pulumi.Input[str]]=None, override_strategy: Optional[pulumi.Input[str]]=None, ssl_settings: Optional[pulumi.Input['SslSettingsArgs']]=None):
        """
        The set of arguments for constructing a DomainMapping resource.
        :param pulumi.Input[str] id: Relative name of the domain serving the application. Example: example.com.
        :param pulumi.Input[str] override_strategy: Whether the domain creation should override any existing mappings for this domain. By default, overrides are rejected.
        :param pulumi.Input['SslSettingsArgs'] ssl_settings: SSL configuration for this domain. If unconfigured, this domain will not serve with SSL.
        """
        pulumi.set(__self__, 'app_id', app_id)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if override_strategy is not None:
            pulumi.set(__self__, 'override_strategy', override_strategy)
        if ssl_settings is not None:
            pulumi.set(__self__, 'ssl_settings', ssl_settings)

    @property
    @pulumi.getter(name='appId')
    def app_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'app_id')

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'app_id', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Relative name of the domain serving the application. Example: example.com.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter(name='overrideStrategy')
    def override_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the domain creation should override any existing mappings for this domain. By default, overrides are rejected.
        """
        return pulumi.get(self, 'override_strategy')

    @override_strategy.setter
    def override_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'override_strategy', value)

    @property
    @pulumi.getter(name='sslSettings')
    def ssl_settings(self) -> Optional[pulumi.Input['SslSettingsArgs']]:
        """
        SSL configuration for this domain. If unconfigured, this domain will not serve with SSL.
        """
        return pulumi.get(self, 'ssl_settings')

    @ssl_settings.setter
    def ssl_settings(self, value: Optional[pulumi.Input['SslSettingsArgs']]):
        pulumi.set(self, 'ssl_settings', value)

class DomainMapping(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_id: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, override_strategy: Optional[pulumi.Input[str]]=None, ssl_settings: Optional[pulumi.Input[pulumi.InputType['SslSettingsArgs']]]=None, __props__=None):
        """
        Maps a domain to an application. A user must be authorized to administer a domain in order to map it to an application. For a list of available authorized domains, see AuthorizedDomains.ListAuthorizedDomains.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Relative name of the domain serving the application. Example: example.com.
        :param pulumi.Input[str] override_strategy: Whether the domain creation should override any existing mappings for this domain. By default, overrides are rejected.
        :param pulumi.Input[pulumi.InputType['SslSettingsArgs']] ssl_settings: SSL configuration for this domain. If unconfigured, this domain will not serve with SSL.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DomainMappingArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Maps a domain to an application. A user must be authorized to administer a domain in order to map it to an application. For a list of available authorized domains, see AuthorizedDomains.ListAuthorizedDomains.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param DomainMappingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(DomainMappingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_id: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, override_strategy: Optional[pulumi.Input[str]]=None, ssl_settings: Optional[pulumi.Input[pulumi.InputType['SslSettingsArgs']]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        else:
            opts = copy.copy(opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainMappingArgs.__new__(DomainMappingArgs)
            if app_id is None and (not opts.urn):
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__['app_id'] = app_id
            __props__.__dict__['id'] = id
            __props__.__dict__['override_strategy'] = override_strategy
            __props__.__dict__['ssl_settings'] = ssl_settings
            __props__.__dict__['name'] = None
            __props__.__dict__['resource_records'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['app_id'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DomainMapping, __self__).__init__('google-native:appengine/v1:DomainMapping', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DomainMapping':
        """
        Get an existing DomainMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DomainMappingArgs.__new__(DomainMappingArgs)
        __props__.__dict__['app_id'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['override_strategy'] = None
        __props__.__dict__['resource_records'] = None
        __props__.__dict__['ssl_settings'] = None
        return DomainMapping(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='appId')
    def app_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'app_id')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Full path to the DomainMapping resource in the API. Example: apps/myapp/domainMapping/example.com.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='overrideStrategy')
    def override_strategy(self) -> pulumi.Output[Optional[str]]:
        """
        Whether the domain creation should override any existing mappings for this domain. By default, overrides are rejected.
        """
        return pulumi.get(self, 'override_strategy')

    @property
    @pulumi.getter(name='resourceRecords')
    def resource_records(self) -> pulumi.Output[Sequence['outputs.ResourceRecordResponse']]:
        """
        The resource records required to configure this domain mapping. These records must be added to the domain's DNS configuration in order to serve the application via this domain mapping.
        """
        return pulumi.get(self, 'resource_records')

    @property
    @pulumi.getter(name='sslSettings')
    def ssl_settings(self) -> pulumi.Output['outputs.SslSettingsResponse']:
        """
        SSL configuration for this domain. If unconfigured, this domain will not serve with SSL.
        """
        return pulumi.get(self, 'ssl_settings')