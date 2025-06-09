import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetSignalRResult', 'AwaitableGetSignalRResult', 'get_signal_r', 'get_signal_r_output']

@pulumi.output_type
class GetSignalRResult:
    """
    A class represent a SignalR service resource.
    """

    def __init__(__self__, cors=None, external_ip=None, features=None, host_name=None, host_name_prefix=None, id=None, kind=None, location=None, name=None, network_acls=None, private_endpoint_connections=None, provisioning_state=None, public_port=None, server_port=None, sku=None, tags=None, type=None, upstream=None, version=None):
        if cors and (not isinstance(cors, dict)):
            raise TypeError("Expected argument 'cors' to be a dict")
        pulumi.set(__self__, 'cors', cors)
        if external_ip and (not isinstance(external_ip, str)):
            raise TypeError("Expected argument 'external_ip' to be a str")
        pulumi.set(__self__, 'external_ip', external_ip)
        if features and (not isinstance(features, list)):
            raise TypeError("Expected argument 'features' to be a list")
        pulumi.set(__self__, 'features', features)
        if host_name and (not isinstance(host_name, str)):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, 'host_name', host_name)
        if host_name_prefix and (not isinstance(host_name_prefix, str)):
            raise TypeError("Expected argument 'host_name_prefix' to be a str")
        pulumi.set(__self__, 'host_name_prefix', host_name_prefix)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if network_acls and (not isinstance(network_acls, dict)):
            raise TypeError("Expected argument 'network_acls' to be a dict")
        pulumi.set(__self__, 'network_acls', network_acls)
        if private_endpoint_connections and (not isinstance(private_endpoint_connections, list)):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, 'private_endpoint_connections', private_endpoint_connections)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if public_port and (not isinstance(public_port, int)):
            raise TypeError("Expected argument 'public_port' to be a int")
        pulumi.set(__self__, 'public_port', public_port)
        if server_port and (not isinstance(server_port, int)):
            raise TypeError("Expected argument 'server_port' to be a int")
        pulumi.set(__self__, 'server_port', server_port)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if upstream and (not isinstance(upstream, dict)):
            raise TypeError("Expected argument 'upstream' to be a dict")
        pulumi.set(__self__, 'upstream', upstream)
        if version and (not isinstance(version, str)):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def cors(self) -> Optional['outputs.SignalRCorsSettingsResponse']:
        """
        Cross-Origin Resource Sharing (CORS) settings.
        """
        return pulumi.get(self, 'cors')

    @property
    @pulumi.getter(name='externalIP')
    def external_ip(self) -> str:
        """
        The publicly accessible IP of the SignalR service.
        """
        return pulumi.get(self, 'external_ip')

    @property
    @pulumi.getter
    def features(self) -> Optional[Sequence['outputs.SignalRFeatureResponse']]:
        """
        List of SignalR featureFlags. e.g. ServiceMode.
        
        FeatureFlags that are not included in the parameters for the update operation will not be modified.
        And the response will only include featureFlags that are explicitly set. 
        When a featureFlag is not explicitly set, SignalR service will use its globally default value. 
        But keep in mind, the default value doesn't mean "false". It varies in terms of different FeatureFlags.
        """
        return pulumi.get(self, 'features')

    @property
    @pulumi.getter(name='hostName')
    def host_name(self) -> str:
        """
        FQDN of the SignalR service instance. Format: xxx.service.signalr.net
        """
        return pulumi.get(self, 'host_name')

    @property
    @pulumi.getter(name='hostNamePrefix')
    def host_name_prefix(self) -> str:
        """
        Prefix for the hostName of the SignalR service. Retained for future use.
        The hostname will be of format: &lt;hostNamePrefix&gt;.service.signalr.net.
        """
        return pulumi.get(self, 'host_name_prefix')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        The kind of the service - e.g. "SignalR", or "RawWebSockets" for "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The GEO location of the SignalR service. e.g. West US | East US | North Central US | South Central US.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='networkACLs')
    def network_acls(self) -> Optional['outputs.SignalRNetworkACLsResponse']:
        """
        Network ACLs
        """
        return pulumi.get(self, 'network_acls')

    @property
    @pulumi.getter(name='privateEndpointConnections')
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        Private endpoint connections to the SignalR resource.
        """
        return pulumi.get(self, 'private_endpoint_connections')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publicPort')
    def public_port(self) -> int:
        """
        The publicly accessible port of the SignalR service which is designed for browser/client side usage.
        """
        return pulumi.get(self, 'public_port')

    @property
    @pulumi.getter(name='serverPort')
    def server_port(self) -> int:
        """
        The publicly accessible port of the SignalR service which is designed for customer server side usage.
        """
        return pulumi.get(self, 'server_port')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ResourceSkuResponse']:
        """
        The billing information of the resource.(e.g. Free, Standard)
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def upstream(self) -> Optional['outputs.ServerlessUpstreamSettingsResponse']:
        """
        Upstream settings when the Azure SignalR is in server-less mode.
        """
        return pulumi.get(self, 'upstream')

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Version of the SignalR resource. Probably you need the same or higher version of client SDKs.
        """
        return pulumi.get(self, 'version')

class AwaitableGetSignalRResult(GetSignalRResult):

    def __await__(self):
        if False:
            yield self
        return GetSignalRResult(cors=self.cors, external_ip=self.external_ip, features=self.features, host_name=self.host_name, host_name_prefix=self.host_name_prefix, id=self.id, kind=self.kind, location=self.location, name=self.name, network_acls=self.network_acls, private_endpoint_connections=self.private_endpoint_connections, provisioning_state=self.provisioning_state, public_port=self.public_port, server_port=self.server_port, sku=self.sku, tags=self.tags, type=self.type, upstream=self.upstream, version=self.version)

def get_signal_r(resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSignalRResult:
    """
    Get the SignalR service and its properties.
    API Version: 2020-05-01.


    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str resource_name: The name of the SignalR resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:signalrservice:getSignalR', __args__, opts=opts, typ=GetSignalRResult).value
    return AwaitableGetSignalRResult(cors=__ret__.cors, external_ip=__ret__.external_ip, features=__ret__.features, host_name=__ret__.host_name, host_name_prefix=__ret__.host_name_prefix, id=__ret__.id, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, network_acls=__ret__.network_acls, private_endpoint_connections=__ret__.private_endpoint_connections, provisioning_state=__ret__.provisioning_state, public_port=__ret__.public_port, server_port=__ret__.server_port, sku=__ret__.sku, tags=__ret__.tags, type=__ret__.type, upstream=__ret__.upstream, version=__ret__.version)

@_utilities.lift_output_func(get_signal_r)
def get_signal_r_output(resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSignalRResult]:
    """
    Get the SignalR service and its properties.
    API Version: 2020-05-01.


    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str resource_name: The name of the SignalR resource.
    """
    ...