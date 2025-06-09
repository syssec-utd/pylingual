from __future__ import annotations
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import entity, json
from . import entity

class WorkbookTableRow(entity.Entity):

    def __init__(self) -> None:
        """
        Instantiates a new workbookTableRow and sets the default values.
        """
        super().__init__()
        self._index: Optional[int] = None
        self.odata_type: Optional[str] = None
        self._values: Optional[json.Json] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> WorkbookTableRow:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: WorkbookTableRow
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return WorkbookTableRow()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import entity, json
        fields: Dict[str, Callable[[Any], None]] = {'index': lambda n: setattr(self, 'index', n.get_int_value()), 'values': lambda n: setattr(self, 'values', n.get_object_value(json.Json))}
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields

    @property
    def index(self) -> Optional[int]:
        """
        Gets the index property value. Returns the index number of the row within the rows collection of the table. Zero-indexed. Read-only.
        Returns: Optional[int]
        """
        return self._index

    @index.setter
    def index(self, value: Optional[int]=None) -> None:
        """
        Sets the index property value. Returns the index number of the row within the rows collection of the table. Zero-indexed. Read-only.
        Args:
            value: Value to set for the index property.
        """
        self._index = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        super().serialize(writer)
        writer.write_int_value('index', self.index)
        writer.write_object_value('values', self.values)

    @property
    def values(self) -> Optional[json.Json]:
        """
        Gets the values property value. Represents the raw values of the specified range. The data returned could be of type string, number, or a boolean. Cell that contain an error will return the error string.
        Returns: Optional[json.Json]
        """
        return self._values

    @values.setter
    def values(self, value: Optional[json.Json]=None) -> None:
        """
        Sets the values property value. Represents the raw values of the specified range. The data returned could be of type string, number, or a boolean. Cell that contain an error will return the error string.
        Args:
            value: Value to set for the values property.
        """
        self._values = value