import sys
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class LldpTlvOui(Base):
    """LLDP Organizationally Specific TLV.
    The LldpTlvOui class encapsulates a required lldpTlvOui resource which will be retrieved from the server every time the property is accessed.
    """
    __slots__ = ()
    _SDM_NAME = 'lldpTlvOui'
    _SDM_ATT_MAP = {'Info': 'info', 'ObjectId': 'objectId', 'Oui': 'oui', 'Subtype': 'subtype'}
    _SDM_ENUM_MAP = {}

    def __init__(self, parent, list_op=False):
        super(LldpTlvOui, self).__init__(parent, list_op)

    @property
    def Info(self):
        """
        Returns
        -------
        - str: Information String.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Info'])

    @Info.setter
    def Info(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Info'], value)

    @property
    def ObjectId(self):
        """
        Returns
        -------
        - str: Unique identifier for this object
        """
        return self._get_attribute(self._SDM_ATT_MAP['ObjectId'])

    @property
    def Oui(self):
        """
        Returns
        -------
        - str: OUI.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Oui'])

    @Oui.setter
    def Oui(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Oui'], value)

    @property
    def Subtype(self):
        """
        Returns
        -------
        - number: OUI Subtype
        """
        return self._get_attribute(self._SDM_ATT_MAP['Subtype'])

    @Subtype.setter
    def Subtype(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Subtype'], value)

    def update(self, Info=None, Oui=None, Subtype=None):
        """Updates lldpTlvOui resource on the server.

        Args
        ----
        - Info (str): Information String.
        - Oui (str): OUI.
        - Subtype (number): OUI Subtype

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Info=None, ObjectId=None, Oui=None, Subtype=None):
        """Finds and retrieves lldpTlvOui resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve lldpTlvOui resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all lldpTlvOui resources from the server.

        Args
        ----
        - Info (str): Information String.
        - ObjectId (str): Unique identifier for this object
        - Oui (str): OUI.
        - Subtype (number): OUI Subtype

        Returns
        -------
        - self: This instance with matching lldpTlvOui resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of lldpTlvOui data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the lldpTlvOui resources from the server available through an iterator or index

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