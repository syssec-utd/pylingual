import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['DatabaseToolsConnectionArgs', 'DatabaseToolsConnection']

@pulumi.input_type
class DatabaseToolsConnectionArgs:

    def __init__(__self__, *, compartment_id: pulumi.Input[str], display_name: pulumi.Input[str], type: pulumi.Input[str], advanced_properties: Optional[pulumi.Input[Mapping[str, Any]]]=None, connection_string: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, key_stores: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, related_resource: Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]=None, user_name: Optional[pulumi.Input[str]]=None, user_password: Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]=None):
        """
        The set of arguments for constructing a DatabaseToolsConnection resource.
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        :param pulumi.Input[str] display_name: (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        :param pulumi.Input[str] type: (Updatable) The DatabaseToolsConnection type.
        :param pulumi.Input[Mapping[str, Any]] advanced_properties: (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        :param pulumi.Input[str] connection_string: (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        :param pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]] key_stores: (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        :param pulumi.Input[str] private_endpoint_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        :param pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs'] related_resource: (Updatable) The related resource
        :param pulumi.Input[str] user_name: (Updatable) The database user name.
        :param pulumi.Input['DatabaseToolsConnectionUserPasswordArgs'] user_password: (Updatable) The user password.
        """
        pulumi.set(__self__, 'compartment_id', compartment_id)
        pulumi.set(__self__, 'display_name', display_name)
        pulumi.set(__self__, 'type', type)
        if advanced_properties is not None:
            pulumi.set(__self__, 'advanced_properties', advanced_properties)
        if connection_string is not None:
            pulumi.set(__self__, 'connection_string', connection_string)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if key_stores is not None:
            pulumi.set(__self__, 'key_stores', key_stores)
        if private_endpoint_id is not None:
            pulumi.set(__self__, 'private_endpoint_id', private_endpoint_id)
        if related_resource is not None:
            pulumi.set(__self__, 'related_resource', related_resource)
        if user_name is not None:
            pulumi.set(__self__, 'user_name', user_name)
        if user_password is not None:
            pulumi.set(__self__, 'user_password', user_password)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Input[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        (Updatable) The DatabaseToolsConnection type.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='advancedProperties')
    def advanced_properties(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        """
        return pulumi.get(self, 'advanced_properties')

    @advanced_properties.setter
    def advanced_properties(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'advanced_properties', value)

    @property
    @pulumi.getter(name='connectionString')
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        """
        return pulumi.get(self, 'connection_string')

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'connection_string', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='keyStores')
    def key_stores(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]:
        """
        (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        """
        return pulumi.get(self, 'key_stores')

    @key_stores.setter
    def key_stores(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]):
        pulumi.set(self, 'key_stores', value)

    @property
    @pulumi.getter(name='privateEndpointId')
    def private_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        """
        return pulumi.get(self, 'private_endpoint_id')

    @private_endpoint_id.setter
    def private_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_id', value)

    @property
    @pulumi.getter(name='relatedResource')
    def related_resource(self) -> Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]:
        """
        (Updatable) The related resource
        """
        return pulumi.get(self, 'related_resource')

    @related_resource.setter
    def related_resource(self, value: Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]):
        pulumi.set(self, 'related_resource', value)

    @property
    @pulumi.getter(name='userName')
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The database user name.
        """
        return pulumi.get(self, 'user_name')

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_name', value)

    @property
    @pulumi.getter(name='userPassword')
    def user_password(self) -> Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]:
        """
        (Updatable) The user password.
        """
        return pulumi.get(self, 'user_password')

    @user_password.setter
    def user_password(self, value: Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]):
        pulumi.set(self, 'user_password', value)

