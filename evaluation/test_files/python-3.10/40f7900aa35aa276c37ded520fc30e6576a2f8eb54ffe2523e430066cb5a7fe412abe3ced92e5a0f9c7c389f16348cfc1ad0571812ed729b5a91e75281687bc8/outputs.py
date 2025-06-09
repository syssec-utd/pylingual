import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['AgentPoolUpgradeSettingsResponse', 'ContainerServiceLinuxProfileResponse', 'ContainerServiceNetworkProfileResponse', 'ContainerServiceSshConfigurationResponse', 'ContainerServiceSshPublicKeyResponse', 'CredentialResultResponse', 'ExtendedLocationResponse', 'KubeletConfigResponse', 'LinuxOSConfigResponse', 'ManagedClusterAADProfileResponse', 'ManagedClusterAPIServerAccessProfileResponse', 'ManagedClusterAddonProfileResponse', 'ManagedClusterAddonProfileResponseIdentity', 'ManagedClusterAgentPoolProfileResponse', 'ManagedClusterAutoUpgradeProfileResponse', 'ManagedClusterHTTPProxyConfigResponse', 'ManagedClusterIdentityResponse', 'ManagedClusterIdentityResponseUserAssignedIdentities', 'ManagedClusterLoadBalancerProfileResponse', 'ManagedClusterLoadBalancerProfileResponseManagedOutboundIPs', 'ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes', 'ManagedClusterLoadBalancerProfileResponseOutboundIPs', 'ManagedClusterPodIdentityExceptionResponse', 'ManagedClusterPodIdentityProfileResponse', 'ManagedClusterPodIdentityProvisioningErrorBodyResponse', 'ManagedClusterPodIdentityProvisioningErrorResponse', 'ManagedClusterPodIdentityResponse', 'ManagedClusterPodIdentityResponseProvisioningInfo', 'ManagedClusterPropertiesResponseAutoScalerProfile', 'ManagedClusterPropertiesResponseIdentityProfile', 'ManagedClusterSKUResponse', 'ManagedClusterServicePrincipalProfileResponse', 'ManagedClusterWindowsProfileResponse', 'PowerStateResponse', 'PrivateEndpointResponse', 'PrivateLinkResourceResponse', 'PrivateLinkServiceConnectionStateResponse', 'ResourceReferenceResponse', 'SysctlConfigResponse', 'SystemDataResponse', 'TimeInWeekResponse', 'TimeSpanResponse', 'UserAssignedIdentityResponse']

@pulumi.output_type
class AgentPoolUpgradeSettingsResponse(dict):
    """
    Settings for upgrading an agentpool
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'maxSurge':
            suggest = 'max_surge'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AgentPoolUpgradeSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AgentPoolUpgradeSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AgentPoolUpgradeSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, max_surge: Optional[str]=None):
        """
        Settings for upgrading an agentpool
        :param str max_surge: This can either be set to an integer (e.g. '5') or a percentage (e.g. '50%'). If a percentage is specified, it is the percentage of the total agent pool size at the time of the upgrade. For percentages, fractional nodes are rounded up. If not specified, the default is 1. For more information, including best practices, see: https://docs.microsoft.com/azure/aks/upgrade-cluster#customize-node-surge-upgrade
        """
        if max_surge is not None:
            pulumi.set(__self__, 'max_surge', max_surge)

    @property
    @pulumi.getter(name='maxSurge')
    def max_surge(self) -> Optional[str]:
        """
        This can either be set to an integer (e.g. '5') or a percentage (e.g. '50%'). If a percentage is specified, it is the percentage of the total agent pool size at the time of the upgrade. For percentages, fractional nodes are rounded up. If not specified, the default is 1. For more information, including best practices, see: https://docs.microsoft.com/azure/aks/upgrade-cluster#customize-node-surge-upgrade
        """
        return pulumi.get(self, 'max_surge')

@pulumi.output_type
class ContainerServiceLinuxProfileResponse(dict):
    """
    Profile for Linux VMs in the container service cluster.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'adminUsername':
            suggest = 'admin_username'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceLinuxProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceLinuxProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContainerServiceLinuxProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, admin_username: str, ssh: 'outputs.ContainerServiceSshConfigurationResponse'):
        """
        Profile for Linux VMs in the container service cluster.
        :param str admin_username: The administrator username to use for Linux VMs.
        :param 'ContainerServiceSshConfigurationResponse' ssh: The SSH configuration for Linux-based VMs running on Azure.
        """
        pulumi.set(__self__, 'admin_username', admin_username)
        pulumi.set(__self__, 'ssh', ssh)

    @property
    @pulumi.getter(name='adminUsername')
    def admin_username(self) -> str:
        """
        The administrator username to use for Linux VMs.
        """
        return pulumi.get(self, 'admin_username')

    @property
    @pulumi.getter
    def ssh(self) -> 'outputs.ContainerServiceSshConfigurationResponse':
        """
        The SSH configuration for Linux-based VMs running on Azure.
        """
        return pulumi.get(self, 'ssh')

