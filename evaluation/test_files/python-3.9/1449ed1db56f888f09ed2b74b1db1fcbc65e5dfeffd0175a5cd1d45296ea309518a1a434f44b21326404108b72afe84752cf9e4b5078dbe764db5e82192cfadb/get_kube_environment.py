import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetKubeEnvironmentResult', 'AwaitableGetKubeEnvironmentResult', 'get_kube_environment', 'get_kube_environment_output']

@pulumi.output_type
class GetKubeEnvironmentResult:
    """
    A Kubernetes cluster specialized for web workloads by Azure App Service
    """

    def __init__(__self__, aks_resource_id=None, app_logs_configuration=None, arc_configuration=None, default_domain=None, deployment_errors=None, extended_location=None, id=None, internal_load_balancer_enabled=None, kind=None, location=None, name=None, provisioning_state=None, static_ip=None, tags=None, type=None):
        if aks_resource_id and (not isinstance(aks_resource_id, str)):
            raise TypeError("Expected argument 'aks_resource_id' to be a str")
        pulumi.set(__self__, 'aks_resource_id', aks_resource_id)
        if app_logs_configuration and (not isinstance(app_logs_configuration, dict)):
            raise TypeError("Expected argument 'app_logs_configuration' to be a dict")
        pulumi.set(__self__, 'app_logs_configuration', app_logs_configuration)
        if arc_configuration and (not isinstance(arc_configuration, dict)):
            raise TypeError("Expected argument 'arc_configuration' to be a dict")
        pulumi.set(__self__, 'arc_configuration', arc_configuration)
        if default_domain and (not isinstance(default_domain, str)):
            raise TypeError("Expected argument 'default_domain' to be a str")
        pulumi.set(__self__, 'default_domain', default_domain)
        if deployment_errors and (not isinstance(deployment_errors, str)):
            raise TypeError("Expected argument 'deployment_errors' to be a str")
        pulumi.set(__self__, 'deployment_errors', deployment_errors)
        if extended_location and (not isinstance(extended_location, dict)):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, 'extended_location', extended_location)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if internal_load_balancer_enabled and (not isinstance(internal_load_balancer_enabled, bool)):
            raise TypeError("Expected argument 'internal_load_balancer_enabled' to be a bool")
        pulumi.set(__self__, 'internal_load_balancer_enabled', internal_load_balancer_enabled)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if static_ip and (not isinstance(static_ip, str)):
            raise TypeError("Expected argument 'static_ip' to be a str")
        pulumi.set(__self__, 'static_ip', static_ip)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='aksResourceID')
    def aks_resource_id(self) -> Optional[str]:
        return pulumi.get(self, 'aks_resource_id')

    @property
    @pulumi.getter(name='appLogsConfiguration')
    def app_logs_configuration(self) -> Optional['outputs.AppLogsConfigurationResponse']:
        """
        Cluster configuration which enables the log daemon to export
        app logs to a destination. Currently only "log-analytics" is
        supported
        """
        return pulumi.get(self, 'app_logs_configuration')

    @property
    @pulumi.getter(name='arcConfiguration')
    def arc_configuration(self) -> Optional['outputs.ArcConfigurationResponse']:
        """
        Cluster configuration which determines the ARC cluster
        components types. Eg: Choosing between BuildService kind,
        FrontEnd Service ArtifactsStorageType etc.
        """
        return pulumi.get(self, 'arc_configuration')

    @property
    @pulumi.getter(name='defaultDomain')
    def default_domain(self) -> str:
        """
        Default Domain Name for the cluster
        """
        return pulumi.get(self, 'default_domain')

    @property
    @pulumi.getter(name='deploymentErrors')
    def deployment_errors(self) -> str:
        """
        Any errors that occurred during deployment or deployment validation
        """
        return pulumi.get(self, 'deployment_errors')

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> Optional['outputs.ExtendedLocationResponse']:
        """
        Extended Location.
        """
        return pulumi.get(self, 'extended_location')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='internalLoadBalancerEnabled')
    def internal_load_balancer_enabled(self) -> Optional[bool]:
        """
        Only visible within Vnet/Subnet
        """
        return pulumi.get(self, 'internal_load_balancer_enabled')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Kubernetes Environment.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='staticIp')
    def static_ip(self) -> Optional[str]:
        """
        Static IP of the KubeEnvironment
        """
        return pulumi.get(self, 'static_ip')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetKubeEnvironmentResult(GetKubeEnvironmentResult):

    def __await__(self):
        if False:
            yield self
        return GetKubeEnvironmentResult(aks_resource_id=self.aks_resource_id, app_logs_configuration=self.app_logs_configuration, arc_configuration=self.arc_configuration, default_domain=self.default_domain, deployment_errors=self.deployment_errors, extended_location=self.extended_location, id=self.id, internal_load_balancer_enabled=self.internal_load_balancer_enabled, kind=self.kind, location=self.location, name=self.name, provisioning_state=self.provisioning_state, static_ip=self.static_ip, tags=self.tags, type=self.type)

def get_kube_environment(name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetKubeEnvironmentResult:
    """
    A Kubernetes cluster specialized for web workloads by Azure App Service
    API Version: 2021-01-01.


    :param str name: Name of the Kubernetes Environment.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web:getKubeEnvironment', __args__, opts=opts, typ=GetKubeEnvironmentResult).value
    return AwaitableGetKubeEnvironmentResult(aks_resource_id=__ret__.aks_resource_id, app_logs_configuration=__ret__.app_logs_configuration, arc_configuration=__ret__.arc_configuration, default_domain=__ret__.default_domain, deployment_errors=__ret__.deployment_errors, extended_location=__ret__.extended_location, id=__ret__.id, internal_load_balancer_enabled=__ret__.internal_load_balancer_enabled, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, static_ip=__ret__.static_ip, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_kube_environment)
def get_kube_environment_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetKubeEnvironmentResult]:
    """
    A Kubernetes cluster specialized for web workloads by Azure App Service
    API Version: 2021-01-01.


    :param str name: Name of the Kubernetes Environment.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...