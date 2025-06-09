from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ........models import json

class ArabicPostRequestBody(AdditionalDataHolder, Parsable):

    def __init__(self) -> None:
        """
        Instantiates a new arabicPostRequestBody and sets the default values.
        """
        self._additional_data: Dict[str, Any] = {}
        self._text: Optional[json.Json] = None

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
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> ArabicPostRequestBody:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: ArabicPostRequestBody
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return ArabicPostRequestBody()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from ........models import json
        fields: Dict[str, Callable[[Any], None]] = {'text': lambda n: setattr(self, 'text', n.get_object_value(json.Json))}
        return fields

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        writer.write_object_value('text', self.text)
        writer.write_additional_data_value(self.additional_data)

    @property
    def text(self) -> Optional[json.Json]:
        """
        Gets the text property value. The text property
        Returns: Optional[json.Json]
        """
        return self._text

    @text.setter
    def text(self, value: Optional[json.Json]=None) -> None:
        """
        Sets the text property value. The text property
        Args:
            value: Value to set for the text property.
        """
        self._text = value