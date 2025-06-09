import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['DicomServiceArgs', 'DicomService']

@pulumi.input_type
class DicomServiceArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], workspace_name: pulumi.Input[str], dicom_service_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input['ServiceManagedIdentityIdentityArgs']]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a DicomService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the service instance.
        :param pulumi.Input[str] workspace_name: The name of workspace resource.
        :param pulumi.Input[str] dicom_service_name: The name of DICOM Service resource.
        :param pulumi.Input['ServiceManagedIdentityIdentityArgs'] identity: Setting indicating whether the service has a managed identity associated with it.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'workspace_name', workspace_name)
        if dicom_service_name is not None:
            pulumi.set(__self__, 'dicom_service_name', dicom_service_name)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the service instance.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='workspaceName')
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of workspace resource.
        """
        return pulumi.get(self, 'workspace_name')

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'workspace_name', value)

    @property
    @pulumi.getter(name='dicomServiceName')
    def dicom_service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of DICOM Service resource.
        """
        return pulumi.get(self, 'dicom_service_name')

    @dicom_service_name.setter
    def dicom_service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dicom_service_name', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ServiceManagedIdentityIdentityArgs']]:
        """
        Setting indicating whether the service has a managed identity associated with it.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ServiceManagedIdentityIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

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

class DicomService(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, dicom_service_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ServiceManagedIdentityIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The description of Dicom Service

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dicom_service_name: The name of DICOM Service resource.
        :param pulumi.Input[pulumi.InputType['ServiceManagedIdentityIdentityArgs']] identity: Setting indicating whether the service has a managed identity associated with it.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the service instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] workspace_name: The name of workspace resource.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DicomServiceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The description of Dicom Service

        :param str resource_name: The name of the resource.
        :param DicomServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(DicomServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, dicom_service_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ServiceManagedIdentityIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DicomServiceArgs.__new__(DicomServiceArgs)
            __props__.__dict__['dicom_service_name'] = dicom_service_name
            __props__.__dict__['identity'] = identity
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            if workspace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__['workspace_name'] = workspace_name
            __props__.__dict__['authentication_configuration'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['private_endpoint_connections'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['public_network_access'] = None
            __props__.__dict__['service_url'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:healthcareapis:DicomService'), pulumi.Alias(type_='azure-native:healthcareapis/v20210601preview:DicomService'), pulumi.Alias(type_='azure-native:healthcareapis/v20220131preview:DicomService'), pulumi.Alias(type_='azure-native:healthcareapis/v20220515:DicomService'), pulumi.Alias(type_='azure-native:healthcareapis/v20220601:DicomService'), pulumi.Alias(type_='azure-native:healthcareapis/v20221001preview:DicomService')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DicomService, __self__).__init__('azure-native:healthcareapis/v20211101:DicomService', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DicomService':
        """
        Get an existing DicomService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DicomServiceArgs.__new__(DicomServiceArgs)
        __props__.__dict__['authentication_configuration'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['identity'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['private_endpoint_connections'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['public_network_access'] = None
        __props__.__dict__['service_url'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return DicomService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='authenticationConfiguration')
    def authentication_configuration(self) -> pulumi.Output[Optional['outputs.DicomServiceAuthenticationConfigurationResponse']]:
        """
        Dicom Service authentication configuration.
        """
        return pulumi.get(self, 'authentication_configuration')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        An etag associated with the resource, used for optimistic concurrency when editing it.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ServiceManagedIdentityResponseIdentity']]:
        """
        Setting indicating whether the service has a managed identity associated with it.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpointConnections')
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        The list of private endpoint connections that are set up for this resource.
        """
        return pulumi.get(self, 'private_endpoint_connections')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publicNetworkAccess')
    def public_network_access(self) -> pulumi.Output[str]:
        """
        Control permission for data plane traffic coming from public networks while private endpoint is enabled.
        """
        return pulumi.get(self, 'public_network_access')

    @property
    @pulumi.getter(name='serviceUrl')
    def service_url(self) -> pulumi.Output[str]:
        """
        The url of the Dicom Services.
        """
        return pulumi.get(self, 'service_url')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
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
        The resource type.
        """
        return pulumi.get(self, 'type')