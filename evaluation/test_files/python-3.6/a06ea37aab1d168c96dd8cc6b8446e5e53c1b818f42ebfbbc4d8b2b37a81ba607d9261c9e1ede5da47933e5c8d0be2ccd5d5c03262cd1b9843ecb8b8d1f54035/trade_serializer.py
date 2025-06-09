from core.trade.InstrumentTrade import InstrumentTrade
from coreutility.string.string_utility import is_empty

def serialize_trade(trade: InstrumentTrade) -> dict:
    serialized = {'instrument_from': trade.instrument_from, 'instrument_to': trade.instrument_to, 'quantity': str(trade.quantity), 'status': trade.status.value, 'mode': trade.mode.value}
    if trade.price is not None:
        serialized['price'] = str(trade.price)
    if trade.value is not None:
        serialized['value'] = str(trade.value)
    if not is_empty(trade.description):
        serialized['description'] = trade.description
    if not is_empty(trade.order_id):
        serialized['order_id'] = trade.order_id
    if trade.instant is not None:
        serialized['instant'] = trade.instant
    return serialized