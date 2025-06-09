import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['NotificationConfigArgs', 'NotificationConfig']

@pulumi.input_type
class NotificationConfigArgs:

    def __init__(__self__, *, config_id: pulumi.Input[str], organization: pulumi.Input[str], pubsub_topic: pulumi.Input[str], streaming_config: pulumi.Input['NotificationConfigStreamingConfigArgs'], description: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a NotificationConfig resource.
        :param pulumi.Input[str] config_id: This must be unique within the organization.
        :param pulumi.Input[str] organization: The organization whose Cloud Security Command Center the Notification
               Config lives in.
        :param pulumi.Input[str] pubsub_topic: The Pub/Sub topic to send notifications to. Its format is
               "projects/[project_id]/topics/[topic]".
        :param pulumi.Input['NotificationConfigStreamingConfigArgs'] streaming_config: The config for triggering streaming-based notifications.
               Structure is documented below.
        :param pulumi.Input[str] description: The description of the notification config (max of 1024 characters).
        """
        pulumi.set(__self__, 'config_id', config_id)
        pulumi.set(__self__, 'organization', organization)
        pulumi.set(__self__, 'pubsub_topic', pubsub_topic)
        pulumi.set(__self__, 'streaming_config', streaming_config)
        if description is not None:
            pulumi.set(__self__, 'description', description)

    @property
    @pulumi.getter(name='configId')
    def config_id(self) -> pulumi.Input[str]:
        """
        This must be unique within the organization.
        """
        return pulumi.get(self, 'config_id')

    @config_id.setter
    def config_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'config_id', value)

    @property
    @pulumi.getter
    def organization(self) -> pulumi.Input[str]:
        """
        The organization whose Cloud Security Command Center the Notification
        Config lives in.
        """
        return pulumi.get(self, 'organization')

    @organization.setter
    def organization(self, value: pulumi.Input[str]):
        pulumi.set(self, 'organization', value)

    @property
    @pulumi.getter(name='pubsubTopic')
    def pubsub_topic(self) -> pulumi.Input[str]:
        """
        The Pub/Sub topic to send notifications to. Its format is
        "projects/[project_id]/topics/[topic]".
        """
        return pulumi.get(self, 'pubsub_topic')

    @pubsub_topic.setter
    def pubsub_topic(self, value: pulumi.Input[str]):
        pulumi.set(self, 'pubsub_topic', value)

    @property
    @pulumi.getter(name='streamingConfig')
    def streaming_config(self) -> pulumi.Input['NotificationConfigStreamingConfigArgs']:
        """
        The config for triggering streaming-based notifications.
        Structure is documented below.
        """
        return pulumi.get(self, 'streaming_config')

    @streaming_config.setter
    def streaming_config(self, value: pulumi.Input['NotificationConfigStreamingConfigArgs']):
        pulumi.set(self, 'streaming_config', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the notification config (max of 1024 characters).
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

@pulumi.input_type
class _NotificationConfigState:

    def __init__(__self__, *, config_id: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, organization: Optional[pulumi.Input[str]]=None, pubsub_topic: Optional[pulumi.Input[str]]=None, service_account: Optional[pulumi.Input[str]]=None, streaming_config: Optional[pulumi.Input['NotificationConfigStreamingConfigArgs']]=None):
        """
        Input properties used for looking up and filtering NotificationConfig resources.
        :param pulumi.Input[str] config_id: This must be unique within the organization.
        :param pulumi.Input[str] description: The description of the notification config (max of 1024 characters).
        :param pulumi.Input[str] name: The resource name of this notification config, in the format
               `organizations/{{organization}}/notificationConfigs/{{config_id}}`.
        :param pulumi.Input[str] organization: The organization whose Cloud Security Command Center the Notification
               Config lives in.
        :param pulumi.Input[str] pubsub_topic: The Pub/Sub topic to send notifications to. Its format is
               "projects/[project_id]/topics/[topic]".
        :param pulumi.Input[str] service_account: The service account that needs "pubsub.topics.publish" permission to
               publish to the Pub/Sub topic.
        :param pulumi.Input['NotificationConfigStreamingConfigArgs'] streaming_config: The config for triggering streaming-based notifications.
               Structure is documented below.
        """
        if config_id is not None:
            pulumi.set(__self__, 'config_id', config_id)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if organization is not None:
            pulumi.set(__self__, 'organization', organization)
        if pubsub_topic is not None:
            pulumi.set(__self__, 'pubsub_topic', pubsub_topic)
        if service_account is not None:
            pulumi.set(__self__, 'service_account', service_account)
        if streaming_config is not None:
            pulumi.set(__self__, 'streaming_config', streaming_config)

    @property
    @pulumi.getter(name='configId')
    def config_id(self) -> Optional[pulumi.Input[str]]:
        """
        This must be unique within the organization.
        """
        return pulumi.get(self, 'config_id')

    @config_id.setter
    def config_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'config_id', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the notification config (max of 1024 characters).
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of this notification config, in the format
        `organizations/{{organization}}/notificationConfigs/{{config_id}}`.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def organization(self) -> Optional[pulumi.Input[str]]:
        """
        The organization whose Cloud Security Command Center the Notification
        Config lives in.
        """
        return pulumi.get(self, 'organization')

    @organization.setter
    def organization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'organization', value)

    @property
    @pulumi.getter(name='pubsubTopic')
    def pubsub_topic(self) -> Optional[pulumi.Input[str]]:
        """
        The Pub/Sub topic to send notifications to. Its format is
        "projects/[project_id]/topics/[topic]".
        """
        return pulumi.get(self, 'pubsub_topic')

    @pubsub_topic.setter
    def pubsub_topic(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'pubsub_topic', value)

    @property
    @pulumi.getter(name='serviceAccount')
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The service account that needs "pubsub.topics.publish" permission to
        publish to the Pub/Sub topic.
        """
        return pulumi.get(self, 'service_account')

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'service_account', value)

    @property
    @pulumi.getter(name='streamingConfig')
    def streaming_config(self) -> Optional[pulumi.Input['NotificationConfigStreamingConfigArgs']]:
        """
        The config for triggering streaming-based notifications.
        Structure is documented below.
        """
        return pulumi.get(self, 'streaming_config')

    @streaming_config.setter
    def streaming_config(self, value: Optional[pulumi.Input['NotificationConfigStreamingConfigArgs']]):
        pulumi.set(self, 'streaming_config', value)

