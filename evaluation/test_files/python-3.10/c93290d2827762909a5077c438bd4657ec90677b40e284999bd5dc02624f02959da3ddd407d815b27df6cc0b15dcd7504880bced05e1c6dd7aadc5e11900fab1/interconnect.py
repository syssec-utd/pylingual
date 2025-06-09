import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['InterconnectArgs', 'Interconnect']

@pulumi.input_type
class InterconnectArgs:

    def __init__(__self__, *, admin_enabled: Optional[pulumi.Input[bool]]=None, customer_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, interconnect_type: Optional[pulumi.Input['InterconnectInterconnectType']]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, link_type: Optional[pulumi.Input['InterconnectLinkType']]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, noc_contact_email: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, requested_link_count: Optional[pulumi.Input[int]]=None):
        """
        The set of arguments for constructing a Interconnect resource.
        :param pulumi.Input[bool] admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true.
        :param pulumi.Input[str] customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input['InterconnectInterconnectType'] interconnect_type: Type of interconnect, which can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty.
        :param pulumi.Input['InterconnectLinkType'] link_type: Type of link requested, which can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle.
        :param pulumi.Input[str] location: URL of the InterconnectLocation object that represents where this connection is to be provisioned.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[str] noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Stackdriver logs alerting and Cloud Notifications.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[int] requested_link_count: Target number of physical links in the link bundle, as requested by the customer.
        """
        if admin_enabled is not None:
            pulumi.set(__self__, 'admin_enabled', admin_enabled)
        if customer_name is not None:
            pulumi.set(__self__, 'customer_name', customer_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if interconnect_type is not None:
            pulumi.set(__self__, 'interconnect_type', interconnect_type)
        if labels is not None:
            pulumi.set(__self__, 'labels', labels)
        if link_type is not None:
            pulumi.set(__self__, 'link_type', link_type)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if noc_contact_email is not None:
            pulumi.set(__self__, 'noc_contact_email', noc_contact_email)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if request_id is not None:
            pulumi.set(__self__, 'request_id', request_id)
        if requested_link_count is not None:
            pulumi.set(__self__, 'requested_link_count', requested_link_count)

    @property
    @pulumi.getter(name='adminEnabled')
    def admin_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true.
        """
        return pulumi.get(self, 'admin_enabled')

    @admin_enabled.setter
    def admin_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'admin_enabled', value)

    @property
    @pulumi.getter(name='customerName')
    def customer_name(self) -> Optional[pulumi.Input[str]]:
        """
        Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.
        """
        return pulumi.get(self, 'customer_name')

    @customer_name.setter
    def customer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'customer_name', value)

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
    @pulumi.getter(name='interconnectType')
    def interconnect_type(self) -> Optional[pulumi.Input['InterconnectInterconnectType']]:
        """
        Type of interconnect, which can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED.
        """
        return pulumi.get(self, 'interconnect_type')

    @interconnect_type.setter
    def interconnect_type(self, value: Optional[pulumi.Input['InterconnectInterconnectType']]):
        pulumi.set(self, 'interconnect_type', value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty.
        """
        return pulumi.get(self, 'labels')

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'labels', value)

    @property
    @pulumi.getter(name='linkType')
    def link_type(self) -> Optional[pulumi.Input['InterconnectLinkType']]:
        """
        Type of link requested, which can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle.
        """
        return pulumi.get(self, 'link_type')

    @link_type.setter
    def link_type(self, value: Optional[pulumi.Input['InterconnectLinkType']]):
        pulumi.set(self, 'link_type', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the InterconnectLocation object that represents where this connection is to be provisioned.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

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
    @pulumi.getter(name='nocContactEmail')
    def noc_contact_email(self) -> Optional[pulumi.Input[str]]:
        """
        Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Stackdriver logs alerting and Cloud Notifications.
        """
        return pulumi.get(self, 'noc_contact_email')

    @noc_contact_email.setter
    def noc_contact_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'noc_contact_email', value)

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
    @pulumi.getter(name='requestedLinkCount')
    def requested_link_count(self) -> Optional[pulumi.Input[int]]:
        """
        Target number of physical links in the link bundle, as requested by the customer.
        """
        return pulumi.get(self, 'requested_link_count')

    @requested_link_count.setter
    def requested_link_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'requested_link_count', value)