@pulumi.input_type
class _DatabaseToolsConnectionState:

    def __init__(__self__, *, advanced_properties: Optional[pulumi.Input[Mapping[str, Any]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, connection_string: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, key_stores: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]=None, lifecycle_details: Optional[pulumi.Input[str]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, related_resource: Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]=None, state: Optional[pulumi.Input[str]]=None, system_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, time_created: Optional[pulumi.Input[str]]=None, time_updated: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, user_password: Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]=None):
        """
        Input properties used for looking up and filtering DatabaseToolsConnection resources.
        :param pulumi.Input[Mapping[str, Any]] advanced_properties: (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        :param pulumi.Input[str] connection_string: (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        :param pulumi.Input[str] display_name: (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        :param pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]] key_stores: (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        :param pulumi.Input[str] lifecycle_details: A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.
        :param pulumi.Input[str] private_endpoint_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        :param pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs'] related_resource: (Updatable) The related resource
        :param pulumi.Input[str] state: The current state of the Database Tools connection.
        :param pulumi.Input[Mapping[str, Any]] system_tags: Usage of system tag keys. These predefined keys are scoped to namespaces. Example: `{"orcl-cloud.free-tier-retained": "true"}`
        :param pulumi.Input[str] time_created: The time the Database Tools connection was created. An RFC3339 formatted datetime string.
        :param pulumi.Input[str] time_updated: The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.
        :param pulumi.Input[str] type: (Updatable) The DatabaseToolsConnection type.
        :param pulumi.Input[str] user_name: (Updatable) The database user name.
        :param pulumi.Input['DatabaseToolsConnectionUserPasswordArgs'] user_password: (Updatable) The user password.
        """
        if advanced_properties is not None:
            pulumi.set(__self__, 'advanced_properties', advanced_properties)
        if compartment_id is not None:
            pulumi.set(__self__, 'compartment_id', compartment_id)
        if connection_string is not None:
            pulumi.set(__self__, 'connection_string', connection_string)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if key_stores is not None:
            pulumi.set(__self__, 'key_stores', key_stores)
        if lifecycle_details is not None:
            pulumi.set(__self__, 'lifecycle_details', lifecycle_details)
        if private_endpoint_id is not None:
            pulumi.set(__self__, 'private_endpoint_id', private_endpoint_id)
        if related_resource is not None:
            pulumi.set(__self__, 'related_resource', related_resource)
        if state is not None:
            pulumi.set(__self__, 'state', state)
        if system_tags is not None:
            pulumi.set(__self__, 'system_tags', system_tags)
        if time_created is not None:
            pulumi.set(__self__, 'time_created', time_created)
        if time_updated is not None:
            pulumi.set(__self__, 'time_updated', time_updated)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if user_name is not None:
            pulumi.set(__self__, 'user_name', user_name)
        if user_password is not None:
            pulumi.set(__self__, 'user_password', user_password)

    @property
    @pulumi.getter(name='advancedProperties')
    def advanced_properties(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        """
        return pulumi.get(self, 'advanced_properties')

    @advanced_properties.setter
    def advanced_properties(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'advanced_properties', value)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter(name='connectionString')
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        """
        return pulumi.get(self, 'connection_string')

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'connection_string', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='keyStores')
    def key_stores(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]:
        """
        (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        """
        return pulumi.get(self, 'key_stores')

    @key_stores.setter
    def key_stores(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseToolsConnectionKeyStoreArgs']]]]):
        pulumi.set(self, 'key_stores', value)

    @property
    @pulumi.getter(name='lifecycleDetails')
    def lifecycle_details(self) -> Optional[pulumi.Input[str]]:
        """
        A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.
        """
        return pulumi.get(self, 'lifecycle_details')

    @lifecycle_details.setter
    def lifecycle_details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'lifecycle_details', value)

    @property
    @pulumi.getter(name='privateEndpointId')
    def private_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        """
        return pulumi.get(self, 'private_endpoint_id')

    @private_endpoint_id.setter
    def private_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_id', value)

    @property
    @pulumi.getter(name='relatedResource')
    def related_resource(self) -> Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]:
        """
        (Updatable) The related resource
        """
        return pulumi.get(self, 'related_resource')

    @related_resource.setter
    def related_resource(self, value: Optional[pulumi.Input['DatabaseToolsConnectionRelatedResourceArgs']]):
        pulumi.set(self, 'related_resource', value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the Database Tools connection.
        """
        return pulumi.get(self, 'state')

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'state', value)

    @property
    @pulumi.getter(name='systemTags')
    def system_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Usage of system tag keys. These predefined keys are scoped to namespaces. Example: `{"orcl-cloud.free-tier-retained": "true"}`
        """
        return pulumi.get(self, 'system_tags')

    @system_tags.setter
    def system_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'system_tags', value)

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> Optional[pulumi.Input[str]]:
        """
        The time the Database Tools connection was created. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_created')

    @time_created.setter
    def time_created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'time_created', value)

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> Optional[pulumi.Input[str]]:
        """
        The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_updated')

    @time_updated.setter
    def time_updated(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'time_updated', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The DatabaseToolsConnection type.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='userName')
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The database user name.
        """
        return pulumi.get(self, 'user_name')

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_name', value)

    @property
    @pulumi.getter(name='userPassword')
    def user_password(self) -> Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]:
        """
        (Updatable) The user password.
        """
        return pulumi.get(self, 'user_password')

    @user_password.setter
    def user_password(self, value: Optional[pulumi.Input['DatabaseToolsConnectionUserPasswordArgs']]):
        pulumi.set(self, 'user_password', value)

