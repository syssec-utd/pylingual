import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['FluxConfigurationArgs', 'FluxConfiguration']

@pulumi.input_type
class FluxConfigurationArgs:

    def __init__(__self__, *, cluster_name: pulumi.Input[str], cluster_resource_name: pulumi.Input[str], cluster_rp: pulumi.Input[str], resource_group_name: pulumi.Input[str], configuration_protected_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, flux_configuration_name: Optional[pulumi.Input[str]]=None, git_repository: Optional[pulumi.Input['GitRepositoryDefinitionArgs']]=None, kustomizations: Optional[pulumi.Input[Mapping[str, pulumi.Input['KustomizationDefinitionArgs']]]]=None, namespace: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[Union[str, 'ScopeType']]]=None, source_kind: Optional[pulumi.Input[Union[str, 'SourceKindType']]]=None, suspend: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a FluxConfiguration resource.
        :param pulumi.Input[str] cluster_name: The name of the kubernetes cluster.
        :param pulumi.Input[str] cluster_resource_name: The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        :param pulumi.Input[str] cluster_rp: The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] configuration_protected_settings: Key-value pairs of protected configuration settings for the configuration
        :param pulumi.Input[str] flux_configuration_name: Name of the Flux Configuration.
        :param pulumi.Input['GitRepositoryDefinitionArgs'] git_repository: Parameters to reconcile to the GitRepository source kind type.
        :param pulumi.Input[Mapping[str, pulumi.Input['KustomizationDefinitionArgs']]] kustomizations: Array of kustomizations used to reconcile the artifact pulled by the source type on the cluster.
        :param pulumi.Input[str] namespace: The namespace to which this configuration is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        :param pulumi.Input[Union[str, 'ScopeType']] scope: Scope at which the operator will be installed.
        :param pulumi.Input[Union[str, 'SourceKindType']] source_kind: Source Kind to pull the configuration data from.
        :param pulumi.Input[bool] suspend: Whether this configuration should suspend its reconciliation of its kustomizations and sources.
        """
        pulumi.set(__self__, 'cluster_name', cluster_name)
        pulumi.set(__self__, 'cluster_resource_name', cluster_resource_name)
        pulumi.set(__self__, 'cluster_rp', cluster_rp)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if configuration_protected_settings is not None:
            pulumi.set(__self__, 'configuration_protected_settings', configuration_protected_settings)
        if flux_configuration_name is not None:
            pulumi.set(__self__, 'flux_configuration_name', flux_configuration_name)
        if git_repository is not None:
            pulumi.set(__self__, 'git_repository', git_repository)
        if kustomizations is not None:
            pulumi.set(__self__, 'kustomizations', kustomizations)
        if namespace is None:
            namespace = 'default'
        if namespace is not None:
            pulumi.set(__self__, 'namespace', namespace)
        if scope is not None:
            pulumi.set(__self__, 'scope', scope)
        if source_kind is not None:
            pulumi.set(__self__, 'source_kind', source_kind)
        if suspend is None:
            suspend = False
        if suspend is not None:
            pulumi.set(__self__, 'suspend', suspend)

    @property
    @pulumi.getter(name='clusterName')
    def cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the kubernetes cluster.
        """
        return pulumi.get(self, 'cluster_name')

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'cluster_name', value)

    @property
    @pulumi.getter(name='clusterResourceName')
    def cluster_resource_name(self) -> pulumi.Input[str]:
        """
        The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        """
        return pulumi.get(self, 'cluster_resource_name')

    @cluster_resource_name.setter
    def cluster_resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'cluster_resource_name', value)

    @property
    @pulumi.getter(name='clusterRp')
    def cluster_rp(self) -> pulumi.Input[str]:
        """
        The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        """
        return pulumi.get(self, 'cluster_rp')

    @cluster_rp.setter
    def cluster_rp(self, value: pulumi.Input[str]):
        pulumi.set(self, 'cluster_rp', value)

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
    @pulumi.getter(name='configurationProtectedSettings')
    def configuration_protected_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of protected configuration settings for the configuration
        """
        return pulumi.get(self, 'configuration_protected_settings')

    @configuration_protected_settings.setter
    def configuration_protected_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'configuration_protected_settings', value)

    @property
    @pulumi.getter(name='fluxConfigurationName')
    def flux_configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Flux Configuration.
        """
        return pulumi.get(self, 'flux_configuration_name')

    @flux_configuration_name.setter
    def flux_configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'flux_configuration_name', value)

    @property
    @pulumi.getter(name='gitRepository')
    def git_repository(self) -> Optional[pulumi.Input['GitRepositoryDefinitionArgs']]:
        """
        Parameters to reconcile to the GitRepository source kind type.
        """
        return pulumi.get(self, 'git_repository')

    @git_repository.setter
    def git_repository(self, value: Optional[pulumi.Input['GitRepositoryDefinitionArgs']]):
        pulumi.set(self, 'git_repository', value)

    @property
    @pulumi.getter
    def kustomizations(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['KustomizationDefinitionArgs']]]]:
        """
        Array of kustomizations used to reconcile the artifact pulled by the source type on the cluster.
        """
        return pulumi.get(self, 'kustomizations')

    @kustomizations.setter
    def kustomizations(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['KustomizationDefinitionArgs']]]]):
        pulumi.set(self, 'kustomizations', value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to which this configuration is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        """
        return pulumi.get(self, 'namespace')

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace', value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[Union[str, 'ScopeType']]]:
        """
        Scope at which the operator will be installed.
        """
        return pulumi.get(self, 'scope')

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[Union[str, 'ScopeType']]]):
        pulumi.set(self, 'scope', value)

    @property
    @pulumi.getter(name='sourceKind')
    def source_kind(self) -> Optional[pulumi.Input[Union[str, 'SourceKindType']]]:
        """
        Source Kind to pull the configuration data from.
        """
        return pulumi.get(self, 'source_kind')

    @source_kind.setter
    def source_kind(self, value: Optional[pulumi.Input[Union[str, 'SourceKindType']]]):
        pulumi.set(self, 'source_kind', value)

    @property
    @pulumi.getter
    def suspend(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this configuration should suspend its reconciliation of its kustomizations and sources.
        """
        return pulumi.get(self, 'suspend')

    @suspend.setter
    def suspend(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'suspend', value)

class FluxConfiguration(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cluster_name: Optional[pulumi.Input[str]]=None, cluster_resource_name: Optional[pulumi.Input[str]]=None, cluster_rp: Optional[pulumi.Input[str]]=None, configuration_protected_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, flux_configuration_name: Optional[pulumi.Input[str]]=None, git_repository: Optional[pulumi.Input[pulumi.InputType['GitRepositoryDefinitionArgs']]]=None, kustomizations: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['KustomizationDefinitionArgs']]]]]=None, namespace: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[Union[str, 'ScopeType']]]=None, source_kind: Optional[pulumi.Input[Union[str, 'SourceKindType']]]=None, suspend: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        The Flux Configuration object returned in Get & Put response.
        API Version: 2021-11-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the kubernetes cluster.
        :param pulumi.Input[str] cluster_resource_name: The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        :param pulumi.Input[str] cluster_rp: The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] configuration_protected_settings: Key-value pairs of protected configuration settings for the configuration
        :param pulumi.Input[str] flux_configuration_name: Name of the Flux Configuration.
        :param pulumi.Input[pulumi.InputType['GitRepositoryDefinitionArgs']] git_repository: Parameters to reconcile to the GitRepository source kind type.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['KustomizationDefinitionArgs']]]] kustomizations: Array of kustomizations used to reconcile the artifact pulled by the source type on the cluster.
        :param pulumi.Input[str] namespace: The namespace to which this configuration is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Union[str, 'ScopeType']] scope: Scope at which the operator will be installed.
        :param pulumi.Input[Union[str, 'SourceKindType']] source_kind: Source Kind to pull the configuration data from.
        :param pulumi.Input[bool] suspend: Whether this configuration should suspend its reconciliation of its kustomizations and sources.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: FluxConfigurationArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The Flux Configuration object returned in Get & Put response.
        API Version: 2021-11-01-preview.

        :param str resource_name: The name of the resource.
        :param FluxConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(FluxConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cluster_name: Optional[pulumi.Input[str]]=None, cluster_resource_name: Optional[pulumi.Input[str]]=None, cluster_rp: Optional[pulumi.Input[str]]=None, configuration_protected_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, flux_configuration_name: Optional[pulumi.Input[str]]=None, git_repository: Optional[pulumi.Input[pulumi.InputType['GitRepositoryDefinitionArgs']]]=None, kustomizations: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['KustomizationDefinitionArgs']]]]]=None, namespace: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[Union[str, 'ScopeType']]]=None, source_kind: Optional[pulumi.Input[Union[str, 'SourceKindType']]]=None, suspend: Optional[pulumi.Input[bool]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FluxConfigurationArgs.__new__(FluxConfigurationArgs)
            if cluster_name is None and (not opts.urn):
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__['cluster_name'] = cluster_name
            if cluster_resource_name is None and (not opts.urn):
                raise TypeError("Missing required property 'cluster_resource_name'")
            __props__.__dict__['cluster_resource_name'] = cluster_resource_name
            if cluster_rp is None and (not opts.urn):
                raise TypeError("Missing required property 'cluster_rp'")
            __props__.__dict__['cluster_rp'] = cluster_rp
            __props__.__dict__['configuration_protected_settings'] = configuration_protected_settings
            __props__.__dict__['flux_configuration_name'] = flux_configuration_name
            __props__.__dict__['git_repository'] = git_repository
            __props__.__dict__['kustomizations'] = kustomizations
            if namespace is None:
                namespace = 'default'
            __props__.__dict__['namespace'] = namespace
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['scope'] = scope
            __props__.__dict__['source_kind'] = source_kind
            if suspend is None:
                suspend = False
            __props__.__dict__['suspend'] = suspend
            __props__.__dict__['compliance_state'] = None
            __props__.__dict__['error_message'] = None
            __props__.__dict__['last_source_synced_at'] = None
            __props__.__dict__['last_source_synced_commit_id'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['repository_public_key'] = None
            __props__.__dict__['statuses'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:kubernetesconfiguration/v20211101preview:FluxConfiguration'), pulumi.Alias(type_='azure-native:kubernetesconfiguration/v20220101preview:FluxConfiguration'), pulumi.Alias(type_='azure-native:kubernetesconfiguration/v20220301:FluxConfiguration'), pulumi.Alias(type_='azure-native:kubernetesconfiguration/v20220701:FluxConfiguration'), pulumi.Alias(type_='azure-native:kubernetesconfiguration/v20221101:FluxConfiguration')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FluxConfiguration, __self__).__init__('azure-native:kubernetesconfiguration:FluxConfiguration', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'FluxConfiguration':
        """
        Get an existing FluxConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = FluxConfigurationArgs.__new__(FluxConfigurationArgs)
        __props__.__dict__['compliance_state'] = None
        __props__.__dict__['configuration_protected_settings'] = None
        __props__.__dict__['error_message'] = None
        __props__.__dict__['git_repository'] = None
        __props__.__dict__['kustomizations'] = None
        __props__.__dict__['last_source_synced_at'] = None
        __props__.__dict__['last_source_synced_commit_id'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['namespace'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['repository_public_key'] = None
        __props__.__dict__['scope'] = None
        __props__.__dict__['source_kind'] = None
        __props__.__dict__['statuses'] = None
        __props__.__dict__['suspend'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return FluxConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='complianceState')
    def compliance_state(self) -> pulumi.Output[str]:
        """
        Combined status of the Flux Kubernetes resources created by the fluxConfiguration or created by the managed objects.
        """
        return pulumi.get(self, 'compliance_state')

    @property
    @pulumi.getter(name='configurationProtectedSettings')
    def configuration_protected_settings(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value pairs of protected configuration settings for the configuration
        """
        return pulumi.get(self, 'configuration_protected_settings')

    @property
    @pulumi.getter(name='errorMessage')
    def error_message(self) -> pulumi.Output[str]:
        """
        Error message returned to the user in the case of provisioning failure.
        """
        return pulumi.get(self, 'error_message')

    @property
    @pulumi.getter(name='gitRepository')
    def git_repository(self) -> pulumi.Output[Optional['outputs.GitRepositoryDefinitionResponse']]:
        """
        Parameters to reconcile to the GitRepository source kind type.
        """
        return pulumi.get(self, 'git_repository')

    @property
    @pulumi.getter
    def kustomizations(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.KustomizationDefinitionResponse']]]:
        """
        Array of kustomizations used to reconcile the artifact pulled by the source type on the cluster.
        """
        return pulumi.get(self, 'kustomizations')

    @property
    @pulumi.getter(name='lastSourceSyncedAt')
    def last_source_synced_at(self) -> pulumi.Output[str]:
        """
        Datetime the fluxConfiguration last synced its source on the cluster.
        """
        return pulumi.get(self, 'last_source_synced_at')

    @property
    @pulumi.getter(name='lastSourceSyncedCommitId')
    def last_source_synced_commit_id(self) -> pulumi.Output[str]:
        """
        Branch and SHA of the last source commit synced with the cluster.
        """
        return pulumi.get(self, 'last_source_synced_commit_id')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to which this configuration is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        """
        return pulumi.get(self, 'namespace')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Status of the creation of the fluxConfiguration.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='repositoryPublicKey')
    def repository_public_key(self) -> pulumi.Output[str]:
        """
        Public Key associated with this fluxConfiguration (either generated within the cluster or provided by the user).
        """
        return pulumi.get(self, 'repository_public_key')

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Optional[str]]:
        """
        Scope at which the operator will be installed.
        """
        return pulumi.get(self, 'scope')

    @property
    @pulumi.getter(name='sourceKind')
    def source_kind(self) -> pulumi.Output[Optional[str]]:
        """
        Source Kind to pull the configuration data from.
        """
        return pulumi.get(self, 'source_kind')

    @property
    @pulumi.getter
    def statuses(self) -> pulumi.Output[Sequence['outputs.ObjectStatusDefinitionResponse']]:
        """
        Statuses of the Flux Kubernetes resources created by the fluxConfiguration or created by the managed objects provisioned by the fluxConfiguration.
        """
        return pulumi.get(self, 'statuses')

    @property
    @pulumi.getter
    def suspend(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether this configuration should suspend its reconciliation of its kustomizations and sources.
        """
        return pulumi.get(self, 'suspend')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Top level metadata https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/common-api-contracts.md#system-metadata-for-all-azure-resources
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')