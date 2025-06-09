import json
from typing import Any, Dict, Optional, Type, Union
from petisco.base.domain.message.message import Message

class Command(Message):
    """
    A base class to model your Command.
    An operation that effects some change to the system (for example, modify the persistence).
    An operation that intentionally creates a side effect.
    """

    def __init__(self, **data: Any) -> None:
        self._set_data()
        self._set_attributes(**data)
        self.type = 'command'

    @staticmethod
    def from_dict(message_data: Dict[str, Any], target_type: Optional[Type['Command']]=None) -> 'Command':
        target_type = Command if target_type is None else target_type
        data = message_data.get('data')
        command = target_type()
        command._set_data(**data)
        return command

    @staticmethod
    def from_json(message_json: Union[str, bytes], target_type: Optional[Type['Command']]=None) -> 'Command':
        event_dict = json.loads(message_json)
        return Command.from_dict(event_dict, target_type)

    def __repr__(self) -> str:
        return self.to_str(class_name='Command', type='domain_event')