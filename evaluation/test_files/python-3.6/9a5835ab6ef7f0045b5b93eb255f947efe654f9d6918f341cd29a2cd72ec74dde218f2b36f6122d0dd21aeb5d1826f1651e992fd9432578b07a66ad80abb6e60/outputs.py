import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['ApiPortalCustomDomainPropertiesResponse', 'ApiPortalInstanceResponse', 'ApiPortalPropertiesResponse', 'ApiPortalResourceRequestsResponse', 'AppResourcePropertiesResponse', 'ApplicationInsightsAgentVersionsResponse', 'AzureFileVolumeResponse', 'BindingResourcePropertiesResponse', 'BuildResultUserSourceInfoResponse', 'BuildServiceAgentPoolPropertiesResponse', 'BuildServiceAgentPoolSizePropertiesResponse', 'BuilderPropertiesResponse', 'BuildpackBindingLaunchPropertiesResponse', 'BuildpackBindingPropertiesResponse', 'BuildpackPropertiesResponse', 'BuildpacksGroupPropertiesResponse', 'ClusterResourcePropertiesResponse', 'ConfigServerGitPropertyResponse', 'ConfigServerPropertiesResponse', 'ConfigServerSettingsResponse', 'ConfigurationServiceGitPropertyResponse', 'ConfigurationServiceGitRepositoryResponse', 'ConfigurationServiceInstanceResponse', 'ConfigurationServicePropertiesResponse', 'ConfigurationServiceResourceRequestsResponse', 'ConfigurationServiceSettingsResponse', 'ContainerProbeSettingsResponse', 'ContentCertificatePropertiesResponse', 'CustomContainerResponse', 'CustomContainerUserSourceInfoResponse', 'CustomDomainPropertiesResponse', 'CustomPersistentDiskResourceResponse', 'DeploymentInstanceResponse', 'DeploymentResourcePropertiesResponse', 'DeploymentSettingsResponse', 'ErrorResponse', 'GatewayApiMetadataPropertiesResponse', 'GatewayApiRouteResponse', 'GatewayCorsPropertiesResponse', 'GatewayCustomDomainPropertiesResponse', 'GatewayInstanceResponse', 'GatewayOperatorPropertiesResponse', 'GatewayOperatorResourceRequestsResponse', 'GatewayPropertiesResponse', 'GatewayResourceRequestsResponse', 'GatewayRouteConfigPropertiesResponse', 'GitPatternRepositoryResponse', 'ImageRegistryCredentialResponse', 'JarUploadedUserSourceInfoResponse', 'KeyVaultCertificatePropertiesResponse', 'LoadedCertificateResponse', 'ManagedIdentityPropertiesResponse', 'MonitoringSettingPropertiesResponse', 'NetCoreZipUploadedUserSourceInfoResponse', 'NetworkProfileResponse', 'NetworkProfileResponseOutboundIPs', 'PersistentDiskResponse', 'RequiredTrafficResponse', 'ResourceRequestsResponse', 'ServiceRegistryInstanceResponse', 'ServiceRegistryPropertiesResponse', 'ServiceRegistryResourceRequestsResponse', 'SkuResponse', 'SourceUploadedUserSourceInfoResponse', 'SsoPropertiesResponse', 'StackPropertiesResponse', 'StorageAccountResponse', 'SystemDataResponse', 'TemporaryDiskResponse', 'UploadedUserSourceInfoResponse', 'UserAssignedManagedIdentityResponse']

@pulumi.output_type
class ApiPortalCustomDomainPropertiesResponse(dict):
    """
    The properties of custom domain for API portal
    """

    def __init__(__self__, *, thumbprint: Optional[str]=None):
        """
        The properties of custom domain for API portal
        :param str thumbprint: The thumbprint of bound certificate.
        """
        if thumbprint is not None:
            pulumi.set(__self__, 'thumbprint', thumbprint)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[str]:
        """
        The thumbprint of bound certificate.
        """
        return pulumi.get(self, 'thumbprint')

@pulumi.output_type
class ApiPortalInstanceResponse(dict):
    """
    Collection of instances belong to the API portal
    """

    def __init__(__self__, *, name: str, status: str):
        """
        Collection of instances belong to the API portal
        :param str name: Name of the API portal instance
        :param str status: Status of the API portal instance
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the API portal instance
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the API portal instance
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class ApiPortalPropertiesResponse(dict):
    """
    API portal properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'resourceRequests':
            suggest = 'resource_requests'
        elif key == 'gatewayIds':
            suggest = 'gateway_ids'
        elif key == 'httpsOnly':
            suggest = 'https_only'
        elif key == 'sourceUrls':
            suggest = 'source_urls'
        elif key == 'ssoProperties':
            suggest = 'sso_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApiPortalPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApiPortalPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ApiPortalPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.ApiPortalInstanceResponse'], provisioning_state: str, resource_requests: 'outputs.ApiPortalResourceRequestsResponse', url: str, gateway_ids: Optional[Sequence[str]]=None, https_only: Optional[bool]=None, public: Optional[bool]=None, source_urls: Optional[Sequence[str]]=None, sso_properties: Optional['outputs.SsoPropertiesResponse']=None):
        """
        API portal properties payload
        :param Sequence['ApiPortalInstanceResponse'] instances: Collection of instances belong to API portal.
        :param str provisioning_state: State of the API portal.
        :param 'ApiPortalResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory.
        :param str url: URL of the API portal, exposed when 'public' is true.
        :param Sequence[str] gateway_ids: The array of resource Ids of gateway to integrate with API portal.
        :param bool https_only: Indicate if only https is allowed.
        :param bool public: Indicates whether the API portal exposes endpoint.
        :param Sequence[str] source_urls: Collection of OpenAPI source URL locations.
        :param 'SsoPropertiesResponse' sso_properties: Single sign-on related configuration
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'resource_requests', resource_requests)
        pulumi.set(__self__, 'url', url)
        if gateway_ids is not None:
            pulumi.set(__self__, 'gateway_ids', gateway_ids)
        if https_only is None:
            https_only = False
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if public is None:
            public = False
        if public is not None:
            pulumi.set(__self__, 'public', public)
        if source_urls is not None:
            pulumi.set(__self__, 'source_urls', source_urls)
        if sso_properties is not None:
            pulumi.set(__self__, 'sso_properties', sso_properties)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.ApiPortalInstanceResponse']:
        """
        Collection of instances belong to API portal.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the API portal.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> 'outputs.ApiPortalResourceRequestsResponse':
        """
        The requested resource quantity for required CPU and Memory.
        """
        return pulumi.get(self, 'resource_requests')

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        URL of the API portal, exposed when 'public' is true.
        """
        return pulumi.get(self, 'url')

    @property
    @pulumi.getter(name='gatewayIds')
    def gateway_ids(self) -> Optional[Sequence[str]]:
        """
        The array of resource Ids of gateway to integrate with API portal.
        """
        return pulumi.get(self, 'gateway_ids')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[bool]:
        """
        Indicate if only https is allowed.
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter
    def public(self) -> Optional[bool]:
        """
        Indicates whether the API portal exposes endpoint.
        """
        return pulumi.get(self, 'public')

    @property
    @pulumi.getter(name='sourceUrls')
    def source_urls(self) -> Optional[Sequence[str]]:
        """
        Collection of OpenAPI source URL locations.
        """
        return pulumi.get(self, 'source_urls')

    @property
    @pulumi.getter(name='ssoProperties')
    def sso_properties(self) -> Optional['outputs.SsoPropertiesResponse']:
        """
        Single sign-on related configuration
        """
        return pulumi.get(self, 'sso_properties')

@pulumi.output_type
class ApiPortalResourceRequestsResponse(dict):
    """
    Resource requests of the API portal
    """

    def __init__(__self__, *, cpu: str, memory: str):
        """
        Resource requests of the API portal
        :param str cpu: Cpu allocated to each API portal instance
        :param str memory: Memory allocated to each API portal instance
        """
        pulumi.set(__self__, 'cpu', cpu)
        pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> str:
        """
        Cpu allocated to each API portal instance
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter
    def memory(self) -> str:
        """
        Memory allocated to each API portal instance
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class AppResourcePropertiesResponse(dict):
    """
    App resource properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'addonConfigs':
            suggest = 'addon_configs'
        elif key == 'customPersistentDisks':
            suggest = 'custom_persistent_disks'
        elif key == 'enableEndToEndTLS':
            suggest = 'enable_end_to_end_tls'
        elif key == 'httpsOnly':
            suggest = 'https_only'
        elif key == 'loadedCertificates':
            suggest = 'loaded_certificates'
        elif key == 'persistentDisk':
            suggest = 'persistent_disk'
        elif key == 'temporaryDisk':
            suggest = 'temporary_disk'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppResourcePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppResourcePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AppResourcePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, url: str, addon_configs: Optional[Mapping[str, Mapping[str, Any]]]=None, custom_persistent_disks: Optional[Sequence['outputs.CustomPersistentDiskResourceResponse']]=None, enable_end_to_end_tls: Optional[bool]=None, fqdn: Optional[str]=None, https_only: Optional[bool]=None, loaded_certificates: Optional[Sequence['outputs.LoadedCertificateResponse']]=None, persistent_disk: Optional['outputs.PersistentDiskResponse']=None, public: Optional[bool]=None, temporary_disk: Optional['outputs.TemporaryDiskResponse']=None):
        """
        App resource properties payload
        :param str provisioning_state: Provisioning state of the App
        :param str url: URL of the App
        :param Mapping[str, Mapping[str, Any]] addon_configs: Collection of addons
        :param Sequence['CustomPersistentDiskResourceResponse'] custom_persistent_disks: List of custom persistent disks
        :param bool enable_end_to_end_tls: Indicate if end to end TLS is enabled.
        :param str fqdn: Fully qualified dns Name.
        :param bool https_only: Indicate if only https is allowed.
        :param Sequence['LoadedCertificateResponse'] loaded_certificates: Collection of loaded certificates
        :param 'PersistentDiskResponse' persistent_disk: Persistent disk settings
        :param bool public: Indicates whether the App exposes public endpoint
        :param 'TemporaryDiskResponse' temporary_disk: Temporary disk settings
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'url', url)
        if addon_configs is not None:
            pulumi.set(__self__, 'addon_configs', addon_configs)
        if custom_persistent_disks is not None:
            pulumi.set(__self__, 'custom_persistent_disks', custom_persistent_disks)
        if enable_end_to_end_tls is None:
            enable_end_to_end_tls = False
        if enable_end_to_end_tls is not None:
            pulumi.set(__self__, 'enable_end_to_end_tls', enable_end_to_end_tls)
        if fqdn is not None:
            pulumi.set(__self__, 'fqdn', fqdn)
        if https_only is None:
            https_only = False
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if loaded_certificates is not None:
            pulumi.set(__self__, 'loaded_certificates', loaded_certificates)
        if persistent_disk is not None:
            pulumi.set(__self__, 'persistent_disk', persistent_disk)
        if public is not None:
            pulumi.set(__self__, 'public', public)
        if temporary_disk is not None:
            pulumi.set(__self__, 'temporary_disk', temporary_disk)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the App
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        URL of the App
        """
        return pulumi.get(self, 'url')

    @property
    @pulumi.getter(name='addonConfigs')
    def addon_configs(self) -> Optional[Mapping[str, Mapping[str, Any]]]:
        """
        Collection of addons
        """
        return pulumi.get(self, 'addon_configs')

    @property
    @pulumi.getter(name='customPersistentDisks')
    def custom_persistent_disks(self) -> Optional[Sequence['outputs.CustomPersistentDiskResourceResponse']]:
        """
        List of custom persistent disks
        """
        return pulumi.get(self, 'custom_persistent_disks')

    @property
    @pulumi.getter(name='enableEndToEndTLS')
    def enable_end_to_end_tls(self) -> Optional[bool]:
        """
        Indicate if end to end TLS is enabled.
        """
        return pulumi.get(self, 'enable_end_to_end_tls')

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        Fully qualified dns Name.
        """
        return pulumi.get(self, 'fqdn')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[bool]:
        """
        Indicate if only https is allowed.
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter(name='loadedCertificates')
    def loaded_certificates(self) -> Optional[Sequence['outputs.LoadedCertificateResponse']]:
        """
        Collection of loaded certificates
        """
        return pulumi.get(self, 'loaded_certificates')

    @property
    @pulumi.getter(name='persistentDisk')
    def persistent_disk(self) -> Optional['outputs.PersistentDiskResponse']:
        """
        Persistent disk settings
        """
        return pulumi.get(self, 'persistent_disk')

    @property
    @pulumi.getter
    def public(self) -> Optional[bool]:
        """
        Indicates whether the App exposes public endpoint
        """
        return pulumi.get(self, 'public')

    @property
    @pulumi.getter(name='temporaryDisk')
    def temporary_disk(self) -> Optional['outputs.TemporaryDiskResponse']:
        """
        Temporary disk settings
        """
        return pulumi.get(self, 'temporary_disk')

@pulumi.output_type
class ApplicationInsightsAgentVersionsResponse(dict):
    """
    Application Insights agent versions properties payload
    """

    def __init__(__self__, *, java: str):
        """
        Application Insights agent versions properties payload
        :param str java: Indicates the version of application insight java agent
        """
        pulumi.set(__self__, 'java', java)

    @property
    @pulumi.getter
    def java(self) -> str:
        """
        Indicates the version of application insight java agent
        """
        return pulumi.get(self, 'java')

@pulumi.output_type
class AzureFileVolumeResponse(dict):
    """
    The properties of the Azure File volume. Azure File shares are mounted as volumes.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'mountPath':
            suggest = 'mount_path'
        elif key == 'shareName':
            suggest = 'share_name'
        elif key == 'mountOptions':
            suggest = 'mount_options'
        elif key == 'readOnly':
            suggest = 'read_only'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzureFileVolumeResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzureFileVolumeResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AzureFileVolumeResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, mount_path: str, share_name: str, type: str, mount_options: Optional[Sequence[str]]=None, read_only: Optional[bool]=None):
        """
        The properties of the Azure File volume. Azure File shares are mounted as volumes.
        :param str mount_path: The mount path of the persistent disk.
        :param str share_name: The share name of the Azure File share.
        :param str type: The type of the underlying resource to mount as a persistent disk.
               Expected value is 'AzureFileVolume'.
        :param Sequence[str] mount_options: These are the mount options for a persistent disk.
        :param bool read_only: Indicates whether the persistent disk is a readOnly one.
        """
        pulumi.set(__self__, 'mount_path', mount_path)
        pulumi.set(__self__, 'share_name', share_name)
        pulumi.set(__self__, 'type', 'AzureFileVolume')
        if mount_options is not None:
            pulumi.set(__self__, 'mount_options', mount_options)
        if read_only is not None:
            pulumi.set(__self__, 'read_only', read_only)

    @property
    @pulumi.getter(name='mountPath')
    def mount_path(self) -> str:
        """
        The mount path of the persistent disk.
        """
        return pulumi.get(self, 'mount_path')

    @property
    @pulumi.getter(name='shareName')
    def share_name(self) -> str:
        """
        The share name of the Azure File share.
        """
        return pulumi.get(self, 'share_name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the underlying resource to mount as a persistent disk.
        Expected value is 'AzureFileVolume'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='mountOptions')
    def mount_options(self) -> Optional[Sequence[str]]:
        """
        These are the mount options for a persistent disk.
        """
        return pulumi.get(self, 'mount_options')

    @property
    @pulumi.getter(name='readOnly')
    def read_only(self) -> Optional[bool]:
        """
        Indicates whether the persistent disk is a readOnly one.
        """
        return pulumi.get(self, 'read_only')

