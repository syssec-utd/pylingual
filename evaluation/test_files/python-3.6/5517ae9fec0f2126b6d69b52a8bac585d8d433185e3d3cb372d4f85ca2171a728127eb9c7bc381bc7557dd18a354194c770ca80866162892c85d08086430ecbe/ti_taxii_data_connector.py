import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['TiTaxiiDataConnectorArgs', 'TiTaxiiDataConnector']

@pulumi.input_type
class TiTaxiiDataConnectorArgs:

    def __init__(__self__, *, data_types: pulumi.Input['TiTaxiiDataConnectorDataTypesArgs'], kind: pulumi.Input[str], polling_frequency: pulumi.Input[Union[str, 'PollingFrequency']], resource_group_name: pulumi.Input[str], tenant_id: pulumi.Input[str], workspace_name: pulumi.Input[str], collection_id: Optional[pulumi.Input[str]]=None, data_connector_id: Optional[pulumi.Input[str]]=None, friendly_name: Optional[pulumi.Input[str]]=None, password: Optional[pulumi.Input[str]]=None, taxii_lookback_period: Optional[pulumi.Input[str]]=None, taxii_server: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, workspace_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a TiTaxiiDataConnector resource.
        :param pulumi.Input['TiTaxiiDataConnectorDataTypesArgs'] data_types: The available data types for Threat Intelligence TAXII data connector.
        :param pulumi.Input[str] kind: The kind of the data connector
               Expected value is 'ThreatIntelligenceTaxii'.
        :param pulumi.Input[Union[str, 'PollingFrequency']] polling_frequency: The polling frequency for the TAXII server.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] tenant_id: The tenant id to connect to, and get the data from.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] collection_id: The collection id of the TAXII server.
        :param pulumi.Input[str] data_connector_id: Connector ID
        :param pulumi.Input[str] friendly_name: The friendly name for the TAXII server.
        :param pulumi.Input[str] password: The password for the TAXII server.
        :param pulumi.Input[str] taxii_lookback_period: The lookback period for the TAXII server.
        :param pulumi.Input[str] taxii_server: The API root for the TAXII server.
        :param pulumi.Input[str] user_name: The userName for the TAXII server.
        :param pulumi.Input[str] workspace_id: The workspace id.
        """
        pulumi.set(__self__, 'data_types', data_types)
        pulumi.set(__self__, 'kind', 'ThreatIntelligenceTaxii')
        pulumi.set(__self__, 'polling_frequency', polling_frequency)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'tenant_id', tenant_id)
        pulumi.set(__self__, 'workspace_name', workspace_name)
        if collection_id is not None:
            pulumi.set(__self__, 'collection_id', collection_id)
        if data_connector_id is not None:
            pulumi.set(__self__, 'data_connector_id', data_connector_id)
        if friendly_name is not None:
            pulumi.set(__self__, 'friendly_name', friendly_name)
        if password is not None:
            pulumi.set(__self__, 'password', password)
        if taxii_lookback_period is not None:
            pulumi.set(__self__, 'taxii_lookback_period', taxii_lookback_period)
        if taxii_server is not None:
            pulumi.set(__self__, 'taxii_server', taxii_server)
        if user_name is not None:
            pulumi.set(__self__, 'user_name', user_name)
        if workspace_id is not None:
            pulumi.set(__self__, 'workspace_id', workspace_id)

    @property
    @pulumi.getter(name='dataTypes')
    def data_types(self) -> pulumi.Input['TiTaxiiDataConnectorDataTypesArgs']:
        """
        The available data types for Threat Intelligence TAXII data connector.
        """
        return pulumi.get(self, 'data_types')

    @data_types.setter
    def data_types(self, value: pulumi.Input['TiTaxiiDataConnectorDataTypesArgs']):
        pulumi.set(self, 'data_types', value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the data connector
        Expected value is 'ThreatIntelligenceTaxii'.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='pollingFrequency')
    def polling_frequency(self) -> pulumi.Input[Union[str, 'PollingFrequency']]:
        """
        The polling frequency for the TAXII server.
        """
        return pulumi.get(self, 'polling_frequency')

    @polling_frequency.setter
    def polling_frequency(self, value: pulumi.Input[Union[str, 'PollingFrequency']]):
        pulumi.set(self, 'polling_frequency', value)

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
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> pulumi.Input[str]:
        """
        The tenant id to connect to, and get the data from.
        """
        return pulumi.get(self, 'tenant_id')

    @tenant_id.setter
    def tenant_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'tenant_id', value)

    @property
    @pulumi.getter(name='workspaceName')
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, 'workspace_name')

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'workspace_name', value)

    @property
    @pulumi.getter(name='collectionId')
    def collection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The collection id of the TAXII server.
        """
        return pulumi.get(self, 'collection_id')

    @collection_id.setter
    def collection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'collection_id', value)

    @property
    @pulumi.getter(name='dataConnectorId')
    def data_connector_id(self) -> Optional[pulumi.Input[str]]:
        """
        Connector ID
        """
        return pulumi.get(self, 'data_connector_id')

    @data_connector_id.setter
    def data_connector_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'data_connector_id', value)

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        The friendly name for the TAXII server.
        """
        return pulumi.get(self, 'friendly_name')

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'friendly_name', value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the TAXII server.
        """
        return pulumi.get(self, 'password')

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'password', value)

    @property
    @pulumi.getter(name='taxiiLookbackPeriod')
    def taxii_lookback_period(self) -> Optional[pulumi.Input[str]]:
        """
        The lookback period for the TAXII server.
        """
        return pulumi.get(self, 'taxii_lookback_period')

    @taxii_lookback_period.setter
    def taxii_lookback_period(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'taxii_lookback_period', value)

    @property
    @pulumi.getter(name='taxiiServer')
    def taxii_server(self) -> Optional[pulumi.Input[str]]:
        """
        The API root for the TAXII server.
        """
        return pulumi.get(self, 'taxii_server')

    @taxii_server.setter
    def taxii_server(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'taxii_server', value)

    @property
    @pulumi.getter(name='userName')
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The userName for the TAXII server.
        """
        return pulumi.get(self, 'user_name')

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_name', value)

    @property
    @pulumi.getter(name='workspaceId')
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The workspace id.
        """
        return pulumi.get(self, 'workspace_id')

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'workspace_id', value)

