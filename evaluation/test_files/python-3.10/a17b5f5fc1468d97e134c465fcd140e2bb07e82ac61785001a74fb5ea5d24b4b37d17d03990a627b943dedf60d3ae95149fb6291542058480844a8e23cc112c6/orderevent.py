"""Declares :class:`OrderEvent`."""
import pydantic
from .event import Event
from .orderstatustype import OrderStatusType

class OrderEvent(Event):
    status: OrderStatusType = pydantic.Field(default=..., title='Status', description='The status of the order resulting from the event.')

    class Config:
        title: str = 'WooCommerceOrderEvent'