@pulumi.output_type
class BindingResourcePropertiesResponse(dict):
    """
    Binding resource properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'createdAt':
            suggest = 'created_at'
        elif key == 'generatedProperties':
            suggest = 'generated_properties'
        elif key == 'resourceName':
            suggest = 'resource_name'
        elif key == 'resourceType':
            suggest = 'resource_type'
        elif key == 'updatedAt':
            suggest = 'updated_at'
        elif key == 'bindingParameters':
            suggest = 'binding_parameters'
        elif key == 'resourceId':
            suggest = 'resource_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BindingResourcePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BindingResourcePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        BindingResourcePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, created_at: str, generated_properties: str, resource_name: str, resource_type: str, updated_at: str, binding_parameters: Optional[Mapping[str, Any]]=None, key: Optional[str]=None, resource_id: Optional[str]=None):
        """
        Binding resource properties payload
        :param str created_at: Creation time of the Binding resource
        :param str generated_properties: The generated Spring Boot property file for this binding. The secret will be deducted.
        :param str resource_name: The name of the bound resource
        :param str resource_type: The standard Azure resource type of the bound resource
        :param str updated_at: Update time of the Binding resource
        :param Mapping[str, Any] binding_parameters: Binding parameters of the Binding resource
        :param str key: The key of the bound resource
        :param str resource_id: The Azure resource id of the bound resource
        """
        pulumi.set(__self__, 'created_at', created_at)
        pulumi.set(__self__, 'generated_properties', generated_properties)
        pulumi.set(__self__, 'resource_name', resource_name)
        pulumi.set(__self__, 'resource_type', resource_type)
        pulumi.set(__self__, 'updated_at', updated_at)
        if binding_parameters is not None:
            pulumi.set(__self__, 'binding_parameters', binding_parameters)
        if key is not None:
            pulumi.set(__self__, 'key', key)
        if resource_id is not None:
            pulumi.set(__self__, 'resource_id', resource_id)

    @property
    @pulumi.getter(name='createdAt')
    def created_at(self) -> str:
        """
        Creation time of the Binding resource
        """
        return pulumi.get(self, 'created_at')

    @property
    @pulumi.getter(name='generatedProperties')
    def generated_properties(self) -> str:
        """
        The generated Spring Boot property file for this binding. The secret will be deducted.
        """
        return pulumi.get(self, 'generated_properties')

    @property
    @pulumi.getter(name='resourceName')
    def resource_name(self) -> str:
        """
        The name of the bound resource
        """
        return pulumi.get(self, 'resource_name')

    @property
    @pulumi.getter(name='resourceType')
    def resource_type(self) -> str:
        """
        The standard Azure resource type of the bound resource
        """
        return pulumi.get(self, 'resource_type')

    @property
    @pulumi.getter(name='updatedAt')
    def updated_at(self) -> str:
        """
        Update time of the Binding resource
        """
        return pulumi.get(self, 'updated_at')

    @property
    @pulumi.getter(name='bindingParameters')
    def binding_parameters(self) -> Optional[Mapping[str, Any]]:
        """
        Binding parameters of the Binding resource
        """
        return pulumi.get(self, 'binding_parameters')

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The key of the bound resource
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> Optional[str]:
        """
        The Azure resource id of the bound resource
        """
        return pulumi.get(self, 'resource_id')

@pulumi.output_type
class BuildResultUserSourceInfoResponse(dict):
    """
    Reference to a build result
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'buildResultId':
            suggest = 'build_result_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BuildResultUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BuildResultUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        BuildResultUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, build_result_id: Optional[str]=None, version: Optional[str]=None):
        """
        Reference to a build result
        :param str type: Type of the source uploaded
               Expected value is 'BuildResult'.
        :param str build_result_id: Resource id of an existing succeeded build result under the same Spring instance.
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'BuildResult')
        if build_result_id is not None:
            pulumi.set(__self__, 'build_result_id', build_result_id)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'BuildResult'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='buildResultId')
    def build_result_id(self) -> Optional[str]:
        """
        Resource id of an existing succeeded build result under the same Spring instance.
        """
        return pulumi.get(self, 'build_result_id')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class BuildServiceAgentPoolPropertiesResponse(dict):
    """
    Build service agent pool properties
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'poolSize':
            suggest = 'pool_size'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BuildServiceAgentPoolPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BuildServiceAgentPoolPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        BuildServiceAgentPoolPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, pool_size: Optional['outputs.BuildServiceAgentPoolSizePropertiesResponse']=None):
        """
        Build service agent pool properties
        :param str provisioning_state: Provisioning state of the build service agent pool
        :param 'BuildServiceAgentPoolSizePropertiesResponse' pool_size: build service agent pool size properties
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if pool_size is not None:
            pulumi.set(__self__, 'pool_size', pool_size)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the build service agent pool
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='poolSize')
    def pool_size(self) -> Optional['outputs.BuildServiceAgentPoolSizePropertiesResponse']:
        """
        build service agent pool size properties
        """
        return pulumi.get(self, 'pool_size')

@pulumi.output_type
class BuildServiceAgentPoolSizePropertiesResponse(dict):
    """
    Build service agent pool size properties
    """

    def __init__(__self__, *, cpu: str, memory: str, name: Optional[str]=None):
        """
        Build service agent pool size properties
        :param str cpu: The cpu property of build service agent pool size
        :param str memory: The memory property of build service agent pool size
        :param str name: The name of build service agent pool size
        """
        pulumi.set(__self__, 'cpu', cpu)
        pulumi.set(__self__, 'memory', memory)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def cpu(self) -> str:
        """
        The cpu property of build service agent pool size
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter
    def memory(self) -> str:
        """
        The memory property of build service agent pool size
        """
        return pulumi.get(self, 'memory')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of build service agent pool size
        """
        return pulumi.get(self, 'name')

@pulumi.output_type
class BuilderPropertiesResponse(dict):
    """
    KPack Builder properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'buildpackGroups':
            suggest = 'buildpack_groups'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BuilderPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BuilderPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        BuilderPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, buildpack_groups: Optional[Sequence['outputs.BuildpacksGroupPropertiesResponse']]=None, stack: Optional['outputs.StackPropertiesResponse']=None):
        """
        KPack Builder properties payload
        :param str provisioning_state: Builder provision status.
        :param Sequence['BuildpacksGroupPropertiesResponse'] buildpack_groups: Builder buildpack groups.
        :param 'StackPropertiesResponse' stack: Builder cluster stack property.
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if buildpack_groups is not None:
            pulumi.set(__self__, 'buildpack_groups', buildpack_groups)
        if stack is not None:
            pulumi.set(__self__, 'stack', stack)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Builder provision status.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='buildpackGroups')
    def buildpack_groups(self) -> Optional[Sequence['outputs.BuildpacksGroupPropertiesResponse']]:
        """
        Builder buildpack groups.
        """
        return pulumi.get(self, 'buildpack_groups')

    @property
    @pulumi.getter
    def stack(self) -> Optional['outputs.StackPropertiesResponse']:
        """
        Builder cluster stack property.
        """
        return pulumi.get(self, 'stack')

@pulumi.output_type
class BuildpackBindingLaunchPropertiesResponse(dict):
    """
    Buildpack Binding Launch Properties
    """

    def __init__(__self__, *, properties: Optional[Mapping[str, str]]=None, secrets: Optional[Mapping[str, str]]=None):
        """
        Buildpack Binding Launch Properties
        :param Mapping[str, str] properties: Non-sensitive properties for launchProperties
        :param Mapping[str, str] secrets: Sensitive properties for launchProperties
        """
        if properties is not None:
            pulumi.set(__self__, 'properties', properties)
        if secrets is not None:
            pulumi.set(__self__, 'secrets', secrets)

    @property
    @pulumi.getter
    def properties(self) -> Optional[Mapping[str, str]]:
        """
        Non-sensitive properties for launchProperties
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def secrets(self) -> Optional[Mapping[str, str]]:
        """
        Sensitive properties for launchProperties
        """
        return pulumi.get(self, 'secrets')

@pulumi.output_type
class BuildpackBindingPropertiesResponse(dict):
    """
    Properties of a buildpack binding
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'bindingType':
            suggest = 'binding_type'
        elif key == 'launchProperties':
            suggest = 'launch_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BuildpackBindingPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BuildpackBindingPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        BuildpackBindingPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, binding_type: Optional[str]=None, launch_properties: Optional['outputs.BuildpackBindingLaunchPropertiesResponse']=None):
        """
        Properties of a buildpack binding
        :param str provisioning_state: State of the Buildpack Binding.
        :param str binding_type: Buildpack Binding Type
        :param 'BuildpackBindingLaunchPropertiesResponse' launch_properties: The object describes the buildpack binding launch properties
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if binding_type is not None:
            pulumi.set(__self__, 'binding_type', binding_type)
        if launch_properties is not None:
            pulumi.set(__self__, 'launch_properties', launch_properties)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Buildpack Binding.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='bindingType')
    def binding_type(self) -> Optional[str]:
        """
        Buildpack Binding Type
        """
        return pulumi.get(self, 'binding_type')

    @property
    @pulumi.getter(name='launchProperties')
    def launch_properties(self) -> Optional['outputs.BuildpackBindingLaunchPropertiesResponse']:
        """
        The object describes the buildpack binding launch properties
        """
        return pulumi.get(self, 'launch_properties')

@pulumi.output_type
class BuildpackPropertiesResponse(dict):
    """
    Buildpack properties payload
    """

    def __init__(__self__, *, id: Optional[str]=None):
        """
        Buildpack properties payload
        :param str id: Id of the buildpack
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Id of the buildpack
        """
        return pulumi.get(self, 'id')

@pulumi.output_type
class BuildpacksGroupPropertiesResponse(dict):
    """
    Buildpack group properties of the Builder
    """

    def __init__(__self__, *, buildpacks: Optional[Sequence['outputs.BuildpackPropertiesResponse']]=None, name: Optional[str]=None):
        """
        Buildpack group properties of the Builder
        :param Sequence['BuildpackPropertiesResponse'] buildpacks: Buildpacks in the buildpack group
        :param str name: Buildpack group name
        """
        if buildpacks is not None:
            pulumi.set(__self__, 'buildpacks', buildpacks)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def buildpacks(self) -> Optional[Sequence['outputs.BuildpackPropertiesResponse']]:
        """
        Buildpacks in the buildpack group
        """
        return pulumi.get(self, 'buildpacks')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Buildpack group name
        """
        return pulumi.get(self, 'name')

@pulumi.output_type
class ClusterResourcePropertiesResponse(dict):
    """
    Service properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'powerState':
            suggest = 'power_state'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'serviceId':
            suggest = 'service_id'
        elif key == 'networkProfile':
            suggest = 'network_profile'
        elif key == 'zoneRedundant':
            suggest = 'zone_redundant'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterResourcePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterResourcePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ClusterResourcePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, fqdn: str, power_state: str, provisioning_state: str, service_id: str, version: int, network_profile: Optional['outputs.NetworkProfileResponse']=None, zone_redundant: Optional[bool]=None):
        """
        Service properties payload
        :param str fqdn: Fully qualified dns name of the service instance
        :param str power_state: Power state of the Service
        :param str provisioning_state: Provisioning state of the Service
        :param str service_id: ServiceInstanceEntity GUID which uniquely identifies a created resource
        :param int version: Version of the Service
        :param 'NetworkProfileResponse' network_profile: Network profile of the Service
        """
        pulumi.set(__self__, 'fqdn', fqdn)
        pulumi.set(__self__, 'power_state', power_state)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'service_id', service_id)
        pulumi.set(__self__, 'version', version)
        if network_profile is not None:
            pulumi.set(__self__, 'network_profile', network_profile)
        if zone_redundant is None:
            zone_redundant = False
        if zone_redundant is not None:
            pulumi.set(__self__, 'zone_redundant', zone_redundant)

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        Fully qualified dns name of the service instance
        """
        return pulumi.get(self, 'fqdn')

    @property
    @pulumi.getter(name='powerState')
    def power_state(self) -> str:
        """
        Power state of the Service
        """
        return pulumi.get(self, 'power_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Service
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='serviceId')
    def service_id(self) -> str:
        """
        ServiceInstanceEntity GUID which uniquely identifies a created resource
        """
        return pulumi.get(self, 'service_id')

    @property
    @pulumi.getter
    def version(self) -> int:
        """
        Version of the Service
        """
        return pulumi.get(self, 'version')

    @property
    @pulumi.getter(name='networkProfile')
    def network_profile(self) -> Optional['outputs.NetworkProfileResponse']:
        """
        Network profile of the Service
        """
        return pulumi.get(self, 'network_profile')

    @property
    @pulumi.getter(name='zoneRedundant')
    def zone_redundant(self) -> Optional[bool]:
        return pulumi.get(self, 'zone_redundant')

@pulumi.output_type
class ConfigServerGitPropertyResponse(dict):
    """
    Property of git.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'hostKey':
            suggest = 'host_key'
        elif key == 'hostKeyAlgorithm':
            suggest = 'host_key_algorithm'
        elif key == 'privateKey':
            suggest = 'private_key'
        elif key == 'searchPaths':
            suggest = 'search_paths'
        elif key == 'strictHostKeyChecking':
            suggest = 'strict_host_key_checking'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigServerGitPropertyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigServerGitPropertyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigServerGitPropertyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, uri: str, host_key: Optional[str]=None, host_key_algorithm: Optional[str]=None, label: Optional[str]=None, password: Optional[str]=None, private_key: Optional[str]=None, repositories: Optional[Sequence['outputs.GitPatternRepositoryResponse']]=None, search_paths: Optional[Sequence[str]]=None, strict_host_key_checking: Optional[bool]=None, username: Optional[str]=None):
        """
        Property of git.
        :param str uri: URI of the repository
        :param str host_key: Public sshKey of git repository.
        :param str host_key_algorithm: SshKey algorithm of git repository.
        :param str label: Label of the repository
        :param str password: Password of git repository basic auth.
        :param str private_key: Private sshKey algorithm of git repository.
        :param Sequence['GitPatternRepositoryResponse'] repositories: Repositories of git.
        :param Sequence[str] search_paths: Searching path of the repository
        :param bool strict_host_key_checking: Strict host key checking or not.
        :param str username: Username of git repository basic auth.
        """
        pulumi.set(__self__, 'uri', uri)
        if host_key is not None:
            pulumi.set(__self__, 'host_key', host_key)
        if host_key_algorithm is not None:
            pulumi.set(__self__, 'host_key_algorithm', host_key_algorithm)
        if label is not None:
            pulumi.set(__self__, 'label', label)
        if password is not None:
            pulumi.set(__self__, 'password', password)
        if private_key is not None:
            pulumi.set(__self__, 'private_key', private_key)
        if repositories is not None:
            pulumi.set(__self__, 'repositories', repositories)
        if search_paths is not None:
            pulumi.set(__self__, 'search_paths', search_paths)
        if strict_host_key_checking is not None:
            pulumi.set(__self__, 'strict_host_key_checking', strict_host_key_checking)
        if username is not None:
            pulumi.set(__self__, 'username', username)

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        URI of the repository
        """
        return pulumi.get(self, 'uri')

    @property
    @pulumi.getter(name='hostKey')
    def host_key(self) -> Optional[str]:
        """
        Public sshKey of git repository.
        """
        return pulumi.get(self, 'host_key')

    @property
    @pulumi.getter(name='hostKeyAlgorithm')
    def host_key_algorithm(self) -> Optional[str]:
        """
        SshKey algorithm of git repository.
        """
        return pulumi.get(self, 'host_key_algorithm')

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        Label of the repository
        """
        return pulumi.get(self, 'label')

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Password of git repository basic auth.
        """
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter(name='privateKey')
    def private_key(self) -> Optional[str]:
        """
        Private sshKey algorithm of git repository.
        """
        return pulumi.get(self, 'private_key')

    @property
    @pulumi.getter
    def repositories(self) -> Optional[Sequence['outputs.GitPatternRepositoryResponse']]:
        """
        Repositories of git.
        """
        return pulumi.get(self, 'repositories')

    @property
    @pulumi.getter(name='searchPaths')
    def search_paths(self) -> Optional[Sequence[str]]:
        """
        Searching path of the repository
        """
        return pulumi.get(self, 'search_paths')

    @property
    @pulumi.getter(name='strictHostKeyChecking')
    def strict_host_key_checking(self) -> Optional[bool]:
        """
        Strict host key checking or not.
        """
        return pulumi.get(self, 'strict_host_key_checking')

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of git repository basic auth.
        """
        return pulumi.get(self, 'username')

