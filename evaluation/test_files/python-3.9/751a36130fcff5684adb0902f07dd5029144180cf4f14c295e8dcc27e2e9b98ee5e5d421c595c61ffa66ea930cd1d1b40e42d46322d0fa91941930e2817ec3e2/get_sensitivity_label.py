import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetSensitivityLabelResult', 'AwaitableGetSensitivityLabelResult', 'get_sensitivity_label', 'get_sensitivity_label_output']

@pulumi.output_type
class GetSensitivityLabelResult:
    """
    A sensitivity label.
    """

    def __init__(__self__, column_name=None, id=None, information_type=None, information_type_id=None, is_disabled=None, label_id=None, label_name=None, managed_by=None, name=None, rank=None, schema_name=None, table_name=None, type=None):
        if column_name and (not isinstance(column_name, str)):
            raise TypeError("Expected argument 'column_name' to be a str")
        pulumi.set(__self__, 'column_name', column_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if information_type and (not isinstance(information_type, str)):
            raise TypeError("Expected argument 'information_type' to be a str")
        pulumi.set(__self__, 'information_type', information_type)
        if information_type_id and (not isinstance(information_type_id, str)):
            raise TypeError("Expected argument 'information_type_id' to be a str")
        pulumi.set(__self__, 'information_type_id', information_type_id)
        if is_disabled and (not isinstance(is_disabled, bool)):
            raise TypeError("Expected argument 'is_disabled' to be a bool")
        pulumi.set(__self__, 'is_disabled', is_disabled)
        if label_id and (not isinstance(label_id, str)):
            raise TypeError("Expected argument 'label_id' to be a str")
        pulumi.set(__self__, 'label_id', label_id)
        if label_name and (not isinstance(label_name, str)):
            raise TypeError("Expected argument 'label_name' to be a str")
        pulumi.set(__self__, 'label_name', label_name)
        if managed_by and (not isinstance(managed_by, str)):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, 'managed_by', managed_by)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if rank and (not isinstance(rank, str)):
            raise TypeError("Expected argument 'rank' to be a str")
        pulumi.set(__self__, 'rank', rank)
        if schema_name and (not isinstance(schema_name, str)):
            raise TypeError("Expected argument 'schema_name' to be a str")
        pulumi.set(__self__, 'schema_name', schema_name)
        if table_name and (not isinstance(table_name, str)):
            raise TypeError("Expected argument 'table_name' to be a str")
        pulumi.set(__self__, 'table_name', table_name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='columnName')
    def column_name(self) -> str:
        """
        The column name.
        """
        return pulumi.get(self, 'column_name')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='informationType')
    def information_type(self) -> Optional[str]:
        """
        The information type.
        """
        return pulumi.get(self, 'information_type')

    @property
    @pulumi.getter(name='informationTypeId')
    def information_type_id(self) -> Optional[str]:
        """
        The information type ID.
        """
        return pulumi.get(self, 'information_type_id')

    @property
    @pulumi.getter(name='isDisabled')
    def is_disabled(self) -> bool:
        """
        Is sensitivity recommendation disabled. Applicable for recommended sensitivity label only. Specifies whether the sensitivity recommendation on this column is disabled (dismissed) or not.
        """
        return pulumi.get(self, 'is_disabled')

    @property
    @pulumi.getter(name='labelId')
    def label_id(self) -> Optional[str]:
        """
        The label ID.
        """
        return pulumi.get(self, 'label_id')

    @property
    @pulumi.getter(name='labelName')
    def label_name(self) -> Optional[str]:
        """
        The label name.
        """
        return pulumi.get(self, 'label_name')

    @property
    @pulumi.getter(name='managedBy')
    def managed_by(self) -> str:
        """
        Resource that manages the sensitivity label.
        """
        return pulumi.get(self, 'managed_by')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def rank(self) -> Optional[str]:
        return pulumi.get(self, 'rank')

    @property
    @pulumi.getter(name='schemaName')
    def schema_name(self) -> str:
        """
        The schema name.
        """
        return pulumi.get(self, 'schema_name')

    @property
    @pulumi.getter(name='tableName')
    def table_name(self) -> str:
        """
        The table name.
        """
        return pulumi.get(self, 'table_name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetSensitivityLabelResult(GetSensitivityLabelResult):

    def __await__(self):
        if False:
            yield self
        return GetSensitivityLabelResult(column_name=self.column_name, id=self.id, information_type=self.information_type, information_type_id=self.information_type_id, is_disabled=self.is_disabled, label_id=self.label_id, label_name=self.label_name, managed_by=self.managed_by, name=self.name, rank=self.rank, schema_name=self.schema_name, table_name=self.table_name, type=self.type)

def get_sensitivity_label(column_name: Optional[str]=None, database_name: Optional[str]=None, resource_group_name: Optional[str]=None, schema_name: Optional[str]=None, sensitivity_label_source: Optional[str]=None, server_name: Optional[str]=None, table_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSensitivityLabelResult:
    """
    Gets the sensitivity label of a given column


    :param str column_name: The name of the column.
    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str schema_name: The name of the schema.
    :param str sensitivity_label_source: The source of the sensitivity label.
    :param str server_name: The name of the server.
    :param str table_name: The name of the table.
    """
    __args__ = dict()
    __args__['columnName'] = column_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['schemaName'] = schema_name
    __args__['sensitivityLabelSource'] = sensitivity_label_source
    __args__['serverName'] = server_name
    __args__['tableName'] = table_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20200202preview:getSensitivityLabel', __args__, opts=opts, typ=GetSensitivityLabelResult).value
    return AwaitableGetSensitivityLabelResult(column_name=__ret__.column_name, id=__ret__.id, information_type=__ret__.information_type, information_type_id=__ret__.information_type_id, is_disabled=__ret__.is_disabled, label_id=__ret__.label_id, label_name=__ret__.label_name, managed_by=__ret__.managed_by, name=__ret__.name, rank=__ret__.rank, schema_name=__ret__.schema_name, table_name=__ret__.table_name, type=__ret__.type)

@_utilities.lift_output_func(get_sensitivity_label)
def get_sensitivity_label_output(column_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, schema_name: Optional[pulumi.Input[str]]=None, sensitivity_label_source: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, table_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSensitivityLabelResult]:
    """
    Gets the sensitivity label of a given column


    :param str column_name: The name of the column.
    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str schema_name: The name of the schema.
    :param str sensitivity_label_source: The source of the sensitivity label.
    :param str server_name: The name of the server.
    :param str table_name: The name of the table.
    """
    ...