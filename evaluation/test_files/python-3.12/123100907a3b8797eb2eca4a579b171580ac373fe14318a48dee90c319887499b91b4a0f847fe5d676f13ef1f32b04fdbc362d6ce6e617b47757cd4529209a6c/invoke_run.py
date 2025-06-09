import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['InvokeRunArgs', 'InvokeRun']

@pulumi.input_type
class InvokeRunArgs:

    def __init__(__self__, *, compartment_id: pulumi.Input[str], application_id: Optional[pulumi.Input[str]]=None, application_log_config: Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]=None, archive_uri: Optional[pulumi.Input[str]]=None, arguments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, asynchronous: Optional[pulumi.Input[bool]]=None, configuration: Optional[pulumi.Input[Mapping[str, Any]]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, driver_shape: Optional[pulumi.Input[str]]=None, driver_shape_config: Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]=None, execute: Optional[pulumi.Input[str]]=None, executor_shape: Optional[pulumi.Input[str]]=None, executor_shape_config: Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, idle_timeout_in_minutes: Optional[pulumi.Input[str]]=None, logs_bucket_uri: Optional[pulumi.Input[str]]=None, max_duration_in_minutes: Optional[pulumi.Input[str]]=None, metastore_id: Optional[pulumi.Input[str]]=None, num_executors: Optional[pulumi.Input[int]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]=None, spark_version: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None, warehouse_bucket_uri: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a InvokeRun resource.
        :param pulumi.Input[str] compartment_id: (Updatable) The OCID of a compartment.
        :param pulumi.Input[str] application_id: The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        :param pulumi.Input['InvokeRunApplicationLogConfigArgs'] application_log_config: Logging details of Application logs for Data Flow Run.
        :param pulumi.Input[str] archive_uri: A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] arguments: The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        :param pulumi.Input[Mapping[str, Any]] configuration: The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] display_name: A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        :param pulumi.Input[str] driver_shape: The VM shape for the driver. Sets the driver cores and memory.
        :param pulumi.Input['InvokeRunDriverShapeConfigArgs'] driver_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] execute: The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        :param pulumi.Input[str] executor_shape: The VM shape for the executors. Sets the executor cores and memory.
        :param pulumi.Input['InvokeRunExecutorShapeConfigArgs'] executor_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[str] idle_timeout_in_minutes: (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        :param pulumi.Input[str] logs_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[str] max_duration_in_minutes: (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        :param pulumi.Input[str] metastore_id: The OCID of Oracle Cloud Infrastructure Hive Metastore.
        :param pulumi.Input[int] num_executors: The number of executor VMs requested.
        :param pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]] parameters: An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        :param pulumi.Input[str] spark_version: The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        :param pulumi.Input[str] type: The Spark application processing type.
        :param pulumi.Input[str] warehouse_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if application_id is not None:
            pulumi.set(__self__, 'application_id', application_id)
        if application_log_config is not None:
            pulumi.set(__self__, 'application_log_config', application_log_config)
        if archive_uri is not None:
            pulumi.set(__self__, 'archive_uri', archive_uri)
        if arguments is not None:
            pulumi.set(__self__, 'arguments', arguments)
        if asynchronous is not None:
            pulumi.set(__self__, 'asynchronous', asynchronous)
        if configuration is not None:
            pulumi.set(__self__, 'configuration', configuration)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if driver_shape is not None:
            pulumi.set(__self__, 'driver_shape', driver_shape)
        if driver_shape_config is not None:
            pulumi.set(__self__, 'driver_shape_config', driver_shape_config)
        if execute is not None:
            pulumi.set(__self__, 'execute', execute)
        if executor_shape is not None:
            pulumi.set(__self__, 'executor_shape', executor_shape)
        if executor_shape_config is not None:
            pulumi.set(__self__, 'executor_shape_config', executor_shape_config)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if idle_timeout_in_minutes is not None:
            pulumi.set(__self__, 'idle_timeout_in_minutes', idle_timeout_in_minutes)
        if logs_bucket_uri is not None:
            pulumi.set(__self__, 'logs_bucket_uri', logs_bucket_uri)
        if max_duration_in_minutes is not None:
            pulumi.set(__self__, 'max_duration_in_minutes', max_duration_in_minutes)
        if metastore_id is not None:
            pulumi.set(__self__, 'metastore_id', metastore_id)
        if num_executors is not None:
            pulumi.set(__self__, 'num_executors', num_executors)
        if parameters is not None:
            pulumi.set(__self__, 'parameters', parameters)
        if spark_version is not None:
            pulumi.set(__self__, 'spark_version', spark_version)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if warehouse_bucket_uri is not None:
            pulumi.set(__self__, 'warehouse_bucket_uri', warehouse_bucket_uri)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Input[str]:
        """
        (Updatable) The OCID of a compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter(name='applicationId')
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        """
        return pulumi.get(self, 'application_id')

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'application_id', value)

    @property
    @pulumi.getter(name='applicationLogConfig')
    def application_log_config(self) -> Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]:
        """
        Logging details of Application logs for Data Flow Run.
        """
        return pulumi.get(self, 'application_log_config')

    @application_log_config.setter
    def application_log_config(self, value: Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]):
        pulumi.set(self, 'application_log_config', value)

    @property
    @pulumi.getter(name='archiveUri')
    def archive_uri(self) -> Optional[pulumi.Input[str]]:
        """
        A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'archive_uri')

    @archive_uri.setter
    def archive_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'archive_uri', value)

    @property
    @pulumi.getter
    def arguments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        """
        return pulumi.get(self, 'arguments')

    @arguments.setter
    def arguments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'arguments', value)

    @property
    @pulumi.getter
    def asynchronous(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, 'asynchronous')

    @asynchronous.setter
    def asynchronous(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'asynchronous', value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        """
        return pulumi.get(self, 'configuration')

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'configuration', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='driverShape')
    def driver_shape(self) -> Optional[pulumi.Input[str]]:
        """
        The VM shape for the driver. Sets the driver cores and memory.
        """
        return pulumi.get(self, 'driver_shape')

    @driver_shape.setter
    def driver_shape(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'driver_shape', value)

    @property
    @pulumi.getter(name='driverShapeConfig')
    def driver_shape_config(self) -> Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'driver_shape_config')

    @driver_shape_config.setter
    def driver_shape_config(self, value: Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]):
        pulumi.set(self, 'driver_shape_config', value)

    @property
    @pulumi.getter
    def execute(self) -> Optional[pulumi.Input[str]]:
        """
        The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        """
        return pulumi.get(self, 'execute')

    @execute.setter
    def execute(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'execute', value)

    @property
    @pulumi.getter(name='executorShape')
    def executor_shape(self) -> Optional[pulumi.Input[str]]:
        """
        The VM shape for the executors. Sets the executor cores and memory.
        """
        return pulumi.get(self, 'executor_shape')

    @executor_shape.setter
    def executor_shape(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'executor_shape', value)

    @property
    @pulumi.getter(name='executorShapeConfig')
    def executor_shape_config(self) -> Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'executor_shape_config')

    @executor_shape_config.setter
    def executor_shape_config(self, value: Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]):
        pulumi.set(self, 'executor_shape_config', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='idleTimeoutInMinutes')
    def idle_timeout_in_minutes(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        """
        return pulumi.get(self, 'idle_timeout_in_minutes')

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'idle_timeout_in_minutes', value)

    @property
    @pulumi.getter(name='logsBucketUri')
    def logs_bucket_uri(self) -> Optional[pulumi.Input[str]]:
        """
        An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'logs_bucket_uri')

    @logs_bucket_uri.setter
    def logs_bucket_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'logs_bucket_uri', value)

    @property
    @pulumi.getter(name='maxDurationInMinutes')
    def max_duration_in_minutes(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        """
        return pulumi.get(self, 'max_duration_in_minutes')

    @max_duration_in_minutes.setter
    def max_duration_in_minutes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'max_duration_in_minutes', value)

    @property
    @pulumi.getter(name='metastoreId')
    def metastore_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of Oracle Cloud Infrastructure Hive Metastore.
        """
        return pulumi.get(self, 'metastore_id')

    @metastore_id.setter
    def metastore_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'metastore_id', value)

    @property
    @pulumi.getter(name='numExecutors')
    def num_executors(self) -> Optional[pulumi.Input[int]]:
        """
        The number of executor VMs requested.
        """
        return pulumi.get(self, 'num_executors')

    @num_executors.setter
    def num_executors(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'num_executors', value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]:
        """
        An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        """
        return pulumi.get(self, 'parameters')

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]):
        pulumi.set(self, 'parameters', value)

    @property
    @pulumi.getter(name='sparkVersion')
    def spark_version(self) -> Optional[pulumi.Input[str]]:
        """
        The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        """
        return pulumi.get(self, 'spark_version')

    @spark_version.setter
    def spark_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'spark_version', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The Spark application processing type.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='warehouseBucketUri')
    def warehouse_bucket_uri(self) -> Optional[pulumi.Input[str]]:
        """
        An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'warehouse_bucket_uri')

    @warehouse_bucket_uri.setter
    def warehouse_bucket_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'warehouse_bucket_uri', value)