@pulumi.output_type
class ConfigServerPropertiesResponse(dict):
    """
    Config server git properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'configServer':
            suggest = 'config_server'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigServerPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigServerPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigServerPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, config_server: Optional['outputs.ConfigServerSettingsResponse']=None, error: Optional['outputs.ErrorResponse']=None):
        """
        Config server git properties payload
        :param str provisioning_state: State of the config server.
        :param 'ConfigServerSettingsResponse' config_server: Settings of config server.
        :param 'ErrorResponse' error: Error when apply config server settings.
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if config_server is not None:
            pulumi.set(__self__, 'config_server', config_server)
        if error is not None:
            pulumi.set(__self__, 'error', error)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the config server.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='configServer')
    def config_server(self) -> Optional['outputs.ConfigServerSettingsResponse']:
        """
        Settings of config server.
        """
        return pulumi.get(self, 'config_server')

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.ErrorResponse']:
        """
        Error when apply config server settings.
        """
        return pulumi.get(self, 'error')

@pulumi.output_type
class ConfigServerSettingsResponse(dict):
    """
    The settings of config server.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'gitProperty':
            suggest = 'git_property'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigServerSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigServerSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigServerSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, git_property: Optional['outputs.ConfigServerGitPropertyResponse']=None):
        """
        The settings of config server.
        :param 'ConfigServerGitPropertyResponse' git_property: Property of git environment.
        """
        if git_property is not None:
            pulumi.set(__self__, 'git_property', git_property)

    @property
    @pulumi.getter(name='gitProperty')
    def git_property(self) -> Optional['outputs.ConfigServerGitPropertyResponse']:
        """
        Property of git environment.
        """
        return pulumi.get(self, 'git_property')

@pulumi.output_type
class ConfigurationServiceGitPropertyResponse(dict):
    """
    Property of git environment.
    """

    def __init__(__self__, *, repositories: Optional[Sequence['outputs.ConfigurationServiceGitRepositoryResponse']]=None):
        """
        Property of git environment.
        :param Sequence['ConfigurationServiceGitRepositoryResponse'] repositories: Repositories of Application Configuration Service git property.
        """
        if repositories is not None:
            pulumi.set(__self__, 'repositories', repositories)

    @property
    @pulumi.getter
    def repositories(self) -> Optional[Sequence['outputs.ConfigurationServiceGitRepositoryResponse']]:
        """
        Repositories of Application Configuration Service git property.
        """
        return pulumi.get(self, 'repositories')

@pulumi.output_type
class ConfigurationServiceGitRepositoryResponse(dict):
    """
    Git repository property payload for Application Configuration Service
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'hostKey':
            suggest = 'host_key'
        elif key == 'hostKeyAlgorithm':
            suggest = 'host_key_algorithm'
        elif key == 'privateKey':
            suggest = 'private_key'
        elif key == 'searchPaths':
            suggest = 'search_paths'
        elif key == 'strictHostKeyChecking':
            suggest = 'strict_host_key_checking'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationServiceGitRepositoryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationServiceGitRepositoryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigurationServiceGitRepositoryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, label: str, name: str, patterns: Sequence[str], uri: str, host_key: Optional[str]=None, host_key_algorithm: Optional[str]=None, password: Optional[str]=None, private_key: Optional[str]=None, search_paths: Optional[Sequence[str]]=None, strict_host_key_checking: Optional[bool]=None, username: Optional[str]=None):
        """
        Git repository property payload for Application Configuration Service
        :param str label: Label of the repository
        :param str name: Name of the repository
        :param Sequence[str] patterns: Collection of patterns of the repository
        :param str uri: URI of the repository
        :param str host_key: Public sshKey of git repository.
        :param str host_key_algorithm: SshKey algorithm of git repository.
        :param str password: Password of git repository basic auth.
        :param str private_key: Private sshKey algorithm of git repository.
        :param Sequence[str] search_paths: Searching path of the repository
        :param bool strict_host_key_checking: Strict host key checking or not.
        :param str username: Username of git repository basic auth.
        """
        pulumi.set(__self__, 'label', label)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'patterns', patterns)
        pulumi.set(__self__, 'uri', uri)
        if host_key is not None:
            pulumi.set(__self__, 'host_key', host_key)
        if host_key_algorithm is not None:
            pulumi.set(__self__, 'host_key_algorithm', host_key_algorithm)
        if password is not None:
            pulumi.set(__self__, 'password', password)
        if private_key is not None:
            pulumi.set(__self__, 'private_key', private_key)
        if search_paths is not None:
            pulumi.set(__self__, 'search_paths', search_paths)
        if strict_host_key_checking is not None:
            pulumi.set(__self__, 'strict_host_key_checking', strict_host_key_checking)
        if username is not None:
            pulumi.set(__self__, 'username', username)

    @property
    @pulumi.getter
    def label(self) -> str:
        """
        Label of the repository
        """
        return pulumi.get(self, 'label')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the repository
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def patterns(self) -> Sequence[str]:
        """
        Collection of patterns of the repository
        """
        return pulumi.get(self, 'patterns')

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        URI of the repository
        """
        return pulumi.get(self, 'uri')

    @property
    @pulumi.getter(name='hostKey')
    def host_key(self) -> Optional[str]:
        """
        Public sshKey of git repository.
        """
        return pulumi.get(self, 'host_key')

    @property
    @pulumi.getter(name='hostKeyAlgorithm')
    def host_key_algorithm(self) -> Optional[str]:
        """
        SshKey algorithm of git repository.
        """
        return pulumi.get(self, 'host_key_algorithm')

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Password of git repository basic auth.
        """
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter(name='privateKey')
    def private_key(self) -> Optional[str]:
        """
        Private sshKey algorithm of git repository.
        """
        return pulumi.get(self, 'private_key')

    @property
    @pulumi.getter(name='searchPaths')
    def search_paths(self) -> Optional[Sequence[str]]:
        """
        Searching path of the repository
        """
        return pulumi.get(self, 'search_paths')

    @property
    @pulumi.getter(name='strictHostKeyChecking')
    def strict_host_key_checking(self) -> Optional[bool]:
        """
        Strict host key checking or not.
        """
        return pulumi.get(self, 'strict_host_key_checking')

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of git repository basic auth.
        """
        return pulumi.get(self, 'username')

@pulumi.output_type
class ConfigurationServiceInstanceResponse(dict):
    """
    Collection of instances belong to the Application Configuration Service
    """

    def __init__(__self__, *, name: str, status: str):
        """
        Collection of instances belong to the Application Configuration Service
        :param str name: Name of the Application Configuration Service instance
        :param str status: Status of the Application Configuration Service instance
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Application Configuration Service instance
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Application Configuration Service instance
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class ConfigurationServicePropertiesResponse(dict):
    """
    Application Configuration Service properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'resourceRequests':
            suggest = 'resource_requests'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationServicePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationServicePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigurationServicePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.ConfigurationServiceInstanceResponse'], provisioning_state: str, resource_requests: 'outputs.ConfigurationServiceResourceRequestsResponse', settings: Optional['outputs.ConfigurationServiceSettingsResponse']=None):
        """
        Application Configuration Service properties payload
        :param Sequence['ConfigurationServiceInstanceResponse'] instances: Collection of instances belong to Application Configuration Service.
        :param str provisioning_state: State of the Application Configuration Service.
        :param 'ConfigurationServiceResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory.
        :param 'ConfigurationServiceSettingsResponse' settings: The settings of Application Configuration Service.
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'resource_requests', resource_requests)
        if settings is not None:
            pulumi.set(__self__, 'settings', settings)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.ConfigurationServiceInstanceResponse']:
        """
        Collection of instances belong to Application Configuration Service.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Application Configuration Service.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> 'outputs.ConfigurationServiceResourceRequestsResponse':
        """
        The requested resource quantity for required CPU and Memory.
        """
        return pulumi.get(self, 'resource_requests')

    @property
    @pulumi.getter
    def settings(self) -> Optional['outputs.ConfigurationServiceSettingsResponse']:
        """
        The settings of Application Configuration Service.
        """
        return pulumi.get(self, 'settings')

@pulumi.output_type
class ConfigurationServiceResourceRequestsResponse(dict):
    """
    Resource request payload of Application Configuration Service
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'instanceCount':
            suggest = 'instance_count'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationServiceResourceRequestsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationServiceResourceRequestsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigurationServiceResourceRequestsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, cpu: str, instance_count: int, memory: str):
        """
        Resource request payload of Application Configuration Service
        :param str cpu: Cpu allocated to each Application Configuration Service instance
        :param int instance_count: Instance count of the Application Configuration Service
        :param str memory: Memory allocated to each Application Configuration Service instance
        """
        pulumi.set(__self__, 'cpu', cpu)
        pulumi.set(__self__, 'instance_count', instance_count)
        pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> str:
        """
        Cpu allocated to each Application Configuration Service instance
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter(name='instanceCount')
    def instance_count(self) -> int:
        """
        Instance count of the Application Configuration Service
        """
        return pulumi.get(self, 'instance_count')

    @property
    @pulumi.getter
    def memory(self) -> str:
        """
        Memory allocated to each Application Configuration Service instance
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class ConfigurationServiceSettingsResponse(dict):
    """
    The settings of Application Configuration Service.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'gitProperty':
            suggest = 'git_property'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationServiceSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationServiceSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ConfigurationServiceSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, git_property: Optional['outputs.ConfigurationServiceGitPropertyResponse']=None):
        """
        The settings of Application Configuration Service.
        :param 'ConfigurationServiceGitPropertyResponse' git_property: Property of git environment.
        """
        if git_property is not None:
            pulumi.set(__self__, 'git_property', git_property)

    @property
    @pulumi.getter(name='gitProperty')
    def git_property(self) -> Optional['outputs.ConfigurationServiceGitPropertyResponse']:
        """
        Property of git environment.
        """
        return pulumi.get(self, 'git_property')

@pulumi.output_type
class ContainerProbeSettingsResponse(dict):
    """
    Container liveness and readiness probe settings
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'disableProbe':
            suggest = 'disable_probe'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerProbeSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerProbeSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContainerProbeSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, disable_probe: Optional[bool]=None):
        """
        Container liveness and readiness probe settings
        :param bool disable_probe: Indicates whether disable the liveness and readiness probe
        """
        if disable_probe is not None:
            pulumi.set(__self__, 'disable_probe', disable_probe)

    @property
    @pulumi.getter(name='disableProbe')
    def disable_probe(self) -> Optional[bool]:
        """
        Indicates whether disable the liveness and readiness probe
        """
        return pulumi.get(self, 'disable_probe')

