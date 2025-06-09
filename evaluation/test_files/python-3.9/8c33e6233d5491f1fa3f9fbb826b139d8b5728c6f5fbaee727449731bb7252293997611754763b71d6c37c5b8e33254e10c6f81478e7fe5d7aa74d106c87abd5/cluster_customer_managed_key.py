import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['ClusterCustomerManagedKeyArgs', 'ClusterCustomerManagedKey']

@pulumi.input_type
class ClusterCustomerManagedKeyArgs:

    def __init__(__self__, *, cluster_id: pulumi.Input[str], key_name: pulumi.Input[str], key_vault_id: pulumi.Input[str], key_version: pulumi.Input[str], user_identity: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a ClusterCustomerManagedKey resource.
        :param pulumi.Input[str] cluster_id: The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] user_identity: The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        pulumi.set(__self__, 'cluster_id', cluster_id)
        pulumi.set(__self__, 'key_name', key_name)
        pulumi.set(__self__, 'key_vault_id', key_vault_id)
        pulumi.set(__self__, 'key_version', key_version)
        if user_identity is not None:
            pulumi.set(__self__, 'user_identity', user_identity)

    @property
    @pulumi.getter(name='clusterId')
    def cluster_id(self) -> pulumi.Input[str]:
        """
        The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'cluster_id')

    @cluster_id.setter
    def cluster_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'cluster_id', value)

    @property
    @pulumi.getter(name='keyName')
    def key_name(self) -> pulumi.Input[str]:
        """
        The name of Key Vault Key.
        """
        return pulumi.get(self, 'key_name')

    @key_name.setter
    def key_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'key_name', value)

    @property
    @pulumi.getter(name='keyVaultId')
    def key_vault_id(self) -> pulumi.Input[str]:
        """
        The ID of the Key Vault.
        """
        return pulumi.get(self, 'key_vault_id')

    @key_vault_id.setter
    def key_vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'key_vault_id', value)

    @property
    @pulumi.getter(name='keyVersion')
    def key_version(self) -> pulumi.Input[str]:
        """
        The version of Key Vault Key.
        """
        return pulumi.get(self, 'key_version')

    @key_version.setter
    def key_version(self, value: pulumi.Input[str]):
        pulumi.set(self, 'key_version', value)

    @property
    @pulumi.getter(name='userIdentity')
    def user_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        return pulumi.get(self, 'user_identity')

    @user_identity.setter
    def user_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_identity', value)

@pulumi.input_type
class _ClusterCustomerManagedKeyState:

    def __init__(__self__, *, cluster_id: Optional[pulumi.Input[str]]=None, key_name: Optional[pulumi.Input[str]]=None, key_vault_id: Optional[pulumi.Input[str]]=None, key_version: Optional[pulumi.Input[str]]=None, user_identity: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering ClusterCustomerManagedKey resources.
        :param pulumi.Input[str] cluster_id: The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] user_identity: The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        if cluster_id is not None:
            pulumi.set(__self__, 'cluster_id', cluster_id)
        if key_name is not None:
            pulumi.set(__self__, 'key_name', key_name)
        if key_vault_id is not None:
            pulumi.set(__self__, 'key_vault_id', key_vault_id)
        if key_version is not None:
            pulumi.set(__self__, 'key_version', key_version)
        if user_identity is not None:
            pulumi.set(__self__, 'user_identity', user_identity)

    @property
    @pulumi.getter(name='clusterId')
    def cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'cluster_id')

    @cluster_id.setter
    def cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cluster_id', value)

    @property
    @pulumi.getter(name='keyName')
    def key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of Key Vault Key.
        """
        return pulumi.get(self, 'key_name')

    @key_name.setter
    def key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_name', value)

    @property
    @pulumi.getter(name='keyVaultId')
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Key Vault.
        """
        return pulumi.get(self, 'key_vault_id')

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_id', value)

    @property
    @pulumi.getter(name='keyVersion')
    def key_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of Key Vault Key.
        """
        return pulumi.get(self, 'key_version')

    @key_version.setter
    def key_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_version', value)

    @property
    @pulumi.getter(name='userIdentity')
    def user_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        return pulumi.get(self, 'user_identity')

    @user_identity.setter
    def user_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_identity', value)

