from typing import Any, Dict, List, Type, TypeVar, Union
import attr
from ..types import UNSET, Unset
T = TypeVar('T', bound='NextStageDialogJsonBody')

@attr.s(auto_attribs=True)
class NextStageDialogJsonBody:
    """
    Attributes:
        state (Union[Unset, str]): String representation of the zero-based index of the stage to go to. Example: 3.
    """
    state: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        state = self.state
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict['state'] = state
        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        state = d.pop('state', UNSET)
        next_stage_dialog_json_body = cls(state=state)
        next_stage_dialog_json_body.additional_properties = d
        return next_stage_dialog_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties