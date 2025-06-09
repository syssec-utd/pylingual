import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['HybridConnectionAuthorizationRuleArgs', 'HybridConnectionAuthorizationRule']

@pulumi.input_type
class HybridConnectionAuthorizationRuleArgs:

    def __init__(__self__, *, hybrid_connection_name: pulumi.Input[str], namespace_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], listen: Optional[pulumi.Input[bool]]=None, manage: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, send: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a HybridConnectionAuthorizationRule resource.
        :param pulumi.Input[str] hybrid_connection_name: Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] namespace_name: Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] listen: Grants listen access to this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] send: Grants send access to this Authorization Rule. Defaults to `false`.
        """
        pulumi.set(__self__, 'hybrid_connection_name', hybrid_connection_name)
        pulumi.set(__self__, 'namespace_name', namespace_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if listen is not None:
            pulumi.set(__self__, 'listen', listen)
        if manage is not None:
            pulumi.set(__self__, 'manage', manage)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if send is not None:
            pulumi.set(__self__, 'send', send)

    @property
    @pulumi.getter(name='hybridConnectionName')
    def hybrid_connection_name(self) -> pulumi.Input[str]:
        """
        Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'hybrid_connection_name')

    @hybrid_connection_name.setter
    def hybrid_connection_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'hybrid_connection_name', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> pulumi.Input[str]:
        """
        Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants listen access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'listen')

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'listen', value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        """
        return pulumi.get(self, 'manage')

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'manage', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants send access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'send')

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'send', value)

@pulumi.input_type
class _HybridConnectionAuthorizationRuleState:

    def __init__(__self__, *, hybrid_connection_name: Optional[pulumi.Input[str]]=None, listen: Optional[pulumi.Input[bool]]=None, manage: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, primary_connection_string: Optional[pulumi.Input[str]]=None, primary_key: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, secondary_connection_string: Optional[pulumi.Input[str]]=None, secondary_key: Optional[pulumi.Input[str]]=None, send: Optional[pulumi.Input[bool]]=None):
        """
        Input properties used for looking up and filtering HybridConnectionAuthorizationRule resources.
        :param pulumi.Input[str] hybrid_connection_name: Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] listen: Grants listen access to this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] namespace_name: Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[bool] send: Grants send access to this Authorization Rule. Defaults to `false`.
        """
        if hybrid_connection_name is not None:
            pulumi.set(__self__, 'hybrid_connection_name', hybrid_connection_name)
        if listen is not None:
            pulumi.set(__self__, 'listen', listen)
        if manage is not None:
            pulumi.set(__self__, 'manage', manage)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if namespace_name is not None:
            pulumi.set(__self__, 'namespace_name', namespace_name)
        if primary_connection_string is not None:
            pulumi.set(__self__, 'primary_connection_string', primary_connection_string)
        if primary_key is not None:
            pulumi.set(__self__, 'primary_key', primary_key)
        if resource_group_name is not None:
            pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if secondary_connection_string is not None:
            pulumi.set(__self__, 'secondary_connection_string', secondary_connection_string)
        if secondary_key is not None:
            pulumi.set(__self__, 'secondary_key', secondary_key)
        if send is not None:
            pulumi.set(__self__, 'send', send)

    @property
    @pulumi.getter(name='hybridConnectionName')
    def hybrid_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'hybrid_connection_name')

    @hybrid_connection_name.setter
    def hybrid_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'hybrid_connection_name', value)

    @property
    @pulumi.getter
    def listen(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants listen access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'listen')

    @listen.setter
    def listen(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'listen', value)

    @property
    @pulumi.getter
    def manage(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        """
        return pulumi.get(self, 'manage')

    @manage.setter
    def manage(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'manage', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter(name='primaryConnectionString')
    def primary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'primary_connection_string')

    @primary_connection_string.setter
    def primary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'primary_connection_string', value)

    @property
    @pulumi.getter(name='primaryKey')
    def primary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Primary Key for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'primary_key')

    @primary_key.setter
    def primary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'primary_key', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='secondaryConnectionString')
    def secondary_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'secondary_connection_string')

    @secondary_connection_string.setter
    def secondary_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'secondary_connection_string', value)

    @property
    @pulumi.getter(name='secondaryKey')
    def secondary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Secondary Key for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'secondary_key')

    @secondary_key.setter
    def secondary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'secondary_key', value)

    @property
    @pulumi.getter
    def send(self) -> Optional[pulumi.Input[bool]]:
        """
        Grants send access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'send')

    @send.setter
    def send(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'send', value)

