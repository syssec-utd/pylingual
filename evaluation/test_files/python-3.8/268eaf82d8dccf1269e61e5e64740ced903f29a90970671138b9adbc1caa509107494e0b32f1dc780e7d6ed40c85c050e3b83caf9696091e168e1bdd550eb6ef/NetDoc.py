"""Script used to check NetDoc integrity."""
__author__ = 'Andrea Dainese'
__contact__ = 'andrea@adainese.it'
__copyright__ = 'Copyright 2022, Andrea Dainese'
__license__ = 'GPLv3'
from extras.reports import Report
from dcim.models import Interface
from ipam.models import Prefix, IPAddress
from netdoc import utils
from netdoc.models import ArpTableEntry

class InterfaceLabels(Report):
    """Check current Interface label compared to Interface name."""
    description = 'Check Interface label compared to Interface name'

    def test_label(self):
        """Test Interface name/label integrity."""
        interface_qs = Interface.objects.all()
        for interface_o in interface_qs:
            name = interface_o.name
            label = interface_o.label
            if utils.normalize_interface_label(name) == label:
                self.log_success(interface_o)
            else:
                self.log_failure(interface_o, 'Interface label does not match interface name')

class VRFIpPrefixIntegrityCheck(Report):
    """Check integrity between VRF, Interface, IPAddress, and Prefix.

    The report verifies that:
    * Interface.VRF == Interface.IPAddress.VRF -> warning if not
    * Interface.IPAddress.VRF in Prefix.VRF -> error if not

    If Interface.VRF != Interface.IPAddress.VRF the user should check if this is expected
    (e.g. when Interface is configured in global but the IPAddress is part of a VRF).

    If Prefix.VRF does not exist for Interface.IPAddress.VRF the user should create it.
    """
    description = 'Check (1) VRF between Interface and IP address,  and' + '(2) prefix exist for the IP address within the same VRF'

    def test_vrf(self):
        """Test VRF between Interface and Interface's IPAddress."""
        interface_qs = Interface.objects.filter(ip_addresses__isnull=False)
        for interface_o in interface_qs:
            interface_vrf_o = interface_o.vrf
            ipaddress_vrf_o = interface_o.ip_addresses.first().vrf
            if interface_vrf_o == ipaddress_vrf_o:
                self.log_success(interface_o)
            else:
                self.log_warning(interface_o, f"VRF differs between interface ({interface_vrf_o}) and interface's IP address ({ipaddress_vrf_o})")

    def test_interface_prefix(self):
        """Test Interface's IPAddress owned by a Prefix."""
        interface_qs = Interface.objects.filter(ip_addresses__isnull=False)
        for interface_o in interface_qs:
            for ip_address_o in interface_o.ip_addresses.all():
                vrf_o = ip_address_o.vrf
                network = f'{str(ip_address_o.address.network)}/{str(ip_address_o.address.prefixlen)}'
                prefix_qs = Prefix.objects.filter(prefix=network, vrf=vrf_o)
                if prefix_qs:
                    self.log_success(interface_o)
                else:
                    self.log_failure(interface_o, f'Prefix missing for IP address {str(ip_address_o.address)} with VRF {vrf_o}')

    def test_address_prefix(self):
        """Test IPAddress owned by a Prefix."""
        ipaddress_qs = IPAddress.objects.all()
        for ip_address_o in ipaddress_qs:
            vrf_o = ip_address_o.vrf
            network = f'{str(ip_address_o.address.network)}/{str(ip_address_o.address.prefixlen)}'
            prefix_qs = Prefix.objects.filter(prefix=network, vrf=vrf_o)
            if prefix_qs:
                self.log_success(ip_address_o)
            else:
                self.log_failure(ip_address_o, f'Prefix missing for IP address {str(ip_address_o.address)} with VRF {vrf_o}')

class IPAMFromARP(Report):
    """Check corrispondence between ARP table and IPAM."""
    description = 'Check corrispondence between ARP table and IPAM'

    def test_ipam(self):
        """For each ARP, check if an IPAddress exist.

        ARPTableEntry.Interface.IPAddress.VRF must be equal to IPAddress.VRF.
        """
        for arptableentry_o in ArpTableEntry.objects.all():
            try:
                interface_vrf_o = arptableentry_o.interface.ip_addresses.first().vrf
            except AttributeError:
                self.log_failure(arptableentry_o, f'IP address not found on interface {arptableentry_o.interface}, maybe some ingestion script has failed')
                continue
            address = str(arptableentry_o.ip_address.ip)
            prefixlen = arptableentry_o.interface.ip_addresses.filter(address__net_contains_or_equals=address).first().address.prefixlen
            ip_address = f'{address}/{prefixlen}'
            ipaddresses_qs = IPAddress.objects.filter(vrf=interface_vrf_o, address=ip_address)
            if ipaddresses_qs:
                self.log_success(arptableentry_o)
            else:
                self.log_warning(arptableentry_o, f'IP address {str(arptableentry_o.ip_address)} not found in IPAM for VRF {interface_vrf_o}')