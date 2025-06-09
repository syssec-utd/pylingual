import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['NetworkProfileArgs', 'OpenShiftAPIPropertiesArgs', 'OpenShiftManagedClusterAADIdentityProviderArgs', 'OpenShiftManagedClusterAgentPoolProfileArgs', 'OpenShiftManagedClusterAuthProfileArgs', 'OpenShiftManagedClusterIdentityProviderArgs', 'OpenShiftManagedClusterMasterPoolProfileArgs', 'OpenShiftManagedClusterMonitorProfileArgs', 'OpenShiftRouterProfileArgs', 'PurchasePlanArgs']

@pulumi.input_type
class NetworkProfileArgs:

    def __init__(__self__, *, management_subnet_cidr: Optional[pulumi.Input[str]]=None, vnet_cidr: Optional[pulumi.Input[str]]=None, vnet_id: Optional[pulumi.Input[str]]=None):
        """
        Represents the OpenShift networking configuration
        :param pulumi.Input[str] management_subnet_cidr: CIDR of subnet used to create PLS needed for management of the cluster
        :param pulumi.Input[str] vnet_cidr: CIDR for the OpenShift Vnet.
        :param pulumi.Input[str] vnet_id: ID of the Vnet created for OSA cluster.
        """
        if management_subnet_cidr is not None:
            pulumi.set(__self__, 'management_subnet_cidr', management_subnet_cidr)
        if vnet_cidr is None:
            vnet_cidr = '10.0.0.0/8'
        if vnet_cidr is not None:
            pulumi.set(__self__, 'vnet_cidr', vnet_cidr)
        if vnet_id is not None:
            pulumi.set(__self__, 'vnet_id', vnet_id)

    @property
    @pulumi.getter(name='managementSubnetCidr')
    def management_subnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        CIDR of subnet used to create PLS needed for management of the cluster
        """
        return pulumi.get(self, 'management_subnet_cidr')

    @management_subnet_cidr.setter
    def management_subnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'management_subnet_cidr', value)

    @property
    @pulumi.getter(name='vnetCidr')
    def vnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        CIDR for the OpenShift Vnet.
        """
        return pulumi.get(self, 'vnet_cidr')

    @vnet_cidr.setter
    def vnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vnet_cidr', value)

    @property
    @pulumi.getter(name='vnetId')
    def vnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Vnet created for OSA cluster.
        """
        return pulumi.get(self, 'vnet_id')

    @vnet_id.setter
    def vnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vnet_id', value)

@pulumi.input_type
class OpenShiftAPIPropertiesArgs:

    def __init__(__self__, *, private_api_server: Optional[pulumi.Input[bool]]=None):
        """
        Defines further properties on the API.
        :param pulumi.Input[bool] private_api_server: Specifies if API server is public or private.
        """
        if private_api_server is not None:
            pulumi.set(__self__, 'private_api_server', private_api_server)

    @property
    @pulumi.getter(name='privateApiServer')
    def private_api_server(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if API server is public or private.
        """
        return pulumi.get(self, 'private_api_server')

    @private_api_server.setter
    def private_api_server(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'private_api_server', value)

