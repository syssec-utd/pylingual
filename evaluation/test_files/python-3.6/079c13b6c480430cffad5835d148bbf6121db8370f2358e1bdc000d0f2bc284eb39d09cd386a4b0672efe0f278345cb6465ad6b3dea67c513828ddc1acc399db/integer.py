"""Library for parsing and encoding INTEGER values."""
from typing import Any
from ical.parsing.property import ParsedProperty
from .data_types import DATA_TYPE

@DATA_TYPE.register('INTEGER')
class IntEncoder:
    """Encode an int ICS value."""

    @classmethod
    def __property_type__(cls) -> type:
        return int

    @classmethod
    def __parse_property_value__(cls, prop: Any) -> int:
        """Parse a rfc5545 int value."""
        if isinstance(prop, ParsedProperty):
            return int(prop.value)
        return int(prop)