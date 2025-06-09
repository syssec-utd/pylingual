import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetRegionTargetTcpProxyResult', 'AwaitableGetRegionTargetTcpProxyResult', 'get_region_target_tcp_proxy', 'get_region_target_tcp_proxy_output']

@pulumi.output_type
class GetRegionTargetTcpProxyResult:

    def __init__(__self__, creation_timestamp=None, description=None, kind=None, name=None, proxy_bind=None, proxy_header=None, region=None, self_link=None, service=None):
        if creation_timestamp and (not isinstance(creation_timestamp, str)):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, 'creation_timestamp', creation_timestamp)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if proxy_bind and (not isinstance(proxy_bind, bool)):
            raise TypeError("Expected argument 'proxy_bind' to be a bool")
        pulumi.set(__self__, 'proxy_bind', proxy_bind)
        if proxy_header and (not isinstance(proxy_header, str)):
            raise TypeError("Expected argument 'proxy_header' to be a str")
        pulumi.set(__self__, 'proxy_header', proxy_header)
        if region and (not isinstance(region, str)):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, 'region', region)
        if self_link and (not isinstance(self_link, str)):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, 'self_link', self_link)
        if service and (not isinstance(service, str)):
            raise TypeError("Expected argument 'service' to be a str")
        pulumi.set(__self__, 'service', service)

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> str:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Type of the resource. Always compute#targetTcpProxy for target TCP proxies.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='proxyBind')
    def proxy_bind(self) -> bool:
        """
        This field only applies when the forwarding rule that references this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED. When this field is set to true, Envoy proxies set up inbound traffic interception and bind to the IP address and port specified in the forwarding rule. This is generally useful when using Traffic Director to configure Envoy as a gateway or middle proxy (in other words, not a sidecar proxy). The Envoy proxy listens for inbound requests and handles requests when it receives them. The default is false.
        """
        return pulumi.get(self, 'proxy_bind')

    @property
    @pulumi.getter(name='proxyHeader')
    def proxy_header(self) -> str:
        """
        Specifies the type of proxy header to append before sending data to the backend, either NONE or PROXY_V1. The default is NONE.
        """
        return pulumi.get(self, 'proxy_header')

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        URL of the region where the regional TCP proxy resides. This field is not applicable to global TCP proxy.
        """
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> str:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        URL to the BackendService resource.
        """
        return pulumi.get(self, 'service')

class AwaitableGetRegionTargetTcpProxyResult(GetRegionTargetTcpProxyResult):

    def __await__(self):
        if False:
            yield self
        return GetRegionTargetTcpProxyResult(creation_timestamp=self.creation_timestamp, description=self.description, kind=self.kind, name=self.name, proxy_bind=self.proxy_bind, proxy_header=self.proxy_header, region=self.region, self_link=self.self_link, service=self.service)

def get_region_target_tcp_proxy(project: Optional[str]=None, region: Optional[str]=None, target_tcp_proxy: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetRegionTargetTcpProxyResult:
    """
    Returns the specified TargetTcpProxy resource.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['region'] = region
    __args__['targetTcpProxy'] = target_tcp_proxy
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:compute/beta:getRegionTargetTcpProxy', __args__, opts=opts, typ=GetRegionTargetTcpProxyResult).value
    return AwaitableGetRegionTargetTcpProxyResult(creation_timestamp=__ret__.creation_timestamp, description=__ret__.description, kind=__ret__.kind, name=__ret__.name, proxy_bind=__ret__.proxy_bind, proxy_header=__ret__.proxy_header, region=__ret__.region, self_link=__ret__.self_link, service=__ret__.service)

@_utilities.lift_output_func(get_region_target_tcp_proxy)
def get_region_target_tcp_proxy_output(project: Optional[pulumi.Input[Optional[str]]]=None, region: Optional[pulumi.Input[str]]=None, target_tcp_proxy: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetRegionTargetTcpProxyResult]:
    """
    Returns the specified TargetTcpProxy resource.
    """
    ...