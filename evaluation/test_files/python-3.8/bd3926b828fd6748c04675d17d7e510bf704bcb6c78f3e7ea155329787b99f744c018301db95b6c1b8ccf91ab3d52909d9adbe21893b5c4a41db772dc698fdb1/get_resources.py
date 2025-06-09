import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetResourcesResult', 'AwaitableGetResourcesResult', 'get_resources', 'get_resources_output']

@pulumi.output_type
class GetResourcesResult:
    """
    A collection of values returned by getResources.
    """

    def __init__(__self__, exclude_compliant_resources=None, id=None, include_compliance_details=None, resource_arn_lists=None, resource_tag_mapping_lists=None, resource_type_filters=None, tag_filters=None):
        if exclude_compliant_resources and (not isinstance(exclude_compliant_resources, bool)):
            raise TypeError("Expected argument 'exclude_compliant_resources' to be a bool")
        pulumi.set(__self__, 'exclude_compliant_resources', exclude_compliant_resources)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if include_compliance_details and (not isinstance(include_compliance_details, bool)):
            raise TypeError("Expected argument 'include_compliance_details' to be a bool")
        pulumi.set(__self__, 'include_compliance_details', include_compliance_details)
        if resource_arn_lists and (not isinstance(resource_arn_lists, list)):
            raise TypeError("Expected argument 'resource_arn_lists' to be a list")
        pulumi.set(__self__, 'resource_arn_lists', resource_arn_lists)
        if resource_tag_mapping_lists and (not isinstance(resource_tag_mapping_lists, list)):
            raise TypeError("Expected argument 'resource_tag_mapping_lists' to be a list")
        pulumi.set(__self__, 'resource_tag_mapping_lists', resource_tag_mapping_lists)
        if resource_type_filters and (not isinstance(resource_type_filters, list)):
            raise TypeError("Expected argument 'resource_type_filters' to be a list")
        pulumi.set(__self__, 'resource_type_filters', resource_type_filters)
        if tag_filters and (not isinstance(tag_filters, list)):
            raise TypeError("Expected argument 'tag_filters' to be a list")
        pulumi.set(__self__, 'tag_filters', tag_filters)

    @property
    @pulumi.getter(name='excludeCompliantResources')
    def exclude_compliant_resources(self) -> Optional[bool]:
        return pulumi.get(self, 'exclude_compliant_resources')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='includeComplianceDetails')
    def include_compliance_details(self) -> Optional[bool]:
        return pulumi.get(self, 'include_compliance_details')

    @property
    @pulumi.getter(name='resourceArnLists')
    def resource_arn_lists(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, 'resource_arn_lists')

    @property
    @pulumi.getter(name='resourceTagMappingLists')
    def resource_tag_mapping_lists(self) -> Sequence['outputs.GetResourcesResourceTagMappingListResult']:
        """
        List of objects matching the search criteria.
        """
        return pulumi.get(self, 'resource_tag_mapping_lists')

    @property
    @pulumi.getter(name='resourceTypeFilters')
    def resource_type_filters(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, 'resource_type_filters')

    @property
    @pulumi.getter(name='tagFilters')
    def tag_filters(self) -> Optional[Sequence['outputs.GetResourcesTagFilterResult']]:
        return pulumi.get(self, 'tag_filters')

class AwaitableGetResourcesResult(GetResourcesResult):

    def __await__(self):
        if False:
            yield self
        return GetResourcesResult(exclude_compliant_resources=self.exclude_compliant_resources, id=self.id, include_compliance_details=self.include_compliance_details, resource_arn_lists=self.resource_arn_lists, resource_tag_mapping_lists=self.resource_tag_mapping_lists, resource_type_filters=self.resource_type_filters, tag_filters=self.tag_filters)

