import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['PacketCaptureArgs', 'PacketCapture']

@pulumi.input_type
class PacketCaptureArgs:

    def __init__(__self__, *, network_watcher_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], storage_location: pulumi.Input['PacketCaptureStorageLocationArgs'], target: pulumi.Input[str], bytes_to_capture_per_packet: Optional[pulumi.Input[int]]=None, filters: Optional[pulumi.Input[Sequence[pulumi.Input['PacketCaptureFilterArgs']]]]=None, packet_capture_name: Optional[pulumi.Input[str]]=None, time_limit_in_seconds: Optional[pulumi.Input[int]]=None, total_bytes_per_session: Optional[pulumi.Input[int]]=None):
        """
        The set of arguments for constructing a PacketCapture resource.
        :param pulumi.Input[str] network_watcher_name: The name of the network watcher.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['PacketCaptureStorageLocationArgs'] storage_location: Describes the storage location for a packet capture session.
        :param pulumi.Input[str] target: The ID of the targeted resource, only VM is currently supported.
        :param pulumi.Input[int] bytes_to_capture_per_packet: Number of bytes captured per packet, the remaining bytes are truncated.
        :param pulumi.Input[str] packet_capture_name: The name of the packet capture session.
        :param pulumi.Input[int] time_limit_in_seconds: Maximum duration of the capture session in seconds.
        :param pulumi.Input[int] total_bytes_per_session: Maximum size of the capture output.
        """
        pulumi.set(__self__, 'network_watcher_name', network_watcher_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'storage_location', storage_location)
        pulumi.set(__self__, 'target', target)
        if bytes_to_capture_per_packet is None:
            bytes_to_capture_per_packet = 0
        if bytes_to_capture_per_packet is not None:
            pulumi.set(__self__, 'bytes_to_capture_per_packet', bytes_to_capture_per_packet)
        if filters is not None:
            pulumi.set(__self__, 'filters', filters)
        if packet_capture_name is not None:
            pulumi.set(__self__, 'packet_capture_name', packet_capture_name)
        if time_limit_in_seconds is None:
            time_limit_in_seconds = 18000
        if time_limit_in_seconds is not None:
            pulumi.set(__self__, 'time_limit_in_seconds', time_limit_in_seconds)
        if total_bytes_per_session is None:
            total_bytes_per_session = 1073741824
        if total_bytes_per_session is not None:
            pulumi.set(__self__, 'total_bytes_per_session', total_bytes_per_session)

    @property
    @pulumi.getter(name='networkWatcherName')
    def network_watcher_name(self) -> pulumi.Input[str]:
        """
        The name of the network watcher.
        """
        return pulumi.get(self, 'network_watcher_name')

    @network_watcher_name.setter
    def network_watcher_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'network_watcher_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='storageLocation')
    def storage_location(self) -> pulumi.Input['PacketCaptureStorageLocationArgs']:
        """
        Describes the storage location for a packet capture session.
        """
        return pulumi.get(self, 'storage_location')

    @storage_location.setter
    def storage_location(self, value: pulumi.Input['PacketCaptureStorageLocationArgs']):
        pulumi.set(self, 'storage_location', value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        The ID of the targeted resource, only VM is currently supported.
        """
        return pulumi.get(self, 'target')

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, 'target', value)

    @property
    @pulumi.getter(name='bytesToCapturePerPacket')
    def bytes_to_capture_per_packet(self) -> Optional[pulumi.Input[int]]:
        """
        Number of bytes captured per packet, the remaining bytes are truncated.
        """
        return pulumi.get(self, 'bytes_to_capture_per_packet')

    @bytes_to_capture_per_packet.setter
    def bytes_to_capture_per_packet(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'bytes_to_capture_per_packet', value)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PacketCaptureFilterArgs']]]]:
        return pulumi.get(self, 'filters')

    @filters.setter
    def filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PacketCaptureFilterArgs']]]]):
        pulumi.set(self, 'filters', value)

    @property
    @pulumi.getter(name='packetCaptureName')
    def packet_capture_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the packet capture session.
        """
        return pulumi.get(self, 'packet_capture_name')

    @packet_capture_name.setter
    def packet_capture_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'packet_capture_name', value)

    @property
    @pulumi.getter(name='timeLimitInSeconds')
    def time_limit_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum duration of the capture session in seconds.
        """
        return pulumi.get(self, 'time_limit_in_seconds')

    @time_limit_in_seconds.setter
    def time_limit_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'time_limit_in_seconds', value)

    @property
    @pulumi.getter(name='totalBytesPerSession')
    def total_bytes_per_session(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum size of the capture output.
        """
        return pulumi.get(self, 'total_bytes_per_session')

    @total_bytes_per_session.setter
    def total_bytes_per_session(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'total_bytes_per_session', value)
warnings.warn('Version 2018-04-01 will be removed in v2 of the provider.', DeprecationWarning)

