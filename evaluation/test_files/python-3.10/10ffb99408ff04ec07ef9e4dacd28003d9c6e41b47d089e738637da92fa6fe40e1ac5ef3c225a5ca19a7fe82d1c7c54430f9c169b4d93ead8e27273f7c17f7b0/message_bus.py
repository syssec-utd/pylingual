import copy
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.types_message import TypeMessage

class MessageBus(ABC, Generic[TypeMessage]):

    @classmethod
    def __repr__(cls) -> str:
        return cls.__name__

    @classmethod
    def info(cls) -> Dict[str, str]:
        return {'name': cls.__name__}

    def _set_additional_meta(self, meta: Dict[str, Any]) -> None:
        self.additional_meta = meta

    def with_meta(self, meta: Dict[str, Any]) -> 'MessageBus[TypeMessage]':
        if not isinstance(meta, Dict):
            raise TypeError('MessageBus.with_meta() expect a dict')
        event_bus = copy.copy(self)
        event_bus._set_additional_meta(meta)
        return event_bus

    def get_configured_meta(self) -> Dict[str, Any]:
        configured_meta: Dict[str, Any] = {}
        if hasattr(self, 'additional_meta'):
            configured_meta = {**configured_meta, **self.additional_meta}
        return configured_meta

    @abstractmethod
    def publish(self, message: TypeMessage) -> None:
        raise NotImplementedError

    @abstractmethod
    def retry_publish_only_on_store_queue(self, message: TypeMessage) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def _check_is_message(self, message: TypeMessage) -> None:
        if not message or not issubclass(message.__class__, Message):
            raise TypeError('MessageBus only publishes Message objects')

    def publish_list(self, messages: List[TypeMessage]) -> None:
        for message in messages:
            self.publish(message)

    def retry_publish_list_only_on_store_queue(self, messages: List[TypeMessage]) -> None:
        for message in messages:
            self.retry_publish_only_on_store_queue(message)