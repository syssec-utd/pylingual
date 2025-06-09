from typing import List, Union, Callable, Any
from chipscopy.tcf.services import DoneHWCommand, Service
from chipscopy.client.core_property_client import PropertyValues
from chipscopy.proxies.CorePropertyProxy import CorePropertyProxy
MEMORY_MODEL_DDRMC = 'memory_model_ddrmc'
MEMORY_MODEL_MILA_DDR = 'memory_model_mila_ddr'
DDRMC_MAIN = 'ddrmc_main'
DDRMC_NOC = 'ddrmc_noc'
DDRMC_UB = 'ddrmc_ub'
DDRMC_CRYPTO = 'ddrmc_crypto'
DDRMC_MAIN_INDEX = 0
DDRMC_NOC_INDEX = 1
DDRMC_UB_INDEX = 2
DDRMC_CRYPTO_INDEX = 3
DDRMC_DOMAIN_COUNT = 4
NAME = 'DDRMC'

class DDRMCService(Service):
    """TCF DDRMC Service interface."""

    def getName(self) -> str:
        """
        Get service name of this service.

        :returns: Service name :const:`NAME`.
        """
        return NAME

class DDRMCProxy(CorePropertyProxy, DDRMCService):

    def __init__(self, channel):
        super().__init__(channel)
        self._listeners = {}

    def initialize(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('initialize', (node_id,), done)

    def terminate(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('terminate', (node_id,), done)

    def write32(self, node_id: str, write_addr: int, data: int, domain_index: int, done: DoneHWCommand) -> None:
        """
        Write 32 bit register.

        :param node_id: Core context id.
        :param write_addr: Address.
        :param data: 32 bit data
        :param domain_index: 0 for DDRMC_MAIN, 1 for DDRMC_NOC
        """
        return self.send_command('write32', (node_id, write_addr, data, domain_index), done)

    def read32(self, node_id: str, read_addr: int, read_word_count: int, domain_index: int, done: DoneHWCommand) -> Union[List[int], int]:
        """
        Read 32 bit register

        :param node_id: Core context id.
        :param read_addr: address to read from.
        :param read_word_count: number of 32 bit words.
        :param domain_index: 0 for DDRMC_MAIN, 1 for DDRMC_NOC
        :return int value if read_word_count == 1. Otherwise list of int values.
        """
        return self.send_command('read32', (node_id, read_addr, read_word_count, domain_index), done)

    def refresh_property(self, node_id: str, prop_names: List[str], done: DoneHWCommand) -> PropertyValues:
        return self.send_command('refreshProperty', (node_id, prop_names), done)

    def refresh_cal_status(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('refreshCalStatus', (node_id,), done)

    def refresh_cal_margin(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('refreshCalMargin', (node_id,), done)

    def refresh_health_status(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('refreshHealthStatus', (node_id,), done)

    def refresh_dqs_status(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('refreshDQSStatus', (node_id,), done)

    def disable_tracking(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('disableTracking', (node_id,), done)

    def enable_tracking(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('enableTracking', (node_id,), done)

    def get_cal_status(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('getCalStatus', (node_id,), done)

    def get_cal_margin_mode(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('getCalMarginMode', (node_id,), done)

    def get_margin_ps_factors(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('getMarginPsFactors', (node_id,), done)

    def is_clock_gated(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('isClockGated', (node_id,), done)

    def run_eye_scan(self, node_id: str, done: DoneHWCommand, progress: Callable[[Any, str or Exception, Any], None]=None) -> bool:
        return self.send_xicom_command('runEyeScan', (node_id,), done, progress)

    def get_eye_scan_data(self, node_id: str, done: DoneHWCommand) -> None:
        return self.send_command('getEyeScanData', (node_id,), done)