from enum import IntEnum
from .enums import Transmit, Application
from .version import AppVersion
from . import pdu_enums as pdu

class ITException(Exception):
    """ Common InterTechElectric exceptions class """
    error: Transmit | Application = Transmit.UNKNOWN

class AssociationResultError(ITException):
    """ Result of the proposed AA establishment and eventually the reason of the rejection of the association establishment request, as it is specified in ISO/IEC 8650-1.
        When no diagnostics are included, a null value is assigned to the result-source-diagnostics field. IEC62056-53 2004 7.3.3 The AARQ and AARE APDUs """
    error = Transmit.NO_ACCESS
    __match_args_ = ('result_source_diagnostics',)

    def __init__(self, result_source_diagnostics: IntEnum):
        Exception.__init__(self, f'Connection is {result_source_diagnostics.name}')
        self.result_source_diagnostics = result_source_diagnostics

class Timeout(ITException):
    """ timeout during connection or exchange """
    error = Transmit.TIMEOUT

class NoPort(ITException):
    """ not found port """
    error = Transmit.NO_PORT

class Abort(ITException):
    """ manual interrupt """
    error = Transmit.ABORT

class ITEConnection(ITException):
    """"""
    error = Transmit.UNKNOWN

class NoTransport(ITEConnection):
    """"""
    error = Transmit.NO_TRANSPORT

class ITEApplication(ITException):
    """"""

class NoObject(ITEApplication):
    """ object missing in collection """
    error = Application.MISSING_OBJ

class IDError(ITEApplication):
    """"""
    error = Application.ID_ERROR

class EmptyObj(ITEApplication):
    """ emtpy field in DLMS object """
    error = Application.EMPTY_OBJ

class NoConfig(ITEApplication):
    """ configuration for device not founded """
    error = Application.NO_CONFIG

class TypeErr(ITEApplication):
    """ unknown device type """
    error = Application.TYPE_ERROR

class VersionError(ITEApplication):
    """ Version error """
    error = Application.VERSION_ERROR

    def __init__(self, error_version: AppVersion, additional: str='device'):
        Exception.__init__(self, f'Unsupported {additional} version: {error_version}')
        self.version = error_version

class ResultError(ITEApplication):
    """ DLMS COSEMpdu_GB83.asn error """
    error = Application.RESULT_ERROR

    def __init__(self, error: pdu.DataAccessResult | pdu.ActionResult, additional: str=''):
        Exception.__init__(self, f'{error.__class__.__name__}: {error.name} {additional}')
        self.result = error

class UnknownError(ITException):
    """ for unknown errors """
    error = Transmit.UNKNOWN
if __name__ == '__main__':
    from gurux_dlms.enums import AssociationResult, SourceDiagnostic
    a = ResultError(pdu.ActionResult.NO_LONG_ACTION_IN_PROGRESS)
    print(a.__dict__)
    match a:
        case AssociationResultError():
            print('ok')
        case _:
            print('nok')