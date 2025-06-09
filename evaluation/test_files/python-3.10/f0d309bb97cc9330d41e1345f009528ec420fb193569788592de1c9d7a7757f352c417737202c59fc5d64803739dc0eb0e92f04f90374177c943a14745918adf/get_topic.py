import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetTopicResult', 'AwaitableGetTopicResult', 'get_topic', 'get_topic_output']

@pulumi.output_type
class GetTopicResult:
    """
    EventGrid Topic
    """

    def __init__(__self__, disable_local_auth=None, endpoint=None, id=None, identity=None, inbound_ip_rules=None, input_schema=None, input_schema_mapping=None, location=None, metric_resource_id=None, name=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, system_data=None, tags=None, type=None):
        if disable_local_auth and (not isinstance(disable_local_auth, bool)):
            raise TypeError("Expected argument 'disable_local_auth' to be a bool")
        pulumi.set(__self__, 'disable_local_auth', disable_local_auth)
        if endpoint and (not isinstance(endpoint, str)):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, 'endpoint', endpoint)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
        if inbound_ip_rules and (not isinstance(inbound_ip_rules, list)):
            raise TypeError("Expected argument 'inbound_ip_rules' to be a list")
        pulumi.set(__self__, 'inbound_ip_rules', inbound_ip_rules)
        if input_schema and (not isinstance(input_schema, str)):
            raise TypeError("Expected argument 'input_schema' to be a str")
        pulumi.set(__self__, 'input_schema', input_schema)
        if input_schema_mapping and (not isinstance(input_schema_mapping, dict)):
            raise TypeError("Expected argument 'input_schema_mapping' to be a dict")
        pulumi.set(__self__, 'input_schema_mapping', input_schema_mapping)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if metric_resource_id and (not isinstance(metric_resource_id, str)):
            raise TypeError("Expected argument 'metric_resource_id' to be a str")
        pulumi.set(__self__, 'metric_resource_id', metric_resource_id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if private_endpoint_connections and (not isinstance(private_endpoint_connections, list)):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, 'private_endpoint_connections', private_endpoint_connections)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if public_network_access and (not isinstance(public_network_access, str)):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, 'public_network_access', public_network_access)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='disableLocalAuth')
    def disable_local_auth(self) -> Optional[bool]:
        """
        This boolean is used to enable or disable local auth. Default value is false. When the property is set to true, only AAD token will be used to authenticate if user is allowed to publish to the topic.
        """
        return pulumi.get(self, 'disable_local_auth')

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        Endpoint for the topic.
        """
        return pulumi.get(self, 'endpoint')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityInfoResponse']:
        """
        Identity information for the resource.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='inboundIpRules')
    def inbound_ip_rules(self) -> Optional[Sequence['outputs.InboundIpRuleResponse']]:
        """
        This can be used to restrict traffic from specific IPs instead of all IPs. Note: These are considered only if PublicNetworkAccess is enabled.
        """
        return pulumi.get(self, 'inbound_ip_rules')

    @property
    @pulumi.getter(name='inputSchema')
    def input_schema(self) -> Optional[str]:
        """
        This determines the format that Event Grid should expect for incoming events published to the topic.
        """
        return pulumi.get(self, 'input_schema')

    @property
    @pulumi.getter(name='inputSchemaMapping')
    def input_schema_mapping(self) -> Optional['outputs.JsonInputSchemaMappingResponse']:
        """
        This enables publishing using custom event schemas. An InputSchemaMapping can be specified to map various properties of a source schema to various required properties of the EventGridEvent schema.
        """
        return pulumi.get(self, 'input_schema_mapping')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location of the resource.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='metricResourceId')
    def metric_resource_id(self) -> str:
        """
        Metric resource id for the topic.
        """
        return pulumi.get(self, 'metric_resource_id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpointConnections')
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        return pulumi.get(self, 'private_endpoint_connections')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the topic.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publicNetworkAccess')
    def public_network_access(self) -> Optional[str]:
        """
        This determines if traffic is allowed over public network. By default it is enabled. 
        You can further restrict to specific IPs by configuring <seealso cref="P:Microsoft.Azure.Events.ResourceProvider.Common.Contracts.TopicProperties.InboundIpRules" />
        """
        return pulumi.get(self, 'public_network_access')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to Topic resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags of the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, 'type')

class AwaitableGetTopicResult(GetTopicResult):

    def __await__(self):
        if False:
            yield self
        return GetTopicResult(disable_local_auth=self.disable_local_auth, endpoint=self.endpoint, id=self.id, identity=self.identity, inbound_ip_rules=self.inbound_ip_rules, input_schema=self.input_schema, input_schema_mapping=self.input_schema_mapping, location=self.location, metric_resource_id=self.metric_resource_id, name=self.name, private_endpoint_connections=self.private_endpoint_connections, provisioning_state=self.provisioning_state, public_network_access=self.public_network_access, system_data=self.system_data, tags=self.tags, type=self.type)

def get_topic(resource_group_name: Optional[str]=None, topic_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetTopicResult:
    """
    EventGrid Topic


    :param str resource_group_name: The name of the resource group within the user's subscription.
    :param str topic_name: Name of the topic.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['topicName'] = topic_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid/v20211201:getTopic', __args__, opts=opts, typ=GetTopicResult).value
    return AwaitableGetTopicResult(disable_local_auth=__ret__.disable_local_auth, endpoint=__ret__.endpoint, id=__ret__.id, identity=__ret__.identity, inbound_ip_rules=__ret__.inbound_ip_rules, input_schema=__ret__.input_schema, input_schema_mapping=__ret__.input_schema_mapping, location=__ret__.location, metric_resource_id=__ret__.metric_resource_id, name=__ret__.name, private_endpoint_connections=__ret__.private_endpoint_connections, provisioning_state=__ret__.provisioning_state, public_network_access=__ret__.public_network_access, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_topic)
def get_topic_output(resource_group_name: Optional[pulumi.Input[str]]=None, topic_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetTopicResult]:
    """
    EventGrid Topic


    :param str resource_group_name: The name of the resource group within the user's subscription.
    :param str topic_name: Name of the topic.
    """
    ...