@pulumi.output_type
class ContentCertificatePropertiesResponse(dict):
    """
    Properties of certificate imported from key vault.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'activateDate':
            suggest = 'activate_date'
        elif key == 'dnsNames':
            suggest = 'dns_names'
        elif key == 'expirationDate':
            suggest = 'expiration_date'
        elif key == 'issuedDate':
            suggest = 'issued_date'
        elif key == 'subjectName':
            suggest = 'subject_name'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContentCertificatePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContentCertificatePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContentCertificatePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, activate_date: str, dns_names: Sequence[str], expiration_date: str, issued_date: str, issuer: str, subject_name: str, thumbprint: str, type: str):
        """
        Properties of certificate imported from key vault.
        :param str activate_date: The activate date of certificate.
        :param Sequence[str] dns_names: The domain list of certificate.
        :param str expiration_date: The expiration date of certificate.
        :param str issued_date: The issue date of certificate.
        :param str issuer: The issuer of certificate.
        :param str subject_name: The subject name of certificate.
        :param str thumbprint: The thumbprint of certificate.
        :param str type: The type of the certificate source.
               Expected value is 'ContentCertificate'.
        """
        pulumi.set(__self__, 'activate_date', activate_date)
        pulumi.set(__self__, 'dns_names', dns_names)
        pulumi.set(__self__, 'expiration_date', expiration_date)
        pulumi.set(__self__, 'issued_date', issued_date)
        pulumi.set(__self__, 'issuer', issuer)
        pulumi.set(__self__, 'subject_name', subject_name)
        pulumi.set(__self__, 'thumbprint', thumbprint)
        pulumi.set(__self__, 'type', 'ContentCertificate')

    @property
    @pulumi.getter(name='activateDate')
    def activate_date(self) -> str:
        """
        The activate date of certificate.
        """
        return pulumi.get(self, 'activate_date')

    @property
    @pulumi.getter(name='dnsNames')
    def dns_names(self) -> Sequence[str]:
        """
        The domain list of certificate.
        """
        return pulumi.get(self, 'dns_names')

    @property
    @pulumi.getter(name='expirationDate')
    def expiration_date(self) -> str:
        """
        The expiration date of certificate.
        """
        return pulumi.get(self, 'expiration_date')

    @property
    @pulumi.getter(name='issuedDate')
    def issued_date(self) -> str:
        """
        The issue date of certificate.
        """
        return pulumi.get(self, 'issued_date')

    @property
    @pulumi.getter
    def issuer(self) -> str:
        """
        The issuer of certificate.
        """
        return pulumi.get(self, 'issuer')

    @property
    @pulumi.getter(name='subjectName')
    def subject_name(self) -> str:
        """
        The subject name of certificate.
        """
        return pulumi.get(self, 'subject_name')

    @property
    @pulumi.getter
    def thumbprint(self) -> str:
        """
        The thumbprint of certificate.
        """
        return pulumi.get(self, 'thumbprint')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the certificate source.
        Expected value is 'ContentCertificate'.
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class CustomContainerResponse(dict):
    """
    Custom container payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'containerImage':
            suggest = 'container_image'
        elif key == 'imageRegistryCredential':
            suggest = 'image_registry_credential'
        elif key == 'languageFramework':
            suggest = 'language_framework'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomContainerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomContainerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CustomContainerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, args: Optional[Sequence[str]]=None, command: Optional[Sequence[str]]=None, container_image: Optional[str]=None, image_registry_credential: Optional['outputs.ImageRegistryCredentialResponse']=None, language_framework: Optional[str]=None, server: Optional[str]=None):
        """
        Custom container payload
        :param Sequence[str] args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided.
        :param Sequence[str] command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided.
        :param str container_image: Container image of the custom container. This should be in the form of <repository>:<tag> without the server name of the registry
        :param 'ImageRegistryCredentialResponse' image_registry_credential: Credential of the image registry
        :param str language_framework: Language framework of the container image uploaded
        :param str server: The name of the registry that contains the container image
        """
        if args is not None:
            pulumi.set(__self__, 'args', args)
        if command is not None:
            pulumi.set(__self__, 'command', command)
        if container_image is not None:
            pulumi.set(__self__, 'container_image', container_image)
        if image_registry_credential is not None:
            pulumi.set(__self__, 'image_registry_credential', image_registry_credential)
        if language_framework is not None:
            pulumi.set(__self__, 'language_framework', language_framework)
        if server is not None:
            pulumi.set(__self__, 'server', server)

    @property
    @pulumi.getter
    def args(self) -> Optional[Sequence[str]]:
        """
        Arguments to the entrypoint. The docker image's CMD is used if this is not provided.
        """
        return pulumi.get(self, 'args')

    @property
    @pulumi.getter
    def command(self) -> Optional[Sequence[str]]:
        """
        Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided.
        """
        return pulumi.get(self, 'command')

    @property
    @pulumi.getter(name='containerImage')
    def container_image(self) -> Optional[str]:
        """
        Container image of the custom container. This should be in the form of <repository>:<tag> without the server name of the registry
        """
        return pulumi.get(self, 'container_image')

    @property
    @pulumi.getter(name='imageRegistryCredential')
    def image_registry_credential(self) -> Optional['outputs.ImageRegistryCredentialResponse']:
        """
        Credential of the image registry
        """
        return pulumi.get(self, 'image_registry_credential')

    @property
    @pulumi.getter(name='languageFramework')
    def language_framework(self) -> Optional[str]:
        """
        Language framework of the container image uploaded
        """
        return pulumi.get(self, 'language_framework')

    @property
    @pulumi.getter
    def server(self) -> Optional[str]:
        """
        The name of the registry that contains the container image
        """
        return pulumi.get(self, 'server')

@pulumi.output_type
class CustomContainerUserSourceInfoResponse(dict):
    """
    Custom container user source info
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'customContainer':
            suggest = 'custom_container'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomContainerUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomContainerUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CustomContainerUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, custom_container: Optional['outputs.CustomContainerResponse']=None, version: Optional[str]=None):
        """
        Custom container user source info
        :param str type: Type of the source uploaded
               Expected value is 'Container'.
        :param 'CustomContainerResponse' custom_container: Custom container payload
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'Container')
        if custom_container is not None:
            pulumi.set(__self__, 'custom_container', custom_container)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'Container'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='customContainer')
    def custom_container(self) -> Optional['outputs.CustomContainerResponse']:
        """
        Custom container payload
        """
        return pulumi.get(self, 'custom_container')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class CustomDomainPropertiesResponse(dict):
    """
    Custom domain of app resource payload.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'appName':
            suggest = 'app_name'
        elif key == 'certName':
            suggest = 'cert_name'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomDomainPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomDomainPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CustomDomainPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, app_name: str, cert_name: Optional[str]=None, thumbprint: Optional[str]=None):
        """
        Custom domain of app resource payload.
        :param str app_name: The app name of domain.
        :param str cert_name: The bound certificate name of domain.
        :param str thumbprint: The thumbprint of bound certificate.
        """
        pulumi.set(__self__, 'app_name', app_name)
        if cert_name is not None:
            pulumi.set(__self__, 'cert_name', cert_name)
        if thumbprint is not None:
            pulumi.set(__self__, 'thumbprint', thumbprint)

    @property
    @pulumi.getter(name='appName')
    def app_name(self) -> str:
        """
        The app name of domain.
        """
        return pulumi.get(self, 'app_name')

    @property
    @pulumi.getter(name='certName')
    def cert_name(self) -> Optional[str]:
        """
        The bound certificate name of domain.
        """
        return pulumi.get(self, 'cert_name')

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[str]:
        """
        The thumbprint of bound certificate.
        """
        return pulumi.get(self, 'thumbprint')

@pulumi.output_type
class CustomPersistentDiskResourceResponse(dict):
    """
    Custom persistent disk resource payload.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'storageId':
            suggest = 'storage_id'
        elif key == 'customPersistentDiskProperties':
            suggest = 'custom_persistent_disk_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CustomPersistentDiskResourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CustomPersistentDiskResourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CustomPersistentDiskResourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, storage_id: str, custom_persistent_disk_properties: Optional['outputs.AzureFileVolumeResponse']=None):
        """
        Custom persistent disk resource payload.
        :param str storage_id: The resource id of Azure Spring Cloud Storage resource.
        :param 'AzureFileVolumeResponse' custom_persistent_disk_properties: Properties of the custom persistent disk resource payload.
        """
        pulumi.set(__self__, 'storage_id', storage_id)
        if custom_persistent_disk_properties is not None:
            pulumi.set(__self__, 'custom_persistent_disk_properties', custom_persistent_disk_properties)

    @property
    @pulumi.getter(name='storageId')
    def storage_id(self) -> str:
        """
        The resource id of Azure Spring Cloud Storage resource.
        """
        return pulumi.get(self, 'storage_id')

    @property
    @pulumi.getter(name='customPersistentDiskProperties')
    def custom_persistent_disk_properties(self) -> Optional['outputs.AzureFileVolumeResponse']:
        """
        Properties of the custom persistent disk resource payload.
        """
        return pulumi.get(self, 'custom_persistent_disk_properties')

@pulumi.output_type
class DeploymentInstanceResponse(dict):
    """
    Deployment instance payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'discoveryStatus':
            suggest = 'discovery_status'
        elif key == 'startTime':
            suggest = 'start_time'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentInstanceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentInstanceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        DeploymentInstanceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, discovery_status: str, name: str, reason: str, start_time: str, status: str, zone: str):
        """
        Deployment instance payload
        :param str discovery_status: Discovery status of the deployment instance
        :param str name: Name of the deployment instance
        :param str reason: Failed reason of the deployment instance
        :param str start_time: Start time of the deployment instance
        :param str status: Status of the deployment instance
        :param str zone: Availability zone information of the deployment instance
        """
        pulumi.set(__self__, 'discovery_status', discovery_status)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'reason', reason)
        pulumi.set(__self__, 'start_time', start_time)
        pulumi.set(__self__, 'status', status)
        pulumi.set(__self__, 'zone', zone)

    @property
    @pulumi.getter(name='discoveryStatus')
    def discovery_status(self) -> str:
        """
        Discovery status of the deployment instance
        """
        return pulumi.get(self, 'discovery_status')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the deployment instance
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def reason(self) -> str:
        """
        Failed reason of the deployment instance
        """
        return pulumi.get(self, 'reason')

    @property
    @pulumi.getter(name='startTime')
    def start_time(self) -> str:
        """
        Start time of the deployment instance
        """
        return pulumi.get(self, 'start_time')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the deployment instance
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        Availability zone information of the deployment instance
        """
        return pulumi.get(self, 'zone')

@pulumi.output_type
class DeploymentResourcePropertiesResponse(dict):
    """
    Deployment resource properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'deploymentSettings':
            suggest = 'deployment_settings'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentResourcePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentResourcePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        DeploymentResourcePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.DeploymentInstanceResponse'], provisioning_state: str, status: str, active: Optional[bool]=None, deployment_settings: Optional['outputs.DeploymentSettingsResponse']=None, source: Optional[Any]=None):
        """
        Deployment resource properties payload
        :param Sequence['DeploymentInstanceResponse'] instances: Collection of instances belong to the Deployment
        :param str provisioning_state: Provisioning state of the Deployment
        :param str status: Status of the Deployment
        :param bool active: Indicates whether the Deployment is active
        :param 'DeploymentSettingsResponse' deployment_settings: Deployment settings of the Deployment
        :param Union['BuildResultUserSourceInfoResponse', 'CustomContainerUserSourceInfoResponse', 'JarUploadedUserSourceInfoResponse', 'NetCoreZipUploadedUserSourceInfoResponse', 'SourceUploadedUserSourceInfoResponse', 'UploadedUserSourceInfoResponse'] source: Uploaded source information of the deployment.
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'status', status)
        if active is not None:
            pulumi.set(__self__, 'active', active)
        if deployment_settings is not None:
            pulumi.set(__self__, 'deployment_settings', deployment_settings)
        if source is not None:
            pulumi.set(__self__, 'source', source)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.DeploymentInstanceResponse']:
        """
        Collection of instances belong to the Deployment
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Deployment
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Deployment
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def active(self) -> Optional[bool]:
        """
        Indicates whether the Deployment is active
        """
        return pulumi.get(self, 'active')

    @property
    @pulumi.getter(name='deploymentSettings')
    def deployment_settings(self) -> Optional['outputs.DeploymentSettingsResponse']:
        """
        Deployment settings of the Deployment
        """
        return pulumi.get(self, 'deployment_settings')

    @property
    @pulumi.getter
    def source(self) -> Optional[Any]:
        """
        Uploaded source information of the deployment.
        """
        return pulumi.get(self, 'source')

@pulumi.output_type
class DeploymentSettingsResponse(dict):
    """
    Deployment settings payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'addonConfigs':
            suggest = 'addon_configs'
        elif key == 'containerProbeSettings':
            suggest = 'container_probe_settings'
        elif key == 'environmentVariables':
            suggest = 'environment_variables'
        elif key == 'resourceRequests':
            suggest = 'resource_requests'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DeploymentSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DeploymentSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        DeploymentSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, addon_configs: Optional[Mapping[str, Mapping[str, Any]]]=None, container_probe_settings: Optional['outputs.ContainerProbeSettingsResponse']=None, environment_variables: Optional[Mapping[str, str]]=None, resource_requests: Optional['outputs.ResourceRequestsResponse']=None):
        """
        Deployment settings payload
        :param Mapping[str, Mapping[str, Any]] addon_configs: Collection of addons
        :param 'ContainerProbeSettingsResponse' container_probe_settings: Container liveness and readiness probe settings
        :param Mapping[str, str] environment_variables: Collection of environment variables
        :param 'ResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory. It is recommended that using this field to represent the required CPU and Memory, the old field cpu and memoryInGB will be deprecated later.
        """
        if addon_configs is not None:
            pulumi.set(__self__, 'addon_configs', addon_configs)
        if container_probe_settings is not None:
            pulumi.set(__self__, 'container_probe_settings', container_probe_settings)
        if environment_variables is not None:
            pulumi.set(__self__, 'environment_variables', environment_variables)
        if resource_requests is not None:
            pulumi.set(__self__, 'resource_requests', resource_requests)

    @property
    @pulumi.getter(name='addonConfigs')
    def addon_configs(self) -> Optional[Mapping[str, Mapping[str, Any]]]:
        """
        Collection of addons
        """
        return pulumi.get(self, 'addon_configs')

    @property
    @pulumi.getter(name='containerProbeSettings')
    def container_probe_settings(self) -> Optional['outputs.ContainerProbeSettingsResponse']:
        """
        Container liveness and readiness probe settings
        """
        return pulumi.get(self, 'container_probe_settings')

    @property
    @pulumi.getter(name='environmentVariables')
    def environment_variables(self) -> Optional[Mapping[str, str]]:
        """
        Collection of environment variables
        """
        return pulumi.get(self, 'environment_variables')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> Optional['outputs.ResourceRequestsResponse']:
        """
        The requested resource quantity for required CPU and Memory. It is recommended that using this field to represent the required CPU and Memory, the old field cpu and memoryInGB will be deprecated later.
        """
        return pulumi.get(self, 'resource_requests')

@pulumi.output_type
class ErrorResponse(dict):
    """
    The error code compose of code and message.
    """

    def __init__(__self__, *, code: Optional[str]=None, message: Optional[str]=None):
        """
        The error code compose of code and message.
        :param str code: The code of error.
        :param str message: The message of error.
        """
        if code is not None:
            pulumi.set(__self__, 'code', code)
        if message is not None:
            pulumi.set(__self__, 'message', message)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        The code of error.
        """
        return pulumi.get(self, 'code')

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        The message of error.
        """
        return pulumi.get(self, 'message')

