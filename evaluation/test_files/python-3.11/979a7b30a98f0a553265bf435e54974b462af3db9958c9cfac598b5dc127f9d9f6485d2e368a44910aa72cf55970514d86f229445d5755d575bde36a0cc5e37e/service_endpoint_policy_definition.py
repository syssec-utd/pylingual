import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['ServiceEndpointPolicyDefinitionInitArgs', 'ServiceEndpointPolicyDefinition']

@pulumi.input_type
class ServiceEndpointPolicyDefinitionInitArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], service_endpoint_policy_name: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, service: Optional[pulumi.Input[str]]=None, service_endpoint_policy_definition_name: Optional[pulumi.Input[str]]=None, service_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ServiceEndpointPolicyDefinition resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_endpoint_policy_name: The name of the service endpoint policy.
        :param pulumi.Input[str] description: A description for this rule. Restricted to 140 chars.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] service: Service endpoint name.
        :param pulumi.Input[str] service_endpoint_policy_definition_name: The name of the service endpoint policy definition name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_resources: A list of service resources.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_endpoint_policy_name', service_endpoint_policy_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if service is not None:
            pulumi.set(__self__, 'service', service)
        if service_endpoint_policy_definition_name is not None:
            pulumi.set(__self__, 'service_endpoint_policy_definition_name', service_endpoint_policy_definition_name)
        if service_resources is not None:
            pulumi.set(__self__, 'service_resources', service_resources)

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
    @pulumi.getter(name='serviceEndpointPolicyName')
    def service_endpoint_policy_name(self) -> pulumi.Input[str]:
        """
        The name of the service endpoint policy.
        """
        return pulumi.get(self, 'service_endpoint_policy_name')

    @service_endpoint_policy_name.setter
    def service_endpoint_policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'service_endpoint_policy_name', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Service endpoint name.
        """
        return pulumi.get(self, 'service')

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'service', value)

    @property
    @pulumi.getter(name='serviceEndpointPolicyDefinitionName')
    def service_endpoint_policy_definition_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service endpoint policy definition name.
        """
        return pulumi.get(self, 'service_endpoint_policy_definition_name')

    @service_endpoint_policy_definition_name.setter
    def service_endpoint_policy_definition_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'service_endpoint_policy_definition_name', value)

    @property
    @pulumi.getter(name='serviceResources')
    def service_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of service resources.
        """
        return pulumi.get(self, 'service_resources')

    @service_resources.setter
    def service_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'service_resources', value)

class ServiceEndpointPolicyDefinition(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service: Optional[pulumi.Input[str]]=None, service_endpoint_policy_definition_name: Optional[pulumi.Input[str]]=None, service_endpoint_policy_name: Optional[pulumi.Input[str]]=None, service_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        Service Endpoint policy definitions.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for this rule. Restricted to 140 chars.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service: Service endpoint name.
        :param pulumi.Input[str] service_endpoint_policy_definition_name: The name of the service endpoint policy definition name.
        :param pulumi.Input[str] service_endpoint_policy_name: The name of the service endpoint policy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_resources: A list of service resources.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ServiceEndpointPolicyDefinitionInitArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Service Endpoint policy definitions.

        :param str resource_name: The name of the resource.
        :param ServiceEndpointPolicyDefinitionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceEndpointPolicyDefinitionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service: Optional[pulumi.Input[str]]=None, service_endpoint_policy_definition_name: Optional[pulumi.Input[str]]=None, service_endpoint_policy_name: Optional[pulumi.Input[str]]=None, service_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceEndpointPolicyDefinitionInitArgs.__new__(ServiceEndpointPolicyDefinitionInitArgs)
            __props__.__dict__['description'] = description
            __props__.__dict__['id'] = id
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['service'] = service
            __props__.__dict__['service_endpoint_policy_definition_name'] = service_endpoint_policy_definition_name
            if service_endpoint_policy_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_endpoint_policy_name'")
            __props__.__dict__['service_endpoint_policy_name'] = service_endpoint_policy_name
            __props__.__dict__['service_resources'] = service_resources
            __props__.__dict__['etag'] = None
            __props__.__dict__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20180701:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20180801:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20181001:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20181101:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20181201:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190201:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190401:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190601:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190701:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190801:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20190901:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20191201:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200301:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200401:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200501:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200601:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200701:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20200801:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20201101:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20210201:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20210301:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20210501:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20210801:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20220101:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20220501:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20220701:ServiceEndpointPolicyDefinition'), pulumi.Alias(type_='azure-native:network/v20220901:ServiceEndpointPolicyDefinition')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ServiceEndpointPolicyDefinition, __self__).__init__('azure-native:network/v20191101:ServiceEndpointPolicyDefinition', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ServiceEndpointPolicyDefinition':
        """
        Get an existing ServiceEndpointPolicyDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ServiceEndpointPolicyDefinitionInitArgs.__new__(ServiceEndpointPolicyDefinitionInitArgs)
        __props__.__dict__['description'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['service'] = None
        __props__.__dict__['service_resources'] = None
        return ServiceEndpointPolicyDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the service endpoint policy definition resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[Optional[str]]:
        """
        Service endpoint name.
        """
        return pulumi.get(self, 'service')

    @property
    @pulumi.getter(name='serviceResources')
    def service_resources(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of service resources.
        """
        return pulumi.get(self, 'service_resources')