import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:

    def __init__(__self__, *, policy: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, name_prefix: Optional[pulumi.Input[str]]=None, path: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] description: Description of the IAM policy.
        :param pulumi.Input[str] name: The name of the policy. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the policy.
               See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags for the IAM Policy
        """
        pulumi.set(__self__, 'policy', policy)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if name_prefix is not None:
            pulumi.set(__self__, 'name_prefix', name_prefix)
        if path is not None:
            pulumi.set(__self__, 'path', path)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, 'policy')

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, 'policy', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the IAM policy.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='namePrefix')
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, 'name_prefix')

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name_prefix', value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        Path in which to create the policy.
        See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        """
        return pulumi.get(self, 'path')

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'path', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags for the IAM Policy
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

@pulumi.input_type
class _PolicyState:

    def __init__(__self__, *, arn: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, name_prefix: Optional[pulumi.Input[str]]=None, path: Optional[pulumi.Input[str]]=None, policy: Optional[pulumi.Input[str]]=None, policy_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input[str] arn: The ARN assigned by AWS to this policy.
        :param pulumi.Input[str] description: Description of the IAM policy.
        :param pulumi.Input[str] name: The name of the policy. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the policy.
               See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] policy_id: The policy's ID.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags for the IAM Policy
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider.
        """
        if arn is not None:
            pulumi.set(__self__, 'arn', arn)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if name_prefix is not None:
            pulumi.set(__self__, 'name_prefix', name_prefix)
        if path is not None:
            pulumi.set(__self__, 'path', path)
        if policy is not None:
            pulumi.set(__self__, 'policy', policy)
        if policy_id is not None:
            pulumi.set(__self__, 'policy_id', policy_id)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if tags_all is not None:
            pulumi.set(__self__, 'tags_all', tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN assigned by AWS to this policy.
        """
        return pulumi.get(self, 'arn')

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'arn', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the IAM policy.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='namePrefix')
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, 'name_prefix')

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name_prefix', value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        Path in which to create the policy.
        See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        """
        return pulumi.get(self, 'path')

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'path', value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, 'policy')

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'policy', value)

    @property
    @pulumi.getter(name='policyId')
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The policy's ID.
        """
        return pulumi.get(self, 'policy_id')

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'policy_id', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags for the IAM Policy
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='tagsAll')
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider.
        """
        return pulumi.get(self, 'tags_all')

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags_all', value)

class Policy(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, name_prefix: Optional[pulumi.Input[str]]=None, path: Optional[pulumi.Input[str]]=None, policy: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Provides an IAM policy.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        policy = aws.iam.Policy("policy",
            path="/",
            description="My test policy",
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["ec2:Describe*"],
                    "Effect": "Allow",
                    "Resource": "*",
                }],
            }))
        ```

        ## Import

        IAM Policies can be imported using the `arn`, e.g.,

        ```sh
         $ pulumi import aws:iam/policy:Policy administrator arn:aws:iam::123456789012:policy/UsersManageOwnCredentials
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the IAM policy.
        :param pulumi.Input[str] name: The name of the policy. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the policy.
               See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags for the IAM Policy
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PolicyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides an IAM policy.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        policy = aws.iam.Policy("policy",
            path="/",
            description="My test policy",
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": ["ec2:Describe*"],
                    "Effect": "Allow",
                    "Resource": "*",
                }],
            }))
        ```

        ## Import

        IAM Policies can be imported using the `arn`, e.g.,

        ```sh
         $ pulumi import aws:iam/policy:Policy administrator arn:aws:iam::123456789012:policy/UsersManageOwnCredentials
        ```

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, name_prefix: Optional[pulumi.Input[str]]=None, path: Optional[pulumi.Input[str]]=None, policy: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyArgs.__new__(PolicyArgs)
            __props__.__dict__['description'] = description
            __props__.__dict__['name'] = name
            __props__.__dict__['name_prefix'] = name_prefix
            __props__.__dict__['path'] = path
            if policy is None and (not opts.urn):
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__['policy'] = policy
            __props__.__dict__['tags'] = tags
            __props__.__dict__['arn'] = None
            __props__.__dict__['policy_id'] = None
            __props__.__dict__['tags_all'] = None
        super(Policy, __self__).__init__('aws:iam/policy:Policy', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, arn: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, name_prefix: Optional[pulumi.Input[str]]=None, path: Optional[pulumi.Input[str]]=None, policy: Optional[pulumi.Input[str]]=None, policy_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN assigned by AWS to this policy.
        :param pulumi.Input[str] description: Description of the IAM policy.
        :param pulumi.Input[str] name: The name of the policy. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the policy.
               See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] policy_id: The policy's ID.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags for the IAM Policy
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _PolicyState.__new__(_PolicyState)
        __props__.__dict__['arn'] = arn
        __props__.__dict__['description'] = description
        __props__.__dict__['name'] = name
        __props__.__dict__['name_prefix'] = name_prefix
        __props__.__dict__['path'] = path
        __props__.__dict__['policy'] = policy
        __props__.__dict__['policy_id'] = policy_id
        __props__.__dict__['tags'] = tags
        __props__.__dict__['tags_all'] = tags_all
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN assigned by AWS to this policy.
        """
        return pulumi.get(self, 'arn')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the IAM policy.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the policy. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='namePrefix')
    def name_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, 'name_prefix')

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        """
        Path in which to create the policy.
        See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html) for more information.
        """
        return pulumi.get(self, 'path')

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, 'policy')

    @property
    @pulumi.getter(name='policyId')
    def policy_id(self) -> pulumi.Output[str]:
        """
        The policy's ID.
        """
        return pulumi.get(self, 'policy_id')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of resource tags for the IAM Policy
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='tagsAll')
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider.
        """
        return pulumi.get(self, 'tags_all')