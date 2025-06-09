from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import hunting_row_result, single_property_schema

class HuntingQueryResults(AdditionalDataHolder, Parsable):

    def __init__(self) -> None:
        """
        Instantiates a new huntingQueryResults and sets the default values.
        """
        self._additional_data: Dict[str, Any] = {}
        self._odata_type: Optional[str] = None
        self._results: Optional[List[hunting_row_result.HuntingRowResult]] = None
        self._schema: Optional[List[single_property_schema.SinglePropertySchema]] = None

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
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> HuntingQueryResults:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: HuntingQueryResults
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return HuntingQueryResults()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import hunting_row_result, single_property_schema
        fields: Dict[str, Callable[[Any], None]] = {'@odata.type': lambda n: setattr(self, 'odata_type', n.get_str_value()), 'results': lambda n: setattr(self, 'results', n.get_collection_of_object_values(hunting_row_result.HuntingRowResult)), 'schema': lambda n: setattr(self, 'schema', n.get_collection_of_object_values(single_property_schema.SinglePropertySchema))}
        return fields

    @property
    def odata_type(self) -> Optional[str]:
        """
        Gets the @odata.type property value. The OdataType property
        Returns: Optional[str]
        """
        return self._odata_type

    @odata_type.setter
    def odata_type(self, value: Optional[str]=None) -> None:
        """
        Sets the @odata.type property value. The OdataType property
        Args:
            value: Value to set for the odata_type property.
        """
        self._odata_type = value

    @property
    def results(self) -> Optional[List[hunting_row_result.HuntingRowResult]]:
        """
        Gets the results property value. The results of the hunting query.
        Returns: Optional[List[hunting_row_result.HuntingRowResult]]
        """
        return self._results

    @results.setter
    def results(self, value: Optional[List[hunting_row_result.HuntingRowResult]]=None) -> None:
        """
        Sets the results property value. The results of the hunting query.
        Args:
            value: Value to set for the results property.
        """
        self._results = value

    @property
    def schema(self) -> Optional[List[single_property_schema.SinglePropertySchema]]:
        """
        Gets the schema property value. The schema for the response.
        Returns: Optional[List[single_property_schema.SinglePropertySchema]]
        """
        return self._schema

    @schema.setter
    def schema(self, value: Optional[List[single_property_schema.SinglePropertySchema]]=None) -> None:
        """
        Sets the schema property value. The schema for the response.
        Args:
            value: Value to set for the schema property.
        """
        self._schema = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        writer.write_str_value('@odata.type', self.odata_type)
        writer.write_collection_of_object_values('results', self.results)
        writer.write_collection_of_object_values('schema', self.schema)
        writer.write_additional_data_value(self.additional_data)