@pulumi.output_type
class GatewayApiMetadataPropertiesResponse(dict):
    """
    API metadata property for Spring Cloud Gateway
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'serverUrl':
            suggest = 'server_url'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayApiMetadataPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayApiMetadataPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayApiMetadataPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, description: Optional[str]=None, documentation: Optional[str]=None, server_url: Optional[str]=None, title: Optional[str]=None, version: Optional[str]=None):
        """
        API metadata property for Spring Cloud Gateway
        :param str description: Detailed description of the APIs available on the Gateway instance (default: `Generated OpenAPI 3 document that describes the API routes configured.`)
        :param str documentation: Location of additional documentation for the APIs available on the Gateway instance
        :param str server_url: Base URL that API consumers will use to access APIs on the Gateway instance.
        :param str title: Title describing the context of the APIs available on the Gateway instance (default: `Spring Cloud Gateway for K8S`)
        :param str version: Version of APIs available on this Gateway instance (default: `unspecified`).
        """
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if documentation is not None:
            pulumi.set(__self__, 'documentation', documentation)
        if server_url is not None:
            pulumi.set(__self__, 'server_url', server_url)
        if title is not None:
            pulumi.set(__self__, 'title', title)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Detailed description of the APIs available on the Gateway instance (default: `Generated OpenAPI 3 document that describes the API routes configured.`)
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def documentation(self) -> Optional[str]:
        """
        Location of additional documentation for the APIs available on the Gateway instance
        """
        return pulumi.get(self, 'documentation')

    @property
    @pulumi.getter(name='serverUrl')
    def server_url(self) -> Optional[str]:
        """
        Base URL that API consumers will use to access APIs on the Gateway instance.
        """
        return pulumi.get(self, 'server_url')

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        Title describing the context of the APIs available on the Gateway instance (default: `Spring Cloud Gateway for K8S`)
        """
        return pulumi.get(self, 'title')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of APIs available on this Gateway instance (default: `unspecified`).
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class GatewayApiRouteResponse(dict):
    """
    API route config of the Spring Cloud Gateway
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'ssoEnabled':
            suggest = 'sso_enabled'
        elif key == 'tokenRelay':
            suggest = 'token_relay'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayApiRouteResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayApiRouteResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayApiRouteResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, description: Optional[str]=None, filters: Optional[Sequence[str]]=None, order: Optional[int]=None, predicates: Optional[Sequence[str]]=None, sso_enabled: Optional[bool]=None, tags: Optional[Sequence[str]]=None, title: Optional[str]=None, token_relay: Optional[bool]=None, uri: Optional[str]=None):
        """
        API route config of the Spring Cloud Gateway
        :param str description: A description, will be applied to methods in the generated OpenAPI documentation.
        :param Sequence[str] filters: To modify the request before sending it to the target endpoint, or the received response.
        :param int order: Route processing order.
        :param Sequence[str] predicates: A number of conditions to evaluate a route for each request. Each predicate may be evaluated against request headers and parameter values. All of the predicates associated with a route must evaluate to true for the route to be matched to the request.
        :param bool sso_enabled: Enable sso validation.
        :param Sequence[str] tags: Classification tags, will be applied to methods in the generated OpenAPI documentation.
        :param str title: A title, will be applied to methods in the generated OpenAPI documentation.
        :param bool token_relay: Pass currently-authenticated user's identity token to application service, default is 'false'
        :param str uri: Full uri, will override `appName`.
        """
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if filters is not None:
            pulumi.set(__self__, 'filters', filters)
        if order is not None:
            pulumi.set(__self__, 'order', order)
        if predicates is not None:
            pulumi.set(__self__, 'predicates', predicates)
        if sso_enabled is not None:
            pulumi.set(__self__, 'sso_enabled', sso_enabled)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if title is not None:
            pulumi.set(__self__, 'title', title)
        if token_relay is not None:
            pulumi.set(__self__, 'token_relay', token_relay)
        if uri is not None:
            pulumi.set(__self__, 'uri', uri)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description, will be applied to methods in the generated OpenAPI documentation.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence[str]]:
        """
        To modify the request before sending it to the target endpoint, or the received response.
        """
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def order(self) -> Optional[int]:
        """
        Route processing order.
        """
        return pulumi.get(self, 'order')

    @property
    @pulumi.getter
    def predicates(self) -> Optional[Sequence[str]]:
        """
        A number of conditions to evaluate a route for each request. Each predicate may be evaluated against request headers and parameter values. All of the predicates associated with a route must evaluate to true for the route to be matched to the request.
        """
        return pulumi.get(self, 'predicates')

    @property
    @pulumi.getter(name='ssoEnabled')
    def sso_enabled(self) -> Optional[bool]:
        """
        Enable sso validation.
        """
        return pulumi.get(self, 'sso_enabled')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence[str]]:
        """
        Classification tags, will be applied to methods in the generated OpenAPI documentation.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        A title, will be applied to methods in the generated OpenAPI documentation.
        """
        return pulumi.get(self, 'title')

    @property
    @pulumi.getter(name='tokenRelay')
    def token_relay(self) -> Optional[bool]:
        """
        Pass currently-authenticated user's identity token to application service, default is 'false'
        """
        return pulumi.get(self, 'token_relay')

    @property
    @pulumi.getter
    def uri(self) -> Optional[str]:
        """
        Full uri, will override `appName`.
        """
        return pulumi.get(self, 'uri')

@pulumi.output_type
class GatewayCorsPropertiesResponse(dict):
    """
    Cross-Origin Resource Sharing property
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'allowCredentials':
            suggest = 'allow_credentials'
        elif key == 'allowedHeaders':
            suggest = 'allowed_headers'
        elif key == 'allowedMethods':
            suggest = 'allowed_methods'
        elif key == 'allowedOrigins':
            suggest = 'allowed_origins'
        elif key == 'exposedHeaders':
            suggest = 'exposed_headers'
        elif key == 'maxAge':
            suggest = 'max_age'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayCorsPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayCorsPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayCorsPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, allow_credentials: Optional[bool]=None, allowed_headers: Optional[Sequence[str]]=None, allowed_methods: Optional[Sequence[str]]=None, allowed_origins: Optional[Sequence[str]]=None, exposed_headers: Optional[Sequence[str]]=None, max_age: Optional[int]=None):
        """
        Cross-Origin Resource Sharing property
        :param bool allow_credentials: Whether user credentials are supported on cross-site requests. Valid values: `true`, `false`.
        :param Sequence[str] allowed_headers: Allowed headers in cross-site requests. The special value `*` allows actual requests to send any header.
        :param Sequence[str] allowed_methods: Allowed HTTP methods on cross-site requests. The special value `*` allows all methods. If not set, `GET` and `HEAD` are allowed by default.
        :param Sequence[str] allowed_origins: Allowed origins to make cross-site requests. The special value `*` allows all domains.
        :param Sequence[str] exposed_headers: HTTP response headers to expose for cross-site requests.
        :param int max_age: How long, in seconds, the response from a pre-flight request can be cached by clients.
        """
        if allow_credentials is not None:
            pulumi.set(__self__, 'allow_credentials', allow_credentials)
        if allowed_headers is not None:
            pulumi.set(__self__, 'allowed_headers', allowed_headers)
        if allowed_methods is not None:
            pulumi.set(__self__, 'allowed_methods', allowed_methods)
        if allowed_origins is not None:
            pulumi.set(__self__, 'allowed_origins', allowed_origins)
        if exposed_headers is not None:
            pulumi.set(__self__, 'exposed_headers', exposed_headers)
        if max_age is not None:
            pulumi.set(__self__, 'max_age', max_age)

    @property
    @pulumi.getter(name='allowCredentials')
    def allow_credentials(self) -> Optional[bool]:
        """
        Whether user credentials are supported on cross-site requests. Valid values: `true`, `false`.
        """
        return pulumi.get(self, 'allow_credentials')

    @property
    @pulumi.getter(name='allowedHeaders')
    def allowed_headers(self) -> Optional[Sequence[str]]:
        """
        Allowed headers in cross-site requests. The special value `*` allows actual requests to send any header.
        """
        return pulumi.get(self, 'allowed_headers')

    @property
    @pulumi.getter(name='allowedMethods')
    def allowed_methods(self) -> Optional[Sequence[str]]:
        """
        Allowed HTTP methods on cross-site requests. The special value `*` allows all methods. If not set, `GET` and `HEAD` are allowed by default.
        """
        return pulumi.get(self, 'allowed_methods')

    @property
    @pulumi.getter(name='allowedOrigins')
    def allowed_origins(self) -> Optional[Sequence[str]]:
        """
        Allowed origins to make cross-site requests. The special value `*` allows all domains.
        """
        return pulumi.get(self, 'allowed_origins')

    @property
    @pulumi.getter(name='exposedHeaders')
    def exposed_headers(self) -> Optional[Sequence[str]]:
        """
        HTTP response headers to expose for cross-site requests.
        """
        return pulumi.get(self, 'exposed_headers')

    @property
    @pulumi.getter(name='maxAge')
    def max_age(self) -> Optional[int]:
        """
        How long, in seconds, the response from a pre-flight request can be cached by clients.
        """
        return pulumi.get(self, 'max_age')

@pulumi.output_type
class GatewayCustomDomainPropertiesResponse(dict):
    """
    The properties of custom domain for Spring Cloud Gateway
    """

    def __init__(__self__, *, thumbprint: Optional[str]=None):
        """
        The properties of custom domain for Spring Cloud Gateway
        :param str thumbprint: The thumbprint of bound certificate.
        """
        if thumbprint is not None:
            pulumi.set(__self__, 'thumbprint', thumbprint)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[str]:
        """
        The thumbprint of bound certificate.
        """
        return pulumi.get(self, 'thumbprint')

@pulumi.output_type
class GatewayInstanceResponse(dict):
    """
    Collection of instances belong to the Spring Cloud Gateway
    """

    def __init__(__self__, *, name: str, status: str):
        """
        Collection of instances belong to the Spring Cloud Gateway
        :param str name: Name of the Spring Cloud Gateway instance
        :param str status: Status of the Spring Cloud Gateway instance
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Spring Cloud Gateway instance
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Spring Cloud Gateway instance
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class GatewayOperatorPropertiesResponse(dict):
    """
    Properties of the Spring Cloud Gateway Operator.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'resourceRequests':
            suggest = 'resource_requests'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayOperatorPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayOperatorPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayOperatorPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.GatewayInstanceResponse'], resource_requests: 'outputs.GatewayOperatorResourceRequestsResponse'):
        """
        Properties of the Spring Cloud Gateway Operator.
        :param Sequence['GatewayInstanceResponse'] instances: Collection of instances belong to Spring Cloud Gateway operator.
        :param 'GatewayOperatorResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory.
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'resource_requests', resource_requests)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.GatewayInstanceResponse']:
        """
        Collection of instances belong to Spring Cloud Gateway operator.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> 'outputs.GatewayOperatorResourceRequestsResponse':
        """
        The requested resource quantity for required CPU and Memory.
        """
        return pulumi.get(self, 'resource_requests')

@pulumi.output_type
class GatewayOperatorResourceRequestsResponse(dict):
    """
    Properties of the Spring Cloud Gateway Operator.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'instanceCount':
            suggest = 'instance_count'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayOperatorResourceRequestsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayOperatorResourceRequestsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayOperatorResourceRequestsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, cpu: str, instance_count: int, memory: str):
        """
        Properties of the Spring Cloud Gateway Operator.
        :param str cpu: Cpu allocated to each Spring Cloud Gateway Operator instance.
        :param int instance_count: Instance count of the Spring Cloud Gateway Operator.
        :param str memory: Memory allocated to each Spring Cloud Gateway Operator instance.
        """
        pulumi.set(__self__, 'cpu', cpu)
        pulumi.set(__self__, 'instance_count', instance_count)
        pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> str:
        """
        Cpu allocated to each Spring Cloud Gateway Operator instance.
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter(name='instanceCount')
    def instance_count(self) -> int:
        """
        Instance count of the Spring Cloud Gateway Operator.
        """
        return pulumi.get(self, 'instance_count')

    @property
    @pulumi.getter
    def memory(self) -> str:
        """
        Memory allocated to each Spring Cloud Gateway Operator instance.
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class GatewayPropertiesResponse(dict):
    """
    Spring Cloud Gateway properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'operatorProperties':
            suggest = 'operator_properties'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'apiMetadataProperties':
            suggest = 'api_metadata_properties'
        elif key == 'corsProperties':
            suggest = 'cors_properties'
        elif key == 'httpsOnly':
            suggest = 'https_only'
        elif key == 'resourceRequests':
            suggest = 'resource_requests'
        elif key == 'ssoProperties':
            suggest = 'sso_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.GatewayInstanceResponse'], operator_properties: 'outputs.GatewayOperatorPropertiesResponse', provisioning_state: str, url: str, api_metadata_properties: Optional['outputs.GatewayApiMetadataPropertiesResponse']=None, cors_properties: Optional['outputs.GatewayCorsPropertiesResponse']=None, https_only: Optional[bool]=None, public: Optional[bool]=None, resource_requests: Optional['outputs.GatewayResourceRequestsResponse']=None, sso_properties: Optional['outputs.SsoPropertiesResponse']=None):
        """
        Spring Cloud Gateway properties payload
        :param Sequence['GatewayInstanceResponse'] instances: Collection of instances belong to Spring Cloud Gateway.
        :param 'GatewayOperatorPropertiesResponse' operator_properties: Properties of the Spring Cloud Gateway Operator.
        :param str provisioning_state: State of the Spring Cloud Gateway.
        :param str url: URL of the Spring Cloud Gateway, exposed when 'public' is true.
        :param 'GatewayApiMetadataPropertiesResponse' api_metadata_properties: API metadata property for Spring Cloud Gateway
        :param 'GatewayCorsPropertiesResponse' cors_properties: Cross-Origin Resource Sharing property
        :param bool https_only: Indicate if only https is allowed.
        :param bool public: Indicates whether the Spring Cloud Gateway exposes endpoint.
        :param 'GatewayResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory.
        :param 'SsoPropertiesResponse' sso_properties: Single sign-on related configuration
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'operator_properties', operator_properties)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'url', url)
        if api_metadata_properties is not None:
            pulumi.set(__self__, 'api_metadata_properties', api_metadata_properties)
        if cors_properties is not None:
            pulumi.set(__self__, 'cors_properties', cors_properties)
        if https_only is None:
            https_only = False
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if public is None:
            public = False
        if public is not None:
            pulumi.set(__self__, 'public', public)
        if resource_requests is not None:
            pulumi.set(__self__, 'resource_requests', resource_requests)
        if sso_properties is not None:
            pulumi.set(__self__, 'sso_properties', sso_properties)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.GatewayInstanceResponse']:
        """
        Collection of instances belong to Spring Cloud Gateway.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='operatorProperties')
    def operator_properties(self) -> 'outputs.GatewayOperatorPropertiesResponse':
        """
        Properties of the Spring Cloud Gateway Operator.
        """
        return pulumi.get(self, 'operator_properties')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Spring Cloud Gateway.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        URL of the Spring Cloud Gateway, exposed when 'public' is true.
        """
        return pulumi.get(self, 'url')

    @property
    @pulumi.getter(name='apiMetadataProperties')
    def api_metadata_properties(self) -> Optional['outputs.GatewayApiMetadataPropertiesResponse']:
        """
        API metadata property for Spring Cloud Gateway
        """
        return pulumi.get(self, 'api_metadata_properties')

    @property
    @pulumi.getter(name='corsProperties')
    def cors_properties(self) -> Optional['outputs.GatewayCorsPropertiesResponse']:
        """
        Cross-Origin Resource Sharing property
        """
        return pulumi.get(self, 'cors_properties')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[bool]:
        """
        Indicate if only https is allowed.
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter
    def public(self) -> Optional[bool]:
        """
        Indicates whether the Spring Cloud Gateway exposes endpoint.
        """
        return pulumi.get(self, 'public')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> Optional['outputs.GatewayResourceRequestsResponse']:
        """
        The requested resource quantity for required CPU and Memory.
        """
        return pulumi.get(self, 'resource_requests')

    @property
    @pulumi.getter(name='ssoProperties')
    def sso_properties(self) -> Optional['outputs.SsoPropertiesResponse']:
        """
        Single sign-on related configuration
        """
        return pulumi.get(self, 'sso_properties')

