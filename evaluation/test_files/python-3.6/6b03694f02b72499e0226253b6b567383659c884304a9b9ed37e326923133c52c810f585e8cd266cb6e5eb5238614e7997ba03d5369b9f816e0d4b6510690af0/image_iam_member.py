import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['ImageIamMemberArgs', 'ImageIamMember']

@pulumi.input_type
class ImageIamMemberArgs:

    def __init__(__self__, *, image: pulumi.Input[str], member: pulumi.Input[str], role: pulumi.Input[str], condition: Optional[pulumi.Input['ImageIamMemberConditionArgs']]=None, project: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a ImageIamMember resource.
        :param pulumi.Input[str] image: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input['ImageIamMemberConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        pulumi.set(__self__, 'image', image)
        pulumi.set(__self__, 'member', member)
        pulumi.set(__self__, 'role', role)
        if condition is not None:
            pulumi.set(__self__, 'condition', condition)
        if project is not None:
            pulumi.set(__self__, 'project', project)

    @property
    @pulumi.getter
    def image(self) -> pulumi.Input[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, 'image')

    @image.setter
    def image(self, value: pulumi.Input[str]):
        pulumi.set(self, 'image', value)

    @property
    @pulumi.getter
    def member(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'member')

    @member.setter
    def member(self, value: pulumi.Input[str]):
        pulumi.set(self, 'member', value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, 'role')

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, 'role', value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ImageIamMemberConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, 'condition')

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ImageIamMemberConditionArgs']]):
        pulumi.set(self, 'condition', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

@pulumi.input_type
class _ImageIamMemberState:

    def __init__(__self__, *, condition: Optional[pulumi.Input['ImageIamMemberConditionArgs']]=None, etag: Optional[pulumi.Input[str]]=None, image: Optional[pulumi.Input[str]]=None, member: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, role: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering ImageIamMember resources.
        :param pulumi.Input['ImageIamMemberConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] image: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, 'condition', condition)
        if etag is not None:
            pulumi.set(__self__, 'etag', etag)
        if image is not None:
            pulumi.set(__self__, 'image', image)
        if member is not None:
            pulumi.set(__self__, 'member', member)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if role is not None:
            pulumi.set(__self__, 'role', role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ImageIamMemberConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, 'condition')

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ImageIamMemberConditionArgs']]):
        pulumi.set(self, 'condition', value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, 'etag')

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'etag', value)

    @property
    @pulumi.getter
    def image(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, 'image')

    @image.setter
    def image(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'image', value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'member')

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'member', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, 'role')

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'role', value)

class ImageIamMember(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, condition: Optional[pulumi.Input[pulumi.InputType['ImageIamMemberConditionArgs']]]=None, image: Optional[pulumi.Input[str]]=None, member: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, role: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Three different resources help you manage your IAM policy for Compute Engine Image. Each of these resources serves a different use case:

        * `compute.ImageIamPolicy`: Authoritative. Sets the IAM policy for the image and replaces any existing policy already attached.
        * `compute.ImageIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the image are preserved.
        * `compute.ImageIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the image are preserved.

        > **Note:** `compute.ImageIamPolicy` **cannot** be used in conjunction with `compute.ImageIamBinding` and `compute.ImageIamMember` or they will fight over what your policy should be.

        > **Note:** `compute.ImageIamBinding` resources **can be** used in conjunction with `compute.ImageIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_compute\\_image\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
        )])
        policy = gcp.compute.ImageIamPolicy("policy",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.compute.ImageIamPolicy("policy",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            policy_data=admin.policy_data)
        ```
        ## google\\_compute\\_image\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.ImageIamBinding("binding",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            members=["user:jane@example.com"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.ImageIamBinding("binding",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
            condition=gcp.compute.ImageIamBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        ## google\\_compute\\_image\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.ImageIamMember("member",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            member="user:jane@example.com")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.ImageIamMember("member",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            member="user:jane@example.com",
            condition=gcp.compute.ImageIamMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/global/images/{{name}} * {{project}}/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Compute Engine image IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor "projects/{{project}}/global/images/{{image}} roles/compute.imageUser user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor "projects/{{project}}/global/images/{{image}} roles/compute.imageUser"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor projects/{{project}}/global/images/{{image}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ImageIamMemberConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] image: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ImageIamMemberArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Three different resources help you manage your IAM policy for Compute Engine Image. Each of these resources serves a different use case:

        * `compute.ImageIamPolicy`: Authoritative. Sets the IAM policy for the image and replaces any existing policy already attached.
        * `compute.ImageIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the image are preserved.
        * `compute.ImageIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the image are preserved.

        > **Note:** `compute.ImageIamPolicy` **cannot** be used in conjunction with `compute.ImageIamBinding` and `compute.ImageIamMember` or they will fight over what your policy should be.

        > **Note:** `compute.ImageIamBinding` resources **can be** used in conjunction with `compute.ImageIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_compute\\_image\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
        )])
        policy = gcp.compute.ImageIamPolicy("policy",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.compute.ImageIamPolicy("policy",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            policy_data=admin.policy_data)
        ```
        ## google\\_compute\\_image\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.ImageIamBinding("binding",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            members=["user:jane@example.com"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.ImageIamBinding("binding",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            members=["user:jane@example.com"],
            condition=gcp.compute.ImageIamBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        ## google\\_compute\\_image\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.ImageIamMember("member",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            member="user:jane@example.com")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.ImageIamMember("member",
            project=google_compute_image["example"]["project"],
            image=google_compute_image["example"]["name"],
            role="roles/compute.imageUser",
            member="user:jane@example.com",
            condition=gcp.compute.ImageIamMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/global/images/{{name}} * {{project}}/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Compute Engine image IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor "projects/{{project}}/global/images/{{image}} roles/compute.imageUser user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor "projects/{{project}}/global/images/{{image}} roles/compute.imageUser"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:compute/imageIamMember:ImageIamMember editor projects/{{project}}/global/images/{{image}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param ImageIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ImageIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, condition: Optional[pulumi.Input[pulumi.InputType['ImageIamMemberConditionArgs']]]=None, image: Optional[pulumi.Input[str]]=None, member: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, role: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageIamMemberArgs.__new__(ImageIamMemberArgs)
            __props__.__dict__['condition'] = condition
            if image is None and (not opts.urn):
                raise TypeError("Missing required property 'image'")
            __props__.__dict__['image'] = image
            if member is None and (not opts.urn):
                raise TypeError("Missing required property 'member'")
            __props__.__dict__['member'] = member
            __props__.__dict__['project'] = project
            if role is None and (not opts.urn):
                raise TypeError("Missing required property 'role'")
            __props__.__dict__['role'] = role
            __props__.__dict__['etag'] = None
        super(ImageIamMember, __self__).__init__('gcp:compute/imageIamMember:ImageIamMember', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, condition: Optional[pulumi.Input[pulumi.InputType['ImageIamMemberConditionArgs']]]=None, etag: Optional[pulumi.Input[str]]=None, image: Optional[pulumi.Input[str]]=None, member: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, role: Optional[pulumi.Input[str]]=None) -> 'ImageIamMember':
        """
        Get an existing ImageIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ImageIamMemberConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] image: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ImageIamMemberState.__new__(_ImageIamMemberState)
        __props__.__dict__['condition'] = condition
        __props__.__dict__['etag'] = etag
        __props__.__dict__['image'] = image
        __props__.__dict__['member'] = member
        __props__.__dict__['project'] = project
        __props__.__dict__['role'] = role
        return ImageIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.ImageIamMemberCondition']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, 'condition')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def image(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, 'image')

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'member')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `compute.ImageIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, 'role')