import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ConnectedRegistryArgs', 'ConnectedRegistry']

@pulumi.input_type
class ConnectedRegistryArgs:

    def __init__(__self__, *, mode: pulumi.Input[Union[str, 'ConnectedRegistryMode']], parent: pulumi.Input['ParentPropertiesArgs'], registry_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], client_token_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, connected_registry_name: Optional[pulumi.Input[str]]=None, logging: Optional[pulumi.Input['LoggingPropertiesArgs']]=None, notifications_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ConnectedRegistry resource.
        :param pulumi.Input[Union[str, 'ConnectedRegistryMode']] mode: The mode of the connected registry resource that indicates the permissions of the registry.
        :param pulumi.Input['ParentPropertiesArgs'] parent: The parent of the connected registry.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_token_ids: The list of the ACR token resource IDs used to authenticate clients to the connected registry.
        :param pulumi.Input[str] connected_registry_name: The name of the connected registry.
        :param pulumi.Input['LoggingPropertiesArgs'] logging: The logging properties of the connected registry.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notifications_list: The list of notifications subscription information for the connected registry.
        """
        pulumi.set(__self__, 'mode', mode)
        pulumi.set(__self__, 'parent', parent)
        pulumi.set(__self__, 'registry_name', registry_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if client_token_ids is not None:
            pulumi.set(__self__, 'client_token_ids', client_token_ids)
        if connected_registry_name is not None:
            pulumi.set(__self__, 'connected_registry_name', connected_registry_name)
        if logging is not None:
            pulumi.set(__self__, 'logging', logging)
        if notifications_list is not None:
            pulumi.set(__self__, 'notifications_list', notifications_list)

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Input[Union[str, 'ConnectedRegistryMode']]:
        """
        The mode of the connected registry resource that indicates the permissions of the registry.
        """
        return pulumi.get(self, 'mode')

    @mode.setter
    def mode(self, value: pulumi.Input[Union[str, 'ConnectedRegistryMode']]):
        pulumi.set(self, 'mode', value)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input['ParentPropertiesArgs']:
        """
        The parent of the connected registry.
        """
        return pulumi.get(self, 'parent')

    @parent.setter
    def parent(self, value: pulumi.Input['ParentPropertiesArgs']):
        pulumi.set(self, 'parent', value)

    @property
    @pulumi.getter(name='registryName')
    def registry_name(self) -> pulumi.Input[str]:
        """
        The name of the container registry.
        """
        return pulumi.get(self, 'registry_name')

    @registry_name.setter
    def registry_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'registry_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group to which the container registry belongs.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='clientTokenIds')
    def client_token_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of the ACR token resource IDs used to authenticate clients to the connected registry.
        """
        return pulumi.get(self, 'client_token_ids')

    @client_token_ids.setter
    def client_token_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'client_token_ids', value)

    @property
    @pulumi.getter(name='connectedRegistryName')
    def connected_registry_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the connected registry.
        """
        return pulumi.get(self, 'connected_registry_name')

    @connected_registry_name.setter
    def connected_registry_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'connected_registry_name', value)

    @property
    @pulumi.getter
    def logging(self) -> Optional[pulumi.Input['LoggingPropertiesArgs']]:
        """
        The logging properties of the connected registry.
        """
        return pulumi.get(self, 'logging')

    @logging.setter
    def logging(self, value: Optional[pulumi.Input['LoggingPropertiesArgs']]):
        pulumi.set(self, 'logging', value)

    @property
    @pulumi.getter(name='notificationsList')
    def notifications_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of notifications subscription information for the connected registry.
        """
        return pulumi.get(self, 'notifications_list')

    @notifications_list.setter
    def notifications_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'notifications_list', value)