@pulumi.output_type
class GatewayResourceRequestsResponse(dict):
    """
    Resource request payload of Spring Cloud Gateway.
    """

    def __init__(__self__, *, cpu: Optional[str]=None, memory: Optional[str]=None):
        """
        Resource request payload of Spring Cloud Gateway.
        :param str cpu: Cpu allocated to each Spring Cloud Gateway instance.
        :param str memory: Memory allocated to each Spring Cloud Gateway instance.
        """
        if cpu is None:
            cpu = '1'
        if cpu is not None:
            pulumi.set(__self__, 'cpu', cpu)
        if memory is None:
            memory = '2Gi'
        if memory is not None:
            pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[str]:
        """
        Cpu allocated to each Spring Cloud Gateway instance.
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter
    def memory(self) -> Optional[str]:
        """
        Memory allocated to each Spring Cloud Gateway instance.
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class GatewayRouteConfigPropertiesResponse(dict):
    """
    API route config of the Spring Cloud Gateway
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'appResourceId':
            suggest = 'app_resource_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayRouteConfigPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayRouteConfigPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GatewayRouteConfigPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, app_resource_id: Optional[str]=None, routes: Optional[Sequence['outputs.GatewayApiRouteResponse']]=None):
        """
        API route config of the Spring Cloud Gateway
        :param str provisioning_state: State of the Spring Cloud Gateway route config.
        :param str app_resource_id: The resource Id of the Azure Spring Cloud app, required unless route defines `uri`.
        :param Sequence['GatewayApiRouteResponse'] routes: Array of API routes, each route contains properties such as `title`, `uri`, `ssoEnabled`, `predicates`, `filters`.
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if app_resource_id is not None:
            pulumi.set(__self__, 'app_resource_id', app_resource_id)
        if routes is not None:
            pulumi.set(__self__, 'routes', routes)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Spring Cloud Gateway route config.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='appResourceId')
    def app_resource_id(self) -> Optional[str]:
        """
        The resource Id of the Azure Spring Cloud app, required unless route defines `uri`.
        """
        return pulumi.get(self, 'app_resource_id')

    @property
    @pulumi.getter
    def routes(self) -> Optional[Sequence['outputs.GatewayApiRouteResponse']]:
        """
        Array of API routes, each route contains properties such as `title`, `uri`, `ssoEnabled`, `predicates`, `filters`.
        """
        return pulumi.get(self, 'routes')

@pulumi.output_type
class GitPatternRepositoryResponse(dict):
    """
    Git repository property payload for config server
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'hostKey':
            suggest = 'host_key'
        elif key == 'hostKeyAlgorithm':
            suggest = 'host_key_algorithm'
        elif key == 'privateKey':
            suggest = 'private_key'
        elif key == 'searchPaths':
            suggest = 'search_paths'
        elif key == 'strictHostKeyChecking':
            suggest = 'strict_host_key_checking'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GitPatternRepositoryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GitPatternRepositoryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GitPatternRepositoryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, name: str, uri: str, host_key: Optional[str]=None, host_key_algorithm: Optional[str]=None, label: Optional[str]=None, password: Optional[str]=None, pattern: Optional[Sequence[str]]=None, private_key: Optional[str]=None, search_paths: Optional[Sequence[str]]=None, strict_host_key_checking: Optional[bool]=None, username: Optional[str]=None):
        """
        Git repository property payload for config server
        :param str name: Name of the repository
        :param str uri: URI of the repository
        :param str host_key: Public sshKey of git repository.
        :param str host_key_algorithm: SshKey algorithm of git repository.
        :param str label: Label of the repository
        :param str password: Password of git repository basic auth.
        :param Sequence[str] pattern: Collection of pattern of the repository
        :param str private_key: Private sshKey algorithm of git repository.
        :param Sequence[str] search_paths: Searching path of the repository
        :param bool strict_host_key_checking: Strict host key checking or not.
        :param str username: Username of git repository basic auth.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'uri', uri)
        if host_key is not None:
            pulumi.set(__self__, 'host_key', host_key)
        if host_key_algorithm is not None:
            pulumi.set(__self__, 'host_key_algorithm', host_key_algorithm)
        if label is not None:
            pulumi.set(__self__, 'label', label)
        if password is not None:
            pulumi.set(__self__, 'password', password)
        if pattern is not None:
            pulumi.set(__self__, 'pattern', pattern)
        if private_key is not None:
            pulumi.set(__self__, 'private_key', private_key)
        if search_paths is not None:
            pulumi.set(__self__, 'search_paths', search_paths)
        if strict_host_key_checking is not None:
            pulumi.set(__self__, 'strict_host_key_checking', strict_host_key_checking)
        if username is not None:
            pulumi.set(__self__, 'username', username)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the repository
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        URI of the repository
        """
        return pulumi.get(self, 'uri')

    @property
    @pulumi.getter(name='hostKey')
    def host_key(self) -> Optional[str]:
        """
        Public sshKey of git repository.
        """
        return pulumi.get(self, 'host_key')

    @property
    @pulumi.getter(name='hostKeyAlgorithm')
    def host_key_algorithm(self) -> Optional[str]:
        """
        SshKey algorithm of git repository.
        """
        return pulumi.get(self, 'host_key_algorithm')

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        Label of the repository
        """
        return pulumi.get(self, 'label')

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Password of git repository basic auth.
        """
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter
    def pattern(self) -> Optional[Sequence[str]]:
        """
        Collection of pattern of the repository
        """
        return pulumi.get(self, 'pattern')

    @property
    @pulumi.getter(name='privateKey')
    def private_key(self) -> Optional[str]:
        """
        Private sshKey algorithm of git repository.
        """
        return pulumi.get(self, 'private_key')

    @property
    @pulumi.getter(name='searchPaths')
    def search_paths(self) -> Optional[Sequence[str]]:
        """
        Searching path of the repository
        """
        return pulumi.get(self, 'search_paths')

    @property
    @pulumi.getter(name='strictHostKeyChecking')
    def strict_host_key_checking(self) -> Optional[bool]:
        """
        Strict host key checking or not.
        """
        return pulumi.get(self, 'strict_host_key_checking')

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of git repository basic auth.
        """
        return pulumi.get(self, 'username')

@pulumi.output_type
class ImageRegistryCredentialResponse(dict):
    """
    Credential of the image registry
    """

    def __init__(__self__, *, password: Optional[str]=None, username: Optional[str]=None):
        """
        Credential of the image registry
        :param str password: The password of the image registry credential
        :param str username: The username of the image registry credential
        """
        if password is not None:
            pulumi.set(__self__, 'password', password)
        if username is not None:
            pulumi.set(__self__, 'username', username)

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        The password of the image registry credential
        """
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        The username of the image registry credential
        """
        return pulumi.get(self, 'username')

@pulumi.output_type
class JarUploadedUserSourceInfoResponse(dict):
    """
    Uploaded Jar binary for a deployment
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'jvmOptions':
            suggest = 'jvm_options'
        elif key == 'relativePath':
            suggest = 'relative_path'
        elif key == 'runtimeVersion':
            suggest = 'runtime_version'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in JarUploadedUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        JarUploadedUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        JarUploadedUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, jvm_options: Optional[str]=None, relative_path: Optional[str]=None, runtime_version: Optional[str]=None, version: Optional[str]=None):
        """
        Uploaded Jar binary for a deployment
        :param str type: Type of the source uploaded
               Expected value is 'Jar'.
        :param str jvm_options: JVM parameter
        :param str relative_path: Relative path of the storage which stores the source
        :param str runtime_version: Runtime version of the Jar file
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'Jar')
        if jvm_options is not None:
            pulumi.set(__self__, 'jvm_options', jvm_options)
        if relative_path is not None:
            pulumi.set(__self__, 'relative_path', relative_path)
        if runtime_version is not None:
            pulumi.set(__self__, 'runtime_version', runtime_version)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'Jar'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='jvmOptions')
    def jvm_options(self) -> Optional[str]:
        """
        JVM parameter
        """
        return pulumi.get(self, 'jvm_options')

    @property
    @pulumi.getter(name='relativePath')
    def relative_path(self) -> Optional[str]:
        """
        Relative path of the storage which stores the source
        """
        return pulumi.get(self, 'relative_path')

    @property
    @pulumi.getter(name='runtimeVersion')
    def runtime_version(self) -> Optional[str]:
        """
        Runtime version of the Jar file
        """
        return pulumi.get(self, 'runtime_version')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class KeyVaultCertificatePropertiesResponse(dict):
    """
    Properties of certificate imported from key vault.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'activateDate':
            suggest = 'activate_date'
        elif key == 'dnsNames':
            suggest = 'dns_names'
        elif key == 'expirationDate':
            suggest = 'expiration_date'
        elif key == 'issuedDate':
            suggest = 'issued_date'
        elif key == 'keyVaultCertName':
            suggest = 'key_vault_cert_name'
        elif key == 'subjectName':
            suggest = 'subject_name'
        elif key == 'vaultUri':
            suggest = 'vault_uri'
        elif key == 'certVersion':
            suggest = 'cert_version'
        elif key == 'excludePrivateKey':
            suggest = 'exclude_private_key'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultCertificatePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultCertificatePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        KeyVaultCertificatePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, activate_date: str, dns_names: Sequence[str], expiration_date: str, issued_date: str, issuer: str, key_vault_cert_name: str, subject_name: str, thumbprint: str, type: str, vault_uri: str, cert_version: Optional[str]=None, exclude_private_key: Optional[bool]=None):
        """
        Properties of certificate imported from key vault.
        :param str activate_date: The activate date of certificate.
        :param Sequence[str] dns_names: The domain list of certificate.
        :param str expiration_date: The expiration date of certificate.
        :param str issued_date: The issue date of certificate.
        :param str issuer: The issuer of certificate.
        :param str key_vault_cert_name: The certificate name of key vault.
        :param str subject_name: The subject name of certificate.
        :param str thumbprint: The thumbprint of certificate.
        :param str type: The type of the certificate source.
               Expected value is 'KeyVaultCertificate'.
        :param str vault_uri: The vault uri of user key vault.
        :param str cert_version: The certificate version of key vault.
        :param bool exclude_private_key: Optional. If set to true, it will not import private key from key vault.
        """
        pulumi.set(__self__, 'activate_date', activate_date)
        pulumi.set(__self__, 'dns_names', dns_names)
        pulumi.set(__self__, 'expiration_date', expiration_date)
        pulumi.set(__self__, 'issued_date', issued_date)
        pulumi.set(__self__, 'issuer', issuer)
        pulumi.set(__self__, 'key_vault_cert_name', key_vault_cert_name)
        pulumi.set(__self__, 'subject_name', subject_name)
        pulumi.set(__self__, 'thumbprint', thumbprint)
        pulumi.set(__self__, 'type', 'KeyVaultCertificate')
        pulumi.set(__self__, 'vault_uri', vault_uri)
        if cert_version is not None:
            pulumi.set(__self__, 'cert_version', cert_version)
        if exclude_private_key is None:
            exclude_private_key = False
        if exclude_private_key is not None:
            pulumi.set(__self__, 'exclude_private_key', exclude_private_key)

    @property
    @pulumi.getter(name='activateDate')
    def activate_date(self) -> str:
        """
        The activate date of certificate.
        """
        return pulumi.get(self, 'activate_date')

    @property
    @pulumi.getter(name='dnsNames')
    def dns_names(self) -> Sequence[str]:
        """
        The domain list of certificate.
        """
        return pulumi.get(self, 'dns_names')

    @property
    @pulumi.getter(name='expirationDate')
    def expiration_date(self) -> str:
        """
        The expiration date of certificate.
        """
        return pulumi.get(self, 'expiration_date')

    @property
    @pulumi.getter(name='issuedDate')
    def issued_date(self) -> str:
        """
        The issue date of certificate.
        """
        return pulumi.get(self, 'issued_date')

    @property
    @pulumi.getter
    def issuer(self) -> str:
        """
        The issuer of certificate.
        """
        return pulumi.get(self, 'issuer')

    @property
    @pulumi.getter(name='keyVaultCertName')
    def key_vault_cert_name(self) -> str:
        """
        The certificate name of key vault.
        """
        return pulumi.get(self, 'key_vault_cert_name')

    @property
    @pulumi.getter(name='subjectName')
    def subject_name(self) -> str:
        """
        The subject name of certificate.
        """
        return pulumi.get(self, 'subject_name')

    @property
    @pulumi.getter
    def thumbprint(self) -> str:
        """
        The thumbprint of certificate.
        """
        return pulumi.get(self, 'thumbprint')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the certificate source.
        Expected value is 'KeyVaultCertificate'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='vaultUri')
    def vault_uri(self) -> str:
        """
        The vault uri of user key vault.
        """
        return pulumi.get(self, 'vault_uri')

    @property
    @pulumi.getter(name='certVersion')
    def cert_version(self) -> Optional[str]:
        """
        The certificate version of key vault.
        """
        return pulumi.get(self, 'cert_version')

    @property
    @pulumi.getter(name='excludePrivateKey')
    def exclude_private_key(self) -> Optional[bool]:
        """
        Optional. If set to true, it will not import private key from key vault.
        """
        return pulumi.get(self, 'exclude_private_key')

@pulumi.output_type
class LoadedCertificateResponse(dict):
    """
    Loaded certificate payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'resourceId':
            suggest = 'resource_id'
        elif key == 'loadTrustStore':
            suggest = 'load_trust_store'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadedCertificateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadedCertificateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        LoadedCertificateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, resource_id: str, load_trust_store: Optional[bool]=None):
        """
        Loaded certificate payload
        :param str resource_id: Resource Id of loaded certificate
        :param bool load_trust_store: Indicate whether the certificate will be loaded into default trust store, only work for Java runtime.
        """
        pulumi.set(__self__, 'resource_id', resource_id)
        if load_trust_store is None:
            load_trust_store = False
        if load_trust_store is not None:
            pulumi.set(__self__, 'load_trust_store', load_trust_store)

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> str:
        """
        Resource Id of loaded certificate
        """
        return pulumi.get(self, 'resource_id')

    @property
    @pulumi.getter(name='loadTrustStore')
    def load_trust_store(self) -> Optional[bool]:
        """
        Indicate whether the certificate will be loaded into default trust store, only work for Java runtime.
        """
        return pulumi.get(self, 'load_trust_store')

