import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['EnvironmentContainerImageArgs', 'EnvironmentVmImageArgs', 'InstanceAcceleratorConfigArgs', 'InstanceContainerImageArgs', 'InstanceIamBindingConditionArgs', 'InstanceIamMemberConditionArgs', 'InstanceReservationAffinityArgs', 'InstanceShieldedInstanceConfigArgs', 'InstanceVmImageArgs', 'RuntimeAccessConfigArgs', 'RuntimeIamBindingConditionArgs', 'RuntimeIamMemberConditionArgs', 'RuntimeMetricArgs', 'RuntimeSoftwareConfigArgs', 'RuntimeSoftwareConfigKernelArgs', 'RuntimeVirtualMachineArgs', 'RuntimeVirtualMachineVirtualMachineConfigArgs', 'RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs', 'RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs', 'RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs', 'RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs', 'RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs', 'RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs']

@pulumi.input_type
class EnvironmentContainerImageArgs:

    def __init__(__self__, *, repository: pulumi.Input[str], tag: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] repository: The path to the container image repository.
               For example: gcr.io/{project_id}/{imageName}
        :param pulumi.Input[str] tag: The tag of the container image. If not specified, this defaults to the latest tag.
        """
        pulumi.set(__self__, 'repository', repository)
        if tag is not None:
            pulumi.set(__self__, 'tag', tag)

    @property
    @pulumi.getter
    def repository(self) -> pulumi.Input[str]:
        """
        The path to the container image repository.
        For example: gcr.io/{project_id}/{imageName}
        """
        return pulumi.get(self, 'repository')

    @repository.setter
    def repository(self, value: pulumi.Input[str]):
        pulumi.set(self, 'repository', value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        The tag of the container image. If not specified, this defaults to the latest tag.
        """
        return pulumi.get(self, 'tag')

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tag', value)