class TiTaxiiDataConnector(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, collection_id: Optional[pulumi.Input[str]]=None, data_connector_id: Optional[pulumi.Input[str]]=None, data_types: Optional[pulumi.Input[pulumi.InputType['TiTaxiiDataConnectorDataTypesArgs']]]=None, friendly_name: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, password: Optional[pulumi.Input[str]]=None, polling_frequency: Optional[pulumi.Input[Union[str, 'PollingFrequency']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, taxii_lookback_period: Optional[pulumi.Input[str]]=None, taxii_server: Optional[pulumi.Input[str]]=None, tenant_id: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, workspace_id: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Data connector to pull Threat intelligence data from TAXII 2.0/2.1 server

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collection_id: The collection id of the TAXII server.
        :param pulumi.Input[str] data_connector_id: Connector ID
        :param pulumi.Input[pulumi.InputType['TiTaxiiDataConnectorDataTypesArgs']] data_types: The available data types for Threat Intelligence TAXII data connector.
        :param pulumi.Input[str] friendly_name: The friendly name for the TAXII server.
        :param pulumi.Input[str] kind: The kind of the data connector
               Expected value is 'ThreatIntelligenceTaxii'.
        :param pulumi.Input[str] password: The password for the TAXII server.
        :param pulumi.Input[Union[str, 'PollingFrequency']] polling_frequency: The polling frequency for the TAXII server.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] taxii_lookback_period: The lookback period for the TAXII server.
        :param pulumi.Input[str] taxii_server: The API root for the TAXII server.
        :param pulumi.Input[str] tenant_id: The tenant id to connect to, and get the data from.
        :param pulumi.Input[str] user_name: The userName for the TAXII server.
        :param pulumi.Input[str] workspace_id: The workspace id.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: TiTaxiiDataConnectorArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Data connector to pull Threat intelligence data from TAXII 2.0/2.1 server

        :param str resource_name: The name of the resource.
        :param TiTaxiiDataConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(TiTaxiiDataConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, collection_id: Optional[pulumi.Input[str]]=None, data_connector_id: Optional[pulumi.Input[str]]=None, data_types: Optional[pulumi.Input[pulumi.InputType['TiTaxiiDataConnectorDataTypesArgs']]]=None, friendly_name: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, password: Optional[pulumi.Input[str]]=None, polling_frequency: Optional[pulumi.Input[Union[str, 'PollingFrequency']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, taxii_lookback_period: Optional[pulumi.Input[str]]=None, taxii_server: Optional[pulumi.Input[str]]=None, tenant_id: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, workspace_id: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TiTaxiiDataConnectorArgs.__new__(TiTaxiiDataConnectorArgs)
            __props__.__dict__['collection_id'] = collection_id
            __props__.__dict__['data_connector_id'] = data_connector_id
            if data_types is None and (not opts.urn):
                raise TypeError("Missing required property 'data_types'")
            __props__.__dict__['data_types'] = data_types
            __props__.__dict__['friendly_name'] = friendly_name
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = 'ThreatIntelligenceTaxii'
            __props__.__dict__['password'] = password
            if polling_frequency is None and (not opts.urn):
                raise TypeError("Missing required property 'polling_frequency'")
            __props__.__dict__['polling_frequency'] = polling_frequency
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['taxii_lookback_period'] = taxii_lookback_period
            __props__.__dict__['taxii_server'] = taxii_server
            if tenant_id is None and (not opts.urn):
                raise TypeError("Missing required property 'tenant_id'")
            __props__.__dict__['tenant_id'] = tenant_id
            __props__.__dict__['user_name'] = user_name
            __props__.__dict__['workspace_id'] = workspace_id
            if workspace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__['workspace_name'] = workspace_name
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:securityinsights:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20190101preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20200101:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20210301preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20210901preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20211001:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220101preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220401preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220501preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220601preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220701preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220801:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220801preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20220901preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20221001preview:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20221101:TiTaxiiDataConnector'), pulumi.Alias(type_='azure-native:securityinsights/v20221101preview:TiTaxiiDataConnector')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(TiTaxiiDataConnector, __self__).__init__('azure-native:securityinsights/v20211001preview:TiTaxiiDataConnector', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'TiTaxiiDataConnector':
        """
        Get an existing TiTaxiiDataConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = TiTaxiiDataConnectorArgs.__new__(TiTaxiiDataConnectorArgs)
        __props__.__dict__['collection_id'] = None
        __props__.__dict__['data_types'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['friendly_name'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['password'] = None
        __props__.__dict__['polling_frequency'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['taxii_lookback_period'] = None
        __props__.__dict__['taxii_server'] = None
        __props__.__dict__['tenant_id'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['user_name'] = None
        __props__.__dict__['workspace_id'] = None
        return TiTaxiiDataConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='collectionId')
    def collection_id(self) -> pulumi.Output[Optional[str]]:
        """
        The collection id of the TAXII server.
        """
        return pulumi.get(self, 'collection_id')

    @property
    @pulumi.getter(name='dataTypes')
    def data_types(self) -> pulumi.Output['outputs.TiTaxiiDataConnectorDataTypesResponse']:
        """
        The available data types for Threat Intelligence TAXII data connector.
        """
        return pulumi.get(self, 'data_types')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        The friendly name for the TAXII server.
        """
        return pulumi.get(self, 'friendly_name')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the data connector
        Expected value is 'ThreatIntelligenceTaxii'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password for the TAXII server.
        """
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter(name='pollingFrequency')
    def polling_frequency(self) -> pulumi.Output[str]:
        """
        The polling frequency for the TAXII server.
        """
        return pulumi.get(self, 'polling_frequency')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter(name='taxiiLookbackPeriod')
    def taxii_lookback_period(self) -> pulumi.Output[Optional[str]]:
        """
        The lookback period for the TAXII server.
        """
        return pulumi.get(self, 'taxii_lookback_period')

    @property
    @pulumi.getter(name='taxiiServer')
    def taxii_server(self) -> pulumi.Output[Optional[str]]:
        """
        The API root for the TAXII server.
        """
        return pulumi.get(self, 'taxii_server')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> pulumi.Output[str]:
        """
        The tenant id to connect to, and get the data from.
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userName')
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        The userName for the TAXII server.
        """
        return pulumi.get(self, 'user_name')

    @property
    @pulumi.getter(name='workspaceId')
    def workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        The workspace id.
        """
        return pulumi.get(self, 'workspace_id')