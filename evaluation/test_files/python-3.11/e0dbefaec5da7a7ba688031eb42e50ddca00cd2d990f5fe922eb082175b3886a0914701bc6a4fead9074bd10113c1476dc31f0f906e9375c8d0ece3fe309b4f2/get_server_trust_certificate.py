import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetServerTrustCertificateResult', 'AwaitableGetServerTrustCertificateResult', 'get_server_trust_certificate', 'get_server_trust_certificate_output']

@pulumi.output_type
class GetServerTrustCertificateResult:
    """
    Server trust certificate imported from box to enable connection between box and Sql Managed Instance.
    """

    def __init__(__self__, certificate_name=None, id=None, name=None, public_blob=None, thumbprint=None, type=None):
        if certificate_name and (not isinstance(certificate_name, str)):
            raise TypeError("Expected argument 'certificate_name' to be a str")
        pulumi.set(__self__, 'certificate_name', certificate_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if public_blob and (not isinstance(public_blob, str)):
            raise TypeError("Expected argument 'public_blob' to be a str")
        pulumi.set(__self__, 'public_blob', public_blob)
        if thumbprint and (not isinstance(thumbprint, str)):
            raise TypeError("Expected argument 'thumbprint' to be a str")
        pulumi.set(__self__, 'thumbprint', thumbprint)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='certificateName')
    def certificate_name(self) -> str:
        """
        The certificate name
        """
        return pulumi.get(self, 'certificate_name')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='publicBlob')
    def public_blob(self) -> Optional[str]:
        """
        The certificate public blob
        """
        return pulumi.get(self, 'public_blob')

    @property
    @pulumi.getter
    def thumbprint(self) -> str:
        """
        The certificate thumbprint
        """
        return pulumi.get(self, 'thumbprint')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetServerTrustCertificateResult(GetServerTrustCertificateResult):

    def __await__(self):
        if False:
            yield self
        return GetServerTrustCertificateResult(certificate_name=self.certificate_name, id=self.id, name=self.name, public_blob=self.public_blob, thumbprint=self.thumbprint, type=self.type)

def get_server_trust_certificate(certificate_name: Optional[str]=None, managed_instance_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetServerTrustCertificateResult:
    """
    Server trust certificate imported from box to enable connection between box and Sql Managed Instance.
    API Version: 2021-05-01-preview.


    :param str certificate_name: Name of of the certificate to get.
    :param str managed_instance_name: The name of the managed instance.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    """
    __args__ = dict()
    __args__['certificateName'] = certificate_name
    __args__['managedInstanceName'] = managed_instance_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql:getServerTrustCertificate', __args__, opts=opts, typ=GetServerTrustCertificateResult).value
    return AwaitableGetServerTrustCertificateResult(certificate_name=__ret__.certificate_name, id=__ret__.id, name=__ret__.name, public_blob=__ret__.public_blob, thumbprint=__ret__.thumbprint, type=__ret__.type)

@_utilities.lift_output_func(get_server_trust_certificate)
def get_server_trust_certificate_output(certificate_name: Optional[pulumi.Input[str]]=None, managed_instance_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetServerTrustCertificateResult]:
    """
    Server trust certificate imported from box to enable connection between box and Sql Managed Instance.
    API Version: 2021-05-01-preview.


    :param str certificate_name: Name of of the certificate to get.
    :param str managed_instance_name: The name of the managed instance.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    """
    ...