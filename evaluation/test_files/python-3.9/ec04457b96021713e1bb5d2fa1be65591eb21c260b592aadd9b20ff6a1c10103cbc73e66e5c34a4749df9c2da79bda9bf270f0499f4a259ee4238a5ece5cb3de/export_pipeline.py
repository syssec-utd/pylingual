import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ExportPipelineArgs', 'ExportPipeline']

@pulumi.input_type
class ExportPipelineArgs:

    def __init__(__self__, *, registry_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], target: pulumi.Input['ExportPipelineTargetPropertiesArgs'], export_pipeline_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input['IdentityPropertiesArgs']]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]]]=None):
        """
        The set of arguments for constructing a ExportPipeline resource.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input['ExportPipelineTargetPropertiesArgs'] target: The target properties of the export pipeline.
        :param pulumi.Input[str] export_pipeline_name: The name of the export pipeline.
        :param pulumi.Input['IdentityPropertiesArgs'] identity: The identity of the export pipeline.
        :param pulumi.Input[str] location: The location of the export pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]] options: The list of all options configured for the pipeline.
        """
        pulumi.set(__self__, 'registry_name', registry_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'target', target)
        if export_pipeline_name is not None:
            pulumi.set(__self__, 'export_pipeline_name', export_pipeline_name)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if options is not None:
            pulumi.set(__self__, 'options', options)

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
    @pulumi.getter
    def target(self) -> pulumi.Input['ExportPipelineTargetPropertiesArgs']:
        """
        The target properties of the export pipeline.
        """
        return pulumi.get(self, 'target')

    @target.setter
    def target(self, value: pulumi.Input['ExportPipelineTargetPropertiesArgs']):
        pulumi.set(self, 'target', value)

    @property
    @pulumi.getter(name='exportPipelineName')
    def export_pipeline_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the export pipeline.
        """
        return pulumi.get(self, 'export_pipeline_name')

    @export_pipeline_name.setter
    def export_pipeline_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'export_pipeline_name', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityPropertiesArgs']]:
        """
        The identity of the export pipeline.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityPropertiesArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the export pipeline.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]]]:
        """
        The list of all options configured for the pipeline.
        """
        return pulumi.get(self, 'options')

    @options.setter
    def options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]]]):
        pulumi.set(self, 'options', value)

class ExportPipeline(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, export_pipeline_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]]]=None, registry_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, target: Optional[pulumi.Input[pulumi.InputType['ExportPipelineTargetPropertiesArgs']]]=None, __props__=None):
        """
        An object that represents an export pipeline for a container registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] export_pipeline_name: The name of the export pipeline.
        :param pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']] identity: The identity of the export pipeline.
        :param pulumi.Input[str] location: The location of the export pipeline.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]] options: The list of all options configured for the pipeline.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[pulumi.InputType['ExportPipelineTargetPropertiesArgs']] target: The target properties of the export pipeline.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ExportPipelineArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        An object that represents an export pipeline for a container registry.

        :param str resource_name: The name of the resource.
        :param ExportPipelineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ExportPipelineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, export_pipeline_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'PipelineOptions']]]]]=None, registry_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, target: Optional[pulumi.Input[pulumi.InputType['ExportPipelineTargetPropertiesArgs']]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExportPipelineArgs.__new__(ExportPipelineArgs)
            __props__.__dict__['export_pipeline_name'] = export_pipeline_name
            __props__.__dict__['identity'] = identity
            __props__.__dict__['location'] = location
            __props__.__dict__['options'] = options
            if registry_name is None and (not opts.urn):
                raise TypeError("Missing required property 'registry_name'")
            __props__.__dict__['registry_name'] = registry_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if target is None and (not opts.urn):
                raise TypeError("Missing required property 'target'")
            __props__.__dict__['target'] = target
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:containerregistry:ExportPipeline'), pulumi.Alias(type_='azure-native:containerregistry/v20191201preview:ExportPipeline'), pulumi.Alias(type_='azure-native:containerregistry/v20201101preview:ExportPipeline'), pulumi.Alias(type_='azure-native:containerregistry/v20210601preview:ExportPipeline'), pulumi.Alias(type_='azure-native:containerregistry/v20210801preview:ExportPipeline'), pulumi.Alias(type_='azure-native:containerregistry/v20211201preview:ExportPipeline')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ExportPipeline, __self__).__init__('azure-native:containerregistry/v20220201preview:ExportPipeline', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ExportPipeline':
        """
        Get an existing ExportPipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ExportPipelineArgs.__new__(ExportPipelineArgs)
        __props__.__dict__['identity'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['options'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['target'] = None
        __props__.__dict__['type'] = None
        return ExportPipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityPropertiesResponse']]:
        """
        The identity of the export pipeline.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the export pipeline.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of all options configured for the pipeline.
        """
        return pulumi.get(self, 'options')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the pipeline at the time the operation was called.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output['outputs.ExportPipelineTargetPropertiesResponse']:
        """
        The target properties of the export pipeline.
        """
        return pulumi.get(self, 'target')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')