@pulumi.input_type
class EnvironmentVmImageArgs:

    def __init__(__self__, *, project: pulumi.Input[str], image_family: Optional[pulumi.Input[str]]=None, image_name: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] project: The name of the Google Cloud project that this VM image belongs to.
               Format: projects/{project_id}
        :param pulumi.Input[str] image_family: Use this VM image family to find the image; the newest image in this family will be used.
        :param pulumi.Input[str] image_name: Use VM image name to find the image.
        """
        pulumi.set(__self__, 'project', project)
        if image_family is not None:
            pulumi.set(__self__, 'image_family', image_family)
        if image_name is not None:
            pulumi.set(__self__, 'image_name', image_name)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The name of the Google Cloud project that this VM image belongs to.
        Format: projects/{project_id}
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter(name='imageFamily')
    def image_family(self) -> Optional[pulumi.Input[str]]:
        """
        Use this VM image family to find the image; the newest image in this family will be used.
        """
        return pulumi.get(self, 'image_family')

    @image_family.setter
    def image_family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'image_family', value)

    @property
    @pulumi.getter(name='imageName')
    def image_name(self) -> Optional[pulumi.Input[str]]:
        """
        Use VM image name to find the image.
        """
        return pulumi.get(self, 'image_name')

    @image_name.setter
    def image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'image_name', value)

@pulumi.input_type
class InstanceAcceleratorConfigArgs:

    def __init__(__self__, *, core_count: pulumi.Input[int], type: pulumi.Input[str]):
        """
        :param pulumi.Input[int] core_count: Count of cores of this accelerator.
        :param pulumi.Input[str] type: Type of this accelerator.
               Possible values are `ACCELERATOR_TYPE_UNSPECIFIED`, `NVIDIA_TESLA_K80`, `NVIDIA_TESLA_P100`, `NVIDIA_TESLA_V100`, `NVIDIA_TESLA_P4`, `NVIDIA_TESLA_T4`, `NVIDIA_TESLA_T4_VWS`, `NVIDIA_TESLA_P100_VWS`, `NVIDIA_TESLA_P4_VWS`, `NVIDIA_TESLA_A100`, `TPU_V2`, and `TPU_V3`.
        """
        pulumi.set(__self__, 'core_count', core_count)
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='coreCount')
    def core_count(self) -> pulumi.Input[int]:
        """
        Count of cores of this accelerator.
        """
        return pulumi.get(self, 'core_count')

    @core_count.setter
    def core_count(self, value: pulumi.Input[int]):
        pulumi.set(self, 'core_count', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of this accelerator.
        Possible values are `ACCELERATOR_TYPE_UNSPECIFIED`, `NVIDIA_TESLA_K80`, `NVIDIA_TESLA_P100`, `NVIDIA_TESLA_V100`, `NVIDIA_TESLA_P4`, `NVIDIA_TESLA_T4`, `NVIDIA_TESLA_T4_VWS`, `NVIDIA_TESLA_P100_VWS`, `NVIDIA_TESLA_P4_VWS`, `NVIDIA_TESLA_A100`, `TPU_V2`, and `TPU_V3`.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class InstanceContainerImageArgs:

    def __init__(__self__, *, repository: pulumi.Input[str], tag: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] repository: The path to the container image repository.
               For example: gcr.io/{project_id}/{imageName}
        :param pulumi.Input[str] tag: The tag of the container image. If not specified, this defaults to the latest tag.
        """
        pulumi.set(__self__, 'repository', repository)
        if tag is not None:
            pulumi.set(__self__, 'tag', tag)

    @property
    @pulumi.getter
    def repository(self) -> pulumi.Input[str]:
        """
        The path to the container image repository.
        For example: gcr.io/{project_id}/{imageName}
        """
        return pulumi.get(self, 'repository')

    @repository.setter
    def repository(self, value: pulumi.Input[str]):
        pulumi.set(self, 'repository', value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        The tag of the container image. If not specified, this defaults to the latest tag.
        """
        return pulumi.get(self, 'tag')

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tag', value)

@pulumi.input_type
class InstanceIamBindingConditionArgs:

    def __init__(__self__, *, expression: pulumi.Input[str], title: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None):
        pulumi.set(__self__, 'expression', expression)
        pulumi.set(__self__, 'title', title)
        if description is not None:
            pulumi.set(__self__, 'description', description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'expression')

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, 'expression', value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'title')

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, 'title', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

@pulumi.input_type
class InstanceIamMemberConditionArgs:

    def __init__(__self__, *, expression: pulumi.Input[str], title: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None):
        pulumi.set(__self__, 'expression', expression)
        pulumi.set(__self__, 'title', title)
        if description is not None:
            pulumi.set(__self__, 'description', description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'expression')

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, 'expression', value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'title')

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, 'title', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

@pulumi.input_type
class InstanceReservationAffinityArgs:

    def __init__(__self__, *, consume_reservation_type: pulumi.Input[str], key: Optional[pulumi.Input[str]]=None, values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        :param pulumi.Input[str] consume_reservation_type: The type of Compute Reservation.
               Possible values are `NO_RESERVATION`, `ANY_RESERVATION`, and `SPECIFIC_RESERVATION`.
        :param pulumi.Input[str] key: Corresponds to the label key of reservation resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: Corresponds to the label values of reservation resource.
        """
        pulumi.set(__self__, 'consume_reservation_type', consume_reservation_type)
        if key is not None:
            pulumi.set(__self__, 'key', key)
        if values is not None:
            pulumi.set(__self__, 'values', values)

    @property
    @pulumi.getter(name='consumeReservationType')
    def consume_reservation_type(self) -> pulumi.Input[str]:
        """
        The type of Compute Reservation.
        Possible values are `NO_RESERVATION`, `ANY_RESERVATION`, and `SPECIFIC_RESERVATION`.
        """
        return pulumi.get(self, 'consume_reservation_type')

    @consume_reservation_type.setter
    def consume_reservation_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'consume_reservation_type', value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        Corresponds to the label key of reservation resource.
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Corresponds to the label values of reservation resource.
        """
        return pulumi.get(self, 'values')

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'values', value)

@pulumi.input_type
class InstanceShieldedInstanceConfigArgs:

    def __init__(__self__, *, enable_integrity_monitoring: Optional[pulumi.Input[bool]]=None, enable_secure_boot: Optional[pulumi.Input[bool]]=None, enable_vtpm: Optional[pulumi.Input[bool]]=None):
        """
        :param pulumi.Input[bool] enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the
               boot integrity of the instance. The attestation is performed against the integrity policy baseline.
               This baseline is initially derived from the implicitly trusted boot image when the instance is created.
               Enabled by default.
        :param pulumi.Input[bool] enable_secure_boot: Defines whether the instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs
               authentic software by verifying the digital signature of all boot components, and halting the boot process
               if signature verification fails.
               Disabled by default.
        :param pulumi.Input[bool] enable_vtpm: Defines whether the instance has the vTPM enabled.
               Enabled by default.
        """
        if enable_integrity_monitoring is not None:
            pulumi.set(__self__, 'enable_integrity_monitoring', enable_integrity_monitoring)
        if enable_secure_boot is not None:
            pulumi.set(__self__, 'enable_secure_boot', enable_secure_boot)
        if enable_vtpm is not None:
            pulumi.set(__self__, 'enable_vtpm', enable_vtpm)

    @property
    @pulumi.getter(name='enableIntegrityMonitoring')
    def enable_integrity_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the
        boot integrity of the instance. The attestation is performed against the integrity policy baseline.
        This baseline is initially derived from the implicitly trusted boot image when the instance is created.
        Enabled by default.
        """
        return pulumi.get(self, 'enable_integrity_monitoring')

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_integrity_monitoring', value)

    @property
    @pulumi.getter(name='enableSecureBoot')
    def enable_secure_boot(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs
        authentic software by verifying the digital signature of all boot components, and halting the boot process
        if signature verification fails.
        Disabled by default.
        """
        return pulumi.get(self, 'enable_secure_boot')

    @enable_secure_boot.setter
    def enable_secure_boot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_secure_boot', value)

    @property
    @pulumi.getter(name='enableVtpm')
    def enable_vtpm(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has the vTPM enabled.
        Enabled by default.
        """
        return pulumi.get(self, 'enable_vtpm')

    @enable_vtpm.setter
    def enable_vtpm(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_vtpm', value)

@pulumi.input_type
class InstanceVmImageArgs:

    def __init__(__self__, *, project: pulumi.Input[str], image_family: Optional[pulumi.Input[str]]=None, image_name: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] project: The name of the Google Cloud project that this VM image belongs to.
               Format: projects/{project_id}
        :param pulumi.Input[str] image_family: Use this VM image family to find the image; the newest image in this family will be used.
        :param pulumi.Input[str] image_name: Use VM image name to find the image.
        """
        pulumi.set(__self__, 'project', project)
        if image_family is not None:
            pulumi.set(__self__, 'image_family', image_family)
        if image_name is not None:
            pulumi.set(__self__, 'image_name', image_name)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The name of the Google Cloud project that this VM image belongs to.
        Format: projects/{project_id}
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter(name='imageFamily')
    def image_family(self) -> Optional[pulumi.Input[str]]:
        """
        Use this VM image family to find the image; the newest image in this family will be used.
        """
        return pulumi.get(self, 'image_family')

    @image_family.setter
    def image_family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'image_family', value)

    @property
    @pulumi.getter(name='imageName')
    def image_name(self) -> Optional[pulumi.Input[str]]:
        """
        Use VM image name to find the image.
        """
        return pulumi.get(self, 'image_name')

    @image_name.setter
    def image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'image_name', value)

@pulumi.input_type
class RuntimeAccessConfigArgs:

    def __init__(__self__, *, access_type: Optional[pulumi.Input[str]]=None, proxy_uri: Optional[pulumi.Input[str]]=None, runtime_owner: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] access_type: The type of access mode this instance. For valid values, see
               `https://cloud.google.com/vertex-ai/docs/workbench/reference/
               rest/v1/projects.locations.runtimes#RuntimeAccessType`.
        :param pulumi.Input[str] proxy_uri: -
               The proxy endpoint that is used to access the runtime.
        :param pulumi.Input[str] runtime_owner: The owner of this runtime after creation. Format: `alias@example.com`.
               Currently supports one owner only.
        """
        if access_type is not None:
            pulumi.set(__self__, 'access_type', access_type)
        if proxy_uri is not None:
            pulumi.set(__self__, 'proxy_uri', proxy_uri)
        if runtime_owner is not None:
            pulumi.set(__self__, 'runtime_owner', runtime_owner)

    @property
    @pulumi.getter(name='accessType')
    def access_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of access mode this instance. For valid values, see
        `https://cloud.google.com/vertex-ai/docs/workbench/reference/
        rest/v1/projects.locations.runtimes#RuntimeAccessType`.
        """
        return pulumi.get(self, 'access_type')

    @access_type.setter
    def access_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'access_type', value)

    @property
    @pulumi.getter(name='proxyUri')
    def proxy_uri(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The proxy endpoint that is used to access the runtime.
        """
        return pulumi.get(self, 'proxy_uri')

    @proxy_uri.setter
    def proxy_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'proxy_uri', value)

    @property
    @pulumi.getter(name='runtimeOwner')
    def runtime_owner(self) -> Optional[pulumi.Input[str]]:
        """
        The owner of this runtime after creation. Format: `alias@example.com`.
        Currently supports one owner only.
        """
        return pulumi.get(self, 'runtime_owner')

    @runtime_owner.setter
    def runtime_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'runtime_owner', value)

@pulumi.input_type
class RuntimeIamBindingConditionArgs:

    def __init__(__self__, *, expression: pulumi.Input[str], title: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None):
        pulumi.set(__self__, 'expression', expression)
        pulumi.set(__self__, 'title', title)
        if description is not None:
            pulumi.set(__self__, 'description', description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'expression')

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, 'expression', value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'title')

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, 'title', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

