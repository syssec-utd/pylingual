import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetDomainOwnershipIdentifierResult', 'AwaitableGetDomainOwnershipIdentifierResult', 'get_domain_ownership_identifier', 'get_domain_ownership_identifier_output']

@pulumi.output_type
class GetDomainOwnershipIdentifierResult:
    """
    Domain ownership Identifier.
    """

    def __init__(__self__, id=None, kind=None, name=None, ownership_id=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if ownership_id and (not isinstance(ownership_id, str)):
            raise TypeError("Expected argument 'ownership_id' to be a str")
        pulumi.set(__self__, 'ownership_id', ownership_id)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='ownershipId')
    def ownership_id(self) -> Optional[str]:
        """
        Ownership Id.
        """
        return pulumi.get(self, 'ownership_id')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetDomainOwnershipIdentifierResult(GetDomainOwnershipIdentifierResult):

    def __await__(self):
        if False:
            yield self
        return GetDomainOwnershipIdentifierResult(id=self.id, kind=self.kind, name=self.name, ownership_id=self.ownership_id, type=self.type)

def get_domain_ownership_identifier(domain_name: Optional[str]=None, name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDomainOwnershipIdentifierResult:
    """
    Domain ownership Identifier.


    :param str domain_name: Name of domain.
    :param str name: Name of identifier.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:domainregistration/v20210201:getDomainOwnershipIdentifier', __args__, opts=opts, typ=GetDomainOwnershipIdentifierResult).value
    return AwaitableGetDomainOwnershipIdentifierResult(id=__ret__.id, kind=__ret__.kind, name=__ret__.name, ownership_id=__ret__.ownership_id, type=__ret__.type)

@_utilities.lift_output_func(get_domain_ownership_identifier)
def get_domain_ownership_identifier_output(domain_name: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDomainOwnershipIdentifierResult]:
    """
    Domain ownership Identifier.


    :param str domain_name: Name of domain.
    :param str name: Name of identifier.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...