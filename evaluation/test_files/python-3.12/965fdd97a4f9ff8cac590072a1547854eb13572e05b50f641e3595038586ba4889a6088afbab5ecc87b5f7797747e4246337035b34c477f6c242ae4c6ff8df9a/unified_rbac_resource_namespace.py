from __future__ import annotations
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import entity, unified_rbac_resource_action
from . import entity

class UnifiedRbacResourceNamespace(entity.Entity):

    def __init__(self) -> None:
        """
        Instantiates a new unifiedRbacResourceNamespace and sets the default values.
        """
        super().__init__()
        self._name: Optional[str] = None
        self.odata_type: Optional[str] = None
        self._resource_actions: Optional[List[unified_rbac_resource_action.UnifiedRbacResourceAction]] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> UnifiedRbacResourceNamespace:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: UnifiedRbacResourceNamespace
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return UnifiedRbacResourceNamespace()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import entity, unified_rbac_resource_action
        fields: Dict[str, Callable[[Any], None]] = {'name': lambda n: setattr(self, 'name', n.get_str_value()), 'resourceActions': lambda n: setattr(self, 'resource_actions', n.get_collection_of_object_values(unified_rbac_resource_action.UnifiedRbacResourceAction))}
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields

    @property
    def name(self) -> Optional[str]:
        """
        Gets the name property value. The name property
        Returns: Optional[str]
        """
        return self._name

    @name.setter
    def name(self, value: Optional[str]=None) -> None:
        """
        Sets the name property value. The name property
        Args:
            value: Value to set for the name property.
        """
        self._name = value

    @property
    def resource_actions(self) -> Optional[List[unified_rbac_resource_action.UnifiedRbacResourceAction]]:
        """
        Gets the resourceActions property value. The resourceActions property
        Returns: Optional[List[unified_rbac_resource_action.UnifiedRbacResourceAction]]
        """
        return self._resource_actions

    @resource_actions.setter
    def resource_actions(self, value: Optional[List[unified_rbac_resource_action.UnifiedRbacResourceAction]]=None) -> None:
        """
        Sets the resourceActions property value. The resourceActions property
        Args:
            value: Value to set for the resource_actions property.
        """
        self._resource_actions = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        super().serialize(writer)
        writer.write_str_value('name', self.name)
        writer.write_collection_of_object_values('resourceActions', self.resource_actions)