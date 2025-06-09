from typing import Dict, Any, List
from algora.api.service.backtest.__util import _get_backtest_request_info, _get_backtests_request_info, _create_backtest_request_info, _update_backtest_request_info, _delete_backtest_request_info
from algora.api.service.backtest.enum import BacktestStatus
from algora.api.service.backtest.model import BacktestRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import __get_request, __put_request, __post_request, __delete_request

@data_request(transformer=no_transform)
def get_backtest(id: str) -> Dict[str, Any]:
    """
    Get backtest by ID.

    Args:
        id (str): Backtest ID

    Returns:
        Dict[str, Any]: Backtest response
    """
    request_info = _get_backtest_request_info(id)
    return __get_request(**request_info)

@data_request(transformer=no_transform)
def get_backtests() -> List[Dict[str, Any]]:
    """
    Get all backtests.

    Returns:
        List[Dict[str, Any]]: List of backtest response
    """
    request_info = _get_backtests_request_info()
    return __get_request(**request_info)

@data_request(transformer=no_transform)
def create_backtest(request: BacktestRequest) -> Dict[str, Any]:
    """
    Create backtest.

    Args:
        request (BacktestRequest): Backtest request

    Returns:
        Dict[str, Any]: Backtest response
    """
    request_info = _create_backtest_request_info(request)
    return __put_request(**request_info)

@data_request(transformer=no_transform)
def update_backtest(id: str, status: BacktestStatus) -> Dict[str, Any]:
    """
    Update backtest.

    Args:
        id (str): Backtest ID
        status (BacktestRequest): Backtest request

    Returns:
        Dict[str, Any]: Backtest response
    """
    request_info = _update_backtest_request_info(id, status)
    return __post_request(**request_info)

@data_request(transformer=no_transform)
def delete_backtest(id: str) -> None:
    """
    Delete backtest by ID.

    Args:
        id (str): Backtest ID

    Returns:
        None
    """
    request_info = _delete_backtest_request_info(id)
    return __delete_request(**request_info)