"""
NSX-V3 Plugin router module
"""
import copy
from oslo_log import log
from vmware_nsxlib._i18n import _
from vmware_nsxlib.v3 import exceptions
from vmware_nsxlib.v3 import nsx_constants
from vmware_nsxlib.v3 import utils
LOG = log.getLogger(__name__)
MIN_EDGE_NODE_NUM = 1
TIER0_ROUTER_LINK_PORT_NAME = 'TIER0-RouterLinkPort'
TIER1_ROUTER_LINK_PORT_NAME = 'TIER1-RouterLinkPort'
ROUTER_INTF_PORT_NAME = 'Tier1-RouterDownLinkPort'
FIP_NAT_PRI = 900
GW_NAT_PRI = 1000

class RouterLib(object):

    def __init__(self, router_client, router_port_client, nsxlib):
        self._router_client = router_client
        self._router_port_client = router_port_client
        self.nsxlib = nsxlib

    def validate_tier0(self, tier0_groups_dict, tier0_uuid):
        err_msg = None
        if not tier0_uuid:
            err_msg = _('validate_tier0 should be called with tier0 uuid')
            raise exceptions.NsxLibInvalidInput(error_message=err_msg)
        try:
            lrouter = self._router_client.get(tier0_uuid)
        except exceptions.ResourceNotFound:
            err_msg = _('Tier0 router %s not found at the backend. Either a valid UUID must be specified or a default tier0 router UUID must be configured in nsx.ini') % tier0_uuid
        else:
            edge_cluster_uuid = lrouter.get('edge_cluster_id')
            if not edge_cluster_uuid:
                err_msg = _('Failed to get edge cluster uuid from tier0 router %s at the backend') % lrouter
            else:
                edge_cluster = self.nsxlib.edge_cluster.get(edge_cluster_uuid)
                member_index_list = [member['member_index'] for member in edge_cluster['members']]
                if len(member_index_list) < MIN_EDGE_NODE_NUM:
                    err_msg = _('%(act_num)s edge members found in edge_cluster %(cluster_id)s, however we require at least %(exp_num)s edge nodes in edge cluster for use') % {'act_num': len(member_index_list), 'exp_num': MIN_EDGE_NODE_NUM, 'cluster_id': edge_cluster_uuid}
        if err_msg:
            raise exceptions.NsxLibInvalidInput(error_message=err_msg)
        else:
            tier0_groups_dict[tier0_uuid] = {'edge_cluster_uuid': edge_cluster_uuid, 'member_index_list': member_index_list}

    def add_router_link_port(self, tier1_uuid, tier0_uuid, tags):
        t0_tags = copy.copy(tags)
        t0_tags = utils.add_v3_tag(t0_tags, 'os-tier0-uuid', tier0_uuid)
        tier0_link_port = self._router_port_client.create(tier0_uuid, display_name=TIER0_ROUTER_LINK_PORT_NAME, tags=t0_tags, resource_type=nsx_constants.LROUTERPORT_LINKONTIER0, logical_port_id=None, address_groups=None)
        linked_logical_port_id = tier0_link_port['id']
        t1_tags = copy.copy(tags)
        t1_tags = utils.add_v3_tag(t1_tags, 'os-tier1-uuid', tier1_uuid)
        try:
            tier1_link_port = self._router_port_client.create(tier1_uuid, display_name=TIER1_ROUTER_LINK_PORT_NAME, tags=t1_tags, resource_type=nsx_constants.LROUTERPORT_LINKONTIER1, logical_port_id=linked_logical_port_id, address_groups=None)
            return (tier0_link_port, tier1_link_port)
        except Exception as e:
            LOG.warning('Failed to create tier1 link port for tier1 router %s, deleting peer tier0 link port %s: %s', tier1_uuid, linked_logical_port_id, e)
            self._router_port_client.delete(linked_logical_port_id)
            raise e

    def remove_router_link_port(self, tier1_uuid, tier0_uuid=None):
        try:
            tier1_link_port = self._router_port_client.get_tier1_link_port(tier1_uuid)
        except exceptions.ResourceNotFound:
            LOG.warning('Logical router link port for tier1 router: %s not found at the backend', tier1_uuid)
            return
        tier1_link_port_id = tier1_link_port['id']
        tier0_link_port_id = tier1_link_port['linked_logical_router_port_id'].get('target_id')
        self._router_port_client.delete(tier1_link_port_id)
        self._router_port_client.delete(tier0_link_port_id)

    def add_centralized_service_port(self, logical_router_id, display_name=None, tags=None, logical_port_id=None, address_groups=None):
        return self._router_port_client.create(logical_router_id, display_name=display_name, tags=tags, logical_port_id=logical_port_id, address_groups=address_groups, resource_type=nsx_constants.LROUTERPORT_CENTRALIZED)

    def update_advertisement(self, logical_router_id, advertise_route_nat, advertise_route_connected, advertise_route_static=False, enabled=True, advertise_lb_vip=False, advertise_lb_snat_ip=False):
        return self.nsxlib.logical_router.update_advertisement(logical_router_id, advertise_nat_routes=advertise_route_nat, advertise_nsx_connected_routes=advertise_route_connected, advertise_static_routes=advertise_route_static, enabled=enabled, advertise_lb_vip=advertise_lb_vip, advertise_lb_snat_ip=advertise_lb_snat_ip)

    def delete_gw_snat_rule(self, logical_router_id, gw_ip):
        """Delete router snat rule matching the gw ip

        assuming there is only one
        """
        return self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, translated_network=gw_ip)

    def delete_gw_snat_rule_by_source(self, logical_router_id, gw_ip, source_net, skip_not_found=False):
        """Delete router snat rule matching the gw ip & source"""
        return self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, translated_network=gw_ip, match_source_network=source_net, skip_not_found=skip_not_found, strict_mode=not skip_not_found)

    def delete_gw_snat_rules(self, logical_router_id, gw_ip):
        """Delete all the snat rules on the router with a specific gw ip"""
        return self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, translated_network=gw_ip, skip_not_found=True, strict_mode=False)

    def add_gw_snat_rule(self, logical_router_id, gw_ip, source_net=None, bypass_firewall=True, tags=None, display_name=None):
        return self.nsxlib.logical_router.add_nat_rule(logical_router_id, action='SNAT', translated_network=gw_ip, source_net=source_net, rule_priority=GW_NAT_PRI, bypass_firewall=bypass_firewall, tags=tags, display_name=display_name)

    def update_router_edge_cluster(self, nsx_router_id, edge_cluster_uuid):
        return self._router_client.update(nsx_router_id, edge_cluster_id=edge_cluster_uuid)

    def update_router_transport_zone(self, nsx_router_id, transport_zone_id):
        return self._router_client.update(nsx_router_id, transport_zone_id=transport_zone_id)

    def create_logical_router_intf_port_by_ls_id(self, logical_router_id, display_name, tags, ls_id, logical_switch_port_id, address_groups, urpf_mode=None, relay_service_uuid=None, resource_type=None):
        try:
            port = self._router_port_client.get_by_lswitch_id(ls_id)
        except exceptions.ResourceNotFound:
            if resource_type is None:
                resource_type = nsx_constants.LROUTERPORT_DOWNLINK
            return self._router_port_client.create(logical_router_id, display_name, tags, resource_type, logical_switch_port_id, address_groups, urpf_mode=urpf_mode, relay_service_uuid=relay_service_uuid)
        else:
            return self._router_port_client.update(port['id'], subnets=address_groups, relay_service_uuid=relay_service_uuid)

    def add_fip_nat_rules(self, logical_router_id, ext_ip, int_ip, match_ports=None, bypass_firewall=True, tags=None, display_name=None):
        self.nsxlib.logical_router.add_nat_rule(logical_router_id, action='SNAT', translated_network=ext_ip, source_net=int_ip, rule_priority=FIP_NAT_PRI, bypass_firewall=bypass_firewall, tags=tags, display_name=display_name)
        self.nsxlib.logical_router.add_nat_rule(logical_router_id, action='DNAT', translated_network=int_ip, dest_net=ext_ip, rule_priority=FIP_NAT_PRI, match_ports=match_ports, bypass_firewall=bypass_firewall, tags=tags, display_name=display_name)

    def delete_fip_nat_rules_by_internal_ip(self, logical_router_id, int_ip):
        self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, action='SNAT', match_source_network=int_ip)
        self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, action='DNAT', translated_network=int_ip)

    def delete_fip_nat_rules(self, logical_router_id, ext_ip, int_ip):
        self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, action='SNAT', translated_network=ext_ip, match_source_network=int_ip)
        self.nsxlib.logical_router.delete_nat_rule_by_values(logical_router_id, action='DNAT', translated_network=int_ip, match_destination_network=ext_ip)

    def add_static_routes(self, nsx_router_id, route):
        return self.nsxlib.logical_router.add_static_route(nsx_router_id, route['destination'], route['nexthop'])

    def delete_static_routes(self, nsx_router_id, route):
        return self.nsxlib.logical_router.delete_static_route_by_values(nsx_router_id, dest_cidr=route['destination'], nexthop=route['nexthop'])

    def change_edge_firewall_status(self, nsx_router_id, action=nsx_constants.FW_DISABLE):
        return self.nsxlib.logical_router.change_edge_firewall_status(nsx_router_id, action)

    def has_service_router(self, nsx_router_id):
        lrouter = self._router_client.get(nsx_router_id)
        if lrouter and lrouter.get('edge_cluster_id'):
            return True
        return False

    def get_tier0_router_tz(self, tier0_uuid):
        lrouter = self._router_client.get(tier0_uuid)
        edge_cluster_uuid = lrouter.get('edge_cluster_id')
        if not edge_cluster_uuid:
            return []
        tier0_transport_nodes = self.nsxlib.edge_cluster.get_transport_nodes(edge_cluster_uuid)
        tier0_tzs = []
        for tn_uuid in tier0_transport_nodes:
            tier0_tzs.extend(self.nsxlib.transport_node.get_transport_zones(tn_uuid))
        return tier0_tzs

    def get_tier0_router_overlay_tz(self, tier0_uuid):
        lrouter = self._router_client.get(tier0_uuid)
        tz_uuid = lrouter.get('advanced_config', {}).get('transport_zone_id')
        if tz_uuid:
            return tz_uuid
        tz_uuids = self.get_tier0_router_tz(tier0_uuid)
        for tz_uuid in tz_uuids:
            backend_type = self.nsxlib.transport_zone.get_transport_type(tz_uuid)
            if backend_type == self.nsxlib.transport_zone.TRANSPORT_TYPE_OVERLAY:
                return tz_uuid

    def get_connected_t0_transit_net(self, tier1_uuid):
        """Return the IP of the tier1->tier0 link port

        return None if the router is not connected to a tier0 router
        """
        try:
            tier1_link_port = self._router_port_client.get_tier1_link_port(tier1_uuid)
        except exceptions.ResourceNotFound:
            return
        for subnet in tier1_link_port.get('subnets', []):
            for ip_address in subnet.get('ip_addresses'):
                return ip_address