@pulumi.output_type
class ContainerServiceNetworkProfileResponse(dict):
    """
    Profile of network configuration.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'dnsServiceIP':
            suggest = 'dns_service_ip'
        elif key == 'dockerBridgeCidr':
            suggest = 'docker_bridge_cidr'
        elif key == 'loadBalancerProfile':
            suggest = 'load_balancer_profile'
        elif key == 'loadBalancerSku':
            suggest = 'load_balancer_sku'
        elif key == 'networkMode':
            suggest = 'network_mode'
        elif key == 'networkPlugin':
            suggest = 'network_plugin'
        elif key == 'networkPolicy':
            suggest = 'network_policy'
        elif key == 'outboundType':
            suggest = 'outbound_type'
        elif key == 'podCidr':
            suggest = 'pod_cidr'
        elif key == 'serviceCidr':
            suggest = 'service_cidr'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceNetworkProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceNetworkProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContainerServiceNetworkProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, dns_service_ip: Optional[str]=None, docker_bridge_cidr: Optional[str]=None, load_balancer_profile: Optional['outputs.ManagedClusterLoadBalancerProfileResponse']=None, load_balancer_sku: Optional[str]=None, network_mode: Optional[str]=None, network_plugin: Optional[str]=None, network_policy: Optional[str]=None, outbound_type: Optional[str]=None, pod_cidr: Optional[str]=None, service_cidr: Optional[str]=None):
        """
        Profile of network configuration.
        :param str dns_service_ip: An IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr.
        :param str docker_bridge_cidr: A CIDR notation IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes service address range.
        :param 'ManagedClusterLoadBalancerProfileResponse' load_balancer_profile: Profile of the cluster load balancer.
        :param str load_balancer_sku: The default is 'standard'. See [Azure Load Balancer SKUs](https://docs.microsoft.com/azure/load-balancer/skus) for more information about the differences between load balancer SKUs.
        :param str network_mode: This cannot be specified if networkPlugin is anything other than 'azure'.
        :param str network_plugin: Network plugin used for building the Kubernetes network.
        :param str network_policy: Network policy used for building the Kubernetes network.
        :param str outbound_type: This can only be set at cluster creation time and cannot be changed later. For more information see [egress outbound type](https://docs.microsoft.com/azure/aks/egress-outboundtype).
        :param str pod_cidr: A CIDR notation IP range from which to assign pod IPs when kubenet is used.
        :param str service_cidr: A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
        """
        if dns_service_ip is None:
            dns_service_ip = '10.0.0.10'
        if dns_service_ip is not None:
            pulumi.set(__self__, 'dns_service_ip', dns_service_ip)
        if docker_bridge_cidr is None:
            docker_bridge_cidr = '172.17.0.1/16'
        if docker_bridge_cidr is not None:
            pulumi.set(__self__, 'docker_bridge_cidr', docker_bridge_cidr)
        if load_balancer_profile is not None:
            pulumi.set(__self__, 'load_balancer_profile', load_balancer_profile)
        if load_balancer_sku is not None:
            pulumi.set(__self__, 'load_balancer_sku', load_balancer_sku)
        if network_mode is not None:
            pulumi.set(__self__, 'network_mode', network_mode)
        if network_plugin is None:
            network_plugin = 'kubenet'
        if network_plugin is not None:
            pulumi.set(__self__, 'network_plugin', network_plugin)
        if network_policy is not None:
            pulumi.set(__self__, 'network_policy', network_policy)
        if outbound_type is None:
            outbound_type = 'loadBalancer'
        if outbound_type is not None:
            pulumi.set(__self__, 'outbound_type', outbound_type)
        if pod_cidr is None:
            pod_cidr = '10.244.0.0/16'
        if pod_cidr is not None:
            pulumi.set(__self__, 'pod_cidr', pod_cidr)
        if service_cidr is None:
            service_cidr = '10.0.0.0/16'
        if service_cidr is not None:
            pulumi.set(__self__, 'service_cidr', service_cidr)

    @property
    @pulumi.getter(name='dnsServiceIP')
    def dns_service_ip(self) -> Optional[str]:
        """
        An IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr.
        """
        return pulumi.get(self, 'dns_service_ip')

    @property
    @pulumi.getter(name='dockerBridgeCidr')
    def docker_bridge_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes service address range.
        """
        return pulumi.get(self, 'docker_bridge_cidr')

    @property
    @pulumi.getter(name='loadBalancerProfile')
    def load_balancer_profile(self) -> Optional['outputs.ManagedClusterLoadBalancerProfileResponse']:
        """
        Profile of the cluster load balancer.
        """
        return pulumi.get(self, 'load_balancer_profile')

    @property
    @pulumi.getter(name='loadBalancerSku')
    def load_balancer_sku(self) -> Optional[str]:
        """
        The default is 'standard'. See [Azure Load Balancer SKUs](https://docs.microsoft.com/azure/load-balancer/skus) for more information about the differences between load balancer SKUs.
        """
        return pulumi.get(self, 'load_balancer_sku')

    @property
    @pulumi.getter(name='networkMode')
    def network_mode(self) -> Optional[str]:
        """
        This cannot be specified if networkPlugin is anything other than 'azure'.
        """
        return pulumi.get(self, 'network_mode')

    @property
    @pulumi.getter(name='networkPlugin')
    def network_plugin(self) -> Optional[str]:
        """
        Network plugin used for building the Kubernetes network.
        """
        return pulumi.get(self, 'network_plugin')

    @property
    @pulumi.getter(name='networkPolicy')
    def network_policy(self) -> Optional[str]:
        """
        Network policy used for building the Kubernetes network.
        """
        return pulumi.get(self, 'network_policy')

    @property
    @pulumi.getter(name='outboundType')
    def outbound_type(self) -> Optional[str]:
        """
        This can only be set at cluster creation time and cannot be changed later. For more information see [egress outbound type](https://docs.microsoft.com/azure/aks/egress-outboundtype).
        """
        return pulumi.get(self, 'outbound_type')

    @property
    @pulumi.getter(name='podCidr')
    def pod_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range from which to assign pod IPs when kubenet is used.
        """
        return pulumi.get(self, 'pod_cidr')

    @property
    @pulumi.getter(name='serviceCidr')
    def service_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
        """
        return pulumi.get(self, 'service_cidr')

@pulumi.output_type
class ContainerServiceSshConfigurationResponse(dict):
    """
    SSH configuration for Linux-based VMs running on Azure.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publicKeys':
            suggest = 'public_keys'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceSshConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceSshConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContainerServiceSshConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, public_keys: Sequence['outputs.ContainerServiceSshPublicKeyResponse']):
        """
        SSH configuration for Linux-based VMs running on Azure.
        :param Sequence['ContainerServiceSshPublicKeyResponse'] public_keys: The list of SSH public keys used to authenticate with Linux-based VMs. A maximum of 1 key may be specified.
        """
        pulumi.set(__self__, 'public_keys', public_keys)

    @property
    @pulumi.getter(name='publicKeys')
    def public_keys(self) -> Sequence['outputs.ContainerServiceSshPublicKeyResponse']:
        """
        The list of SSH public keys used to authenticate with Linux-based VMs. A maximum of 1 key may be specified.
        """
        return pulumi.get(self, 'public_keys')

@pulumi.output_type
class ContainerServiceSshPublicKeyResponse(dict):
    """
    Contains information about SSH certificate public key data.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'keyData':
            suggest = 'key_data'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceSshPublicKeyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceSshPublicKeyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ContainerServiceSshPublicKeyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, key_data: str):
        """
        Contains information about SSH certificate public key data.
        :param str key_data: Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        pulumi.set(__self__, 'key_data', key_data)

    @property
    @pulumi.getter(name='keyData')
    def key_data(self) -> str:
        """
        Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        return pulumi.get(self, 'key_data')

@pulumi.output_type
class CredentialResultResponse(dict):
    """
    The credential result response.
    """

    def __init__(__self__, *, name: str, value: str):
        """
        The credential result response.
        :param str name: The name of the credential.
        :param str value: Base64-encoded Kubernetes configuration file.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the credential.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Base64-encoded Kubernetes configuration file.
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class ExtendedLocationResponse(dict):
    """
    The complex type of the extended location.
    """

    def __init__(__self__, *, name: Optional[str]=None, type: Optional[str]=None):
        """
        The complex type of the extended location.
        :param str name: The name of the extended location.
        :param str type: The type of the extended location.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the extended location.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the extended location.
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class KubeletConfigResponse(dict):
    """
    See [AKS custom node configuration](https://docs.microsoft.com/azure/aks/custom-node-configuration) for more details.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'allowedUnsafeSysctls':
            suggest = 'allowed_unsafe_sysctls'
        elif key == 'containerLogMaxFiles':
            suggest = 'container_log_max_files'
        elif key == 'containerLogMaxSizeMB':
            suggest = 'container_log_max_size_mb'
        elif key == 'cpuCfsQuota':
            suggest = 'cpu_cfs_quota'
        elif key == 'cpuCfsQuotaPeriod':
            suggest = 'cpu_cfs_quota_period'
        elif key == 'cpuManagerPolicy':
            suggest = 'cpu_manager_policy'
        elif key == 'failSwapOn':
            suggest = 'fail_swap_on'
        elif key == 'imageGcHighThreshold':
            suggest = 'image_gc_high_threshold'
        elif key == 'imageGcLowThreshold':
            suggest = 'image_gc_low_threshold'
        elif key == 'podMaxPids':
            suggest = 'pod_max_pids'
        elif key == 'topologyManagerPolicy':
            suggest = 'topology_manager_policy'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubeletConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubeletConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        KubeletConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, allowed_unsafe_sysctls: Optional[Sequence[str]]=None, container_log_max_files: Optional[int]=None, container_log_max_size_mb: Optional[int]=None, cpu_cfs_quota: Optional[bool]=None, cpu_cfs_quota_period: Optional[str]=None, cpu_manager_policy: Optional[str]=None, fail_swap_on: Optional[bool]=None, image_gc_high_threshold: Optional[int]=None, image_gc_low_threshold: Optional[int]=None, pod_max_pids: Optional[int]=None, topology_manager_policy: Optional[str]=None):
        """
        See [AKS custom node configuration](https://docs.microsoft.com/azure/aks/custom-node-configuration) for more details.
        :param Sequence[str] allowed_unsafe_sysctls: Allowed list of unsafe sysctls or unsafe sysctl patterns (ending in `*`).
        :param int container_log_max_files: The maximum number of container log files that can be present for a container. The number must be ≥ 2.
        :param int container_log_max_size_mb: The maximum size (e.g. 10Mi) of container log file before it is rotated.
        :param bool cpu_cfs_quota: The default is true.
        :param str cpu_cfs_quota_period: The default is '100ms.' Valid values are a sequence of decimal numbers with an optional fraction and a unit suffix. For example: '300ms', '2h45m'. Supported units are 'ns', 'us', 'ms', 's', 'm', and 'h'.
        :param str cpu_manager_policy: The default is 'none'. See [Kubernetes CPU management policies](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/#cpu-management-policies) for more information. Allowed values are 'none' and 'static'.
        :param bool fail_swap_on: If set to true it will make the Kubelet fail to start if swap is enabled on the node.
        :param int image_gc_high_threshold: To disable image garbage collection, set to 100. The default is 85%
        :param int image_gc_low_threshold: This cannot be set higher than imageGcHighThreshold. The default is 80%
        :param int pod_max_pids: The maximum number of processes per pod.
        :param str topology_manager_policy: For more information see [Kubernetes Topology Manager](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager). The default is 'none'. Allowed values are 'none', 'best-effort', 'restricted', and 'single-numa-node'.
        """
        if allowed_unsafe_sysctls is not None:
            pulumi.set(__self__, 'allowed_unsafe_sysctls', allowed_unsafe_sysctls)
        if container_log_max_files is not None:
            pulumi.set(__self__, 'container_log_max_files', container_log_max_files)
        if container_log_max_size_mb is not None:
            pulumi.set(__self__, 'container_log_max_size_mb', container_log_max_size_mb)
        if cpu_cfs_quota is not None:
            pulumi.set(__self__, 'cpu_cfs_quota', cpu_cfs_quota)
        if cpu_cfs_quota_period is not None:
            pulumi.set(__self__, 'cpu_cfs_quota_period', cpu_cfs_quota_period)
        if cpu_manager_policy is not None:
            pulumi.set(__self__, 'cpu_manager_policy', cpu_manager_policy)
        if fail_swap_on is not None:
            pulumi.set(__self__, 'fail_swap_on', fail_swap_on)
        if image_gc_high_threshold is not None:
            pulumi.set(__self__, 'image_gc_high_threshold', image_gc_high_threshold)
        if image_gc_low_threshold is not None:
            pulumi.set(__self__, 'image_gc_low_threshold', image_gc_low_threshold)
        if pod_max_pids is not None:
            pulumi.set(__self__, 'pod_max_pids', pod_max_pids)
        if topology_manager_policy is not None:
            pulumi.set(__self__, 'topology_manager_policy', topology_manager_policy)

    @property
    @pulumi.getter(name='allowedUnsafeSysctls')
    def allowed_unsafe_sysctls(self) -> Optional[Sequence[str]]:
        """
        Allowed list of unsafe sysctls or unsafe sysctl patterns (ending in `*`).
        """
        return pulumi.get(self, 'allowed_unsafe_sysctls')

    @property
    @pulumi.getter(name='containerLogMaxFiles')
    def container_log_max_files(self) -> Optional[int]:
        """
        The maximum number of container log files that can be present for a container. The number must be ≥ 2.
        """
        return pulumi.get(self, 'container_log_max_files')

    @property
    @pulumi.getter(name='containerLogMaxSizeMB')
    def container_log_max_size_mb(self) -> Optional[int]:
        """
        The maximum size (e.g. 10Mi) of container log file before it is rotated.
        """
        return pulumi.get(self, 'container_log_max_size_mb')

    @property
    @pulumi.getter(name='cpuCfsQuota')
    def cpu_cfs_quota(self) -> Optional[bool]:
        """
        The default is true.
        """
        return pulumi.get(self, 'cpu_cfs_quota')

    @property
    @pulumi.getter(name='cpuCfsQuotaPeriod')
    def cpu_cfs_quota_period(self) -> Optional[str]:
        """
        The default is '100ms.' Valid values are a sequence of decimal numbers with an optional fraction and a unit suffix. For example: '300ms', '2h45m'. Supported units are 'ns', 'us', 'ms', 's', 'm', and 'h'.
        """
        return pulumi.get(self, 'cpu_cfs_quota_period')

    @property
    @pulumi.getter(name='cpuManagerPolicy')
    def cpu_manager_policy(self) -> Optional[str]:
        """
        The default is 'none'. See [Kubernetes CPU management policies](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/#cpu-management-policies) for more information. Allowed values are 'none' and 'static'.
        """
        return pulumi.get(self, 'cpu_manager_policy')

    @property
    @pulumi.getter(name='failSwapOn')
    def fail_swap_on(self) -> Optional[bool]:
        """
        If set to true it will make the Kubelet fail to start if swap is enabled on the node.
        """
        return pulumi.get(self, 'fail_swap_on')

    @property
    @pulumi.getter(name='imageGcHighThreshold')
    def image_gc_high_threshold(self) -> Optional[int]:
        """
        To disable image garbage collection, set to 100. The default is 85%
        """
        return pulumi.get(self, 'image_gc_high_threshold')

    @property
    @pulumi.getter(name='imageGcLowThreshold')
    def image_gc_low_threshold(self) -> Optional[int]:
        """
        This cannot be set higher than imageGcHighThreshold. The default is 80%
        """
        return pulumi.get(self, 'image_gc_low_threshold')

    @property
    @pulumi.getter(name='podMaxPids')
    def pod_max_pids(self) -> Optional[int]:
        """
        The maximum number of processes per pod.
        """
        return pulumi.get(self, 'pod_max_pids')

    @property
    @pulumi.getter(name='topologyManagerPolicy')
    def topology_manager_policy(self) -> Optional[str]:
        """
        For more information see [Kubernetes Topology Manager](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager). The default is 'none'. Allowed values are 'none', 'best-effort', 'restricted', and 'single-numa-node'.
        """
        return pulumi.get(self, 'topology_manager_policy')

@pulumi.output_type
class LinuxOSConfigResponse(dict):
    """
    See [AKS custom node configuration](https://docs.microsoft.com/azure/aks/custom-node-configuration) for more details.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'swapFileSizeMB':
            suggest = 'swap_file_size_mb'
        elif key == 'transparentHugePageDefrag':
            suggest = 'transparent_huge_page_defrag'
        elif key == 'transparentHugePageEnabled':
            suggest = 'transparent_huge_page_enabled'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LinuxOSConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LinuxOSConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        LinuxOSConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, swap_file_size_mb: Optional[int]=None, sysctls: Optional['outputs.SysctlConfigResponse']=None, transparent_huge_page_defrag: Optional[str]=None, transparent_huge_page_enabled: Optional[str]=None):
        """
        See [AKS custom node configuration](https://docs.microsoft.com/azure/aks/custom-node-configuration) for more details.
        :param int swap_file_size_mb: The size in MB of a swap file that will be created on each node.
        :param 'SysctlConfigResponse' sysctls: Sysctl settings for Linux agent nodes.
        :param str transparent_huge_page_defrag: Valid values are 'always', 'defer', 'defer+madvise', 'madvise' and 'never'. The default is 'madvise'. For more information see [Transparent Hugepages](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html#admin-guide-transhuge).
        :param str transparent_huge_page_enabled: Valid values are 'always', 'madvise', and 'never'. The default is 'always'. For more information see [Transparent Hugepages](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html#admin-guide-transhuge).
        """
        if swap_file_size_mb is not None:
            pulumi.set(__self__, 'swap_file_size_mb', swap_file_size_mb)
        if sysctls is not None:
            pulumi.set(__self__, 'sysctls', sysctls)
        if transparent_huge_page_defrag is not None:
            pulumi.set(__self__, 'transparent_huge_page_defrag', transparent_huge_page_defrag)
        if transparent_huge_page_enabled is not None:
            pulumi.set(__self__, 'transparent_huge_page_enabled', transparent_huge_page_enabled)

    @property
    @pulumi.getter(name='swapFileSizeMB')
    def swap_file_size_mb(self) -> Optional[int]:
        """
        The size in MB of a swap file that will be created on each node.
        """
        return pulumi.get(self, 'swap_file_size_mb')

    @property
    @pulumi.getter
    def sysctls(self) -> Optional['outputs.SysctlConfigResponse']:
        """
        Sysctl settings for Linux agent nodes.
        """
        return pulumi.get(self, 'sysctls')

    @property
    @pulumi.getter(name='transparentHugePageDefrag')
    def transparent_huge_page_defrag(self) -> Optional[str]:
        """
        Valid values are 'always', 'defer', 'defer+madvise', 'madvise' and 'never'. The default is 'madvise'. For more information see [Transparent Hugepages](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html#admin-guide-transhuge).
        """
        return pulumi.get(self, 'transparent_huge_page_defrag')

    @property
    @pulumi.getter(name='transparentHugePageEnabled')
    def transparent_huge_page_enabled(self) -> Optional[str]:
        """
        Valid values are 'always', 'madvise', and 'never'. The default is 'always'. For more information see [Transparent Hugepages](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html#admin-guide-transhuge).
        """
        return pulumi.get(self, 'transparent_huge_page_enabled')

@pulumi.output_type
class ManagedClusterAADProfileResponse(dict):
    """
    For more details see [managed AAD on AKS](https://docs.microsoft.com/azure/aks/managed-aad).
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'adminGroupObjectIDs':
            suggest = 'admin_group_object_ids'
        elif key == 'clientAppID':
            suggest = 'client_app_id'
        elif key == 'enableAzureRBAC':
            suggest = 'enable_azure_rbac'
        elif key == 'serverAppID':
            suggest = 'server_app_id'
        elif key == 'serverAppSecret':
            suggest = 'server_app_secret'
        elif key == 'tenantID':
            suggest = 'tenant_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAADProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAADProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterAADProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, admin_group_object_ids: Optional[Sequence[str]]=None, client_app_id: Optional[str]=None, enable_azure_rbac: Optional[bool]=None, managed: Optional[bool]=None, server_app_id: Optional[str]=None, server_app_secret: Optional[str]=None, tenant_id: Optional[str]=None):
        """
        For more details see [managed AAD on AKS](https://docs.microsoft.com/azure/aks/managed-aad).
        :param Sequence[str] admin_group_object_ids: The list of AAD group object IDs that will have admin role of the cluster.
        :param str client_app_id: The client AAD application ID.
        :param bool enable_azure_rbac: Whether to enable Azure RBAC for Kubernetes authorization.
        :param bool managed: Whether to enable managed AAD.
        :param str server_app_id: The server AAD application ID.
        :param str server_app_secret: The server AAD application secret.
        :param str tenant_id: The AAD tenant ID to use for authentication. If not specified, will use the tenant of the deployment subscription.
        """
        if admin_group_object_ids is not None:
            pulumi.set(__self__, 'admin_group_object_ids', admin_group_object_ids)
        if client_app_id is not None:
            pulumi.set(__self__, 'client_app_id', client_app_id)
        if enable_azure_rbac is not None:
            pulumi.set(__self__, 'enable_azure_rbac', enable_azure_rbac)
        if managed is not None:
            pulumi.set(__self__, 'managed', managed)
        if server_app_id is not None:
            pulumi.set(__self__, 'server_app_id', server_app_id)
        if server_app_secret is not None:
            pulumi.set(__self__, 'server_app_secret', server_app_secret)
        if tenant_id is not None:
            pulumi.set(__self__, 'tenant_id', tenant_id)

    @property
    @pulumi.getter(name='adminGroupObjectIDs')
    def admin_group_object_ids(self) -> Optional[Sequence[str]]:
        """
        The list of AAD group object IDs that will have admin role of the cluster.
        """
        return pulumi.get(self, 'admin_group_object_ids')

    @property
    @pulumi.getter(name='clientAppID')
    def client_app_id(self) -> Optional[str]:
        """
        The client AAD application ID.
        """
        return pulumi.get(self, 'client_app_id')

    @property
    @pulumi.getter(name='enableAzureRBAC')
    def enable_azure_rbac(self) -> Optional[bool]:
        """
        Whether to enable Azure RBAC for Kubernetes authorization.
        """
        return pulumi.get(self, 'enable_azure_rbac')

    @property
    @pulumi.getter
    def managed(self) -> Optional[bool]:
        """
        Whether to enable managed AAD.
        """
        return pulumi.get(self, 'managed')

    @property
    @pulumi.getter(name='serverAppID')
    def server_app_id(self) -> Optional[str]:
        """
        The server AAD application ID.
        """
        return pulumi.get(self, 'server_app_id')

    @property
    @pulumi.getter(name='serverAppSecret')
    def server_app_secret(self) -> Optional[str]:
        """
        The server AAD application secret.
        """
        return pulumi.get(self, 'server_app_secret')

    @property
    @pulumi.getter(name='tenantID')
    def tenant_id(self) -> Optional[str]:
        """
        The AAD tenant ID to use for authentication. If not specified, will use the tenant of the deployment subscription.
        """
        return pulumi.get(self, 'tenant_id')

@pulumi.output_type
class ManagedClusterAPIServerAccessProfileResponse(dict):
    """
    Access profile for managed cluster API server.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'authorizedIPRanges':
            suggest = 'authorized_ip_ranges'
        elif key == 'enablePrivateCluster':
            suggest = 'enable_private_cluster'
        elif key == 'enablePrivateClusterPublicFQDN':
            suggest = 'enable_private_cluster_public_fqdn'
        elif key == 'privateDNSZone':
            suggest = 'private_dns_zone'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAPIServerAccessProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAPIServerAccessProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterAPIServerAccessProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, authorized_ip_ranges: Optional[Sequence[str]]=None, enable_private_cluster: Optional[bool]=None, enable_private_cluster_public_fqdn: Optional[bool]=None, private_dns_zone: Optional[str]=None):
        """
        Access profile for managed cluster API server.
        :param Sequence[str] authorized_ip_ranges: IP ranges are specified in CIDR format, e.g. 137.117.106.88/29. This feature is not compatible with clusters that use Public IP Per Node, or clusters that are using a Basic Load Balancer. For more information see [API server authorized IP ranges](https://docs.microsoft.com/azure/aks/api-server-authorized-ip-ranges).
        :param bool enable_private_cluster: For more details, see [Creating a private AKS cluster](https://docs.microsoft.com/azure/aks/private-clusters).
        :param bool enable_private_cluster_public_fqdn: Whether to create additional public FQDN for private cluster or not.
        :param str private_dns_zone: The default is System. For more details see [configure private DNS zone](https://docs.microsoft.com/azure/aks/private-clusters#configure-private-dns-zone). Allowed values are 'system' and 'none'.
        """
        if authorized_ip_ranges is not None:
            pulumi.set(__self__, 'authorized_ip_ranges', authorized_ip_ranges)
        if enable_private_cluster is not None:
            pulumi.set(__self__, 'enable_private_cluster', enable_private_cluster)
        if enable_private_cluster_public_fqdn is not None:
            pulumi.set(__self__, 'enable_private_cluster_public_fqdn', enable_private_cluster_public_fqdn)
        if private_dns_zone is not None:
            pulumi.set(__self__, 'private_dns_zone', private_dns_zone)

    @property
    @pulumi.getter(name='authorizedIPRanges')
    def authorized_ip_ranges(self) -> Optional[Sequence[str]]:
        """
        IP ranges are specified in CIDR format, e.g. 137.117.106.88/29. This feature is not compatible with clusters that use Public IP Per Node, or clusters that are using a Basic Load Balancer. For more information see [API server authorized IP ranges](https://docs.microsoft.com/azure/aks/api-server-authorized-ip-ranges).
        """
        return pulumi.get(self, 'authorized_ip_ranges')

    @property
    @pulumi.getter(name='enablePrivateCluster')
    def enable_private_cluster(self) -> Optional[bool]:
        """
        For more details, see [Creating a private AKS cluster](https://docs.microsoft.com/azure/aks/private-clusters).
        """
        return pulumi.get(self, 'enable_private_cluster')

    @property
    @pulumi.getter(name='enablePrivateClusterPublicFQDN')
    def enable_private_cluster_public_fqdn(self) -> Optional[bool]:
        """
        Whether to create additional public FQDN for private cluster or not.
        """
        return pulumi.get(self, 'enable_private_cluster_public_fqdn')

    @property
    @pulumi.getter(name='privateDNSZone')
    def private_dns_zone(self) -> Optional[str]:
        """
        The default is System. For more details see [configure private DNS zone](https://docs.microsoft.com/azure/aks/private-clusters#configure-private-dns-zone). Allowed values are 'system' and 'none'.
        """
        return pulumi.get(self, 'private_dns_zone')

@pulumi.output_type
class ManagedClusterAddonProfileResponse(dict):
    """
    A Kubernetes add-on profile for a managed cluster.
    """

    def __init__(__self__, *, enabled: bool, identity: 'outputs.ManagedClusterAddonProfileResponseIdentity', config: Optional[Mapping[str, str]]=None):
        """
        A Kubernetes add-on profile for a managed cluster.
        :param bool enabled: Whether the add-on is enabled or not.
        :param 'ManagedClusterAddonProfileResponseIdentity' identity: Information of user assigned identity used by this add-on.
        :param Mapping[str, str] config: Key-value pairs for configuring an add-on.
        """
        pulumi.set(__self__, 'enabled', enabled)
        pulumi.set(__self__, 'identity', identity)
        if config is not None:
            pulumi.set(__self__, 'config', config)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Whether the add-on is enabled or not.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def identity(self) -> 'outputs.ManagedClusterAddonProfileResponseIdentity':
        """
        Information of user assigned identity used by this add-on.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def config(self) -> Optional[Mapping[str, str]]:
        """
        Key-value pairs for configuring an add-on.
        """
        return pulumi.get(self, 'config')

@pulumi.output_type
class ManagedClusterAddonProfileResponseIdentity(dict):
    """
    Information of user assigned identity used by this add-on.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'objectId':
            suggest = 'object_id'
        elif key == 'resourceId':
            suggest = 'resource_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAddonProfileResponseIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAddonProfileResponseIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterAddonProfileResponseIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: Optional[str]=None, object_id: Optional[str]=None, resource_id: Optional[str]=None):
        """
        Information of user assigned identity used by this add-on.
        :param str client_id: The client ID of the user assigned identity.
        :param str object_id: The object ID of the user assigned identity.
        :param str resource_id: The resource ID of the user assigned identity.
        """
        if client_id is not None:
            pulumi.set(__self__, 'client_id', client_id)
        if object_id is not None:
            pulumi.set(__self__, 'object_id', object_id)
        if resource_id is not None:
            pulumi.set(__self__, 'resource_id', resource_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> Optional[str]:
        """
        The client ID of the user assigned identity.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='objectId')
    def object_id(self) -> Optional[str]:
        """
        The object ID of the user assigned identity.
        """
        return pulumi.get(self, 'object_id')

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> Optional[str]:
        """
        The resource ID of the user assigned identity.
        """
        return pulumi.get(self, 'resource_id')

@pulumi.output_type
class ManagedClusterAgentPoolProfileResponse(dict):
    """
    Profile for the container service agent pool.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'nodeImageVersion':
            suggest = 'node_image_version'
        elif key == 'powerState':
            suggest = 'power_state'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'availabilityZones':
            suggest = 'availability_zones'
        elif key == 'enableAutoScaling':
            suggest = 'enable_auto_scaling'
        elif key == 'enableEncryptionAtHost':
            suggest = 'enable_encryption_at_host'
        elif key == 'enableFIPS':
            suggest = 'enable_fips'
        elif key == 'enableNodePublicIP':
            suggest = 'enable_node_public_ip'
        elif key == 'enableUltraSSD':
            suggest = 'enable_ultra_ssd'
        elif key == 'gpuInstanceProfile':
            suggest = 'gpu_instance_profile'
        elif key == 'kubeletConfig':
            suggest = 'kubelet_config'
        elif key == 'kubeletDiskType':
            suggest = 'kubelet_disk_type'
        elif key == 'linuxOSConfig':
            suggest = 'linux_os_config'
        elif key == 'maxCount':
            suggest = 'max_count'
        elif key == 'maxPods':
            suggest = 'max_pods'
        elif key == 'minCount':
            suggest = 'min_count'
        elif key == 'nodeLabels':
            suggest = 'node_labels'
        elif key == 'nodePublicIPPrefixID':
            suggest = 'node_public_ip_prefix_id'
        elif key == 'nodeTaints':
            suggest = 'node_taints'
        elif key == 'orchestratorVersion':
            suggest = 'orchestrator_version'
        elif key == 'osDiskSizeGB':
            suggest = 'os_disk_size_gb'
        elif key == 'osDiskType':
            suggest = 'os_disk_type'
        elif key == 'osSKU':
            suggest = 'os_sku'
        elif key == 'osType':
            suggest = 'os_type'
        elif key == 'podSubnetID':
            suggest = 'pod_subnet_id'
        elif key == 'proximityPlacementGroupID':
            suggest = 'proximity_placement_group_id'
        elif key == 'scaleSetEvictionPolicy':
            suggest = 'scale_set_eviction_policy'
        elif key == 'scaleSetPriority':
            suggest = 'scale_set_priority'
        elif key == 'spotMaxPrice':
            suggest = 'spot_max_price'
        elif key == 'upgradeSettings':
            suggest = 'upgrade_settings'
        elif key == 'vmSize':
            suggest = 'vm_size'
        elif key == 'vnetSubnetID':
            suggest = 'vnet_subnet_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAgentPoolProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAgentPoolProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterAgentPoolProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, name: str, node_image_version: str, power_state: 'outputs.PowerStateResponse', provisioning_state: str, availability_zones: Optional[Sequence[str]]=None, count: Optional[int]=None, enable_auto_scaling: Optional[bool]=None, enable_encryption_at_host: Optional[bool]=None, enable_fips: Optional[bool]=None, enable_node_public_ip: Optional[bool]=None, enable_ultra_ssd: Optional[bool]=None, gpu_instance_profile: Optional[str]=None, kubelet_config: Optional['outputs.KubeletConfigResponse']=None, kubelet_disk_type: Optional[str]=None, linux_os_config: Optional['outputs.LinuxOSConfigResponse']=None, max_count: Optional[int]=None, max_pods: Optional[int]=None, min_count: Optional[int]=None, mode: Optional[str]=None, node_labels: Optional[Mapping[str, str]]=None, node_public_ip_prefix_id: Optional[str]=None, node_taints: Optional[Sequence[str]]=None, orchestrator_version: Optional[str]=None, os_disk_size_gb: Optional[int]=None, os_disk_type: Optional[str]=None, os_sku: Optional[str]=None, os_type: Optional[str]=None, pod_subnet_id: Optional[str]=None, proximity_placement_group_id: Optional[str]=None, scale_set_eviction_policy: Optional[str]=None, scale_set_priority: Optional[str]=None, spot_max_price: Optional[float]=None, tags: Optional[Mapping[str, str]]=None, type: Optional[str]=None, upgrade_settings: Optional['outputs.AgentPoolUpgradeSettingsResponse']=None, vm_size: Optional[str]=None, vnet_subnet_id: Optional[str]=None):
        """
        Profile for the container service agent pool.
        :param str name: Windows agent pool names must be 6 characters or less.
        :param str node_image_version: The version of node image
        :param 'PowerStateResponse' power_state: Describes whether the Agent Pool is Running or Stopped
        :param str provisioning_state: The current deployment or provisioning state.
        :param Sequence[str] availability_zones: The list of Availability zones to use for nodes. This can only be specified if the AgentPoolType property is 'VirtualMachineScaleSets'.
        :param int count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 0 to 1000 (inclusive) for user pools and in the range of 1 to 1000 (inclusive) for system pools. The default value is 1.
        :param bool enable_auto_scaling: Whether to enable auto-scaler
        :param bool enable_encryption_at_host: This is only supported on certain VM sizes and in certain Azure regions. For more information, see: https://docs.microsoft.com/azure/aks/enable-host-encryption
        :param bool enable_fips: See [Add a FIPS-enabled node pool](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#add-a-fips-enabled-node-pool-preview) for more details.
        :param bool enable_node_public_ip: Some scenarios may require nodes in a node pool to receive their own dedicated public IP addresses. A common scenario is for gaming workloads, where a console needs to make a direct connection to a cloud virtual machine to minimize hops. For more information see [assigning a public IP per node](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#assign-a-public-ip-per-node-for-your-node-pools). The default is false.
        :param bool enable_ultra_ssd: Whether to enable UltraSSD
        :param str gpu_instance_profile: GPUInstanceProfile to be used to specify GPU MIG instance profile for supported GPU VM SKU.
        :param 'KubeletConfigResponse' kubelet_config: The Kubelet configuration on the agent pool nodes.
        :param str kubelet_disk_type: Determines the placement of emptyDir volumes, container runtime data root, and Kubelet ephemeral storage.
        :param 'LinuxOSConfigResponse' linux_os_config: The OS configuration of Linux agent nodes.
        :param int max_count: The maximum number of nodes for auto-scaling
        :param int max_pods: The maximum number of pods that can run on a node.
        :param int min_count: The minimum number of nodes for auto-scaling
        :param str mode: A cluster must have at least one 'System' Agent Pool at all times. For additional information on agent pool restrictions and best practices, see: https://docs.microsoft.com/azure/aks/use-system-pools
        :param Mapping[str, str] node_labels: The node labels to be persisted across all nodes in agent pool.
        :param str node_public_ip_prefix_id: This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPPrefixes/{publicIPPrefixName}
        :param Sequence[str] node_taints: The taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        :param str orchestrator_version: As a best practice, you should upgrade all node pools in an AKS cluster to the same Kubernetes version. The node pool version must have the same major version as the control plane. The node pool minor version must be within two minor versions of the control plane version. The node pool version cannot be greater than the control plane version. For more information see [upgrading a node pool](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#upgrade-a-node-pool).
        :param int os_disk_size_gb: OS Disk Size in GB to be used to specify the disk size for every machine in the master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        :param str os_disk_type: The default is 'Ephemeral' if the VM supports it and has a cache disk larger than the requested OSDiskSizeGB. Otherwise, defaults to 'Managed'. May not be changed after creation. For more information see [Ephemeral OS](https://docs.microsoft.com/azure/aks/cluster-configuration#ephemeral-os).
        :param str os_sku: Specifies an OS SKU. This value must not be specified if OSType is Windows.
        :param str os_type: The operating system type. The default is Linux.
        :param str pod_subnet_id: If omitted, pod IPs are statically assigned on the node subnet (see vnetSubnetID for more details). This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}
        :param str proximity_placement_group_id: The ID for Proximity Placement Group.
        :param str scale_set_eviction_policy: This cannot be specified unless the scaleSetPriority is 'Spot'. If not specified, the default is 'Delete'.
        :param str scale_set_priority: The Virtual Machine Scale Set priority. If not specified, the default is 'Regular'.
        :param float spot_max_price: Possible values are any decimal value greater than zero or -1 which indicates the willingness to pay any on-demand price. For more details on spot pricing, see [spot VMs pricing](https://docs.microsoft.com/azure/virtual-machines/spot-vms#pricing)
        :param Mapping[str, str] tags: The tags to be persisted on the agent pool virtual machine scale set.
        :param str type: The type of Agent Pool.
        :param 'AgentPoolUpgradeSettingsResponse' upgrade_settings: Settings for upgrading the agentpool
        :param str vm_size: VM size availability varies by region. If a node contains insufficient compute resources (memory, cpu, etc) pods might fail to run correctly. For more details on restricted VM sizes, see: https://docs.microsoft.com/azure/aks/quotas-skus-regions
        :param str vnet_subnet_id: If this is not specified, a VNET and subnet will be generated and used. If no podSubnetID is specified, this applies to nodes and pods, otherwise it applies to just nodes. This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'node_image_version', node_image_version)
        pulumi.set(__self__, 'power_state', power_state)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if availability_zones is not None:
            pulumi.set(__self__, 'availability_zones', availability_zones)
        if count is not None:
            pulumi.set(__self__, 'count', count)
        if enable_auto_scaling is not None:
            pulumi.set(__self__, 'enable_auto_scaling', enable_auto_scaling)
        if enable_encryption_at_host is not None:
            pulumi.set(__self__, 'enable_encryption_at_host', enable_encryption_at_host)
        if enable_fips is not None:
            pulumi.set(__self__, 'enable_fips', enable_fips)
        if enable_node_public_ip is not None:
            pulumi.set(__self__, 'enable_node_public_ip', enable_node_public_ip)
        if enable_ultra_ssd is not None:
            pulumi.set(__self__, 'enable_ultra_ssd', enable_ultra_ssd)
        if gpu_instance_profile is not None:
            pulumi.set(__self__, 'gpu_instance_profile', gpu_instance_profile)
        if kubelet_config is not None:
            pulumi.set(__self__, 'kubelet_config', kubelet_config)
        if kubelet_disk_type is not None:
            pulumi.set(__self__, 'kubelet_disk_type', kubelet_disk_type)
        if linux_os_config is not None:
            pulumi.set(__self__, 'linux_os_config', linux_os_config)
        if max_count is not None:
            pulumi.set(__self__, 'max_count', max_count)
        if max_pods is not None:
            pulumi.set(__self__, 'max_pods', max_pods)
        if min_count is not None:
            pulumi.set(__self__, 'min_count', min_count)
        if mode is not None:
            pulumi.set(__self__, 'mode', mode)
        if node_labels is not None:
            pulumi.set(__self__, 'node_labels', node_labels)
        if node_public_ip_prefix_id is not None:
            pulumi.set(__self__, 'node_public_ip_prefix_id', node_public_ip_prefix_id)
        if node_taints is not None:
            pulumi.set(__self__, 'node_taints', node_taints)
        if orchestrator_version is not None:
            pulumi.set(__self__, 'orchestrator_version', orchestrator_version)
        if os_disk_size_gb is not None:
            pulumi.set(__self__, 'os_disk_size_gb', os_disk_size_gb)
        if os_disk_type is not None:
            pulumi.set(__self__, 'os_disk_type', os_disk_type)
        if os_sku is not None:
            pulumi.set(__self__, 'os_sku', os_sku)
        if os_type is not None:
            pulumi.set(__self__, 'os_type', os_type)
        if pod_subnet_id is not None:
            pulumi.set(__self__, 'pod_subnet_id', pod_subnet_id)
        if proximity_placement_group_id is not None:
            pulumi.set(__self__, 'proximity_placement_group_id', proximity_placement_group_id)
        if scale_set_eviction_policy is not None:
            pulumi.set(__self__, 'scale_set_eviction_policy', scale_set_eviction_policy)
        if scale_set_priority is not None:
            pulumi.set(__self__, 'scale_set_priority', scale_set_priority)
        if spot_max_price is not None:
            pulumi.set(__self__, 'spot_max_price', spot_max_price)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if upgrade_settings is not None:
            pulumi.set(__self__, 'upgrade_settings', upgrade_settings)
        if vm_size is not None:
            pulumi.set(__self__, 'vm_size', vm_size)
        if vnet_subnet_id is not None:
            pulumi.set(__self__, 'vnet_subnet_id', vnet_subnet_id)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Windows agent pool names must be 6 characters or less.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='nodeImageVersion')
    def node_image_version(self) -> str:
        """
        The version of node image
        """
        return pulumi.get(self, 'node_image_version')

    @property
    @pulumi.getter(name='powerState')
    def power_state(self) -> 'outputs.PowerStateResponse':
        """
        Describes whether the Agent Pool is Running or Stopped
        """
        return pulumi.get(self, 'power_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The current deployment or provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='availabilityZones')
    def availability_zones(self) -> Optional[Sequence[str]]:
        """
        The list of Availability zones to use for nodes. This can only be specified if the AgentPoolType property is 'VirtualMachineScaleSets'.
        """
        return pulumi.get(self, 'availability_zones')

    @property
    @pulumi.getter
    def count(self) -> Optional[int]:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 0 to 1000 (inclusive) for user pools and in the range of 1 to 1000 (inclusive) for system pools. The default value is 1.
        """
        return pulumi.get(self, 'count')

    @property
    @pulumi.getter(name='enableAutoScaling')
    def enable_auto_scaling(self) -> Optional[bool]:
        """
        Whether to enable auto-scaler
        """
        return pulumi.get(self, 'enable_auto_scaling')

    @property
    @pulumi.getter(name='enableEncryptionAtHost')
    def enable_encryption_at_host(self) -> Optional[bool]:
        """
        This is only supported on certain VM sizes and in certain Azure regions. For more information, see: https://docs.microsoft.com/azure/aks/enable-host-encryption
        """
        return pulumi.get(self, 'enable_encryption_at_host')

    @property
    @pulumi.getter(name='enableFIPS')
    def enable_fips(self) -> Optional[bool]:
        """
        See [Add a FIPS-enabled node pool](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#add-a-fips-enabled-node-pool-preview) for more details.
        """
        return pulumi.get(self, 'enable_fips')

    @property
    @pulumi.getter(name='enableNodePublicIP')
    def enable_node_public_ip(self) -> Optional[bool]:
        """
        Some scenarios may require nodes in a node pool to receive their own dedicated public IP addresses. A common scenario is for gaming workloads, where a console needs to make a direct connection to a cloud virtual machine to minimize hops. For more information see [assigning a public IP per node](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#assign-a-public-ip-per-node-for-your-node-pools). The default is false.
        """
        return pulumi.get(self, 'enable_node_public_ip')

    @property
    @pulumi.getter(name='enableUltraSSD')
    def enable_ultra_ssd(self) -> Optional[bool]:
        """
        Whether to enable UltraSSD
        """
        return pulumi.get(self, 'enable_ultra_ssd')

    @property
    @pulumi.getter(name='gpuInstanceProfile')
    def gpu_instance_profile(self) -> Optional[str]:
        """
        GPUInstanceProfile to be used to specify GPU MIG instance profile for supported GPU VM SKU.
        """
        return pulumi.get(self, 'gpu_instance_profile')

    @property
    @pulumi.getter(name='kubeletConfig')
    def kubelet_config(self) -> Optional['outputs.KubeletConfigResponse']:
        """
        The Kubelet configuration on the agent pool nodes.
        """
        return pulumi.get(self, 'kubelet_config')

    @property
    @pulumi.getter(name='kubeletDiskType')
    def kubelet_disk_type(self) -> Optional[str]:
        """
        Determines the placement of emptyDir volumes, container runtime data root, and Kubelet ephemeral storage.
        """
        return pulumi.get(self, 'kubelet_disk_type')

    @property
    @pulumi.getter(name='linuxOSConfig')
    def linux_os_config(self) -> Optional['outputs.LinuxOSConfigResponse']:
        """
        The OS configuration of Linux agent nodes.
        """
        return pulumi.get(self, 'linux_os_config')

    @property
    @pulumi.getter(name='maxCount')
    def max_count(self) -> Optional[int]:
        """
        The maximum number of nodes for auto-scaling
        """
        return pulumi.get(self, 'max_count')

    @property
    @pulumi.getter(name='maxPods')
    def max_pods(self) -> Optional[int]:
        """
        The maximum number of pods that can run on a node.
        """
        return pulumi.get(self, 'max_pods')

    @property
    @pulumi.getter(name='minCount')
    def min_count(self) -> Optional[int]:
        """
        The minimum number of nodes for auto-scaling
        """
        return pulumi.get(self, 'min_count')

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        A cluster must have at least one 'System' Agent Pool at all times. For additional information on agent pool restrictions and best practices, see: https://docs.microsoft.com/azure/aks/use-system-pools
        """
        return pulumi.get(self, 'mode')

    @property
    @pulumi.getter(name='nodeLabels')
    def node_labels(self) -> Optional[Mapping[str, str]]:
        """
        The node labels to be persisted across all nodes in agent pool.
        """
        return pulumi.get(self, 'node_labels')

    @property
    @pulumi.getter(name='nodePublicIPPrefixID')
    def node_public_ip_prefix_id(self) -> Optional[str]:
        """
        This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPPrefixes/{publicIPPrefixName}
        """
        return pulumi.get(self, 'node_public_ip_prefix_id')

    @property
    @pulumi.getter(name='nodeTaints')
    def node_taints(self) -> Optional[Sequence[str]]:
        """
        The taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        """
        return pulumi.get(self, 'node_taints')

    @property
    @pulumi.getter(name='orchestratorVersion')
    def orchestrator_version(self) -> Optional[str]:
        """
        As a best practice, you should upgrade all node pools in an AKS cluster to the same Kubernetes version. The node pool version must have the same major version as the control plane. The node pool minor version must be within two minor versions of the control plane version. The node pool version cannot be greater than the control plane version. For more information see [upgrading a node pool](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#upgrade-a-node-pool).
        """
        return pulumi.get(self, 'orchestrator_version')

    @property
    @pulumi.getter(name='osDiskSizeGB')
    def os_disk_size_gb(self) -> Optional[int]:
        """
        OS Disk Size in GB to be used to specify the disk size for every machine in the master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        """
        return pulumi.get(self, 'os_disk_size_gb')

    @property
    @pulumi.getter(name='osDiskType')
    def os_disk_type(self) -> Optional[str]:
        """
        The default is 'Ephemeral' if the VM supports it and has a cache disk larger than the requested OSDiskSizeGB. Otherwise, defaults to 'Managed'. May not be changed after creation. For more information see [Ephemeral OS](https://docs.microsoft.com/azure/aks/cluster-configuration#ephemeral-os).
        """
        return pulumi.get(self, 'os_disk_type')

    @property
    @pulumi.getter(name='osSKU')
    def os_sku(self) -> Optional[str]:
        """
        Specifies an OS SKU. This value must not be specified if OSType is Windows.
        """
        return pulumi.get(self, 'os_sku')

    @property
    @pulumi.getter(name='osType')
    def os_type(self) -> Optional[str]:
        """
        The operating system type. The default is Linux.
        """
        return pulumi.get(self, 'os_type')

    @property
    @pulumi.getter(name='podSubnetID')
    def pod_subnet_id(self) -> Optional[str]:
        """
        If omitted, pod IPs are statically assigned on the node subnet (see vnetSubnetID for more details). This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}
        """
        return pulumi.get(self, 'pod_subnet_id')

    @property
    @pulumi.getter(name='proximityPlacementGroupID')
    def proximity_placement_group_id(self) -> Optional[str]:
        """
        The ID for Proximity Placement Group.
        """
        return pulumi.get(self, 'proximity_placement_group_id')

    @property
    @pulumi.getter(name='scaleSetEvictionPolicy')
    def scale_set_eviction_policy(self) -> Optional[str]:
        """
        This cannot be specified unless the scaleSetPriority is 'Spot'. If not specified, the default is 'Delete'.
        """
        return pulumi.get(self, 'scale_set_eviction_policy')

    @property
    @pulumi.getter(name='scaleSetPriority')
    def scale_set_priority(self) -> Optional[str]:
        """
        The Virtual Machine Scale Set priority. If not specified, the default is 'Regular'.
        """
        return pulumi.get(self, 'scale_set_priority')

    @property
    @pulumi.getter(name='spotMaxPrice')
    def spot_max_price(self) -> Optional[float]:
        """
        Possible values are any decimal value greater than zero or -1 which indicates the willingness to pay any on-demand price. For more details on spot pricing, see [spot VMs pricing](https://docs.microsoft.com/azure/virtual-machines/spot-vms#pricing)
        """
        return pulumi.get(self, 'spot_max_price')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags to be persisted on the agent pool virtual machine scale set.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of Agent Pool.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='upgradeSettings')
    def upgrade_settings(self) -> Optional['outputs.AgentPoolUpgradeSettingsResponse']:
        """
        Settings for upgrading the agentpool
        """
        return pulumi.get(self, 'upgrade_settings')

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> Optional[str]:
        """
        VM size availability varies by region. If a node contains insufficient compute resources (memory, cpu, etc) pods might fail to run correctly. For more details on restricted VM sizes, see: https://docs.microsoft.com/azure/aks/quotas-skus-regions
        """
        return pulumi.get(self, 'vm_size')

    @property
    @pulumi.getter(name='vnetSubnetID')
    def vnet_subnet_id(self) -> Optional[str]:
        """
        If this is not specified, a VNET and subnet will be generated and used. If no podSubnetID is specified, this applies to nodes and pods, otherwise it applies to just nodes. This is of the form: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}
        """
        return pulumi.get(self, 'vnet_subnet_id')

@pulumi.output_type
class ManagedClusterAutoUpgradeProfileResponse(dict):
    """
    Auto upgrade profile for a managed cluster.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'upgradeChannel':
            suggest = 'upgrade_channel'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAutoUpgradeProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAutoUpgradeProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterAutoUpgradeProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, upgrade_channel: Optional[str]=None):
        """
        Auto upgrade profile for a managed cluster.
        :param str upgrade_channel: For more information see [setting the AKS cluster auto-upgrade channel](https://docs.microsoft.com/azure/aks/upgrade-cluster#set-auto-upgrade-channel).
        """
        if upgrade_channel is not None:
            pulumi.set(__self__, 'upgrade_channel', upgrade_channel)

    @property
    @pulumi.getter(name='upgradeChannel')
    def upgrade_channel(self) -> Optional[str]:
        """
        For more information see [setting the AKS cluster auto-upgrade channel](https://docs.microsoft.com/azure/aks/upgrade-cluster#set-auto-upgrade-channel).
        """
        return pulumi.get(self, 'upgrade_channel')

@pulumi.output_type
class ManagedClusterHTTPProxyConfigResponse(dict):
    """
    Cluster HTTP proxy configuration.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'httpProxy':
            suggest = 'http_proxy'
        elif key == 'httpsProxy':
            suggest = 'https_proxy'
        elif key == 'noProxy':
            suggest = 'no_proxy'
        elif key == 'trustedCa':
            suggest = 'trusted_ca'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterHTTPProxyConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterHTTPProxyConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterHTTPProxyConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, http_proxy: Optional[str]=None, https_proxy: Optional[str]=None, no_proxy: Optional[Sequence[str]]=None, trusted_ca: Optional[str]=None):
        """
        Cluster HTTP proxy configuration.
        :param str http_proxy: The HTTP proxy server endpoint to use.
        :param str https_proxy: The HTTPS proxy server endpoint to use.
        :param Sequence[str] no_proxy: The endpoints that should not go through proxy.
        :param str trusted_ca: Alternative CA cert to use for connecting to proxy servers.
        """
        if http_proxy is not None:
            pulumi.set(__self__, 'http_proxy', http_proxy)
        if https_proxy is not None:
            pulumi.set(__self__, 'https_proxy', https_proxy)
        if no_proxy is not None:
            pulumi.set(__self__, 'no_proxy', no_proxy)
        if trusted_ca is not None:
            pulumi.set(__self__, 'trusted_ca', trusted_ca)

    @property
    @pulumi.getter(name='httpProxy')
    def http_proxy(self) -> Optional[str]:
        """
        The HTTP proxy server endpoint to use.
        """
        return pulumi.get(self, 'http_proxy')

    @property
    @pulumi.getter(name='httpsProxy')
    def https_proxy(self) -> Optional[str]:
        """
        The HTTPS proxy server endpoint to use.
        """
        return pulumi.get(self, 'https_proxy')

    @property
    @pulumi.getter(name='noProxy')
    def no_proxy(self) -> Optional[Sequence[str]]:
        """
        The endpoints that should not go through proxy.
        """
        return pulumi.get(self, 'no_proxy')

    @property
    @pulumi.getter(name='trustedCa')
    def trusted_ca(self) -> Optional[str]:
        """
        Alternative CA cert to use for connecting to proxy servers.
        """
        return pulumi.get(self, 'trusted_ca')

@pulumi.output_type
class ManagedClusterIdentityResponse(dict):
    """
    Identity for the managed cluster.
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
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, principal_id: str, tenant_id: str, type: Optional[str]=None, user_assigned_identities: Optional[Mapping[str, 'outputs.ManagedClusterIdentityResponseUserAssignedIdentities']]=None):
        """
        Identity for the managed cluster.
        :param str principal_id: The principal id of the system assigned identity which is used by master components.
        :param str tenant_id: The tenant id of the system assigned identity which is used by master components.
        :param str type: For more information see [use managed identities in AKS](https://docs.microsoft.com/azure/aks/use-managed-identity).
        :param Mapping[str, 'ManagedClusterIdentityResponseUserAssignedIdentities'] user_assigned_identities: The keys must be ARM resource IDs in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, 'principal_id', principal_id)
        pulumi.set(__self__, 'tenant_id', tenant_id)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, 'user_assigned_identities', user_assigned_identities)

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> str:
        """
        The principal id of the system assigned identity which is used by master components.
        """
        return pulumi.get(self, 'principal_id')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> str:
        """
        The tenant id of the system assigned identity which is used by master components.
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        For more information see [use managed identities in AKS](https://docs.microsoft.com/azure/aks/use-managed-identity).
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userAssignedIdentities')
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.ManagedClusterIdentityResponseUserAssignedIdentities']]:
        """
        The keys must be ARM resource IDs in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, 'user_assigned_identities')

@pulumi.output_type
class ManagedClusterIdentityResponseUserAssignedIdentities(dict):

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'principalId':
            suggest = 'principal_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterIdentityResponseUserAssignedIdentities. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterIdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterIdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: str, principal_id: str):
        """
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, 'client_id', client_id)
        pulumi.set(__self__, 'principal_id', principal_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, 'principal_id')

@pulumi.output_type
class ManagedClusterLoadBalancerProfileResponse(dict):
    """
    Profile of the managed cluster load balancer.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'allocatedOutboundPorts':
            suggest = 'allocated_outbound_ports'
        elif key == 'effectiveOutboundIPs':
            suggest = 'effective_outbound_ips'
        elif key == 'idleTimeoutInMinutes':
            suggest = 'idle_timeout_in_minutes'
        elif key == 'managedOutboundIPs':
            suggest = 'managed_outbound_ips'
        elif key == 'outboundIPPrefixes':
            suggest = 'outbound_ip_prefixes'
        elif key == 'outboundIPs':
            suggest = 'outbound_ips'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterLoadBalancerProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterLoadBalancerProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterLoadBalancerProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, allocated_outbound_ports: Optional[int]=None, effective_outbound_ips: Optional[Sequence['outputs.ResourceReferenceResponse']]=None, idle_timeout_in_minutes: Optional[int]=None, managed_outbound_ips: Optional['outputs.ManagedClusterLoadBalancerProfileResponseManagedOutboundIPs']=None, outbound_ip_prefixes: Optional['outputs.ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes']=None, outbound_ips: Optional['outputs.ManagedClusterLoadBalancerProfileResponseOutboundIPs']=None):
        """
        Profile of the managed cluster load balancer.
        :param int allocated_outbound_ports: The desired number of allocated SNAT ports per VM. Allowed values are in the range of 0 to 64000 (inclusive). The default value is 0 which results in Azure dynamically allocating ports.
        :param Sequence['ResourceReferenceResponse'] effective_outbound_ips: The effective outbound IP resources of the cluster load balancer.
        :param int idle_timeout_in_minutes: Desired outbound flow idle timeout in minutes. Allowed values are in the range of 4 to 120 (inclusive). The default value is 30 minutes.
        :param 'ManagedClusterLoadBalancerProfileResponseManagedOutboundIPs' managed_outbound_ips: Desired managed outbound IPs for the cluster load balancer.
        :param 'ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes' outbound_ip_prefixes: Desired outbound IP Prefix resources for the cluster load balancer.
        :param 'ManagedClusterLoadBalancerProfileResponseOutboundIPs' outbound_ips: Desired outbound IP resources for the cluster load balancer.
        """
        if allocated_outbound_ports is None:
            allocated_outbound_ports = 0
        if allocated_outbound_ports is not None:
            pulumi.set(__self__, 'allocated_outbound_ports', allocated_outbound_ports)
        if effective_outbound_ips is not None:
            pulumi.set(__self__, 'effective_outbound_ips', effective_outbound_ips)
        if idle_timeout_in_minutes is None:
            idle_timeout_in_minutes = 30
        if idle_timeout_in_minutes is not None:
            pulumi.set(__self__, 'idle_timeout_in_minutes', idle_timeout_in_minutes)
        if managed_outbound_ips is not None:
            pulumi.set(__self__, 'managed_outbound_ips', managed_outbound_ips)
        if outbound_ip_prefixes is not None:
            pulumi.set(__self__, 'outbound_ip_prefixes', outbound_ip_prefixes)
        if outbound_ips is not None:
            pulumi.set(__self__, 'outbound_ips', outbound_ips)

    @property
    @pulumi.getter(name='allocatedOutboundPorts')
    def allocated_outbound_ports(self) -> Optional[int]:
        """
        The desired number of allocated SNAT ports per VM. Allowed values are in the range of 0 to 64000 (inclusive). The default value is 0 which results in Azure dynamically allocating ports.
        """
        return pulumi.get(self, 'allocated_outbound_ports')

    @property
    @pulumi.getter(name='effectiveOutboundIPs')
    def effective_outbound_ips(self) -> Optional[Sequence['outputs.ResourceReferenceResponse']]:
        """
        The effective outbound IP resources of the cluster load balancer.
        """
        return pulumi.get(self, 'effective_outbound_ips')

    @property
    @pulumi.getter(name='idleTimeoutInMinutes')
    def idle_timeout_in_minutes(self) -> Optional[int]:
        """
        Desired outbound flow idle timeout in minutes. Allowed values are in the range of 4 to 120 (inclusive). The default value is 30 minutes.
        """
        return pulumi.get(self, 'idle_timeout_in_minutes')

    @property
    @pulumi.getter(name='managedOutboundIPs')
    def managed_outbound_ips(self) -> Optional['outputs.ManagedClusterLoadBalancerProfileResponseManagedOutboundIPs']:
        """
        Desired managed outbound IPs for the cluster load balancer.
        """
        return pulumi.get(self, 'managed_outbound_ips')

    @property
    @pulumi.getter(name='outboundIPPrefixes')
    def outbound_ip_prefixes(self) -> Optional['outputs.ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes']:
        """
        Desired outbound IP Prefix resources for the cluster load balancer.
        """
        return pulumi.get(self, 'outbound_ip_prefixes')

    @property
    @pulumi.getter(name='outboundIPs')
    def outbound_ips(self) -> Optional['outputs.ManagedClusterLoadBalancerProfileResponseOutboundIPs']:
        """
        Desired outbound IP resources for the cluster load balancer.
        """
        return pulumi.get(self, 'outbound_ips')

@pulumi.output_type
class ManagedClusterLoadBalancerProfileResponseManagedOutboundIPs(dict):
    """
    Desired managed outbound IPs for the cluster load balancer.
    """

    def __init__(__self__, *, count: Optional[int]=None):
        """
        Desired managed outbound IPs for the cluster load balancer.
        :param int count: The desired number of outbound IPs created/managed by Azure for the cluster load balancer. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        """
        if count is None:
            count = 1
        if count is not None:
            pulumi.set(__self__, 'count', count)

    @property
    @pulumi.getter
    def count(self) -> Optional[int]:
        """
        The desired number of outbound IPs created/managed by Azure for the cluster load balancer. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        """
        return pulumi.get(self, 'count')

@pulumi.output_type
class ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes(dict):
    """
    Desired outbound IP Prefix resources for the cluster load balancer.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publicIPPrefixes':
            suggest = 'public_ip_prefixes'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterLoadBalancerProfileResponseOutboundIPPrefixes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, public_ip_prefixes: Optional[Sequence['outputs.ResourceReferenceResponse']]=None):
        """
        Desired outbound IP Prefix resources for the cluster load balancer.
        :param Sequence['ResourceReferenceResponse'] public_ip_prefixes: A list of public IP prefix resources.
        """
        if public_ip_prefixes is not None:
            pulumi.set(__self__, 'public_ip_prefixes', public_ip_prefixes)

    @property
    @pulumi.getter(name='publicIPPrefixes')
    def public_ip_prefixes(self) -> Optional[Sequence['outputs.ResourceReferenceResponse']]:
        """
        A list of public IP prefix resources.
        """
        return pulumi.get(self, 'public_ip_prefixes')

@pulumi.output_type
class ManagedClusterLoadBalancerProfileResponseOutboundIPs(dict):
    """
    Desired outbound IP resources for the cluster load balancer.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publicIPs':
            suggest = 'public_ips'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterLoadBalancerProfileResponseOutboundIPs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterLoadBalancerProfileResponseOutboundIPs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterLoadBalancerProfileResponseOutboundIPs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, public_ips: Optional[Sequence['outputs.ResourceReferenceResponse']]=None):
        """
        Desired outbound IP resources for the cluster load balancer.
        :param Sequence['ResourceReferenceResponse'] public_ips: A list of public IP resources.
        """
        if public_ips is not None:
            pulumi.set(__self__, 'public_ips', public_ips)

    @property
    @pulumi.getter(name='publicIPs')
    def public_ips(self) -> Optional[Sequence['outputs.ResourceReferenceResponse']]:
        """
        A list of public IP resources.
        """
        return pulumi.get(self, 'public_ips')

@pulumi.output_type
class ManagedClusterPodIdentityExceptionResponse(dict):
    """
    See [disable AAD Pod Identity for a specific Pod/Application](https://azure.github.io/aad-pod-identity/docs/configure/application_exception/) for more details.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'podLabels':
            suggest = 'pod_labels'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterPodIdentityExceptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterPodIdentityExceptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterPodIdentityExceptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, name: str, namespace: str, pod_labels: Mapping[str, str]):
        """
        See [disable AAD Pod Identity for a specific Pod/Application](https://azure.github.io/aad-pod-identity/docs/configure/application_exception/) for more details.
        :param str name: The name of the pod identity exception.
        :param str namespace: The namespace of the pod identity exception.
        :param Mapping[str, str] pod_labels: The pod labels to match.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'namespace', namespace)
        pulumi.set(__self__, 'pod_labels', pod_labels)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the pod identity exception.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        The namespace of the pod identity exception.
        """
        return pulumi.get(self, 'namespace')

    @property
    @pulumi.getter(name='podLabels')
    def pod_labels(self) -> Mapping[str, str]:
        """
        The pod labels to match.
        """
        return pulumi.get(self, 'pod_labels')

@pulumi.output_type
class ManagedClusterPodIdentityProfileResponse(dict):
    """
    See [use AAD pod identity](https://docs.microsoft.com/azure/aks/use-azure-ad-pod-identity) for more details on pod identity integration.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'allowNetworkPluginKubenet':
            suggest = 'allow_network_plugin_kubenet'
        elif key == 'userAssignedIdentities':
            suggest = 'user_assigned_identities'
        elif key == 'userAssignedIdentityExceptions':
            suggest = 'user_assigned_identity_exceptions'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterPodIdentityProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterPodIdentityProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterPodIdentityProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, allow_network_plugin_kubenet: Optional[bool]=None, enabled: Optional[bool]=None, user_assigned_identities: Optional[Sequence['outputs.ManagedClusterPodIdentityResponse']]=None, user_assigned_identity_exceptions: Optional[Sequence['outputs.ManagedClusterPodIdentityExceptionResponse']]=None):
        """
        See [use AAD pod identity](https://docs.microsoft.com/azure/aks/use-azure-ad-pod-identity) for more details on pod identity integration.
        :param bool allow_network_plugin_kubenet: Running in Kubenet is disabled by default due to the security related nature of AAD Pod Identity and the risks of IP spoofing. See [using Kubenet network plugin with AAD Pod Identity](https://docs.microsoft.com/azure/aks/use-azure-ad-pod-identity#using-kubenet-network-plugin-with-azure-active-directory-pod-managed-identities) for more information.
        :param bool enabled: Whether the pod identity addon is enabled.
        :param Sequence['ManagedClusterPodIdentityResponse'] user_assigned_identities: The pod identities to use in the cluster.
        :param Sequence['ManagedClusterPodIdentityExceptionResponse'] user_assigned_identity_exceptions: The pod identity exceptions to allow.
        """
        if allow_network_plugin_kubenet is not None:
            pulumi.set(__self__, 'allow_network_plugin_kubenet', allow_network_plugin_kubenet)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if user_assigned_identities is not None:
            pulumi.set(__self__, 'user_assigned_identities', user_assigned_identities)
        if user_assigned_identity_exceptions is not None:
            pulumi.set(__self__, 'user_assigned_identity_exceptions', user_assigned_identity_exceptions)

    @property
    @pulumi.getter(name='allowNetworkPluginKubenet')
    def allow_network_plugin_kubenet(self) -> Optional[bool]:
        """
        Running in Kubenet is disabled by default due to the security related nature of AAD Pod Identity and the risks of IP spoofing. See [using Kubenet network plugin with AAD Pod Identity](https://docs.microsoft.com/azure/aks/use-azure-ad-pod-identity#using-kubenet-network-plugin-with-azure-active-directory-pod-managed-identities) for more information.
        """
        return pulumi.get(self, 'allow_network_plugin_kubenet')

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Whether the pod identity addon is enabled.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter(name='userAssignedIdentities')
    def user_assigned_identities(self) -> Optional[Sequence['outputs.ManagedClusterPodIdentityResponse']]:
        """
        The pod identities to use in the cluster.
        """
        return pulumi.get(self, 'user_assigned_identities')

    @property
    @pulumi.getter(name='userAssignedIdentityExceptions')
    def user_assigned_identity_exceptions(self) -> Optional[Sequence['outputs.ManagedClusterPodIdentityExceptionResponse']]:
        """
        The pod identity exceptions to allow.
        """
        return pulumi.get(self, 'user_assigned_identity_exceptions')

@pulumi.output_type
class ManagedClusterPodIdentityProvisioningErrorBodyResponse(dict):
    """
    An error response from the pod identity provisioning.
    """

    def __init__(__self__, *, code: Optional[str]=None, details: Optional[Sequence['outputs.ManagedClusterPodIdentityProvisioningErrorBodyResponse']]=None, message: Optional[str]=None, target: Optional[str]=None):
        """
        An error response from the pod identity provisioning.
        :param str code: An identifier for the error. Codes are invariant and are intended to be consumed programmatically.
        :param Sequence['ManagedClusterPodIdentityProvisioningErrorBodyResponse'] details: A list of additional details about the error.
        :param str message: A message describing the error, intended to be suitable for display in a user interface.
        :param str target: The target of the particular error. For example, the name of the property in error.
        """
        if code is not None:
            pulumi.set(__self__, 'code', code)
        if details is not None:
            pulumi.set(__self__, 'details', details)
        if message is not None:
            pulumi.set(__self__, 'message', message)
        if target is not None:
            pulumi.set(__self__, 'target', target)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        An identifier for the error. Codes are invariant and are intended to be consumed programmatically.
        """
        return pulumi.get(self, 'code')

    @property
    @pulumi.getter
    def details(self) -> Optional[Sequence['outputs.ManagedClusterPodIdentityProvisioningErrorBodyResponse']]:
        """
        A list of additional details about the error.
        """
        return pulumi.get(self, 'details')

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        A message describing the error, intended to be suitable for display in a user interface.
        """
        return pulumi.get(self, 'message')

    @property
    @pulumi.getter
    def target(self) -> Optional[str]:
        """
        The target of the particular error. For example, the name of the property in error.
        """
        return pulumi.get(self, 'target')

@pulumi.output_type
class ManagedClusterPodIdentityProvisioningErrorResponse(dict):
    """
    An error response from the pod identity provisioning.
    """

    def __init__(__self__, *, error: Optional['outputs.ManagedClusterPodIdentityProvisioningErrorBodyResponse']=None):
        """
        An error response from the pod identity provisioning.
        :param 'ManagedClusterPodIdentityProvisioningErrorBodyResponse' error: Details about the error.
        """
        if error is not None:
            pulumi.set(__self__, 'error', error)

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.ManagedClusterPodIdentityProvisioningErrorBodyResponse']:
        """
        Details about the error.
        """
        return pulumi.get(self, 'error')

@pulumi.output_type
class ManagedClusterPodIdentityResponse(dict):
    """
    Details about the pod identity assigned to the Managed Cluster.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'provisioningInfo':
            suggest = 'provisioning_info'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'bindingSelector':
            suggest = 'binding_selector'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterPodIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterPodIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterPodIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, identity: 'outputs.UserAssignedIdentityResponse', name: str, namespace: str, provisioning_info: 'outputs.ManagedClusterPodIdentityResponseProvisioningInfo', provisioning_state: str, binding_selector: Optional[str]=None):
        """
        Details about the pod identity assigned to the Managed Cluster.
        :param 'UserAssignedIdentityResponse' identity: The user assigned identity details.
        :param str name: The name of the pod identity.
        :param str namespace: The namespace of the pod identity.
        :param str provisioning_state: The current provisioning state of the pod identity.
        :param str binding_selector: The binding selector to use for the AzureIdentityBinding resource.
        """
        pulumi.set(__self__, 'identity', identity)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'namespace', namespace)
        pulumi.set(__self__, 'provisioning_info', provisioning_info)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if binding_selector is not None:
            pulumi.set(__self__, 'binding_selector', binding_selector)

    @property
    @pulumi.getter
    def identity(self) -> 'outputs.UserAssignedIdentityResponse':
        """
        The user assigned identity details.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the pod identity.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        The namespace of the pod identity.
        """
        return pulumi.get(self, 'namespace')

    @property
    @pulumi.getter(name='provisioningInfo')
    def provisioning_info(self) -> 'outputs.ManagedClusterPodIdentityResponseProvisioningInfo':
        return pulumi.get(self, 'provisioning_info')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The current provisioning state of the pod identity.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='bindingSelector')
    def binding_selector(self) -> Optional[str]:
        """
        The binding selector to use for the AzureIdentityBinding resource.
        """
        return pulumi.get(self, 'binding_selector')

@pulumi.output_type
class ManagedClusterPodIdentityResponseProvisioningInfo(dict):

    def __init__(__self__, *, error: Optional['outputs.ManagedClusterPodIdentityProvisioningErrorResponse']=None):
        """
        :param 'ManagedClusterPodIdentityProvisioningErrorResponse' error: Pod identity assignment error (if any).
        """
        if error is not None:
            pulumi.set(__self__, 'error', error)

    @property
    @pulumi.getter
    def error(self) -> Optional['outputs.ManagedClusterPodIdentityProvisioningErrorResponse']:
        """
        Pod identity assignment error (if any).
        """
        return pulumi.get(self, 'error')

@pulumi.output_type
class ManagedClusterPropertiesResponseAutoScalerProfile(dict):
    """
    Parameters to be applied to the cluster-autoscaler when enabled
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'balanceSimilarNodeGroups':
            suggest = 'balance_similar_node_groups'
        elif key == 'maxEmptyBulkDelete':
            suggest = 'max_empty_bulk_delete'
        elif key == 'maxGracefulTerminationSec':
            suggest = 'max_graceful_termination_sec'
        elif key == 'maxNodeProvisionTime':
            suggest = 'max_node_provision_time'
        elif key == 'maxTotalUnreadyPercentage':
            suggest = 'max_total_unready_percentage'
        elif key == 'newPodScaleUpDelay':
            suggest = 'new_pod_scale_up_delay'
        elif key == 'okTotalUnreadyCount':
            suggest = 'ok_total_unready_count'
        elif key == 'scaleDownDelayAfterAdd':
            suggest = 'scale_down_delay_after_add'
        elif key == 'scaleDownDelayAfterDelete':
            suggest = 'scale_down_delay_after_delete'
        elif key == 'scaleDownDelayAfterFailure':
            suggest = 'scale_down_delay_after_failure'
        elif key == 'scaleDownUnneededTime':
            suggest = 'scale_down_unneeded_time'
        elif key == 'scaleDownUnreadyTime':
            suggest = 'scale_down_unready_time'
        elif key == 'scaleDownUtilizationThreshold':
            suggest = 'scale_down_utilization_threshold'
        elif key == 'scanInterval':
            suggest = 'scan_interval'
        elif key == 'skipNodesWithLocalStorage':
            suggest = 'skip_nodes_with_local_storage'
        elif key == 'skipNodesWithSystemPods':
            suggest = 'skip_nodes_with_system_pods'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterPropertiesResponseAutoScalerProfile. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterPropertiesResponseAutoScalerProfile.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterPropertiesResponseAutoScalerProfile.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, balance_similar_node_groups: Optional[str]=None, expander: Optional[str]=None, max_empty_bulk_delete: Optional[str]=None, max_graceful_termination_sec: Optional[str]=None, max_node_provision_time: Optional[str]=None, max_total_unready_percentage: Optional[str]=None, new_pod_scale_up_delay: Optional[str]=None, ok_total_unready_count: Optional[str]=None, scale_down_delay_after_add: Optional[str]=None, scale_down_delay_after_delete: Optional[str]=None, scale_down_delay_after_failure: Optional[str]=None, scale_down_unneeded_time: Optional[str]=None, scale_down_unready_time: Optional[str]=None, scale_down_utilization_threshold: Optional[str]=None, scan_interval: Optional[str]=None, skip_nodes_with_local_storage: Optional[str]=None, skip_nodes_with_system_pods: Optional[str]=None):
        """
        Parameters to be applied to the cluster-autoscaler when enabled
        :param str balance_similar_node_groups: Valid values are 'true' and 'false'
        :param str expander: If not specified, the default is 'random'. See [expanders](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders) for more information.
        :param str max_empty_bulk_delete: The default is 10.
        :param str max_graceful_termination_sec: The default is 600.
        :param str max_node_provision_time: The default is '15m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str max_total_unready_percentage: The default is 45. The maximum is 100 and the minimum is 0.
        :param str new_pod_scale_up_delay: For scenarios like burst/batch scale where you don't want CA to act before the kubernetes scheduler could schedule all the pods, you can tell CA to ignore unscheduled pods before they're a certain age. The default is '0s'. Values must be an integer followed by a unit ('s' for seconds, 'm' for minutes, 'h' for hours, etc).
        :param str ok_total_unready_count: This must be an integer. The default is 3.
        :param str scale_down_delay_after_add: The default is '10m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str scale_down_delay_after_delete: The default is the scan-interval. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str scale_down_delay_after_failure: The default is '3m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str scale_down_unneeded_time: The default is '10m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str scale_down_unready_time: The default is '20m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        :param str scale_down_utilization_threshold: The default is '0.5'.
        :param str scan_interval: The default is '10'. Values must be an integer number of seconds.
        :param str skip_nodes_with_local_storage: The default is true.
        :param str skip_nodes_with_system_pods: The default is true.
        """
        if balance_similar_node_groups is not None:
            pulumi.set(__self__, 'balance_similar_node_groups', balance_similar_node_groups)
        if expander is not None:
            pulumi.set(__self__, 'expander', expander)
        if max_empty_bulk_delete is not None:
            pulumi.set(__self__, 'max_empty_bulk_delete', max_empty_bulk_delete)
        if max_graceful_termination_sec is not None:
            pulumi.set(__self__, 'max_graceful_termination_sec', max_graceful_termination_sec)
        if max_node_provision_time is not None:
            pulumi.set(__self__, 'max_node_provision_time', max_node_provision_time)
        if max_total_unready_percentage is not None:
            pulumi.set(__self__, 'max_total_unready_percentage', max_total_unready_percentage)
        if new_pod_scale_up_delay is not None:
            pulumi.set(__self__, 'new_pod_scale_up_delay', new_pod_scale_up_delay)
        if ok_total_unready_count is not None:
            pulumi.set(__self__, 'ok_total_unready_count', ok_total_unready_count)
        if scale_down_delay_after_add is not None:
            pulumi.set(__self__, 'scale_down_delay_after_add', scale_down_delay_after_add)
        if scale_down_delay_after_delete is not None:
            pulumi.set(__self__, 'scale_down_delay_after_delete', scale_down_delay_after_delete)
        if scale_down_delay_after_failure is not None:
            pulumi.set(__self__, 'scale_down_delay_after_failure', scale_down_delay_after_failure)
        if scale_down_unneeded_time is not None:
            pulumi.set(__self__, 'scale_down_unneeded_time', scale_down_unneeded_time)
        if scale_down_unready_time is not None:
            pulumi.set(__self__, 'scale_down_unready_time', scale_down_unready_time)
        if scale_down_utilization_threshold is not None:
            pulumi.set(__self__, 'scale_down_utilization_threshold', scale_down_utilization_threshold)
        if scan_interval is not None:
            pulumi.set(__self__, 'scan_interval', scan_interval)
        if skip_nodes_with_local_storage is not None:
            pulumi.set(__self__, 'skip_nodes_with_local_storage', skip_nodes_with_local_storage)
        if skip_nodes_with_system_pods is not None:
            pulumi.set(__self__, 'skip_nodes_with_system_pods', skip_nodes_with_system_pods)

    @property
    @pulumi.getter(name='balanceSimilarNodeGroups')
    def balance_similar_node_groups(self) -> Optional[str]:
        """
        Valid values are 'true' and 'false'
        """
        return pulumi.get(self, 'balance_similar_node_groups')

    @property
    @pulumi.getter
    def expander(self) -> Optional[str]:
        """
        If not specified, the default is 'random'. See [expanders](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders) for more information.
        """
        return pulumi.get(self, 'expander')

    @property
    @pulumi.getter(name='maxEmptyBulkDelete')
    def max_empty_bulk_delete(self) -> Optional[str]:
        """
        The default is 10.
        """
        return pulumi.get(self, 'max_empty_bulk_delete')

    @property
    @pulumi.getter(name='maxGracefulTerminationSec')
    def max_graceful_termination_sec(self) -> Optional[str]:
        """
        The default is 600.
        """
        return pulumi.get(self, 'max_graceful_termination_sec')

    @property
    @pulumi.getter(name='maxNodeProvisionTime')
    def max_node_provision_time(self) -> Optional[str]:
        """
        The default is '15m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'max_node_provision_time')

    @property
    @pulumi.getter(name='maxTotalUnreadyPercentage')
    def max_total_unready_percentage(self) -> Optional[str]:
        """
        The default is 45. The maximum is 100 and the minimum is 0.
        """
        return pulumi.get(self, 'max_total_unready_percentage')

    @property
    @pulumi.getter(name='newPodScaleUpDelay')
    def new_pod_scale_up_delay(self) -> Optional[str]:
        """
        For scenarios like burst/batch scale where you don't want CA to act before the kubernetes scheduler could schedule all the pods, you can tell CA to ignore unscheduled pods before they're a certain age. The default is '0s'. Values must be an integer followed by a unit ('s' for seconds, 'm' for minutes, 'h' for hours, etc).
        """
        return pulumi.get(self, 'new_pod_scale_up_delay')

    @property
    @pulumi.getter(name='okTotalUnreadyCount')
    def ok_total_unready_count(self) -> Optional[str]:
        """
        This must be an integer. The default is 3.
        """
        return pulumi.get(self, 'ok_total_unready_count')

    @property
    @pulumi.getter(name='scaleDownDelayAfterAdd')
    def scale_down_delay_after_add(self) -> Optional[str]:
        """
        The default is '10m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'scale_down_delay_after_add')

    @property
    @pulumi.getter(name='scaleDownDelayAfterDelete')
    def scale_down_delay_after_delete(self) -> Optional[str]:
        """
        The default is the scan-interval. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'scale_down_delay_after_delete')

    @property
    @pulumi.getter(name='scaleDownDelayAfterFailure')
    def scale_down_delay_after_failure(self) -> Optional[str]:
        """
        The default is '3m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'scale_down_delay_after_failure')

    @property
    @pulumi.getter(name='scaleDownUnneededTime')
    def scale_down_unneeded_time(self) -> Optional[str]:
        """
        The default is '10m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'scale_down_unneeded_time')

    @property
    @pulumi.getter(name='scaleDownUnreadyTime')
    def scale_down_unready_time(self) -> Optional[str]:
        """
        The default is '20m'. Values must be an integer followed by an 'm'. No unit of time other than minutes (m) is supported.
        """
        return pulumi.get(self, 'scale_down_unready_time')

    @property
    @pulumi.getter(name='scaleDownUtilizationThreshold')
    def scale_down_utilization_threshold(self) -> Optional[str]:
        """
        The default is '0.5'.
        """
        return pulumi.get(self, 'scale_down_utilization_threshold')

    @property
    @pulumi.getter(name='scanInterval')
    def scan_interval(self) -> Optional[str]:
        """
        The default is '10'. Values must be an integer number of seconds.
        """
        return pulumi.get(self, 'scan_interval')

    @property
    @pulumi.getter(name='skipNodesWithLocalStorage')
    def skip_nodes_with_local_storage(self) -> Optional[str]:
        """
        The default is true.
        """
        return pulumi.get(self, 'skip_nodes_with_local_storage')

    @property
    @pulumi.getter(name='skipNodesWithSystemPods')
    def skip_nodes_with_system_pods(self) -> Optional[str]:
        """
        The default is true.
        """
        return pulumi.get(self, 'skip_nodes_with_system_pods')

@pulumi.output_type
class ManagedClusterPropertiesResponseIdentityProfile(dict):

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'objectId':
            suggest = 'object_id'
        elif key == 'resourceId':
            suggest = 'resource_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterPropertiesResponseIdentityProfile. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterPropertiesResponseIdentityProfile.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterPropertiesResponseIdentityProfile.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: Optional[str]=None, object_id: Optional[str]=None, resource_id: Optional[str]=None):
        """
        :param str client_id: The client ID of the user assigned identity.
        :param str object_id: The object ID of the user assigned identity.
        :param str resource_id: The resource ID of the user assigned identity.
        """
        if client_id is not None:
            pulumi.set(__self__, 'client_id', client_id)
        if object_id is not None:
            pulumi.set(__self__, 'object_id', object_id)
        if resource_id is not None:
            pulumi.set(__self__, 'resource_id', resource_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> Optional[str]:
        """
        The client ID of the user assigned identity.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='objectId')
    def object_id(self) -> Optional[str]:
        """
        The object ID of the user assigned identity.
        """
        return pulumi.get(self, 'object_id')

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> Optional[str]:
        """
        The resource ID of the user assigned identity.
        """
        return pulumi.get(self, 'resource_id')

@pulumi.output_type
class ManagedClusterSKUResponse(dict):
    """
    The SKU of a Managed Cluster.
    """

    def __init__(__self__, *, name: Optional[str]=None, tier: Optional[str]=None):
        """
        The SKU of a Managed Cluster.
        :param str name: The name of a managed cluster SKU.
        :param str tier: If not specified, the default is 'Free'. See [uptime SLA](https://docs.microsoft.com/azure/aks/uptime-sla) for more details.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if tier is not None:
            pulumi.set(__self__, 'tier', tier)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of a managed cluster SKU.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        If not specified, the default is 'Free'. See [uptime SLA](https://docs.microsoft.com/azure/aks/uptime-sla) for more details.
        """
        return pulumi.get(self, 'tier')

@pulumi.output_type
class ManagedClusterServicePrincipalProfileResponse(dict):
    """
    Information about a service principal identity for the cluster to use for manipulating Azure APIs.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterServicePrincipalProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterServicePrincipalProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterServicePrincipalProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: str, secret: Optional[str]=None):
        """
        Information about a service principal identity for the cluster to use for manipulating Azure APIs.
        :param str client_id: The ID for the service principal.
        :param str secret: The secret password associated with the service principal in plain text.
        """
        pulumi.set(__self__, 'client_id', client_id)
        if secret is not None:
            pulumi.set(__self__, 'secret', secret)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> str:
        """
        The ID for the service principal.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter
    def secret(self) -> Optional[str]:
        """
        The secret password associated with the service principal in plain text.
        """
        return pulumi.get(self, 'secret')

@pulumi.output_type
class ManagedClusterWindowsProfileResponse(dict):
    """
    Profile for Windows VMs in the managed cluster.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'adminUsername':
            suggest = 'admin_username'
        elif key == 'adminPassword':
            suggest = 'admin_password'
        elif key == 'enableCSIProxy':
            suggest = 'enable_csi_proxy'
        elif key == 'licenseType':
            suggest = 'license_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterWindowsProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterWindowsProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedClusterWindowsProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, admin_username: str, admin_password: Optional[str]=None, enable_csi_proxy: Optional[bool]=None, license_type: Optional[str]=None):
        """
        Profile for Windows VMs in the managed cluster.
        :param str admin_username: Specifies the name of the administrator account. <br><br> **Restriction:** Cannot end in "." <br><br> **Disallowed values:** "administrator", "admin", "user", "user1", "test", "user2", "test1", "user3", "admin1", "1", "123", "a", "actuser", "adm", "admin2", "aspnet", "backup", "console", "david", "guest", "john", "owner", "root", "server", "sql", "support", "support_388945a0", "sys", "test2", "test3", "user4", "user5". <br><br> **Minimum-length:** 1 character <br><br> **Max-length:** 20 characters
        :param str admin_password: Specifies the password of the administrator account. <br><br> **Minimum-length:** 8 characters <br><br> **Max-length:** 123 characters <br><br> **Complexity requirements:** 3 out of 4 conditions below need to be fulfilled <br> Has lower characters <br>Has upper characters <br> Has a digit <br> Has a special character (Regex match [\\W_]) <br><br> **Disallowed values:** "abc@123", "P@$$w0rd", "P@ssw0rd", "P@ssword123", "Pa$$word", "pass@word1", "Password!", "Password1", "Password22", "iloveyou!"
        :param bool enable_csi_proxy: For more details on CSI proxy, see the [CSI proxy GitHub repo](https://github.com/kubernetes-csi/csi-proxy).
        :param str license_type: The license type to use for Windows VMs. See [Azure Hybrid User Benefits](https://azure.microsoft.com/pricing/hybrid-benefit/faq/) for more details.
        """
        pulumi.set(__self__, 'admin_username', admin_username)
        if admin_password is not None:
            pulumi.set(__self__, 'admin_password', admin_password)
        if enable_csi_proxy is not None:
            pulumi.set(__self__, 'enable_csi_proxy', enable_csi_proxy)
        if license_type is not None:
            pulumi.set(__self__, 'license_type', license_type)

    @property
    @pulumi.getter(name='adminUsername')
    def admin_username(self) -> str:
        """
        Specifies the name of the administrator account. <br><br> **Restriction:** Cannot end in "." <br><br> **Disallowed values:** "administrator", "admin", "user", "user1", "test", "user2", "test1", "user3", "admin1", "1", "123", "a", "actuser", "adm", "admin2", "aspnet", "backup", "console", "david", "guest", "john", "owner", "root", "server", "sql", "support", "support_388945a0", "sys", "test2", "test3", "user4", "user5". <br><br> **Minimum-length:** 1 character <br><br> **Max-length:** 20 characters
        """
        return pulumi.get(self, 'admin_username')

    @property
    @pulumi.getter(name='adminPassword')
    def admin_password(self) -> Optional[str]:
        """
        Specifies the password of the administrator account. <br><br> **Minimum-length:** 8 characters <br><br> **Max-length:** 123 characters <br><br> **Complexity requirements:** 3 out of 4 conditions below need to be fulfilled <br> Has lower characters <br>Has upper characters <br> Has a digit <br> Has a special character (Regex match [\\W_]) <br><br> **Disallowed values:** "abc@123", "P@$$w0rd", "P@ssw0rd", "P@ssword123", "Pa$$word", "pass@word1", "Password!", "Password1", "Password22", "iloveyou!"
        """
        return pulumi.get(self, 'admin_password')

    @property
    @pulumi.getter(name='enableCSIProxy')
    def enable_csi_proxy(self) -> Optional[bool]:
        """
        For more details on CSI proxy, see the [CSI proxy GitHub repo](https://github.com/kubernetes-csi/csi-proxy).
        """
        return pulumi.get(self, 'enable_csi_proxy')

    @property
    @pulumi.getter(name='licenseType')
    def license_type(self) -> Optional[str]:
        """
        The license type to use for Windows VMs. See [Azure Hybrid User Benefits](https://azure.microsoft.com/pricing/hybrid-benefit/faq/) for more details.
        """
        return pulumi.get(self, 'license_type')

@pulumi.output_type
class PowerStateResponse(dict):
    """
    Describes the Power State of the cluster
    """

    def __init__(__self__, *, code: Optional[str]=None):
        """
        Describes the Power State of the cluster
        :param str code: Tells whether the cluster is Running or Stopped
        """
        if code is not None:
            pulumi.set(__self__, 'code', code)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        Tells whether the cluster is Running or Stopped
        """
        return pulumi.get(self, 'code')

@pulumi.output_type
class PrivateEndpointResponse(dict):
    """
    Private endpoint which a connection belongs to.
    """

    def __init__(__self__, *, id: Optional[str]=None):
        """
        Private endpoint which a connection belongs to.
        :param str id: The resource ID of the private endpoint
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The resource ID of the private endpoint
        """
        return pulumi.get(self, 'id')

@pulumi.output_type
class PrivateLinkResourceResponse(dict):
    """
    A private link resource
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'privateLinkServiceID':
            suggest = 'private_link_service_id'
        elif key == 'groupId':
            suggest = 'group_id'
        elif key == 'requiredMembers':
            suggest = 'required_members'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkResourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkResourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        PrivateLinkResourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, private_link_service_id: str, group_id: Optional[str]=None, id: Optional[str]=None, name: Optional[str]=None, required_members: Optional[Sequence[str]]=None, type: Optional[str]=None):
        """
        A private link resource
        :param str private_link_service_id: The private link service ID of the resource, this field is exposed only to NRP internally.
        :param str group_id: The group ID of the resource.
        :param str id: The ID of the private link resource.
        :param str name: The name of the private link resource.
        :param Sequence[str] required_members: The RequiredMembers of the resource
        :param str type: The resource type.
        """
        pulumi.set(__self__, 'private_link_service_id', private_link_service_id)
        if group_id is not None:
            pulumi.set(__self__, 'group_id', group_id)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if required_members is not None:
            pulumi.set(__self__, 'required_members', required_members)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='privateLinkServiceID')
    def private_link_service_id(self) -> str:
        """
        The private link service ID of the resource, this field is exposed only to NRP internally.
        """
        return pulumi.get(self, 'private_link_service_id')

    @property
    @pulumi.getter(name='groupId')
    def group_id(self) -> Optional[str]:
        """
        The group ID of the resource.
        """
        return pulumi.get(self, 'group_id')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the private link resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the private link resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='requiredMembers')
    def required_members(self) -> Optional[Sequence[str]]:
        """
        The RequiredMembers of the resource
        """
        return pulumi.get(self, 'required_members')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The resource type.
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class PrivateLinkServiceConnectionStateResponse(dict):
    """
    The state of a private link service connection.
    """

    def __init__(__self__, *, description: Optional[str]=None, status: Optional[str]=None):
        """
        The state of a private link service connection.
        :param str description: The private link service connection description.
        :param str status: The private link service connection status.
        """
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The private link service connection description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The private link service connection status.
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class ResourceReferenceResponse(dict):
    """
    A reference to an Azure resource.
    """

    def __init__(__self__, *, id: Optional[str]=None):
        """
        A reference to an Azure resource.
        :param str id: The fully qualified Azure resource id.
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The fully qualified Azure resource id.
        """
        return pulumi.get(self, 'id')

@pulumi.output_type
class SysctlConfigResponse(dict):
    """
    Sysctl settings for Linux agent nodes.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'fsAioMaxNr':
            suggest = 'fs_aio_max_nr'
        elif key == 'fsFileMax':
            suggest = 'fs_file_max'
        elif key == 'fsInotifyMaxUserWatches':
            suggest = 'fs_inotify_max_user_watches'
        elif key == 'fsNrOpen':
            suggest = 'fs_nr_open'
        elif key == 'kernelThreadsMax':
            suggest = 'kernel_threads_max'
        elif key == 'netCoreNetdevMaxBacklog':
            suggest = 'net_core_netdev_max_backlog'
        elif key == 'netCoreOptmemMax':
            suggest = 'net_core_optmem_max'
        elif key == 'netCoreRmemDefault':
            suggest = 'net_core_rmem_default'
        elif key == 'netCoreRmemMax':
            suggest = 'net_core_rmem_max'
        elif key == 'netCoreSomaxconn':
            suggest = 'net_core_somaxconn'
        elif key == 'netCoreWmemDefault':
            suggest = 'net_core_wmem_default'
        elif key == 'netCoreWmemMax':
            suggest = 'net_core_wmem_max'
        elif key == 'netIpv4IpLocalPortRange':
            suggest = 'net_ipv4_ip_local_port_range'
        elif key == 'netIpv4NeighDefaultGcThresh1':
            suggest = 'net_ipv4_neigh_default_gc_thresh1'
        elif key == 'netIpv4NeighDefaultGcThresh2':
            suggest = 'net_ipv4_neigh_default_gc_thresh2'
        elif key == 'netIpv4NeighDefaultGcThresh3':
            suggest = 'net_ipv4_neigh_default_gc_thresh3'
        elif key == 'netIpv4TcpFinTimeout':
            suggest = 'net_ipv4_tcp_fin_timeout'
        elif key == 'netIpv4TcpKeepaliveProbes':
            suggest = 'net_ipv4_tcp_keepalive_probes'
        elif key == 'netIpv4TcpKeepaliveTime':
            suggest = 'net_ipv4_tcp_keepalive_time'
        elif key == 'netIpv4TcpMaxSynBacklog':
            suggest = 'net_ipv4_tcp_max_syn_backlog'
        elif key == 'netIpv4TcpMaxTwBuckets':
            suggest = 'net_ipv4_tcp_max_tw_buckets'
        elif key == 'netIpv4TcpTwReuse':
            suggest = 'net_ipv4_tcp_tw_reuse'
        elif key == 'netIpv4TcpkeepaliveIntvl':
            suggest = 'net_ipv4_tcpkeepalive_intvl'
        elif key == 'netNetfilterNfConntrackBuckets':
            suggest = 'net_netfilter_nf_conntrack_buckets'
        elif key == 'netNetfilterNfConntrackMax':
            suggest = 'net_netfilter_nf_conntrack_max'
        elif key == 'vmMaxMapCount':
            suggest = 'vm_max_map_count'
        elif key == 'vmSwappiness':
            suggest = 'vm_swappiness'
        elif key == 'vmVfsCachePressure':
            suggest = 'vm_vfs_cache_pressure'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SysctlConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SysctlConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SysctlConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, fs_aio_max_nr: Optional[int]=None, fs_file_max: Optional[int]=None, fs_inotify_max_user_watches: Optional[int]=None, fs_nr_open: Optional[int]=None, kernel_threads_max: Optional[int]=None, net_core_netdev_max_backlog: Optional[int]=None, net_core_optmem_max: Optional[int]=None, net_core_rmem_default: Optional[int]=None, net_core_rmem_max: Optional[int]=None, net_core_somaxconn: Optional[int]=None, net_core_wmem_default: Optional[int]=None, net_core_wmem_max: Optional[int]=None, net_ipv4_ip_local_port_range: Optional[str]=None, net_ipv4_neigh_default_gc_thresh1: Optional[int]=None, net_ipv4_neigh_default_gc_thresh2: Optional[int]=None, net_ipv4_neigh_default_gc_thresh3: Optional[int]=None, net_ipv4_tcp_fin_timeout: Optional[int]=None, net_ipv4_tcp_keepalive_probes: Optional[int]=None, net_ipv4_tcp_keepalive_time: Optional[int]=None, net_ipv4_tcp_max_syn_backlog: Optional[int]=None, net_ipv4_tcp_max_tw_buckets: Optional[int]=None, net_ipv4_tcp_tw_reuse: Optional[bool]=None, net_ipv4_tcpkeepalive_intvl: Optional[int]=None, net_netfilter_nf_conntrack_buckets: Optional[int]=None, net_netfilter_nf_conntrack_max: Optional[int]=None, vm_max_map_count: Optional[int]=None, vm_swappiness: Optional[int]=None, vm_vfs_cache_pressure: Optional[int]=None):
        """
        Sysctl settings for Linux agent nodes.
        :param int fs_aio_max_nr: Sysctl setting fs.aio-max-nr.
        :param int fs_file_max: Sysctl setting fs.file-max.
        :param int fs_inotify_max_user_watches: Sysctl setting fs.inotify.max_user_watches.
        :param int fs_nr_open: Sysctl setting fs.nr_open.
        :param int kernel_threads_max: Sysctl setting kernel.threads-max.
        :param int net_core_netdev_max_backlog: Sysctl setting net.core.netdev_max_backlog.
        :param int net_core_optmem_max: Sysctl setting net.core.optmem_max.
        :param int net_core_rmem_default: Sysctl setting net.core.rmem_default.
        :param int net_core_rmem_max: Sysctl setting net.core.rmem_max.
        :param int net_core_somaxconn: Sysctl setting net.core.somaxconn.
        :param int net_core_wmem_default: Sysctl setting net.core.wmem_default.
        :param int net_core_wmem_max: Sysctl setting net.core.wmem_max.
        :param str net_ipv4_ip_local_port_range: Sysctl setting net.ipv4.ip_local_port_range.
        :param int net_ipv4_neigh_default_gc_thresh1: Sysctl setting net.ipv4.neigh.default.gc_thresh1.
        :param int net_ipv4_neigh_default_gc_thresh2: Sysctl setting net.ipv4.neigh.default.gc_thresh2.
        :param int net_ipv4_neigh_default_gc_thresh3: Sysctl setting net.ipv4.neigh.default.gc_thresh3.
        :param int net_ipv4_tcp_fin_timeout: Sysctl setting net.ipv4.tcp_fin_timeout.
        :param int net_ipv4_tcp_keepalive_probes: Sysctl setting net.ipv4.tcp_keepalive_probes.
        :param int net_ipv4_tcp_keepalive_time: Sysctl setting net.ipv4.tcp_keepalive_time.
        :param int net_ipv4_tcp_max_syn_backlog: Sysctl setting net.ipv4.tcp_max_syn_backlog.
        :param int net_ipv4_tcp_max_tw_buckets: Sysctl setting net.ipv4.tcp_max_tw_buckets.
        :param bool net_ipv4_tcp_tw_reuse: Sysctl setting net.ipv4.tcp_tw_reuse.
        :param int net_ipv4_tcpkeepalive_intvl: Sysctl setting net.ipv4.tcp_keepalive_intvl.
        :param int net_netfilter_nf_conntrack_buckets: Sysctl setting net.netfilter.nf_conntrack_buckets.
        :param int net_netfilter_nf_conntrack_max: Sysctl setting net.netfilter.nf_conntrack_max.
        :param int vm_max_map_count: Sysctl setting vm.max_map_count.
        :param int vm_swappiness: Sysctl setting vm.swappiness.
        :param int vm_vfs_cache_pressure: Sysctl setting vm.vfs_cache_pressure.
        """
        if fs_aio_max_nr is not None:
            pulumi.set(__self__, 'fs_aio_max_nr', fs_aio_max_nr)
        if fs_file_max is not None:
            pulumi.set(__self__, 'fs_file_max', fs_file_max)
        if fs_inotify_max_user_watches is not None:
            pulumi.set(__self__, 'fs_inotify_max_user_watches', fs_inotify_max_user_watches)
        if fs_nr_open is not None:
            pulumi.set(__self__, 'fs_nr_open', fs_nr_open)
        if kernel_threads_max is not None:
            pulumi.set(__self__, 'kernel_threads_max', kernel_threads_max)
        if net_core_netdev_max_backlog is not None:
            pulumi.set(__self__, 'net_core_netdev_max_backlog', net_core_netdev_max_backlog)
        if net_core_optmem_max is not None:
            pulumi.set(__self__, 'net_core_optmem_max', net_core_optmem_max)
        if net_core_rmem_default is not None:
            pulumi.set(__self__, 'net_core_rmem_default', net_core_rmem_default)
        if net_core_rmem_max is not None:
            pulumi.set(__self__, 'net_core_rmem_max', net_core_rmem_max)
        if net_core_somaxconn is not None:
            pulumi.set(__self__, 'net_core_somaxconn', net_core_somaxconn)
        if net_core_wmem_default is not None:
            pulumi.set(__self__, 'net_core_wmem_default', net_core_wmem_default)
        if net_core_wmem_max is not None:
            pulumi.set(__self__, 'net_core_wmem_max', net_core_wmem_max)
        if net_ipv4_ip_local_port_range is not None:
            pulumi.set(__self__, 'net_ipv4_ip_local_port_range', net_ipv4_ip_local_port_range)
        if net_ipv4_neigh_default_gc_thresh1 is not None:
            pulumi.set(__self__, 'net_ipv4_neigh_default_gc_thresh1', net_ipv4_neigh_default_gc_thresh1)
        if net_ipv4_neigh_default_gc_thresh2 is not None:
            pulumi.set(__self__, 'net_ipv4_neigh_default_gc_thresh2', net_ipv4_neigh_default_gc_thresh2)
        if net_ipv4_neigh_default_gc_thresh3 is not None:
            pulumi.set(__self__, 'net_ipv4_neigh_default_gc_thresh3', net_ipv4_neigh_default_gc_thresh3)
        if net_ipv4_tcp_fin_timeout is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_fin_timeout', net_ipv4_tcp_fin_timeout)
        if net_ipv4_tcp_keepalive_probes is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_keepalive_probes', net_ipv4_tcp_keepalive_probes)
        if net_ipv4_tcp_keepalive_time is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_keepalive_time', net_ipv4_tcp_keepalive_time)
        if net_ipv4_tcp_max_syn_backlog is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_max_syn_backlog', net_ipv4_tcp_max_syn_backlog)
        if net_ipv4_tcp_max_tw_buckets is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_max_tw_buckets', net_ipv4_tcp_max_tw_buckets)
        if net_ipv4_tcp_tw_reuse is not None:
            pulumi.set(__self__, 'net_ipv4_tcp_tw_reuse', net_ipv4_tcp_tw_reuse)
        if net_ipv4_tcpkeepalive_intvl is not None:
            pulumi.set(__self__, 'net_ipv4_tcpkeepalive_intvl', net_ipv4_tcpkeepalive_intvl)
        if net_netfilter_nf_conntrack_buckets is not None:
            pulumi.set(__self__, 'net_netfilter_nf_conntrack_buckets', net_netfilter_nf_conntrack_buckets)
        if net_netfilter_nf_conntrack_max is not None:
            pulumi.set(__self__, 'net_netfilter_nf_conntrack_max', net_netfilter_nf_conntrack_max)
        if vm_max_map_count is not None:
            pulumi.set(__self__, 'vm_max_map_count', vm_max_map_count)
        if vm_swappiness is not None:
            pulumi.set(__self__, 'vm_swappiness', vm_swappiness)
        if vm_vfs_cache_pressure is not None:
            pulumi.set(__self__, 'vm_vfs_cache_pressure', vm_vfs_cache_pressure)

    @property
    @pulumi.getter(name='fsAioMaxNr')
    def fs_aio_max_nr(self) -> Optional[int]:
        """
        Sysctl setting fs.aio-max-nr.
        """
        return pulumi.get(self, 'fs_aio_max_nr')

    @property
    @pulumi.getter(name='fsFileMax')
    def fs_file_max(self) -> Optional[int]:
        """
        Sysctl setting fs.file-max.
        """
        return pulumi.get(self, 'fs_file_max')

    @property
    @pulumi.getter(name='fsInotifyMaxUserWatches')
    def fs_inotify_max_user_watches(self) -> Optional[int]:
        """
        Sysctl setting fs.inotify.max_user_watches.
        """
        return pulumi.get(self, 'fs_inotify_max_user_watches')

    @property
    @pulumi.getter(name='fsNrOpen')
    def fs_nr_open(self) -> Optional[int]:
        """
        Sysctl setting fs.nr_open.
        """
        return pulumi.get(self, 'fs_nr_open')

    @property
    @pulumi.getter(name='kernelThreadsMax')
    def kernel_threads_max(self) -> Optional[int]:
        """
        Sysctl setting kernel.threads-max.
        """
        return pulumi.get(self, 'kernel_threads_max')

    @property
    @pulumi.getter(name='netCoreNetdevMaxBacklog')
    def net_core_netdev_max_backlog(self) -> Optional[int]:
        """
        Sysctl setting net.core.netdev_max_backlog.
        """
        return pulumi.get(self, 'net_core_netdev_max_backlog')

    @property
    @pulumi.getter(name='netCoreOptmemMax')
    def net_core_optmem_max(self) -> Optional[int]:
        """
        Sysctl setting net.core.optmem_max.
        """
        return pulumi.get(self, 'net_core_optmem_max')

    @property
    @pulumi.getter(name='netCoreRmemDefault')
    def net_core_rmem_default(self) -> Optional[int]:
        """
        Sysctl setting net.core.rmem_default.
        """
        return pulumi.get(self, 'net_core_rmem_default')

    @property
    @pulumi.getter(name='netCoreRmemMax')
    def net_core_rmem_max(self) -> Optional[int]:
        """
        Sysctl setting net.core.rmem_max.
        """
        return pulumi.get(self, 'net_core_rmem_max')

    @property
    @pulumi.getter(name='netCoreSomaxconn')
    def net_core_somaxconn(self) -> Optional[int]:
        """
        Sysctl setting net.core.somaxconn.
        """
        return pulumi.get(self, 'net_core_somaxconn')

    @property
    @pulumi.getter(name='netCoreWmemDefault')
    def net_core_wmem_default(self) -> Optional[int]:
        """
        Sysctl setting net.core.wmem_default.
        """
        return pulumi.get(self, 'net_core_wmem_default')

    @property
    @pulumi.getter(name='netCoreWmemMax')
    def net_core_wmem_max(self) -> Optional[int]:
        """
        Sysctl setting net.core.wmem_max.
        """
        return pulumi.get(self, 'net_core_wmem_max')

    @property
    @pulumi.getter(name='netIpv4IpLocalPortRange')
    def net_ipv4_ip_local_port_range(self) -> Optional[str]:
        """
        Sysctl setting net.ipv4.ip_local_port_range.
        """
        return pulumi.get(self, 'net_ipv4_ip_local_port_range')

    @property
    @pulumi.getter(name='netIpv4NeighDefaultGcThresh1')
    def net_ipv4_neigh_default_gc_thresh1(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.neigh.default.gc_thresh1.
        """
        return pulumi.get(self, 'net_ipv4_neigh_default_gc_thresh1')

    @property
    @pulumi.getter(name='netIpv4NeighDefaultGcThresh2')
    def net_ipv4_neigh_default_gc_thresh2(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.neigh.default.gc_thresh2.
        """
        return pulumi.get(self, 'net_ipv4_neigh_default_gc_thresh2')

    @property
    @pulumi.getter(name='netIpv4NeighDefaultGcThresh3')
    def net_ipv4_neigh_default_gc_thresh3(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.neigh.default.gc_thresh3.
        """
        return pulumi.get(self, 'net_ipv4_neigh_default_gc_thresh3')

    @property
    @pulumi.getter(name='netIpv4TcpFinTimeout')
    def net_ipv4_tcp_fin_timeout(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_fin_timeout.
        """
        return pulumi.get(self, 'net_ipv4_tcp_fin_timeout')

    @property
    @pulumi.getter(name='netIpv4TcpKeepaliveProbes')
    def net_ipv4_tcp_keepalive_probes(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_keepalive_probes.
        """
        return pulumi.get(self, 'net_ipv4_tcp_keepalive_probes')

    @property
    @pulumi.getter(name='netIpv4TcpKeepaliveTime')
    def net_ipv4_tcp_keepalive_time(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_keepalive_time.
        """
        return pulumi.get(self, 'net_ipv4_tcp_keepalive_time')

    @property
    @pulumi.getter(name='netIpv4TcpMaxSynBacklog')
    def net_ipv4_tcp_max_syn_backlog(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_max_syn_backlog.
        """
        return pulumi.get(self, 'net_ipv4_tcp_max_syn_backlog')

    @property
    @pulumi.getter(name='netIpv4TcpMaxTwBuckets')
    def net_ipv4_tcp_max_tw_buckets(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_max_tw_buckets.
        """
        return pulumi.get(self, 'net_ipv4_tcp_max_tw_buckets')

    @property
    @pulumi.getter(name='netIpv4TcpTwReuse')
    def net_ipv4_tcp_tw_reuse(self) -> Optional[bool]:
        """
        Sysctl setting net.ipv4.tcp_tw_reuse.
        """
        return pulumi.get(self, 'net_ipv4_tcp_tw_reuse')

    @property
    @pulumi.getter(name='netIpv4TcpkeepaliveIntvl')
    def net_ipv4_tcpkeepalive_intvl(self) -> Optional[int]:
        """
        Sysctl setting net.ipv4.tcp_keepalive_intvl.
        """
        return pulumi.get(self, 'net_ipv4_tcpkeepalive_intvl')

    @property
    @pulumi.getter(name='netNetfilterNfConntrackBuckets')
    def net_netfilter_nf_conntrack_buckets(self) -> Optional[int]:
        """
        Sysctl setting net.netfilter.nf_conntrack_buckets.
        """
        return pulumi.get(self, 'net_netfilter_nf_conntrack_buckets')

    @property
    @pulumi.getter(name='netNetfilterNfConntrackMax')
    def net_netfilter_nf_conntrack_max(self) -> Optional[int]:
        """
        Sysctl setting net.netfilter.nf_conntrack_max.
        """
        return pulumi.get(self, 'net_netfilter_nf_conntrack_max')

    @property
    @pulumi.getter(name='vmMaxMapCount')
    def vm_max_map_count(self) -> Optional[int]:
        """
        Sysctl setting vm.max_map_count.
        """
        return pulumi.get(self, 'vm_max_map_count')

    @property
    @pulumi.getter(name='vmSwappiness')
    def vm_swappiness(self) -> Optional[int]:
        """
        Sysctl setting vm.swappiness.
        """
        return pulumi.get(self, 'vm_swappiness')

    @property
    @pulumi.getter(name='vmVfsCachePressure')
    def vm_vfs_cache_pressure(self) -> Optional[int]:
        """
        Sysctl setting vm.vfs_cache_pressure.
        """
        return pulumi.get(self, 'vm_vfs_cache_pressure')

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
        :param str created_at: The UTC timestamp of resource creation.
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The type of identity that last modified the resource.
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
        The UTC timestamp of resource creation.
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
        The type of identity that last modified the resource.
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
class TimeInWeekResponse(dict):
    """
    Time in a week.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'hourSlots':
            suggest = 'hour_slots'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TimeInWeekResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TimeInWeekResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        TimeInWeekResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, day: Optional[str]=None, hour_slots: Optional[Sequence[int]]=None):
        """
        Time in a week.
        :param str day: The day of the week.
        :param Sequence[int] hour_slots: Each integer hour represents a time range beginning at 0m after the hour ending at the next hour (non-inclusive). 0 corresponds to 00:00 UTC, 23 corresponds to 23:00 UTC. Specifying [0, 1] means the 00:00 - 02:00 UTC time range.
        """
        if day is not None:
            pulumi.set(__self__, 'day', day)
        if hour_slots is not None:
            pulumi.set(__self__, 'hour_slots', hour_slots)

    @property
    @pulumi.getter
    def day(self) -> Optional[str]:
        """
        The day of the week.
        """
        return pulumi.get(self, 'day')

    @property
    @pulumi.getter(name='hourSlots')
    def hour_slots(self) -> Optional[Sequence[int]]:
        """
        Each integer hour represents a time range beginning at 0m after the hour ending at the next hour (non-inclusive). 0 corresponds to 00:00 UTC, 23 corresponds to 23:00 UTC. Specifying [0, 1] means the 00:00 - 02:00 UTC time range.
        """
        return pulumi.get(self, 'hour_slots')

@pulumi.output_type
class TimeSpanResponse(dict):
    """
    For example, between 2021-05-25T13:00:00Z and 2021-05-25T14:00:00Z.
    """

    def __init__(__self__, *, end: Optional[str]=None, start: Optional[str]=None):
        """
        For example, between 2021-05-25T13:00:00Z and 2021-05-25T14:00:00Z.
        :param str end: The end of a time span
        :param str start: The start of a time span
        """
        if end is not None:
            pulumi.set(__self__, 'end', end)
        if start is not None:
            pulumi.set(__self__, 'start', start)

    @property
    @pulumi.getter
    def end(self) -> Optional[str]:
        """
        The end of a time span
        """
        return pulumi.get(self, 'end')

    @property
    @pulumi.getter
    def start(self) -> Optional[str]:
        """
        The start of a time span
        """
        return pulumi.get(self, 'start')

@pulumi.output_type
class UserAssignedIdentityResponse(dict):
    """
    Details about a user assigned identity.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'objectId':
            suggest = 'object_id'
        elif key == 'resourceId':
            suggest = 'resource_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UserAssignedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: Optional[str]=None, object_id: Optional[str]=None, resource_id: Optional[str]=None):
        """
        Details about a user assigned identity.
        :param str client_id: The client ID of the user assigned identity.
        :param str object_id: The object ID of the user assigned identity.
        :param str resource_id: The resource ID of the user assigned identity.
        """
        if client_id is not None:
            pulumi.set(__self__, 'client_id', client_id)
        if object_id is not None:
            pulumi.set(__self__, 'object_id', object_id)
        if resource_id is not None:
            pulumi.set(__self__, 'resource_id', resource_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> Optional[str]:
        """
        The client ID of the user assigned identity.
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='objectId')
    def object_id(self) -> Optional[str]:
        """
        The object ID of the user assigned identity.
        """
        return pulumi.get(self, 'object_id')

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> Optional[str]:
        """
        The resource ID of the user assigned identity.
        """
        return pulumi.get(self, 'resource_id')