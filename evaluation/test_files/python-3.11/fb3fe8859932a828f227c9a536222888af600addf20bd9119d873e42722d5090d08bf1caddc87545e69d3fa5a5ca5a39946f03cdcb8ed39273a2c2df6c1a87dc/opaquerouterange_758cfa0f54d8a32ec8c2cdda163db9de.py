import sys
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class OpaqueRouteRange(Base):
    """Applies the route range information on the opaque route block.
    The OpaqueRouteRange class encapsulates a list of opaqueRouteRange resources that are managed by the user.
    A list of resources can be retrieved from the server using the OpaqueRouteRange.find() method.
    The list can be managed by using the OpaqueRouteRange.add() and OpaqueRouteRange.remove() methods.
    """
    __slots__ = ()
    _SDM_NAME = 'opaqueRouteRange'
    _SDM_ATT_MAP = {'Id__': '__id__', 'Enabled': 'enabled', 'ImportedFile': 'importedFile', 'NextHopAsIs': 'nextHopAsIs', 'NumberOfRoutes': 'numberOfRoutes', 'SendMultiExitDiscovery': 'sendMultiExitDiscovery', 'Status': 'status'}
    _SDM_ENUM_MAP = {}

    def __init__(self, parent, list_op=False):
        super(OpaqueRouteRange, self).__init__(parent, list_op)

    @property
    def Id__(self):
        """
        Returns
        -------
        - str: NOT DEFINED
        """
        return self._get_attribute(self._SDM_ATT_MAP['Id__'])

    @Id__.setter
    def Id__(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Id__'], value)

    @property
    def Enabled(self):
        """
        Returns
        -------
        - bool: Appends the local AsNumber.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Enabled'])

    @Enabled.setter
    def Enabled(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Enabled'], value)

    @property
    def ImportedFile(self):
        """
        Returns
        -------
        - str: Location of the route import file.
        """
        return self._get_attribute(self._SDM_ATT_MAP['ImportedFile'])

    @ImportedFile.setter
    def ImportedFile(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ImportedFile'], value)

    @property
    def NextHopAsIs(self):
        """
        Returns
        -------
        - bool: If true, it takes the next Hop AsIs.
        """
        return self._get_attribute(self._SDM_ATT_MAP['NextHopAsIs'])

    @NextHopAsIs.setter
    def NextHopAsIs(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NextHopAsIs'], value)

    @property
    def NumberOfRoutes(self):
        """
        Returns
        -------
        - number: Total number of opaque routes.
        """
        return self._get_attribute(self._SDM_ATT_MAP['NumberOfRoutes'])

    @NumberOfRoutes.setter
    def NumberOfRoutes(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NumberOfRoutes'], value)

    @property
    def SendMultiExitDiscovery(self):
        """
        Returns
        -------
        - bool: If true, sends a Multi Exit Discriminator attribute with the indicated value.
        """
        return self._get_attribute(self._SDM_ATT_MAP['SendMultiExitDiscovery'])

    @SendMultiExitDiscovery.setter
    def SendMultiExitDiscovery(self, value):
        self._set_attribute(self._SDM_ATT_MAP['SendMultiExitDiscovery'], value)

    @property
    def Status(self):
        """
        Returns
        -------
        - str: Indicates the status of the imported file.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Status'])

    def update(self, Id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None):
        """Updates opaqueRouteRange resource on the server.

        Args
        ----
        - Id__ (str): NOT DEFINED
        - Enabled (bool): Appends the local AsNumber.
        - ImportedFile (str): Location of the route import file.
        - NextHopAsIs (bool): If true, it takes the next Hop AsIs.
        - NumberOfRoutes (number): Total number of opaque routes.
        - SendMultiExitDiscovery (bool): If true, sends a Multi Exit Discriminator attribute with the indicated value.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, Id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None):
        """Adds a new opaqueRouteRange resource on the server and adds it to the container.

        Args
        ----
        - Id__ (str): NOT DEFINED
        - Enabled (bool): Appends the local AsNumber.
        - ImportedFile (str): Location of the route import file.
        - NextHopAsIs (bool): If true, it takes the next Hop AsIs.
        - NumberOfRoutes (number): Total number of opaque routes.
        - SendMultiExitDiscovery (bool): If true, sends a Multi Exit Discriminator attribute with the indicated value.

        Returns
        -------
        - self: This instance with all currently retrieved opaqueRouteRange resources using find and the newly added opaqueRouteRange resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained opaqueRouteRange resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None, Status=None):
        """Finds and retrieves opaqueRouteRange resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve opaqueRouteRange resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all opaqueRouteRange resources from the server.

        Args
        ----
        - Id__ (str): NOT DEFINED
        - Enabled (bool): Appends the local AsNumber.
        - ImportedFile (str): Location of the route import file.
        - NextHopAsIs (bool): If true, it takes the next Hop AsIs.
        - NumberOfRoutes (number): Total number of opaque routes.
        - SendMultiExitDiscovery (bool): If true, sends a Multi Exit Discriminator attribute with the indicated value.
        - Status (str): Indicates the status of the imported file.

        Returns
        -------
        - self: This instance with matching opaqueRouteRange resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of opaqueRouteRange data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the opaqueRouteRange resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def ApplyOpaqueRouteRange(self, *args, **kwargs):
        """Executes the applyOpaqueRouteRange operation on the server.

        This function allows to Apply the route range information on the opaque route block.

        applyOpaqueRouteRange(async_operation=bool)string
        -------------------------------------------------
        - async_operation (bool=False): True to execute the operation asynchronously. Any subsequent rest api calls made through the Connection class will block until the operation is complete.
        - Returns str: NOT DEFINED

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
        return self._execute('applyOpaqueRouteRange', payload=payload, response_object=None)