@pulumi.input_type
class OpenShiftManagedClusterAADIdentityProviderArgs:

    def __init__(__self__, *, kind: pulumi.Input[str], client_id: Optional[pulumi.Input[str]]=None, customer_admin_group_id: Optional[pulumi.Input[str]]=None, secret: Optional[pulumi.Input[str]]=None, tenant_id: Optional[pulumi.Input[str]]=None):
        """
        Defines the Identity provider for MS AAD.
        :param pulumi.Input[str] kind: The kind of the provider.
               Expected value is 'AADIdentityProvider'.
        :param pulumi.Input[str] client_id: The clientId password associated with the provider.
        :param pulumi.Input[str] customer_admin_group_id: The groupId to be granted cluster admin role.
        :param pulumi.Input[str] secret: The secret password associated with the provider.
        :param pulumi.Input[str] tenant_id: The tenantId associated with the provider.
        """
        pulumi.set(__self__, 'kind', 'AADIdentityProvider')
        if client_id is not None:
            pulumi.set(__self__, 'client_id', client_id)
        if customer_admin_group_id is not None:
            pulumi.set(__self__, 'customer_admin_group_id', customer_admin_group_id)
        if secret is not None:
            pulumi.set(__self__, 'secret', secret)
        if tenant_id is not None:
            pulumi.set(__self__, 'tenant_id', tenant_id)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the provider.
        Expected value is 'AADIdentityProvider'.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The clientId password associated with the provider.
        """
        return pulumi.get(self, 'client_id')

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'client_id', value)

    @property
    @pulumi.getter(name='customerAdminGroupId')
    def customer_admin_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The groupId to be granted cluster admin role.
        """
        return pulumi.get(self, 'customer_admin_group_id')

    @customer_admin_group_id.setter
    def customer_admin_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'customer_admin_group_id', value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[str]]:
        """
        The secret password associated with the provider.
        """
        return pulumi.get(self, 'secret')

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'secret', value)

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The tenantId associated with the provider.
        """
        return pulumi.get(self, 'tenant_id')

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tenant_id', value)

@pulumi.input_type
class OpenShiftManagedClusterAgentPoolProfileArgs:

    def __init__(__self__, *, count: pulumi.Input[int], name: pulumi.Input[str], vm_size: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']], os_type: Optional[pulumi.Input[Union[str, 'OSType']]]=None, role: Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]]=None, subnet_cidr: Optional[pulumi.Input[str]]=None):
        """
        Defines the configuration of the OpenShift cluster VMs.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers.
        :param pulumi.Input[str] name: Unique name of the pool profile in the context of the subscription and resource group.
        :param pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']] vm_size: Size of agent VMs.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']] role: Define the role of the AgentPoolProfile.
        :param pulumi.Input[str] subnet_cidr: Subnet CIDR for the peering.
        """
        pulumi.set(__self__, 'count', count)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'vm_size', vm_size)
        if os_type is not None:
            pulumi.set(__self__, 'os_type', os_type)
        if role is not None:
            pulumi.set(__self__, 'role', role)
        if subnet_cidr is None:
            subnet_cidr = '10.0.0.0/24'
        if subnet_cidr is not None:
            pulumi.set(__self__, 'subnet_cidr', subnet_cidr)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Input[int]:
        """
        Number of agents (VMs) to host docker containers.
        """
        return pulumi.get(self, 'count')

    @count.setter
    def count(self, value: pulumi.Input[int]):
        pulumi.set(self, 'count', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the pool profile in the context of the subscription and resource group.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, 'vm_size')

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]):
        pulumi.set(self, 'vm_size', value)

    @property
    @pulumi.getter(name='osType')
    def os_type(self) -> Optional[pulumi.Input[Union[str, 'OSType']]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, 'os_type')

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[Union[str, 'OSType']]]):
        pulumi.set(self, 'os_type', value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]]:
        """
        Define the role of the AgentPoolProfile.
        """
        return pulumi.get(self, 'role')

    @role.setter
    def role(self, value: Optional[pulumi.Input[Union[str, 'OpenShiftAgentPoolProfileRole']]]):
        pulumi.set(self, 'role', value)

    @property
    @pulumi.getter(name='subnetCidr')
    def subnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        Subnet CIDR for the peering.
        """
        return pulumi.get(self, 'subnet_cidr')

    @subnet_cidr.setter
    def subnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnet_cidr', value)

@pulumi.input_type
class OpenShiftManagedClusterAuthProfileArgs:

    def __init__(__self__, *, identity_providers: Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]]=None):
        """
        Defines all possible authentication profiles for the OpenShift cluster.
        :param pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]] identity_providers: Type of authentication profile to use.
        """
        if identity_providers is not None:
            pulumi.set(__self__, 'identity_providers', identity_providers)

    @property
    @pulumi.getter(name='identityProviders')
    def identity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]]:
        """
        Type of authentication profile to use.
        """
        return pulumi.get(self, 'identity_providers')

    @identity_providers.setter
    def identity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OpenShiftManagedClusterIdentityProviderArgs']]]]):
        pulumi.set(self, 'identity_providers', value)