@pulumi.output_type
class ManagedIdentityPropertiesResponse(dict):
    """
    Managed identity properties retrieved from ARM request headers.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'principalId':
            suggest = 'principal_id'
        elif key == 'tenantId':
            suggest = 'tenant_id'
        elif key == 'userAssignedIdentities':
            suggest = 'user_assigned_identities'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedIdentityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedIdentityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedIdentityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, principal_id: Optional[str]=None, tenant_id: Optional[str]=None, type: Optional[str]=None, user_assigned_identities: Optional[Mapping[str, 'outputs.UserAssignedManagedIdentityResponse']]=None):
        """
        Managed identity properties retrieved from ARM request headers.
        :param str principal_id: Principal Id of system-assigned managed identity.
        :param str tenant_id: Tenant Id of system-assigned managed identity.
        :param str type: Type of the managed identity
        :param Mapping[str, 'UserAssignedManagedIdentityResponse'] user_assigned_identities: Properties of user-assigned managed identities
        """
        if principal_id is not None:
            pulumi.set(__self__, 'principal_id', principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, 'tenant_id', tenant_id)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, 'user_assigned_identities', user_assigned_identities)

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> Optional[str]:
        """
        Principal Id of system-assigned managed identity.
        """
        return pulumi.get(self, 'principal_id')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> Optional[str]:
        """
        Tenant Id of system-assigned managed identity.
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Type of the managed identity
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userAssignedIdentities')
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserAssignedManagedIdentityResponse']]:
        """
        Properties of user-assigned managed identities
        """
        return pulumi.get(self, 'user_assigned_identities')

@pulumi.output_type
class MonitoringSettingPropertiesResponse(dict):
    """
    Monitoring Setting properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'appInsightsAgentVersions':
            suggest = 'app_insights_agent_versions'
        elif key == 'appInsightsInstrumentationKey':
            suggest = 'app_insights_instrumentation_key'
        elif key == 'appInsightsSamplingRate':
            suggest = 'app_insights_sampling_rate'
        elif key == 'traceEnabled':
            suggest = 'trace_enabled'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitoringSettingPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitoringSettingPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        MonitoringSettingPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, provisioning_state: str, app_insights_agent_versions: Optional['outputs.ApplicationInsightsAgentVersionsResponse']=None, app_insights_instrumentation_key: Optional[str]=None, app_insights_sampling_rate: Optional[float]=None, error: Optional['outputs.ErrorResponse']=None, trace_enabled: Optional[bool]=None):
        """
        Monitoring Setting properties payload
        :param str provisioning_state: State of the Monitoring Setting.
        :param 'ApplicationInsightsAgentVersionsResponse' app_insights_agent_versions: Indicates the versions of application insight agent
        :param str app_insights_instrumentation_key: Target application insight instrumentation key, null or whitespace include empty will disable monitoringSettings
        :param float app_insights_sampling_rate: Indicates the sampling rate of application insight agent, should be in range [0.0, 100.0]
        :param 'ErrorResponse' error: Error when apply Monitoring Setting changes.
        :param bool trace_enabled: Indicates whether enable the trace functionality, which will be deprecated since api version 2020-11-01-preview. Please leverage appInsightsInstrumentationKey to indicate if monitoringSettings enabled or not
        """
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if app_insights_agent_versions is not None:
            pulumi.set(__self__, 'app_insights_agent_versions', app_insights_agent_versions)
        if app_insights_instrumentation_key is not None:
            pulumi.set(__self__, 'app_insights_instrumentation_key', app_insights_instrumentation_key)
        if app_insights_sampling_rate is not None:
            pulumi.set(__self__, 'app_insights_sampling_rate', app_insights_sampling_rate)
        if error is not None:
            pulumi.set(__self__, 'error', error)
        if trace_enabled is not None:
            pulumi.set(__self__, 'trace_enabled', trace_enabled)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Monitoring Setting.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='appInsightsAgentVersions')
    def app_insights_agent_versions(self) -> Optional['outputs.ApplicationInsightsAgentVersionsResponse']:
        """
        Indicates the versions of application insight agent
        """
        return pulumi.get(self, 'app_insights_agent_versions')

    @property
    @pulumi.getter(name='appInsightsInstrumentationKey')
    def app_insights_instrumentation_key(self) -> Optional[str]:
        """
        Target application insight instrumentation key, null or whitespace include empty will disable monitoringSettings
        """
        return pulumi.get(self, 'app_insights_instrumentation_key')

    @property
    @pulumi.getter(name='appInsightsSamplingRate')
    def app_insights_sampling_rate(self) -> Optional[float]:
        """
        Indicates the sampling rate of application insight agent, should be in range [0.0, 100.0]
        """
        return pulumi.get(self, 'app_insights_sampling_rate')

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.ErrorResponse']:
        """
        Error when apply Monitoring Setting changes.
        """
        return pulumi.get(self, 'error')

    @property
    @pulumi.getter(name='traceEnabled')
    def trace_enabled(self) -> Optional[bool]:
        """
        Indicates whether enable the trace functionality, which will be deprecated since api version 2020-11-01-preview. Please leverage appInsightsInstrumentationKey to indicate if monitoringSettings enabled or not
        """
        return pulumi.get(self, 'trace_enabled')

@pulumi.output_type
class NetCoreZipUploadedUserSourceInfoResponse(dict):
    """
    Uploaded Jar binary for a deployment
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'netCoreMainEntryPath':
            suggest = 'net_core_main_entry_path'
        elif key == 'relativePath':
            suggest = 'relative_path'
        elif key == 'runtimeVersion':
            suggest = 'runtime_version'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetCoreZipUploadedUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetCoreZipUploadedUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        NetCoreZipUploadedUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, net_core_main_entry_path: Optional[str]=None, relative_path: Optional[str]=None, runtime_version: Optional[str]=None, version: Optional[str]=None):
        """
        Uploaded Jar binary for a deployment
        :param str type: Type of the source uploaded
               Expected value is 'NetCoreZip'.
        :param str net_core_main_entry_path: The path to the .NET executable relative to zip root
        :param str relative_path: Relative path of the storage which stores the source
        :param str runtime_version: Runtime version of the .Net file
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'NetCoreZip')
        if net_core_main_entry_path is not None:
            pulumi.set(__self__, 'net_core_main_entry_path', net_core_main_entry_path)
        if relative_path is not None:
            pulumi.set(__self__, 'relative_path', relative_path)
        if runtime_version is not None:
            pulumi.set(__self__, 'runtime_version', runtime_version)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'NetCoreZip'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='netCoreMainEntryPath')
    def net_core_main_entry_path(self) -> Optional[str]:
        """
        The path to the .NET executable relative to zip root
        """
        return pulumi.get(self, 'net_core_main_entry_path')

    @property
    @pulumi.getter(name='relativePath')
    def relative_path(self) -> Optional[str]:
        """
        Relative path of the storage which stores the source
        """
        return pulumi.get(self, 'relative_path')

    @property
    @pulumi.getter(name='runtimeVersion')
    def runtime_version(self) -> Optional[str]:
        """
        Runtime version of the .Net file
        """
        return pulumi.get(self, 'runtime_version')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class NetworkProfileResponse(dict):
    """
    Service network profile payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'outboundIPs':
            suggest = 'outbound_ips'
        elif key == 'requiredTraffics':
            suggest = 'required_traffics'
        elif key == 'appNetworkResourceGroup':
            suggest = 'app_network_resource_group'
        elif key == 'appSubnetId':
            suggest = 'app_subnet_id'
        elif key == 'serviceCidr':
            suggest = 'service_cidr'
        elif key == 'serviceRuntimeNetworkResourceGroup':
            suggest = 'service_runtime_network_resource_group'
        elif key == 'serviceRuntimeSubnetId':
            suggest = 'service_runtime_subnet_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, outbound_ips: 'outputs.NetworkProfileResponseOutboundIPs', required_traffics: Sequence['outputs.RequiredTrafficResponse'], app_network_resource_group: Optional[str]=None, app_subnet_id: Optional[str]=None, service_cidr: Optional[str]=None, service_runtime_network_resource_group: Optional[str]=None, service_runtime_subnet_id: Optional[str]=None):
        """
        Service network profile payload
        :param 'NetworkProfileResponseOutboundIPs' outbound_ips: Desired outbound IP resources for Azure Spring Cloud instance.
        :param Sequence['RequiredTrafficResponse'] required_traffics: Required inbound or outbound traffics for Azure Spring Cloud instance.
        :param str app_network_resource_group: Name of the resource group containing network resources of Azure Spring Cloud Apps
        :param str app_subnet_id: Fully qualified resource Id of the subnet to host Azure Spring Cloud Apps
        :param str service_cidr: Azure Spring Cloud service reserved CIDR
        :param str service_runtime_network_resource_group: Name of the resource group containing network resources of Azure Spring Cloud Service Runtime
        :param str service_runtime_subnet_id: Fully qualified resource Id of the subnet to host Azure Spring Cloud Service Runtime
        """
        pulumi.set(__self__, 'outbound_ips', outbound_ips)
        pulumi.set(__self__, 'required_traffics', required_traffics)
        if app_network_resource_group is not None:
            pulumi.set(__self__, 'app_network_resource_group', app_network_resource_group)
        if app_subnet_id is not None:
            pulumi.set(__self__, 'app_subnet_id', app_subnet_id)
        if service_cidr is not None:
            pulumi.set(__self__, 'service_cidr', service_cidr)
        if service_runtime_network_resource_group is not None:
            pulumi.set(__self__, 'service_runtime_network_resource_group', service_runtime_network_resource_group)
        if service_runtime_subnet_id is not None:
            pulumi.set(__self__, 'service_runtime_subnet_id', service_runtime_subnet_id)

    @property
    @pulumi.getter(name='outboundIPs')
    def outbound_ips(self) -> 'outputs.NetworkProfileResponseOutboundIPs':
        """
        Desired outbound IP resources for Azure Spring Cloud instance.
        """
        return pulumi.get(self, 'outbound_ips')

    @property
    @pulumi.getter(name='requiredTraffics')
    def required_traffics(self) -> Sequence['outputs.RequiredTrafficResponse']:
        """
        Required inbound or outbound traffics for Azure Spring Cloud instance.
        """
        return pulumi.get(self, 'required_traffics')

    @property
    @pulumi.getter(name='appNetworkResourceGroup')
    def app_network_resource_group(self) -> Optional[str]:
        """
        Name of the resource group containing network resources of Azure Spring Cloud Apps
        """
        return pulumi.get(self, 'app_network_resource_group')

    @property
    @pulumi.getter(name='appSubnetId')
    def app_subnet_id(self) -> Optional[str]:
        """
        Fully qualified resource Id of the subnet to host Azure Spring Cloud Apps
        """
        return pulumi.get(self, 'app_subnet_id')

    @property
    @pulumi.getter(name='serviceCidr')
    def service_cidr(self) -> Optional[str]:
        """
        Azure Spring Cloud service reserved CIDR
        """
        return pulumi.get(self, 'service_cidr')

    @property
    @pulumi.getter(name='serviceRuntimeNetworkResourceGroup')
    def service_runtime_network_resource_group(self) -> Optional[str]:
        """
        Name of the resource group containing network resources of Azure Spring Cloud Service Runtime
        """
        return pulumi.get(self, 'service_runtime_network_resource_group')

    @property
    @pulumi.getter(name='serviceRuntimeSubnetId')
    def service_runtime_subnet_id(self) -> Optional[str]:
        """
        Fully qualified resource Id of the subnet to host Azure Spring Cloud Service Runtime
        """
        return pulumi.get(self, 'service_runtime_subnet_id')

@pulumi.output_type
class NetworkProfileResponseOutboundIPs(dict):
    """
    Desired outbound IP resources for Azure Spring Cloud instance.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publicIPs':
            suggest = 'public_ips'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkProfileResponseOutboundIPs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkProfileResponseOutboundIPs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        NetworkProfileResponseOutboundIPs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, public_ips: Sequence[str]):
        """
        Desired outbound IP resources for Azure Spring Cloud instance.
        :param Sequence[str] public_ips: A list of public IP addresses.
        """
        pulumi.set(__self__, 'public_ips', public_ips)

    @property
    @pulumi.getter(name='publicIPs')
    def public_ips(self) -> Sequence[str]:
        """
        A list of public IP addresses.
        """
        return pulumi.get(self, 'public_ips')

@pulumi.output_type
class PersistentDiskResponse(dict):
    """
    Persistent disk payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'usedInGB':
            suggest = 'used_in_gb'
        elif key == 'mountPath':
            suggest = 'mount_path'
        elif key == 'sizeInGB':
            suggest = 'size_in_gb'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PersistentDiskResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PersistentDiskResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        PersistentDiskResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, used_in_gb: int, mount_path: Optional[str]=None, size_in_gb: Optional[int]=None):
        """
        Persistent disk payload
        :param int used_in_gb: Size of the used persistent disk in GB
        :param str mount_path: Mount path of the persistent disk
        :param int size_in_gb: Size of the persistent disk in GB
        """
        pulumi.set(__self__, 'used_in_gb', used_in_gb)
        if mount_path is not None:
            pulumi.set(__self__, 'mount_path', mount_path)
        if size_in_gb is not None:
            pulumi.set(__self__, 'size_in_gb', size_in_gb)

    @property
    @pulumi.getter(name='usedInGB')
    def used_in_gb(self) -> int:
        """
        Size of the used persistent disk in GB
        """
        return pulumi.get(self, 'used_in_gb')

    @property
    @pulumi.getter(name='mountPath')
    def mount_path(self) -> Optional[str]:
        """
        Mount path of the persistent disk
        """
        return pulumi.get(self, 'mount_path')

    @property
    @pulumi.getter(name='sizeInGB')
    def size_in_gb(self) -> Optional[int]:
        """
        Size of the persistent disk in GB
        """
        return pulumi.get(self, 'size_in_gb')

@pulumi.output_type
class RequiredTrafficResponse(dict):
    """
    Required inbound or outbound traffic for Azure Spring Cloud instance.
    """

    def __init__(__self__, *, direction: str, fqdns: Sequence[str], ips: Sequence[str], port: int, protocol: str):
        """
        Required inbound or outbound traffic for Azure Spring Cloud instance.
        :param str direction: The direction of required traffic
        :param Sequence[str] fqdns: The FQDN list of required traffic
        :param Sequence[str] ips: The ip list of required traffic
        :param int port: The port of required traffic
        :param str protocol: The protocol of required traffic
        """
        pulumi.set(__self__, 'direction', direction)
        pulumi.set(__self__, 'fqdns', fqdns)
        pulumi.set(__self__, 'ips', ips)
        pulumi.set(__self__, 'port', port)
        pulumi.set(__self__, 'protocol', protocol)

    @property
    @pulumi.getter
    def direction(self) -> str:
        """
        The direction of required traffic
        """
        return pulumi.get(self, 'direction')

    @property
    @pulumi.getter
    def fqdns(self) -> Sequence[str]:
        """
        The FQDN list of required traffic
        """
        return pulumi.get(self, 'fqdns')

    @property
    @pulumi.getter
    def ips(self) -> Sequence[str]:
        """
        The ip list of required traffic
        """
        return pulumi.get(self, 'ips')

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port of required traffic
        """
        return pulumi.get(self, 'port')

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        The protocol of required traffic
        """
        return pulumi.get(self, 'protocol')

