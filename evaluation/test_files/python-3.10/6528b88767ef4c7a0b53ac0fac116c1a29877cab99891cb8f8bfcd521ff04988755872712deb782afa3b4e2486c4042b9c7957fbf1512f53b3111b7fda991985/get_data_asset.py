import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetDataAssetResult', 'AwaitableGetDataAssetResult', 'get_data_asset', 'get_data_asset_output']

@pulumi.output_type
class GetDataAssetResult:
    """
    A collection of values returned by getDataAsset.
    """

    def __init__(__self__, catalog_id=None, created_by_id=None, data_asset_key=None, description=None, display_name=None, external_key=None, fields=None, id=None, key=None, properties=None, state=None, time_created=None, time_harvested=None, time_updated=None, type_key=None, updated_by_id=None, uri=None):
        if catalog_id and (not isinstance(catalog_id, str)):
            raise TypeError("Expected argument 'catalog_id' to be a str")
        pulumi.set(__self__, 'catalog_id', catalog_id)
        if created_by_id and (not isinstance(created_by_id, str)):
            raise TypeError("Expected argument 'created_by_id' to be a str")
        pulumi.set(__self__, 'created_by_id', created_by_id)
        if data_asset_key and (not isinstance(data_asset_key, str)):
            raise TypeError("Expected argument 'data_asset_key' to be a str")
        pulumi.set(__self__, 'data_asset_key', data_asset_key)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if external_key and (not isinstance(external_key, str)):
            raise TypeError("Expected argument 'external_key' to be a str")
        pulumi.set(__self__, 'external_key', external_key)
        if fields and (not isinstance(fields, list)):
            raise TypeError("Expected argument 'fields' to be a list")
        pulumi.set(__self__, 'fields', fields)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if key and (not isinstance(key, str)):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, 'key', key)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if time_created and (not isinstance(time_created, str)):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, 'time_created', time_created)
        if time_harvested and (not isinstance(time_harvested, str)):
            raise TypeError("Expected argument 'time_harvested' to be a str")
        pulumi.set(__self__, 'time_harvested', time_harvested)
        if time_updated and (not isinstance(time_updated, str)):
            raise TypeError("Expected argument 'time_updated' to be a str")
        pulumi.set(__self__, 'time_updated', time_updated)
        if type_key and (not isinstance(type_key, str)):
            raise TypeError("Expected argument 'type_key' to be a str")
        pulumi.set(__self__, 'type_key', type_key)
        if updated_by_id and (not isinstance(updated_by_id, str)):
            raise TypeError("Expected argument 'updated_by_id' to be a str")
        pulumi.set(__self__, 'updated_by_id', updated_by_id)
        if uri and (not isinstance(uri, str)):
            raise TypeError("Expected argument 'uri' to be a str")
        pulumi.set(__self__, 'uri', uri)

    @property
    @pulumi.getter(name='catalogId')
    def catalog_id(self) -> str:
        """
        The data catalog's OCID.
        """
        return pulumi.get(self, 'catalog_id')

    @property
    @pulumi.getter(name='createdById')
    def created_by_id(self) -> str:
        """
        OCID of the user who created the data asset.
        """
        return pulumi.get(self, 'created_by_id')

    @property
    @pulumi.getter(name='dataAssetKey')
    def data_asset_key(self) -> str:
        return pulumi.get(self, 'data_asset_key')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Detailed description of the data asset.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        A user-friendly display name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='externalKey')
    def external_key(self) -> str:
        """
        External URI that can be used to reference the object. Format will differ based on the type of object.
        """
        return pulumi.get(self, 'external_key')

    @property
    @pulumi.getter
    def fields(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, 'fields')

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Unique data asset key that is immutable.
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, Any]:
        """
        A map of maps that contains the properties which are specific to the asset type. Each data asset type definition defines it's set of required and optional properties. The map keys are category names and the values are maps of property name to property value. Every property is contained inside of a category. Most data assets have required properties within the "default" category. Example: `{"properties": { "default": { "host": "host1", "port": "1521", "database": "orcl"}}}`
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the data asset.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> str:
        """
        The date and time the data asset was created, in the format defined by [RFC3339](https://tools.ietf.org/html/rfc3339). Example: `2019-03-25T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='timeHarvested')
    def time_harvested(self) -> str:
        """
        The last time that a harvest was performed on the data asset. An [RFC3339](https://tools.ietf.org/html/rfc3339) formatted datetime string.
        """
        return pulumi.get(self, 'time_harvested')

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> str:
        """
        The last time that any change was made to the data asset. An [RFC3339](https://tools.ietf.org/html/rfc3339) formatted datetime string.
        """
        return pulumi.get(self, 'time_updated')

    @property
    @pulumi.getter(name='typeKey')
    def type_key(self) -> str:
        """
        The key of the object type. Type key's can be found via the '/types' endpoint.
        """
        return pulumi.get(self, 'type_key')

    @property
    @pulumi.getter(name='updatedById')
    def updated_by_id(self) -> str:
        """
        OCID of the user who last modified the data asset.
        """
        return pulumi.get(self, 'updated_by_id')

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        URI to the data asset instance in the API.
        """
        return pulumi.get(self, 'uri')

class AwaitableGetDataAssetResult(GetDataAssetResult):

    def __await__(self):
        if False:
            yield self
        return GetDataAssetResult(catalog_id=self.catalog_id, created_by_id=self.created_by_id, data_asset_key=self.data_asset_key, description=self.description, display_name=self.display_name, external_key=self.external_key, fields=self.fields, id=self.id, key=self.key, properties=self.properties, state=self.state, time_created=self.time_created, time_harvested=self.time_harvested, time_updated=self.time_updated, type_key=self.type_key, updated_by_id=self.updated_by_id, uri=self.uri)

def get_data_asset(catalog_id: Optional[str]=None, data_asset_key: Optional[str]=None, fields: Optional[Sequence[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDataAssetResult:
    """
    This data source provides details about a specific Data Asset resource in Oracle Cloud Infrastructure Data Catalog service.

    Gets a specific data asset for the given key within a data catalog.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_data_asset = oci.DataCatalog.get_data_asset(catalog_id=oci_datacatalog_catalog["test_catalog"]["id"],
        data_asset_key=var["data_asset_data_asset_key"],
        fields=var["data_asset_fields"])
    ```


    :param str catalog_id: Unique catalog identifier.
    :param str data_asset_key: Unique data asset key.
    :param Sequence[str] fields: Specifies the fields to return in a data asset response.
    """
    __args__ = dict()
    __args__['catalogId'] = catalog_id
    __args__['dataAssetKey'] = data_asset_key
    __args__['fields'] = fields
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:DataCatalog/getDataAsset:getDataAsset', __args__, opts=opts, typ=GetDataAssetResult).value
    return AwaitableGetDataAssetResult(catalog_id=__ret__.catalog_id, created_by_id=__ret__.created_by_id, data_asset_key=__ret__.data_asset_key, description=__ret__.description, display_name=__ret__.display_name, external_key=__ret__.external_key, fields=__ret__.fields, id=__ret__.id, key=__ret__.key, properties=__ret__.properties, state=__ret__.state, time_created=__ret__.time_created, time_harvested=__ret__.time_harvested, time_updated=__ret__.time_updated, type_key=__ret__.type_key, updated_by_id=__ret__.updated_by_id, uri=__ret__.uri)

@_utilities.lift_output_func(get_data_asset)
def get_data_asset_output(catalog_id: Optional[pulumi.Input[str]]=None, data_asset_key: Optional[pulumi.Input[str]]=None, fields: Optional[pulumi.Input[Optional[Sequence[str]]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDataAssetResult]:
    """
    This data source provides details about a specific Data Asset resource in Oracle Cloud Infrastructure Data Catalog service.

    Gets a specific data asset for the given key within a data catalog.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_data_asset = oci.DataCatalog.get_data_asset(catalog_id=oci_datacatalog_catalog["test_catalog"]["id"],
        data_asset_key=var["data_asset_data_asset_key"],
        fields=var["data_asset_fields"])
    ```


    :param str catalog_id: Unique catalog identifier.
    :param str data_asset_key: Unique data asset key.
    :param Sequence[str] fields: Specifies the fields to return in a data asset response.
    """
    ...