class ClusterCustomerManagedKey(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cluster_id: Optional[pulumi.Input[str]]=None, key_name: Optional[pulumi.Input[str]]=None, key_vault_id: Optional[pulumi.Input[str]]=None, key_version: Optional[pulumi.Input[str]]=None, user_identity: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Manages a Customer Managed Key for a Kusto Cluster.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_key_vault = azure.keyvault.KeyVault("exampleKeyVault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            tenant_id=current.tenant_id,
            sku_name="standard",
            purge_protection_enabled=True)
        example_cluster = azure.kusto.Cluster("exampleCluster",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.kusto.ClusterSkuArgs(
                name="Standard_D13_v2",
                capacity=2,
            ),
            identity=azure.kusto.ClusterIdentityArgs(
                type="SystemAssigned",
            ))
        cluster = azure.keyvault.AccessPolicy("cluster",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=example_cluster.identity.principal_id,
            key_permissions=[
                "Get",
                "UnwrapKey",
                "WrapKey",
            ])
        client = azure.keyvault.AccessPolicy("client",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=current.object_id,
            key_permissions=[
                "Get",
                "List",
                "Create",
                "Delete",
                "Recover",
            ])
        example_key = azure.keyvault.Key("exampleKey",
            key_vault_id=example_key_vault.id,
            key_type="RSA",
            key_size=2048,
            key_opts=[
                "decrypt",
                "encrypt",
                "sign",
                "unwrapKey",
                "verify",
                "wrapKey",
            ],
            opts=pulumi.ResourceOptions(depends_on=[
                    client,
                    cluster,
                ]))
        example_cluster_customer_managed_key = azure.kusto.ClusterCustomerManagedKey("exampleClusterCustomerManagedKey",
            cluster_id=example_cluster.id,
            key_vault_id=example_key_vault.id,
            key_name=example_key.name,
            key_version=example_key.version)
        ```

        ## Import

        Customer Managed Keys for a Kusto Cluster can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:kusto/clusterCustomerManagedKey:ClusterCustomerManagedKey example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Kusto/Clusters/cluster1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] user_identity: The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ClusterCustomerManagedKeyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages a Customer Managed Key for a Kusto Cluster.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        current = azure.core.get_client_config()
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_key_vault = azure.keyvault.KeyVault("exampleKeyVault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            tenant_id=current.tenant_id,
            sku_name="standard",
            purge_protection_enabled=True)
        example_cluster = azure.kusto.Cluster("exampleCluster",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.kusto.ClusterSkuArgs(
                name="Standard_D13_v2",
                capacity=2,
            ),
            identity=azure.kusto.ClusterIdentityArgs(
                type="SystemAssigned",
            ))
        cluster = azure.keyvault.AccessPolicy("cluster",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=example_cluster.identity.principal_id,
            key_permissions=[
                "Get",
                "UnwrapKey",
                "WrapKey",
            ])
        client = azure.keyvault.AccessPolicy("client",
            key_vault_id=example_key_vault.id,
            tenant_id=current.tenant_id,
            object_id=current.object_id,
            key_permissions=[
                "Get",
                "List",
                "Create",
                "Delete",
                "Recover",
            ])
        example_key = azure.keyvault.Key("exampleKey",
            key_vault_id=example_key_vault.id,
            key_type="RSA",
            key_size=2048,
            key_opts=[
                "decrypt",
                "encrypt",
                "sign",
                "unwrapKey",
                "verify",
                "wrapKey",
            ],
            opts=pulumi.ResourceOptions(depends_on=[
                    client,
                    cluster,
                ]))
        example_cluster_customer_managed_key = azure.kusto.ClusterCustomerManagedKey("exampleClusterCustomerManagedKey",
            cluster_id=example_cluster.id,
            key_vault_id=example_key_vault.id,
            key_name=example_key.name,
            key_version=example_key.version)
        ```

        ## Import

        Customer Managed Keys for a Kusto Cluster can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:kusto/clusterCustomerManagedKey:ClusterCustomerManagedKey example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Kusto/Clusters/cluster1
        ```

        :param str resource_name: The name of the resource.
        :param ClusterCustomerManagedKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ClusterCustomerManagedKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cluster_id: Optional[pulumi.Input[str]]=None, key_name: Optional[pulumi.Input[str]]=None, key_vault_id: Optional[pulumi.Input[str]]=None, key_version: Optional[pulumi.Input[str]]=None, user_identity: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterCustomerManagedKeyArgs.__new__(ClusterCustomerManagedKeyArgs)
            if cluster_id is None and (not opts.urn):
                raise TypeError("Missing required property 'cluster_id'")
            __props__.__dict__['cluster_id'] = cluster_id
            if key_name is None and (not opts.urn):
                raise TypeError("Missing required property 'key_name'")
            __props__.__dict__['key_name'] = key_name
            if key_vault_id is None and (not opts.urn):
                raise TypeError("Missing required property 'key_vault_id'")
            __props__.__dict__['key_vault_id'] = key_vault_id
            if key_version is None and (not opts.urn):
                raise TypeError("Missing required property 'key_version'")
            __props__.__dict__['key_version'] = key_version
            __props__.__dict__['user_identity'] = user_identity
        super(ClusterCustomerManagedKey, __self__).__init__('azure:kusto/clusterCustomerManagedKey:ClusterCustomerManagedKey', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, cluster_id: Optional[pulumi.Input[str]]=None, key_name: Optional[pulumi.Input[str]]=None, key_vault_id: Optional[pulumi.Input[str]]=None, key_version: Optional[pulumi.Input[str]]=None, user_identity: Optional[pulumi.Input[str]]=None) -> 'ClusterCustomerManagedKey':
        """
        Get an existing ClusterCustomerManagedKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] user_identity: The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ClusterCustomerManagedKeyState.__new__(_ClusterCustomerManagedKeyState)
        __props__.__dict__['cluster_id'] = cluster_id
        __props__.__dict__['key_name'] = key_name
        __props__.__dict__['key_vault_id'] = key_vault_id
        __props__.__dict__['key_version'] = key_version
        __props__.__dict__['user_identity'] = user_identity
        return ClusterCustomerManagedKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='clusterId')
    def cluster_id(self) -> pulumi.Output[str]:
        """
        The ID of the Kusto Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'cluster_id')

    @property
    @pulumi.getter(name='keyName')
    def key_name(self) -> pulumi.Output[str]:
        """
        The name of Key Vault Key.
        """
        return pulumi.get(self, 'key_name')

    @property
    @pulumi.getter(name='keyVaultId')
    def key_vault_id(self) -> pulumi.Output[str]:
        """
        The ID of the Key Vault.
        """
        return pulumi.get(self, 'key_vault_id')

    @property
    @pulumi.getter(name='keyVersion')
    def key_version(self) -> pulumi.Output[str]:
        """
        The version of Key Vault Key.
        """
        return pulumi.get(self, 'key_version')

    @property
    @pulumi.getter(name='userIdentity')
    def user_identity(self) -> pulumi.Output[Optional[str]]:
        """
        The user assigned identity that has access to the Key Vault Key. If not specified, system assigned identity will be used.
        """
        return pulumi.get(self, 'user_identity')