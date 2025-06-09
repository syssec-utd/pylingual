import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetAwsS3DataConnectorResult', 'AwaitableGetAwsS3DataConnectorResult', 'get_aws_s3_data_connector', 'get_aws_s3_data_connector_output']

@pulumi.output_type
class GetAwsS3DataConnectorResult:
    """
    Represents Amazon Web Services S3 data connector.
    """

    def __init__(__self__, data_types=None, destination_table=None, etag=None, id=None, kind=None, name=None, role_arn=None, sqs_urls=None, system_data=None, type=None):
        if data_types and (not isinstance(data_types, dict)):
            raise TypeError("Expected argument 'data_types' to be a dict")
        pulumi.set(__self__, 'data_types', data_types)
        if destination_table and (not isinstance(destination_table, str)):
            raise TypeError("Expected argument 'destination_table' to be a str")
        pulumi.set(__self__, 'destination_table', destination_table)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if role_arn and (not isinstance(role_arn, str)):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, 'role_arn', role_arn)
        if sqs_urls and (not isinstance(sqs_urls, list)):
            raise TypeError("Expected argument 'sqs_urls' to be a list")
        pulumi.set(__self__, 'sqs_urls', sqs_urls)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='dataTypes')
    def data_types(self) -> 'outputs.AwsS3DataConnectorDataTypesResponse':
        """
        The available data types for the connector.
        """
        return pulumi.get(self, 'data_types')

    @property
    @pulumi.getter(name='destinationTable')
    def destination_table(self) -> str:
        """
        The logs destination table name in LogAnalytics.
        """
        return pulumi.get(self, 'destination_table')

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the data connector
        Expected value is 'AmazonWebServicesS3'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='roleArn')
    def role_arn(self) -> str:
        """
        The Aws Role Arn that is used to access the Aws account.
        """
        return pulumi.get(self, 'role_arn')

    @property
    @pulumi.getter(name='sqsUrls')
    def sqs_urls(self) -> Sequence[str]:
        """
        The AWS sqs urls for the connector.
        """
        return pulumi.get(self, 'sqs_urls')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetAwsS3DataConnectorResult(GetAwsS3DataConnectorResult):

    def __await__(self):
        if False:
            yield self
        return GetAwsS3DataConnectorResult(data_types=self.data_types, destination_table=self.destination_table, etag=self.etag, id=self.id, kind=self.kind, name=self.name, role_arn=self.role_arn, sqs_urls=self.sqs_urls, system_data=self.system_data, type=self.type)

def get_aws_s3_data_connector(data_connector_id: Optional[str]=None, resource_group_name: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetAwsS3DataConnectorResult:
    """
    Represents Amazon Web Services S3 data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['dataConnectorId'] = data_connector_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20211001preview:getAwsS3DataConnector', __args__, opts=opts, typ=GetAwsS3DataConnectorResult).value
    return AwaitableGetAwsS3DataConnectorResult(data_types=__ret__.data_types, destination_table=__ret__.destination_table, etag=__ret__.etag, id=__ret__.id, kind=__ret__.kind, name=__ret__.name, role_arn=__ret__.role_arn, sqs_urls=__ret__.sqs_urls, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_aws_s3_data_connector)
def get_aws_s3_data_connector_output(data_connector_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetAwsS3DataConnectorResult]:
    """
    Represents Amazon Web Services S3 data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...