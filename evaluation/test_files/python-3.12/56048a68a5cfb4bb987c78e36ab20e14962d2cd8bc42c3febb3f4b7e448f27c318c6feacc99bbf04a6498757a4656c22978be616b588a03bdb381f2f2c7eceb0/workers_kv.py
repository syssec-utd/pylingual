import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
__all__ = ['WorkersKvArgs', 'WorkersKv']

@pulumi.input_type
class WorkersKvArgs:

    def __init__(__self__, *, key: pulumi.Input[str], namespace_id: pulumi.Input[str], value: pulumi.Input[str], account_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a WorkersKv resource.
        :param pulumi.Input[str] key: Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] namespace_id: The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] value: Value of the KV pair.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource.
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'namespace_id', namespace_id)
        pulumi.set(__self__, 'value', value)
        if account_id is not None:
            pulumi.set(__self__, 'account_id', account_id)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter(name='namespaceId')
    def namespace_id(self) -> pulumi.Input[str]:
        """
        The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'namespace_id')

    @namespace_id.setter
    def namespace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace_id', value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Value of the KV pair.
        """
        return pulumi.get(self, 'value')

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, 'value', value)

    @property
    @pulumi.getter(name='accountId')
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account identifier to target for the resource.
        """
        return pulumi.get(self, 'account_id')

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'account_id', value)

@pulumi.input_type
class _WorkersKvState:

    def __init__(__self__, *, account_id: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[str]]=None, namespace_id: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering WorkersKv resources.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource.
        :param pulumi.Input[str] key: Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] namespace_id: The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] value: Value of the KV pair.
        """
        if account_id is not None:
            pulumi.set(__self__, 'account_id', account_id)
        if key is not None:
            pulumi.set(__self__, 'key', key)
        if namespace_id is not None:
            pulumi.set(__self__, 'namespace_id', namespace_id)
        if value is not None:
            pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter(name='accountId')
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account identifier to target for the resource.
        """
        return pulumi.get(self, 'account_id')

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'account_id', value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter(name='namespaceId')
    def namespace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'namespace_id')

    @namespace_id.setter
    def namespace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_id', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of the KV pair.
        """
        return pulumi.get(self, 'value')

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'value', value)

class WorkersKv(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_id: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[str]]=None, namespace_id: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Provides a resource to manage a Cloudflare Workers KV Pair.

        > This resource uses the Cloudflare account APIs. This requires setting the
        `CLOUDFLARE_ACCOUNT_ID` environment variable or `account_id` provider argument
        if you do not explicitly set the resource level `account_id` value.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example_ns = cloudflare.WorkersKvNamespace("exampleNs",
            account_id="f037e56e89293a057740de681ac9abbe",
            title="test-namespace")
        example = cloudflare.WorkersKv("example",
            account_id="f037e56e89293a057740de681ac9abbe",
            namespace_id=example_ns.id,
            key="test-key",
            value="test value")
        ```

        ## Import

        ```sh
         $ pulumi import cloudflare:index/workersKv:WorkersKv example <account_id>/<namespace_id>/<key_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource.
        :param pulumi.Input[str] key: Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] namespace_id: The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] value: Value of the KV pair.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WorkersKvArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a resource to manage a Cloudflare Workers KV Pair.

        > This resource uses the Cloudflare account APIs. This requires setting the
        `CLOUDFLARE_ACCOUNT_ID` environment variable or `account_id` provider argument
        if you do not explicitly set the resource level `account_id` value.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example_ns = cloudflare.WorkersKvNamespace("exampleNs",
            account_id="f037e56e89293a057740de681ac9abbe",
            title="test-namespace")
        example = cloudflare.WorkersKv("example",
            account_id="f037e56e89293a057740de681ac9abbe",
            namespace_id=example_ns.id,
            key="test-key",
            value="test value")
        ```

        ## Import

        ```sh
         $ pulumi import cloudflare:index/workersKv:WorkersKv example <account_id>/<namespace_id>/<key_name>
        ```

        :param str resource_name: The name of the resource.
        :param WorkersKvArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkersKvArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_id: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[str]]=None, namespace_id: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkersKvArgs.__new__(WorkersKvArgs)
            __props__.__dict__['account_id'] = account_id
            if key is None and (not opts.urn):
                raise TypeError("Missing required property 'key'")
            __props__.__dict__['key'] = key
            if namespace_id is None and (not opts.urn):
                raise TypeError("Missing required property 'namespace_id'")
            __props__.__dict__['namespace_id'] = namespace_id
            if value is None and (not opts.urn):
                raise TypeError("Missing required property 'value'")
            __props__.__dict__['value'] = value
        super(WorkersKv, __self__).__init__('cloudflare:index/workersKv:WorkersKv', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, account_id: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[str]]=None, namespace_id: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None) -> 'WorkersKv':
        """
        Get an existing WorkersKv resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account identifier to target for the resource.
        :param pulumi.Input[str] key: Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] namespace_id: The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] value: Value of the KV pair.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _WorkersKvState.__new__(_WorkersKvState)
        __props__.__dict__['account_id'] = account_id
        __props__.__dict__['key'] = key
        __props__.__dict__['namespace_id'] = namespace_id
        __props__.__dict__['value'] = value
        return WorkersKv(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='accountId')
    def account_id(self) -> pulumi.Output[str]:
        """
        The account identifier to target for the resource.
        """
        return pulumi.get(self, 'account_id')

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        Name of the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter(name='namespaceId')
    def namespace_id(self) -> pulumi.Output[str]:
        """
        The ID of the Workers KV namespace in which you want to create the KV pair. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, 'namespace_id')

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[str]:
        """
        Value of the KV pair.
        """
        return pulumi.get(self, 'value')