def get_resources(exclude_compliant_resources: Optional[bool]=None, include_compliance_details: Optional[bool]=None, resource_arn_lists: Optional[Sequence[str]]=None, resource_type_filters: Optional[Sequence[str]]=None, tag_filters: Optional[Sequence[pulumi.InputType['GetResourcesTagFilterArgs']]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetResourcesResult:
    """
    Provides details about resource tagging.

    ## Example Usage
    ### Get All Resource Tag Mappings

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources()
    ```
    ### Filter By Tag Key and Value

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources(tag_filters=[aws.resourcegroupstaggingapi.GetResourcesTagFilterArgs(
        key="tag-key",
        values=[
            "tag-value-1",
            "tag-value-2",
        ],
    )])
    ```
    ### Filter By Resource Type

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources(resource_type_filters=["ec2:instance"])
    ```


    :param bool exclude_compliant_resources: Specifies whether to exclude resources that are compliant with the tag policy. You can use this parameter only if the `include_compliance_details` argument is also set to `true`.
    :param bool include_compliance_details: Specifies whether to include details regarding the compliance with the effective tag policy.
    :param Sequence[str] resource_arn_lists: Specifies a list of ARNs of resources for which you want to retrieve tag data. Conflicts with `filter`.
    :param Sequence[str] resource_type_filters: The constraints on the resources that you want returned. The format of each resource type is `service:resourceType`. For example, specifying a resource type of `ec2` returns all Amazon EC2 resources (which includes EC2 instances). Specifying a resource type of `ec2:instance` returns only EC2 instances.
    :param Sequence[pulumi.InputType['GetResourcesTagFilterArgs']] tag_filters: Specifies a list of Tag Filters (keys and values) to restrict the output to only those resources that have the specified tag and, if included, the specified value. See Tag Filter below. Conflicts with `resource_arn_list`.
    """
    __args__ = dict()
    __args__['excludeCompliantResources'] = exclude_compliant_resources
    __args__['includeComplianceDetails'] = include_compliance_details
    __args__['resourceArnLists'] = resource_arn_lists
    __args__['resourceTypeFilters'] = resource_type_filters
    __args__['tagFilters'] = tag_filters
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:resourcegroupstaggingapi/getResources:getResources', __args__, opts=opts, typ=GetResourcesResult).value
    return AwaitableGetResourcesResult(exclude_compliant_resources=__ret__.exclude_compliant_resources, id=__ret__.id, include_compliance_details=__ret__.include_compliance_details, resource_arn_lists=__ret__.resource_arn_lists, resource_tag_mapping_lists=__ret__.resource_tag_mapping_lists, resource_type_filters=__ret__.resource_type_filters, tag_filters=__ret__.tag_filters)

@_utilities.lift_output_func(get_resources)
def get_resources_output(exclude_compliant_resources: Optional[pulumi.Input[Optional[bool]]]=None, include_compliance_details: Optional[pulumi.Input[Optional[bool]]]=None, resource_arn_lists: Optional[pulumi.Input[Optional[Sequence[str]]]]=None, resource_type_filters: Optional[pulumi.Input[Optional[Sequence[str]]]]=None, tag_filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetResourcesTagFilterArgs']]]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetResourcesResult]:
    """
    Provides details about resource tagging.

    ## Example Usage
    ### Get All Resource Tag Mappings

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources()
    ```
    ### Filter By Tag Key and Value

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources(tag_filters=[aws.resourcegroupstaggingapi.GetResourcesTagFilterArgs(
        key="tag-key",
        values=[
            "tag-value-1",
            "tag-value-2",
        ],
    )])
    ```
    ### Filter By Resource Type

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.resourcegroupstaggingapi.get_resources(resource_type_filters=["ec2:instance"])
    ```


    :param bool exclude_compliant_resources: Specifies whether to exclude resources that are compliant with the tag policy. You can use this parameter only if the `include_compliance_details` argument is also set to `true`.
    :param bool include_compliance_details: Specifies whether to include details regarding the compliance with the effective tag policy.
    :param Sequence[str] resource_arn_lists: Specifies a list of ARNs of resources for which you want to retrieve tag data. Conflicts with `filter`.
    :param Sequence[str] resource_type_filters: The constraints on the resources that you want returned. The format of each resource type is `service:resourceType`. For example, specifying a resource type of `ec2` returns all Amazon EC2 resources (which includes EC2 instances). Specifying a resource type of `ec2:instance` returns only EC2 instances.
    :param Sequence[pulumi.InputType['GetResourcesTagFilterArgs']] tag_filters: Specifies a list of Tag Filters (keys and values) to restrict the output to only those resources that have the specified tag and, if included, the specified value. See Tag Filter below. Conflicts with `resource_arn_list`.
    """
    ...