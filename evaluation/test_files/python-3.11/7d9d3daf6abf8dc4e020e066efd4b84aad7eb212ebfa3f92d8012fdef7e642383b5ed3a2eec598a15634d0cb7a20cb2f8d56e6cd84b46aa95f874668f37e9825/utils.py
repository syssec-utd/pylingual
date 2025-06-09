from typing import Any, Type

class AntiForwardRef:
    """
    i.e:
    Union["someString"] would return a ForwardRef, this class is a simple hack
    to just return a type contains the name.
    Also, this is a workaround for types that reference each-other,
    otherwise it would cause recursion error.
    """
    name: str
    type_map: dict

    @classmethod
    def resolve(cls) -> Any:
        return cls.type_map[cls.name]

def anti_forward_ref(name: str, type_map: dict) -> Type[AntiForwardRef]:
    return type(name, (AntiForwardRef,), {'name': name, 'type_map': type_map})