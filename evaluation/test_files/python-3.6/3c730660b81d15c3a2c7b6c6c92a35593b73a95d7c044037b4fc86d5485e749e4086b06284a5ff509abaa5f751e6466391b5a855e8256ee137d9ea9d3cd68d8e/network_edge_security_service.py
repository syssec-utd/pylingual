import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['NetworkEdgeSecurityServiceArgs', 'NetworkEdgeSecurityService']

@pulumi.input_type
class NetworkEdgeSecurityServiceArgs:

    def __init__(__self__, *, region: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, security_policy: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a NetworkEdgeSecurityService resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[str] security_policy: The resource URL for the network edge security service associated with this network edge security service.
        :param pulumi.Input[str] validate_only: If true, the request will not be committed.
        """
        pulumi.set(__self__, 'region', region)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if request_id is not None:
            pulumi.set(__self__, 'request_id', request_id)
        if security_policy is not None:
            pulumi.set(__self__, 'security_policy', security_policy)
        if validate_only is not None:
            pulumi.set(__self__, 'validate_only', validate_only)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'region')

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, 'region', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter(name='requestId')
    def request_id(self) -> Optional[pulumi.Input[str]]:
        """
        An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, 'request_id')

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'request_id', value)

    @property
    @pulumi.getter(name='securityPolicy')
    def security_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The resource URL for the network edge security service associated with this network edge security service.
        """
        return pulumi.get(self, 'security_policy')

    @security_policy.setter
    def security_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'security_policy', value)

    @property
    @pulumi.getter(name='validateOnly')
    def validate_only(self) -> Optional[pulumi.Input[str]]:
        """
        If true, the request will not be committed.
        """
        return pulumi.get(self, 'validate_only')

    @validate_only.setter
    def validate_only(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'validate_only', value)

class NetworkEdgeSecurityService(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, security_policy: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Creates a new service in the specified project using the data included in the request.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[str] security_policy: The resource URL for the network edge security service associated with this network edge security service.
        :param pulumi.Input[str] validate_only: If true, the request will not be committed.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: NetworkEdgeSecurityServiceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a new service in the specified project using the data included in the request.

        :param str resource_name: The name of the resource.
        :param NetworkEdgeSecurityServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(NetworkEdgeSecurityServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, security_policy: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[str]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        else:
            opts = copy.copy(opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkEdgeSecurityServiceArgs.__new__(NetworkEdgeSecurityServiceArgs)
            __props__.__dict__['description'] = description
            __props__.__dict__['name'] = name
            __props__.__dict__['project'] = project
            if region is None and (not opts.urn):
                raise TypeError("Missing required property 'region'")
            __props__.__dict__['region'] = region
            __props__.__dict__['request_id'] = request_id
            __props__.__dict__['security_policy'] = security_policy
            __props__.__dict__['validate_only'] = validate_only
            __props__.__dict__['creation_timestamp'] = None
            __props__.__dict__['fingerprint'] = None
            __props__.__dict__['kind'] = None
            __props__.__dict__['self_link'] = None
            __props__.__dict__['self_link_with_id'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['project', 'region'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(NetworkEdgeSecurityService, __self__).__init__('google-native:compute/alpha:NetworkEdgeSecurityService', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'NetworkEdgeSecurityService':
        """
        Get an existing NetworkEdgeSecurityService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = NetworkEdgeSecurityServiceArgs.__new__(NetworkEdgeSecurityServiceArgs)
        __props__.__dict__['creation_timestamp'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['fingerprint'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['region'] = None
        __props__.__dict__['request_id'] = None
        __props__.__dict__['security_policy'] = None
        __props__.__dict__['self_link'] = None
        __props__.__dict__['self_link_with_id'] = None
        __props__.__dict__['validate_only'] = None
        return NetworkEdgeSecurityService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a NetworkEdgeSecurityService. An up-to-date fingerprint must be provided in order to update the NetworkEdgeSecurityService, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a NetworkEdgeSecurityService.
        """
        return pulumi.get(self, 'fingerprint')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        [Output only] Type of the resource. Always compute#networkEdgeSecurityService for NetworkEdgeSecurityServices
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter(name='requestId')
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, 'request_id')

    @property
    @pulumi.getter(name='securityPolicy')
    def security_policy(self) -> pulumi.Output[str]:
        """
        The resource URL for the network edge security service associated with this network edge security service.
        """
        return pulumi.get(self, 'security_policy')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> pulumi.Output[str]:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter(name='selfLinkWithId')
    def self_link_with_id(self) -> pulumi.Output[str]:
        """
        Server-defined URL for this resource with the resource id.
        """
        return pulumi.get(self, 'self_link_with_id')

    @property
    @pulumi.getter(name='validateOnly')
    def validate_only(self) -> pulumi.Output[Optional[str]]:
        """
        If true, the request will not be committed.
        """
        return pulumi.get(self, 'validate_only')