@pulumi.input_type
class RuntimeIamMemberConditionArgs:

    def __init__(__self__, *, expression: pulumi.Input[str], title: pulumi.Input[str], description: Optional[pulumi.Input[str]]=None):
        pulumi.set(__self__, 'expression', expression)
        pulumi.set(__self__, 'title', title)
        if description is not None:
            pulumi.set(__self__, 'description', description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'expression')

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, 'expression', value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'title')

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, 'title', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

@pulumi.input_type
class RuntimeMetricArgs:

    def __init__(__self__, *, system_metrics: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        if system_metrics is not None:
            pulumi.set(__self__, 'system_metrics', system_metrics)

    @property
    @pulumi.getter(name='systemMetrics')
    def system_metrics(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, 'system_metrics')

    @system_metrics.setter
    def system_metrics(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'system_metrics', value)

@pulumi.input_type
class RuntimeSoftwareConfigArgs:

    def __init__(__self__, *, custom_gpu_driver_path: Optional[pulumi.Input[str]]=None, enable_health_monitoring: Optional[pulumi.Input[bool]]=None, idle_shutdown: Optional[pulumi.Input[bool]]=None, idle_shutdown_timeout: Optional[pulumi.Input[int]]=None, install_gpu_driver: Optional[pulumi.Input[bool]]=None, kernels: Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeSoftwareConfigKernelArgs']]]]=None, notebook_upgrade_schedule: Optional[pulumi.Input[str]]=None, post_startup_script: Optional[pulumi.Input[str]]=None, post_startup_script_behavior: Optional[pulumi.Input[str]]=None, upgradeable: Optional[pulumi.Input[bool]]=None):
        """
        :param pulumi.Input[str] custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored.
               If not specified, we'll automatically choose from official GPU drivers.
        :param pulumi.Input[bool] enable_health_monitoring: Verifies core internal services are running. Default: True.
        :param pulumi.Input[bool] idle_shutdown: Runtime will automatically shutdown after idle_shutdown_time.
               Default: True
        :param pulumi.Input[int] idle_shutdown_timeout: Time in minutes to wait before shuting down runtime.
               Default: 180 minutes
        :param pulumi.Input[bool] install_gpu_driver: Install Nvidia Driver automatically.
        :param pulumi.Input[Sequence[pulumi.Input['RuntimeSoftwareConfigKernelArgs']]] kernels: Use a list of container images to use as Kernels in the notebook instance.
               Structure is documented below.
        :param pulumi.Input[str] notebook_upgrade_schedule: Cron expression in UTC timezone for schedule instance auto upgrade.
               Please follow the [cron format](https://en.wikipedia.org/wiki/Cron).
        :param pulumi.Input[str] post_startup_script: Path to a Bash script that automatically runs after a notebook instance
               fully boots up. The path must be a URL or
               Cloud Storage path (gs://path-to-file/file-name).
        :param pulumi.Input[str] post_startup_script_behavior: Behavior for the post startup script.
               Possible values are `POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED`, `RUN_EVERY_START`, and `DOWNLOAD_AND_RUN_EVERY_START`.
        :param pulumi.Input[bool] upgradeable: -
               Bool indicating whether an newer image is available in an image family.
        """
        if custom_gpu_driver_path is not None:
            pulumi.set(__self__, 'custom_gpu_driver_path', custom_gpu_driver_path)
        if enable_health_monitoring is not None:
            pulumi.set(__self__, 'enable_health_monitoring', enable_health_monitoring)
        if idle_shutdown is not None:
            pulumi.set(__self__, 'idle_shutdown', idle_shutdown)
        if idle_shutdown_timeout is not None:
            pulumi.set(__self__, 'idle_shutdown_timeout', idle_shutdown_timeout)
        if install_gpu_driver is not None:
            pulumi.set(__self__, 'install_gpu_driver', install_gpu_driver)
        if kernels is not None:
            pulumi.set(__self__, 'kernels', kernels)
        if notebook_upgrade_schedule is not None:
            pulumi.set(__self__, 'notebook_upgrade_schedule', notebook_upgrade_schedule)
        if post_startup_script is not None:
            pulumi.set(__self__, 'post_startup_script', post_startup_script)
        if post_startup_script_behavior is not None:
            pulumi.set(__self__, 'post_startup_script_behavior', post_startup_script_behavior)
        if upgradeable is not None:
            pulumi.set(__self__, 'upgradeable', upgradeable)

    @property
    @pulumi.getter(name='customGpuDriverPath')
    def custom_gpu_driver_path(self) -> Optional[pulumi.Input[str]]:
        """
        Specify a custom Cloud Storage path where the GPU driver is stored.
        If not specified, we'll automatically choose from official GPU drivers.
        """
        return pulumi.get(self, 'custom_gpu_driver_path')

    @custom_gpu_driver_path.setter
    def custom_gpu_driver_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'custom_gpu_driver_path', value)

    @property
    @pulumi.getter(name='enableHealthMonitoring')
    def enable_health_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Verifies core internal services are running. Default: True.
        """
        return pulumi.get(self, 'enable_health_monitoring')

    @enable_health_monitoring.setter
    def enable_health_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_health_monitoring', value)

    @property
    @pulumi.getter(name='idleShutdown')
    def idle_shutdown(self) -> Optional[pulumi.Input[bool]]:
        """
        Runtime will automatically shutdown after idle_shutdown_time.
        Default: True
        """
        return pulumi.get(self, 'idle_shutdown')

    @idle_shutdown.setter
    def idle_shutdown(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'idle_shutdown', value)

    @property
    @pulumi.getter(name='idleShutdownTimeout')
    def idle_shutdown_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        Time in minutes to wait before shuting down runtime.
        Default: 180 minutes
        """
        return pulumi.get(self, 'idle_shutdown_timeout')

    @idle_shutdown_timeout.setter
    def idle_shutdown_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'idle_shutdown_timeout', value)

    @property
    @pulumi.getter(name='installGpuDriver')
    def install_gpu_driver(self) -> Optional[pulumi.Input[bool]]:
        """
        Install Nvidia Driver automatically.
        """
        return pulumi.get(self, 'install_gpu_driver')

    @install_gpu_driver.setter
    def install_gpu_driver(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'install_gpu_driver', value)

    @property
    @pulumi.getter
    def kernels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeSoftwareConfigKernelArgs']]]]:
        """
        Use a list of container images to use as Kernels in the notebook instance.
        Structure is documented below.
        """
        return pulumi.get(self, 'kernels')

    @kernels.setter
    def kernels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeSoftwareConfigKernelArgs']]]]):
        pulumi.set(self, 'kernels', value)

    @property
    @pulumi.getter(name='notebookUpgradeSchedule')
    def notebook_upgrade_schedule(self) -> Optional[pulumi.Input[str]]:
        """
        Cron expression in UTC timezone for schedule instance auto upgrade.
        Please follow the [cron format](https://en.wikipedia.org/wiki/Cron).
        """
        return pulumi.get(self, 'notebook_upgrade_schedule')

    @notebook_upgrade_schedule.setter
    def notebook_upgrade_schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'notebook_upgrade_schedule', value)

    @property
    @pulumi.getter(name='postStartupScript')
    def post_startup_script(self) -> Optional[pulumi.Input[str]]:
        """
        Path to a Bash script that automatically runs after a notebook instance
        fully boots up. The path must be a URL or
        Cloud Storage path (gs://path-to-file/file-name).
        """
        return pulumi.get(self, 'post_startup_script')

    @post_startup_script.setter
    def post_startup_script(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'post_startup_script', value)

    @property
    @pulumi.getter(name='postStartupScriptBehavior')
    def post_startup_script_behavior(self) -> Optional[pulumi.Input[str]]:
        """
        Behavior for the post startup script.
        Possible values are `POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED`, `RUN_EVERY_START`, and `DOWNLOAD_AND_RUN_EVERY_START`.
        """
        return pulumi.get(self, 'post_startup_script_behavior')

    @post_startup_script_behavior.setter
    def post_startup_script_behavior(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'post_startup_script_behavior', value)

    @property
    @pulumi.getter
    def upgradeable(self) -> Optional[pulumi.Input[bool]]:
        """
        -
        Bool indicating whether an newer image is available in an image family.
        """
        return pulumi.get(self, 'upgradeable')

    @upgradeable.setter
    def upgradeable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'upgradeable', value)