@pulumi.input_type
class _InvokeRunState:

    def __init__(__self__, *, application_id: Optional[pulumi.Input[str]]=None, application_log_config: Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]=None, archive_uri: Optional[pulumi.Input[str]]=None, arguments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, asynchronous: Optional[pulumi.Input[bool]]=None, class_name: Optional[pulumi.Input[str]]=None, compartment_id: Optional[pulumi.Input[str]]=None, configuration: Optional[pulumi.Input[Mapping[str, Any]]]=None, data_read_in_bytes: Optional[pulumi.Input[str]]=None, data_written_in_bytes: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, driver_shape: Optional[pulumi.Input[str]]=None, driver_shape_config: Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]=None, execute: Optional[pulumi.Input[str]]=None, executor_shape: Optional[pulumi.Input[str]]=None, executor_shape_config: Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]=None, file_uri: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, idle_timeout_in_minutes: Optional[pulumi.Input[str]]=None, language: Optional[pulumi.Input[str]]=None, lifecycle_details: Optional[pulumi.Input[str]]=None, logs_bucket_uri: Optional[pulumi.Input[str]]=None, max_duration_in_minutes: Optional[pulumi.Input[str]]=None, metastore_id: Optional[pulumi.Input[str]]=None, num_executors: Optional[pulumi.Input[int]]=None, opc_request_id: Optional[pulumi.Input[str]]=None, owner_principal_id: Optional[pulumi.Input[str]]=None, owner_user_name: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]=None, private_endpoint_dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, private_endpoint_max_host_count: Optional[pulumi.Input[int]]=None, private_endpoint_nsg_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, private_endpoint_subnet_id: Optional[pulumi.Input[str]]=None, run_duration_in_milliseconds: Optional[pulumi.Input[str]]=None, spark_version: Optional[pulumi.Input[str]]=None, state: Optional[pulumi.Input[str]]=None, time_created: Optional[pulumi.Input[str]]=None, time_updated: Optional[pulumi.Input[str]]=None, total_ocpu: Optional[pulumi.Input[int]]=None, type: Optional[pulumi.Input[str]]=None, warehouse_bucket_uri: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering InvokeRun resources.
        :param pulumi.Input[str] application_id: The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        :param pulumi.Input['InvokeRunApplicationLogConfigArgs'] application_log_config: Logging details of Application logs for Data Flow Run.
        :param pulumi.Input[str] archive_uri: A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] arguments: The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        :param pulumi.Input[str] class_name: The class for the application.
        :param pulumi.Input[str] compartment_id: (Updatable) The OCID of a compartment.
        :param pulumi.Input[Mapping[str, Any]] configuration: The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        :param pulumi.Input[str] data_read_in_bytes: The data read by the run in bytes.
        :param pulumi.Input[str] data_written_in_bytes: The data written by the run in bytes.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] display_name: A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        :param pulumi.Input[str] driver_shape: The VM shape for the driver. Sets the driver cores and memory.
        :param pulumi.Input['InvokeRunDriverShapeConfigArgs'] driver_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] execute: The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        :param pulumi.Input[str] executor_shape: The VM shape for the executors. Sets the executor cores and memory.
        :param pulumi.Input['InvokeRunExecutorShapeConfigArgs'] executor_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] file_uri: An Oracle Cloud Infrastructure URI of the file containing the application to execute. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[str] idle_timeout_in_minutes: (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        :param pulumi.Input[str] language: The Spark language.
        :param pulumi.Input[str] lifecycle_details: The detailed messages about the lifecycle state.
        :param pulumi.Input[str] logs_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[str] max_duration_in_minutes: (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        :param pulumi.Input[str] metastore_id: The OCID of Oracle Cloud Infrastructure Hive Metastore.
        :param pulumi.Input[int] num_executors: The number of executor VMs requested.
        :param pulumi.Input[str] opc_request_id: Unique Oracle assigned identifier for the request. If you need to contact Oracle about a particular request, please provide the request ID.
        :param pulumi.Input[str] owner_principal_id: The OCID of the user who created the resource.
        :param pulumi.Input[str] owner_user_name: The username of the user who created the resource.  If the username of the owner does not exist, `null` will be returned and the caller should refer to the ownerPrincipalId value instead.
        :param pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]] parameters: An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_endpoint_dns_zones: An array of DNS zone names. Example: `[ "app.examplecorp.com", "app.examplecorp2.com" ]`
        :param pulumi.Input[str] private_endpoint_id: The OCID of a private endpoint.
        :param pulumi.Input[int] private_endpoint_max_host_count: The maximum number of hosts to be accessed through the private endpoint. This value is used to calculate the relevant CIDR block and should be a multiple of 256.  If the value is not a multiple of 256, it is rounded up to the next multiple of 256. For example, 300 is rounded up to 512.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_endpoint_nsg_ids: An array of network security group OCIDs.
        :param pulumi.Input[str] private_endpoint_subnet_id: The OCID of a subnet.
        :param pulumi.Input[str] run_duration_in_milliseconds: The duration of the run in milliseconds.
        :param pulumi.Input[str] spark_version: The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        :param pulumi.Input[str] state: The current state of this run.
        :param pulumi.Input[str] time_created: The date and time a application was created, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        :param pulumi.Input[str] time_updated: The date and time a application was updated, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        :param pulumi.Input[int] total_ocpu: The total number of oCPU requested by the run.
        :param pulumi.Input[str] type: The Spark application processing type.
        :param pulumi.Input[str] warehouse_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        if application_id is not None:
            pulumi.set(__self__, 'application_id', application_id)
        if application_log_config is not None:
            pulumi.set(__self__, 'application_log_config', application_log_config)
        if archive_uri is not None:
            pulumi.set(__self__, 'archive_uri', archive_uri)
        if arguments is not None:
            pulumi.set(__self__, 'arguments', arguments)
        if asynchronous is not None:
            pulumi.set(__self__, 'asynchronous', asynchronous)
        if class_name is not None:
            pulumi.set(__self__, 'class_name', class_name)
        if compartment_id is not None:
            pulumi.set(__self__, 'compartment_id', compartment_id)
        if configuration is not None:
            pulumi.set(__self__, 'configuration', configuration)
        if data_read_in_bytes is not None:
            pulumi.set(__self__, 'data_read_in_bytes', data_read_in_bytes)
        if data_written_in_bytes is not None:
            pulumi.set(__self__, 'data_written_in_bytes', data_written_in_bytes)
        if defined_tags is not None:
            pulumi.set(__self__, 'defined_tags', defined_tags)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if driver_shape is not None:
            pulumi.set(__self__, 'driver_shape', driver_shape)
        if driver_shape_config is not None:
            pulumi.set(__self__, 'driver_shape_config', driver_shape_config)
        if execute is not None:
            pulumi.set(__self__, 'execute', execute)
        if executor_shape is not None:
            pulumi.set(__self__, 'executor_shape', executor_shape)
        if executor_shape_config is not None:
            pulumi.set(__self__, 'executor_shape_config', executor_shape_config)
        if file_uri is not None:
            pulumi.set(__self__, 'file_uri', file_uri)
        if freeform_tags is not None:
            pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if idle_timeout_in_minutes is not None:
            pulumi.set(__self__, 'idle_timeout_in_minutes', idle_timeout_in_minutes)
        if language is not None:
            pulumi.set(__self__, 'language', language)
        if lifecycle_details is not None:
            pulumi.set(__self__, 'lifecycle_details', lifecycle_details)
        if logs_bucket_uri is not None:
            pulumi.set(__self__, 'logs_bucket_uri', logs_bucket_uri)
        if max_duration_in_minutes is not None:
            pulumi.set(__self__, 'max_duration_in_minutes', max_duration_in_minutes)
        if metastore_id is not None:
            pulumi.set(__self__, 'metastore_id', metastore_id)
        if num_executors is not None:
            pulumi.set(__self__, 'num_executors', num_executors)
        if opc_request_id is not None:
            pulumi.set(__self__, 'opc_request_id', opc_request_id)
        if owner_principal_id is not None:
            pulumi.set(__self__, 'owner_principal_id', owner_principal_id)
        if owner_user_name is not None:
            pulumi.set(__self__, 'owner_user_name', owner_user_name)
        if parameters is not None:
            pulumi.set(__self__, 'parameters', parameters)
        if private_endpoint_dns_zones is not None:
            pulumi.set(__self__, 'private_endpoint_dns_zones', private_endpoint_dns_zones)
        if private_endpoint_id is not None:
            pulumi.set(__self__, 'private_endpoint_id', private_endpoint_id)
        if private_endpoint_max_host_count is not None:
            pulumi.set(__self__, 'private_endpoint_max_host_count', private_endpoint_max_host_count)
        if private_endpoint_nsg_ids is not None:
            pulumi.set(__self__, 'private_endpoint_nsg_ids', private_endpoint_nsg_ids)
        if private_endpoint_subnet_id is not None:
            pulumi.set(__self__, 'private_endpoint_subnet_id', private_endpoint_subnet_id)
        if run_duration_in_milliseconds is not None:
            pulumi.set(__self__, 'run_duration_in_milliseconds', run_duration_in_milliseconds)
        if spark_version is not None:
            pulumi.set(__self__, 'spark_version', spark_version)
        if state is not None:
            pulumi.set(__self__, 'state', state)
        if time_created is not None:
            pulumi.set(__self__, 'time_created', time_created)
        if time_updated is not None:
            pulumi.set(__self__, 'time_updated', time_updated)
        if total_ocpu is not None:
            pulumi.set(__self__, 'total_ocpu', total_ocpu)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if warehouse_bucket_uri is not None:
            pulumi.set(__self__, 'warehouse_bucket_uri', warehouse_bucket_uri)

    @property
    @pulumi.getter(name='applicationId')
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        """
        return pulumi.get(self, 'application_id')

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'application_id', value)

    @property
    @pulumi.getter(name='applicationLogConfig')
    def application_log_config(self) -> Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]:
        """
        Logging details of Application logs for Data Flow Run.
        """
        return pulumi.get(self, 'application_log_config')

    @application_log_config.setter
    def application_log_config(self, value: Optional[pulumi.Input['InvokeRunApplicationLogConfigArgs']]):
        pulumi.set(self, 'application_log_config', value)

    @property
    @pulumi.getter(name='archiveUri')
    def archive_uri(self) -> Optional[pulumi.Input[str]]:
        """
        A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'archive_uri')

    @archive_uri.setter
    def archive_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'archive_uri', value)

    @property
    @pulumi.getter
    def arguments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        """
        return pulumi.get(self, 'arguments')

    @arguments.setter
    def arguments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'arguments', value)

    @property
    @pulumi.getter
    def asynchronous(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, 'asynchronous')

    @asynchronous.setter
    def asynchronous(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'asynchronous', value)

    @property
    @pulumi.getter(name='className')
    def class_name(self) -> Optional[pulumi.Input[str]]:
        """
        The class for the application.
        """
        return pulumi.get(self, 'class_name')

    @class_name.setter
    def class_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'class_name', value)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The OCID of a compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @compartment_id.setter
    def compartment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'compartment_id', value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        """
        return pulumi.get(self, 'configuration')

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'configuration', value)

    @property
    @pulumi.getter(name='dataReadInBytes')
    def data_read_in_bytes(self) -> Optional[pulumi.Input[str]]:
        """
        The data read by the run in bytes.
        """
        return pulumi.get(self, 'data_read_in_bytes')

    @data_read_in_bytes.setter
    def data_read_in_bytes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'data_read_in_bytes', value)

    @property
    @pulumi.getter(name='dataWrittenInBytes')
    def data_written_in_bytes(self) -> Optional[pulumi.Input[str]]:
        """
        The data written by the run in bytes.
        """
        return pulumi.get(self, 'data_written_in_bytes')

    @data_written_in_bytes.setter
    def data_written_in_bytes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'data_written_in_bytes', value)

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @defined_tags.setter
    def defined_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'defined_tags', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='driverShape')
    def driver_shape(self) -> Optional[pulumi.Input[str]]:
        """
        The VM shape for the driver. Sets the driver cores and memory.
        """
        return pulumi.get(self, 'driver_shape')

    @driver_shape.setter
    def driver_shape(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'driver_shape', value)

    @property
    @pulumi.getter(name='driverShapeConfig')
    def driver_shape_config(self) -> Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'driver_shape_config')

    @driver_shape_config.setter
    def driver_shape_config(self, value: Optional[pulumi.Input['InvokeRunDriverShapeConfigArgs']]):
        pulumi.set(self, 'driver_shape_config', value)

    @property
    @pulumi.getter
    def execute(self) -> Optional[pulumi.Input[str]]:
        """
        The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        """
        return pulumi.get(self, 'execute')

    @execute.setter
    def execute(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'execute', value)

    @property
    @pulumi.getter(name='executorShape')
    def executor_shape(self) -> Optional[pulumi.Input[str]]:
        """
        The VM shape for the executors. Sets the executor cores and memory.
        """
        return pulumi.get(self, 'executor_shape')

    @executor_shape.setter
    def executor_shape(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'executor_shape', value)

    @property
    @pulumi.getter(name='executorShapeConfig')
    def executor_shape_config(self) -> Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'executor_shape_config')

    @executor_shape_config.setter
    def executor_shape_config(self, value: Optional[pulumi.Input['InvokeRunExecutorShapeConfigArgs']]):
        pulumi.set(self, 'executor_shape_config', value)

    @property
    @pulumi.getter(name='fileUri')
    def file_uri(self) -> Optional[pulumi.Input[str]]:
        """
        An Oracle Cloud Infrastructure URI of the file containing the application to execute. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'file_uri')

    @file_uri.setter
    def file_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'file_uri', value)

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @freeform_tags.setter
    def freeform_tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'freeform_tags', value)

    @property
    @pulumi.getter(name='idleTimeoutInMinutes')
    def idle_timeout_in_minutes(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        """
        return pulumi.get(self, 'idle_timeout_in_minutes')

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'idle_timeout_in_minutes', value)

    @property
    @pulumi.getter
    def language(self) -> Optional[pulumi.Input[str]]:
        """
        The Spark language.
        """
        return pulumi.get(self, 'language')

    @language.setter
    def language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'language', value)

    @property
    @pulumi.getter(name='lifecycleDetails')
    def lifecycle_details(self) -> Optional[pulumi.Input[str]]:
        """
        The detailed messages about the lifecycle state.
        """
        return pulumi.get(self, 'lifecycle_details')

    @lifecycle_details.setter
    def lifecycle_details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'lifecycle_details', value)

    @property
    @pulumi.getter(name='logsBucketUri')
    def logs_bucket_uri(self) -> Optional[pulumi.Input[str]]:
        """
        An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'logs_bucket_uri')

    @logs_bucket_uri.setter
    def logs_bucket_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'logs_bucket_uri', value)

    @property
    @pulumi.getter(name='maxDurationInMinutes')
    def max_duration_in_minutes(self) -> Optional[pulumi.Input[str]]:
        """
        (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        """
        return pulumi.get(self, 'max_duration_in_minutes')

    @max_duration_in_minutes.setter
    def max_duration_in_minutes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'max_duration_in_minutes', value)

    @property
    @pulumi.getter(name='metastoreId')
    def metastore_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of Oracle Cloud Infrastructure Hive Metastore.
        """
        return pulumi.get(self, 'metastore_id')

    @metastore_id.setter
    def metastore_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'metastore_id', value)

    @property
    @pulumi.getter(name='numExecutors')
    def num_executors(self) -> Optional[pulumi.Input[int]]:
        """
        The number of executor VMs requested.
        """
        return pulumi.get(self, 'num_executors')

    @num_executors.setter
    def num_executors(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'num_executors', value)

    @property
    @pulumi.getter(name='opcRequestId')
    def opc_request_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique Oracle assigned identifier for the request. If you need to contact Oracle about a particular request, please provide the request ID.
        """
        return pulumi.get(self, 'opc_request_id')

    @opc_request_id.setter
    def opc_request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'opc_request_id', value)

    @property
    @pulumi.getter(name='ownerPrincipalId')
    def owner_principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the user who created the resource.
        """
        return pulumi.get(self, 'owner_principal_id')

    @owner_principal_id.setter
    def owner_principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'owner_principal_id', value)

    @property
    @pulumi.getter(name='ownerUserName')
    def owner_user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The username of the user who created the resource.  If the username of the owner does not exist, `null` will be returned and the caller should refer to the ownerPrincipalId value instead.
        """
        return pulumi.get(self, 'owner_user_name')

    @owner_user_name.setter
    def owner_user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'owner_user_name', value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]:
        """
        An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        """
        return pulumi.get(self, 'parameters')

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InvokeRunParameterArgs']]]]):
        pulumi.set(self, 'parameters', value)

    @property
    @pulumi.getter(name='privateEndpointDnsZones')
    def private_endpoint_dns_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of DNS zone names. Example: `[ "app.examplecorp.com", "app.examplecorp2.com" ]`
        """
        return pulumi.get(self, 'private_endpoint_dns_zones')

    @private_endpoint_dns_zones.setter
    def private_endpoint_dns_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'private_endpoint_dns_zones', value)

    @property
    @pulumi.getter(name='privateEndpointId')
    def private_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of a private endpoint.
        """
        return pulumi.get(self, 'private_endpoint_id')

    @private_endpoint_id.setter
    def private_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_id', value)

    @property
    @pulumi.getter(name='privateEndpointMaxHostCount')
    def private_endpoint_max_host_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of hosts to be accessed through the private endpoint. This value is used to calculate the relevant CIDR block and should be a multiple of 256.  If the value is not a multiple of 256, it is rounded up to the next multiple of 256. For example, 300 is rounded up to 512.
        """
        return pulumi.get(self, 'private_endpoint_max_host_count')

    @private_endpoint_max_host_count.setter
    def private_endpoint_max_host_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'private_endpoint_max_host_count', value)

    @property
    @pulumi.getter(name='privateEndpointNsgIds')
    def private_endpoint_nsg_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of network security group OCIDs.
        """
        return pulumi.get(self, 'private_endpoint_nsg_ids')

    @private_endpoint_nsg_ids.setter
    def private_endpoint_nsg_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'private_endpoint_nsg_ids', value)

    @property
    @pulumi.getter(name='privateEndpointSubnetId')
    def private_endpoint_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of a subnet.
        """
        return pulumi.get(self, 'private_endpoint_subnet_id')

    @private_endpoint_subnet_id.setter
    def private_endpoint_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_subnet_id', value)

    @property
    @pulumi.getter(name='runDurationInMilliseconds')
    def run_duration_in_milliseconds(self) -> Optional[pulumi.Input[str]]:
        """
        The duration of the run in milliseconds.
        """
        return pulumi.get(self, 'run_duration_in_milliseconds')

    @run_duration_in_milliseconds.setter
    def run_duration_in_milliseconds(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'run_duration_in_milliseconds', value)

    @property
    @pulumi.getter(name='sparkVersion')
    def spark_version(self) -> Optional[pulumi.Input[str]]:
        """
        The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        """
        return pulumi.get(self, 'spark_version')

    @spark_version.setter
    def spark_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'spark_version', value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of this run.
        """
        return pulumi.get(self, 'state')

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'state', value)

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time a application was created, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_created')

    @time_created.setter
    def time_created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'time_created', value)

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time a application was updated, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_updated')

    @time_updated.setter
    def time_updated(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'time_updated', value)

    @property
    @pulumi.getter(name='totalOcpu')
    def total_ocpu(self) -> Optional[pulumi.Input[int]]:
        """
        The total number of oCPU requested by the run.
        """
        return pulumi.get(self, 'total_ocpu')

    @total_ocpu.setter
    def total_ocpu(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'total_ocpu', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The Spark application processing type.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='warehouseBucketUri')
    def warehouse_bucket_uri(self) -> Optional[pulumi.Input[str]]:
        """
        An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'warehouse_bucket_uri')

    @warehouse_bucket_uri.setter
    def warehouse_bucket_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'warehouse_bucket_uri', value)

