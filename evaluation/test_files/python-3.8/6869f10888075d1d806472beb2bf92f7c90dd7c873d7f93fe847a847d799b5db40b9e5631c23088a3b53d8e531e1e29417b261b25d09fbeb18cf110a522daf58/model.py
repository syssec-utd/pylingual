import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ModelArgs', 'Model']

@pulumi.input_type
class ModelArgs:

    def __init__(__self__, *, description: Optional[pulumi.Input[str]]=None, etag: Optional[pulumi.Input[str]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, name: Optional[pulumi.Input[str]]=None, online_prediction_console_logging: Optional[pulumi.Input[bool]]=None, online_prediction_logging: Optional[pulumi.Input[bool]]=None, project: Optional[pulumi.Input[str]]=None, regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Model resource.
        :param pulumi.Input[str] description: Optional. The description specified for the model when it was created.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a model from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform model updates in order to avoid race conditions: An `etag` is returned in the response to `GetModel`, and systems are expected to put that etag in the request to `UpdateModel` to ensure that their change will be applied to the model as intended.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. One or more labels that you can add, to organize your models. Each label is a key-value pair, where both the key and the value are arbitrary strings that you supply. For more information, see the documentation on using labels. Note that this field is not updatable for mls1* models.
        :param pulumi.Input[str] name: The name specified for the model when it was created. The model name must be unique within the project it is created in.
        :param pulumi.Input[bool] online_prediction_console_logging: Optional. If true, online prediction nodes send `stderr` and `stdout` streams to Cloud Logging. These can be more verbose than the standard access logs (see `onlinePredictionLogging`) and can incur higher cost. However, they are helpful for debugging. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high QPS. Estimate your costs before enabling this option. Default is false.
        :param pulumi.Input[bool] online_prediction_logging: Optional. If true, online prediction access logs are sent to Cloud Logging. These logs are like standard server access logs, containing information like timestamp and latency for each request. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high queries per second rate (QPS). Estimate your costs before enabling this option. Default is false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: Optional. The list of regions where the model is going to be deployed. Only one region per model is supported. Defaults to 'us-central1' if nothing is set. See the available regions for AI Platform services. Note: * No matter where a model is deployed, it can always be accessed by users from anywhere, both for online and batch prediction. * The region for a batch prediction job is set by the region field when submitting the batch prediction job and does not take its value from this field.
        """
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if etag is not None:
            pulumi.set(__self__, 'etag', etag)
        if labels is not None:
            pulumi.set(__self__, 'labels', labels)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if online_prediction_console_logging is not None:
            pulumi.set(__self__, 'online_prediction_console_logging', online_prediction_console_logging)
        if online_prediction_logging is not None:
            pulumi.set(__self__, 'online_prediction_logging', online_prediction_logging)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if regions is not None:
            pulumi.set(__self__, 'regions', regions)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The description specified for the model when it was created.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a model from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform model updates in order to avoid race conditions: An `etag` is returned in the response to `GetModel`, and systems are expected to put that etag in the request to `UpdateModel` to ensure that their change will be applied to the model as intended.
        """
        return pulumi.get(self, 'etag')

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'etag', value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. One or more labels that you can add, to organize your models. Each label is a key-value pair, where both the key and the value are arbitrary strings that you supply. For more information, see the documentation on using labels. Note that this field is not updatable for mls1* models.
        """
        return pulumi.get(self, 'labels')

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'labels', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name specified for the model when it was created. The model name must be unique within the project it is created in.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='onlinePredictionConsoleLogging')
    def online_prediction_console_logging(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. If true, online prediction nodes send `stderr` and `stdout` streams to Cloud Logging. These can be more verbose than the standard access logs (see `onlinePredictionLogging`) and can incur higher cost. However, they are helpful for debugging. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high QPS. Estimate your costs before enabling this option. Default is false.
        """
        return pulumi.get(self, 'online_prediction_console_logging')

    @online_prediction_console_logging.setter
    def online_prediction_console_logging(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'online_prediction_console_logging', value)

    @property
    @pulumi.getter(name='onlinePredictionLogging')
    def online_prediction_logging(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. If true, online prediction access logs are sent to Cloud Logging. These logs are like standard server access logs, containing information like timestamp and latency for each request. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high queries per second rate (QPS). Estimate your costs before enabling this option. Default is false.
        """
        return pulumi.get(self, 'online_prediction_logging')

    @online_prediction_logging.setter
    def online_prediction_logging(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'online_prediction_logging', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter
    def regions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. The list of regions where the model is going to be deployed. Only one region per model is supported. Defaults to 'us-central1' if nothing is set. See the available regions for AI Platform services. Note: * No matter where a model is deployed, it can always be accessed by users from anywhere, both for online and batch prediction. * The region for a batch prediction job is set by the region field when submitting the batch prediction job and does not take its value from this field.
        """
        return pulumi.get(self, 'regions')

    @regions.setter
    def regions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'regions', value)

class Model(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, etag: Optional[pulumi.Input[str]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, name: Optional[pulumi.Input[str]]=None, online_prediction_console_logging: Optional[pulumi.Input[bool]]=None, online_prediction_logging: Optional[pulumi.Input[bool]]=None, project: Optional[pulumi.Input[str]]=None, regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        Creates a model which will later contain one or more versions. You must add at least one version before you can request predictions from the model. Add versions by calling projects.models.versions.create.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. The description specified for the model when it was created.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a model from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform model updates in order to avoid race conditions: An `etag` is returned in the response to `GetModel`, and systems are expected to put that etag in the request to `UpdateModel` to ensure that their change will be applied to the model as intended.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. One or more labels that you can add, to organize your models. Each label is a key-value pair, where both the key and the value are arbitrary strings that you supply. For more information, see the documentation on using labels. Note that this field is not updatable for mls1* models.
        :param pulumi.Input[str] name: The name specified for the model when it was created. The model name must be unique within the project it is created in.
        :param pulumi.Input[bool] online_prediction_console_logging: Optional. If true, online prediction nodes send `stderr` and `stdout` streams to Cloud Logging. These can be more verbose than the standard access logs (see `onlinePredictionLogging`) and can incur higher cost. However, they are helpful for debugging. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high QPS. Estimate your costs before enabling this option. Default is false.
        :param pulumi.Input[bool] online_prediction_logging: Optional. If true, online prediction access logs are sent to Cloud Logging. These logs are like standard server access logs, containing information like timestamp and latency for each request. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high queries per second rate (QPS). Estimate your costs before enabling this option. Default is false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: Optional. The list of regions where the model is going to be deployed. Only one region per model is supported. Defaults to 'us-central1' if nothing is set. See the available regions for AI Platform services. Note: * No matter where a model is deployed, it can always be accessed by users from anywhere, both for online and batch prediction. * The region for a batch prediction job is set by the region field when submitting the batch prediction job and does not take its value from this field.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: Optional[ModelArgs]=None, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a model which will later contain one or more versions. You must add at least one version before you can request predictions from the model. Add versions by calling projects.models.versions.create.

        :param str resource_name: The name of the resource.
        :param ModelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ModelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, description: Optional[pulumi.Input[str]]=None, etag: Optional[pulumi.Input[str]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, name: Optional[pulumi.Input[str]]=None, online_prediction_console_logging: Optional[pulumi.Input[bool]]=None, online_prediction_logging: Optional[pulumi.Input[bool]]=None, project: Optional[pulumi.Input[str]]=None, regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
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
            __props__ = ModelArgs.__new__(ModelArgs)
            __props__.__dict__['description'] = description
            __props__.__dict__['etag'] = etag
            __props__.__dict__['labels'] = labels
            __props__.__dict__['name'] = name
            __props__.__dict__['online_prediction_console_logging'] = online_prediction_console_logging
            __props__.__dict__['online_prediction_logging'] = online_prediction_logging
            __props__.__dict__['project'] = project
            __props__.__dict__['regions'] = regions
            __props__.__dict__['default_version'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Model, __self__).__init__('google-native:ml/v1:Model', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Model':
        """
        Get an existing Model resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ModelArgs.__new__(ModelArgs)
        __props__.__dict__['default_version'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['labels'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['online_prediction_console_logging'] = None
        __props__.__dict__['online_prediction_logging'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['regions'] = None
        return Model(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='defaultVersion')
    def default_version(self) -> pulumi.Output['outputs.GoogleCloudMlV1__VersionResponse']:
        """
        The default version of the model. This version will be used to handle prediction requests that do not specify a version. You can change the default version by calling projects.models.versions.setDefault.
        """
        return pulumi.get(self, 'default_version')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. The description specified for the model when it was created.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a model from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform model updates in order to avoid race conditions: An `etag` is returned in the response to `GetModel`, and systems are expected to put that etag in the request to `UpdateModel` to ensure that their change will be applied to the model as intended.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Optional. One or more labels that you can add, to organize your models. Each label is a key-value pair, where both the key and the value are arbitrary strings that you supply. For more information, see the documentation on using labels. Note that this field is not updatable for mls1* models.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name specified for the model when it was created. The model name must be unique within the project it is created in.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='onlinePredictionConsoleLogging')
    def online_prediction_console_logging(self) -> pulumi.Output[bool]:
        """
        Optional. If true, online prediction nodes send `stderr` and `stdout` streams to Cloud Logging. These can be more verbose than the standard access logs (see `onlinePredictionLogging`) and can incur higher cost. However, they are helpful for debugging. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high QPS. Estimate your costs before enabling this option. Default is false.
        """
        return pulumi.get(self, 'online_prediction_console_logging')

    @property
    @pulumi.getter(name='onlinePredictionLogging')
    def online_prediction_logging(self) -> pulumi.Output[bool]:
        """
        Optional. If true, online prediction access logs are sent to Cloud Logging. These logs are like standard server access logs, containing information like timestamp and latency for each request. Note that [logs may incur a cost](/stackdriver/pricing), especially if your project receives prediction requests at a high queries per second rate (QPS). Estimate your costs before enabling this option. Default is false.
        """
        return pulumi.get(self, 'online_prediction_logging')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter
    def regions(self) -> pulumi.Output[Sequence[str]]:
        """
        Optional. The list of regions where the model is going to be deployed. Only one region per model is supported. Defaults to 'us-central1' if nothing is set. See the available regions for AI Platform services. Note: * No matter where a model is deployed, it can always be accessed by users from anywhere, both for online and batch prediction. * The region for a batch prediction job is set by the region field when submitting the batch prediction job and does not take its value from this field.
        """
        return pulumi.get(self, 'regions')