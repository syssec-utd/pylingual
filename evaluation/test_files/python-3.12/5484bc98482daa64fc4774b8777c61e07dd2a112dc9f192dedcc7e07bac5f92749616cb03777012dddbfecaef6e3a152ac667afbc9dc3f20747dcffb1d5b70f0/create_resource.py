from typing import Any, Dict, List, Type, TypeVar, Union
import attr
from ..models.create_resource_value import CreateResourceValue
from ..types import UNSET, Unset
T = TypeVar('T', bound='CreateResource')

@attr.s(auto_attribs=True)
class CreateResource:
    """ """
    path: str
    value: CreateResourceValue
    resource_type: str
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value.to_dict()
        resource_type = self.resource_type
        description = self.description
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({'path': path, 'value': value, 'resource_type': resource_type})
        if description is not UNSET:
            field_dict['description'] = description
        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop('path')
        value = CreateResourceValue.from_dict(d.pop('value'))
        resource_type = d.pop('resource_type')
        description = d.pop('description', UNSET)
        create_resource = cls(path=path, value=value, resource_type=resource_type, description=description)
        create_resource.additional_properties = d
        return create_resource

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