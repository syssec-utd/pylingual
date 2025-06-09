from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import recommended_action, simulation_events_content, training_events_content

class SimulationReportOverview(AdditionalDataHolder, Parsable):

    def __init__(self) -> None:
        """
        Instantiates a new simulationReportOverview and sets the default values.
        """
        self._additional_data: Dict[str, Any] = {}
        self._odata_type: Optional[str] = None
        self._recommended_actions: Optional[List[recommended_action.RecommendedAction]] = None
        self._resolved_targets_count: Optional[int] = None
        self._simulation_events_content: Optional[simulation_events_content.SimulationEventsContent] = None
        self._training_events_content: Optional[training_events_content.TrainingEventsContent] = None

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
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> SimulationReportOverview:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: SimulationReportOverview
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return SimulationReportOverview()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import recommended_action, simulation_events_content, training_events_content
        fields: Dict[str, Callable[[Any], None]] = {'@odata.type': lambda n: setattr(self, 'odata_type', n.get_str_value()), 'recommendedActions': lambda n: setattr(self, 'recommended_actions', n.get_collection_of_object_values(recommended_action.RecommendedAction)), 'resolvedTargetsCount': lambda n: setattr(self, 'resolved_targets_count', n.get_int_value()), 'simulationEventsContent': lambda n: setattr(self, 'simulation_events_content', n.get_object_value(simulation_events_content.SimulationEventsContent)), 'trainingEventsContent': lambda n: setattr(self, 'training_events_content', n.get_object_value(training_events_content.TrainingEventsContent))}
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
    def recommended_actions(self) -> Optional[List[recommended_action.RecommendedAction]]:
        """
        Gets the recommendedActions property value. List of recommended actions for a tenant to improve its security posture based on the attack simulation and training campaign attack type.
        Returns: Optional[List[recommended_action.RecommendedAction]]
        """
        return self._recommended_actions

    @recommended_actions.setter
    def recommended_actions(self, value: Optional[List[recommended_action.RecommendedAction]]=None) -> None:
        """
        Sets the recommendedActions property value. List of recommended actions for a tenant to improve its security posture based on the attack simulation and training campaign attack type.
        Args:
            value: Value to set for the recommended_actions property.
        """
        self._recommended_actions = value

    @property
    def resolved_targets_count(self) -> Optional[int]:
        """
        Gets the resolvedTargetsCount property value. Number of valid users in the attack simulation and training campaign.
        Returns: Optional[int]
        """
        return self._resolved_targets_count

    @resolved_targets_count.setter
    def resolved_targets_count(self, value: Optional[int]=None) -> None:
        """
        Sets the resolvedTargetsCount property value. Number of valid users in the attack simulation and training campaign.
        Args:
            value: Value to set for the resolved_targets_count property.
        """
        self._resolved_targets_count = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        writer.write_str_value('@odata.type', self.odata_type)
        writer.write_collection_of_object_values('recommendedActions', self.recommended_actions)
        writer.write_int_value('resolvedTargetsCount', self.resolved_targets_count)
        writer.write_object_value('simulationEventsContent', self.simulation_events_content)
        writer.write_object_value('trainingEventsContent', self.training_events_content)
        writer.write_additional_data_value(self.additional_data)

    @property
    def simulation_events_content(self) -> Optional[simulation_events_content.SimulationEventsContent]:
        """
        Gets the simulationEventsContent property value. Summary of simulation events in the attack simulation and training campaign.
        Returns: Optional[simulation_events_content.SimulationEventsContent]
        """
        return self._simulation_events_content

    @simulation_events_content.setter
    def simulation_events_content(self, value: Optional[simulation_events_content.SimulationEventsContent]=None) -> None:
        """
        Sets the simulationEventsContent property value. Summary of simulation events in the attack simulation and training campaign.
        Args:
            value: Value to set for the simulation_events_content property.
        """
        self._simulation_events_content = value

    @property
    def training_events_content(self) -> Optional[training_events_content.TrainingEventsContent]:
        """
        Gets the trainingEventsContent property value. Summary of assigned trainings in the attack simulation and training campaign.
        Returns: Optional[training_events_content.TrainingEventsContent]
        """
        return self._training_events_content

    @training_events_content.setter
    def training_events_content(self, value: Optional[training_events_content.TrainingEventsContent]=None) -> None:
        """
        Sets the trainingEventsContent property value. Summary of assigned trainings in the attack simulation and training campaign.
        Args:
            value: Value to set for the training_events_content property.
        """
        self._training_events_content = value