class Interconnect(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, admin_enabled: Optional[pulumi.Input[bool]]=None, customer_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, interconnect_type: Optional[pulumi.Input['InterconnectInterconnectType']]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, link_type: Optional[pulumi.Input['InterconnectLinkType']]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, noc_contact_email: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, requested_link_count: Optional[pulumi.Input[int]]=None, __props__=None):
        """
        Creates a Interconnect in the specified project using the data included in the request.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] admin_enabled: Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true.
        :param pulumi.Input[str] customer_name: Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input['InterconnectInterconnectType'] interconnect_type: Type of interconnect, which can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty.
        :param pulumi.Input['InterconnectLinkType'] link_type: Type of link requested, which can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle.
        :param pulumi.Input[str] location: URL of the InterconnectLocation object that represents where this connection is to be provisioned.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[str] noc_contact_email: Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Stackdriver logs alerting and Cloud Notifications.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[int] requested_link_count: Target number of physical links in the link bundle, as requested by the customer.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: Optional[InterconnectArgs]=None, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a Interconnect in the specified project using the data included in the request.

        :param str resource_name: The name of the resource.
        :param InterconnectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(InterconnectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, admin_enabled: Optional[pulumi.Input[bool]]=None, customer_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, interconnect_type: Optional[pulumi.Input['InterconnectInterconnectType']]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, link_type: Optional[pulumi.Input['InterconnectLinkType']]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, noc_contact_email: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, requested_link_count: Optional[pulumi.Input[int]]=None, __props__=None):
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
            __props__ = InterconnectArgs.__new__(InterconnectArgs)
            __props__.__dict__['admin_enabled'] = admin_enabled
            __props__.__dict__['customer_name'] = customer_name
            __props__.__dict__['description'] = description
            __props__.__dict__['interconnect_type'] = interconnect_type
            __props__.__dict__['labels'] = labels
            __props__.__dict__['link_type'] = link_type
            __props__.__dict__['location'] = location
            __props__.__dict__['name'] = name
            __props__.__dict__['noc_contact_email'] = noc_contact_email
            __props__.__dict__['project'] = project
            __props__.__dict__['request_id'] = request_id
            __props__.__dict__['requested_link_count'] = requested_link_count
            __props__.__dict__['circuit_infos'] = None
            __props__.__dict__['creation_timestamp'] = None
            __props__.__dict__['expected_outages'] = None
            __props__.__dict__['google_ip_address'] = None
            __props__.__dict__['google_reference_id'] = None
            __props__.__dict__['interconnect_attachments'] = None
            __props__.__dict__['kind'] = None
            __props__.__dict__['label_fingerprint'] = None
            __props__.__dict__['operational_status'] = None
            __props__.__dict__['peer_ip_address'] = None
            __props__.__dict__['provisioned_link_count'] = None
            __props__.__dict__['satisfies_pzs'] = None
            __props__.__dict__['self_link'] = None
            __props__.__dict__['state'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Interconnect, __self__).__init__('google-native:compute/beta:Interconnect', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Interconnect':
        """
        Get an existing Interconnect resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = InterconnectArgs.__new__(InterconnectArgs)
        __props__.__dict__['admin_enabled'] = None
        __props__.__dict__['circuit_infos'] = None
        __props__.__dict__['creation_timestamp'] = None
        __props__.__dict__['customer_name'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['expected_outages'] = None
        __props__.__dict__['google_ip_address'] = None
        __props__.__dict__['google_reference_id'] = None
        __props__.__dict__['interconnect_attachments'] = None
        __props__.__dict__['interconnect_type'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['label_fingerprint'] = None
        __props__.__dict__['labels'] = None
        __props__.__dict__['link_type'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['noc_contact_email'] = None
        __props__.__dict__['operational_status'] = None
        __props__.__dict__['peer_ip_address'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['provisioned_link_count'] = None
        __props__.__dict__['request_id'] = None
        __props__.__dict__['requested_link_count'] = None
        __props__.__dict__['satisfies_pzs'] = None
        __props__.__dict__['self_link'] = None
        __props__.__dict__['state'] = None
        return Interconnect(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='adminEnabled')
    def admin_enabled(self) -> pulumi.Output[bool]:
        """
        Administrative status of the interconnect. When this is set to true, the Interconnect is functional and can carry traffic. When set to false, no packets can be carried over the interconnect and no BGP routes are exchanged over it. By default, the status is set to true.
        """
        return pulumi.get(self, 'admin_enabled')

    @property
    @pulumi.getter(name='circuitInfos')
    def circuit_infos(self) -> pulumi.Output[Sequence['outputs.InterconnectCircuitInfoResponse']]:
        """
        A list of CircuitInfo objects, that describe the individual circuits in this LAG.
        """
        return pulumi.get(self, 'circuit_infos')

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter(name='customerName')
    def customer_name(self) -> pulumi.Output[str]:
        """
        Customer name, to put in the Letter of Authorization as the party authorized to request a crossconnect.
        """
        return pulumi.get(self, 'customer_name')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='expectedOutages')
    def expected_outages(self) -> pulumi.Output[Sequence['outputs.InterconnectOutageNotificationResponse']]:
        """
        A list of outages expected for this Interconnect.
        """
        return pulumi.get(self, 'expected_outages')

    @property
    @pulumi.getter(name='googleIpAddress')
    def google_ip_address(self) -> pulumi.Output[str]:
        """
        IP address configured on the Google side of the Interconnect link. This can be used only for ping tests.
        """
        return pulumi.get(self, 'google_ip_address')

    @property
    @pulumi.getter(name='googleReferenceId')
    def google_reference_id(self) -> pulumi.Output[str]:
        """
        Google reference ID to be used when raising support tickets with Google or otherwise to debug backend connectivity issues.
        """
        return pulumi.get(self, 'google_reference_id')

    @property
    @pulumi.getter(name='interconnectAttachments')
    def interconnect_attachments(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of the URLs of all InterconnectAttachments configured to use this Interconnect.
        """
        return pulumi.get(self, 'interconnect_attachments')

    @property
    @pulumi.getter(name='interconnectType')
    def interconnect_type(self) -> pulumi.Output[str]:
        """
        Type of interconnect, which can take one of the following values: - PARTNER: A partner-managed interconnection shared between customers though a partner. - DEDICATED: A dedicated physical interconnection with the customer. Note that a value IT_PRIVATE has been deprecated in favor of DEDICATED.
        """
        return pulumi.get(self, 'interconnect_type')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Type of the resource. Always compute#interconnect for interconnects.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='labelFingerprint')
    def label_fingerprint(self) -> pulumi.Output[str]:
        """
        A fingerprint for the labels being applied to this Interconnect, which is essentially a hash of the labels set used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve an Interconnect.
        """
        return pulumi.get(self, 'label_fingerprint')

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter(name='linkType')
    def link_type(self) -> pulumi.Output[str]:
        """
        Type of link requested, which can take one of the following values: - LINK_TYPE_ETHERNET_10G_LR: A 10G Ethernet with LR optics - LINK_TYPE_ETHERNET_100G_LR: A 100G Ethernet with LR optics. Note that this field indicates the speed of each of the links in the bundle, not the speed of the entire bundle.
        """
        return pulumi.get(self, 'link_type')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        URL of the InterconnectLocation object that represents where this connection is to be provisioned.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='nocContactEmail')
    def noc_contact_email(self) -> pulumi.Output[str]:
        """
        Email address to contact the customer NOC for operations and maintenance notifications regarding this Interconnect. If specified, this will be used for notifications in addition to all other forms described, such as Stackdriver logs alerting and Cloud Notifications.
        """
        return pulumi.get(self, 'noc_contact_email')

    @property
    @pulumi.getter(name='operationalStatus')
    def operational_status(self) -> pulumi.Output[str]:
        """
        The current status of this Interconnect's functionality, which can take one of the following values: - OS_ACTIVE: A valid Interconnect, which is turned up and is ready to use. Attachments may be provisioned on this Interconnect. - OS_UNPROVISIONED: An Interconnect that has not completed turnup. No attachments may be provisioned on this Interconnect. - OS_UNDER_MAINTENANCE: An Interconnect that is undergoing internal maintenance. No attachments may be provisioned or updated on this Interconnect. 
        """
        return pulumi.get(self, 'operational_status')

    @property
    @pulumi.getter(name='peerIpAddress')
    def peer_ip_address(self) -> pulumi.Output[str]:
        """
        IP address configured on the customer side of the Interconnect link. The customer should configure this IP address during turnup when prompted by Google NOC. This can be used only for ping tests.
        """
        return pulumi.get(self, 'peer_ip_address')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter(name='provisionedLinkCount')
    def provisioned_link_count(self) -> pulumi.Output[int]:
        """
        Number of links actually provisioned in this interconnect.
        """
        return pulumi.get(self, 'provisioned_link_count')

    @property
    @pulumi.getter(name='requestId')
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, 'request_id')

    @property
    @pulumi.getter(name='requestedLinkCount')
    def requested_link_count(self) -> pulumi.Output[int]:
        """
        Target number of physical links in the link bundle, as requested by the customer.
        """
        return pulumi.get(self, 'requested_link_count')

    @property
    @pulumi.getter(name='satisfiesPzs')
    def satisfies_pzs(self) -> pulumi.Output[bool]:
        """
        Set to true if the resource satisfies the zone separation organization policy constraints and false otherwise. Defaults to false if the field is not present.
        """
        return pulumi.get(self, 'satisfies_pzs')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> pulumi.Output[str]:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of Interconnect functionality, which can take one of the following values: - ACTIVE: The Interconnect is valid, turned up and ready to use. Attachments may be provisioned on this Interconnect. - UNPROVISIONED: The Interconnect has not completed turnup. No attachments may be provisioned on this Interconnect. - UNDER_MAINTENANCE: The Interconnect is undergoing internal maintenance. No attachments may be provisioned or updated on this Interconnect. 
        """
        return pulumi.get(self, 'state')