@pulumi.input_type
class RuntimeSoftwareConfigKernelArgs:

    def __init__(__self__, *, repository: pulumi.Input[str], tag: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] repository: The path to the container image repository.
               For example: gcr.io/{project_id}/{imageName}
        :param pulumi.Input[str] tag: The tag of the container image. If not specified, this defaults to the latest tag.
        """
        pulumi.set(__self__, 'repository', repository)
        if tag is not None:
            pulumi.set(__self__, 'tag', tag)

    @property
    @pulumi.getter
    def repository(self) -> pulumi.Input[str]:
        """
        The path to the container image repository.
        For example: gcr.io/{project_id}/{imageName}
        """
        return pulumi.get(self, 'repository')

    @repository.setter
    def repository(self, value: pulumi.Input[str]):
        pulumi.set(self, 'repository', value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        The tag of the container image. If not specified, this defaults to the latest tag.
        """
        return pulumi.get(self, 'tag')

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tag', value)

@pulumi.input_type
class RuntimeVirtualMachineArgs:

    def __init__(__self__, *, instance_id: Optional[pulumi.Input[str]]=None, instance_name: Optional[pulumi.Input[str]]=None, virtual_machine_config: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigArgs']]=None):
        """
        :param pulumi.Input[str] instance_id: -
               The unique identifier of the Managed Compute Engine instance.
        :param pulumi.Input[str] instance_name: -
               The user-friendly name of the Managed Compute Engine instance.
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigArgs'] virtual_machine_config: Virtual Machine configuration settings.
               Structure is documented below.
        """
        if instance_id is not None:
            pulumi.set(__self__, 'instance_id', instance_id)
        if instance_name is not None:
            pulumi.set(__self__, 'instance_name', instance_name)
        if virtual_machine_config is not None:
            pulumi.set(__self__, 'virtual_machine_config', virtual_machine_config)

    @property
    @pulumi.getter(name='instanceId')
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The unique identifier of the Managed Compute Engine instance.
        """
        return pulumi.get(self, 'instance_id')

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'instance_id', value)

    @property
    @pulumi.getter(name='instanceName')
    def instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The user-friendly name of the Managed Compute Engine instance.
        """
        return pulumi.get(self, 'instance_name')

    @instance_name.setter
    def instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'instance_name', value)

    @property
    @pulumi.getter(name='virtualMachineConfig')
    def virtual_machine_config(self) -> Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigArgs']]:
        """
        Virtual Machine configuration settings.
        Structure is documented below.
        """
        return pulumi.get(self, 'virtual_machine_config')

    @virtual_machine_config.setter
    def virtual_machine_config(self, value: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigArgs']]):
        pulumi.set(self, 'virtual_machine_config', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigArgs:

    def __init__(__self__, *, data_disk: pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs'], machine_type: pulumi.Input[str], accelerator_config: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs']]=None, container_images: Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs']]]]=None, encryption_config: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs']]=None, guest_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, internal_ip_only: Optional[pulumi.Input[bool]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, network: Optional[pulumi.Input[str]]=None, nic_type: Optional[pulumi.Input[str]]=None, reserved_ip_range: Optional[pulumi.Input[str]]=None, shielded_instance_config: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs']]=None, subnet: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, zone: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs'] data_disk: Data disk option configuration settings.
               Structure is documented below.
        :param pulumi.Input[str] machine_type: The Compute Engine machine type used for runtimes.
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs'] accelerator_config: The Compute Engine accelerator configuration for this runtime.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs']]] container_images: Use a list of container images to start the notebook instance.
               Structure is documented below.
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs'] encryption_config: Encryption settings for virtual machine data disk.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] guest_attributes: -
               The Compute Engine guest attributes. (see [Project and instance
               guest attributes](https://cloud.google.com/compute/docs/
               storing-retrieving-metadata#guest_attributes)).
        :param pulumi.Input[bool] internal_ip_only: If true, runtime will only have internal IP addresses. By default,
               runtimes are not restricted to internal IP addresses, and will
               have ephemeral external IP addresses assigned to each vm. This
               `internal_ip_only` restriction can only be enabled for subnetwork
               enabled networks, and all dependencies must be configured to be
               accessible without external IP addresses.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels to apply to this disk. These can be later modified
               by the disks.setLabels method. This field is only
               applicable for persistent disks.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: The Compute Engine metadata entries to add to virtual machine.
               (see [Project and instance metadata](https://cloud.google.com
               /compute/docs/storing-retrieving-metadata#project_and_instance
               _metadata)).
        :param pulumi.Input[str] network: The Compute Engine network to be used for machine communications.
               Cannot be specified with subnetwork. If neither `network` nor
               `subnet` is specified, the "default" network of the project is
               used, if it exists. A full URL or partial URI. Examples:
               * `https://www.googleapis.com/compute/v1/projects/[project_id]/
               regions/global/default`
               * `projects/[project_id]/regions/global/default`
               Runtimes are managed resources inside Google Infrastructure.
               Runtimes support the following network configurations:
               * Google Managed Network (Network & subnet are empty)
               * Consumer Project VPC (network & subnet are required). Requires
               configuring Private Service Access.
               * Shared VPC (network & subnet are required). Requires
               configuring Private Service Access.
        :param pulumi.Input[str] nic_type: The type of vNIC to be used on this interface. This may be gVNIC
               or VirtioNet.
               Possible values are `UNSPECIFIED_NIC_TYPE`, `VIRTIO_NET`, and `GVNIC`.
        :param pulumi.Input[str] reserved_ip_range: Reserved IP Range name is used for VPC Peering. The
               subnetwork allocation will use the range *name* if it's assigned.
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs'] shielded_instance_config: Shielded VM Instance configuration settings.
               Structure is documented below.
        :param pulumi.Input[str] subnet: The Compute Engine subnetwork to be used for machine
               communications. Cannot be specified with network. A full URL or
               partial URI are valid. Examples:
               * `https://www.googleapis.com/compute/v1/projects/[project_id]/
               regions/us-east1/subnetworks/sub0`
               * `projects/[project_id]/regions/us-east1/subnetworks/sub0`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The Compute Engine tags to add to runtime (see [Tagging instances]
               (https://cloud.google.com/compute/docs/
               label-or-tag-resources#tags)).
        :param pulumi.Input[str] zone: -
               The zone where the virtual machine is located.
        """
        pulumi.set(__self__, 'data_disk', data_disk)
        pulumi.set(__self__, 'machine_type', machine_type)
        if accelerator_config is not None:
            pulumi.set(__self__, 'accelerator_config', accelerator_config)
        if container_images is not None:
            pulumi.set(__self__, 'container_images', container_images)
        if encryption_config is not None:
            pulumi.set(__self__, 'encryption_config', encryption_config)
        if guest_attributes is not None:
            pulumi.set(__self__, 'guest_attributes', guest_attributes)
        if internal_ip_only is not None:
            pulumi.set(__self__, 'internal_ip_only', internal_ip_only)
        if labels is not None:
            pulumi.set(__self__, 'labels', labels)
        if metadata is not None:
            pulumi.set(__self__, 'metadata', metadata)
        if network is not None:
            pulumi.set(__self__, 'network', network)
        if nic_type is not None:
            pulumi.set(__self__, 'nic_type', nic_type)
        if reserved_ip_range is not None:
            pulumi.set(__self__, 'reserved_ip_range', reserved_ip_range)
        if shielded_instance_config is not None:
            pulumi.set(__self__, 'shielded_instance_config', shielded_instance_config)
        if subnet is not None:
            pulumi.set(__self__, 'subnet', subnet)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zone is not None:
            pulumi.set(__self__, 'zone', zone)

    @property
    @pulumi.getter(name='dataDisk')
    def data_disk(self) -> pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs']:
        """
        Data disk option configuration settings.
        Structure is documented below.
        """
        return pulumi.get(self, 'data_disk')

    @data_disk.setter
    def data_disk(self, value: pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs']):
        pulumi.set(self, 'data_disk', value)

    @property
    @pulumi.getter(name='machineType')
    def machine_type(self) -> pulumi.Input[str]:
        """
        The Compute Engine machine type used for runtimes.
        """
        return pulumi.get(self, 'machine_type')

    @machine_type.setter
    def machine_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'machine_type', value)

    @property
    @pulumi.getter(name='acceleratorConfig')
    def accelerator_config(self) -> Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs']]:
        """
        The Compute Engine accelerator configuration for this runtime.
        Structure is documented below.
        """
        return pulumi.get(self, 'accelerator_config')

    @accelerator_config.setter
    def accelerator_config(self, value: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs']]):
        pulumi.set(self, 'accelerator_config', value)

    @property
    @pulumi.getter(name='containerImages')
    def container_images(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs']]]]:
        """
        Use a list of container images to start the notebook instance.
        Structure is documented below.
        """
        return pulumi.get(self, 'container_images')

    @container_images.setter
    def container_images(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs']]]]):
        pulumi.set(self, 'container_images', value)

    @property
    @pulumi.getter(name='encryptionConfig')
    def encryption_config(self) -> Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs']]:
        """
        Encryption settings for virtual machine data disk.
        Structure is documented below.
        """
        return pulumi.get(self, 'encryption_config')

    @encryption_config.setter
    def encryption_config(self, value: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs']]):
        pulumi.set(self, 'encryption_config', value)

    @property
    @pulumi.getter(name='guestAttributes')
    def guest_attributes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        -
        The Compute Engine guest attributes. (see [Project and instance
        guest attributes](https://cloud.google.com/compute/docs/
        storing-retrieving-metadata#guest_attributes)).
        """
        return pulumi.get(self, 'guest_attributes')

    @guest_attributes.setter
    def guest_attributes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'guest_attributes', value)

    @property
    @pulumi.getter(name='internalIpOnly')
    def internal_ip_only(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, runtime will only have internal IP addresses. By default,
        runtimes are not restricted to internal IP addresses, and will
        have ephemeral external IP addresses assigned to each vm. This
        `internal_ip_only` restriction can only be enabled for subnetwork
        enabled networks, and all dependencies must be configured to be
        accessible without external IP addresses.
        """
        return pulumi.get(self, 'internal_ip_only')

    @internal_ip_only.setter
    def internal_ip_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'internal_ip_only', value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels to apply to this disk. These can be later modified
        by the disks.setLabels method. This field is only
        applicable for persistent disks.
        """
        return pulumi.get(self, 'labels')

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'labels', value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The Compute Engine metadata entries to add to virtual machine.
        (see [Project and instance metadata](https://cloud.google.com
        /compute/docs/storing-retrieving-metadata#project_and_instance
        _metadata)).
        """
        return pulumi.get(self, 'metadata')

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'metadata', value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The Compute Engine network to be used for machine communications.
        Cannot be specified with subnetwork. If neither `network` nor
        `subnet` is specified, the "default" network of the project is
        used, if it exists. A full URL or partial URI. Examples:
        * `https://www.googleapis.com/compute/v1/projects/[project_id]/
        regions/global/default`
        * `projects/[project_id]/regions/global/default`
        Runtimes are managed resources inside Google Infrastructure.
        Runtimes support the following network configurations:
        * Google Managed Network (Network & subnet are empty)
        * Consumer Project VPC (network & subnet are required). Requires
        configuring Private Service Access.
        * Shared VPC (network & subnet are required). Requires
        configuring Private Service Access.
        """
        return pulumi.get(self, 'network')

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'network', value)

    @property
    @pulumi.getter(name='nicType')
    def nic_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of vNIC to be used on this interface. This may be gVNIC
        or VirtioNet.
        Possible values are `UNSPECIFIED_NIC_TYPE`, `VIRTIO_NET`, and `GVNIC`.
        """
        return pulumi.get(self, 'nic_type')

    @nic_type.setter
    def nic_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'nic_type', value)

    @property
    @pulumi.getter(name='reservedIpRange')
    def reserved_ip_range(self) -> Optional[pulumi.Input[str]]:
        """
        Reserved IP Range name is used for VPC Peering. The
        subnetwork allocation will use the range *name* if it's assigned.
        """
        return pulumi.get(self, 'reserved_ip_range')

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'reserved_ip_range', value)

    @property
    @pulumi.getter(name='shieldedInstanceConfig')
    def shielded_instance_config(self) -> Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs']]:
        """
        Shielded VM Instance configuration settings.
        Structure is documented below.
        """
        return pulumi.get(self, 'shielded_instance_config')

    @shielded_instance_config.setter
    def shielded_instance_config(self, value: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs']]):
        pulumi.set(self, 'shielded_instance_config', value)

    @property
    @pulumi.getter
    def subnet(self) -> Optional[pulumi.Input[str]]:
        """
        The Compute Engine subnetwork to be used for machine
        communications. Cannot be specified with network. A full URL or
        partial URI are valid. Examples:
        * `https://www.googleapis.com/compute/v1/projects/[project_id]/
        regions/us-east1/subnetworks/sub0`
        * `projects/[project_id]/regions/us-east1/subnetworks/sub0`
        """
        return pulumi.get(self, 'subnet')

    @subnet.setter
    def subnet(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnet', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Compute Engine tags to add to runtime (see [Tagging instances]
        (https://cloud.google.com/compute/docs/
        label-or-tag-resources#tags)).
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The zone where the virtual machine is located.
        """
        return pulumi.get(self, 'zone')

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zone', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigAcceleratorConfigArgs:

    def __init__(__self__, *, core_count: Optional[pulumi.Input[int]]=None, type: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[int] core_count: Count of cores of this accelerator.
        :param pulumi.Input[str] type: Accelerator model. For valid values, see
               `https://cloud.google.com/vertex-ai/docs/workbench/reference/
               rest/v1/projects.locations.runtimes#AcceleratorType`
        """
        if core_count is not None:
            pulumi.set(__self__, 'core_count', core_count)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='coreCount')
    def core_count(self) -> Optional[pulumi.Input[int]]:
        """
        Count of cores of this accelerator.
        """
        return pulumi.get(self, 'core_count')

    @core_count.setter
    def core_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'core_count', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Accelerator model. For valid values, see
        `https://cloud.google.com/vertex-ai/docs/workbench/reference/
        rest/v1/projects.locations.runtimes#AcceleratorType`
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigContainerImageArgs:

    def __init__(__self__, *, repository: pulumi.Input[str], tag: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] repository: The path to the container image repository.
               For example: gcr.io/{project_id}/{imageName}
        :param pulumi.Input[str] tag: The tag of the container image. If not specified, this defaults to the latest tag.
        """
        pulumi.set(__self__, 'repository', repository)
        if tag is not None:
            pulumi.set(__self__, 'tag', tag)

    @property
    @pulumi.getter
    def repository(self) -> pulumi.Input[str]:
        """
        The path to the container image repository.
        For example: gcr.io/{project_id}/{imageName}
        """
        return pulumi.get(self, 'repository')

    @repository.setter
    def repository(self, value: pulumi.Input[str]):
        pulumi.set(self, 'repository', value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        The tag of the container image. If not specified, this defaults to the latest tag.
        """
        return pulumi.get(self, 'tag')

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tag', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigDataDiskArgs:

    def __init__(__self__, *, auto_delete: Optional[pulumi.Input[bool]]=None, boot: Optional[pulumi.Input[bool]]=None, device_name: Optional[pulumi.Input[str]]=None, guest_os_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, index: Optional[pulumi.Input[int]]=None, initialize_params: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs']]=None, interface: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, licenses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, mode: Optional[pulumi.Input[str]]=None, source: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[bool] auto_delete: -
               Optional. Specifies whether the disk will be auto-deleted
               when the instance is deleted (but not when the disk is
               detached from the instance).
        :param pulumi.Input[bool] boot: -
               Optional. Indicates that this is a boot disk. The virtual
               machine will use the first partition of the disk for its
               root filesystem.
        :param pulumi.Input[str] device_name: -
               Optional. Specifies a unique device name of your choice
               that is reflected into the /dev/disk/by-id/google-* tree
               of a Linux operating system running within the instance.
               This name can be used to reference the device for mounting,
               resizing, and so on, from within the instance.
               If not specified, the server chooses a default device name
               to apply to this disk, in the form persistent-disk-x, where
               x is a number assigned by Google Compute Engine. This field
               is only applicable for persistent disks.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] guest_os_features: -
               Indicates a list of features to enable on the guest operating
               system. Applicable only for bootable images. To see a list of
               available features, read `https://cloud.google.com/compute/docs/
               images/create-delete-deprecate-private-images#guest-os-features`
               options. ``
        :param pulumi.Input[int] index: -
               Output only. A zero-based index to this disk, where 0 is
               reserved for the boot disk. If you have many disks attached
               to an instance, each disk would have a unique index number.
        :param pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs'] initialize_params: Input only. Specifies the parameters for a new disk that will
               be created alongside the new instance. Use initialization
               parameters to create boot disks or local SSDs attached to the
               new instance. This property is mutually exclusive with the
               source property; you can only define one or the other, but not
               both.
               Structure is documented below.
        :param pulumi.Input[str] interface: "Specifies the disk interface to use for attaching this disk,
               which is either SCSI or NVME. The default is SCSI. Persistent
               disks must always use SCSI and the request will fail if you attempt
               to attach a persistent disk in any other format than SCSI. Local SSDs
               can use either NVME or SCSI. For performance characteristics of SCSI
               over NVMe, see Local SSD performance. Valid values: * NVME * SCSI".
        :param pulumi.Input[str] kind: -
               Type of the resource. Always compute#attachedDisk for attached
               disks.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] licenses: -
               Output only. Any valid publicly visible licenses.
        :param pulumi.Input[str] mode: The mode in which to attach this disk, either READ_WRITE
               or READ_ONLY. If not specified, the default is to attach
               the disk in READ_WRITE mode.
        :param pulumi.Input[str] source: Specifies a valid partial or full URL to an existing
               Persistent Disk resource.
        :param pulumi.Input[str] type: Accelerator model. For valid values, see
               `https://cloud.google.com/vertex-ai/docs/workbench/reference/
               rest/v1/projects.locations.runtimes#AcceleratorType`
        """
        if auto_delete is not None:
            pulumi.set(__self__, 'auto_delete', auto_delete)
        if boot is not None:
            pulumi.set(__self__, 'boot', boot)
        if device_name is not None:
            pulumi.set(__self__, 'device_name', device_name)
        if guest_os_features is not None:
            pulumi.set(__self__, 'guest_os_features', guest_os_features)
        if index is not None:
            pulumi.set(__self__, 'index', index)
        if initialize_params is not None:
            pulumi.set(__self__, 'initialize_params', initialize_params)
        if interface is not None:
            pulumi.set(__self__, 'interface', interface)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if licenses is not None:
            pulumi.set(__self__, 'licenses', licenses)
        if mode is not None:
            pulumi.set(__self__, 'mode', mode)
        if source is not None:
            pulumi.set(__self__, 'source', source)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='autoDelete')
    def auto_delete(self) -> Optional[pulumi.Input[bool]]:
        """
        -
        Optional. Specifies whether the disk will be auto-deleted
        when the instance is deleted (but not when the disk is
        detached from the instance).
        """
        return pulumi.get(self, 'auto_delete')

    @auto_delete.setter
    def auto_delete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_delete', value)

    @property
    @pulumi.getter
    def boot(self) -> Optional[pulumi.Input[bool]]:
        """
        -
        Optional. Indicates that this is a boot disk. The virtual
        machine will use the first partition of the disk for its
        root filesystem.
        """
        return pulumi.get(self, 'boot')

    @boot.setter
    def boot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'boot', value)

    @property
    @pulumi.getter(name='deviceName')
    def device_name(self) -> Optional[pulumi.Input[str]]:
        """
        -
        Optional. Specifies a unique device name of your choice
        that is reflected into the /dev/disk/by-id/google-* tree
        of a Linux operating system running within the instance.
        This name can be used to reference the device for mounting,
        resizing, and so on, from within the instance.
        If not specified, the server chooses a default device name
        to apply to this disk, in the form persistent-disk-x, where
        x is a number assigned by Google Compute Engine. This field
        is only applicable for persistent disks.
        """
        return pulumi.get(self, 'device_name')

    @device_name.setter
    def device_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'device_name', value)

    @property
    @pulumi.getter(name='guestOsFeatures')
    def guest_os_features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        -
        Indicates a list of features to enable on the guest operating
        system. Applicable only for bootable images. To see a list of
        available features, read `https://cloud.google.com/compute/docs/
        images/create-delete-deprecate-private-images#guest-os-features`
        options. ``
        """
        return pulumi.get(self, 'guest_os_features')

    @guest_os_features.setter
    def guest_os_features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'guest_os_features', value)

    @property
    @pulumi.getter
    def index(self) -> Optional[pulumi.Input[int]]:
        """
        -
        Output only. A zero-based index to this disk, where 0 is
        reserved for the boot disk. If you have many disks attached
        to an instance, each disk would have a unique index number.
        """
        return pulumi.get(self, 'index')

    @index.setter
    def index(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'index', value)

    @property
    @pulumi.getter(name='initializeParams')
    def initialize_params(self) -> Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs']]:
        """
        Input only. Specifies the parameters for a new disk that will
        be created alongside the new instance. Use initialization
        parameters to create boot disks or local SSDs attached to the
        new instance. This property is mutually exclusive with the
        source property; you can only define one or the other, but not
        both.
        Structure is documented below.
        """
        return pulumi.get(self, 'initialize_params')

    @initialize_params.setter
    def initialize_params(self, value: Optional[pulumi.Input['RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs']]):
        pulumi.set(self, 'initialize_params', value)

    @property
    @pulumi.getter
    def interface(self) -> Optional[pulumi.Input[str]]:
        """
        "Specifies the disk interface to use for attaching this disk,
        which is either SCSI or NVME. The default is SCSI. Persistent
        disks must always use SCSI and the request will fail if you attempt
        to attach a persistent disk in any other format than SCSI. Local SSDs
        can use either NVME or SCSI. For performance characteristics of SCSI
        over NVMe, see Local SSD performance. Valid values: * NVME * SCSI".
        """
        return pulumi.get(self, 'interface')

    @interface.setter
    def interface(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'interface', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        -
        Type of the resource. Always compute#attachedDisk for attached
        disks.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def licenses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        -
        Output only. Any valid publicly visible licenses.
        """
        return pulumi.get(self, 'licenses')

    @licenses.setter
    def licenses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'licenses', value)

    @property
    @pulumi.getter
    def mode(self) -> Optional[pulumi.Input[str]]:
        """
        The mode in which to attach this disk, either READ_WRITE
        or READ_ONLY. If not specified, the default is to attach
        the disk in READ_WRITE mode.
        """
        return pulumi.get(self, 'mode')

    @mode.setter
    def mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'mode', value)

    @property
    @pulumi.getter
    def source(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a valid partial or full URL to an existing
        Persistent Disk resource.
        """
        return pulumi.get(self, 'source')

    @source.setter
    def source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'source', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Accelerator model. For valid values, see
        `https://cloud.google.com/vertex-ai/docs/workbench/reference/
        rest/v1/projects.locations.runtimes#AcceleratorType`
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigDataDiskInitializeParamsArgs:

    def __init__(__self__, *, description: Optional[pulumi.Input[str]]=None, disk_name: Optional[pulumi.Input[str]]=None, disk_size_gb: Optional[pulumi.Input[int]]=None, disk_type: Optional[pulumi.Input[str]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        :param pulumi.Input[str] description: Provide this property when creating the disk.
        :param pulumi.Input[str] disk_name: Specifies the disk name. If not specified, the default is
               to use the name of the instance. If the disk with the
               instance name exists already in the given zone/region, a
               new name will be automatically generated.
        :param pulumi.Input[int] disk_size_gb: Specifies the size of the disk in base-2 GB. If not
               specified, the disk will be the same size as the image
               (usually 10GB). If specified, the size must be equal to
               or larger than 10GB. Default 100 GB.
        :param pulumi.Input[str] disk_type: The type of the boot disk attached to this runtime,
               defaults to standard persistent disk. For valid values,
               see `https://cloud.google.com/vertex-ai/docs/workbench/
               reference/rest/v1/projects.locations.runtimes#disktype`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels to apply to this disk. These can be later modified
               by the disks.setLabels method. This field is only
               applicable for persistent disks.
        """
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if disk_name is not None:
            pulumi.set(__self__, 'disk_name', disk_name)
        if disk_size_gb is not None:
            pulumi.set(__self__, 'disk_size_gb', disk_size_gb)
        if disk_type is not None:
            pulumi.set(__self__, 'disk_type', disk_type)
        if labels is not None:
            pulumi.set(__self__, 'labels', labels)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Provide this property when creating the disk.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='diskName')
    def disk_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the disk name. If not specified, the default is
        to use the name of the instance. If the disk with the
        instance name exists already in the given zone/region, a
        new name will be automatically generated.
        """
        return pulumi.get(self, 'disk_name')

    @disk_name.setter
    def disk_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'disk_name', value)

    @property
    @pulumi.getter(name='diskSizeGb')
    def disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the size of the disk in base-2 GB. If not
        specified, the disk will be the same size as the image
        (usually 10GB). If specified, the size must be equal to
        or larger than 10GB. Default 100 GB.
        """
        return pulumi.get(self, 'disk_size_gb')

    @disk_size_gb.setter
    def disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'disk_size_gb', value)

    @property
    @pulumi.getter(name='diskType')
    def disk_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the boot disk attached to this runtime,
        defaults to standard persistent disk. For valid values,
        see `https://cloud.google.com/vertex-ai/docs/workbench/
        reference/rest/v1/projects.locations.runtimes#disktype`
        """
        return pulumi.get(self, 'disk_type')

    @disk_type.setter
    def disk_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'disk_type', value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels to apply to this disk. These can be later modified
        by the disks.setLabels method. This field is only
        applicable for persistent disks.
        """
        return pulumi.get(self, 'labels')

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'labels', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigEncryptionConfigArgs:

    def __init__(__self__, *, kms_key: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] kms_key: The Cloud KMS resource identifier of the customer-managed
               encryption key used to protect a resource, such as a disks.
               It has the following format:
               `projects/{PROJECT_ID}/locations/{REGION}/keyRings/
               {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}`
        """
        if kms_key is not None:
            pulumi.set(__self__, 'kms_key', kms_key)

    @property
    @pulumi.getter(name='kmsKey')
    def kms_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Cloud KMS resource identifier of the customer-managed
        encryption key used to protect a resource, such as a disks.
        It has the following format:
        `projects/{PROJECT_ID}/locations/{REGION}/keyRings/
        {KEY_RING_NAME}/cryptoKeys/{KEY_NAME}`
        """
        return pulumi.get(self, 'kms_key')

    @kms_key.setter
    def kms_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kms_key', value)

