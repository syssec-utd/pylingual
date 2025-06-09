import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ApplicationGroupArgs', 'ApplicationGroup']

@pulumi.input_type
class ApplicationGroupArgs:

    def __init__(__self__, *, application_group_type: pulumi.Input[Union[str, 'ApplicationGroupType']], host_pool_arm_path: pulumi.Input[str], resource_group_name: pulumi.Input[str], application_group_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, friendly_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetIdentityArgs']]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, managed_by: Optional[pulumi.Input[str]]=None, migration_request: Optional[pulumi.Input['MigrationRequestPropertiesArgs']]=None, plan: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetPlanArgs']]=None, sku: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetSkuArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ApplicationGroup resource.
        :param pulumi.Input[Union[str, 'ApplicationGroupType']] application_group_type: Resource Type of ApplicationGroup.
        :param pulumi.Input[str] host_pool_arm_path: HostPool arm path of ApplicationGroup.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[str] description: Description of ApplicationGroup.
        :param pulumi.Input[str] friendly_name: Friendly name of ApplicationGroup.
        :param pulumi.Input[str] kind: Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_by: The fully qualified resource ID of the resource that manages this resource. Indicates if this resource is managed by another Azure resource. If this is present, complete mode deployment will not delete the resource if it is removed from the template since it is managed by another resource.
        :param pulumi.Input['MigrationRequestPropertiesArgs'] migration_request: The registration info of HostPool.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'application_group_type', application_group_type)
        pulumi.set(__self__, 'host_pool_arm_path', host_pool_arm_path)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if application_group_name is not None:
            pulumi.set(__self__, 'application_group_name', application_group_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if friendly_name is not None:
            pulumi.set(__self__, 'friendly_name', friendly_name)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if managed_by is not None:
            pulumi.set(__self__, 'managed_by', managed_by)
        if migration_request is not None:
            pulumi.set(__self__, 'migration_request', migration_request)
        if plan is not None:
            pulumi.set(__self__, 'plan', plan)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='applicationGroupType')
    def application_group_type(self) -> pulumi.Input[Union[str, 'ApplicationGroupType']]:
        """
        Resource Type of ApplicationGroup.
        """
        return pulumi.get(self, 'application_group_type')

    @application_group_type.setter
    def application_group_type(self, value: pulumi.Input[Union[str, 'ApplicationGroupType']]):
        pulumi.set(self, 'application_group_type', value)

    @property
    @pulumi.getter(name='hostPoolArmPath')
    def host_pool_arm_path(self) -> pulumi.Input[str]:
        """
        HostPool arm path of ApplicationGroup.
        """
        return pulumi.get(self, 'host_pool_arm_path')

    @host_pool_arm_path.setter
    def host_pool_arm_path(self, value: pulumi.Input[str]):
        pulumi.set(self, 'host_pool_arm_path', value)

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
    @pulumi.getter(name='applicationGroupName')
    def application_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application group
        """
        return pulumi.get(self, 'application_group_name')

    @application_group_name.setter
    def application_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'application_group_name', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of ApplicationGroup.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly name of ApplicationGroup.
        """
        return pulumi.get(self, 'friendly_name')

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'friendly_name', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceModelWithAllowedPropertySetIdentityArgs']]:
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='managedBy')
    def managed_by(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified resource ID of the resource that manages this resource. Indicates if this resource is managed by another Azure resource. If this is present, complete mode deployment will not delete the resource if it is removed from the template since it is managed by another resource.
        """
        return pulumi.get(self, 'managed_by')

    @managed_by.setter
    def managed_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'managed_by', value)

    @property
    @pulumi.getter(name='migrationRequest')
    def migration_request(self) -> Optional[pulumi.Input['MigrationRequestPropertiesArgs']]:
        """
        The registration info of HostPool.
        """
        return pulumi.get(self, 'migration_request')

    @migration_request.setter
    def migration_request(self, value: Optional[pulumi.Input['MigrationRequestPropertiesArgs']]):
        pulumi.set(self, 'migration_request', value)

    @property
    @pulumi.getter
    def plan(self) -> Optional[pulumi.Input['ResourceModelWithAllowedPropertySetPlanArgs']]:
        return pulumi.get(self, 'plan')

    @plan.setter
    def plan(self, value: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetPlanArgs']]):
        pulumi.set(self, 'plan', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ResourceModelWithAllowedPropertySetSkuArgs']]:
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ResourceModelWithAllowedPropertySetSkuArgs']]):
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

class ApplicationGroup(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_group_name: Optional[pulumi.Input[str]]=None, application_group_type: Optional[pulumi.Input[Union[str, 'ApplicationGroupType']]]=None, description: Optional[pulumi.Input[str]]=None, friendly_name: Optional[pulumi.Input[str]]=None, host_pool_arm_path: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetIdentityArgs']]]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, managed_by: Optional[pulumi.Input[str]]=None, migration_request: Optional[pulumi.Input[pulumi.InputType['MigrationRequestPropertiesArgs']]]=None, plan: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetPlanArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetSkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Represents a ApplicationGroup definition.
        API Version: 2021-02-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[Union[str, 'ApplicationGroupType']] application_group_type: Resource Type of ApplicationGroup.
        :param pulumi.Input[str] description: Description of ApplicationGroup.
        :param pulumi.Input[str] friendly_name: Friendly name of ApplicationGroup.
        :param pulumi.Input[str] host_pool_arm_path: HostPool arm path of ApplicationGroup.
        :param pulumi.Input[str] kind: Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_by: The fully qualified resource ID of the resource that manages this resource. Indicates if this resource is managed by another Azure resource. If this is present, complete mode deployment will not delete the resource if it is removed from the template since it is managed by another resource.
        :param pulumi.Input[pulumi.InputType['MigrationRequestPropertiesArgs']] migration_request: The registration info of HostPool.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ApplicationGroupArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Represents a ApplicationGroup definition.
        API Version: 2021-02-01-preview.

        :param str resource_name: The name of the resource.
        :param ApplicationGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ApplicationGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_group_name: Optional[pulumi.Input[str]]=None, application_group_type: Optional[pulumi.Input[Union[str, 'ApplicationGroupType']]]=None, description: Optional[pulumi.Input[str]]=None, friendly_name: Optional[pulumi.Input[str]]=None, host_pool_arm_path: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetIdentityArgs']]]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, managed_by: Optional[pulumi.Input[str]]=None, migration_request: Optional[pulumi.Input[pulumi.InputType['MigrationRequestPropertiesArgs']]]=None, plan: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetPlanArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ResourceModelWithAllowedPropertySetSkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationGroupArgs.__new__(ApplicationGroupArgs)
            __props__.__dict__['application_group_name'] = application_group_name
            if application_group_type is None and (not opts.urn):
                raise TypeError("Missing required property 'application_group_type'")
            __props__.__dict__['application_group_type'] = application_group_type
            __props__.__dict__['description'] = description
            __props__.__dict__['friendly_name'] = friendly_name
            if host_pool_arm_path is None and (not opts.urn):
                raise TypeError("Missing required property 'host_pool_arm_path'")
            __props__.__dict__['host_pool_arm_path'] = host_pool_arm_path
            __props__.__dict__['identity'] = identity
            __props__.__dict__['kind'] = kind
            __props__.__dict__['location'] = location
            __props__.__dict__['managed_by'] = managed_by
            __props__.__dict__['migration_request'] = migration_request
            __props__.__dict__['plan'] = plan
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['tags'] = tags
            __props__.__dict__['cloud_pc_resource'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['object_id'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['workspace_arm_path'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:desktopvirtualization/v20190123preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20190924preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20191210preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20200921preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20201019preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20201102preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20201110preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210114preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210201preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210309preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210401preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210712:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20210903preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20220210preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20220401preview:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20220909:ApplicationGroup'), pulumi.Alias(type_='azure-native:desktopvirtualization/v20221014preview:ApplicationGroup')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationGroup, __self__).__init__('azure-native:desktopvirtualization:ApplicationGroup', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ApplicationGroup':
        """
        Get an existing ApplicationGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ApplicationGroupArgs.__new__(ApplicationGroupArgs)
        __props__.__dict__['application_group_type'] = None
        __props__.__dict__['cloud_pc_resource'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['friendly_name'] = None
        __props__.__dict__['host_pool_arm_path'] = None
        __props__.__dict__['identity'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['managed_by'] = None
        __props__.__dict__['migration_request'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['object_id'] = None
        __props__.__dict__['plan'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['workspace_arm_path'] = None
        return ApplicationGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='applicationGroupType')
    def application_group_type(self) -> pulumi.Output[str]:
        """
        Resource Type of ApplicationGroup.
        """
        return pulumi.get(self, 'application_group_type')

    @property
    @pulumi.getter(name='cloudPcResource')
    def cloud_pc_resource(self) -> pulumi.Output[bool]:
        """
        Is cloud pc resource.
        """
        return pulumi.get(self, 'cloud_pc_resource')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of ApplicationGroup.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal etag convention.  Entity tags are used for comparing two or more entities from the same requested resource. HTTP/1.1 uses entity tags in the etag (section 14.19), If-Match (section 14.24), If-None-Match (section 14.26), and If-Range (section 14.27) header fields. 
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly name of ApplicationGroup.
        """
        return pulumi.get(self, 'friendly_name')

    @property
    @pulumi.getter(name='hostPoolArmPath')
    def host_pool_arm_path(self) -> pulumi.Output[str]:
        """
        HostPool arm path of ApplicationGroup.
        """
        return pulumi.get(self, 'host_pool_arm_path')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ResourceModelWithAllowedPropertySetResponseIdentity']]:
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='managedBy')
    def managed_by(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified resource ID of the resource that manages this resource. Indicates if this resource is managed by another Azure resource. If this is present, complete mode deployment will not delete the resource if it is removed from the template since it is managed by another resource.
        """
        return pulumi.get(self, 'managed_by')

    @property
    @pulumi.getter(name='migrationRequest')
    def migration_request(self) -> pulumi.Output[Optional['outputs.MigrationRequestPropertiesResponse']]:
        """
        The registration info of HostPool.
        """
        return pulumi.get(self, 'migration_request')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='objectId')
    def object_id(self) -> pulumi.Output[str]:
        """
        ObjectId of ApplicationGroup. (internal use)
        """
        return pulumi.get(self, 'object_id')

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output[Optional['outputs.ResourceModelWithAllowedPropertySetResponsePlan']]:
        return pulumi.get(self, 'plan')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ResourceModelWithAllowedPropertySetResponseSku']]:
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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='workspaceArmPath')
    def workspace_arm_path(self) -> pulumi.Output[str]:
        """
        Workspace arm path of ApplicationGroup.
        """
        return pulumi.get(self, 'workspace_arm_path')