class HybridConnectionAuthorizationRule(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, hybrid_connection_name: Optional[pulumi.Input[str]]=None, listen: Optional[pulumi.Input[bool]]=None, manage: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, send: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        Manages an Azure Relay Hybrid Connection Authorization Rule.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_namespace = azure.relay.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Standard",
            tags={
                "source": "terraform",
            })
        example_hybrid_connection = azure.relay.HybridConnection("exampleHybridConnection",
            resource_group_name=example_resource_group.name,
            relay_namespace_name=example_namespace.name,
            requires_client_authorization=False,
            user_metadata="testmetadata")
        example_hybrid_connection_authorization_rule = azure.relay.HybridConnectionAuthorizationRule("exampleHybridConnectionAuthorizationRule",
            resource_group_name=example_resource_group.name,
            hybrid_connection_name=example_hybrid_connection.name,
            namespace_name=example_namespace.name,
            listen=True,
            send=True,
            manage=False)
        ```

        ## Import

        Azure Relay Hybrid Connection Authorization Rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:relay/hybridConnectionAuthorizationRule:HybridConnectionAuthorizationRule example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Relay/namespaces/namespace1/hybridConnections/connection1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hybrid_connection_name: Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] listen: Grants listen access to this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] namespace_name: Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] send: Grants send access to this Authorization Rule. Defaults to `false`.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: HybridConnectionAuthorizationRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages an Azure Relay Hybrid Connection Authorization Rule.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_namespace = azure.relay.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku_name="Standard",
            tags={
                "source": "terraform",
            })
        example_hybrid_connection = azure.relay.HybridConnection("exampleHybridConnection",
            resource_group_name=example_resource_group.name,
            relay_namespace_name=example_namespace.name,
            requires_client_authorization=False,
            user_metadata="testmetadata")
        example_hybrid_connection_authorization_rule = azure.relay.HybridConnectionAuthorizationRule("exampleHybridConnectionAuthorizationRule",
            resource_group_name=example_resource_group.name,
            hybrid_connection_name=example_hybrid_connection.name,
            namespace_name=example_namespace.name,
            listen=True,
            send=True,
            manage=False)
        ```

        ## Import

        Azure Relay Hybrid Connection Authorization Rules can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:relay/hybridConnectionAuthorizationRule:HybridConnectionAuthorizationRule example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Relay/namespaces/namespace1/hybridConnections/connection1/authorizationRules/rule1
        ```

        :param str resource_name: The name of the resource.
        :param HybridConnectionAuthorizationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HybridConnectionAuthorizationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, hybrid_connection_name: Optional[pulumi.Input[str]]=None, listen: Optional[pulumi.Input[bool]]=None, manage: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, send: Optional[pulumi.Input[bool]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HybridConnectionAuthorizationRuleArgs.__new__(HybridConnectionAuthorizationRuleArgs)
            if hybrid_connection_name is None and (not opts.urn):
                raise TypeError("Missing required property 'hybrid_connection_name'")
            __props__.__dict__['hybrid_connection_name'] = hybrid_connection_name
            __props__.__dict__['listen'] = listen
            __props__.__dict__['manage'] = manage
            __props__.__dict__['name'] = name
            if namespace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__['namespace_name'] = namespace_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['send'] = send
            __props__.__dict__['primary_connection_string'] = None
            __props__.__dict__['primary_key'] = None
            __props__.__dict__['secondary_connection_string'] = None
            __props__.__dict__['secondary_key'] = None
        super(HybridConnectionAuthorizationRule, __self__).__init__('azure:relay/hybridConnectionAuthorizationRule:HybridConnectionAuthorizationRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, hybrid_connection_name: Optional[pulumi.Input[str]]=None, listen: Optional[pulumi.Input[bool]]=None, manage: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, primary_connection_string: Optional[pulumi.Input[str]]=None, primary_key: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, secondary_connection_string: Optional[pulumi.Input[str]]=None, secondary_key: Optional[pulumi.Input[str]]=None, send: Optional[pulumi.Input[bool]]=None) -> 'HybridConnectionAuthorizationRule':
        """
        Get an existing HybridConnectionAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hybrid_connection_name: Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[bool] listen: Grants listen access to this Authorization Rule. Defaults to `false`.
        :param pulumi.Input[bool] manage: Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        :param pulumi.Input[str] name: The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] namespace_name: Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] primary_connection_string: The Primary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] primary_key: The Primary Key for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        :param pulumi.Input[str] secondary_connection_string: The Secondary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[str] secondary_key: The Secondary Key for the Azure Relay Hybrid Connection Authorization Rule.
        :param pulumi.Input[bool] send: Grants send access to this Authorization Rule. Defaults to `false`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _HybridConnectionAuthorizationRuleState.__new__(_HybridConnectionAuthorizationRuleState)
        __props__.__dict__['hybrid_connection_name'] = hybrid_connection_name
        __props__.__dict__['listen'] = listen
        __props__.__dict__['manage'] = manage
        __props__.__dict__['name'] = name
        __props__.__dict__['namespace_name'] = namespace_name
        __props__.__dict__['primary_connection_string'] = primary_connection_string
        __props__.__dict__['primary_key'] = primary_key
        __props__.__dict__['resource_group_name'] = resource_group_name
        __props__.__dict__['secondary_connection_string'] = secondary_connection_string
        __props__.__dict__['secondary_key'] = secondary_key
        __props__.__dict__['send'] = send
        return HybridConnectionAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='hybridConnectionName')
    def hybrid_connection_name(self) -> pulumi.Output[str]:
        """
        Name of the Azure Relay Hybrid Connection for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'hybrid_connection_name')

    @property
    @pulumi.getter
    def listen(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants listen access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'listen')

    @property
    @pulumi.getter
    def manage(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants manage access to this Authorization Rule. When this property is `true` - both `listen` and `send` must be set to `true` too. Defaults to `false`.
        """
        return pulumi.get(self, 'manage')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Azure Relay Hybrid Connection Authorization Rule. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> pulumi.Output[str]:
        """
        Name of the Azure Relay Namespace for which this Azure Relay Hybrid Connection Authorization Rule will be created. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'namespace_name')

    @property
    @pulumi.getter(name='primaryConnectionString')
    def primary_connection_string(self) -> pulumi.Output[str]:
        """
        The Primary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'primary_connection_string')

    @property
    @pulumi.getter(name='primaryKey')
    def primary_key(self) -> pulumi.Output[str]:
        """
        The Primary Key for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'primary_key')

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Azure Relay Hybrid Connection Authorization Rule should exist. Changing this forces a new Azure Relay Hybrid Connection Authorization Rule to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @property
    @pulumi.getter(name='secondaryConnectionString')
    def secondary_connection_string(self) -> pulumi.Output[str]:
        """
        The Secondary Connection String for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'secondary_connection_string')

    @property
    @pulumi.getter(name='secondaryKey')
    def secondary_key(self) -> pulumi.Output[str]:
        """
        The Secondary Key for the Azure Relay Hybrid Connection Authorization Rule.
        """
        return pulumi.get(self, 'secondary_key')

    @property
    @pulumi.getter
    def send(self) -> pulumi.Output[Optional[bool]]:
        """
        Grants send access to this Authorization Rule. Defaults to `false`.
        """
        return pulumi.get(self, 'send')