from typing import Iterator, Mapping, Sequence, Type
from apischema.conversions.conversions import DefaultConversion
from apischema.conversions.visitor import DeserializationVisitor
from apischema.objects import ObjectField
from apischema.objects.visitor import DeserializationObjectVisitor
from apischema.types import AnyType
from apischema.utils import get_origin_or_type
from apischema.visitor import Unsupported

class InitFlattenedAliasVisitor(DeserializationObjectVisitor[Iterator[str]], DeserializationVisitor[Iterator[str]]):

    def mapping(self, cls: Type[Mapping], key_type: AnyType, value_type: AnyType) -> Iterator[str]:
        yield from ()

    def object(self, tp: AnyType, fields: Sequence[ObjectField]) -> Iterator[str]:
        for field in fields:
            if field.flattened:
                yield from get_deserialization_flattened_aliases(get_origin_or_type(tp), field, self.default_conversion)
            elif not field.is_aggregate:
                yield field.alias

    def _visited_union(self, results: Sequence[Iterator[str]]) -> Iterator[str]:
        if len(results) != 1:
            raise NotImplementedError
        return results[0]

def get_deserialization_flattened_aliases(cls: Type, field: ObjectField, default_conversion: DefaultConversion) -> Iterator[str]:
    assert field.flattened
    try:
        yield from InitFlattenedAliasVisitor(default_conversion).visit_with_conv(field.type, field.deserialization)
    except (NotImplementedError, Unsupported):
        raise TypeError(f'Flattened field {cls.__name__}.{field.name} must have an object type') from None