import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetApprovalRuleTemplateResult', 'AwaitableGetApprovalRuleTemplateResult', 'get_approval_rule_template', 'get_approval_rule_template_output']

@pulumi.output_type
class GetApprovalRuleTemplateResult:
    """
    A collection of values returned by getApprovalRuleTemplate.
    """

    def __init__(__self__, approval_rule_template_id=None, content=None, creation_date=None, description=None, id=None, last_modified_date=None, last_modified_user=None, name=None, rule_content_sha256=None):
        if approval_rule_template_id and (not isinstance(approval_rule_template_id, str)):
            raise TypeError("Expected argument 'approval_rule_template_id' to be a str")
        pulumi.set(__self__, 'approval_rule_template_id', approval_rule_template_id)
        if content and (not isinstance(content, str)):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, 'content', content)
        if creation_date and (not isinstance(creation_date, str)):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, 'creation_date', creation_date)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if last_modified_date and (not isinstance(last_modified_date, str)):
            raise TypeError("Expected argument 'last_modified_date' to be a str")
        pulumi.set(__self__, 'last_modified_date', last_modified_date)
        if last_modified_user and (not isinstance(last_modified_user, str)):
            raise TypeError("Expected argument 'last_modified_user' to be a str")
        pulumi.set(__self__, 'last_modified_user', last_modified_user)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if rule_content_sha256 and (not isinstance(rule_content_sha256, str)):
            raise TypeError("Expected argument 'rule_content_sha256' to be a str")
        pulumi.set(__self__, 'rule_content_sha256', rule_content_sha256)

    @property
    @pulumi.getter(name='approvalRuleTemplateId')
    def approval_rule_template_id(self) -> str:
        """
        The ID of the approval rule template.
        """
        return pulumi.get(self, 'approval_rule_template_id')

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The content of the approval rule template.
        """
        return pulumi.get(self, 'content')

    @property
    @pulumi.getter(name='creationDate')
    def creation_date(self) -> str:
        """
        The date the approval rule template was created, in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, 'creation_date')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the approval rule template.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='lastModifiedDate')
    def last_modified_date(self) -> str:
        """
        The date the approval rule template was most recently changed, in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, 'last_modified_date')

    @property
    @pulumi.getter(name='lastModifiedUser')
    def last_modified_user(self) -> str:
        """
        The Amazon Resource Name (ARN) of the user who made the most recent changes to the approval rule template.
        """
        return pulumi.get(self, 'last_modified_user')

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='ruleContentSha256')
    def rule_content_sha256(self) -> str:
        """
        The SHA-256 hash signature for the content of the approval rule template.
        """
        return pulumi.get(self, 'rule_content_sha256')

class AwaitableGetApprovalRuleTemplateResult(GetApprovalRuleTemplateResult):

    def __await__(self):
        if False:
            yield self
        return GetApprovalRuleTemplateResult(approval_rule_template_id=self.approval_rule_template_id, content=self.content, creation_date=self.creation_date, description=self.description, id=self.id, last_modified_date=self.last_modified_date, last_modified_user=self.last_modified_user, name=self.name, rule_content_sha256=self.rule_content_sha256)

def get_approval_rule_template(name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetApprovalRuleTemplateResult:
    """
    Provides details about a specific CodeCommit Approval Rule Template.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.codecommit.get_approval_rule_template(name="MyExampleApprovalRuleTemplate")
    ```


    :param str name: The name for the approval rule template. This needs to be less than 100 characters.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:codecommit/getApprovalRuleTemplate:getApprovalRuleTemplate', __args__, opts=opts, typ=GetApprovalRuleTemplateResult).value
    return AwaitableGetApprovalRuleTemplateResult(approval_rule_template_id=__ret__.approval_rule_template_id, content=__ret__.content, creation_date=__ret__.creation_date, description=__ret__.description, id=__ret__.id, last_modified_date=__ret__.last_modified_date, last_modified_user=__ret__.last_modified_user, name=__ret__.name, rule_content_sha256=__ret__.rule_content_sha256)

@_utilities.lift_output_func(get_approval_rule_template)
def get_approval_rule_template_output(name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetApprovalRuleTemplateResult]:
    """
    Provides details about a specific CodeCommit Approval Rule Template.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.codecommit.get_approval_rule_template(name="MyExampleApprovalRuleTemplate")
    ```


    :param str name: The name for the approval rule template. This needs to be less than 100 characters.
    """
    ...