@pulumi.input_type
class RuntimeVirtualMachineVirtualMachineConfigShieldedInstanceConfigArgs:

    def __init__(__self__, *, enable_integrity_monitoring: Optional[pulumi.Input[bool]]=None, enable_secure_boot: Optional[pulumi.Input[bool]]=None, enable_vtpm: Optional[pulumi.Input[bool]]=None):
        """
        :param pulumi.Input[bool] enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled.
               Enables monitoring and attestation of the boot integrity of
               the instance. The attestation is performed against the
               integrity policy baseline. This baseline is initially derived
               from the implicitly trusted boot image when the instance is
               created. Enabled by default.
        :param pulumi.Input[bool] enable_secure_boot: Defines whether the instance has Secure Boot enabled.Secure
               Boot helps ensure that the system only runs authentic software
               by verifying the digital signature of all boot components, and
               halting the boot process if signature verification fails.
               Disabled by default.
        :param pulumi.Input[bool] enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by
               default.
        """
        if enable_integrity_monitoring is not None:
            pulumi.set(__self__, 'enable_integrity_monitoring', enable_integrity_monitoring)
        if enable_secure_boot is not None:
            pulumi.set(__self__, 'enable_secure_boot', enable_secure_boot)
        if enable_vtpm is not None:
            pulumi.set(__self__, 'enable_vtpm', enable_vtpm)

    @property
    @pulumi.getter(name='enableIntegrityMonitoring')
    def enable_integrity_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has integrity monitoring enabled.
        Enables monitoring and attestation of the boot integrity of
        the instance. The attestation is performed against the
        integrity policy baseline. This baseline is initially derived
        from the implicitly trusted boot image when the instance is
        created. Enabled by default.
        """
        return pulumi.get(self, 'enable_integrity_monitoring')

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_integrity_monitoring', value)

    @property
    @pulumi.getter(name='enableSecureBoot')
    def enable_secure_boot(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has Secure Boot enabled.Secure
        Boot helps ensure that the system only runs authentic software
        by verifying the digital signature of all boot components, and
        halting the boot process if signature verification fails.
        Disabled by default.
        """
        return pulumi.get(self, 'enable_secure_boot')

    @enable_secure_boot.setter
    def enable_secure_boot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_secure_boot', value)

    @property
    @pulumi.getter(name='enableVtpm')
    def enable_vtpm(self) -> Optional[pulumi.Input[bool]]:
        """
        Defines whether the instance has the vTPM enabled. Enabled by
        default.
        """
        return pulumi.get(self, 'enable_vtpm')

    @enable_vtpm.setter
    def enable_vtpm(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_vtpm', value)