class PacketCapture(pulumi.CustomResource):
    warnings.warn('Version 2018-04-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, bytes_to_capture_per_packet: Optional[pulumi.Input[int]]=None, filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PacketCaptureFilterArgs']]]]]=None, network_watcher_name: Optional[pulumi.Input[str]]=None, packet_capture_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_location: Optional[pulumi.Input[pulumi.InputType['PacketCaptureStorageLocationArgs']]]=None, target: Optional[pulumi.Input[str]]=None, time_limit_in_seconds: Optional[pulumi.Input[int]]=None, total_bytes_per_session: Optional[pulumi.Input[int]]=None, __props__=None):
        """
        Information about packet capture session.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] bytes_to_capture_per_packet: Number of bytes captured per packet, the remaining bytes are truncated.
        :param pulumi.Input[str] network_watcher_name: The name of the network watcher.
        :param pulumi.Input[str] packet_capture_name: The name of the packet capture session.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['PacketCaptureStorageLocationArgs']] storage_location: Describes the storage location for a packet capture session.
        :param pulumi.Input[str] target: The ID of the targeted resource, only VM is currently supported.
        :param pulumi.Input[int] time_limit_in_seconds: Maximum duration of the capture session in seconds.
        :param pulumi.Input[int] total_bytes_per_session: Maximum size of the capture output.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PacketCaptureArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Information about packet capture session.

        :param str resource_name: The name of the resource.
        :param PacketCaptureArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PacketCaptureArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, bytes_to_capture_per_packet: Optional[pulumi.Input[int]]=None, filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PacketCaptureFilterArgs']]]]]=None, network_watcher_name: Optional[pulumi.Input[str]]=None, packet_capture_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_location: Optional[pulumi.Input[pulumi.InputType['PacketCaptureStorageLocationArgs']]]=None, target: Optional[pulumi.Input[str]]=None, time_limit_in_seconds: Optional[pulumi.Input[int]]=None, total_bytes_per_session: Optional[pulumi.Input[int]]=None, __props__=None):
        pulumi.log.warn('PacketCapture is deprecated: Version 2018-04-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PacketCaptureArgs.__new__(PacketCaptureArgs)
            if bytes_to_capture_per_packet is None:
                bytes_to_capture_per_packet = 0
            __props__.__dict__['bytes_to_capture_per_packet'] = bytes_to_capture_per_packet
            __props__.__dict__['filters'] = filters
            if network_watcher_name is None and (not opts.urn):
                raise TypeError("Missing required property 'network_watcher_name'")
            __props__.__dict__['network_watcher_name'] = network_watcher_name
            __props__.__dict__['packet_capture_name'] = packet_capture_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if storage_location is None and (not opts.urn):
                raise TypeError("Missing required property 'storage_location'")
            __props__.__dict__['storage_location'] = storage_location
            if target is None and (not opts.urn):
                raise TypeError("Missing required property 'target'")
            __props__.__dict__['target'] = target
            if time_limit_in_seconds is None:
                time_limit_in_seconds = 18000
            __props__.__dict__['time_limit_in_seconds'] = time_limit_in_seconds
            if total_bytes_per_session is None:
                total_bytes_per_session = 1073741824
            __props__.__dict__['total_bytes_per_session'] = total_bytes_per_session
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20160901:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20161201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20170301:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20170601:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20170801:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20170901:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20171001:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20171101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20180101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20180201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20180601:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20180701:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20180801:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20181001:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20181101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20181201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190401:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190601:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190701:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190801:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20190901:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20191101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20191201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200301:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200401:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200501:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200601:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200701:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20200801:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20201101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20210201:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20210301:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20210501:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20210801:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20220101:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20220501:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20220701:PacketCapture'), pulumi.Alias(type_='azure-native:network/v20220901:PacketCapture')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PacketCapture, __self__).__init__('azure-native:network/v20180401:PacketCapture', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'PacketCapture':
        """
        Get an existing PacketCapture resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = PacketCaptureArgs.__new__(PacketCaptureArgs)
        __props__.__dict__['bytes_to_capture_per_packet'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['filters'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['storage_location'] = None
        __props__.__dict__['target'] = None
        __props__.__dict__['time_limit_in_seconds'] = None
        __props__.__dict__['total_bytes_per_session'] = None
        return PacketCapture(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='bytesToCapturePerPacket')
    def bytes_to_capture_per_packet(self) -> pulumi.Output[Optional[int]]:
        """
        Number of bytes captured per packet, the remaining bytes are truncated.
        """
        return pulumi.get(self, 'bytes_to_capture_per_packet')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Output[Optional[Sequence['outputs.PacketCaptureFilterResponse']]]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the packet capture session.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioning state of the packet capture session.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='storageLocation')
    def storage_location(self) -> pulumi.Output['outputs.PacketCaptureStorageLocationResponse']:
        """
        Describes the storage location for a packet capture session.
        """
        return pulumi.get(self, 'storage_location')

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        The ID of the targeted resource, only VM is currently supported.
        """
        return pulumi.get(self, 'target')

    @property
    @pulumi.getter(name='timeLimitInSeconds')
    def time_limit_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum duration of the capture session in seconds.
        """
        return pulumi.get(self, 'time_limit_in_seconds')

    @property
    @pulumi.getter(name='totalBytesPerSession')
    def total_bytes_per_session(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum size of the capture output.
        """
        return pulumi.get(self, 'total_bytes_per_session')