@pulumi.input_type
class OpenShiftManagedClusterIdentityProviderArgs:

    def __init__(__self__, *, name: Optional[pulumi.Input[str]]=None, provider: Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']]=None):
        """
        Defines the configuration of the identity providers to be used in the OpenShift cluster.
        :param pulumi.Input[str] name: Name of the provider.
        :param pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs'] provider: Configuration of the provider.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if provider is not None:
            pulumi.set(__self__, 'provider', provider)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the provider.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def provider(self) -> Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']]:
        """
        Configuration of the provider.
        """
        return pulumi.get(self, 'provider')

    @provider.setter
    def provider(self, value: Optional[pulumi.Input['OpenShiftManagedClusterAADIdentityProviderArgs']]):
        pulumi.set(self, 'provider', value)

@pulumi.input_type
class OpenShiftManagedClusterMasterPoolProfileArgs:

    def __init__(__self__, *, count: pulumi.Input[int], vm_size: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']], api_properties: Optional[pulumi.Input['OpenShiftAPIPropertiesArgs']]=None, subnet_cidr: Optional[pulumi.Input[str]]=None):
        """
        OpenShiftManagedClusterMaterPoolProfile contains configuration for OpenShift master VMs.
        :param pulumi.Input[int] count: Number of masters (VMs) to host docker containers. The default value is 3.
        :param pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']] vm_size: Size of agent VMs.
        :param pulumi.Input['OpenShiftAPIPropertiesArgs'] api_properties: Defines further properties on the API.
        :param pulumi.Input[str] subnet_cidr: Subnet CIDR for the peering.
        """
        pulumi.set(__self__, 'count', count)
        pulumi.set(__self__, 'vm_size', vm_size)
        if api_properties is not None:
            pulumi.set(__self__, 'api_properties', api_properties)
        if subnet_cidr is not None:
            pulumi.set(__self__, 'subnet_cidr', subnet_cidr)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Input[int]:
        """
        Number of masters (VMs) to host docker containers. The default value is 3.
        """
        return pulumi.get(self, 'count')

    @count.setter
    def count(self, value: pulumi.Input[int]):
        pulumi.set(self, 'count', value)

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, 'vm_size')

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[Union[str, 'OpenShiftContainerServiceVMSize']]):
        pulumi.set(self, 'vm_size', value)

    @property
    @pulumi.getter(name='apiProperties')
    def api_properties(self) -> Optional[pulumi.Input['OpenShiftAPIPropertiesArgs']]:
        """
        Defines further properties on the API.
        """
        return pulumi.get(self, 'api_properties')

    @api_properties.setter
    def api_properties(self, value: Optional[pulumi.Input['OpenShiftAPIPropertiesArgs']]):
        pulumi.set(self, 'api_properties', value)

    @property
    @pulumi.getter(name='subnetCidr')
    def subnet_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        Subnet CIDR for the peering.
        """
        return pulumi.get(self, 'subnet_cidr')

    @subnet_cidr.setter
    def subnet_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnet_cidr', value)

@pulumi.input_type
class OpenShiftManagedClusterMonitorProfileArgs:

    def __init__(__self__, *, enabled: Optional[pulumi.Input[bool]]=None, workspace_resource_id: Optional[pulumi.Input[str]]=None):
        """
        Defines the configuration for Log Analytics integration.
        :param pulumi.Input[bool] enabled: If the Log analytics integration should be turned on or off
        :param pulumi.Input[str] workspace_resource_id: Azure Resource Manager Resource ID for the Log Analytics workspace to integrate with.
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if workspace_resource_id is not None:
            pulumi.set(__self__, 'workspace_resource_id', workspace_resource_id)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If the Log analytics integration should be turned on or off
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='workspaceResourceID')
    def workspace_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Azure Resource Manager Resource ID for the Log Analytics workspace to integrate with.
        """
        return pulumi.get(self, 'workspace_resource_id')

    @workspace_resource_id.setter
    def workspace_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'workspace_resource_id', value)

@pulumi.input_type
class OpenShiftRouterProfileArgs:

    def __init__(__self__, *, name: Optional[pulumi.Input[str]]=None):
        """
        Represents an OpenShift router
        :param pulumi.Input[str] name: Name of the router profile.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the router profile.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

@pulumi.input_type
class PurchasePlanArgs:

    def __init__(__self__, *, name: Optional[pulumi.Input[str]]=None, product: Optional[pulumi.Input[str]]=None, promotion_code: Optional[pulumi.Input[str]]=None, publisher: Optional[pulumi.Input[str]]=None):
        """
        Used for establishing the purchase context of any 3rd Party artifact through MarketPlace.
        :param pulumi.Input[str] name: The plan ID.
        :param pulumi.Input[str] product: Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
        :param pulumi.Input[str] promotion_code: The promotion code.
        :param pulumi.Input[str] publisher: The plan ID.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if product is not None:
            pulumi.set(__self__, 'product', product)
        if promotion_code is not None:
            pulumi.set(__self__, 'promotion_code', promotion_code)
        if publisher is not None:
            pulumi.set(__self__, 'publisher', publisher)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The plan ID.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def product(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the product of the image from the marketplace. This is the same value as Offer under the imageReference element.
        """
        return pulumi.get(self, 'product')

    @product.setter
    def product(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'product', value)

    @property
    @pulumi.getter(name='promotionCode')
    def promotion_code(self) -> Optional[pulumi.Input[str]]:
        """
        The promotion code.
        """
        return pulumi.get(self, 'promotion_code')

    @promotion_code.setter
    def promotion_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'promotion_code', value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The plan ID.
        """
        return pulumi.get(self, 'publisher')

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'publisher', value)