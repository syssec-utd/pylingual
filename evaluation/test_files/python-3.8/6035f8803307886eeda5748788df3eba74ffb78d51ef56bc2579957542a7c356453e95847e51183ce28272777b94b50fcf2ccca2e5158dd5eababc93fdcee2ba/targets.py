from typing import Any, List, Optional
from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.targets import AliveTest
from gvm.protocols.gmpv208.entities.targets import TargetsMixin as Gmp208TargetsMixin
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

class TargetsMixin(Gmp208TargetsMixin):

    def create_target(self, name: str, *, asset_hosts_filter: Optional[str]=None, hosts: Optional[List[str]]=None, comment: Optional[str]=None, exclude_hosts: Optional[List[str]]=None, ssh_credential_id: Optional[str]=None, ssh_credential_port: Optional[int]=None, smb_credential_id: Optional[str]=None, esxi_credential_id: Optional[str]=None, snmp_credential_id: Optional[str]=None, alive_test: Optional[AliveTest]=None, allow_simultaneous_ips: Optional[bool]=None, reverse_lookup_only: Optional[bool]=None, reverse_lookup_unify: Optional[bool]=None, port_range: Optional[str]=None, port_list_id: Optional[str]=None) -> Any:
        """Create a new target

        Arguments:
            name: Name of the target
            asset_hosts_filter: Filter to select target host from assets hosts
            hosts: List of hosts addresses to scan
            exclude_hosts: List of hosts addresses to exclude from scan
            comment: Comment for the target
            ssh_credential_id: UUID of a ssh credential to use on target
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of a smb credential to use on target
            snmp_credential_id: UUID of a snmp credential to use on target
            esxi_credential_id: UUID of a esxi credential to use on target
            alive_test: Which alive test to use
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
            port_range: Port range for the target
            port_list_id: UUID of the port list to use on target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(function=self.create_target.__name__, argument='name')
        cmd = XmlCommand('create_target')
        cmd.add_element('name', name)
        if asset_hosts_filter:
            cmd.add_element('asset_hosts', attrs={'filter': str(asset_hosts_filter)})
        elif hosts:
            cmd.add_element('hosts', to_comma_list(hosts))
        else:
            raise RequiredArgument(function=self.create_target.__name__, argument='hosts or asset_hosts_filter')
        if comment:
            cmd.add_element('comment', comment)
        if exclude_hosts:
            cmd.add_element('exclude_hosts', to_comma_list(exclude_hosts))
        if ssh_credential_id:
            _xmlssh = cmd.add_element('ssh_credential', attrs={'id': ssh_credential_id})
            if ssh_credential_port:
                _xmlssh.add_element('port', str(ssh_credential_port))
        if smb_credential_id:
            cmd.add_element('smb_credential', attrs={'id': smb_credential_id})
        if esxi_credential_id:
            cmd.add_element('esxi_credential', attrs={'id': esxi_credential_id})
        if snmp_credential_id:
            cmd.add_element('snmp_credential', attrs={'id': snmp_credential_id})
        if alive_test:
            if not isinstance(alive_test, AliveTest):
                raise InvalidArgumentType(function=self.create_target.__name__, argument='alive_test', arg_type=AliveTest.__name__)
            cmd.add_element('alive_tests', alive_test.value)
        if allow_simultaneous_ips is not None:
            cmd.add_element('allow_simultaneous_ips', to_bool(allow_simultaneous_ips))
        if reverse_lookup_only is not None:
            cmd.add_element('reverse_lookup_only', to_bool(reverse_lookup_only))
        if reverse_lookup_unify is not None:
            cmd.add_element('reverse_lookup_unify', to_bool(reverse_lookup_unify))
        if port_range:
            cmd.add_element('port_range', port_range)
        if port_list_id:
            cmd.add_element('port_list', attrs={'id': port_list_id})
        return self._send_xml_command(cmd)

    def modify_target(self, target_id: str, *, name: Optional[str]=None, comment: Optional[str]=None, hosts: Optional[List[str]]=None, exclude_hosts: Optional[List[str]]=None, ssh_credential_id: Optional[str]=None, ssh_credential_port: Optional[bool]=None, smb_credential_id: Optional[str]=None, esxi_credential_id: Optional[str]=None, snmp_credential_id: Optional[str]=None, alive_test: Optional[AliveTest]=None, allow_simultaneous_ips: Optional[bool]=None, reverse_lookup_only: Optional[bool]=None, reverse_lookup_unify: Optional[bool]=None, port_list_id: Optional[str]=None) -> Any:
        """Modifies an existing target.

        Arguments:
            target_id: ID of target to modify.
            comment: Comment on target.
            name: Name of target.
            hosts: List of target hosts.
            exclude_hosts: A list of hosts to exclude.
            ssh_credential_id: UUID of SSH credential to use on target.
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of SMB credential to use on target.
            esxi_credential_id: UUID of ESXi credential to use on target.
            snmp_credential_id: UUID of SNMP credential to use on target.
            port_list_id: UUID of port list describing ports to scan.
            alive_test: Which alive tests to use.
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names.
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(function=self.modify_target.__name__, argument='target_id')
        cmd = XmlCommand('modify_target')
        cmd.set_attribute('target_id', target_id)
        if comment:
            cmd.add_element('comment', comment)
        if name:
            cmd.add_element('name', name)
        if hosts:
            cmd.add_element('hosts', to_comma_list(hosts))
            if exclude_hosts is None:
                exclude_hosts = ['']
        if exclude_hosts:
            cmd.add_element('exclude_hosts', to_comma_list(exclude_hosts))
        if alive_test:
            if not isinstance(alive_test, AliveTest):
                raise InvalidArgumentType(function=self.modify_target.__name__, argument='alive_test', arg_type=AliveTest.__name__)
            cmd.add_element('alive_tests', alive_test.value)
        if ssh_credential_id:
            _xmlssh = cmd.add_element('ssh_credential', attrs={'id': ssh_credential_id})
            if ssh_credential_port:
                _xmlssh.add_element('port', str(ssh_credential_port))
        if smb_credential_id:
            cmd.add_element('smb_credential', attrs={'id': smb_credential_id})
        if esxi_credential_id:
            cmd.add_element('esxi_credential', attrs={'id': esxi_credential_id})
        if snmp_credential_id:
            cmd.add_element('snmp_credential', attrs={'id': snmp_credential_id})
        if allow_simultaneous_ips is not None:
            cmd.add_element('allow_simultaneous_ips', to_bool(allow_simultaneous_ips))
        if reverse_lookup_only is not None:
            cmd.add_element('reverse_lookup_only', to_bool(reverse_lookup_only))
        if reverse_lookup_unify is not None:
            cmd.add_element('reverse_lookup_unify', to_bool(reverse_lookup_unify))
        if port_list_id:
            cmd.add_element('port_list', attrs={'id': port_list_id})
        return self._send_xml_command(cmd)