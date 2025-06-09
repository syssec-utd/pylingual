import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['WebAppDeploymentSlotArgs', 'WebAppDeploymentSlot']

@pulumi.input_type
class WebAppDeploymentSlotArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], slot: pulumi.Input[str], active: Optional[pulumi.Input[bool]]=None, author: Optional[pulumi.Input[str]]=None, author_email: Optional[pulumi.Input[str]]=None, deployer: Optional[pulumi.Input[str]]=None, details: Optional[pulumi.Input[str]]=None, end_time: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, message: Optional[pulumi.Input[str]]=None, start_time: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[int]]=None):
        """
        The set of arguments for constructing a WebAppDeploymentSlot resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API creates a deployment for the production slot.
        :param pulumi.Input[bool] active: True if deployment is currently active, false if completed and null if not started.
        :param pulumi.Input[str] author: Who authored the deployment.
        :param pulumi.Input[str] author_email: Author email.
        :param pulumi.Input[str] deployer: Who performed the deployment.
        :param pulumi.Input[str] details: Details on deployment.
        :param pulumi.Input[str] end_time: End time.
        :param pulumi.Input[str] id: ID of an existing deployment.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] message: Details about deployment status.
        :param pulumi.Input[str] start_time: Start time.
        :param pulumi.Input[int] status: Deployment status.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'slot', slot)
        if active is not None:
            pulumi.set(__self__, 'active', active)
        if author is not None:
            pulumi.set(__self__, 'author', author)
        if author_email is not None:
            pulumi.set(__self__, 'author_email', author_email)
        if deployer is not None:
            pulumi.set(__self__, 'deployer', deployer)
        if details is not None:
            pulumi.set(__self__, 'details', details)
        if end_time is not None:
            pulumi.set(__self__, 'end_time', end_time)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if message is not None:
            pulumi.set(__self__, 'message', message)
        if start_time is not None:
            pulumi.set(__self__, 'start_time', start_time)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the app.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def slot(self) -> pulumi.Input[str]:
        """
        Name of the deployment slot. If a slot is not specified, the API creates a deployment for the production slot.
        """
        return pulumi.get(self, 'slot')

    @slot.setter
    def slot(self, value: pulumi.Input[str]):
        pulumi.set(self, 'slot', value)

    @property
    @pulumi.getter
    def active(self) -> Optional[pulumi.Input[bool]]:
        """
        True if deployment is currently active, false if completed and null if not started.
        """
        return pulumi.get(self, 'active')

    @active.setter
    def active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'active', value)

    @property
    @pulumi.getter
    def author(self) -> Optional[pulumi.Input[str]]:
        """
        Who authored the deployment.
        """
        return pulumi.get(self, 'author')

    @author.setter
    def author(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'author', value)

    @property
    @pulumi.getter(name='authorEmail')
    def author_email(self) -> Optional[pulumi.Input[str]]:
        """
        Author email.
        """
        return pulumi.get(self, 'author_email')

    @author_email.setter
    def author_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'author_email', value)

    @property
    @pulumi.getter
    def deployer(self) -> Optional[pulumi.Input[str]]:
        """
        Who performed the deployment.
        """
        return pulumi.get(self, 'deployer')

    @deployer.setter
    def deployer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'deployer', value)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input[str]]:
        """
        Details on deployment.
        """
        return pulumi.get(self, 'details')

    @details.setter
    def details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'details', value)

    @property
    @pulumi.getter(name='endTime')
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        End time.
        """
        return pulumi.get(self, 'end_time')

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'end_time', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of an existing deployment.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Details about deployment status.
        """
        return pulumi.get(self, 'message')

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'message', value)

    @property
    @pulumi.getter(name='startTime')
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Start time.
        """
        return pulumi.get(self, 'start_time')

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'start_time', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[int]]:
        """
        Deployment status.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'status', value)

class WebAppDeploymentSlot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, active: Optional[pulumi.Input[bool]]=None, author: Optional[pulumi.Input[str]]=None, author_email: Optional[pulumi.Input[str]]=None, deployer: Optional[pulumi.Input[str]]=None, details: Optional[pulumi.Input[str]]=None, end_time: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, message: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, start_time: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[int]]=None, __props__=None):
        """
        User credentials used for publishing activity.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: True if deployment is currently active, false if completed and null if not started.
        :param pulumi.Input[str] author: Who authored the deployment.
        :param pulumi.Input[str] author_email: Author email.
        :param pulumi.Input[str] deployer: Who performed the deployment.
        :param pulumi.Input[str] details: Details on deployment.
        :param pulumi.Input[str] end_time: End time.
        :param pulumi.Input[str] id: ID of an existing deployment.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] message: Details about deployment status.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API creates a deployment for the production slot.
        :param pulumi.Input[str] start_time: Start time.
        :param pulumi.Input[int] status: Deployment status.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WebAppDeploymentSlotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        User credentials used for publishing activity.

        :param str resource_name: The name of the resource.
        :param WebAppDeploymentSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppDeploymentSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, active: Optional[pulumi.Input[bool]]=None, author: Optional[pulumi.Input[str]]=None, author_email: Optional[pulumi.Input[str]]=None, deployer: Optional[pulumi.Input[str]]=None, details: Optional[pulumi.Input[str]]=None, end_time: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, message: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, start_time: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[int]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebAppDeploymentSlotArgs.__new__(WebAppDeploymentSlotArgs)
            __props__.__dict__['active'] = active
            __props__.__dict__['author'] = author
            __props__.__dict__['author_email'] = author_email
            __props__.__dict__['deployer'] = deployer
            __props__.__dict__['details'] = details
            __props__.__dict__['end_time'] = end_time
            __props__.__dict__['id'] = id
            __props__.__dict__['kind'] = kind
            __props__.__dict__['message'] = message
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if slot is None and (not opts.urn):
                raise TypeError("Missing required property 'slot'")
            __props__.__dict__['slot'] = slot
            __props__.__dict__['start_time'] = start_time
            __props__.__dict__['status'] = status
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:web:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20150801:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20160801:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20180201:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20181101:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20190801:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20200601:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20200901:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20201001:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20201201:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20210101:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20210201:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20210301:WebAppDeploymentSlot'), pulumi.Alias(type_='azure-native:web/v20220301:WebAppDeploymentSlot')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppDeploymentSlot, __self__).__init__('azure-native:web/v20210115:WebAppDeploymentSlot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'WebAppDeploymentSlot':
        """
        Get an existing WebAppDeploymentSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = WebAppDeploymentSlotArgs.__new__(WebAppDeploymentSlotArgs)
        __props__.__dict__['active'] = None
        __props__.__dict__['author'] = None
        __props__.__dict__['author_email'] = None
        __props__.__dict__['deployer'] = None
        __props__.__dict__['details'] = None
        __props__.__dict__['end_time'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['message'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['start_time'] = None
        __props__.__dict__['status'] = None
        __props__.__dict__['type'] = None
        return WebAppDeploymentSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def active(self) -> pulumi.Output[Optional[bool]]:
        """
        True if deployment is currently active, false if completed and null if not started.
        """
        return pulumi.get(self, 'active')

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[Optional[str]]:
        """
        Who authored the deployment.
        """
        return pulumi.get(self, 'author')

    @property
    @pulumi.getter(name='authorEmail')
    def author_email(self) -> pulumi.Output[Optional[str]]:
        """
        Author email.
        """
        return pulumi.get(self, 'author_email')

    @property
    @pulumi.getter
    def deployer(self) -> pulumi.Output[Optional[str]]:
        """
        Who performed the deployment.
        """
        return pulumi.get(self, 'deployer')

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[str]]:
        """
        Details on deployment.
        """
        return pulumi.get(self, 'details')

    @property
    @pulumi.getter(name='endTime')
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        End time.
        """
        return pulumi.get(self, 'end_time')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[Optional[str]]:
        """
        Details about deployment status.
        """
        return pulumi.get(self, 'message')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='startTime')
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        Start time.
        """
        return pulumi.get(self, 'start_time')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[int]]:
        """
        Deployment status.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')