class NotificationConfig(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, config_id: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, organization: Optional[pulumi.Input[str]]=None, pubsub_topic: Optional[pulumi.Input[str]]=None, streaming_config: Optional[pulumi.Input[pulumi.InputType['NotificationConfigStreamingConfigArgs']]]=None, __props__=None):
        """
        A Cloud Security Command Center (Cloud SCC) notification configs. A
        notification config is a Cloud SCC resource that contains the
        configuration to send notifications for create/update events of
        findings, assets and etc.
        > **Note:** In order to use Cloud SCC resources, your organization must be enrolled
        in [SCC Standard/Premium](https://cloud.google.com/security-command-center/docs/quickstart-security-command-center).
        Without doing so, you may run into errors during resource creation.

        To get more information about NotificationConfig, see:

        * [API documentation](https://cloud.google.com/security-command-center/docs/reference/rest/v1/organizations.notificationConfigs)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/security-command-center/docs)

        ## Example Usage
        ### Scc Notification Config Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        scc_notification = gcp.pubsub.Topic("sccNotification")
        custom_notification_config = gcp.securitycenter.NotificationConfig("customNotificationConfig",
            config_id="my-config",
            organization="123456789",
            description="My custom Cloud Security Command Center Finding Notification Configuration",
            pubsub_topic=scc_notification.id,
            streaming_config=gcp.securitycenter.NotificationConfigStreamingConfigArgs(
                filter="category = \\"OPEN_FIREWALL\\" AND state = \\"ACTIVE\\"",
            ))
        ```

        ## Import

        NotificationConfig can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:securitycenter/notificationConfig:NotificationConfig default organizations/{{organization}}/notificationConfigs/{{name}}
        ```

        ```sh
         $ pulumi import gcp:securitycenter/notificationConfig:NotificationConfig default {{organization}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config_id: This must be unique within the organization.
        :param pulumi.Input[str] description: The description of the notification config (max of 1024 characters).
        :param pulumi.Input[str] organization: The organization whose Cloud Security Command Center the Notification
               Config lives in.
        :param pulumi.Input[str] pubsub_topic: The Pub/Sub topic to send notifications to. Its format is
               "projects/[project_id]/topics/[topic]".
        :param pulumi.Input[pulumi.InputType['NotificationConfigStreamingConfigArgs']] streaming_config: The config for triggering streaming-based notifications.
               Structure is documented below.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: NotificationConfigArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A Cloud Security Command Center (Cloud SCC) notification configs. A
        notification config is a Cloud SCC resource that contains the
        configuration to send notifications for create/update events of
        findings, assets and etc.
        > **Note:** In order to use Cloud SCC resources, your organization must be enrolled
        in [SCC Standard/Premium](https://cloud.google.com/security-command-center/docs/quickstart-security-command-center).
        Without doing so, you may run into errors during resource creation.

        To get more information about NotificationConfig, see:

        * [API documentation](https://cloud.google.com/security-command-center/docs/reference/rest/v1/organizations.notificationConfigs)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/security-command-center/docs)

        ## Example Usage
        ### Scc Notification Config Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        scc_notification = gcp.pubsub.Topic("sccNotification")
        custom_notification_config = gcp.securitycenter.NotificationConfig("customNotificationConfig",
            config_id="my-config",
            organization="123456789",
            description="My custom Cloud Security Command Center Finding Notification Configuration",
            pubsub_topic=scc_notification.id,
            streaming_config=gcp.securitycenter.NotificationConfigStreamingConfigArgs(
                filter="category = \\"OPEN_FIREWALL\\" AND state = \\"ACTIVE\\"",
            ))
        ```

        ## Import

        NotificationConfig can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:securitycenter/notificationConfig:NotificationConfig default organizations/{{organization}}/notificationConfigs/{{name}}
        ```

        ```sh
         $ pulumi import gcp:securitycenter/notificationConfig:NotificationConfig default {{organization}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param NotificationConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(NotificationConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, config_id: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, organization: Optional[pulumi.Input[str]]=None, pubsub_topic: Optional[pulumi.Input[str]]=None, streaming_config: Optional[pulumi.Input[pulumi.InputType['NotificationConfigStreamingConfigArgs']]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NotificationConfigArgs.__new__(NotificationConfigArgs)
            if config_id is None and (not opts.urn):
                raise TypeError("Missing required property 'config_id'")
            __props__.__dict__['config_id'] = config_id
            __props__.__dict__['description'] = description
            if organization is None and (not opts.urn):
                raise TypeError("Missing required property 'organization'")
            __props__.__dict__['organization'] = organization
            if pubsub_topic is None and (not opts.urn):
                raise TypeError("Missing required property 'pubsub_topic'")
            __props__.__dict__['pubsub_topic'] = pubsub_topic
            if streaming_config is None and (not opts.urn):
                raise TypeError("Missing required property 'streaming_config'")
            __props__.__dict__['streaming_config'] = streaming_config
            __props__.__dict__['name'] = None
            __props__.__dict__['service_account'] = None
        super(NotificationConfig, __self__).__init__('gcp:securitycenter/notificationConfig:NotificationConfig', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, config_id: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, organization: Optional[pulumi.Input[str]]=None, pubsub_topic: Optional[pulumi.Input[str]]=None, service_account: Optional[pulumi.Input[str]]=None, streaming_config: Optional[pulumi.Input[pulumi.InputType['NotificationConfigStreamingConfigArgs']]]=None) -> 'NotificationConfig':
        """
        Get an existing NotificationConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config_id: This must be unique within the organization.
        :param pulumi.Input[str] description: The description of the notification config (max of 1024 characters).
        :param pulumi.Input[str] name: The resource name of this notification config, in the format
               `organizations/{{organization}}/notificationConfigs/{{config_id}}`.
        :param pulumi.Input[str] organization: The organization whose Cloud Security Command Center the Notification
               Config lives in.
        :param pulumi.Input[str] pubsub_topic: The Pub/Sub topic to send notifications to. Its format is
               "projects/[project_id]/topics/[topic]".
        :param pulumi.Input[str] service_account: The service account that needs "pubsub.topics.publish" permission to
               publish to the Pub/Sub topic.
        :param pulumi.Input[pulumi.InputType['NotificationConfigStreamingConfigArgs']] streaming_config: The config for triggering streaming-based notifications.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _NotificationConfigState.__new__(_NotificationConfigState)
        __props__.__dict__['config_id'] = config_id
        __props__.__dict__['description'] = description
        __props__.__dict__['name'] = name
        __props__.__dict__['organization'] = organization
        __props__.__dict__['pubsub_topic'] = pubsub_topic
        __props__.__dict__['service_account'] = service_account
        __props__.__dict__['streaming_config'] = streaming_config
        return NotificationConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='configId')
    def config_id(self) -> pulumi.Output[str]:
        """
        This must be unique within the organization.
        """
        return pulumi.get(self, 'config_id')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the notification config (max of 1024 characters).
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of this notification config, in the format
        `organizations/{{organization}}/notificationConfigs/{{config_id}}`.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def organization(self) -> pulumi.Output[str]:
        """
        The organization whose Cloud Security Command Center the Notification
        Config lives in.
        """
        return pulumi.get(self, 'organization')

    @property
    @pulumi.getter(name='pubsubTopic')
    def pubsub_topic(self) -> pulumi.Output[str]:
        """
        The Pub/Sub topic to send notifications to. Its format is
        "projects/[project_id]/topics/[topic]".
        """
        return pulumi.get(self, 'pubsub_topic')

    @property
    @pulumi.getter(name='serviceAccount')
    def service_account(self) -> pulumi.Output[str]:
        """
        The service account that needs "pubsub.topics.publish" permission to
        publish to the Pub/Sub topic.
        """
        return pulumi.get(self, 'service_account')

    @property
    @pulumi.getter(name='streamingConfig')
    def streaming_config(self) -> pulumi.Output['outputs.NotificationConfigStreamingConfig']:
        """
        The config for triggering streaming-based notifications.
        Structure is documented below.
        """
        return pulumi.get(self, 'streaming_config')