class ConnectedRegistry(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_token_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, connected_registry_name: Optional[pulumi.Input[str]]=None, logging: Optional[pulumi.Input[pulumi.InputType['LoggingPropertiesArgs']]]=None, mode: Optional[pulumi.Input[Union[str, 'ConnectedRegistryMode']]]=None, notifications_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, parent: Optional[pulumi.Input[pulumi.InputType['ParentPropertiesArgs']]]=None, registry_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        An object that represents a connected registry for a container registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] client_token_ids: The list of the ACR token resource IDs used to authenticate clients to the connected registry.
        :param pulumi.Input[str] connected_registry_name: The name of the connected registry.
        :param pulumi.Input[pulumi.InputType['LoggingPropertiesArgs']] logging: The logging properties of the connected registry.
        :param pulumi.Input[Union[str, 'ConnectedRegistryMode']] mode: The mode of the connected registry resource that indicates the permissions of the registry.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notifications_list: The list of notifications subscription information for the connected registry.
        :param pulumi.Input[pulumi.InputType['ParentPropertiesArgs']] parent: The parent of the connected registry.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ConnectedRegistryArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        An object that represents a connected registry for a container registry.

        :param str resource_name: The name of the resource.
        :param ConnectedRegistryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ConnectedRegistryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_token_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, connected_registry_name: Optional[pulumi.Input[str]]=None, logging: Optional[pulumi.Input[pulumi.InputType['LoggingPropertiesArgs']]]=None, mode: Optional[pulumi.Input[Union[str, 'ConnectedRegistryMode']]]=None, notifications_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, parent: Optional[pulumi.Input[pulumi.InputType['ParentPropertiesArgs']]]=None, registry_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectedRegistryArgs.__new__(ConnectedRegistryArgs)
            __props__.__dict__['client_token_ids'] = client_token_ids
            __props__.__dict__['connected_registry_name'] = connected_registry_name
            __props__.__dict__['logging'] = logging
            if mode is None and (not opts.urn):
                raise TypeError("Missing required property 'mode'")
            __props__.__dict__['mode'] = mode
            __props__.__dict__['notifications_list'] = notifications_list
            if parent is None and (not opts.urn):
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__['parent'] = parent
            if registry_name is None and (not opts.urn):
                raise TypeError("Missing required property 'registry_name'")
            __props__.__dict__['registry_name'] = registry_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['activation'] = None
            __props__.__dict__['connection_state'] = None
            __props__.__dict__['last_activity_time'] = None
            __props__.__dict__['login_server'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['status_details'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['version'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:containerregistry:ConnectedRegistry'), pulumi.Alias(type_='azure-native:containerregistry/v20201101preview:ConnectedRegistry'), pulumi.Alias(type_='azure-native:containerregistry/v20210601preview:ConnectedRegistry'), pulumi.Alias(type_='azure-native:containerregistry/v20210801preview:ConnectedRegistry'), pulumi.Alias(type_='azure-native:containerregistry/v20211201preview:ConnectedRegistry'), pulumi.Alias(type_='azure-native:containerregistry/v20230101preview:ConnectedRegistry')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConnectedRegistry, __self__).__init__('azure-native:containerregistry/v20220201preview:ConnectedRegistry', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ConnectedRegistry':
        """
        Get an existing ConnectedRegistry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ConnectedRegistryArgs.__new__(ConnectedRegistryArgs)
        __props__.__dict__['activation'] = None
        __props__.__dict__['client_token_ids'] = None
        __props__.__dict__['connection_state'] = None
        __props__.__dict__['last_activity_time'] = None
        __props__.__dict__['logging'] = None
        __props__.__dict__['login_server'] = None
        __props__.__dict__['mode'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['notifications_list'] = None
        __props__.__dict__['parent'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['status_details'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['version'] = None
        return ConnectedRegistry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def activation(self) -> pulumi.Output['outputs.ActivationPropertiesResponse']:
        """
        The activation properties of the connected registry.
        """
        return pulumi.get(self, 'activation')

    @property
    @pulumi.getter(name='clientTokenIds')
    def client_token_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of the ACR token resource IDs used to authenticate clients to the connected registry.
        """
        return pulumi.get(self, 'client_token_ids')

    @property
    @pulumi.getter(name='connectionState')
    def connection_state(self) -> pulumi.Output[str]:
        """
        The current connection state of the connected registry.
        """
        return pulumi.get(self, 'connection_state')

    @property
    @pulumi.getter(name='lastActivityTime')
    def last_activity_time(self) -> pulumi.Output[str]:
        """
        The last activity time of the connected registry.
        """
        return pulumi.get(self, 'last_activity_time')

    @property
    @pulumi.getter
    def logging(self) -> pulumi.Output[Optional['outputs.LoggingPropertiesResponse']]:
        """
        The logging properties of the connected registry.
        """
        return pulumi.get(self, 'logging')

    @property
    @pulumi.getter(name='loginServer')
    def login_server(self) -> pulumi.Output[Optional['outputs.LoginServerPropertiesResponse']]:
        """
        The login server properties of the connected registry.
        """
        return pulumi.get(self, 'login_server')

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Output[str]:
        """
        The mode of the connected registry resource that indicates the permissions of the registry.
        """
        return pulumi.get(self, 'mode')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='notificationsList')
    def notifications_list(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of notifications subscription information for the connected registry.
        """
        return pulumi.get(self, 'notifications_list')

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output['outputs.ParentPropertiesResponse']:
        """
        The parent of the connected registry.
        """
        return pulumi.get(self, 'parent')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='statusDetails')
    def status_details(self) -> pulumi.Output[Sequence['outputs.StatusDetailPropertiesResponse']]:
        """
        The list of current statuses of the connected registry.
        """
        return pulumi.get(self, 'status_details')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The current version of ACR runtime on the connected registry.
        """
        return pulumi.get(self, 'version')