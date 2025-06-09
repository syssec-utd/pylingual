import logging
from ctypes import cdll, CDLL
from .exc import PSPBoardNotMatch, PSPBusyInUses, PSPDriverNotLoad, PSPError, PSPInvalid, PSPNotExist, PSPNotOpened, PSPNotSupport
from .lmbinc import ERR_BoardNotMatch, ERR_BusyInUses, ERR_DriverNotLoad, ERR_Error, ERR_IPMI_IDLESTATE, ERR_IPMI_WRITESTATE, ERR_IPMI_READSTATE, ERR_IPMI_IBF0, ERR_IPMI_OBF1, ERR_Invalid, ERR_NotExist, ERR_NotOpened, ERR_NotSupport, ERR_Success
from .utils import is_root
logger = logging.getLogger(__name__)
DEFAULT_LMB_IO_PATH = '/opt/lanner/psp/bin/amd64/lib/liblmbio.so'
DEFAULT_LMB_API_PATH = '/opt/lanner/psp/bin/amd64/lib/liblmbapi.so'

class PSP:
    """
    Lanner Platform Support Package (PSP).

    :raises PermissionError: if not running as root user
    """
    lmb_io_path = DEFAULT_LMB_IO_PATH
    lmb_api_path = DEFAULT_LMB_API_PATH

    def __init__(self) -> None:
        if not is_root():
            raise PermissionError('Please uses root user !!!')
        self._liblmbio = cdll.LoadLibrary(self.lmb_io_path)
        self._liblmbapi = cdll.LoadLibrary(self.lmb_api_path)

    def __enter__(self) -> 'PSP':
        """
        Initialize the Lanner common API and board libraries.

        :returns: the :class:`PSP` instance
        :rtype: PSP
        :raises PSPNotExist: Board library is not found.
        :raises PSPBoardNotMatch: Library and M/B do not match.
        :raises PSPError: Initializing library failed.
        """
        i_ret = self._liblmbapi.LMB_DLL_Init()
        msg = get_psp_exc_msg('LMB_DLL_Init', i_ret)
        if i_ret == ERR_Success:
            return self
        msg += ' please confirm the API libraries is matched this platform or the lmbiodrv driver was loaded'
        if i_ret == ERR_NotExist:
            raise PSPNotExist(msg)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_BusyInUses:
            raise PSPBusyInUses(msg)
        elif i_ret == ERR_BoardNotMatch:
            raise PSPBoardNotMatch(msg)
        elif i_ret == ERR_DriverNotLoad:
            raise PSPDriverNotLoad(msg)
        else:
            raise PSPError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Release the Lanner common API library.

        .. note::

            This function will auto-release board-level library.

        :raises PSPBusyInUses: Libray is busy or a certain process is in use.
        :raises PSPError: For generic PSP error.
        """
        i_ret = self._liblmbapi.LMB_DLL_DeInit()
        msg = get_psp_exc_msg('LMB_DLL_DeInit', i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_BusyInUses:
            raise PSPBusyInUses(msg)
        else:
            raise PSPError(msg)
        return False

    @property
    def lib(self) -> CDLL:
        """
        Get the DLL/SO to call C functions directly.

        Example:

        .. code-block:: pycon

            >>> with PSP() as psp:  # Automatically Init() and DeInit().
            ...     psp.lib.LMB_SLED_SetLteStateLED(0)
            ...
            0
        """
        return self._liblmbapi

def get_psp_exc_msg(func_name: str, ret_code: int) -> str:
    """
    Get the message of the execution result of the PSP function
    by ``func_name`` and ``ret_code``.

    :param str func_name: the name of the C function where the error occurred
    :param int ret_code: error code returned by the C function
    :return: error message details
    :rtype: str
    """
    msg = f'{func_name} return code ( 0x{ret_code & 4294967295:08x} --> '
    if ret_code == ERR_Success:
        msg += 'OK )'
    elif ret_code == ERR_Error:
        msg += 'general error )'
    elif ret_code == ERR_NotExist:
        msg += 'device or file not exist )'
    elif ret_code == ERR_NotOpened:
        msg += 'library not opened yet )'
    elif ret_code == ERR_Invalid:
        msg += 'parameter out of range or invalid )'
    elif ret_code == ERR_NotSupport:
        msg += 'hardware or function not support )'
    elif ret_code == ERR_BusyInUses:
        msg += 'device is busy now )'
    elif ret_code == ERR_BoardNotMatch:
        msg += 'board BIOSID and library not matched )'
    elif ret_code == ERR_DriverNotLoad:
        msg += 'the lmbiodrv driver or i2c-dev driver not loading )'
    elif ret_code == ERR_IPMI_IDLESTATE:
        msg += 'IPMI idle state error )'
    elif ret_code == ERR_IPMI_WRITESTATE:
        msg += 'IPMI write state error )'
    elif ret_code == ERR_IPMI_READSTATE:
        msg += 'IPMI read state error )'
    elif ret_code == ERR_IPMI_IBF0:
        msg += 'IPMI input wait error )'
    elif ret_code == ERR_IPMI_OBF1:
        msg += 'IPMI output wait error )'
    else:
        msg += 'unknown error )'
    return msg