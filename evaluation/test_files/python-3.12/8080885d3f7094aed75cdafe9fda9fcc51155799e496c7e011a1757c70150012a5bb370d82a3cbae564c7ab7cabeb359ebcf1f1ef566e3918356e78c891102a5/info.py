from xend_finance.models.schemas import Addresses
from xend_finance.strategies.contract import getContract
from xend_finance.strategies.abis.index import ESUSU_SERVICE, ESUSU_STORAGE
from xend_finance.utils.exceptions.handleErrors import BaseError

def esusu_info(esusu_id: int, provider: str, addresses: Addresses):
    try:
        contract = getContract(provider, ESUSU_SERVICE, addresses.ESUSU_SERVICE)
        data = contract.functions.GetEsusuCycle(esusu_id).call()
        return {'status': 'success', 'data': data}
    except BaseError as e:
        raise BaseError({'status': 'error', 'message': e})

def esusu_cycles_in_group(group_id: int, provider: str, addresses: Addresses):
    try:
        contract = getContract(provider, ESUSU_STORAGE, addresses.ESUSU_STORAGE)
        cycles_in_group_count = int(contract.functions.GetCycleIndexFromGroupId(group_id).call())
        cycles = []
        if cycles_in_group_count > 0:
            for cycle in range(cycles_in_group_count, 0, -1):
                id_of_esusu_by_position_in_group = contract.functions.GetCycleIdFromCycleIndexAndGroupId(group_id, cycle).call()
                data = esusu_info(id_of_esusu_by_position_in_group, provider, addresses)
                cycles.append(data)
        return {'status': 'success', 'data': cycles}
    except BaseError as e:
        raise BaseError({'status': 'error', 'message': e})