@pulumi.output_type
class ResourceRequestsResponse(dict):
    """
    Deployment resource request payload
    """

    def __init__(__self__, *, cpu: Optional[str]=None, memory: Optional[str]=None):
        """
        Deployment resource request payload
        :param str cpu: Required CPU. 1 core can be represented by 1 or 1000m. This should be 500m or 1 for Basic tier, and {500m, 1, 2, 3, 4} for Standard tier.
        :param str memory: Required memory. 1 GB can be represented by 1Gi or 1024Mi. This should be {512Mi, 1Gi, 2Gi} for Basic tier, and {512Mi, 1Gi, 2Gi, ..., 8Gi} for Standard tier.
        """
        if cpu is not None:
            pulumi.set(__self__, 'cpu', cpu)
        if memory is not None:
            pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[str]:
        """
        Required CPU. 1 core can be represented by 1 or 1000m. This should be 500m or 1 for Basic tier, and {500m, 1, 2, 3, 4} for Standard tier.
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter
    def memory(self) -> Optional[str]:
        """
        Required memory. 1 GB can be represented by 1Gi or 1024Mi. This should be {512Mi, 1Gi, 2Gi} for Basic tier, and {512Mi, 1Gi, 2Gi, ..., 8Gi} for Standard tier.
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class ServiceRegistryInstanceResponse(dict):
    """
    Collection of instances belong to the Service Registry
    """

    def __init__(__self__, *, name: str, status: str):
        """
        Collection of instances belong to the Service Registry
        :param str name: Name of the Service Registry instance
        :param str status: Status of the Service Registry instance
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Service Registry instance
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Service Registry instance
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class ServiceRegistryPropertiesResponse(dict):
    """
    Service Registry properties payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'resourceRequests':
            suggest = 'resource_requests'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceRegistryPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceRegistryPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ServiceRegistryPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, instances: Sequence['outputs.ServiceRegistryInstanceResponse'], provisioning_state: str, resource_requests: 'outputs.ServiceRegistryResourceRequestsResponse'):
        """
        Service Registry properties payload
        :param Sequence['ServiceRegistryInstanceResponse'] instances: Collection of instances belong to Service Registry.
        :param str provisioning_state: State of the Service Registry.
        :param 'ServiceRegistryResourceRequestsResponse' resource_requests: The requested resource quantity for required CPU and Memory.
        """
        pulumi.set(__self__, 'instances', instances)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'resource_requests', resource_requests)

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.ServiceRegistryInstanceResponse']:
        """
        Collection of instances belong to Service Registry.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        State of the Service Registry.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceRequests')
    def resource_requests(self) -> 'outputs.ServiceRegistryResourceRequestsResponse':
        """
        The requested resource quantity for required CPU and Memory.
        """
        return pulumi.get(self, 'resource_requests')

@pulumi.output_type
class ServiceRegistryResourceRequestsResponse(dict):
    """
    Resource request payload of Service Registry
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'instanceCount':
            suggest = 'instance_count'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceRegistryResourceRequestsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceRegistryResourceRequestsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ServiceRegistryResourceRequestsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, cpu: str, instance_count: int, memory: str):
        """
        Resource request payload of Service Registry
        :param str cpu: Cpu allocated to each Service Registry instance
        :param int instance_count: Instance count of the Service Registry
        :param str memory: Memory allocated to each Service Registry instance
        """
        pulumi.set(__self__, 'cpu', cpu)
        pulumi.set(__self__, 'instance_count', instance_count)
        pulumi.set(__self__, 'memory', memory)

    @property
    @pulumi.getter
    def cpu(self) -> str:
        """
        Cpu allocated to each Service Registry instance
        """
        return pulumi.get(self, 'cpu')

    @property
    @pulumi.getter(name='instanceCount')
    def instance_count(self) -> int:
        """
        Instance count of the Service Registry
        """
        return pulumi.get(self, 'instance_count')

    @property
    @pulumi.getter
    def memory(self) -> str:
        """
        Memory allocated to each Service Registry instance
        """
        return pulumi.get(self, 'memory')

@pulumi.output_type
class SkuResponse(dict):
    """
    Sku of Azure Spring Cloud
    """

    def __init__(__self__, *, capacity: Optional[int]=None, name: Optional[str]=None, tier: Optional[str]=None):
        """
        Sku of Azure Spring Cloud
        :param int capacity: Current capacity of the target resource
        :param str name: Name of the Sku
        :param str tier: Tier of the Sku
        """
        if capacity is not None:
            pulumi.set(__self__, 'capacity', capacity)
        if name is None:
            name = 'S0'
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if tier is None:
            tier = 'Standard'
        if tier is not None:
            pulumi.set(__self__, 'tier', tier)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        Current capacity of the target resource
        """
        return pulumi.get(self, 'capacity')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the Sku
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        Tier of the Sku
        """
        return pulumi.get(self, 'tier')

@pulumi.output_type
class SourceUploadedUserSourceInfoResponse(dict):
    """
    Uploaded Java source code binary for a deployment
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'artifactSelector':
            suggest = 'artifact_selector'
        elif key == 'relativePath':
            suggest = 'relative_path'
        elif key == 'runtimeVersion':
            suggest = 'runtime_version'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SourceUploadedUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SourceUploadedUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SourceUploadedUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, artifact_selector: Optional[str]=None, relative_path: Optional[str]=None, runtime_version: Optional[str]=None, version: Optional[str]=None):
        """
        Uploaded Java source code binary for a deployment
        :param str type: Type of the source uploaded
               Expected value is 'Source'.
        :param str artifact_selector: Selector for the artifact to be used for the deployment for multi-module projects. This should be
               the relative path to the target module/project.
        :param str relative_path: Relative path of the storage which stores the source
        :param str runtime_version: Runtime version of the source file
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'Source')
        if artifact_selector is not None:
            pulumi.set(__self__, 'artifact_selector', artifact_selector)
        if relative_path is not None:
            pulumi.set(__self__, 'relative_path', relative_path)
        if runtime_version is not None:
            pulumi.set(__self__, 'runtime_version', runtime_version)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'Source'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='artifactSelector')
    def artifact_selector(self) -> Optional[str]:
        """
        Selector for the artifact to be used for the deployment for multi-module projects. This should be
        the relative path to the target module/project.
        """
        return pulumi.get(self, 'artifact_selector')

    @property
    @pulumi.getter(name='relativePath')
    def relative_path(self) -> Optional[str]:
        """
        Relative path of the storage which stores the source
        """
        return pulumi.get(self, 'relative_path')

    @property
    @pulumi.getter(name='runtimeVersion')
    def runtime_version(self) -> Optional[str]:
        """
        Runtime version of the source file
        """
        return pulumi.get(self, 'runtime_version')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class SsoPropertiesResponse(dict):
    """
    Single sign-on related configuration
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'clientSecret':
            suggest = 'client_secret'
        elif key == 'issuerUri':
            suggest = 'issuer_uri'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SsoPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SsoPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SsoPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: Optional[str]=None, client_secret: Optional[str]=None, issuer_uri: Optional[str]=None, scope: Optional[Sequence[str]]=None):
        """
        Single sign-on related configuration
        :param str client_id: The public identifier for the application
        :param str client_secret: The secret known only to the application and the authorization server
        :param str issuer_uri: The URI of Issuer Identifier
        :param Sequence[str] scope: It defines the specific actions applications can be allowed to do on a user's behalf
        """
        if client_id is not None:
            pulumi.set(__self__, 'client_id', client_id)
        if client_secret is not None:
            pulumi.set(__self__, 'client_secret', client_secret)
        if issuer_uri is not None:
            pulumi.set(__self__, 'issuer_uri', issuer_uri)
        if scope is not None:
            pulumi.set(__self__, 'scope', scope)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> Optional[str]:
        """
        The public identifier for the application
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='clientSecret')
    def client_secret(self) -> Optional[str]:
        """
        The secret known only to the application and the authorization server
        """
        return pulumi.get(self, 'client_secret')

    @property
    @pulumi.getter(name='issuerUri')
    def issuer_uri(self) -> Optional[str]:
        """
        The URI of Issuer Identifier
        """
        return pulumi.get(self, 'issuer_uri')

    @property
    @pulumi.getter
    def scope(self) -> Optional[Sequence[str]]:
        """
        It defines the specific actions applications can be allowed to do on a user's behalf
        """
        return pulumi.get(self, 'scope')

@pulumi.output_type
class StackPropertiesResponse(dict):
    """
    KPack ClusterStack properties payload
    """

    def __init__(__self__, *, id: Optional[str]=None, version: Optional[str]=None):
        """
        KPack ClusterStack properties payload
        :param str id: Id of the ClusterStack.
        :param str version: Version of the ClusterStack
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Id of the ClusterStack.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the ClusterStack
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class StorageAccountResponse(dict):
    """
    storage resource of type Azure Storage Account.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'accountName':
            suggest = 'account_name'
        elif key == 'storageType':
            suggest = 'storage_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StorageAccountResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StorageAccountResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        StorageAccountResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, account_name: str, storage_type: str):
        """
        storage resource of type Azure Storage Account.
        :param str account_name: The account name of the Azure Storage Account.
        :param str storage_type: The type of the storage.
               Expected value is 'StorageAccount'.
        """
        pulumi.set(__self__, 'account_name', account_name)
        pulumi.set(__self__, 'storage_type', 'StorageAccount')

    @property
    @pulumi.getter(name='accountName')
    def account_name(self) -> str:
        """
        The account name of the Azure Storage Account.
        """
        return pulumi.get(self, 'account_name')

    @property
    @pulumi.getter(name='storageType')
    def storage_type(self) -> str:
        """
        The type of the storage.
        Expected value is 'StorageAccount'.
        """
        return pulumi.get(self, 'storage_type')

@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'createdAt':
            suggest = 'created_at'
        elif key == 'createdBy':
            suggest = 'created_by'
        elif key == 'createdByType':
            suggest = 'created_by_type'
        elif key == 'lastModifiedAt':
            suggest = 'last_modified_at'
        elif key == 'lastModifiedBy':
            suggest = 'last_modified_by'
        elif key == 'lastModifiedByType':
            suggest = 'last_modified_by_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, created_at: Optional[str]=None, created_by: Optional[str]=None, created_by_type: Optional[str]=None, last_modified_at: Optional[str]=None, last_modified_by: Optional[str]=None, last_modified_by_type: Optional[str]=None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource modification (UTC).
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, 'created_at', created_at)
        if created_by is not None:
            pulumi.set(__self__, 'created_by', created_by)
        if created_by_type is not None:
            pulumi.set(__self__, 'created_by_type', created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, 'last_modified_at', last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, 'last_modified_by', last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, 'last_modified_by_type', last_modified_by_type)

    @property
    @pulumi.getter(name='createdAt')
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, 'created_at')

    @property
    @pulumi.getter(name='createdBy')
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, 'created_by')

    @property
    @pulumi.getter(name='createdByType')
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, 'created_by_type')

    @property
    @pulumi.getter(name='lastModifiedAt')
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource modification (UTC).
        """
        return pulumi.get(self, 'last_modified_at')

    @property
    @pulumi.getter(name='lastModifiedBy')
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, 'last_modified_by')

    @property
    @pulumi.getter(name='lastModifiedByType')
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, 'last_modified_by_type')

@pulumi.output_type
class TemporaryDiskResponse(dict):
    """
    Temporary disk payload
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'mountPath':
            suggest = 'mount_path'
        elif key == 'sizeInGB':
            suggest = 'size_in_gb'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TemporaryDiskResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TemporaryDiskResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        TemporaryDiskResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, mount_path: Optional[str]=None, size_in_gb: Optional[int]=None):
        """
        Temporary disk payload
        :param str mount_path: Mount path of the temporary disk
        :param int size_in_gb: Size of the temporary disk in GB
        """
        if mount_path is None:
            mount_path = '/tmp'
        if mount_path is not None:
            pulumi.set(__self__, 'mount_path', mount_path)
        if size_in_gb is not None:
            pulumi.set(__self__, 'size_in_gb', size_in_gb)

    @property
    @pulumi.getter(name='mountPath')
    def mount_path(self) -> Optional[str]:
        """
        Mount path of the temporary disk
        """
        return pulumi.get(self, 'mount_path')

    @property
    @pulumi.getter(name='sizeInGB')
    def size_in_gb(self) -> Optional[int]:
        """
        Size of the temporary disk in GB
        """
        return pulumi.get(self, 'size_in_gb')

@pulumi.output_type
class UploadedUserSourceInfoResponse(dict):
    """
    Source with uploaded location
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'relativePath':
            suggest = 'relative_path'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UploadedUserSourceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UploadedUserSourceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UploadedUserSourceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, type: str, relative_path: Optional[str]=None, version: Optional[str]=None):
        """
        Source with uploaded location
        :param str type: Type of the source uploaded
               Expected value is 'UploadedUserSourceInfo'.
        :param str relative_path: Relative path of the storage which stores the source
        :param str version: Version of the source
        """
        pulumi.set(__self__, 'type', 'UploadedUserSourceInfo')
        if relative_path is not None:
            pulumi.set(__self__, 'relative_path', relative_path)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the source uploaded
        Expected value is 'UploadedUserSourceInfo'.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='relativePath')
    def relative_path(self) -> Optional[str]:
        """
        Relative path of the storage which stores the source
        """
        return pulumi.get(self, 'relative_path')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the source
        """
        return pulumi.get(self, 'version')

@pulumi.output_type
class UserAssignedManagedIdentityResponse(dict):
    """
    The details of the user-assigned managed identity assigned to an App.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'principalId':
            suggest = 'principal_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedManagedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedManagedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UserAssignedManagedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: str, principal_id: str):
        """
        The details of the user-assigned managed identity assigned to an App.
        :param str client_id: Client Id of user-assigned managed identity.
        :param str principal_id: Principal Id of user-assigned managed identity.
        """
        pulumi.set(__self__, 'client_id', client_id)
        pulumi.set(__self__, 'principal_id', principal_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> str:
        """
        Client Id of user-assigned managed identity.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> str:
        """
        Principal Id of user-assigned managed identity.
        """
        return pulumi.get(self, 'principal_id')