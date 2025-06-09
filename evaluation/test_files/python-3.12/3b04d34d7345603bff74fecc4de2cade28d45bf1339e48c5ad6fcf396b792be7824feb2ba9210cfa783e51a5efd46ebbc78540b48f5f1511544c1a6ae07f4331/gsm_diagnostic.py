from .__class_init__ import *

class Status(cdt.Enum):
    """ Indicates the registration status of the  modem. """
    ELEMENTS = {b'\x00': en.NOT_REGISTERED, b'\x01': en.REGISTERED_HOME_NETWORK, b'\x02': en.NOT_REGISTERED_BUT_MT, b'\x03': en.REGISTRATION_DENIED, b'\x04': en.UNKNOWN, b'\x05': en.REGISTERED_ROAMING}

class CSAttachment(cdt.Enum):
    """ Indicates the current circuit switched status."""
    ELEMENTS = {b'\x00': en.INACTIVE, b'\x01': en.INCOMING_CALL, b'\x02': en.ACTIVE}

class PSStatus(cdt.Enum):
    """ Indicates the packet switched status of the modem. """
    ELEMENTS = {b'\x00': en.INACTIVE, b'\x01': en.GPRS, b'\x02': en.EDGE, b'\x03': en.UMTS, b'\x04': en.HSDPA}

class SignalQuality(cdt.Unsigned):
    """for string report"""

    @property
    def report(self) -> str:
        value = int(self)
        if value == 0:
            return f'–113 dBm {en.OR_LESS}(0)'
        elif value == 1:
            return f'–111 dBm(1)'
        elif value < 31:
            return f'{-109 + (value - 2) * 2} dBm({value})'
        elif value == 31:
            return f'–51 dBm {en.OR_GREATER}(31)'
        elif value == 99:
            return f'{en.NOT_KNOWN_OR_NOT_DETECTABLE}'
        else:
            return f'wrong value={value!r}'

class CellInfoType(cdt.Structure):
    """ Params of element """
    values: tuple[cdt.LongUnsigned, cdt.LongUnsigned, SignalQuality, cdt.Unsigned]
    ELEMENTS = (cdt.StructElement(cdt.se.CELL_ID, cdt.LongUnsigned), cdt.StructElement(cdt.se.LOCATION_ID, cdt.LongUnsigned), cdt.StructElement(cdt.se.SIGNAL_QUALITY, SignalQuality), cdt.StructElement(cdt.se.BER, cdt.Unsigned))

    @property
    def cell_ID(self) -> cdt.LongUnsigned:
        """Two-byte cell ID in hexadecimal format"""
        return self.values[0]

    @property
    def location_ID(self) -> cdt.LongUnsigned:
        """Two-byte location area code (LAC) in hexadecimal format"""
        return self.values[1]

    @property
    def signal_quality(self) -> SignalQuality:
        """represents the signal quality"""
        return self.values[2]

    @property
    def ber(self) -> cdt.Unsigned:
        """Bit error (BER) measurement in percent:
        (0...7) as RXQUAL_n values specified in ETSI GSM 05.08 8.2.4
        (99) not known or not detectable."""
        return self.values[3]

class AdjacentCellInfo(cdt.Structure):
    values: tuple[cdt.LongUnsigned, cdt.Unsigned]
    ELEMENTS = (cdt.StructElement(cdt.se.CELL_ID, cdt.LongUnsigned), cdt.StructElement(cdt.se.SIGNAL_QUALITY, cdt.Unsigned))

    @property
    def cell_ID(self) -> cdt.LongUnsigned:
        """Two-byte cell ID in hexadecimal format"""
        return self.values[0]

    @property
    def signal_quality(self) -> cdt.Unsigned:
        """represents the signal quality:
            0: -113 dBm or less,
            1: -11q dBm,
            2..30: -109...53 dBm,
            31: -51 or greater,
            99 not known or not detectable"""
        return self.values[1]

class AdjacentCells(cdt.Array):
    TYPE = AdjacentCellInfo

class GSMDiagnostic(ic.COSEMInterfaceClasses):
    """ The GSM/GPRS network is undergoing constant changes in terms of registration status, signal quality etc. It is necessary to monitor and log the relevant parameters in order
     to obtain diagnostic information that allows identifying communication problems in the network. An instance of the 'GSM diagnostic' class stores parameters of the GSM/GPRS
     network necessary for analysing the operation of the network."""
    NAME = cn.GSM_DIAGNOSTIC
    CLASS_ID = ut.CosemClassId(class_id.GSM_DIAGNOSTIC)
    VERSION = cdt.Unsigned(0)
    A_ELEMENTS = (ic.ICAElement(an.OPERATOR, cdt.VisibleString), ic.ICAElement(an.STATUS, Status, 0, 255, 0), ic.ICAElement(an.CS_ATTACHMENT, CSAttachment, 0, 255, 0), ic.ICAElement(an.PS_STATUS, PSStatus, 0, 255, 0), ic.ICAElement(an.CELL_INFO, CellInfoType), ic.ICAElement(an.ADJACENT_CELL, AdjacentCells), ic.ICAElement(an.CAPTURE_TIME, cdt.DateTime))

    def characteristics_init(self):
        """nothing do it"""

    @property
    def operator(self) -> cdt.VisibleString:
        return self.get_attr(2)

    @property
    def status(self) -> Status:
        return self.get_attr(3)

    @property
    def cs_attachment(self) -> CSAttachment:
        return self.get_attr(4)

    @property
    def ps_status(self) -> PSStatus:
        return self.get_attr(5)

    @property
    def cell_info(self) -> CellInfoType:
        return self.get_attr(6)

    @property
    def adjacent_cell(self) -> AdjacentCells:
        return self.get_attr(7)

    @property
    def capture_time(self) -> cdt.DateTime:
        return self.get_attr(8)