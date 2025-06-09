import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetWafPoliciesResult', 'AwaitableGetWafPoliciesResult', 'get_waf_policies', 'get_waf_policies_output']

@pulumi.output_type
class GetWafPoliciesResult:
    """
    A collection of values returned by getWafPolicies.
    """

    def __init__(__self__, id=None, ids=None, name_regex=None, names=None, output_file=None, policies=None, query_args=None, status=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if ids and (not isinstance(ids, list)):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, 'ids', ids)
        if name_regex and (not isinstance(name_regex, str)):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, 'name_regex', name_regex)
        if names and (not isinstance(names, list)):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, 'names', names)
        if output_file and (not isinstance(output_file, str)):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, 'output_file', output_file)
        if policies and (not isinstance(policies, list)):
            raise TypeError("Expected argument 'policies' to be a list")
        pulumi.set(__self__, 'policies', policies)
        if query_args and (not isinstance(query_args, str)):
            raise TypeError("Expected argument 'query_args' to be a str")
        pulumi.set(__self__, 'query_args', query_args)
        if status and (not isinstance(status, str)):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, 'ids')

    @property
    @pulumi.getter(name='nameRegex')
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, 'name_regex')

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, 'names')

    @property
    @pulumi.getter(name='outputFile')
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, 'output_file')

    @property
    @pulumi.getter
    def policies(self) -> Sequence['outputs.GetWafPoliciesPolicyResult']:
        return pulumi.get(self, 'policies')

    @property
    @pulumi.getter(name='queryArgs')
    def query_args(self) -> Optional[str]:
        return pulumi.get(self, 'query_args')

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, 'status')

class AwaitableGetWafPoliciesResult(GetWafPoliciesResult):

    def __await__(self):
        if False:
            yield self
        return GetWafPoliciesResult(id=self.id, ids=self.ids, name_regex=self.name_regex, names=self.names, output_file=self.output_file, policies=self.policies, query_args=self.query_args, status=self.status)

def get_waf_policies(ids: Optional[Sequence[str]]=None, name_regex: Optional[str]=None, output_file: Optional[str]=None, query_args: Optional[str]=None, status: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWafPoliciesResult:
    """
    This data source provides the Dcdn Waf Policies of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.184.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.dcdn.get_waf_policies()
    pulumi.export("dcdnWafPolicyId1", ids.policies[0].id)
    ```


    :param Sequence[str] ids: A list of Waf Policy IDs.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str query_args: The query conditions. The value is a string in the JSON format. Format: `{"PolicyIds":"The ID of the proteuleIds":"Thection policy","R range of protection rule IDs","PolicyNameLike":"The name of the protection policy","DomainNames":"The protected domain names","PolicyType":"default","DefenseScenes":"waf_group","PolicyStatus":"on","OrderBy":"GmtModified","Desc":"false"}`.
    :param str status: The status of the resource.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['queryArgs'] = query_args
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:dcdn/getWafPolicies:getWafPolicies', __args__, opts=opts, typ=GetWafPoliciesResult).value
    return AwaitableGetWafPoliciesResult(id=__ret__.id, ids=__ret__.ids, name_regex=__ret__.name_regex, names=__ret__.names, output_file=__ret__.output_file, policies=__ret__.policies, query_args=__ret__.query_args, status=__ret__.status)

@_utilities.lift_output_func(get_waf_policies)
def get_waf_policies_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]]=None, name_regex: Optional[pulumi.Input[Optional[str]]]=None, output_file: Optional[pulumi.Input[Optional[str]]]=None, query_args: Optional[pulumi.Input[Optional[str]]]=None, status: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWafPoliciesResult]:
    """
    This data source provides the Dcdn Waf Policies of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.184.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.dcdn.get_waf_policies()
    pulumi.export("dcdnWafPolicyId1", ids.policies[0].id)
    ```


    :param Sequence[str] ids: A list of Waf Policy IDs.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str query_args: The query conditions. The value is a string in the JSON format. Format: `{"PolicyIds":"The ID of the proteuleIds":"Thection policy","R range of protection rule IDs","PolicyNameLike":"The name of the protection policy","DomainNames":"The protected domain names","PolicyType":"default","DefenseScenes":"waf_group","PolicyStatus":"on","OrderBy":"GmtModified","Desc":"false"}`.
    :param str status: The status of the resource.
    """
    ...