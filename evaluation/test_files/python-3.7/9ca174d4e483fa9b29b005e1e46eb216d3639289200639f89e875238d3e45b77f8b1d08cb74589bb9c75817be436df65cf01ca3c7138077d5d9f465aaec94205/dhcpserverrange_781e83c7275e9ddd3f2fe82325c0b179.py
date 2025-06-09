import sys
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class DhcpServerRange(Base):
    """Configuration parameters for a pool of IPv4/IPv6 addresses.
    The DhcpServerRange class encapsulates a required dhcpServerRange resource which will be retrieved from the server every time the property is accessed.
    """
    __slots__ = ()
    _SDM_NAME = 'dhcpServerRange'
    _SDM_ATT_MAP = {'Count': 'count', 'Dhcp4EchoRelayInfo': 'dhcp4EchoRelayInfo', 'Dhcp6IaType': 'dhcp6IaType', 'Enabled': 'enabled', 'IpAddress': 'ipAddress', 'IpAddressIncrement': 'ipAddressIncrement', 'IpAddressPoolIncrement': 'ipAddressPoolIncrement', 'IpAddressPrefix': 'ipAddressPrefix', 'IpAddressPrefixIncrement': 'ipAddressPrefixIncrement', 'IpAddressPrefixPoolIncrement': 'ipAddressPrefixPoolIncrement', 'IpDns1': 'ipDns1', 'IpDns2': 'ipDns2', 'IpGateway': 'ipGateway', 'IpGatewayIncrement': 'ipGatewayIncrement', 'IpPrefix': 'ipPrefix', 'IpType': 'ipType', 'Name': 'name', 'ObjectId': 'objectId', 'PrefixCount': 'prefixCount', 'PrefixLength': 'prefixLength', 'ServerAddress': 'serverAddress', 'ServerAddressIncrement': 'serverAddressIncrement', 'ServerCount': 'serverCount', 'ServerGateway': 'serverGateway', 'ServerGatewayIncrement': 'serverGatewayIncrement', 'ServerPrefix': 'serverPrefix', 'UseRapidCommit': 'useRapidCommit'}
    _SDM_ENUM_MAP = {}

    def __init__(self, parent, list_op=False):
        super(DhcpServerRange, self).__init__(parent, list_op)

    @property
    def Count(self):
        """
        Returns
        -------
        - number: The number of leases to be allocated per each server address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @Count.setter
    def Count(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Count'], value)

    @property
    def Dhcp4EchoRelayInfo(self):
        """
        Returns
        -------
        - bool: Enable echoing of DHCP option 82.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Dhcp4EchoRelayInfo'])

    @Dhcp4EchoRelayInfo.setter
    def Dhcp4EchoRelayInfo(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Dhcp4EchoRelayInfo'], value)

    @property
    def Dhcp6IaType(self):
        """
        Returns
        -------
        - str: The Identity Association type supported by IPv6 address pools.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Dhcp6IaType'])

    @Dhcp6IaType.setter
    def Dhcp6IaType(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Dhcp6IaType'], value)

    @property
    def Enabled(self):
        """
        Returns
        -------
        - bool: Disabled ranges won't be configured nor validated.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Enabled'])

    @Enabled.setter
    def Enabled(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Enabled'], value)

    @property
    def IpAddress(self):
        """
        Returns
        -------
        - str: The IP address of the first lease pool.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddress'])

    @IpAddress.setter
    def IpAddress(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddress'], value)

    @property
    def IpAddressIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the lease address within the lease pool.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddressIncrement'])

    @IpAddressIncrement.setter
    def IpAddressIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddressIncrement'], value)

    @property
    def IpAddressPoolIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the starting lease address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddressPoolIncrement'])

    @IpAddressPoolIncrement.setter
    def IpAddressPoolIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddressPoolIncrement'], value)

    @property
    def IpAddressPrefix(self):
        """
        Returns
        -------
        - str: The prefix of the first lease pool.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddressPrefix'])

    @IpAddressPrefix.setter
    def IpAddressPrefix(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddressPrefix'], value)

    @property
    def IpAddressPrefixIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the prefix of the lease address within the lease pool.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddressPrefixIncrement'])

    @IpAddressPrefixIncrement.setter
    def IpAddressPrefixIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddressPrefixIncrement'], value)

    @property
    def IpAddressPrefixPoolIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the prefix of the starting lease.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpAddressPrefixPoolIncrement'])

    @IpAddressPrefixPoolIncrement.setter
    def IpAddressPrefixPoolIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpAddressPrefixPoolIncrement'], value)

    @property
    def IpDns1(self):
        """
        Returns
        -------
        - str: The first DNS address advertised in DHCP Offer and Reply messages.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpDns1'])

    @IpDns1.setter
    def IpDns1(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpDns1'], value)

    @property
    def IpDns2(self):
        """
        Returns
        -------
        - str: The second DNS address advertised in DHCP Offer and Reply messages.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpDns2'])

    @IpDns2.setter
    def IpDns2(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpDns2'], value)

    @property
    def IpGateway(self):
        """
        Returns
        -------
        - str: The Router address advertised in DHCP Offer and Reply messages.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpGateway'])

    @IpGateway.setter
    def IpGateway(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpGateway'], value)

    @property
    def IpGatewayIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the Router address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpGatewayIncrement'])

    @IpGatewayIncrement.setter
    def IpGatewayIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpGatewayIncrement'], value)

    @property
    def IpPrefix(self):
        """
        Returns
        -------
        - number: The Subnet Address length used to compute the subnetwork the advertised lease is part of.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpPrefix'])

    @IpPrefix.setter
    def IpPrefix(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpPrefix'], value)

    @property
    def IpType(self):
        """
        Returns
        -------
        - str: The type of IP addresses to be created by this range.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IpType'])

    @IpType.setter
    def IpType(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IpType'], value)

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of range
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])

    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def ObjectId(self):
        """
        Returns
        -------
        - str: Unique identifier for this object
        """
        return self._get_attribute(self._SDM_ATT_MAP['ObjectId'])

    @property
    def PrefixCount(self):
        """
        Returns
        -------
        - number: The number of leases to be allocated per each server prefix.
        """
        return self._get_attribute(self._SDM_ATT_MAP['PrefixCount'])

    @PrefixCount.setter
    def PrefixCount(self, value):
        self._set_attribute(self._SDM_ATT_MAP['PrefixCount'], value)

    @property
    def PrefixLength(self):
        """
        Returns
        -------
        - number: The Subnet Prefix length advertised in DHCP Offer and Reply messages.
        """
        return self._get_attribute(self._SDM_ATT_MAP['PrefixLength'])

    @PrefixLength.setter
    def PrefixLength(self, value):
        self._set_attribute(self._SDM_ATT_MAP['PrefixLength'], value)

    @property
    def ServerAddress(self):
        """
        Returns
        -------
        - str: The IP address of the first server interface.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerAddress'])

    @ServerAddress.setter
    def ServerAddress(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerAddress'], value)

    @property
    def ServerAddressIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the server address.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerAddressIncrement'])

    @ServerAddressIncrement.setter
    def ServerAddressIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerAddressIncrement'], value)

    @property
    def ServerCount(self):
        """
        Returns
        -------
        - number: The number of server addresses to create for this range.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerCount'])

    @ServerCount.setter
    def ServerCount(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerCount'], value)

    @property
    def ServerGateway(self):
        """
        Returns
        -------
        - str: The gateway address associated with DHCP server interfaces.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerGateway'])

    @ServerGateway.setter
    def ServerGateway(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerGateway'], value)

    @property
    def ServerGatewayIncrement(self):
        """
        Returns
        -------
        - str: The increment value for the gateway addresses.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerGatewayIncrement'])

    @ServerGatewayIncrement.setter
    def ServerGatewayIncrement(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerGatewayIncrement'], value)

    @property
    def ServerPrefix(self):
        """
        Returns
        -------
        - number: The subnet prefix length associated with server interfaces.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ServerPrefix'])

    @ServerPrefix.setter
    def ServerPrefix(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ServerPrefix'], value)

    @property
    def UseRapidCommit(self):
        """
        Returns
        -------
        - bool: Enables DHCP Server to negotiate leases with rapid commit for DHCP Clients that request it.
        """
        return self._get_attribute(self._SDM_ATT_MAP['UseRapidCommit'])

    @UseRapidCommit.setter
    def UseRapidCommit(self, value):
        self._set_attribute(self._SDM_ATT_MAP['UseRapidCommit'], value)

    def update(self, Count=None, Dhcp4EchoRelayInfo=None, Dhcp6IaType=None, Enabled=None, IpAddress=None, IpAddressIncrement=None, IpAddressPoolIncrement=None, IpAddressPrefix=None, IpAddressPrefixIncrement=None, IpAddressPrefixPoolIncrement=None, IpDns1=None, IpDns2=None, IpGateway=None, IpGatewayIncrement=None, IpPrefix=None, IpType=None, Name=None, PrefixCount=None, PrefixLength=None, ServerAddress=None, ServerAddressIncrement=None, ServerCount=None, ServerGateway=None, ServerGatewayIncrement=None, ServerPrefix=None, UseRapidCommit=None):
        """Updates dhcpServerRange resource on the server.

        Args
        ----
        - Count (number): The number of leases to be allocated per each server address.
        - Dhcp4EchoRelayInfo (bool): Enable echoing of DHCP option 82.
        - Dhcp6IaType (str): The Identity Association type supported by IPv6 address pools.
        - Enabled (bool): Disabled ranges won't be configured nor validated.
        - IpAddress (str): The IP address of the first lease pool.
        - IpAddressIncrement (str): The increment value for the lease address within the lease pool.
        - IpAddressPoolIncrement (str): The increment value for the starting lease address.
        - IpAddressPrefix (str): The prefix of the first lease pool.
        - IpAddressPrefixIncrement (str): The increment value for the prefix of the lease address within the lease pool.
        - IpAddressPrefixPoolIncrement (str): The increment value for the prefix of the starting lease.
        - IpDns1 (str): The first DNS address advertised in DHCP Offer and Reply messages.
        - IpDns2 (str): The second DNS address advertised in DHCP Offer and Reply messages.
        - IpGateway (str): The Router address advertised in DHCP Offer and Reply messages.
        - IpGatewayIncrement (str): The increment value for the Router address.
        - IpPrefix (number): The Subnet Address length used to compute the subnetwork the advertised lease is part of.
        - IpType (str): The type of IP addresses to be created by this range.
        - Name (str): Name of range
        - PrefixCount (number): The number of leases to be allocated per each server prefix.
        - PrefixLength (number): The Subnet Prefix length advertised in DHCP Offer and Reply messages.
        - ServerAddress (str): The IP address of the first server interface.
        - ServerAddressIncrement (str): The increment value for the server address.
        - ServerCount (number): The number of server addresses to create for this range.
        - ServerGateway (str): The gateway address associated with DHCP server interfaces.
        - ServerGatewayIncrement (str): The increment value for the gateway addresses.
        - ServerPrefix (number): The subnet prefix length associated with server interfaces.
        - UseRapidCommit (bool): Enables DHCP Server to negotiate leases with rapid commit for DHCP Clients that request it.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Count=None, Dhcp4EchoRelayInfo=None, Dhcp6IaType=None, Enabled=None, IpAddress=None, IpAddressIncrement=None, IpAddressPoolIncrement=None, IpAddressPrefix=None, IpAddressPrefixIncrement=None, IpAddressPrefixPoolIncrement=None, IpDns1=None, IpDns2=None, IpGateway=None, IpGatewayIncrement=None, IpPrefix=None, IpType=None, Name=None, ObjectId=None, PrefixCount=None, PrefixLength=None, ServerAddress=None, ServerAddressIncrement=None, ServerCount=None, ServerGateway=None, ServerGatewayIncrement=None, ServerPrefix=None, UseRapidCommit=None):
        """Finds and retrieves dhcpServerRange resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve dhcpServerRange resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all dhcpServerRange resources from the server.

        Args
        ----
        - Count (number): The number of leases to be allocated per each server address.
        - Dhcp4EchoRelayInfo (bool): Enable echoing of DHCP option 82.
        - Dhcp6IaType (str): The Identity Association type supported by IPv6 address pools.
        - Enabled (bool): Disabled ranges won't be configured nor validated.
        - IpAddress (str): The IP address of the first lease pool.
        - IpAddressIncrement (str): The increment value for the lease address within the lease pool.
        - IpAddressPoolIncrement (str): The increment value for the starting lease address.
        - IpAddressPrefix (str): The prefix of the first lease pool.
        - IpAddressPrefixIncrement (str): The increment value for the prefix of the lease address within the lease pool.
        - IpAddressPrefixPoolIncrement (str): The increment value for the prefix of the starting lease.
        - IpDns1 (str): The first DNS address advertised in DHCP Offer and Reply messages.
        - IpDns2 (str): The second DNS address advertised in DHCP Offer and Reply messages.
        - IpGateway (str): The Router address advertised in DHCP Offer and Reply messages.
        - IpGatewayIncrement (str): The increment value for the Router address.
        - IpPrefix (number): The Subnet Address length used to compute the subnetwork the advertised lease is part of.
        - IpType (str): The type of IP addresses to be created by this range.
        - Name (str): Name of range
        - ObjectId (str): Unique identifier for this object
        - PrefixCount (number): The number of leases to be allocated per each server prefix.
        - PrefixLength (number): The Subnet Prefix length advertised in DHCP Offer and Reply messages.
        - ServerAddress (str): The IP address of the first server interface.
        - ServerAddressIncrement (str): The increment value for the server address.
        - ServerCount (number): The number of server addresses to create for this range.
        - ServerGateway (str): The gateway address associated with DHCP server interfaces.
        - ServerGatewayIncrement (str): The increment value for the gateway addresses.
        - ServerPrefix (number): The subnet prefix length associated with server interfaces.
        - UseRapidCommit (bool): Enables DHCP Server to negotiate leases with rapid commit for DHCP Clients that request it.

        Returns
        -------
        - self: This instance with matching dhcpServerRange resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of dhcpServerRange data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the dhcpServerRange resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def CustomProtocolStack(self, *args, **kwargs):
        """Executes the customProtocolStack operation on the server.

        Create custom protocol stack under /vport/protocolStack

        customProtocolStack(Arg2=list, Arg3=enum, async_operation=bool)
        ---------------------------------------------------------------
        - Arg2 (list(str)): List of plugin types to be added in the new custom stack
        - Arg3 (str(kAppend | kMerge | kOverwrite)): Append, merge or overwrite existing protocol stack
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = {'Arg1': self}
        for i in range(len(args)):
            payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items():
            payload[item[0]] = item[1]
        return self._execute('customProtocolStack', payload=payload, response_object=None)

    def DisableProtocolStack(self, *args, **kwargs):
        """Executes the disableProtocolStack operation on the server.

        Disable a protocol under protocolStack using the class name

        disableProtocolStack(Arg2=string, async_operation=bool)string
        -------------------------------------------------------------
        - Arg2 (str): Protocol class name to disable
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.
        - Returns str: Status of the exec

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = {'Arg1': self.href}
        for i in range(len(args)):
            payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items():
            payload[item[0]] = item[1]
        return self._execute('disableProtocolStack', payload=payload, response_object=None)

    def EnableProtocolStack(self, *args, **kwargs):
        """Executes the enableProtocolStack operation on the server.

        Enable a protocol under protocolStack using the class name

        enableProtocolStack(Arg2=string, async_operation=bool)string
        ------------------------------------------------------------
        - Arg2 (str): Protocol class name to enable
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.
        - Returns str: Status of the exec

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = {'Arg1': self.href}
        for i in range(len(args)):
            payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items():
            payload[item[0]] = item[1]
        return self._execute('enableProtocolStack', payload=payload, response_object=None)