class InvokeRun(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_id: Optional[pulumi.Input[str]]=None, application_log_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunApplicationLogConfigArgs']]]=None, archive_uri: Optional[pulumi.Input[str]]=None, arguments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, asynchronous: Optional[pulumi.Input[bool]]=None, compartment_id: Optional[pulumi.Input[str]]=None, configuration: Optional[pulumi.Input[Mapping[str, Any]]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, driver_shape: Optional[pulumi.Input[str]]=None, driver_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunDriverShapeConfigArgs']]]=None, execute: Optional[pulumi.Input[str]]=None, executor_shape: Optional[pulumi.Input[str]]=None, executor_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunExecutorShapeConfigArgs']]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, idle_timeout_in_minutes: Optional[pulumi.Input[str]]=None, logs_bucket_uri: Optional[pulumi.Input[str]]=None, max_duration_in_minutes: Optional[pulumi.Input[str]]=None, metastore_id: Optional[pulumi.Input[str]]=None, num_executors: Optional[pulumi.Input[int]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InvokeRunParameterArgs']]]]]=None, spark_version: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None, warehouse_bucket_uri: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        This resource provides the Invoke Run resource in Oracle Cloud Infrastructure Data Flow service.

        Creates a run for an application.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_invoke_run = oci.data_flow.InvokeRun("testInvokeRun",
            compartment_id=var["compartment_id"],
            application_id=oci_dataflow_application["test_application"]["id"],
            application_log_config=oci.data_flow.InvokeRunApplicationLogConfigArgs(
                log_group_id=oci_logging_log_group["test_log_group"]["id"],
                log_id=oci_logging_log["test_log"]["id"],
            ),
            archive_uri=var["invoke_run_archive_uri"],
            arguments=var["invoke_run_arguments"],
            configuration=var["invoke_run_configuration"],
            defined_tags={
                "Operations.CostCenter": "42",
            },
            display_name=var["invoke_run_display_name"],
            driver_shape=var["invoke_run_driver_shape"],
            driver_shape_config=oci.data_flow.InvokeRunDriverShapeConfigArgs(
                memory_in_gbs=var["invoke_run_driver_shape_config_memory_in_gbs"],
                ocpus=var["invoke_run_driver_shape_config_ocpus"],
            ),
            execute=var["invoke_run_execute"],
            executor_shape=var["invoke_run_executor_shape"],
            executor_shape_config=oci.data_flow.InvokeRunExecutorShapeConfigArgs(
                memory_in_gbs=var["invoke_run_executor_shape_config_memory_in_gbs"],
                ocpus=var["invoke_run_executor_shape_config_ocpus"],
            ),
            freeform_tags={
                "Department": "Finance",
            },
            idle_timeout_in_minutes=var["invoke_run_idle_timeout_in_minutes"],
            logs_bucket_uri=var["invoke_run_logs_bucket_uri"],
            max_duration_in_minutes=var["invoke_run_max_duration_in_minutes"],
            metastore_id=var["metastore_id"],
            num_executors=var["invoke_run_num_executors"],
            parameters=[oci.data_flow.InvokeRunParameterArgs(
                name=var["invoke_run_parameters_name"],
                value=var["invoke_run_parameters_value"],
            )],
            spark_version=var["invoke_run_spark_version"],
            type=var["invoke_run_type"],
            warehouse_bucket_uri=var["invoke_run_warehouse_bucket_uri"])
        ```
        ## Note

        At a time service allows only one run to succeed if user is trying to invoke runs on multiple applications which have Private Endpoints and service will proceed invoking only one run and put the rest of them in failed state.

        ## Import

        InvokeRuns can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:DataFlow/invokeRun:InvokeRun test_invoke_run "id"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        :param pulumi.Input[pulumi.InputType['InvokeRunApplicationLogConfigArgs']] application_log_config: Logging details of Application logs for Data Flow Run.
        :param pulumi.Input[str] archive_uri: A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] arguments: The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        :param pulumi.Input[str] compartment_id: (Updatable) The OCID of a compartment.
        :param pulumi.Input[Mapping[str, Any]] configuration: The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] display_name: A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        :param pulumi.Input[str] driver_shape: The VM shape for the driver. Sets the driver cores and memory.
        :param pulumi.Input[pulumi.InputType['InvokeRunDriverShapeConfigArgs']] driver_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] execute: The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        :param pulumi.Input[str] executor_shape: The VM shape for the executors. Sets the executor cores and memory.
        :param pulumi.Input[pulumi.InputType['InvokeRunExecutorShapeConfigArgs']] executor_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[str] idle_timeout_in_minutes: (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        :param pulumi.Input[str] logs_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[str] max_duration_in_minutes: (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        :param pulumi.Input[str] metastore_id: The OCID of Oracle Cloud Infrastructure Hive Metastore.
        :param pulumi.Input[int] num_executors: The number of executor VMs requested.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InvokeRunParameterArgs']]]] parameters: An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        :param pulumi.Input[str] spark_version: The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        :param pulumi.Input[str] type: The Spark application processing type.
        :param pulumi.Input[str] warehouse_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: InvokeRunArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        This resource provides the Invoke Run resource in Oracle Cloud Infrastructure Data Flow service.

        Creates a run for an application.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_oci as oci

        test_invoke_run = oci.data_flow.InvokeRun("testInvokeRun",
            compartment_id=var["compartment_id"],
            application_id=oci_dataflow_application["test_application"]["id"],
            application_log_config=oci.data_flow.InvokeRunApplicationLogConfigArgs(
                log_group_id=oci_logging_log_group["test_log_group"]["id"],
                log_id=oci_logging_log["test_log"]["id"],
            ),
            archive_uri=var["invoke_run_archive_uri"],
            arguments=var["invoke_run_arguments"],
            configuration=var["invoke_run_configuration"],
            defined_tags={
                "Operations.CostCenter": "42",
            },
            display_name=var["invoke_run_display_name"],
            driver_shape=var["invoke_run_driver_shape"],
            driver_shape_config=oci.data_flow.InvokeRunDriverShapeConfigArgs(
                memory_in_gbs=var["invoke_run_driver_shape_config_memory_in_gbs"],
                ocpus=var["invoke_run_driver_shape_config_ocpus"],
            ),
            execute=var["invoke_run_execute"],
            executor_shape=var["invoke_run_executor_shape"],
            executor_shape_config=oci.data_flow.InvokeRunExecutorShapeConfigArgs(
                memory_in_gbs=var["invoke_run_executor_shape_config_memory_in_gbs"],
                ocpus=var["invoke_run_executor_shape_config_ocpus"],
            ),
            freeform_tags={
                "Department": "Finance",
            },
            idle_timeout_in_minutes=var["invoke_run_idle_timeout_in_minutes"],
            logs_bucket_uri=var["invoke_run_logs_bucket_uri"],
            max_duration_in_minutes=var["invoke_run_max_duration_in_minutes"],
            metastore_id=var["metastore_id"],
            num_executors=var["invoke_run_num_executors"],
            parameters=[oci.data_flow.InvokeRunParameterArgs(
                name=var["invoke_run_parameters_name"],
                value=var["invoke_run_parameters_value"],
            )],
            spark_version=var["invoke_run_spark_version"],
            type=var["invoke_run_type"],
            warehouse_bucket_uri=var["invoke_run_warehouse_bucket_uri"])
        ```
        ## Note

        At a time service allows only one run to succeed if user is trying to invoke runs on multiple applications which have Private Endpoints and service will proceed invoking only one run and put the rest of them in failed state.

        ## Import

        InvokeRuns can be imported using the `id`, e.g.

        ```sh
         $ pulumi import oci:DataFlow/invokeRun:InvokeRun test_invoke_run "id"
        ```

        :param str resource_name: The name of the resource.
        :param InvokeRunArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InvokeRunArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_id: Optional[pulumi.Input[str]]=None, application_log_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunApplicationLogConfigArgs']]]=None, archive_uri: Optional[pulumi.Input[str]]=None, arguments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, asynchronous: Optional[pulumi.Input[bool]]=None, compartment_id: Optional[pulumi.Input[str]]=None, configuration: Optional[pulumi.Input[Mapping[str, Any]]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, driver_shape: Optional[pulumi.Input[str]]=None, driver_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunDriverShapeConfigArgs']]]=None, execute: Optional[pulumi.Input[str]]=None, executor_shape: Optional[pulumi.Input[str]]=None, executor_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunExecutorShapeConfigArgs']]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, idle_timeout_in_minutes: Optional[pulumi.Input[str]]=None, logs_bucket_uri: Optional[pulumi.Input[str]]=None, max_duration_in_minutes: Optional[pulumi.Input[str]]=None, metastore_id: Optional[pulumi.Input[str]]=None, num_executors: Optional[pulumi.Input[int]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InvokeRunParameterArgs']]]]]=None, spark_version: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None, warehouse_bucket_uri: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InvokeRunArgs.__new__(InvokeRunArgs)
            __props__.__dict__['application_id'] = application_id
            __props__.__dict__['application_log_config'] = application_log_config
            __props__.__dict__['archive_uri'] = archive_uri
            __props__.__dict__['arguments'] = arguments
            __props__.__dict__['asynchronous'] = asynchronous
            if compartment_id is None and (not opts.urn):
                raise TypeError("Missing required property 'compartment_id'")
            __props__.__dict__['compartment_id'] = compartment_id
            __props__.__dict__['configuration'] = configuration
            __props__.__dict__['defined_tags'] = defined_tags
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['driver_shape'] = driver_shape
            __props__.__dict__['driver_shape_config'] = driver_shape_config
            __props__.__dict__['execute'] = execute
            __props__.__dict__['executor_shape'] = executor_shape
            __props__.__dict__['executor_shape_config'] = executor_shape_config
            __props__.__dict__['freeform_tags'] = freeform_tags
            __props__.__dict__['idle_timeout_in_minutes'] = idle_timeout_in_minutes
            __props__.__dict__['logs_bucket_uri'] = logs_bucket_uri
            __props__.__dict__['max_duration_in_minutes'] = max_duration_in_minutes
            __props__.__dict__['metastore_id'] = metastore_id
            __props__.__dict__['num_executors'] = num_executors
            __props__.__dict__['parameters'] = parameters
            __props__.__dict__['spark_version'] = spark_version
            __props__.__dict__['type'] = type
            __props__.__dict__['warehouse_bucket_uri'] = warehouse_bucket_uri
            __props__.__dict__['class_name'] = None
            __props__.__dict__['data_read_in_bytes'] = None
            __props__.__dict__['data_written_in_bytes'] = None
            __props__.__dict__['file_uri'] = None
            __props__.__dict__['language'] = None
            __props__.__dict__['lifecycle_details'] = None
            __props__.__dict__['opc_request_id'] = None
            __props__.__dict__['owner_principal_id'] = None
            __props__.__dict__['owner_user_name'] = None
            __props__.__dict__['private_endpoint_dns_zones'] = None
            __props__.__dict__['private_endpoint_id'] = None
            __props__.__dict__['private_endpoint_max_host_count'] = None
            __props__.__dict__['private_endpoint_nsg_ids'] = None
            __props__.__dict__['private_endpoint_subnet_id'] = None
            __props__.__dict__['run_duration_in_milliseconds'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['time_created'] = None
            __props__.__dict__['time_updated'] = None
            __props__.__dict__['total_ocpu'] = None
        super(InvokeRun, __self__).__init__('oci:DataFlow/invokeRun:InvokeRun', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, application_id: Optional[pulumi.Input[str]]=None, application_log_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunApplicationLogConfigArgs']]]=None, archive_uri: Optional[pulumi.Input[str]]=None, arguments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, asynchronous: Optional[pulumi.Input[bool]]=None, class_name: Optional[pulumi.Input[str]]=None, compartment_id: Optional[pulumi.Input[str]]=None, configuration: Optional[pulumi.Input[Mapping[str, Any]]]=None, data_read_in_bytes: Optional[pulumi.Input[str]]=None, data_written_in_bytes: Optional[pulumi.Input[str]]=None, defined_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, display_name: Optional[pulumi.Input[str]]=None, driver_shape: Optional[pulumi.Input[str]]=None, driver_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunDriverShapeConfigArgs']]]=None, execute: Optional[pulumi.Input[str]]=None, executor_shape: Optional[pulumi.Input[str]]=None, executor_shape_config: Optional[pulumi.Input[pulumi.InputType['InvokeRunExecutorShapeConfigArgs']]]=None, file_uri: Optional[pulumi.Input[str]]=None, freeform_tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, idle_timeout_in_minutes: Optional[pulumi.Input[str]]=None, language: Optional[pulumi.Input[str]]=None, lifecycle_details: Optional[pulumi.Input[str]]=None, logs_bucket_uri: Optional[pulumi.Input[str]]=None, max_duration_in_minutes: Optional[pulumi.Input[str]]=None, metastore_id: Optional[pulumi.Input[str]]=None, num_executors: Optional[pulumi.Input[int]]=None, opc_request_id: Optional[pulumi.Input[str]]=None, owner_principal_id: Optional[pulumi.Input[str]]=None, owner_user_name: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InvokeRunParameterArgs']]]]]=None, private_endpoint_dns_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, private_endpoint_id: Optional[pulumi.Input[str]]=None, private_endpoint_max_host_count: Optional[pulumi.Input[int]]=None, private_endpoint_nsg_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, private_endpoint_subnet_id: Optional[pulumi.Input[str]]=None, run_duration_in_milliseconds: Optional[pulumi.Input[str]]=None, spark_version: Optional[pulumi.Input[str]]=None, state: Optional[pulumi.Input[str]]=None, time_created: Optional[pulumi.Input[str]]=None, time_updated: Optional[pulumi.Input[str]]=None, total_ocpu: Optional[pulumi.Input[int]]=None, type: Optional[pulumi.Input[str]]=None, warehouse_bucket_uri: Optional[pulumi.Input[str]]=None) -> 'InvokeRun':
        """
        Get an existing InvokeRun resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        :param pulumi.Input[pulumi.InputType['InvokeRunApplicationLogConfigArgs']] application_log_config: Logging details of Application logs for Data Flow Run.
        :param pulumi.Input[str] archive_uri: A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] arguments: The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        :param pulumi.Input[str] class_name: The class for the application.
        :param pulumi.Input[str] compartment_id: (Updatable) The OCID of a compartment.
        :param pulumi.Input[Mapping[str, Any]] configuration: The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        :param pulumi.Input[str] data_read_in_bytes: The data read by the run in bytes.
        :param pulumi.Input[str] data_written_in_bytes: The data written by the run in bytes.
        :param pulumi.Input[Mapping[str, Any]] defined_tags: (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        :param pulumi.Input[str] display_name: A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        :param pulumi.Input[str] driver_shape: The VM shape for the driver. Sets the driver cores and memory.
        :param pulumi.Input[pulumi.InputType['InvokeRunDriverShapeConfigArgs']] driver_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] execute: The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        :param pulumi.Input[str] executor_shape: The VM shape for the executors. Sets the executor cores and memory.
        :param pulumi.Input[pulumi.InputType['InvokeRunExecutorShapeConfigArgs']] executor_shape_config: This is used to configure the shape of the driver or executor if a flexible shape is used.
        :param pulumi.Input[str] file_uri: An Oracle Cloud Infrastructure URI of the file containing the application to execute. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[Mapping[str, Any]] freeform_tags: (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        :param pulumi.Input[str] idle_timeout_in_minutes: (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        :param pulumi.Input[str] language: The Spark language.
        :param pulumi.Input[str] lifecycle_details: The detailed messages about the lifecycle state.
        :param pulumi.Input[str] logs_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        :param pulumi.Input[str] max_duration_in_minutes: (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        :param pulumi.Input[str] metastore_id: The OCID of Oracle Cloud Infrastructure Hive Metastore.
        :param pulumi.Input[int] num_executors: The number of executor VMs requested.
        :param pulumi.Input[str] opc_request_id: Unique Oracle assigned identifier for the request. If you need to contact Oracle about a particular request, please provide the request ID.
        :param pulumi.Input[str] owner_principal_id: The OCID of the user who created the resource.
        :param pulumi.Input[str] owner_user_name: The username of the user who created the resource.  If the username of the owner does not exist, `null` will be returned and the caller should refer to the ownerPrincipalId value instead.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InvokeRunParameterArgs']]]] parameters: An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_endpoint_dns_zones: An array of DNS zone names. Example: `[ "app.examplecorp.com", "app.examplecorp2.com" ]`
        :param pulumi.Input[str] private_endpoint_id: The OCID of a private endpoint.
        :param pulumi.Input[int] private_endpoint_max_host_count: The maximum number of hosts to be accessed through the private endpoint. This value is used to calculate the relevant CIDR block and should be a multiple of 256.  If the value is not a multiple of 256, it is rounded up to the next multiple of 256. For example, 300 is rounded up to 512.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] private_endpoint_nsg_ids: An array of network security group OCIDs.
        :param pulumi.Input[str] private_endpoint_subnet_id: The OCID of a subnet.
        :param pulumi.Input[str] run_duration_in_milliseconds: The duration of the run in milliseconds.
        :param pulumi.Input[str] spark_version: The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        :param pulumi.Input[str] state: The current state of this run.
        :param pulumi.Input[str] time_created: The date and time a application was created, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        :param pulumi.Input[str] time_updated: The date and time a application was updated, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        :param pulumi.Input[int] total_ocpu: The total number of oCPU requested by the run.
        :param pulumi.Input[str] type: The Spark application processing type.
        :param pulumi.Input[str] warehouse_bucket_uri: An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _InvokeRunState.__new__(_InvokeRunState)
        __props__.__dict__['application_id'] = application_id
        __props__.__dict__['application_log_config'] = application_log_config
        __props__.__dict__['archive_uri'] = archive_uri
        __props__.__dict__['arguments'] = arguments
        __props__.__dict__['asynchronous'] = asynchronous
        __props__.__dict__['class_name'] = class_name
        __props__.__dict__['compartment_id'] = compartment_id
        __props__.__dict__['configuration'] = configuration
        __props__.__dict__['data_read_in_bytes'] = data_read_in_bytes
        __props__.__dict__['data_written_in_bytes'] = data_written_in_bytes
        __props__.__dict__['defined_tags'] = defined_tags
        __props__.__dict__['display_name'] = display_name
        __props__.__dict__['driver_shape'] = driver_shape
        __props__.__dict__['driver_shape_config'] = driver_shape_config
        __props__.__dict__['execute'] = execute
        __props__.__dict__['executor_shape'] = executor_shape
        __props__.__dict__['executor_shape_config'] = executor_shape_config
        __props__.__dict__['file_uri'] = file_uri
        __props__.__dict__['freeform_tags'] = freeform_tags
        __props__.__dict__['idle_timeout_in_minutes'] = idle_timeout_in_minutes
        __props__.__dict__['language'] = language
        __props__.__dict__['lifecycle_details'] = lifecycle_details
        __props__.__dict__['logs_bucket_uri'] = logs_bucket_uri
        __props__.__dict__['max_duration_in_minutes'] = max_duration_in_minutes
        __props__.__dict__['metastore_id'] = metastore_id
        __props__.__dict__['num_executors'] = num_executors
        __props__.__dict__['opc_request_id'] = opc_request_id
        __props__.__dict__['owner_principal_id'] = owner_principal_id
        __props__.__dict__['owner_user_name'] = owner_user_name
        __props__.__dict__['parameters'] = parameters
        __props__.__dict__['private_endpoint_dns_zones'] = private_endpoint_dns_zones
        __props__.__dict__['private_endpoint_id'] = private_endpoint_id
        __props__.__dict__['private_endpoint_max_host_count'] = private_endpoint_max_host_count
        __props__.__dict__['private_endpoint_nsg_ids'] = private_endpoint_nsg_ids
        __props__.__dict__['private_endpoint_subnet_id'] = private_endpoint_subnet_id
        __props__.__dict__['run_duration_in_milliseconds'] = run_duration_in_milliseconds
        __props__.__dict__['spark_version'] = spark_version
        __props__.__dict__['state'] = state
        __props__.__dict__['time_created'] = time_created
        __props__.__dict__['time_updated'] = time_updated
        __props__.__dict__['total_ocpu'] = total_ocpu
        __props__.__dict__['type'] = type
        __props__.__dict__['warehouse_bucket_uri'] = warehouse_bucket_uri
        return InvokeRun(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='applicationId')
    def application_id(self) -> pulumi.Output[str]:
        """
        The OCID of the associated application. If this value is set, then no value for the execute parameter is required. If this value is not set, then a value for the execute parameter is required, and a new application is created and associated with the new run.
        """
        return pulumi.get(self, 'application_id')

    @property
    @pulumi.getter(name='applicationLogConfig')
    def application_log_config(self) -> pulumi.Output['outputs.InvokeRunApplicationLogConfig']:
        """
        Logging details of Application logs for Data Flow Run.
        """
        return pulumi.get(self, 'application_log_config')

    @property
    @pulumi.getter(name='archiveUri')
    def archive_uri(self) -> pulumi.Output[str]:
        """
        A comma separated list of one or more archive files as Oracle Cloud Infrastructure URIs. For example, ``oci://path/to/a.zip,oci://path/to/b.zip``. An Oracle Cloud Infrastructure URI of an archive.zip file containing custom dependencies that may be used to support the execution of a Python, Java, or Scala application. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'archive_uri')

    @property
    @pulumi.getter
    def arguments(self) -> pulumi.Output[Sequence[str]]:
        """
        The arguments passed to the running application as command line arguments.  An argument is either a plain text or a placeholder. Placeholders are replaced using values from the parameters map.  Each placeholder specified must be represented in the parameters map else the request (POST or PUT) will fail with a HTTP 400 status code.  Placeholders are specified as `Service Api Spec`, where `name` is the name of the parameter. Example:  `[ "--input", "${input_file}", "--name", "John Doe" ]` If "input_file" has a value of "mydata.xml", then the value above will be translated to `--input mydata.xml --name "John Doe"`
        """
        return pulumi.get(self, 'arguments')

    @property
    @pulumi.getter
    def asynchronous(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, 'asynchronous')

    @property
    @pulumi.getter(name='className')
    def class_name(self) -> pulumi.Output[str]:
        """
        The class for the application.
        """
        return pulumi.get(self, 'class_name')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> pulumi.Output[str]:
        """
        (Updatable) The OCID of a compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter
    def configuration(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        The Spark configuration passed to the running process. See https://spark.apache.org/docs/latest/configuration.html#available-properties Example: { "spark.app.name" : "My App Name", "spark.shuffle.io.maxRetries" : "4" } Note: Not all Spark properties are permitted to be set.  Attempting to set a property that is not allowed to be overwritten will cause a 400 status to be returned.
        """
        return pulumi.get(self, 'configuration')

    @property
    @pulumi.getter(name='dataReadInBytes')
    def data_read_in_bytes(self) -> pulumi.Output[str]:
        """
        The data read by the run in bytes.
        """
        return pulumi.get(self, 'data_read_in_bytes')

    @property
    @pulumi.getter(name='dataWrittenInBytes')
    def data_written_in_bytes(self) -> pulumi.Output[str]:
        """
        The data written by the run in bytes.
        """
        return pulumi.get(self, 'data_written_in_bytes')

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Operations.CostCenter": "42"}`
        """
        return pulumi.get(self, 'defined_tags')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        A user-friendly name that does not have to be unique. Avoid entering confidential information. If this value is not specified, it will be derived from the associated application's displayName or set by API using fileUri's application file name.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='driverShape')
    def driver_shape(self) -> pulumi.Output[str]:
        """
        The VM shape for the driver. Sets the driver cores and memory.
        """
        return pulumi.get(self, 'driver_shape')

    @property
    @pulumi.getter(name='driverShapeConfig')
    def driver_shape_config(self) -> pulumi.Output['outputs.InvokeRunDriverShapeConfig']:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'driver_shape_config')

    @property
    @pulumi.getter
    def execute(self) -> pulumi.Output[str]:
        """
        The input used for spark-submit command. For more details see https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit. Supported options include ``--class``, ``--file``, ``--jars``, ``--conf``, ``--py-files``, and main application file with arguments. Example: ``--jars oci://path/to/a.jar,oci://path/to/b.jar --files oci://path/to/a.json,oci://path/to/b.csv --py-files oci://path/to/a.py,oci://path/to/b.py --conf spark.sql.crossJoin.enabled=true --class org.apache.spark.examples.SparkPi oci://path/to/main.jar 10`` Note: If execute is specified together with applicationId, className, configuration, fileUri, language, arguments, parameters during application create/update, or run create/submit, Data Flow service will use derived information from execute input only.
        """
        return pulumi.get(self, 'execute')

    @property
    @pulumi.getter(name='executorShape')
    def executor_shape(self) -> pulumi.Output[str]:
        """
        The VM shape for the executors. Sets the executor cores and memory.
        """
        return pulumi.get(self, 'executor_shape')

    @property
    @pulumi.getter(name='executorShapeConfig')
    def executor_shape_config(self) -> pulumi.Output['outputs.InvokeRunExecutorShapeConfig']:
        """
        This is used to configure the shape of the driver or executor if a flexible shape is used.
        """
        return pulumi.get(self, 'executor_shape_config')

    @property
    @pulumi.getter(name='fileUri')
    def file_uri(self) -> pulumi.Output[str]:
        """
        An Oracle Cloud Infrastructure URI of the file containing the application to execute. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'file_uri')

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        (Updatable) Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). Example: `{"Department": "Finance"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @property
    @pulumi.getter(name='idleTimeoutInMinutes')
    def idle_timeout_in_minutes(self) -> pulumi.Output[str]:
        """
        (Updatable) The timeout value in minutes used to manage Runs. A Run would be stopped after inactivity for this amount of time period. Note: This parameter is currently only applicable for Runs of type `SESSION`. Default value is 2880 minutes (2 days)
        """
        return pulumi.get(self, 'idle_timeout_in_minutes')

    @property
    @pulumi.getter
    def language(self) -> pulumi.Output[str]:
        """
        The Spark language.
        """
        return pulumi.get(self, 'language')

    @property
    @pulumi.getter(name='lifecycleDetails')
    def lifecycle_details(self) -> pulumi.Output[str]:
        """
        The detailed messages about the lifecycle state.
        """
        return pulumi.get(self, 'lifecycle_details')

    @property
    @pulumi.getter(name='logsBucketUri')
    def logs_bucket_uri(self) -> pulumi.Output[str]:
        """
        An Oracle Cloud Infrastructure URI of the bucket where the Spark job logs are to be uploaded. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'logs_bucket_uri')

    @property
    @pulumi.getter(name='maxDurationInMinutes')
    def max_duration_in_minutes(self) -> pulumi.Output[str]:
        """
        (Updatable) The maximum duration in minutes for which an Application should run. Data Flow Run would be terminated once it reaches this duration from the time it transitions to `IN_PROGRESS` state.
        """
        return pulumi.get(self, 'max_duration_in_minutes')

    @property
    @pulumi.getter(name='metastoreId')
    def metastore_id(self) -> pulumi.Output[str]:
        """
        The OCID of Oracle Cloud Infrastructure Hive Metastore.
        """
        return pulumi.get(self, 'metastore_id')

    @property
    @pulumi.getter(name='numExecutors')
    def num_executors(self) -> pulumi.Output[int]:
        """
        The number of executor VMs requested.
        """
        return pulumi.get(self, 'num_executors')

    @property
    @pulumi.getter(name='opcRequestId')
    def opc_request_id(self) -> pulumi.Output[str]:
        """
        Unique Oracle assigned identifier for the request. If you need to contact Oracle about a particular request, please provide the request ID.
        """
        return pulumi.get(self, 'opc_request_id')

    @property
    @pulumi.getter(name='ownerPrincipalId')
    def owner_principal_id(self) -> pulumi.Output[str]:
        """
        The OCID of the user who created the resource.
        """
        return pulumi.get(self, 'owner_principal_id')

    @property
    @pulumi.getter(name='ownerUserName')
    def owner_user_name(self) -> pulumi.Output[str]:
        """
        The username of the user who created the resource.  If the username of the owner does not exist, `null` will be returned and the caller should refer to the ownerPrincipalId value instead.
        """
        return pulumi.get(self, 'owner_user_name')

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Sequence['outputs.InvokeRunParameter']]:
        """
        An array of name/value pairs used to fill placeholders found in properties like `Application.arguments`.  The name must be a string of one or more word characters (a-z, A-Z, 0-9, _).  The value can be a string of 0 or more characters of any kind. Example:  [ { name: "iterations", value: "10"}, { name: "input_file", value: "mydata.xml" }, { name: "variable_x", value: "${x}"} ]
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter(name='privateEndpointDnsZones')
    def private_endpoint_dns_zones(self) -> pulumi.Output[Sequence[str]]:
        """
        An array of DNS zone names. Example: `[ "app.examplecorp.com", "app.examplecorp2.com" ]`
        """
        return pulumi.get(self, 'private_endpoint_dns_zones')

    @property
    @pulumi.getter(name='privateEndpointId')
    def private_endpoint_id(self) -> pulumi.Output[str]:
        """
        The OCID of a private endpoint.
        """
        return pulumi.get(self, 'private_endpoint_id')

    @property
    @pulumi.getter(name='privateEndpointMaxHostCount')
    def private_endpoint_max_host_count(self) -> pulumi.Output[int]:
        """
        The maximum number of hosts to be accessed through the private endpoint. This value is used to calculate the relevant CIDR block and should be a multiple of 256.  If the value is not a multiple of 256, it is rounded up to the next multiple of 256. For example, 300 is rounded up to 512.
        """
        return pulumi.get(self, 'private_endpoint_max_host_count')

    @property
    @pulumi.getter(name='privateEndpointNsgIds')
    def private_endpoint_nsg_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        An array of network security group OCIDs.
        """
        return pulumi.get(self, 'private_endpoint_nsg_ids')

    @property
    @pulumi.getter(name='privateEndpointSubnetId')
    def private_endpoint_subnet_id(self) -> pulumi.Output[str]:
        """
        The OCID of a subnet.
        """
        return pulumi.get(self, 'private_endpoint_subnet_id')

    @property
    @pulumi.getter(name='runDurationInMilliseconds')
    def run_duration_in_milliseconds(self) -> pulumi.Output[str]:
        """
        The duration of the run in milliseconds.
        """
        return pulumi.get(self, 'run_duration_in_milliseconds')

    @property
    @pulumi.getter(name='sparkVersion')
    def spark_version(self) -> pulumi.Output[str]:
        """
        The Spark version utilized to run the application. This value may be set if applicationId is not since the Spark version will be taken from the associated application.
        """
        return pulumi.get(self, 'spark_version')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of this run.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> pulumi.Output[str]:
        """
        The date and time a application was created, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> pulumi.Output[str]:
        """
        The date and time a application was updated, expressed in [RFC 3339](https://tools.ietf.org/html/rfc3339) timestamp format. Example: `2018-04-03T21:10:29.600Z`
        """
        return pulumi.get(self, 'time_updated')

    @property
    @pulumi.getter(name='totalOcpu')
    def total_ocpu(self) -> pulumi.Output[int]:
        """
        The total number of oCPU requested by the run.
        """
        return pulumi.get(self, 'total_ocpu')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The Spark application processing type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='warehouseBucketUri')
    def warehouse_bucket_uri(self) -> pulumi.Output[str]:
        """
        An Oracle Cloud Infrastructure URI of the bucket to be used as default warehouse directory for BATCH SQL runs. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.
        """
        return pulumi.get(self, 'warehouse_bucket_uri')