class DatabaseToolsConnection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, advanced_properties: Optional[pulumi.Input[Mapping[str, Any]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, connection_string: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, key_stores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionKeyStoreArgs']]]]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, related_resource: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionRelatedResourceArgs']]]=None, type: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, user_password: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionUserPasswordArgs']]]=None, __props__=None):
        """
        This resource provides the Database Tools Connection resource in Oracle Cloud Infrastructure Database Tools service.

        Creates a new Database Tools connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_database_tools_connection = oci.database_tools.DatabaseToolsConnection("testDatabaseToolsConnection",
            compartment_id=var["compartment_id"],
            display_name=var["database_tools_connection_display_name"],
            type=var["database_tools_connection_type"],
            advanced_properties=var["database_tools_connection_advanced_properties"],
            connection_string=var["database_tools_connection_connection_string"],
            defined_tags={
                "foo-namespace.bar-key": "value",
            },
            freeform_tags={
                "bar-key": "value",
            },
            key_stores=[oci.database_tools.DatabaseToolsConnectionKeyStoreArgs(
                key_store_content=oci.database_tools.DatabaseToolsConnectionKeyStoreKeyStoreContentArgs(
                    value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                    secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                ),
                key_store_password=oci.database_tools.DatabaseToolsConnectionKeyStoreKeyStorePasswordArgs(
                    value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                    secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                ),
                key_store_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            )],
            private_endpoint_id=oci_dataflow_private_endpoint["test_private_endpoint"]["id"],
            related_resource=oci.database_tools.DatabaseToolsConnectionRelatedResourceArgs(
                entity_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                identifier=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            user_name=oci_identity_user["test_user"]["name"],
            user_password=oci.database_tools.DatabaseToolsConnectionUserPasswordArgs(
                secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ))
        ```

        ## Import

        DatabaseToolsConnections can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:DatabaseTools/databaseToolsConnection:DatabaseToolsConnection test_database_tools_connection "id"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] advanced_properties: (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        :param pulumi.Input[str] connection_string: (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        :param pulumi.Input[str] display_name: (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionKeyStoreArgs']]]] key_stores: (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        :param pulumi.Input[str] private_endpoint_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        :param pulumi.Input[pulumi.InputType['DatabaseToolsConnectionRelatedResourceArgs']] related_resource: (Updatable) The related resource
        :param pulumi.Input[str] type: (Updatable) The DatabaseToolsConnection type.
        :param pulumi.Input[str] user_name: (Updatable) The database user name.
        :param pulumi.Input[pulumi.InputType['DatabaseToolsConnectionUserPasswordArgs']] user_password: (Updatable) The user password.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DatabaseToolsConnectionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        This resource provides the Database Tools Connection resource in Oracle Cloud Infrastructure Database Tools service.

        Creates a new Database Tools connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_database_tools_connection = oci.database_tools.DatabaseToolsConnection("testDatabaseToolsConnection",
            compartment_id=var["compartment_id"],
            display_name=var["database_tools_connection_display_name"],
            type=var["database_tools_connection_type"],
            advanced_properties=var["database_tools_connection_advanced_properties"],
            connection_string=var["database_tools_connection_connection_string"],
            defined_tags={
                "foo-namespace.bar-key": "value",
            },
            freeform_tags={
                "bar-key": "value",
            },
            key_stores=[oci.database_tools.DatabaseToolsConnectionKeyStoreArgs(
                key_store_content=oci.database_tools.DatabaseToolsConnectionKeyStoreKeyStoreContentArgs(
                    value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                    secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                ),
                key_store_password=oci.database_tools.DatabaseToolsConnectionKeyStoreKeyStorePasswordArgs(
                    value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                    secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                ),
                key_store_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            )],
            private_endpoint_id=oci_dataflow_private_endpoint["test_private_endpoint"]["id"],
            related_resource=oci.database_tools.DatabaseToolsConnectionRelatedResourceArgs(
                entity_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                identifier=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            user_name=oci_identity_user["test_user"]["name"],
            user_password=oci.database_tools.DatabaseToolsConnectionUserPasswordArgs(
                secret_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                value_type=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ))
        ```

        ## Import

        DatabaseToolsConnections can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:DatabaseTools/databaseToolsConnection:DatabaseToolsConnection test_database_tools_connection "id"
        ```

        :param str resource_name: The name of the resource.
        :param DatabaseToolsConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(DatabaseToolsConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, advanced_properties: Optional[pulumi.Input[Mapping[str, Any]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, connection_string: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, key_stores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionKeyStoreArgs']]]]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, related_resource: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionRelatedResourceArgs']]]=None, type: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, user_password: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionUserPasswordArgs']]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseToolsConnectionArgs.__new__(DatabaseToolsConnectionArgs)
            __props__.__dict__['advanced_properties'] = advanced_properties
            if compartment_id is None and (not opts.urn):
                raise TypeError("Missing required property 'compartment_id'")
            __props__.__dict__['compartment_id'] = compartment_id
            __props__.__dict__['connection_string'] = connection_string
            __props__.__dict__['defined_tags'] = defined_tags
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['freeform_tags'] = freeform_tags
            __props__.__dict__['key_stores'] = key_stores
            __props__.__dict__['private_endpoint_id'] = private_endpoint_id
            __props__.__dict__['related_resource'] = related_resource
            if type is None and (not opts.urn):
                raise TypeError("Missing required property 'type'")
            __props__.__dict__['type'] = type
            __props__.__dict__['user_name'] = user_name
            __props__.__dict__['user_password'] = user_password
            __props__.__dict__['lifecycle_details'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['system_tags'] = None
            __props__.__dict__['time_created'] = None
            __props__.__dict__['time_updated'] = None
        super(DatabaseToolsConnection, __self__).__init__('oci:DatabaseTools/databaseToolsConnection:DatabaseToolsConnection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, advanced_properties: Optional[pulumi.Input[Mapping[str, Any]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, connection_string: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, key_stores: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionKeyStoreArgs']]]]]=None, lifecycle_details: Optional[pulumi.Input[str]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, related_resource: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionRelatedResourceArgs']]]=None, state: Optional[pulumi.Input[str]]=None, system_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, time_created: Optional[pulumi.Input[str]]=None, time_updated: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None, user_name: Optional[pulumi.Input[str]]=None, user_password: Optional[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionUserPasswordArgs']]]=None) -> 'DatabaseToolsConnection':
        """
        Get an existing DatabaseToolsConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] advanced_properties: (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        :param pulumi.Input[str] compartment_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        :param pulumi.Input[str] connection_string: (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        :param pulumi.Input[str] display_name: (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseToolsConnectionKeyStoreArgs']]]] key_stores: (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        :param pulumi.Input[str] lifecycle_details: A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.
        :param pulumi.Input[str] private_endpoint_id: (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        :param pulumi.Input[pulumi.InputType['DatabaseToolsConnectionRelatedResourceArgs']] related_resource: (Updatable) The related resource
        :param pulumi.Input[str] state: The current state of the Database Tools connection.
        :param pulumi.Input[Mapping[str, Any]] system_tags: Usage of system tag keys. These predefined keys are scoped to namespaces. Example: `{"orcl-cloud.free-tier-retained": "true"}`
        :param pulumi.Input[str] time_created: The time the Database Tools connection was created. An RFC3339 formatted datetime string.
        :param pulumi.Input[str] time_updated: The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.
        :param pulumi.Input[str] type: (Updatable) The DatabaseToolsConnection type.
        :param pulumi.Input[str] user_name: (Updatable) The database user name.
        :param pulumi.Input[pulumi.InputType['DatabaseToolsConnectionUserPasswordArgs']] user_password: (Updatable) The user password.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _DatabaseToolsConnectionState.__new__(_DatabaseToolsConnectionState)
        __props__.__dict__['advanced_properties'] = advanced_properties
        __props__.__dict__['compartment_id'] = compartment_id
        __props__.__dict__['connection_string'] = connection_string
        __props__.__dict__['defined_tags'] = defined_tags
        __props__.__dict__['display_name'] = display_name
        __props__.__dict__['freeform_tags'] = freeform_tags
        __props__.__dict__['key_stores'] = key_stores
        __props__.__dict__['lifecycle_details'] = lifecycle_details
        __props__.__dict__['private_endpoint_id'] = private_endpoint_id
        __props__.__dict__['related_resource'] = related_resource
        __props__.__dict__['state'] = state
        __props__.__dict__['system_tags'] = system_tags
        __props__.__dict__['time_created'] = time_created
        __props__.__dict__['time_updated'] = time_updated
        __props__.__dict__['type'] = type
        __props__.__dict__['user_name'] = user_name
        __props__.__dict__['user_password'] = user_password
        return DatabaseToolsConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='advancedProperties')
    def advanced_properties(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) The advanced connection properties key-value pair (e.g., `oracle.net.ssl_server_dn_match`).
        """
        return pulumi.get(self, 'advanced_properties')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment containing the Database Tools connection.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='connectionString')
    def connection_string(self) -> pulumi.Output[str]:
        """
        (Updatable) The connect descriptor or Easy Connect Naming method use to connect to the database.
        """
        return pulumi.get(self, 'connection_string')

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        """
        return pulumi.get(self, 'defined_tags')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        (Updatable) A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @property
    @pulumi.getter(name='keyStores')
    def key_stores(self) -> pulumi.Output[Sequence['outputs.DatabaseToolsConnectionKeyStore']]:
        """
        (Updatable) Oracle wallet or Java Keystores containing trusted certificates for authenticating the server's public certificate and the client private key and associated certificates required for client authentication.
        """
        return pulumi.get(self, 'key_stores')

    @property
    @pulumi.getter(name='lifecycleDetails')
    def lifecycle_details(self) -> pulumi.Output[str]:
        """
        A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.
        """
        return pulumi.get(self, 'lifecycle_details')

    @property
    @pulumi.getter(name='privateEndpointId')
    def private_endpoint_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the Database Tools private endpoint used to access the database in the customer VCN.
        """
        return pulumi.get(self, 'private_endpoint_id')

    @property
    @pulumi.getter(name='relatedResource')
    def related_resource(self) -> pulumi.Output['outputs.DatabaseToolsConnectionRelatedResource']:
        """
        (Updatable) The related resource
        """
        return pulumi.get(self, 'related_resource')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the Database Tools connection.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='systemTags')
    def system_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        Usage of system tag keys. These predefined keys are scoped to namespaces. Example: `{"orcl-cloud.free-tier-retained": "true"}`
        """
        return pulumi.get(self, 'system_tags')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> pulumi.Output[str]:
        """
        The time the Database Tools connection was created. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> pulumi.Output[str]:
        """
        The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_updated')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        (Updatable) The DatabaseToolsConnection type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userName')
    def user_name(self) -> pulumi.Output[str]:
        """
        (Updatable) The database user name.
        """
        return pulumi.get(self, 'user_name')

    @property
    @pulumi.getter(name='userPassword')
    def user_password(self) -> pulumi.Output['outputs.DatabaseToolsConnectionUserPassword']:
        """
        (Updatable) The user password.
        """
        return pulumi.get(self, 'user_password')