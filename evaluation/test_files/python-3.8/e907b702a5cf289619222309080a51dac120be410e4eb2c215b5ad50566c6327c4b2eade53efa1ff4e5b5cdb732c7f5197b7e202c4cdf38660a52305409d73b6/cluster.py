import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ClusterArgs', 'Cluster']

@pulumi.input_type
class ClusterArgs:

    def __init__(__self__, *, addons_config: Optional[pulumi.Input['AddonsConfigArgs']]=None, authenticator_groups_config: Optional[pulumi.Input['AuthenticatorGroupsConfigArgs']]=None, autopilot: Optional[pulumi.Input['AutopilotArgs']]=None, autoscaling: Optional[pulumi.Input['ClusterAutoscalingArgs']]=None, binary_authorization: Optional[pulumi.Input['BinaryAuthorizationArgs']]=None, cluster_ipv4_cidr: Optional[pulumi.Input[str]]=None, cluster_telemetry: Optional[pulumi.Input['ClusterTelemetryArgs']]=None, conditions: Optional[pulumi.Input[Sequence[pulumi.Input['StatusConditionArgs']]]]=None, confidential_nodes: Optional[pulumi.Input['ConfidentialNodesArgs']]=None, cost_management_config: Optional[pulumi.Input['CostManagementConfigArgs']]=None, database_encryption: Optional[pulumi.Input['DatabaseEncryptionArgs']]=None, default_max_pods_constraint: Optional[pulumi.Input['MaxPodsConstraintArgs']]=None, description: Optional[pulumi.Input[str]]=None, enable_kubernetes_alpha: Optional[pulumi.Input[bool]]=None, enable_tpu: Optional[pulumi.Input[bool]]=None, identity_service_config: Optional[pulumi.Input['IdentityServiceConfigArgs']]=None, initial_cluster_version: Optional[pulumi.Input[str]]=None, initial_node_count: Optional[pulumi.Input[int]]=None, instance_group_urls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ip_allocation_policy: Optional[pulumi.Input['IPAllocationPolicyArgs']]=None, legacy_abac: Optional[pulumi.Input['LegacyAbacArgs']]=None, location: Optional[pulumi.Input[str]]=None, locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, logging_config: Optional[pulumi.Input['LoggingConfigArgs']]=None, logging_service: Optional[pulumi.Input[str]]=None, maintenance_policy: Optional[pulumi.Input['MaintenancePolicyArgs']]=None, master: Optional[pulumi.Input['MasterArgs']]=None, master_auth: Optional[pulumi.Input['MasterAuthArgs']]=None, master_authorized_networks_config: Optional[pulumi.Input['MasterAuthorizedNetworksConfigArgs']]=None, master_ipv4_cidr_block: Optional[pulumi.Input[str]]=None, mesh_certificates: Optional[pulumi.Input['MeshCertificatesArgs']]=None, monitoring_config: Optional[pulumi.Input['MonitoringConfigArgs']]=None, monitoring_service: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network: Optional[pulumi.Input[str]]=None, network_config: Optional[pulumi.Input['NetworkConfigArgs']]=None, network_policy: Optional[pulumi.Input['NetworkPolicyArgs']]=None, node_config: Optional[pulumi.Input['NodeConfigArgs']]=None, node_pool_auto_config: Optional[pulumi.Input['NodePoolAutoConfigArgs']]=None, node_pool_defaults: Optional[pulumi.Input['NodePoolDefaultsArgs']]=None, node_pools: Optional[pulumi.Input[Sequence[pulumi.Input['NodePoolArgs']]]]=None, notification_config: Optional[pulumi.Input['NotificationConfigArgs']]=None, parent: Optional[pulumi.Input[str]]=None, pod_security_policy_config: Optional[pulumi.Input['PodSecurityPolicyConfigArgs']]=None, private_cluster: Optional[pulumi.Input[bool]]=None, private_cluster_config: Optional[pulumi.Input['PrivateClusterConfigArgs']]=None, project: Optional[pulumi.Input[str]]=None, protect_config: Optional[pulumi.Input['ProtectConfigArgs']]=None, release_channel: Optional[pulumi.Input['ReleaseChannelArgs']]=None, resource_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, resource_usage_export_config: Optional[pulumi.Input['ResourceUsageExportConfigArgs']]=None, shielded_nodes: Optional[pulumi.Input['ShieldedNodesArgs']]=None, subnetwork: Optional[pulumi.Input[str]]=None, tpu_config: Optional[pulumi.Input['TpuConfigArgs']]=None, vertical_pod_autoscaling: Optional[pulumi.Input['VerticalPodAutoscalingArgs']]=None, workload_alts_config: Optional[pulumi.Input['WorkloadALTSConfigArgs']]=None, workload_certificates: Optional[pulumi.Input['WorkloadCertificatesArgs']]=None, workload_identity_config: Optional[pulumi.Input['WorkloadIdentityConfigArgs']]=None, zone: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Cluster resource.
        :param pulumi.Input['AddonsConfigArgs'] addons_config: Configurations for the various addons available to run in the cluster.
        :param pulumi.Input['AuthenticatorGroupsConfigArgs'] authenticator_groups_config: Configuration controlling RBAC group membership information.
        :param pulumi.Input['AutopilotArgs'] autopilot: Autopilot configuration for the cluster.
        :param pulumi.Input['ClusterAutoscalingArgs'] autoscaling: Cluster-level autoscaling configuration.
        :param pulumi.Input['BinaryAuthorizationArgs'] binary_authorization: Configuration for Binary Authorization.
        :param pulumi.Input[str] cluster_ipv4_cidr: The IP address range of the container pods in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `10.96.0.0/14`). Leave blank to have one automatically chosen or specify a `/14` block in `10.0.0.0/8`.
        :param pulumi.Input['ClusterTelemetryArgs'] cluster_telemetry: Telemetry integration for the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['StatusConditionArgs']]] conditions: Which conditions caused the current cluster state.
        :param pulumi.Input['ConfidentialNodesArgs'] confidential_nodes: Configuration of Confidential Nodes. All the nodes in the cluster will be Confidential VM once enabled.
        :param pulumi.Input['CostManagementConfigArgs'] cost_management_config: Configuration for the fine-grained cost management feature.
        :param pulumi.Input['DatabaseEncryptionArgs'] database_encryption: Configuration of etcd encryption.
        :param pulumi.Input['MaxPodsConstraintArgs'] default_max_pods_constraint: The default constraint on the maximum number of pods that can be run simultaneously on a node in the node pool of this cluster. Only honored if cluster created with IP Alias support.
        :param pulumi.Input[str] description: An optional description of this cluster.
        :param pulumi.Input[bool] enable_kubernetes_alpha: Kubernetes alpha features are enabled on this cluster. This includes alpha API groups (e.g. v1beta1) and features that may not be production ready in the kubernetes version of the master and nodes. The cluster has no SLA for uptime and master/node upgrades are disabled. Alpha enabled clusters are automatically deleted thirty days after creation.
        :param pulumi.Input[bool] enable_tpu: Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.
        :param pulumi.Input['IdentityServiceConfigArgs'] identity_service_config: Configuration for Identity Service component.
        :param pulumi.Input[str] initial_cluster_version: The initial Kubernetes version for this cluster. Valid versions are those found in validMasterVersions returned by getServerConfig. The version can be upgraded over time; such upgrades are reflected in currentMasterVersion and currentNodeVersion. Users may specify either explicit versions offered by Kubernetes Engine or version aliases, which have the following behavior: - "latest": picks the highest valid Kubernetes version - "1.X": picks the highest valid patch+gke.N patch in the 1.X version - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version - "1.X.Y-gke.N": picks an explicit Kubernetes version - "","-": picks the default Kubernetes version
        :param pulumi.Input[int] initial_node_count: The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_group_urls: Deprecated. Use node_pools.instance_group_urls.
        :param pulumi.Input['IPAllocationPolicyArgs'] ip_allocation_policy: Configuration for cluster IP allocation.
        :param pulumi.Input['LegacyAbacArgs'] legacy_abac: Configuration for the legacy ABAC authorization mode.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations: The list of Google Compute Engine [zones](https://cloud.google.com/compute/docs/zones#available) in which the cluster's nodes should be located. This field provides a default value if [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) are not specified during node pool creation. Warning: changing cluster locations will update the [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) of all node pools and will result in nodes being added and/or removed.
        :param pulumi.Input['LoggingConfigArgs'] logging_config: Logging configuration for the cluster.
        :param pulumi.Input[str] logging_service: The logging service the cluster should use to write logs. Currently available options: * `logging.googleapis.com/kubernetes` - The Cloud Logging service with a Kubernetes-native resource model * `logging.googleapis.com` - The legacy Cloud Logging service (no longer available as of GKE 1.15). * `none` - no logs will be exported from the cluster. If left as an empty string,`logging.googleapis.com/kubernetes` will be used for GKE 1.14+ or `logging.googleapis.com` for earlier versions.
        :param pulumi.Input['MaintenancePolicyArgs'] maintenance_policy: Configure the maintenance policy for this cluster.
        :param pulumi.Input['MasterArgs'] master: Configuration for master components.
        :param pulumi.Input['MasterAuthArgs'] master_auth: The authentication information for accessing the master endpoint. If unspecified, the defaults are used: For clusters before v1.12, if master_auth is unspecified, `username` will be set to "admin", a random password will be generated, and a client certificate will be issued.
        :param pulumi.Input['MasterAuthorizedNetworksConfigArgs'] master_authorized_networks_config: The configuration options for master authorized networks feature.
        :param pulumi.Input[str] master_ipv4_cidr_block: The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.
        :param pulumi.Input['MeshCertificatesArgs'] mesh_certificates: Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        :param pulumi.Input['MonitoringConfigArgs'] monitoring_config: Monitoring configuration for the cluster.
        :param pulumi.Input[str] monitoring_service: The monitoring service the cluster should use to write metrics. Currently available options: * "monitoring.googleapis.com/kubernetes" - The Cloud Monitoring service with a Kubernetes-native resource model * `monitoring.googleapis.com` - The legacy Cloud Monitoring service (no longer available as of GKE 1.15). * `none` - No metrics will be exported from the cluster. If left as an empty string,`monitoring.googleapis.com/kubernetes` will be used for GKE 1.14+ or `monitoring.googleapis.com` for earlier versions.
        :param pulumi.Input[str] name: The name of this cluster. The name must be unique within this project and location (e.g. zone or region), and can be up to 40 characters with the following restrictions: * Lowercase letters, numbers, and hyphens only. * Must start with a letter. * Must end with a number or a letter.
        :param pulumi.Input[str] network: The name of the Google Compute Engine [network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks) to which the cluster is connected. If left unspecified, the `default` network will be used. On output this shows the network ID instead of the name.
        :param pulumi.Input['NetworkConfigArgs'] network_config: Configuration for cluster networking.
        :param pulumi.Input['NetworkPolicyArgs'] network_policy: Configuration options for the NetworkPolicy feature.
        :param pulumi.Input['NodeConfigArgs'] node_config: Parameters used in creating the cluster's nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.
        :param pulumi.Input['NodePoolAutoConfigArgs'] node_pool_auto_config: Node pool configs that apply to all auto-provisioned node pools in autopilot clusters and node auto-provisioning enabled clusters.
        :param pulumi.Input['NodePoolDefaultsArgs'] node_pool_defaults: Default NodePool settings for the entire cluster. These settings are overridden if specified on the specific NodePool object.
        :param pulumi.Input[Sequence[pulumi.Input['NodePoolArgs']]] node_pools: The node pools associated with this cluster. This field should not be set if "node_config" or "initial_node_count" are specified.
        :param pulumi.Input['NotificationConfigArgs'] notification_config: Notification configuration of the cluster.
        :param pulumi.Input[str] parent: The parent (project and location) where the cluster will be created. Specified in the format `projects/*/locations/*`.
        :param pulumi.Input['PodSecurityPolicyConfigArgs'] pod_security_policy_config: Configuration for the PodSecurityPolicy feature.
        :param pulumi.Input[bool] private_cluster: If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.
        :param pulumi.Input['PrivateClusterConfigArgs'] private_cluster_config: Configuration for private cluster.
        :param pulumi.Input[str] project: Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.
        :param pulumi.Input['ProtectConfigArgs'] protect_config: Enable/Disable Protect API features for the cluster.
        :param pulumi.Input['ReleaseChannelArgs'] release_channel: Release channel configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_labels: The resource labels for the cluster to use to annotate any related Google Compute Engine resources.
        :param pulumi.Input['ResourceUsageExportConfigArgs'] resource_usage_export_config: Configuration for exporting resource usages. Resource usage export is disabled when this config unspecified.
        :param pulumi.Input['ShieldedNodesArgs'] shielded_nodes: Shielded Nodes configuration.
        :param pulumi.Input[str] subnetwork: The name of the Google Compute Engine [subnetwork](https://cloud.google.com/compute/docs/subnetworks) to which the cluster is connected. On output this shows the subnetwork ID instead of the name.
        :param pulumi.Input['TpuConfigArgs'] tpu_config: Configuration for Cloud TPU support;
        :param pulumi.Input['VerticalPodAutoscalingArgs'] vertical_pod_autoscaling: Cluster-level Vertical Pod Autoscaling configuration.
        :param pulumi.Input['WorkloadALTSConfigArgs'] workload_alts_config: Configuration for direct-path (via ALTS) with workload identity.
        :param pulumi.Input['WorkloadCertificatesArgs'] workload_certificates: Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        :param pulumi.Input['WorkloadIdentityConfigArgs'] workload_identity_config: Configuration for the use of Kubernetes Service Accounts in GCP IAM policies.
        :param pulumi.Input[str] zone: Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.
        """
        if addons_config is not None:
            pulumi.set(__self__, 'addons_config', addons_config)
        if authenticator_groups_config is not None:
            pulumi.set(__self__, 'authenticator_groups_config', authenticator_groups_config)
        if autopilot is not None:
            pulumi.set(__self__, 'autopilot', autopilot)
        if autoscaling is not None:
            pulumi.set(__self__, 'autoscaling', autoscaling)
        if binary_authorization is not None:
            pulumi.set(__self__, 'binary_authorization', binary_authorization)
        if cluster_ipv4_cidr is not None:
            pulumi.set(__self__, 'cluster_ipv4_cidr', cluster_ipv4_cidr)
        if cluster_telemetry is not None:
            pulumi.set(__self__, 'cluster_telemetry', cluster_telemetry)
        if conditions is not None:
            pulumi.set(__self__, 'conditions', conditions)
        if confidential_nodes is not None:
            pulumi.set(__self__, 'confidential_nodes', confidential_nodes)
        if cost_management_config is not None:
            pulumi.set(__self__, 'cost_management_config', cost_management_config)
        if database_encryption is not None:
            pulumi.set(__self__, 'database_encryption', database_encryption)
        if default_max_pods_constraint is not None:
            pulumi.set(__self__, 'default_max_pods_constraint', default_max_pods_constraint)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if enable_kubernetes_alpha is not None:
            pulumi.set(__self__, 'enable_kubernetes_alpha', enable_kubernetes_alpha)
        if enable_tpu is not None:
            warnings.warn('Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.', DeprecationWarning)
            pulumi.log.warn('enable_tpu is deprecated: Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.')
        if enable_tpu is not None:
            pulumi.set(__self__, 'enable_tpu', enable_tpu)
        if identity_service_config is not None:
            pulumi.set(__self__, 'identity_service_config', identity_service_config)
        if initial_cluster_version is not None:
            pulumi.set(__self__, 'initial_cluster_version', initial_cluster_version)
        if initial_node_count is not None:
            warnings.warn('The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.', DeprecationWarning)
            pulumi.log.warn('initial_node_count is deprecated: The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.')
        if initial_node_count is not None:
            pulumi.set(__self__, 'initial_node_count', initial_node_count)
        if instance_group_urls is not None:
            warnings.warn('Deprecated. Use node_pools.instance_group_urls.', DeprecationWarning)
            pulumi.log.warn('instance_group_urls is deprecated: Deprecated. Use node_pools.instance_group_urls.')
        if instance_group_urls is not None:
            pulumi.set(__self__, 'instance_group_urls', instance_group_urls)
        if ip_allocation_policy is not None:
            pulumi.set(__self__, 'ip_allocation_policy', ip_allocation_policy)
        if legacy_abac is not None:
            pulumi.set(__self__, 'legacy_abac', legacy_abac)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if locations is not None:
            pulumi.set(__self__, 'locations', locations)
        if logging_config is not None:
            pulumi.set(__self__, 'logging_config', logging_config)
        if logging_service is not None:
            pulumi.set(__self__, 'logging_service', logging_service)
        if maintenance_policy is not None:
            pulumi.set(__self__, 'maintenance_policy', maintenance_policy)
        if master is not None:
            pulumi.set(__self__, 'master', master)
        if master_auth is not None:
            pulumi.set(__self__, 'master_auth', master_auth)
        if master_authorized_networks_config is not None:
            pulumi.set(__self__, 'master_authorized_networks_config', master_authorized_networks_config)
        if master_ipv4_cidr_block is not None:
            warnings.warn('The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.', DeprecationWarning)
            pulumi.log.warn('master_ipv4_cidr_block is deprecated: The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.')
        if master_ipv4_cidr_block is not None:
            pulumi.set(__self__, 'master_ipv4_cidr_block', master_ipv4_cidr_block)
        if mesh_certificates is not None:
            pulumi.set(__self__, 'mesh_certificates', mesh_certificates)
        if monitoring_config is not None:
            pulumi.set(__self__, 'monitoring_config', monitoring_config)
        if monitoring_service is not None:
            pulumi.set(__self__, 'monitoring_service', monitoring_service)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if network is not None:
            pulumi.set(__self__, 'network', network)
        if network_config is not None:
            pulumi.set(__self__, 'network_config', network_config)
        if network_policy is not None:
            pulumi.set(__self__, 'network_policy', network_policy)
        if node_config is not None:
            warnings.warn('Parameters used in creating the cluster\'s nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.', DeprecationWarning)
            pulumi.log.warn('node_config is deprecated: Parameters used in creating the cluster\'s nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.')
        if node_config is not None:
            pulumi.set(__self__, 'node_config', node_config)
        if node_pool_auto_config is not None:
            pulumi.set(__self__, 'node_pool_auto_config', node_pool_auto_config)
        if node_pool_defaults is not None:
            pulumi.set(__self__, 'node_pool_defaults', node_pool_defaults)
        if node_pools is not None:
            pulumi.set(__self__, 'node_pools', node_pools)
        if notification_config is not None:
            pulumi.set(__self__, 'notification_config', notification_config)
        if parent is not None:
            pulumi.set(__self__, 'parent', parent)
        if pod_security_policy_config is not None:
            pulumi.set(__self__, 'pod_security_policy_config', pod_security_policy_config)
        if private_cluster is not None:
            warnings.warn('If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.', DeprecationWarning)
            pulumi.log.warn('private_cluster is deprecated: If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.')
        if private_cluster is not None:
            pulumi.set(__self__, 'private_cluster', private_cluster)
        if private_cluster_config is not None:
            pulumi.set(__self__, 'private_cluster_config', private_cluster_config)
        if project is not None:
            warnings.warn('Required. Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.', DeprecationWarning)
            pulumi.log.warn('project is deprecated: Required. Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.')
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if protect_config is not None:
            pulumi.set(__self__, 'protect_config', protect_config)
        if release_channel is not None:
            pulumi.set(__self__, 'release_channel', release_channel)
        if resource_labels is not None:
            pulumi.set(__self__, 'resource_labels', resource_labels)
        if resource_usage_export_config is not None:
            pulumi.set(__self__, 'resource_usage_export_config', resource_usage_export_config)
        if shielded_nodes is not None:
            pulumi.set(__self__, 'shielded_nodes', shielded_nodes)
        if subnetwork is not None:
            pulumi.set(__self__, 'subnetwork', subnetwork)
        if tpu_config is not None:
            pulumi.set(__self__, 'tpu_config', tpu_config)
        if vertical_pod_autoscaling is not None:
            pulumi.set(__self__, 'vertical_pod_autoscaling', vertical_pod_autoscaling)
        if workload_alts_config is not None:
            pulumi.set(__self__, 'workload_alts_config', workload_alts_config)
        if workload_certificates is not None:
            pulumi.set(__self__, 'workload_certificates', workload_certificates)
        if workload_identity_config is not None:
            pulumi.set(__self__, 'workload_identity_config', workload_identity_config)
        if zone is not None:
            warnings.warn('Required. Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.', DeprecationWarning)
            pulumi.log.warn('zone is deprecated: Required. Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.')
        if zone is not None:
            pulumi.set(__self__, 'zone', zone)

    @property
    @pulumi.getter(name='addonsConfig')
    def addons_config(self) -> Optional[pulumi.Input['AddonsConfigArgs']]:
        """
        Configurations for the various addons available to run in the cluster.
        """
        return pulumi.get(self, 'addons_config')

    @addons_config.setter
    def addons_config(self, value: Optional[pulumi.Input['AddonsConfigArgs']]):
        pulumi.set(self, 'addons_config', value)

    @property
    @pulumi.getter(name='authenticatorGroupsConfig')
    def authenticator_groups_config(self) -> Optional[pulumi.Input['AuthenticatorGroupsConfigArgs']]:
        """
        Configuration controlling RBAC group membership information.
        """
        return pulumi.get(self, 'authenticator_groups_config')

    @authenticator_groups_config.setter
    def authenticator_groups_config(self, value: Optional[pulumi.Input['AuthenticatorGroupsConfigArgs']]):
        pulumi.set(self, 'authenticator_groups_config', value)

    @property
    @pulumi.getter
    def autopilot(self) -> Optional[pulumi.Input['AutopilotArgs']]:
        """
        Autopilot configuration for the cluster.
        """
        return pulumi.get(self, 'autopilot')

    @autopilot.setter
    def autopilot(self, value: Optional[pulumi.Input['AutopilotArgs']]):
        pulumi.set(self, 'autopilot', value)

    @property
    @pulumi.getter
    def autoscaling(self) -> Optional[pulumi.Input['ClusterAutoscalingArgs']]:
        """
        Cluster-level autoscaling configuration.
        """
        return pulumi.get(self, 'autoscaling')

    @autoscaling.setter
    def autoscaling(self, value: Optional[pulumi.Input['ClusterAutoscalingArgs']]):
        pulumi.set(self, 'autoscaling', value)

    @property
    @pulumi.getter(name='binaryAuthorization')
    def binary_authorization(self) -> Optional[pulumi.Input['BinaryAuthorizationArgs']]:
        """
        Configuration for Binary Authorization.
        """
        return pulumi.get(self, 'binary_authorization')

    @binary_authorization.setter
    def binary_authorization(self, value: Optional[pulumi.Input['BinaryAuthorizationArgs']]):
        pulumi.set(self, 'binary_authorization', value)

    @property
    @pulumi.getter(name='clusterIpv4Cidr')
    def cluster_ipv4_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address range of the container pods in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `10.96.0.0/14`). Leave blank to have one automatically chosen or specify a `/14` block in `10.0.0.0/8`.
        """
        return pulumi.get(self, 'cluster_ipv4_cidr')

    @cluster_ipv4_cidr.setter
    def cluster_ipv4_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cluster_ipv4_cidr', value)

    @property
    @pulumi.getter(name='clusterTelemetry')
    def cluster_telemetry(self) -> Optional[pulumi.Input['ClusterTelemetryArgs']]:
        """
        Telemetry integration for the cluster.
        """
        return pulumi.get(self, 'cluster_telemetry')

    @cluster_telemetry.setter
    def cluster_telemetry(self, value: Optional[pulumi.Input['ClusterTelemetryArgs']]):
        pulumi.set(self, 'cluster_telemetry', value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StatusConditionArgs']]]]:
        """
        Which conditions caused the current cluster state.
        """
        return pulumi.get(self, 'conditions')

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StatusConditionArgs']]]]):
        pulumi.set(self, 'conditions', value)

    @property
    @pulumi.getter(name='confidentialNodes')
    def confidential_nodes(self) -> Optional[pulumi.Input['ConfidentialNodesArgs']]:
        """
        Configuration of Confidential Nodes. All the nodes in the cluster will be Confidential VM once enabled.
        """
        return pulumi.get(self, 'confidential_nodes')

    @confidential_nodes.setter
    def confidential_nodes(self, value: Optional[pulumi.Input['ConfidentialNodesArgs']]):
        pulumi.set(self, 'confidential_nodes', value)

    @property
    @pulumi.getter(name='costManagementConfig')
    def cost_management_config(self) -> Optional[pulumi.Input['CostManagementConfigArgs']]:
        """
        Configuration for the fine-grained cost management feature.
        """
        return pulumi.get(self, 'cost_management_config')

    @cost_management_config.setter
    def cost_management_config(self, value: Optional[pulumi.Input['CostManagementConfigArgs']]):
        pulumi.set(self, 'cost_management_config', value)

    @property
    @pulumi.getter(name='databaseEncryption')
    def database_encryption(self) -> Optional[pulumi.Input['DatabaseEncryptionArgs']]:
        """
        Configuration of etcd encryption.
        """
        return pulumi.get(self, 'database_encryption')

    @database_encryption.setter
    def database_encryption(self, value: Optional[pulumi.Input['DatabaseEncryptionArgs']]):
        pulumi.set(self, 'database_encryption', value)

    @property
    @pulumi.getter(name='defaultMaxPodsConstraint')
    def default_max_pods_constraint(self) -> Optional[pulumi.Input['MaxPodsConstraintArgs']]:
        """
        The default constraint on the maximum number of pods that can be run simultaneously on a node in the node pool of this cluster. Only honored if cluster created with IP Alias support.
        """
        return pulumi.get(self, 'default_max_pods_constraint')

    @default_max_pods_constraint.setter
    def default_max_pods_constraint(self, value: Optional[pulumi.Input['MaxPodsConstraintArgs']]):
        pulumi.set(self, 'default_max_pods_constraint', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this cluster.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='enableKubernetesAlpha')
    def enable_kubernetes_alpha(self) -> Optional[pulumi.Input[bool]]:
        """
        Kubernetes alpha features are enabled on this cluster. This includes alpha API groups (e.g. v1beta1) and features that may not be production ready in the kubernetes version of the master and nodes. The cluster has no SLA for uptime and master/node upgrades are disabled. Alpha enabled clusters are automatically deleted thirty days after creation.
        """
        return pulumi.get(self, 'enable_kubernetes_alpha')

    @enable_kubernetes_alpha.setter
    def enable_kubernetes_alpha(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_kubernetes_alpha', value)

    @property
    @pulumi.getter(name='enableTpu')
    def enable_tpu(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.
        """
        return pulumi.get(self, 'enable_tpu')

    @enable_tpu.setter
    def enable_tpu(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_tpu', value)

    @property
    @pulumi.getter(name='identityServiceConfig')
    def identity_service_config(self) -> Optional[pulumi.Input['IdentityServiceConfigArgs']]:
        """
        Configuration for Identity Service component.
        """
        return pulumi.get(self, 'identity_service_config')

    @identity_service_config.setter
    def identity_service_config(self, value: Optional[pulumi.Input['IdentityServiceConfigArgs']]):
        pulumi.set(self, 'identity_service_config', value)

    @property
    @pulumi.getter(name='initialClusterVersion')
    def initial_cluster_version(self) -> Optional[pulumi.Input[str]]:
        """
        The initial Kubernetes version for this cluster. Valid versions are those found in validMasterVersions returned by getServerConfig. The version can be upgraded over time; such upgrades are reflected in currentMasterVersion and currentNodeVersion. Users may specify either explicit versions offered by Kubernetes Engine or version aliases, which have the following behavior: - "latest": picks the highest valid Kubernetes version - "1.X": picks the highest valid patch+gke.N patch in the 1.X version - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version - "1.X.Y-gke.N": picks an explicit Kubernetes version - "","-": picks the default Kubernetes version
        """
        return pulumi.get(self, 'initial_cluster_version')

    @initial_cluster_version.setter
    def initial_cluster_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'initial_cluster_version', value)

    @property
    @pulumi.getter(name='initialNodeCount')
    def initial_node_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.
        """
        return pulumi.get(self, 'initial_node_count')

    @initial_node_count.setter
    def initial_node_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'initial_node_count', value)

    @property
    @pulumi.getter(name='instanceGroupUrls')
    def instance_group_urls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Deprecated. Use node_pools.instance_group_urls.
        """
        return pulumi.get(self, 'instance_group_urls')

    @instance_group_urls.setter
    def instance_group_urls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'instance_group_urls', value)

    @property
    @pulumi.getter(name='ipAllocationPolicy')
    def ip_allocation_policy(self) -> Optional[pulumi.Input['IPAllocationPolicyArgs']]:
        """
        Configuration for cluster IP allocation.
        """
        return pulumi.get(self, 'ip_allocation_policy')

    @ip_allocation_policy.setter
    def ip_allocation_policy(self, value: Optional[pulumi.Input['IPAllocationPolicyArgs']]):
        pulumi.set(self, 'ip_allocation_policy', value)

    @property
    @pulumi.getter(name='legacyAbac')
    def legacy_abac(self) -> Optional[pulumi.Input['LegacyAbacArgs']]:
        """
        Configuration for the legacy ABAC authorization mode.
        """
        return pulumi.get(self, 'legacy_abac')

    @legacy_abac.setter
    def legacy_abac(self, value: Optional[pulumi.Input['LegacyAbacArgs']]):
        pulumi.set(self, 'legacy_abac', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of Google Compute Engine [zones](https://cloud.google.com/compute/docs/zones#available) in which the cluster's nodes should be located. This field provides a default value if [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) are not specified during node pool creation. Warning: changing cluster locations will update the [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) of all node pools and will result in nodes being added and/or removed.
        """
        return pulumi.get(self, 'locations')

    @locations.setter
    def locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'locations', value)

    @property
    @pulumi.getter(name='loggingConfig')
    def logging_config(self) -> Optional[pulumi.Input['LoggingConfigArgs']]:
        """
        Logging configuration for the cluster.
        """
        return pulumi.get(self, 'logging_config')

    @logging_config.setter
    def logging_config(self, value: Optional[pulumi.Input['LoggingConfigArgs']]):
        pulumi.set(self, 'logging_config', value)

    @property
    @pulumi.getter(name='loggingService')
    def logging_service(self) -> Optional[pulumi.Input[str]]:
        """
        The logging service the cluster should use to write logs. Currently available options: * `logging.googleapis.com/kubernetes` - The Cloud Logging service with a Kubernetes-native resource model * `logging.googleapis.com` - The legacy Cloud Logging service (no longer available as of GKE 1.15). * `none` - no logs will be exported from the cluster. If left as an empty string,`logging.googleapis.com/kubernetes` will be used for GKE 1.14+ or `logging.googleapis.com` for earlier versions.
        """
        return pulumi.get(self, 'logging_service')

    @logging_service.setter
    def logging_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'logging_service', value)

    @property
    @pulumi.getter(name='maintenancePolicy')
    def maintenance_policy(self) -> Optional[pulumi.Input['MaintenancePolicyArgs']]:
        """
        Configure the maintenance policy for this cluster.
        """
        return pulumi.get(self, 'maintenance_policy')

    @maintenance_policy.setter
    def maintenance_policy(self, value: Optional[pulumi.Input['MaintenancePolicyArgs']]):
        pulumi.set(self, 'maintenance_policy', value)

    @property
    @pulumi.getter
    def master(self) -> Optional[pulumi.Input['MasterArgs']]:
        """
        Configuration for master components.
        """
        return pulumi.get(self, 'master')

    @master.setter
    def master(self, value: Optional[pulumi.Input['MasterArgs']]):
        pulumi.set(self, 'master', value)

    @property
    @pulumi.getter(name='masterAuth')
    def master_auth(self) -> Optional[pulumi.Input['MasterAuthArgs']]:
        """
        The authentication information for accessing the master endpoint. If unspecified, the defaults are used: For clusters before v1.12, if master_auth is unspecified, `username` will be set to "admin", a random password will be generated, and a client certificate will be issued.
        """
        return pulumi.get(self, 'master_auth')

    @master_auth.setter
    def master_auth(self, value: Optional[pulumi.Input['MasterAuthArgs']]):
        pulumi.set(self, 'master_auth', value)

    @property
    @pulumi.getter(name='masterAuthorizedNetworksConfig')
    def master_authorized_networks_config(self) -> Optional[pulumi.Input['MasterAuthorizedNetworksConfigArgs']]:
        """
        The configuration options for master authorized networks feature.
        """
        return pulumi.get(self, 'master_authorized_networks_config')

    @master_authorized_networks_config.setter
    def master_authorized_networks_config(self, value: Optional[pulumi.Input['MasterAuthorizedNetworksConfigArgs']]):
        pulumi.set(self, 'master_authorized_networks_config', value)

    @property
    @pulumi.getter(name='masterIpv4CidrBlock')
    def master_ipv4_cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.
        """
        return pulumi.get(self, 'master_ipv4_cidr_block')

    @master_ipv4_cidr_block.setter
    def master_ipv4_cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'master_ipv4_cidr_block', value)

    @property
    @pulumi.getter(name='meshCertificates')
    def mesh_certificates(self) -> Optional[pulumi.Input['MeshCertificatesArgs']]:
        """
        Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        """
        return pulumi.get(self, 'mesh_certificates')

    @mesh_certificates.setter
    def mesh_certificates(self, value: Optional[pulumi.Input['MeshCertificatesArgs']]):
        pulumi.set(self, 'mesh_certificates', value)

    @property
    @pulumi.getter(name='monitoringConfig')
    def monitoring_config(self) -> Optional[pulumi.Input['MonitoringConfigArgs']]:
        """
        Monitoring configuration for the cluster.
        """
        return pulumi.get(self, 'monitoring_config')

    @monitoring_config.setter
    def monitoring_config(self, value: Optional[pulumi.Input['MonitoringConfigArgs']]):
        pulumi.set(self, 'monitoring_config', value)

    @property
    @pulumi.getter(name='monitoringService')
    def monitoring_service(self) -> Optional[pulumi.Input[str]]:
        """
        The monitoring service the cluster should use to write metrics. Currently available options: * "monitoring.googleapis.com/kubernetes" - The Cloud Monitoring service with a Kubernetes-native resource model * `monitoring.googleapis.com` - The legacy Cloud Monitoring service (no longer available as of GKE 1.15). * `none` - No metrics will be exported from the cluster. If left as an empty string,`monitoring.googleapis.com/kubernetes` will be used for GKE 1.14+ or `monitoring.googleapis.com` for earlier versions.
        """
        return pulumi.get(self, 'monitoring_service')

    @monitoring_service.setter
    def monitoring_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'monitoring_service', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of this cluster. The name must be unique within this project and location (e.g. zone or region), and can be up to 40 characters with the following restrictions: * Lowercase letters, numbers, and hyphens only. * Must start with a letter. * Must end with a number or a letter.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Google Compute Engine [network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks) to which the cluster is connected. If left unspecified, the `default` network will be used. On output this shows the network ID instead of the name.
        """
        return pulumi.get(self, 'network')

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'network', value)

    @property
    @pulumi.getter(name='networkConfig')
    def network_config(self) -> Optional[pulumi.Input['NetworkConfigArgs']]:
        """
        Configuration for cluster networking.
        """
        return pulumi.get(self, 'network_config')

    @network_config.setter
    def network_config(self, value: Optional[pulumi.Input['NetworkConfigArgs']]):
        pulumi.set(self, 'network_config', value)

    @property
    @pulumi.getter(name='networkPolicy')
    def network_policy(self) -> Optional[pulumi.Input['NetworkPolicyArgs']]:
        """
        Configuration options for the NetworkPolicy feature.
        """
        return pulumi.get(self, 'network_policy')

    @network_policy.setter
    def network_policy(self, value: Optional[pulumi.Input['NetworkPolicyArgs']]):
        pulumi.set(self, 'network_policy', value)

    @property
    @pulumi.getter(name='nodeConfig')
    def node_config(self) -> Optional[pulumi.Input['NodeConfigArgs']]:
        """
        Parameters used in creating the cluster's nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.
        """
        return pulumi.get(self, 'node_config')

    @node_config.setter
    def node_config(self, value: Optional[pulumi.Input['NodeConfigArgs']]):
        pulumi.set(self, 'node_config', value)

    @property
    @pulumi.getter(name='nodePoolAutoConfig')
    def node_pool_auto_config(self) -> Optional[pulumi.Input['NodePoolAutoConfigArgs']]:
        """
        Node pool configs that apply to all auto-provisioned node pools in autopilot clusters and node auto-provisioning enabled clusters.
        """
        return pulumi.get(self, 'node_pool_auto_config')

    @node_pool_auto_config.setter
    def node_pool_auto_config(self, value: Optional[pulumi.Input['NodePoolAutoConfigArgs']]):
        pulumi.set(self, 'node_pool_auto_config', value)

    @property
    @pulumi.getter(name='nodePoolDefaults')
    def node_pool_defaults(self) -> Optional[pulumi.Input['NodePoolDefaultsArgs']]:
        """
        Default NodePool settings for the entire cluster. These settings are overridden if specified on the specific NodePool object.
        """
        return pulumi.get(self, 'node_pool_defaults')

    @node_pool_defaults.setter
    def node_pool_defaults(self, value: Optional[pulumi.Input['NodePoolDefaultsArgs']]):
        pulumi.set(self, 'node_pool_defaults', value)

    @property
    @pulumi.getter(name='nodePools')
    def node_pools(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NodePoolArgs']]]]:
        """
        The node pools associated with this cluster. This field should not be set if "node_config" or "initial_node_count" are specified.
        """
        return pulumi.get(self, 'node_pools')

    @node_pools.setter
    def node_pools(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NodePoolArgs']]]]):
        pulumi.set(self, 'node_pools', value)

    @property
    @pulumi.getter(name='notificationConfig')
    def notification_config(self) -> Optional[pulumi.Input['NotificationConfigArgs']]:
        """
        Notification configuration of the cluster.
        """
        return pulumi.get(self, 'notification_config')

    @notification_config.setter
    def notification_config(self, value: Optional[pulumi.Input['NotificationConfigArgs']]):
        pulumi.set(self, 'notification_config', value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The parent (project and location) where the cluster will be created. Specified in the format `projects/*/locations/*`.
        """
        return pulumi.get(self, 'parent')

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'parent', value)

    @property
    @pulumi.getter(name='podSecurityPolicyConfig')
    def pod_security_policy_config(self) -> Optional[pulumi.Input['PodSecurityPolicyConfigArgs']]:
        """
        Configuration for the PodSecurityPolicy feature.
        """
        return pulumi.get(self, 'pod_security_policy_config')

    @pod_security_policy_config.setter
    def pod_security_policy_config(self, value: Optional[pulumi.Input['PodSecurityPolicyConfigArgs']]):
        pulumi.set(self, 'pod_security_policy_config', value)

    @property
    @pulumi.getter(name='privateCluster')
    def private_cluster(self) -> Optional[pulumi.Input[bool]]:
        """
        If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.
        """
        return pulumi.get(self, 'private_cluster')

    @private_cluster.setter
    def private_cluster(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'private_cluster', value)

    @property
    @pulumi.getter(name='privateClusterConfig')
    def private_cluster_config(self) -> Optional[pulumi.Input['PrivateClusterConfigArgs']]:
        """
        Configuration for private cluster.
        """
        return pulumi.get(self, 'private_cluster_config')

    @private_cluster_config.setter
    def private_cluster_config(self, value: Optional[pulumi.Input['PrivateClusterConfigArgs']]):
        pulumi.set(self, 'private_cluster_config', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter(name='protectConfig')
    def protect_config(self) -> Optional[pulumi.Input['ProtectConfigArgs']]:
        """
        Enable/Disable Protect API features for the cluster.
        """
        return pulumi.get(self, 'protect_config')

    @protect_config.setter
    def protect_config(self, value: Optional[pulumi.Input['ProtectConfigArgs']]):
        pulumi.set(self, 'protect_config', value)

    @property
    @pulumi.getter(name='releaseChannel')
    def release_channel(self) -> Optional[pulumi.Input['ReleaseChannelArgs']]:
        """
        Release channel configuration.
        """
        return pulumi.get(self, 'release_channel')

    @release_channel.setter
    def release_channel(self, value: Optional[pulumi.Input['ReleaseChannelArgs']]):
        pulumi.set(self, 'release_channel', value)

    @property
    @pulumi.getter(name='resourceLabels')
    def resource_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource labels for the cluster to use to annotate any related Google Compute Engine resources.
        """
        return pulumi.get(self, 'resource_labels')

    @resource_labels.setter
    def resource_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'resource_labels', value)

    @property
    @pulumi.getter(name='resourceUsageExportConfig')
    def resource_usage_export_config(self) -> Optional[pulumi.Input['ResourceUsageExportConfigArgs']]:
        """
        Configuration for exporting resource usages. Resource usage export is disabled when this config unspecified.
        """
        return pulumi.get(self, 'resource_usage_export_config')

    @resource_usage_export_config.setter
    def resource_usage_export_config(self, value: Optional[pulumi.Input['ResourceUsageExportConfigArgs']]):
        pulumi.set(self, 'resource_usage_export_config', value)

    @property
    @pulumi.getter(name='shieldedNodes')
    def shielded_nodes(self) -> Optional[pulumi.Input['ShieldedNodesArgs']]:
        """
        Shielded Nodes configuration.
        """
        return pulumi.get(self, 'shielded_nodes')

    @shielded_nodes.setter
    def shielded_nodes(self, value: Optional[pulumi.Input['ShieldedNodesArgs']]):
        pulumi.set(self, 'shielded_nodes', value)

    @property
    @pulumi.getter
    def subnetwork(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Google Compute Engine [subnetwork](https://cloud.google.com/compute/docs/subnetworks) to which the cluster is connected. On output this shows the subnetwork ID instead of the name.
        """
        return pulumi.get(self, 'subnetwork')

    @subnetwork.setter
    def subnetwork(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnetwork', value)

    @property
    @pulumi.getter(name='tpuConfig')
    def tpu_config(self) -> Optional[pulumi.Input['TpuConfigArgs']]:
        """
        Configuration for Cloud TPU support;
        """
        return pulumi.get(self, 'tpu_config')

    @tpu_config.setter
    def tpu_config(self, value: Optional[pulumi.Input['TpuConfigArgs']]):
        pulumi.set(self, 'tpu_config', value)

    @property
    @pulumi.getter(name='verticalPodAutoscaling')
    def vertical_pod_autoscaling(self) -> Optional[pulumi.Input['VerticalPodAutoscalingArgs']]:
        """
        Cluster-level Vertical Pod Autoscaling configuration.
        """
        return pulumi.get(self, 'vertical_pod_autoscaling')

    @vertical_pod_autoscaling.setter
    def vertical_pod_autoscaling(self, value: Optional[pulumi.Input['VerticalPodAutoscalingArgs']]):
        pulumi.set(self, 'vertical_pod_autoscaling', value)

    @property
    @pulumi.getter(name='workloadAltsConfig')
    def workload_alts_config(self) -> Optional[pulumi.Input['WorkloadALTSConfigArgs']]:
        """
        Configuration for direct-path (via ALTS) with workload identity.
        """
        return pulumi.get(self, 'workload_alts_config')

    @workload_alts_config.setter
    def workload_alts_config(self, value: Optional[pulumi.Input['WorkloadALTSConfigArgs']]):
        pulumi.set(self, 'workload_alts_config', value)

    @property
    @pulumi.getter(name='workloadCertificates')
    def workload_certificates(self) -> Optional[pulumi.Input['WorkloadCertificatesArgs']]:
        """
        Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        """
        return pulumi.get(self, 'workload_certificates')

    @workload_certificates.setter
    def workload_certificates(self, value: Optional[pulumi.Input['WorkloadCertificatesArgs']]):
        pulumi.set(self, 'workload_certificates', value)

    @property
    @pulumi.getter(name='workloadIdentityConfig')
    def workload_identity_config(self) -> Optional[pulumi.Input['WorkloadIdentityConfigArgs']]:
        """
        Configuration for the use of Kubernetes Service Accounts in GCP IAM policies.
        """
        return pulumi.get(self, 'workload_identity_config')

    @workload_identity_config.setter
    def workload_identity_config(self, value: Optional[pulumi.Input['WorkloadIdentityConfigArgs']]):
        pulumi.set(self, 'workload_identity_config', value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.
        """
        return pulumi.get(self, 'zone')

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zone', value)

class Cluster(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, addons_config: Optional[pulumi.Input[pulumi.InputType['AddonsConfigArgs']]]=None, authenticator_groups_config: Optional[pulumi.Input[pulumi.InputType['AuthenticatorGroupsConfigArgs']]]=None, autopilot: Optional[pulumi.Input[pulumi.InputType['AutopilotArgs']]]=None, autoscaling: Optional[pulumi.Input[pulumi.InputType['ClusterAutoscalingArgs']]]=None, binary_authorization: Optional[pulumi.Input[pulumi.InputType['BinaryAuthorizationArgs']]]=None, cluster_ipv4_cidr: Optional[pulumi.Input[str]]=None, cluster_telemetry: Optional[pulumi.Input[pulumi.InputType['ClusterTelemetryArgs']]]=None, conditions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StatusConditionArgs']]]]]=None, confidential_nodes: Optional[pulumi.Input[pulumi.InputType['ConfidentialNodesArgs']]]=None, cost_management_config: Optional[pulumi.Input[pulumi.InputType['CostManagementConfigArgs']]]=None, database_encryption: Optional[pulumi.Input[pulumi.InputType['DatabaseEncryptionArgs']]]=None, default_max_pods_constraint: Optional[pulumi.Input[pulumi.InputType['MaxPodsConstraintArgs']]]=None, description: Optional[pulumi.Input[str]]=None, enable_kubernetes_alpha: Optional[pulumi.Input[bool]]=None, enable_tpu: Optional[pulumi.Input[bool]]=None, identity_service_config: Optional[pulumi.Input[pulumi.InputType['IdentityServiceConfigArgs']]]=None, initial_cluster_version: Optional[pulumi.Input[str]]=None, initial_node_count: Optional[pulumi.Input[int]]=None, instance_group_urls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ip_allocation_policy: Optional[pulumi.Input[pulumi.InputType['IPAllocationPolicyArgs']]]=None, legacy_abac: Optional[pulumi.Input[pulumi.InputType['LegacyAbacArgs']]]=None, location: Optional[pulumi.Input[str]]=None, locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, logging_config: Optional[pulumi.Input[pulumi.InputType['LoggingConfigArgs']]]=None, logging_service: Optional[pulumi.Input[str]]=None, maintenance_policy: Optional[pulumi.Input[pulumi.InputType['MaintenancePolicyArgs']]]=None, master: Optional[pulumi.Input[pulumi.InputType['MasterArgs']]]=None, master_auth: Optional[pulumi.Input[pulumi.InputType['MasterAuthArgs']]]=None, master_authorized_networks_config: Optional[pulumi.Input[pulumi.InputType['MasterAuthorizedNetworksConfigArgs']]]=None, master_ipv4_cidr_block: Optional[pulumi.Input[str]]=None, mesh_certificates: Optional[pulumi.Input[pulumi.InputType['MeshCertificatesArgs']]]=None, monitoring_config: Optional[pulumi.Input[pulumi.InputType['MonitoringConfigArgs']]]=None, monitoring_service: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network: Optional[pulumi.Input[str]]=None, network_config: Optional[pulumi.Input[pulumi.InputType['NetworkConfigArgs']]]=None, network_policy: Optional[pulumi.Input[pulumi.InputType['NetworkPolicyArgs']]]=None, node_config: Optional[pulumi.Input[pulumi.InputType['NodeConfigArgs']]]=None, node_pool_auto_config: Optional[pulumi.Input[pulumi.InputType['NodePoolAutoConfigArgs']]]=None, node_pool_defaults: Optional[pulumi.Input[pulumi.InputType['NodePoolDefaultsArgs']]]=None, node_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NodePoolArgs']]]]]=None, notification_config: Optional[pulumi.Input[pulumi.InputType['NotificationConfigArgs']]]=None, parent: Optional[pulumi.Input[str]]=None, pod_security_policy_config: Optional[pulumi.Input[pulumi.InputType['PodSecurityPolicyConfigArgs']]]=None, private_cluster: Optional[pulumi.Input[bool]]=None, private_cluster_config: Optional[pulumi.Input[pulumi.InputType['PrivateClusterConfigArgs']]]=None, project: Optional[pulumi.Input[str]]=None, protect_config: Optional[pulumi.Input[pulumi.InputType['ProtectConfigArgs']]]=None, release_channel: Optional[pulumi.Input[pulumi.InputType['ReleaseChannelArgs']]]=None, resource_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, resource_usage_export_config: Optional[pulumi.Input[pulumi.InputType['ResourceUsageExportConfigArgs']]]=None, shielded_nodes: Optional[pulumi.Input[pulumi.InputType['ShieldedNodesArgs']]]=None, subnetwork: Optional[pulumi.Input[str]]=None, tpu_config: Optional[pulumi.Input[pulumi.InputType['TpuConfigArgs']]]=None, vertical_pod_autoscaling: Optional[pulumi.Input[pulumi.InputType['VerticalPodAutoscalingArgs']]]=None, workload_alts_config: Optional[pulumi.Input[pulumi.InputType['WorkloadALTSConfigArgs']]]=None, workload_certificates: Optional[pulumi.Input[pulumi.InputType['WorkloadCertificatesArgs']]]=None, workload_identity_config: Optional[pulumi.Input[pulumi.InputType['WorkloadIdentityConfigArgs']]]=None, zone: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Creates a cluster, consisting of the specified number and type of Google Compute Engine instances. By default, the cluster is created in the project's [default network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks). One firewall is added for the cluster. After cluster creation, the Kubelet creates routes for each node to allow the containers on that node to communicate with all other instances in the cluster. Finally, an entry is added to the project's global metadata indicating which CIDR range the cluster is using.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AddonsConfigArgs']] addons_config: Configurations for the various addons available to run in the cluster.
        :param pulumi.Input[pulumi.InputType['AuthenticatorGroupsConfigArgs']] authenticator_groups_config: Configuration controlling RBAC group membership information.
        :param pulumi.Input[pulumi.InputType['AutopilotArgs']] autopilot: Autopilot configuration for the cluster.
        :param pulumi.Input[pulumi.InputType['ClusterAutoscalingArgs']] autoscaling: Cluster-level autoscaling configuration.
        :param pulumi.Input[pulumi.InputType['BinaryAuthorizationArgs']] binary_authorization: Configuration for Binary Authorization.
        :param pulumi.Input[str] cluster_ipv4_cidr: The IP address range of the container pods in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `10.96.0.0/14`). Leave blank to have one automatically chosen or specify a `/14` block in `10.0.0.0/8`.
        :param pulumi.Input[pulumi.InputType['ClusterTelemetryArgs']] cluster_telemetry: Telemetry integration for the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StatusConditionArgs']]]] conditions: Which conditions caused the current cluster state.
        :param pulumi.Input[pulumi.InputType['ConfidentialNodesArgs']] confidential_nodes: Configuration of Confidential Nodes. All the nodes in the cluster will be Confidential VM once enabled.
        :param pulumi.Input[pulumi.InputType['CostManagementConfigArgs']] cost_management_config: Configuration for the fine-grained cost management feature.
        :param pulumi.Input[pulumi.InputType['DatabaseEncryptionArgs']] database_encryption: Configuration of etcd encryption.
        :param pulumi.Input[pulumi.InputType['MaxPodsConstraintArgs']] default_max_pods_constraint: The default constraint on the maximum number of pods that can be run simultaneously on a node in the node pool of this cluster. Only honored if cluster created with IP Alias support.
        :param pulumi.Input[str] description: An optional description of this cluster.
        :param pulumi.Input[bool] enable_kubernetes_alpha: Kubernetes alpha features are enabled on this cluster. This includes alpha API groups (e.g. v1beta1) and features that may not be production ready in the kubernetes version of the master and nodes. The cluster has no SLA for uptime and master/node upgrades are disabled. Alpha enabled clusters are automatically deleted thirty days after creation.
        :param pulumi.Input[bool] enable_tpu: Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.
        :param pulumi.Input[pulumi.InputType['IdentityServiceConfigArgs']] identity_service_config: Configuration for Identity Service component.
        :param pulumi.Input[str] initial_cluster_version: The initial Kubernetes version for this cluster. Valid versions are those found in validMasterVersions returned by getServerConfig. The version can be upgraded over time; such upgrades are reflected in currentMasterVersion and currentNodeVersion. Users may specify either explicit versions offered by Kubernetes Engine or version aliases, which have the following behavior: - "latest": picks the highest valid Kubernetes version - "1.X": picks the highest valid patch+gke.N patch in the 1.X version - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version - "1.X.Y-gke.N": picks an explicit Kubernetes version - "","-": picks the default Kubernetes version
        :param pulumi.Input[int] initial_node_count: The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_group_urls: Deprecated. Use node_pools.instance_group_urls.
        :param pulumi.Input[pulumi.InputType['IPAllocationPolicyArgs']] ip_allocation_policy: Configuration for cluster IP allocation.
        :param pulumi.Input[pulumi.InputType['LegacyAbacArgs']] legacy_abac: Configuration for the legacy ABAC authorization mode.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations: The list of Google Compute Engine [zones](https://cloud.google.com/compute/docs/zones#available) in which the cluster's nodes should be located. This field provides a default value if [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) are not specified during node pool creation. Warning: changing cluster locations will update the [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) of all node pools and will result in nodes being added and/or removed.
        :param pulumi.Input[pulumi.InputType['LoggingConfigArgs']] logging_config: Logging configuration for the cluster.
        :param pulumi.Input[str] logging_service: The logging service the cluster should use to write logs. Currently available options: * `logging.googleapis.com/kubernetes` - The Cloud Logging service with a Kubernetes-native resource model * `logging.googleapis.com` - The legacy Cloud Logging service (no longer available as of GKE 1.15). * `none` - no logs will be exported from the cluster. If left as an empty string,`logging.googleapis.com/kubernetes` will be used for GKE 1.14+ or `logging.googleapis.com` for earlier versions.
        :param pulumi.Input[pulumi.InputType['MaintenancePolicyArgs']] maintenance_policy: Configure the maintenance policy for this cluster.
        :param pulumi.Input[pulumi.InputType['MasterArgs']] master: Configuration for master components.
        :param pulumi.Input[pulumi.InputType['MasterAuthArgs']] master_auth: The authentication information for accessing the master endpoint. If unspecified, the defaults are used: For clusters before v1.12, if master_auth is unspecified, `username` will be set to "admin", a random password will be generated, and a client certificate will be issued.
        :param pulumi.Input[pulumi.InputType['MasterAuthorizedNetworksConfigArgs']] master_authorized_networks_config: The configuration options for master authorized networks feature.
        :param pulumi.Input[str] master_ipv4_cidr_block: The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.
        :param pulumi.Input[pulumi.InputType['MeshCertificatesArgs']] mesh_certificates: Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        :param pulumi.Input[pulumi.InputType['MonitoringConfigArgs']] monitoring_config: Monitoring configuration for the cluster.
        :param pulumi.Input[str] monitoring_service: The monitoring service the cluster should use to write metrics. Currently available options: * "monitoring.googleapis.com/kubernetes" - The Cloud Monitoring service with a Kubernetes-native resource model * `monitoring.googleapis.com` - The legacy Cloud Monitoring service (no longer available as of GKE 1.15). * `none` - No metrics will be exported from the cluster. If left as an empty string,`monitoring.googleapis.com/kubernetes` will be used for GKE 1.14+ or `monitoring.googleapis.com` for earlier versions.
        :param pulumi.Input[str] name: The name of this cluster. The name must be unique within this project and location (e.g. zone or region), and can be up to 40 characters with the following restrictions: * Lowercase letters, numbers, and hyphens only. * Must start with a letter. * Must end with a number or a letter.
        :param pulumi.Input[str] network: The name of the Google Compute Engine [network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks) to which the cluster is connected. If left unspecified, the `default` network will be used. On output this shows the network ID instead of the name.
        :param pulumi.Input[pulumi.InputType['NetworkConfigArgs']] network_config: Configuration for cluster networking.
        :param pulumi.Input[pulumi.InputType['NetworkPolicyArgs']] network_policy: Configuration options for the NetworkPolicy feature.
        :param pulumi.Input[pulumi.InputType['NodeConfigArgs']] node_config: Parameters used in creating the cluster's nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.
        :param pulumi.Input[pulumi.InputType['NodePoolAutoConfigArgs']] node_pool_auto_config: Node pool configs that apply to all auto-provisioned node pools in autopilot clusters and node auto-provisioning enabled clusters.
        :param pulumi.Input[pulumi.InputType['NodePoolDefaultsArgs']] node_pool_defaults: Default NodePool settings for the entire cluster. These settings are overridden if specified on the specific NodePool object.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NodePoolArgs']]]] node_pools: The node pools associated with this cluster. This field should not be set if "node_config" or "initial_node_count" are specified.
        :param pulumi.Input[pulumi.InputType['NotificationConfigArgs']] notification_config: Notification configuration of the cluster.
        :param pulumi.Input[str] parent: The parent (project and location) where the cluster will be created. Specified in the format `projects/*/locations/*`.
        :param pulumi.Input[pulumi.InputType['PodSecurityPolicyConfigArgs']] pod_security_policy_config: Configuration for the PodSecurityPolicy feature.
        :param pulumi.Input[bool] private_cluster: If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.
        :param pulumi.Input[pulumi.InputType['PrivateClusterConfigArgs']] private_cluster_config: Configuration for private cluster.
        :param pulumi.Input[str] project: Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.
        :param pulumi.Input[pulumi.InputType['ProtectConfigArgs']] protect_config: Enable/Disable Protect API features for the cluster.
        :param pulumi.Input[pulumi.InputType['ReleaseChannelArgs']] release_channel: Release channel configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] resource_labels: The resource labels for the cluster to use to annotate any related Google Compute Engine resources.
        :param pulumi.Input[pulumi.InputType['ResourceUsageExportConfigArgs']] resource_usage_export_config: Configuration for exporting resource usages. Resource usage export is disabled when this config unspecified.
        :param pulumi.Input[pulumi.InputType['ShieldedNodesArgs']] shielded_nodes: Shielded Nodes configuration.
        :param pulumi.Input[str] subnetwork: The name of the Google Compute Engine [subnetwork](https://cloud.google.com/compute/docs/subnetworks) to which the cluster is connected. On output this shows the subnetwork ID instead of the name.
        :param pulumi.Input[pulumi.InputType['TpuConfigArgs']] tpu_config: Configuration for Cloud TPU support;
        :param pulumi.Input[pulumi.InputType['VerticalPodAutoscalingArgs']] vertical_pod_autoscaling: Cluster-level Vertical Pod Autoscaling configuration.
        :param pulumi.Input[pulumi.InputType['WorkloadALTSConfigArgs']] workload_alts_config: Configuration for direct-path (via ALTS) with workload identity.
        :param pulumi.Input[pulumi.InputType['WorkloadCertificatesArgs']] workload_certificates: Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        :param pulumi.Input[pulumi.InputType['WorkloadIdentityConfigArgs']] workload_identity_config: Configuration for the use of Kubernetes Service Accounts in GCP IAM policies.
        :param pulumi.Input[str] zone: Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: Optional[ClusterArgs]=None, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a cluster, consisting of the specified number and type of Google Compute Engine instances. By default, the cluster is created in the project's [default network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks). One firewall is added for the cluster. After cluster creation, the Kubelet creates routes for each node to allow the containers on that node to communicate with all other instances in the cluster. Finally, an entry is added to the project's global metadata indicating which CIDR range the cluster is using.

        :param str resource_name: The name of the resource.
        :param ClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, addons_config: Optional[pulumi.Input[pulumi.InputType['AddonsConfigArgs']]]=None, authenticator_groups_config: Optional[pulumi.Input[pulumi.InputType['AuthenticatorGroupsConfigArgs']]]=None, autopilot: Optional[pulumi.Input[pulumi.InputType['AutopilotArgs']]]=None, autoscaling: Optional[pulumi.Input[pulumi.InputType['ClusterAutoscalingArgs']]]=None, binary_authorization: Optional[pulumi.Input[pulumi.InputType['BinaryAuthorizationArgs']]]=None, cluster_ipv4_cidr: Optional[pulumi.Input[str]]=None, cluster_telemetry: Optional[pulumi.Input[pulumi.InputType['ClusterTelemetryArgs']]]=None, conditions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StatusConditionArgs']]]]]=None, confidential_nodes: Optional[pulumi.Input[pulumi.InputType['ConfidentialNodesArgs']]]=None, cost_management_config: Optional[pulumi.Input[pulumi.InputType['CostManagementConfigArgs']]]=None, database_encryption: Optional[pulumi.Input[pulumi.InputType['DatabaseEncryptionArgs']]]=None, default_max_pods_constraint: Optional[pulumi.Input[pulumi.InputType['MaxPodsConstraintArgs']]]=None, description: Optional[pulumi.Input[str]]=None, enable_kubernetes_alpha: Optional[pulumi.Input[bool]]=None, enable_tpu: Optional[pulumi.Input[bool]]=None, identity_service_config: Optional[pulumi.Input[pulumi.InputType['IdentityServiceConfigArgs']]]=None, initial_cluster_version: Optional[pulumi.Input[str]]=None, initial_node_count: Optional[pulumi.Input[int]]=None, instance_group_urls: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ip_allocation_policy: Optional[pulumi.Input[pulumi.InputType['IPAllocationPolicyArgs']]]=None, legacy_abac: Optional[pulumi.Input[pulumi.InputType['LegacyAbacArgs']]]=None, location: Optional[pulumi.Input[str]]=None, locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, logging_config: Optional[pulumi.Input[pulumi.InputType['LoggingConfigArgs']]]=None, logging_service: Optional[pulumi.Input[str]]=None, maintenance_policy: Optional[pulumi.Input[pulumi.InputType['MaintenancePolicyArgs']]]=None, master: Optional[pulumi.Input[pulumi.InputType['MasterArgs']]]=None, master_auth: Optional[pulumi.Input[pulumi.InputType['MasterAuthArgs']]]=None, master_authorized_networks_config: Optional[pulumi.Input[pulumi.InputType['MasterAuthorizedNetworksConfigArgs']]]=None, master_ipv4_cidr_block: Optional[pulumi.Input[str]]=None, mesh_certificates: Optional[pulumi.Input[pulumi.InputType['MeshCertificatesArgs']]]=None, monitoring_config: Optional[pulumi.Input[pulumi.InputType['MonitoringConfigArgs']]]=None, monitoring_service: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network: Optional[pulumi.Input[str]]=None, network_config: Optional[pulumi.Input[pulumi.InputType['NetworkConfigArgs']]]=None, network_policy: Optional[pulumi.Input[pulumi.InputType['NetworkPolicyArgs']]]=None, node_config: Optional[pulumi.Input[pulumi.InputType['NodeConfigArgs']]]=None, node_pool_auto_config: Optional[pulumi.Input[pulumi.InputType['NodePoolAutoConfigArgs']]]=None, node_pool_defaults: Optional[pulumi.Input[pulumi.InputType['NodePoolDefaultsArgs']]]=None, node_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NodePoolArgs']]]]]=None, notification_config: Optional[pulumi.Input[pulumi.InputType['NotificationConfigArgs']]]=None, parent: Optional[pulumi.Input[str]]=None, pod_security_policy_config: Optional[pulumi.Input[pulumi.InputType['PodSecurityPolicyConfigArgs']]]=None, private_cluster: Optional[pulumi.Input[bool]]=None, private_cluster_config: Optional[pulumi.Input[pulumi.InputType['PrivateClusterConfigArgs']]]=None, project: Optional[pulumi.Input[str]]=None, protect_config: Optional[pulumi.Input[pulumi.InputType['ProtectConfigArgs']]]=None, release_channel: Optional[pulumi.Input[pulumi.InputType['ReleaseChannelArgs']]]=None, resource_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, resource_usage_export_config: Optional[pulumi.Input[pulumi.InputType['ResourceUsageExportConfigArgs']]]=None, shielded_nodes: Optional[pulumi.Input[pulumi.InputType['ShieldedNodesArgs']]]=None, subnetwork: Optional[pulumi.Input[str]]=None, tpu_config: Optional[pulumi.Input[pulumi.InputType['TpuConfigArgs']]]=None, vertical_pod_autoscaling: Optional[pulumi.Input[pulumi.InputType['VerticalPodAutoscalingArgs']]]=None, workload_alts_config: Optional[pulumi.Input[pulumi.InputType['WorkloadALTSConfigArgs']]]=None, workload_certificates: Optional[pulumi.Input[pulumi.InputType['WorkloadCertificatesArgs']]]=None, workload_identity_config: Optional[pulumi.Input[pulumi.InputType['WorkloadIdentityConfigArgs']]]=None, zone: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterArgs.__new__(ClusterArgs)
            __props__.__dict__['addons_config'] = addons_config
            __props__.__dict__['authenticator_groups_config'] = authenticator_groups_config
            __props__.__dict__['autopilot'] = autopilot
            __props__.__dict__['autoscaling'] = autoscaling
            __props__.__dict__['binary_authorization'] = binary_authorization
            __props__.__dict__['cluster_ipv4_cidr'] = cluster_ipv4_cidr
            __props__.__dict__['cluster_telemetry'] = cluster_telemetry
            __props__.__dict__['conditions'] = conditions
            __props__.__dict__['confidential_nodes'] = confidential_nodes
            __props__.__dict__['cost_management_config'] = cost_management_config
            __props__.__dict__['database_encryption'] = database_encryption
            __props__.__dict__['default_max_pods_constraint'] = default_max_pods_constraint
            __props__.__dict__['description'] = description
            __props__.__dict__['enable_kubernetes_alpha'] = enable_kubernetes_alpha
            if enable_tpu is not None and (not opts.urn):
                warnings.warn('Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.', DeprecationWarning)
                pulumi.log.warn('enable_tpu is deprecated: Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.')
            __props__.__dict__['enable_tpu'] = enable_tpu
            __props__.__dict__['identity_service_config'] = identity_service_config
            __props__.__dict__['initial_cluster_version'] = initial_cluster_version
            if initial_node_count is not None and (not opts.urn):
                warnings.warn('The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.', DeprecationWarning)
                pulumi.log.warn('initial_node_count is deprecated: The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.')
            __props__.__dict__['initial_node_count'] = initial_node_count
            if instance_group_urls is not None and (not opts.urn):
                warnings.warn('Deprecated. Use node_pools.instance_group_urls.', DeprecationWarning)
                pulumi.log.warn('instance_group_urls is deprecated: Deprecated. Use node_pools.instance_group_urls.')
            __props__.__dict__['instance_group_urls'] = instance_group_urls
            __props__.__dict__['ip_allocation_policy'] = ip_allocation_policy
            __props__.__dict__['legacy_abac'] = legacy_abac
            __props__.__dict__['location'] = location
            __props__.__dict__['locations'] = locations
            __props__.__dict__['logging_config'] = logging_config
            __props__.__dict__['logging_service'] = logging_service
            __props__.__dict__['maintenance_policy'] = maintenance_policy
            __props__.__dict__['master'] = master
            __props__.__dict__['master_auth'] = master_auth
            __props__.__dict__['master_authorized_networks_config'] = master_authorized_networks_config
            if master_ipv4_cidr_block is not None and (not opts.urn):
                warnings.warn('The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.', DeprecationWarning)
                pulumi.log.warn('master_ipv4_cidr_block is deprecated: The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.')
            __props__.__dict__['master_ipv4_cidr_block'] = master_ipv4_cidr_block
            __props__.__dict__['mesh_certificates'] = mesh_certificates
            __props__.__dict__['monitoring_config'] = monitoring_config
            __props__.__dict__['monitoring_service'] = monitoring_service
            __props__.__dict__['name'] = name
            __props__.__dict__['network'] = network
            __props__.__dict__['network_config'] = network_config
            __props__.__dict__['network_policy'] = network_policy
            if node_config is not None and (not opts.urn):
                warnings.warn('Parameters used in creating the cluster\'s nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.', DeprecationWarning)
                pulumi.log.warn('node_config is deprecated: Parameters used in creating the cluster\'s nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.')
            __props__.__dict__['node_config'] = node_config
            __props__.__dict__['node_pool_auto_config'] = node_pool_auto_config
            __props__.__dict__['node_pool_defaults'] = node_pool_defaults
            __props__.__dict__['node_pools'] = node_pools
            __props__.__dict__['notification_config'] = notification_config
            __props__.__dict__['parent'] = parent
            __props__.__dict__['pod_security_policy_config'] = pod_security_policy_config
            if private_cluster is not None and (not opts.urn):
                warnings.warn('If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.', DeprecationWarning)
                pulumi.log.warn('private_cluster is deprecated: If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.')
            __props__.__dict__['private_cluster'] = private_cluster
            __props__.__dict__['private_cluster_config'] = private_cluster_config
            if project is not None and (not opts.urn):
                warnings.warn('Required. Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.', DeprecationWarning)
                pulumi.log.warn('project is deprecated: Required. Deprecated. The Google Developers Console [project ID or project number](https://cloud.google.com/resource-manager/docs/creating-managing-projects). This field has been deprecated and replaced by the parent field.')
            __props__.__dict__['project'] = project
            __props__.__dict__['protect_config'] = protect_config
            __props__.__dict__['release_channel'] = release_channel
            __props__.__dict__['resource_labels'] = resource_labels
            __props__.__dict__['resource_usage_export_config'] = resource_usage_export_config
            __props__.__dict__['shielded_nodes'] = shielded_nodes
            __props__.__dict__['subnetwork'] = subnetwork
            __props__.__dict__['tpu_config'] = tpu_config
            __props__.__dict__['vertical_pod_autoscaling'] = vertical_pod_autoscaling
            __props__.__dict__['workload_alts_config'] = workload_alts_config
            __props__.__dict__['workload_certificates'] = workload_certificates
            __props__.__dict__['workload_identity_config'] = workload_identity_config
            if zone is not None and (not opts.urn):
                warnings.warn('Required. Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.', DeprecationWarning)
                pulumi.log.warn('zone is deprecated: Required. Deprecated. The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field has been deprecated and replaced by the parent field.')
            __props__.__dict__['zone'] = zone
            __props__.__dict__['create_time'] = None
            __props__.__dict__['current_master_version'] = None
            __props__.__dict__['current_node_count'] = None
            __props__.__dict__['current_node_version'] = None
            __props__.__dict__['endpoint'] = None
            __props__.__dict__['expire_time'] = None
            __props__.__dict__['label_fingerprint'] = None
            __props__.__dict__['node_ipv4_cidr_size'] = None
            __props__.__dict__['self_link'] = None
            __props__.__dict__['services_ipv4_cidr'] = None
            __props__.__dict__['status'] = None
            __props__.__dict__['status_message'] = None
            __props__.__dict__['tpu_ipv4_cidr_block'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['location', 'project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Cluster, __self__).__init__('google-native:container/v1beta1:Cluster', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ClusterArgs.__new__(ClusterArgs)
        __props__.__dict__['addons_config'] = None
        __props__.__dict__['authenticator_groups_config'] = None
        __props__.__dict__['autopilot'] = None
        __props__.__dict__['autoscaling'] = None
        __props__.__dict__['binary_authorization'] = None
        __props__.__dict__['cluster_ipv4_cidr'] = None
        __props__.__dict__['cluster_telemetry'] = None
        __props__.__dict__['conditions'] = None
        __props__.__dict__['confidential_nodes'] = None
        __props__.__dict__['cost_management_config'] = None
        __props__.__dict__['create_time'] = None
        __props__.__dict__['current_master_version'] = None
        __props__.__dict__['current_node_count'] = None
        __props__.__dict__['current_node_version'] = None
        __props__.__dict__['database_encryption'] = None
        __props__.__dict__['default_max_pods_constraint'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['enable_kubernetes_alpha'] = None
        __props__.__dict__['enable_tpu'] = None
        __props__.__dict__['endpoint'] = None
        __props__.__dict__['expire_time'] = None
        __props__.__dict__['identity_service_config'] = None
        __props__.__dict__['initial_cluster_version'] = None
        __props__.__dict__['initial_node_count'] = None
        __props__.__dict__['instance_group_urls'] = None
        __props__.__dict__['ip_allocation_policy'] = None
        __props__.__dict__['label_fingerprint'] = None
        __props__.__dict__['legacy_abac'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['locations'] = None
        __props__.__dict__['logging_config'] = None
        __props__.__dict__['logging_service'] = None
        __props__.__dict__['maintenance_policy'] = None
        __props__.__dict__['master'] = None
        __props__.__dict__['master_auth'] = None
        __props__.__dict__['master_authorized_networks_config'] = None
        __props__.__dict__['master_ipv4_cidr_block'] = None
        __props__.__dict__['mesh_certificates'] = None
        __props__.__dict__['monitoring_config'] = None
        __props__.__dict__['monitoring_service'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['network'] = None
        __props__.__dict__['network_config'] = None
        __props__.__dict__['network_policy'] = None
        __props__.__dict__['node_config'] = None
        __props__.__dict__['node_ipv4_cidr_size'] = None
        __props__.__dict__['node_pool_auto_config'] = None
        __props__.__dict__['node_pool_defaults'] = None
        __props__.__dict__['node_pools'] = None
        __props__.__dict__['notification_config'] = None
        __props__.__dict__['pod_security_policy_config'] = None
        __props__.__dict__['private_cluster'] = None
        __props__.__dict__['private_cluster_config'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['protect_config'] = None
        __props__.__dict__['release_channel'] = None
        __props__.__dict__['resource_labels'] = None
        __props__.__dict__['resource_usage_export_config'] = None
        __props__.__dict__['self_link'] = None
        __props__.__dict__['services_ipv4_cidr'] = None
        __props__.__dict__['shielded_nodes'] = None
        __props__.__dict__['status'] = None
        __props__.__dict__['status_message'] = None
        __props__.__dict__['subnetwork'] = None
        __props__.__dict__['tpu_config'] = None
        __props__.__dict__['tpu_ipv4_cidr_block'] = None
        __props__.__dict__['vertical_pod_autoscaling'] = None
        __props__.__dict__['workload_alts_config'] = None
        __props__.__dict__['workload_certificates'] = None
        __props__.__dict__['workload_identity_config'] = None
        __props__.__dict__['zone'] = None
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='addonsConfig')
    def addons_config(self) -> pulumi.Output['outputs.AddonsConfigResponse']:
        """
        Configurations for the various addons available to run in the cluster.
        """
        return pulumi.get(self, 'addons_config')

    @property
    @pulumi.getter(name='authenticatorGroupsConfig')
    def authenticator_groups_config(self) -> pulumi.Output['outputs.AuthenticatorGroupsConfigResponse']:
        """
        Configuration controlling RBAC group membership information.
        """
        return pulumi.get(self, 'authenticator_groups_config')

    @property
    @pulumi.getter
    def autopilot(self) -> pulumi.Output['outputs.AutopilotResponse']:
        """
        Autopilot configuration for the cluster.
        """
        return pulumi.get(self, 'autopilot')

    @property
    @pulumi.getter
    def autoscaling(self) -> pulumi.Output['outputs.ClusterAutoscalingResponse']:
        """
        Cluster-level autoscaling configuration.
        """
        return pulumi.get(self, 'autoscaling')

    @property
    @pulumi.getter(name='binaryAuthorization')
    def binary_authorization(self) -> pulumi.Output['outputs.BinaryAuthorizationResponse']:
        """
        Configuration for Binary Authorization.
        """
        return pulumi.get(self, 'binary_authorization')

    @property
    @pulumi.getter(name='clusterIpv4Cidr')
    def cluster_ipv4_cidr(self) -> pulumi.Output[str]:
        """
        The IP address range of the container pods in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `10.96.0.0/14`). Leave blank to have one automatically chosen or specify a `/14` block in `10.0.0.0/8`.
        """
        return pulumi.get(self, 'cluster_ipv4_cidr')

    @property
    @pulumi.getter(name='clusterTelemetry')
    def cluster_telemetry(self) -> pulumi.Output['outputs.ClusterTelemetryResponse']:
        """
        Telemetry integration for the cluster.
        """
        return pulumi.get(self, 'cluster_telemetry')

    @property
    @pulumi.getter
    def conditions(self) -> pulumi.Output[Sequence['outputs.StatusConditionResponse']]:
        """
        Which conditions caused the current cluster state.
        """
        return pulumi.get(self, 'conditions')

    @property
    @pulumi.getter(name='confidentialNodes')
    def confidential_nodes(self) -> pulumi.Output['outputs.ConfidentialNodesResponse']:
        """
        Configuration of Confidential Nodes. All the nodes in the cluster will be Confidential VM once enabled.
        """
        return pulumi.get(self, 'confidential_nodes')

    @property
    @pulumi.getter(name='costManagementConfig')
    def cost_management_config(self) -> pulumi.Output['outputs.CostManagementConfigResponse']:
        """
        Configuration for the fine-grained cost management feature.
        """
        return pulumi.get(self, 'cost_management_config')

    @property
    @pulumi.getter(name='createTime')
    def create_time(self) -> pulumi.Output[str]:
        """
        [Output only] The time the cluster was created, in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) text format.
        """
        return pulumi.get(self, 'create_time')

    @property
    @pulumi.getter(name='currentMasterVersion')
    def current_master_version(self) -> pulumi.Output[str]:
        """
        [Output only] The current software version of the master endpoint.
        """
        return pulumi.get(self, 'current_master_version')

    @property
    @pulumi.getter(name='currentNodeCount')
    def current_node_count(self) -> pulumi.Output[int]:
        """
        [Output only] The number of nodes currently in the cluster. Deprecated. Call Kubernetes API directly to retrieve node information.
        """
        return pulumi.get(self, 'current_node_count')

    @property
    @pulumi.getter(name='currentNodeVersion')
    def current_node_version(self) -> pulumi.Output[str]:
        """
        [Output only] Deprecated, use [NodePool.version](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.clusters.nodePools) instead. The current version of the node software components. If they are currently at multiple versions because they're in the process of being upgraded, this reflects the minimum version of all nodes.
        """
        return pulumi.get(self, 'current_node_version')

    @property
    @pulumi.getter(name='databaseEncryption')
    def database_encryption(self) -> pulumi.Output['outputs.DatabaseEncryptionResponse']:
        """
        Configuration of etcd encryption.
        """
        return pulumi.get(self, 'database_encryption')

    @property
    @pulumi.getter(name='defaultMaxPodsConstraint')
    def default_max_pods_constraint(self) -> pulumi.Output['outputs.MaxPodsConstraintResponse']:
        """
        The default constraint on the maximum number of pods that can be run simultaneously on a node in the node pool of this cluster. Only honored if cluster created with IP Alias support.
        """
        return pulumi.get(self, 'default_max_pods_constraint')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this cluster.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='enableKubernetesAlpha')
    def enable_kubernetes_alpha(self) -> pulumi.Output[bool]:
        """
        Kubernetes alpha features are enabled on this cluster. This includes alpha API groups (e.g. v1beta1) and features that may not be production ready in the kubernetes version of the master and nodes. The cluster has no SLA for uptime and master/node upgrades are disabled. Alpha enabled clusters are automatically deleted thirty days after creation.
        """
        return pulumi.get(self, 'enable_kubernetes_alpha')

    @property
    @pulumi.getter(name='enableTpu')
    def enable_tpu(self) -> pulumi.Output[bool]:
        """
        Enable the ability to use Cloud TPUs in this cluster. This field is deprecated, use tpu_config.enabled instead.
        """
        return pulumi.get(self, 'enable_tpu')

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[str]:
        """
        [Output only] The IP address of this cluster's master endpoint. The endpoint can be accessed from the internet at `https://username:password@endpoint/`. See the `masterAuth` property of this resource for username and password information.
        """
        return pulumi.get(self, 'endpoint')

    @property
    @pulumi.getter(name='expireTime')
    def expire_time(self) -> pulumi.Output[str]:
        """
        [Output only] The time the cluster will be automatically deleted in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) text format.
        """
        return pulumi.get(self, 'expire_time')

    @property
    @pulumi.getter(name='identityServiceConfig')
    def identity_service_config(self) -> pulumi.Output['outputs.IdentityServiceConfigResponse']:
        """
        Configuration for Identity Service component.
        """
        return pulumi.get(self, 'identity_service_config')

    @property
    @pulumi.getter(name='initialClusterVersion')
    def initial_cluster_version(self) -> pulumi.Output[str]:
        """
        The initial Kubernetes version for this cluster. Valid versions are those found in validMasterVersions returned by getServerConfig. The version can be upgraded over time; such upgrades are reflected in currentMasterVersion and currentNodeVersion. Users may specify either explicit versions offered by Kubernetes Engine or version aliases, which have the following behavior: - "latest": picks the highest valid Kubernetes version - "1.X": picks the highest valid patch+gke.N patch in the 1.X version - "1.X.Y": picks the highest valid gke.N patch in the 1.X.Y version - "1.X.Y-gke.N": picks an explicit Kubernetes version - "","-": picks the default Kubernetes version
        """
        return pulumi.get(self, 'initial_cluster_version')

    @property
    @pulumi.getter(name='initialNodeCount')
    def initial_node_count(self) -> pulumi.Output[int]:
        """
        The number of nodes to create in this cluster. You must ensure that your Compute Engine [resource quota](https://cloud.google.com/compute/quotas) is sufficient for this number of instances. You must also have available firewall and routes quota. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "node_config") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. This field is deprecated, use node_pool.initial_node_count instead.
        """
        return pulumi.get(self, 'initial_node_count')

    @property
    @pulumi.getter(name='instanceGroupUrls')
    def instance_group_urls(self) -> pulumi.Output[Sequence[str]]:
        """
        Deprecated. Use node_pools.instance_group_urls.
        """
        return pulumi.get(self, 'instance_group_urls')

    @property
    @pulumi.getter(name='ipAllocationPolicy')
    def ip_allocation_policy(self) -> pulumi.Output['outputs.IPAllocationPolicyResponse']:
        """
        Configuration for cluster IP allocation.
        """
        return pulumi.get(self, 'ip_allocation_policy')

    @property
    @pulumi.getter(name='labelFingerprint')
    def label_fingerprint(self) -> pulumi.Output[str]:
        """
        The fingerprint of the set of labels for this cluster.
        """
        return pulumi.get(self, 'label_fingerprint')

    @property
    @pulumi.getter(name='legacyAbac')
    def legacy_abac(self) -> pulumi.Output['outputs.LegacyAbacResponse']:
        """
        Configuration for the legacy ABAC authorization mode.
        """
        return pulumi.get(self, 'legacy_abac')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Output[Sequence[str]]:
        """
        The list of Google Compute Engine [zones](https://cloud.google.com/compute/docs/zones#available) in which the cluster's nodes should be located. This field provides a default value if [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) are not specified during node pool creation. Warning: changing cluster locations will update the [NodePool.Locations](https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations) of all node pools and will result in nodes being added and/or removed.
        """
        return pulumi.get(self, 'locations')

    @property
    @pulumi.getter(name='loggingConfig')
    def logging_config(self) -> pulumi.Output['outputs.LoggingConfigResponse']:
        """
        Logging configuration for the cluster.
        """
        return pulumi.get(self, 'logging_config')

    @property
    @pulumi.getter(name='loggingService')
    def logging_service(self) -> pulumi.Output[str]:
        """
        The logging service the cluster should use to write logs. Currently available options: * `logging.googleapis.com/kubernetes` - The Cloud Logging service with a Kubernetes-native resource model * `logging.googleapis.com` - The legacy Cloud Logging service (no longer available as of GKE 1.15). * `none` - no logs will be exported from the cluster. If left as an empty string,`logging.googleapis.com/kubernetes` will be used for GKE 1.14+ or `logging.googleapis.com` for earlier versions.
        """
        return pulumi.get(self, 'logging_service')

    @property
    @pulumi.getter(name='maintenancePolicy')
    def maintenance_policy(self) -> pulumi.Output['outputs.MaintenancePolicyResponse']:
        """
        Configure the maintenance policy for this cluster.
        """
        return pulumi.get(self, 'maintenance_policy')

    @property
    @pulumi.getter
    def master(self) -> pulumi.Output['outputs.MasterResponse']:
        """
        Configuration for master components.
        """
        return pulumi.get(self, 'master')

    @property
    @pulumi.getter(name='masterAuth')
    def master_auth(self) -> pulumi.Output['outputs.MasterAuthResponse']:
        """
        The authentication information for accessing the master endpoint. If unspecified, the defaults are used: For clusters before v1.12, if master_auth is unspecified, `username` will be set to "admin", a random password will be generated, and a client certificate will be issued.
        """
        return pulumi.get(self, 'master_auth')

    @property
    @pulumi.getter(name='masterAuthorizedNetworksConfig')
    def master_authorized_networks_config(self) -> pulumi.Output['outputs.MasterAuthorizedNetworksConfigResponse']:
        """
        The configuration options for master authorized networks feature.
        """
        return pulumi.get(self, 'master_authorized_networks_config')

    @property
    @pulumi.getter(name='masterIpv4CidrBlock')
    def master_ipv4_cidr_block(self) -> pulumi.Output[str]:
        """
        The IP prefix in CIDR notation to use for the hosted master network. This prefix will be used for assigning private IP addresses to the master or set of masters, as well as the ILB VIP. This field is deprecated, use private_cluster_config.master_ipv4_cidr_block instead.
        """
        return pulumi.get(self, 'master_ipv4_cidr_block')

    @property
    @pulumi.getter(name='meshCertificates')
    def mesh_certificates(self) -> pulumi.Output['outputs.MeshCertificatesResponse']:
        """
        Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        """
        return pulumi.get(self, 'mesh_certificates')

    @property
    @pulumi.getter(name='monitoringConfig')
    def monitoring_config(self) -> pulumi.Output['outputs.MonitoringConfigResponse']:
        """
        Monitoring configuration for the cluster.
        """
        return pulumi.get(self, 'monitoring_config')

    @property
    @pulumi.getter(name='monitoringService')
    def monitoring_service(self) -> pulumi.Output[str]:
        """
        The monitoring service the cluster should use to write metrics. Currently available options: * "monitoring.googleapis.com/kubernetes" - The Cloud Monitoring service with a Kubernetes-native resource model * `monitoring.googleapis.com` - The legacy Cloud Monitoring service (no longer available as of GKE 1.15). * `none` - No metrics will be exported from the cluster. If left as an empty string,`monitoring.googleapis.com/kubernetes` will be used for GKE 1.14+ or `monitoring.googleapis.com` for earlier versions.
        """
        return pulumi.get(self, 'monitoring_service')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of this cluster. The name must be unique within this project and location (e.g. zone or region), and can be up to 40 characters with the following restrictions: * Lowercase letters, numbers, and hyphens only. * Must start with a letter. * Must end with a number or a letter.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The name of the Google Compute Engine [network](https://cloud.google.com/compute/docs/networks-and-firewalls#networks) to which the cluster is connected. If left unspecified, the `default` network will be used. On output this shows the network ID instead of the name.
        """
        return pulumi.get(self, 'network')

    @property
    @pulumi.getter(name='networkConfig')
    def network_config(self) -> pulumi.Output['outputs.NetworkConfigResponse']:
        """
        Configuration for cluster networking.
        """
        return pulumi.get(self, 'network_config')

    @property
    @pulumi.getter(name='networkPolicy')
    def network_policy(self) -> pulumi.Output['outputs.NetworkPolicyResponse']:
        """
        Configuration options for the NetworkPolicy feature.
        """
        return pulumi.get(self, 'network_policy')

    @property
    @pulumi.getter(name='nodeConfig')
    def node_config(self) -> pulumi.Output['outputs.NodeConfigResponse']:
        """
        Parameters used in creating the cluster's nodes. For requests, this field should only be used in lieu of a "node_pool" object, since this configuration (along with the "initial_node_count") will be used to create a "NodePool" object with an auto-generated name. Do not use this and a node_pool at the same time. For responses, this field will be populated with the node configuration of the first node pool. (For configuration of each node pool, see `node_pool.config`) If unspecified, the defaults are used. This field is deprecated, use node_pool.config instead.
        """
        return pulumi.get(self, 'node_config')

    @property
    @pulumi.getter(name='nodeIpv4CidrSize')
    def node_ipv4_cidr_size(self) -> pulumi.Output[int]:
        """
        [Output only] The size of the address space on each node for hosting containers. This is provisioned from within the `container_ipv4_cidr` range. This field will only be set when cluster is in route-based network mode.
        """
        return pulumi.get(self, 'node_ipv4_cidr_size')

    @property
    @pulumi.getter(name='nodePoolAutoConfig')
    def node_pool_auto_config(self) -> pulumi.Output['outputs.NodePoolAutoConfigResponse']:
        """
        Node pool configs that apply to all auto-provisioned node pools in autopilot clusters and node auto-provisioning enabled clusters.
        """
        return pulumi.get(self, 'node_pool_auto_config')

    @property
    @pulumi.getter(name='nodePoolDefaults')
    def node_pool_defaults(self) -> pulumi.Output['outputs.NodePoolDefaultsResponse']:
        """
        Default NodePool settings for the entire cluster. These settings are overridden if specified on the specific NodePool object.
        """
        return pulumi.get(self, 'node_pool_defaults')

    @property
    @pulumi.getter(name='nodePools')
    def node_pools(self) -> pulumi.Output[Sequence['outputs.NodePoolResponse']]:
        """
        The node pools associated with this cluster. This field should not be set if "node_config" or "initial_node_count" are specified.
        """
        return pulumi.get(self, 'node_pools')

    @property
    @pulumi.getter(name='notificationConfig')
    def notification_config(self) -> pulumi.Output['outputs.NotificationConfigResponse']:
        """
        Notification configuration of the cluster.
        """
        return pulumi.get(self, 'notification_config')

    @property
    @pulumi.getter(name='podSecurityPolicyConfig')
    def pod_security_policy_config(self) -> pulumi.Output['outputs.PodSecurityPolicyConfigResponse']:
        """
        Configuration for the PodSecurityPolicy feature.
        """
        return pulumi.get(self, 'pod_security_policy_config')

    @property
    @pulumi.getter(name='privateCluster')
    def private_cluster(self) -> pulumi.Output[bool]:
        """
        If this is a private cluster setup. Private clusters are clusters that, by default have no external IP addresses on the nodes and where nodes and the master communicate over private IP addresses. This field is deprecated, use private_cluster_config.enable_private_nodes instead.
        """
        return pulumi.get(self, 'private_cluster')

    @property
    @pulumi.getter(name='privateClusterConfig')
    def private_cluster_config(self) -> pulumi.Output['outputs.PrivateClusterConfigResponse']:
        """
        Configuration for private cluster.
        """
        return pulumi.get(self, 'private_cluster_config')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter(name='protectConfig')
    def protect_config(self) -> pulumi.Output['outputs.ProtectConfigResponse']:
        """
        Enable/Disable Protect API features for the cluster.
        """
        return pulumi.get(self, 'protect_config')

    @property
    @pulumi.getter(name='releaseChannel')
    def release_channel(self) -> pulumi.Output['outputs.ReleaseChannelResponse']:
        """
        Release channel configuration.
        """
        return pulumi.get(self, 'release_channel')

    @property
    @pulumi.getter(name='resourceLabels')
    def resource_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The resource labels for the cluster to use to annotate any related Google Compute Engine resources.
        """
        return pulumi.get(self, 'resource_labels')

    @property
    @pulumi.getter(name='resourceUsageExportConfig')
    def resource_usage_export_config(self) -> pulumi.Output['outputs.ResourceUsageExportConfigResponse']:
        """
        Configuration for exporting resource usages. Resource usage export is disabled when this config unspecified.
        """
        return pulumi.get(self, 'resource_usage_export_config')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> pulumi.Output[str]:
        """
        [Output only] Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter(name='servicesIpv4Cidr')
    def services_ipv4_cidr(self) -> pulumi.Output[str]:
        """
        [Output only] The IP address range of the Kubernetes services in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `1.2.3.4/29`). Service addresses are typically put in the last `/16` from the container CIDR.
        """
        return pulumi.get(self, 'services_ipv4_cidr')

    @property
    @pulumi.getter(name='shieldedNodes')
    def shielded_nodes(self) -> pulumi.Output['outputs.ShieldedNodesResponse']:
        """
        Shielded Nodes configuration.
        """
        return pulumi.get(self, 'shielded_nodes')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        [Output only] The current status of this cluster.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter(name='statusMessage')
    def status_message(self) -> pulumi.Output[str]:
        """
        [Output only] Deprecated. Use conditions instead. Additional information about the current status of this cluster, if available.
        """
        return pulumi.get(self, 'status_message')

    @property
    @pulumi.getter
    def subnetwork(self) -> pulumi.Output[str]:
        """
        The name of the Google Compute Engine [subnetwork](https://cloud.google.com/compute/docs/subnetworks) to which the cluster is connected. On output this shows the subnetwork ID instead of the name.
        """
        return pulumi.get(self, 'subnetwork')

    @property
    @pulumi.getter(name='tpuConfig')
    def tpu_config(self) -> pulumi.Output['outputs.TpuConfigResponse']:
        """
        Configuration for Cloud TPU support;
        """
        return pulumi.get(self, 'tpu_config')

    @property
    @pulumi.getter(name='tpuIpv4CidrBlock')
    def tpu_ipv4_cidr_block(self) -> pulumi.Output[str]:
        """
        [Output only] The IP address range of the Cloud TPUs in this cluster, in [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation (e.g. `1.2.3.4/29`).
        """
        return pulumi.get(self, 'tpu_ipv4_cidr_block')

    @property
    @pulumi.getter(name='verticalPodAutoscaling')
    def vertical_pod_autoscaling(self) -> pulumi.Output['outputs.VerticalPodAutoscalingResponse']:
        """
        Cluster-level Vertical Pod Autoscaling configuration.
        """
        return pulumi.get(self, 'vertical_pod_autoscaling')

    @property
    @pulumi.getter(name='workloadAltsConfig')
    def workload_alts_config(self) -> pulumi.Output['outputs.WorkloadALTSConfigResponse']:
        """
        Configuration for direct-path (via ALTS) with workload identity.
        """
        return pulumi.get(self, 'workload_alts_config')

    @property
    @pulumi.getter(name='workloadCertificates')
    def workload_certificates(self) -> pulumi.Output['outputs.WorkloadCertificatesResponse']:
        """
        Configuration for issuance of mTLS keys and certificates to Kubernetes pods.
        """
        return pulumi.get(self, 'workload_certificates')

    @property
    @pulumi.getter(name='workloadIdentityConfig')
    def workload_identity_config(self) -> pulumi.Output['outputs.WorkloadIdentityConfigResponse']:
        """
        Configuration for the use of Kubernetes Service Accounts in GCP IAM policies.
        """
        return pulumi.get(self, 'workload_identity_config')

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        """
        [Output only] The name of the Google Compute Engine [zone](https://cloud.google.com/compute/docs/zones#available) in which the cluster resides. This field is deprecated, use location instead.
        """
        return pulumi.get(self, 'zone')

    @pulumi.output_type
    class GetKubeconfigResult:

        def __init__(__self__, kubeconfig=None):
            if kubeconfig and (not isinstance(kubeconfig, str)):
                raise TypeError("Expected argument 'kubeconfig' to be a str")
            pulumi.set(__self__, 'kubeconfig', kubeconfig)

        @property
        @pulumi.getter
        def kubeconfig(self) -> str:
            return pulumi.get(self, 'kubeconfig')

    def get_kubeconfig(__self__) -> pulumi.Output['str']:
        """
        Generate a kubeconfig for cluster authentication.

        The kubeconfig generated is automatically stringified for ease of use with the pulumi/kubernetes provider.
        The kubeconfig uses the new `gke-gcloud-auth-plugin` authentication plugin as recommended by Google.

        See for more details:
        - https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
        """
        __args__ = dict()
        __args__['__self__'] = __self__
        __result__ = pulumi.runtime.call('google-native:container/v1beta1:Cluster/getKubeconfig', __args__, res=__self__, typ=Cluster.GetKubeconfigResult)
        return __result__.kubeconfig