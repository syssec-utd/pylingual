import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['DeploymentScriptArgs', 'DeploymentScript']

@pulumi.input_type
class DeploymentScriptArgs:

    def __init__(__self__, *, identity: pulumi.Input['ManagedServiceIdentityArgs'], kind: pulumi.Input[Union[str, 'ScriptType']], resource_group_name: pulumi.Input[str], location: Optional[pulumi.Input[str]]=None, script_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a DeploymentScript resource.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: Managed identity to be used for this deployment script. Currently, only user-assigned MSI is supported.
        :param pulumi.Input[Union[str, 'ScriptType']] kind: Type of the script.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] location: The location of the ACI and the storage account for the deployment script.
        :param pulumi.Input[str] script_name: Name of the deployment script.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'identity', identity)
        pulumi.set(__self__, 'kind', kind)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if script_name is not None:
            pulumi.set(__self__, 'script_name', script_name)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Input['ManagedServiceIdentityArgs']:
        """
        Managed identity to be used for this deployment script. Currently, only user-assigned MSI is supported.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: pulumi.Input['ManagedServiceIdentityArgs']):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[Union[str, 'ScriptType']]:
        """
        Type of the script.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[Union[str, 'ScriptType']]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the ACI and the storage account for the deployment script.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='scriptName')
    def script_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the deployment script.
        """
        return pulumi.get(self, 'script_name')

    @script_name.setter
    def script_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'script_name', value)

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
warnings.warn('Please use one of the variants: AzureCliScript, AzurePowerShellScript.', DeprecationWarning)

class DeploymentScript(pulumi.CustomResource):
    warnings.warn('Please use one of the variants: AzureCliScript, AzurePowerShellScript.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, kind: Optional[pulumi.Input[Union[str, 'ScriptType']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, script_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Deployment script object.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: Managed identity to be used for this deployment script. Currently, only user-assigned MSI is supported.
        :param pulumi.Input[Union[str, 'ScriptType']] kind: Type of the script.
        :param pulumi.Input[str] location: The location of the ACI and the storage account for the deployment script.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] script_name: Name of the deployment script.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DeploymentScriptArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Deployment script object.

        :param str resource_name: The name of the resource.
        :param DeploymentScriptArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeploymentScriptArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, kind: Optional[pulumi.Input[Union[str, 'ScriptType']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, script_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        pulumi.log.warn('DeploymentScript is deprecated: Please use one of the variants: AzureCliScript, AzurePowerShellScript.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeploymentScriptArgs.__new__(DeploymentScriptArgs)
            if identity is None and (not opts.urn):
                raise TypeError("Missing required property 'identity'")
            __props__.__dict__['identity'] = identity
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = kind
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['script_name'] = script_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:resources:DeploymentScript'), pulumi.Alias(type_='azure-native:resources/v20201001:DeploymentScript')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DeploymentScript, __self__).__init__('azure-native:resources/v20191001preview:DeploymentScript', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DeploymentScript':
        """
        Get an existing DeploymentScript resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DeploymentScriptArgs.__new__(DeploymentScriptArgs)
        __props__.__dict__['identity'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return DeploymentScript(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.ManagedServiceIdentityResponse']:
        """
        Managed identity to be used for this deployment script. Currently, only user-assigned MSI is supported.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Type of the script.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the ACI and the storage account for the deployment script.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of this resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, 'system_data')

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
        Type of this resource.
        """
        return pulumi.get(self, 'type')