import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GatewaySlbListArgs']

@pulumi.input_type
class GatewaySlbListArgs:

    def __init__(__self__, *, associate_id: Optional[pulumi.Input[str]]=None, gateway_slb_mode: Optional[pulumi.Input[str]]=None, gateway_slb_status: Optional[pulumi.Input[str]]=None, gmt_create: Optional[pulumi.Input[str]]=None, slb_id: Optional[pulumi.Input[str]]=None, slb_ip: Optional[pulumi.Input[str]]=None, slb_port: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] associate_id: The associate id.
        :param pulumi.Input[str] gateway_slb_mode: The Mode of the gateway slb.
        :param pulumi.Input[str] gateway_slb_status: The Status of the gateway slb.
        :param pulumi.Input[str] gmt_create: The creation time of the gateway slb.
        :param pulumi.Input[str] slb_id: The ID of the gateway slb.
        :param pulumi.Input[str] slb_ip: The ip of the gateway slb.
        :param pulumi.Input[str] slb_port: The port of the gateway slb.
        :param pulumi.Input[str] type: The type of the gateway slb.
        """
        if associate_id is not None:
            pulumi.set(__self__, 'associate_id', associate_id)
        if gateway_slb_mode is not None:
            pulumi.set(__self__, 'gateway_slb_mode', gateway_slb_mode)
        if gateway_slb_status is not None:
            pulumi.set(__self__, 'gateway_slb_status', gateway_slb_status)
        if gmt_create is not None:
            pulumi.set(__self__, 'gmt_create', gmt_create)
        if slb_id is not None:
            pulumi.set(__self__, 'slb_id', slb_id)
        if slb_ip is not None:
            pulumi.set(__self__, 'slb_ip', slb_ip)
        if slb_port is not None:
            pulumi.set(__self__, 'slb_port', slb_port)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='associateId')
    def associate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The associate id.
        """
        return pulumi.get(self, 'associate_id')

    @associate_id.setter
    def associate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'associate_id', value)

    @property
    @pulumi.getter(name='gatewaySlbMode')
    def gateway_slb_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Mode of the gateway slb.
        """
        return pulumi.get(self, 'gateway_slb_mode')

    @gateway_slb_mode.setter
    def gateway_slb_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'gateway_slb_mode', value)

    @property
    @pulumi.getter(name='gatewaySlbStatus')
    def gateway_slb_status(self) -> Optional[pulumi.Input[str]]:
        """
        The Status of the gateway slb.
        """
        return pulumi.get(self, 'gateway_slb_status')

    @gateway_slb_status.setter
    def gateway_slb_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'gateway_slb_status', value)

    @property
    @pulumi.getter(name='gmtCreate')
    def gmt_create(self) -> Optional[pulumi.Input[str]]:
        """
        The creation time of the gateway slb.
        """
        return pulumi.get(self, 'gmt_create')

    @gmt_create.setter
    def gmt_create(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'gmt_create', value)

    @property
    @pulumi.getter(name='slbId')
    def slb_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the gateway slb.
        """
        return pulumi.get(self, 'slb_id')

    @slb_id.setter
    def slb_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'slb_id', value)

    @property
    @pulumi.getter(name='slbIp')
    def slb_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The ip of the gateway slb.
        """
        return pulumi.get(self, 'slb_ip')

    @slb_ip.setter
    def slb_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'slb_ip', value)

    @property
    @pulumi.getter(name='slbPort')
    def slb_port(self) -> Optional[pulumi.Input[str]]:
        """
        The port of the gateway slb.
        """
        return pulumi.get(self, 'slb_port')

    @slb_port.setter
    def slb_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'slb_port', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the gateway slb.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)