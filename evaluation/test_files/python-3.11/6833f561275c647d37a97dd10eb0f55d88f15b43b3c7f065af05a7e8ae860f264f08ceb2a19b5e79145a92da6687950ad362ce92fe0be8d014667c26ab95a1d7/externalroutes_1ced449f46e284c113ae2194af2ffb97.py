import sys
from uhd_restpy.base import Base
from uhd_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class ExternalRoutes(Base):
    """External routes with external metric
    The ExternalRoutes class encapsulates a list of externalRoutes resources that are managed by the system.
    A list of resources can be retrieved from the server using the ExternalRoutes.find() method.
    """
    __slots__ = ()
    _SDM_NAME = 'externalRoutes'
    _SDM_ATT_MAP = {'Active': 'active', 'Algorithm': 'algorithm', 'ConfigureSIDIndexLabel': 'configureSIDIndexLabel', 'Count': 'count', 'DescriptiveName': 'descriptiveName', 'EBit': 'eBit', 'EFlag': 'eFlag', 'ExternalRouteTag': 'externalRouteTag', 'FBit': 'fBit', 'ForwardingAddress': 'forwardingAddress', 'LABit': 'lABit', 'LFlag': 'lFlag', 'LinkStateId': 'linkStateId', 'LinkStateIdStep': 'linkStateIdStep', 'MCBit': 'mCBit', 'MFlag': 'mFlag', 'Metric': 'metric', 'NUBit': 'nUBit', 'Name': 'name', 'NetworkAddress': 'networkAddress', 'NpFlag': 'npFlag', 'PBit': 'pBit', 'Prefix': 'prefix', 'RangeSize': 'rangeSize', 'RefLSType': 'refLSType', 'ReferencedLinkStateId': 'referencedLinkStateId', 'SidIndexLabel': 'sidIndexLabel', 'TBit': 'tBit', 'UnusedBit4': 'unusedBit4', 'UnusedBit5': 'unusedBit5', 'UnusedBit6': 'unusedBit6', 'UnusedBit7': 'unusedBit7', 'VFlag': 'vFlag'}
    _SDM_ENUM_MAP = {}

    def __init__(self, parent, list_op=False):
        super(ExternalRoutes, self).__init__(parent, list_op)

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Whether this is to be advertised or not
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Active']))

    @property
    def Algorithm(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Algorithm
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Algorithm']))

    @property
    def ConfigureSIDIndexLabel(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Lets the corresponding router send Prefix SID. By default, it is selected
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ConfigureSIDIndexLabel']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offer more context.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def EBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): External Metric Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EBit']))

    @property
    def EFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): E Flag: Explicit-Null Flag: If set, any upstream neighbor of the Prefix-SID originator MUST replace the Prefix-SID with a Prefix-SID having an Explicit-NULL value (0 for IPv4 and 2 for IPv6) before forwarding the packet
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EFlag']))

    @property
    def ExternalRouteTag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): External Route Tag
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ExternalRouteTag']))

    @property
    def FBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Forwarding Address Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['FBit']))

    @property
    def ForwardingAddress(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): 128 Bits IPv6 address.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ForwardingAddress']))

    @property
    def LABit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-LA Bit(Local Address)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LABit']))

    @property
    def LFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): L-Flag: Local Flag. If set, then the value/index carried by the SID has local significance
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LFlag']))

    @property
    def LinkStateId(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Link State Id of the simulated IPv6 network
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LinkStateId']))

    @property
    def LinkStateIdStep(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Link State Id Step for the LSAs to be generated for this set of IPv6 Inter-Area networks.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LinkStateIdStep']))

    @property
    def MCBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-MC Bit(Multicast)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['MCBit']))

    @property
    def MFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): M-Flag: Mapping Server Flag: If set, the SID was advertised by a Segment Routing Mapping Server
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['MFlag']))

    @property
    def Metric(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Metric
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Metric']))

    @property
    def NUBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-NU Bit(No Unicast)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NUBit']))

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of NGPF element, guaranteed to be unique in Scenario
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])

    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def NetworkAddress(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Prefixes of the simulated IPv6 network
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NetworkAddress']))

    @property
    def NpFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): NP Flag: No-PHP Flag: If set, then the penultimate hop MUST NOT pop the Prefix-SID before delivering the packet to the node that advertised the Prefix-SID
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['NpFlag']))

    @property
    def PBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-P Bit(Propagate)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['PBit']))

    @property
    def Prefix(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Prefix Length
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Prefix']))

    @property
    def RangeSize(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Range Size
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['RangeSize']))

    @property
    def RefLSType(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Reference LS Type
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['RefLSType']))

    @property
    def ReferencedLinkStateId(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Referenced Link State Id
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['ReferencedLinkStateId']))

    @property
    def SidIndexLabel(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): SID/Index/Label value associated with the IGP Prefix segment attached to the specific IPv6 prefix
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['SidIndexLabel']))

    @property
    def TBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): External Route Tag Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['TBit']))

    @property
    def UnusedBit4(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(4)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit4']))

    @property
    def UnusedBit5(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(5)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit5']))

    @property
    def UnusedBit6(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(6)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit6']))

    @property
    def UnusedBit7(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Options-(7)Unused
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['UnusedBit7']))

    @property
    def VFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): V-Flag: Value flag. If set, then the SID carries an absolute value label value
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['VFlag']))

    def update(self, Name=None):
        """Updates externalRoutes resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, Name=None):
        """Adds a new externalRoutes resource on the json, only valid with batch add utility

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns
        -------
        - self: This instance with all currently retrieved externalRoutes resources using find and the newly added externalRoutes resources available through an iterator or index

        Raises
        ------
        - Exception: if this function is not being used with config assistance
        """
        return self._add_xpath(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Count=None, DescriptiveName=None, Name=None):
        """Finds and retrieves externalRoutes resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve externalRoutes resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all externalRoutes resources from the server.

        Args
        ----
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offer more context.
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns
        -------
        - self: This instance with matching externalRoutes resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of externalRoutes data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the externalRoutes resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def Abort(self, *args, **kwargs):
        """Executes the abort operation on the server.

        Abort CPF control plane (equals to demote to kUnconfigured state).

        abort(async_operation=bool)
        ---------------------------
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
        return self._execute('abort', payload=payload, response_object=None)

    def Advertise(self, *args, **kwargs):
        """Executes the advertise operation on the server.

        Advertise selected routes

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        advertise(async_operation=bool)
        -------------------------------
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.

        advertise(SessionIndices=list, async_operation=bool)
        ----------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 1 2 3
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.

        advertise(SessionIndices=string, async_operation=bool)
        ------------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12
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
        return self._execute('advertise', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Start CPF control plane (equals to promote to negotiated state).

        start(async_operation=bool)
        ---------------------------
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
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self, *args, **kwargs):
        """Executes the stop operation on the server.

        Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

        stop(async_operation=bool)
        --------------------------
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
        return self._execute('stop', payload=payload, response_object=None)

    def Withdraw(self, *args, **kwargs):
        """Executes the withdraw operation on the server.

        Withdraw selected routes

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        withdraw(async_operation=bool)
        ------------------------------
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.

        withdraw(SessionIndices=list, async_operation=bool)
        ---------------------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 1 2 3
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.

        withdraw(SessionIndices=string, async_operation=bool)
        -----------------------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12
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
        return self._execute('withdraw', payload=payload, response_object=None)

    def get_device_ids(self, PortNames=None, Active=None, Algorithm=None, ConfigureSIDIndexLabel=None, EBit=None, EFlag=None, ExternalRouteTag=None, FBit=None, ForwardingAddress=None, LABit=None, LFlag=None, LinkStateId=None, LinkStateIdStep=None, MCBit=None, MFlag=None, Metric=None, NUBit=None, NetworkAddress=None, NpFlag=None, PBit=None, Prefix=None, RangeSize=None, RefLSType=None, ReferencedLinkStateId=None, SidIndexLabel=None, TBit=None, UnusedBit4=None, UnusedBit5=None, UnusedBit6=None, UnusedBit7=None, VFlag=None):
        """Base class infrastructure that gets a list of externalRoutes device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - Algorithm (str): optional regex of algorithm
        - ConfigureSIDIndexLabel (str): optional regex of configureSIDIndexLabel
        - EBit (str): optional regex of eBit
        - EFlag (str): optional regex of eFlag
        - ExternalRouteTag (str): optional regex of externalRouteTag
        - FBit (str): optional regex of fBit
        - ForwardingAddress (str): optional regex of forwardingAddress
        - LABit (str): optional regex of lABit
        - LFlag (str): optional regex of lFlag
        - LinkStateId (str): optional regex of linkStateId
        - LinkStateIdStep (str): optional regex of linkStateIdStep
        - MCBit (str): optional regex of mCBit
        - MFlag (str): optional regex of mFlag
        - Metric (str): optional regex of metric
        - NUBit (str): optional regex of nUBit
        - NetworkAddress (str): optional regex of networkAddress
        - NpFlag (str): optional regex of npFlag
        - PBit (str): optional regex of pBit
        - Prefix (str): optional regex of prefix
        - RangeSize (str): optional regex of rangeSize
        - RefLSType (str): optional regex of refLSType
        - ReferencedLinkStateId (str): optional regex of referencedLinkStateId
        - SidIndexLabel (str): optional regex of sidIndexLabel
        - TBit (str): optional regex of tBit
        - UnusedBit4 (str): optional regex of unusedBit4
        - UnusedBit5 (str): optional regex of unusedBit5
        - UnusedBit6 (str): optional regex of unusedBit6
        - UnusedBit7 (str): optional regex of unusedBit7
        - VFlag (str): optional regex of vFlag

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())