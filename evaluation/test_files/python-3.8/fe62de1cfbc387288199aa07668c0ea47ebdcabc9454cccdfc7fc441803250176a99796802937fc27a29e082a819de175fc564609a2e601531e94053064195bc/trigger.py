import sys
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class Trigger(Base):
    """This object specifies the field properties.
    The Trigger class encapsulates a required trigger resource which will be retrieved from the server every time the property is accessed.
    """
    __slots__ = ()
    _SDM_NAME = 'trigger'
    _SDM_ATT_MAP = {'CaptureTriggerDA': 'captureTriggerDA', 'CaptureTriggerEnable': 'captureTriggerEnable', 'CaptureTriggerError': 'captureTriggerError', 'CaptureTriggerExpressionString': 'captureTriggerExpressionString', 'CaptureTriggerFrameSizeEnable': 'captureTriggerFrameSizeEnable', 'CaptureTriggerFrameSizeFrom': 'captureTriggerFrameSizeFrom', 'CaptureTriggerFrameSizeTo': 'captureTriggerFrameSizeTo', 'CaptureTriggerPattern': 'captureTriggerPattern', 'CaptureTriggerSA': 'captureTriggerSA'}
    _SDM_ENUM_MAP = {'captureTriggerDA': ['addr1', 'addr2', 'anyAddr', 'notAddr1', 'notAddr2'], 'captureTriggerError': ['errAnyFrame', 'errBadCRC', 'errGoodFrame', 'errBadFrame', 'errAnySequencekError', 'errBigSequenceError', 'errSmallSequenceError', 'errReverseSequenceError', 'errDataIntegrityError', 'errAnyIpTcpUdpChecksumError', 'errInvalidFcoeFrame'], 'captureTriggerPattern': ['anyPattern', 'notPattern1', 'notPattern2', 'pattern1', 'pattern1AndPattern2', 'pattern2'], 'captureTriggerSA': ['addr1', 'addr2', 'anyAddr', 'notAddr1', 'notAddr2']}

    def __init__(self, parent, list_op=False):
        super(Trigger, self).__init__(parent, list_op)

    @property
    def CaptureTriggerDA(self):
        """
        Returns
        -------
        - str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2): One of two available destination MAC addresses to filter on. Applicable only when captureTriggerEnable is set to true.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerDA'])

    @CaptureTriggerDA.setter
    def CaptureTriggerDA(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerDA'], value)

    @property
    def CaptureTriggerEnable(self):
        """
        Returns
        -------
        - bool: Enables or disables the capture trigger.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerEnable'])

    @CaptureTriggerEnable.setter
    def CaptureTriggerEnable(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerEnable'], value)

    @property
    def CaptureTriggerError(self):
        """
        Returns
        -------
        - str(errAnyFrame | errBadCRC | errGoodFrame | errBadFrame | errAnySequencekError | errBigSequenceError | errSmallSequenceError | errReverseSequenceError | errDataIntegrityError | errAnyIpTcpUdpChecksumError | errInvalidFcoeFrame): Applicable only when captureTriggerEnable is set to true.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerError'])

    @CaptureTriggerError.setter
    def CaptureTriggerError(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerError'], value)

    @property
    def CaptureTriggerExpressionString(self):
        """
        Returns
        -------
        - str: String composed of SA1, DA1, P1, P2, optionally negated with '!', and connected with operators 'and', 'or', 'xor', 'nand' or 'nor'. (Eg: {DA1 and SA1 or !P1 and P2} ). NOTE: The 'or', 'xor', 'nand' and 'nor' operators are available only on the following load modules: XMVDC, NGY, XMSP12, LAVA(MK), Xcellon AP, Xcellon NP.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerExpressionString'])

    @CaptureTriggerExpressionString.setter
    def CaptureTriggerExpressionString(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerExpressionString'], value)

    @property
    def CaptureTriggerFrameSizeEnable(self):
        """
        Returns
        -------
        - bool: Enables or disables the frame size constraint which specifies a range of frame.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeEnable'])

    @CaptureTriggerFrameSizeEnable.setter
    def CaptureTriggerFrameSizeEnable(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeEnable'], value)

    @property
    def CaptureTriggerFrameSizeFrom(self):
        """
        Returns
        -------
        - number: Applicable only when captureTriggerFrameSizeEnable is enabled. The minimum range of the size of frame to be triggered.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeFrom'])

    @CaptureTriggerFrameSizeFrom.setter
    def CaptureTriggerFrameSizeFrom(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeFrom'], value)

    @property
    def CaptureTriggerFrameSizeTo(self):
        """
        Returns
        -------
        - number: Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeTo'])

    @CaptureTriggerFrameSizeTo.setter
    def CaptureTriggerFrameSizeTo(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerFrameSizeTo'], value)

    @property
    def CaptureTriggerPattern(self):
        """
        Returns
        -------
        - str(anyPattern | notPattern1 | notPattern2 | pattern1 | pattern1AndPattern2 | pattern2): Applicable only when captureTriggerEnable is set to true.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerPattern'])

    @CaptureTriggerPattern.setter
    def CaptureTriggerPattern(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerPattern'], value)

    @property
    def CaptureTriggerSA(self):
        """
        Returns
        -------
        - str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2): Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CaptureTriggerSA'])

    @CaptureTriggerSA.setter
    def CaptureTriggerSA(self, value):
        self._set_attribute(self._SDM_ATT_MAP['CaptureTriggerSA'], value)

    def update(self, CaptureTriggerDA=None, CaptureTriggerEnable=None, CaptureTriggerError=None, CaptureTriggerExpressionString=None, CaptureTriggerFrameSizeEnable=None, CaptureTriggerFrameSizeFrom=None, CaptureTriggerFrameSizeTo=None, CaptureTriggerPattern=None, CaptureTriggerSA=None):
        """Updates trigger resource on the server.

        Args
        ----
        - CaptureTriggerDA (str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2)): One of two available destination MAC addresses to filter on. Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerEnable (bool): Enables or disables the capture trigger.
        - CaptureTriggerError (str(errAnyFrame | errBadCRC | errGoodFrame | errBadFrame | errAnySequencekError | errBigSequenceError | errSmallSequenceError | errReverseSequenceError | errDataIntegrityError | errAnyIpTcpUdpChecksumError | errInvalidFcoeFrame)): Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerExpressionString (str): String composed of SA1, DA1, P1, P2, optionally negated with '!', and connected with operators 'and', 'or', 'xor', 'nand' or 'nor'. (Eg: {DA1 and SA1 or !P1 and P2} ). NOTE: The 'or', 'xor', 'nand' and 'nor' operators are available only on the following load modules: XMVDC, NGY, XMSP12, LAVA(MK), Xcellon AP, Xcellon NP.
        - CaptureTriggerFrameSizeEnable (bool): Enables or disables the frame size constraint which specifies a range of frame.
        - CaptureTriggerFrameSizeFrom (number): Applicable only when captureTriggerFrameSizeEnable is enabled. The minimum range of the size of frame to be triggered.
        - CaptureTriggerFrameSizeTo (number): Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.
        - CaptureTriggerPattern (str(anyPattern | notPattern1 | notPattern2 | pattern1 | pattern1AndPattern2 | pattern2)): Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerSA (str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2)): Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, CaptureTriggerDA=None, CaptureTriggerEnable=None, CaptureTriggerError=None, CaptureTriggerExpressionString=None, CaptureTriggerFrameSizeEnable=None, CaptureTriggerFrameSizeFrom=None, CaptureTriggerFrameSizeTo=None, CaptureTriggerPattern=None, CaptureTriggerSA=None):
        """Finds and retrieves trigger resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve trigger resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all trigger resources from the server.

        Args
        ----
        - CaptureTriggerDA (str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2)): One of two available destination MAC addresses to filter on. Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerEnable (bool): Enables or disables the capture trigger.
        - CaptureTriggerError (str(errAnyFrame | errBadCRC | errGoodFrame | errBadFrame | errAnySequencekError | errBigSequenceError | errSmallSequenceError | errReverseSequenceError | errDataIntegrityError | errAnyIpTcpUdpChecksumError | errInvalidFcoeFrame)): Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerExpressionString (str): String composed of SA1, DA1, P1, P2, optionally negated with '!', and connected with operators 'and', 'or', 'xor', 'nand' or 'nor'. (Eg: {DA1 and SA1 or !P1 and P2} ). NOTE: The 'or', 'xor', 'nand' and 'nor' operators are available only on the following load modules: XMVDC, NGY, XMSP12, LAVA(MK), Xcellon AP, Xcellon NP.
        - CaptureTriggerFrameSizeEnable (bool): Enables or disables the frame size constraint which specifies a range of frame.
        - CaptureTriggerFrameSizeFrom (number): Applicable only when captureTriggerFrameSizeEnable is enabled. The minimum range of the size of frame to be triggered.
        - CaptureTriggerFrameSizeTo (number): Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.
        - CaptureTriggerPattern (str(anyPattern | notPattern1 | notPattern2 | pattern1 | pattern1AndPattern2 | pattern2)): Applicable only when captureTriggerEnable is set to true.
        - CaptureTriggerSA (str(addr1 | addr2 | anyAddr | notAddr1 | notAddr2)): Applicable only when captureTriggerFrameSizeEnable is enabled. The maximum range of the size of frame to be triggered.

        Returns
        -------
        - self: This instance with matching trigger resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of trigger data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the trigger resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)