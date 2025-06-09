import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetApplicationResult', 'AwaitableGetApplicationResult', 'get_application', 'get_application_output']

@pulumi.output_type
class GetApplicationResult:
    """
    Information about managed application.
    """

    def __init__(__self__, application_definition_id=None, artifacts=None, authorizations=None, billing_details=None, created_by=None, customer_support=None, id=None, identity=None, jit_access_policy=None, kind=None, location=None, managed_by=None, managed_resource_group_id=None, management_mode=None, name=None, outputs=None, parameters=None, plan=None, provisioning_state=None, publisher_tenant_id=None, sku=None, support_urls=None, tags=None, type=None, updated_by=None):
        if application_definition_id and (not isinstance(application_definition_id, str)):
            raise TypeError("Expected argument 'application_definition_id' to be a str")
        pulumi.set(__self__, 'application_definition_id', application_definition_id)
        if artifacts and (not isinstance(artifacts, list)):
            raise TypeError("Expected argument 'artifacts' to be a list")
        pulumi.set(__self__, 'artifacts', artifacts)
        if authorizations and (not isinstance(authorizations, list)):
            raise TypeError("Expected argument 'authorizations' to be a list")
        pulumi.set(__self__, 'authorizations', authorizations)
        if billing_details and (not isinstance(billing_details, dict)):
            raise TypeError("Expected argument 'billing_details' to be a dict")
        pulumi.set(__self__, 'billing_details', billing_details)
        if created_by and (not isinstance(created_by, dict)):
            raise TypeError("Expected argument 'created_by' to be a dict")
        pulumi.set(__self__, 'created_by', created_by)
        if customer_support and (not isinstance(customer_support, dict)):
            raise TypeError("Expected argument 'customer_support' to be a dict")
        pulumi.set(__self__, 'customer_support', customer_support)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
        if jit_access_policy and (not isinstance(jit_access_policy, dict)):
            raise TypeError("Expected argument 'jit_access_policy' to be a dict")
        pulumi.set(__self__, 'jit_access_policy', jit_access_policy)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if managed_by and (not isinstance(managed_by, str)):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, 'managed_by', managed_by)
        if managed_resource_group_id and (not isinstance(managed_resource_group_id, str)):
            raise TypeError("Expected argument 'managed_resource_group_id' to be a str")
        pulumi.set(__self__, 'managed_resource_group_id', managed_resource_group_id)
        if management_mode and (not isinstance(management_mode, str)):
            raise TypeError("Expected argument 'management_mode' to be a str")
        pulumi.set(__self__, 'management_mode', management_mode)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if outputs and (not isinstance(outputs, dict)):
            raise TypeError("Expected argument 'outputs' to be a dict")
        pulumi.set(__self__, 'outputs', outputs)
        if parameters and (not isinstance(parameters, dict)):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, 'parameters', parameters)
        if plan and (not isinstance(plan, dict)):
            raise TypeError("Expected argument 'plan' to be a dict")
        pulumi.set(__self__, 'plan', plan)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if publisher_tenant_id and (not isinstance(publisher_tenant_id, str)):
            raise TypeError("Expected argument 'publisher_tenant_id' to be a str")
        pulumi.set(__self__, 'publisher_tenant_id', publisher_tenant_id)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if support_urls and (not isinstance(support_urls, dict)):
            raise TypeError("Expected argument 'support_urls' to be a dict")
        pulumi.set(__self__, 'support_urls', support_urls)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if updated_by and (not isinstance(updated_by, dict)):
            raise TypeError("Expected argument 'updated_by' to be a dict")
        pulumi.set(__self__, 'updated_by', updated_by)

    @property
    @pulumi.getter(name='applicationDefinitionId')
    def application_definition_id(self) -> Optional[str]:
        """
        The fully qualified path of managed application definition Id.
        """
        return pulumi.get(self, 'application_definition_id')

    @property
    @pulumi.getter
    def artifacts(self) -> Sequence['outputs.ApplicationArtifactResponse']:
        """
        The collection of managed application artifacts.
        """
        return pulumi.get(self, 'artifacts')

    @property
    @pulumi.getter
    def authorizations(self) -> Sequence['outputs.ApplicationAuthorizationResponse']:
        """
        The  read-only authorizations property that is retrieved from the application package.
        """
        return pulumi.get(self, 'authorizations')

    @property
    @pulumi.getter(name='billingDetails')
    def billing_details(self) -> 'outputs.ApplicationBillingDetailsDefinitionResponse':
        """
        The managed application billing details.
        """
        return pulumi.get(self, 'billing_details')

    @property
    @pulumi.getter(name='createdBy')
    def created_by(self) -> 'outputs.ApplicationClientDetailsResponse':
        """
        The client entity that created the JIT request.
        """
        return pulumi.get(self, 'created_by')

    @property
    @pulumi.getter(name='customerSupport')
    def customer_support(self) -> 'outputs.ApplicationPackageContactResponse':
        """
        The read-only customer support property that is retrieved from the application package.
        """
        return pulumi.get(self, 'customer_support')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity of the resource.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='jitAccessPolicy')
    def jit_access_policy(self) -> Optional['outputs.ApplicationJitAccessPolicyResponse']:
        """
        The managed application Jit access policy.
        """
        return pulumi.get(self, 'jit_access_policy')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the managed application. Allowed values are MarketPlace and ServiceCatalog.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='managedBy')
    def managed_by(self) -> Optional[str]:
        """
        ID of the resource that manages this resource.
        """
        return pulumi.get(self, 'managed_by')

    @property
    @pulumi.getter(name='managedResourceGroupId')
    def managed_resource_group_id(self) -> Optional[str]:
        """
        The managed resource group Id.
        """
        return pulumi.get(self, 'managed_resource_group_id')

    @property
    @pulumi.getter(name='managementMode')
    def management_mode(self) -> str:
        """
        The managed application management mode.
        """
        return pulumi.get(self, 'management_mode')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def outputs(self) -> Any:
        """
        Name and value pairs that define the managed application outputs.
        """
        return pulumi.get(self, 'outputs')

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        """
        Name and value pairs that define the managed application parameters. It can be a JObject or a well formed JSON string.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter
    def plan(self) -> Optional['outputs.PlanResponse']:
        """
        The plan information.
        """
        return pulumi.get(self, 'plan')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The managed application provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publisherTenantId')
    def publisher_tenant_id(self) -> str:
        """
        The publisher tenant Id.
        """
        return pulumi.get(self, 'publisher_tenant_id')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The SKU of the resource.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='supportUrls')
    def support_urls(self) -> 'outputs.ApplicationPackageSupportUrlsResponse':
        """
        The read-only support URLs property that is retrieved from the application package.
        """
        return pulumi.get(self, 'support_urls')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='updatedBy')
    def updated_by(self) -> 'outputs.ApplicationClientDetailsResponse':
        """
        The client entity that last updated the JIT request.
        """
        return pulumi.get(self, 'updated_by')

class AwaitableGetApplicationResult(GetApplicationResult):

    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(application_definition_id=self.application_definition_id, artifacts=self.artifacts, authorizations=self.authorizations, billing_details=self.billing_details, created_by=self.created_by, customer_support=self.customer_support, id=self.id, identity=self.identity, jit_access_policy=self.jit_access_policy, kind=self.kind, location=self.location, managed_by=self.managed_by, managed_resource_group_id=self.managed_resource_group_id, management_mode=self.management_mode, name=self.name, outputs=self.outputs, parameters=self.parameters, plan=self.plan, provisioning_state=self.provisioning_state, publisher_tenant_id=self.publisher_tenant_id, sku=self.sku, support_urls=self.support_urls, tags=self.tags, type=self.type, updated_by=self.updated_by)

def get_application(application_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetApplicationResult:
    """
    Information about managed application.
    API Version: 2019-07-01.


    :param str application_name: The name of the managed application.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['applicationName'] = application_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:solutions:getApplication', __args__, opts=opts, typ=GetApplicationResult).value
    return AwaitableGetApplicationResult(application_definition_id=__ret__.application_definition_id, artifacts=__ret__.artifacts, authorizations=__ret__.authorizations, billing_details=__ret__.billing_details, created_by=__ret__.created_by, customer_support=__ret__.customer_support, id=__ret__.id, identity=__ret__.identity, jit_access_policy=__ret__.jit_access_policy, kind=__ret__.kind, location=__ret__.location, managed_by=__ret__.managed_by, managed_resource_group_id=__ret__.managed_resource_group_id, management_mode=__ret__.management_mode, name=__ret__.name, outputs=__ret__.outputs, parameters=__ret__.parameters, plan=__ret__.plan, provisioning_state=__ret__.provisioning_state, publisher_tenant_id=__ret__.publisher_tenant_id, sku=__ret__.sku, support_urls=__ret__.support_urls, tags=__ret__.tags, type=__ret__.type, updated_by=__ret__.updated_by)

@_utilities.lift_output_func(get_application)
def get_application_output(application_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetApplicationResult]:
    """
    Information about managed application.
    API Version: 2019-07-01.


    :param str application_name: The name of the managed application.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...