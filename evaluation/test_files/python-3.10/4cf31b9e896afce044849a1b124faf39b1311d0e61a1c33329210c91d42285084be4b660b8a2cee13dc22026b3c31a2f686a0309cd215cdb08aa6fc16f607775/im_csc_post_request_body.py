from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ........models import json

class ImCscPostRequestBody(AdditionalDataHolder, Parsable):

    def __init__(self) -> None:
        """
        Instantiates a new imCscPostRequestBody and sets the default values.
        """
        self._additional_data: Dict[str, Any] = {}
        self._inumber: Optional[json.Json] = None

    @property
    def additional_data(self) -> Dict[str, Any]:
        """
        Gets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Returns: Dict[str, Any]
        """
        return self._additional_data

    @additional_data.setter
    def additional_data(self, value: Dict[str, Any]) -> None:
        """
        Sets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Args:
            value: Value to set for the AdditionalData property.
        """
        self._additional_data = value

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> ImCscPostRequestBody:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: ImCscPostRequestBody
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return ImCscPostRequestBody()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from ........models import json
        fields: Dict[str, Callable[[Any], None]] = {'inumber': lambda n: setattr(self, 'inumber', n.get_object_value(json.Json))}
        return fields

    @property
    def inumber(self) -> Optional[json.Json]:
        """
        Gets the inumber property value. The inumber property
        Returns: Optional[json.Json]
        """
        return self._inumber

    @inumber.setter
    def inumber(self, value: Optional[json.Json]=None) -> None:
        """
        Sets the inumber property value. The inumber property
        Args:
            value: Value to set for the inumber property.
        """
        self._inumber = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        writer.write_object_value('inumber', self.inumber)
        writer.write_additional_data_value(self.additional_data)