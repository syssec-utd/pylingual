from __future__ import annotations
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import entity, workbook_chart_legend_format
from . import entity

class WorkbookChartLegend(entity.Entity):

    def __init__(self) -> None:
        """
        Instantiates a new workbookChartLegend and sets the default values.
        """
        super().__init__()
        self._format: Optional[workbook_chart_legend_format.WorkbookChartLegendFormat] = None
        self.odata_type: Optional[str] = None
        self._overlay: Optional[bool] = None
        self._position: Optional[str] = None
        self._visible: Optional[bool] = None

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> WorkbookChartLegend:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: WorkbookChartLegend
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        return WorkbookChartLegend()

    @property
    def format(self) -> Optional[workbook_chart_legend_format.WorkbookChartLegendFormat]:
        """
        Gets the format property value. Represents the formatting of a chart legend, which includes fill and font formatting. Read-only.
        Returns: Optional[workbook_chart_legend_format.WorkbookChartLegendFormat]
        """
        return self._format

    @format.setter
    def format(self, value: Optional[workbook_chart_legend_format.WorkbookChartLegendFormat]=None) -> None:
        """
        Sets the format property value. Represents the formatting of a chart legend, which includes fill and font formatting. Read-only.
        Args:
            value: Value to set for the format property.
        """
        self._format = value

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import entity, workbook_chart_legend_format
        fields: Dict[str, Callable[[Any], None]] = {'format': lambda n: setattr(self, 'format', n.get_object_value(workbook_chart_legend_format.WorkbookChartLegendFormat)), 'overlay': lambda n: setattr(self, 'overlay', n.get_bool_value()), 'position': lambda n: setattr(self, 'position', n.get_str_value()), 'visible': lambda n: setattr(self, 'visible', n.get_bool_value())}
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields

    @property
    def overlay(self) -> Optional[bool]:
        """
        Gets the overlay property value. Boolean value for whether the chart legend should overlap with the main body of the chart.
        Returns: Optional[bool]
        """
        return self._overlay

    @overlay.setter
    def overlay(self, value: Optional[bool]=None) -> None:
        """
        Sets the overlay property value. Boolean value for whether the chart legend should overlap with the main body of the chart.
        Args:
            value: Value to set for the overlay property.
        """
        self._overlay = value

    @property
    def position(self) -> Optional[str]:
        """
        Gets the position property value. Represents the position of the legend on the chart. The possible values are: Top, Bottom, Left, Right, Corner, Custom.
        Returns: Optional[str]
        """
        return self._position

    @position.setter
    def position(self, value: Optional[str]=None) -> None:
        """
        Sets the position property value. Represents the position of the legend on the chart. The possible values are: Top, Bottom, Left, Right, Corner, Custom.
        Args:
            value: Value to set for the position property.
        """
        self._position = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        super().serialize(writer)
        writer.write_object_value('format', self.format)
        writer.write_bool_value('overlay', self.overlay)
        writer.write_str_value('position', self.position)
        writer.write_bool_value('visible', self.visible)

    @property
    def visible(self) -> Optional[bool]:
        """
        Gets the visible property value. A boolean value the represents the visibility of a ChartLegend object.
        Returns: Optional[bool]
        """
        return self._visible

    @visible.setter
    def visible(self, value: Optional[bool]=None) -> None:
        """
        Sets the visible property value. A boolean value the represents the visibility of a ChartLegend object.
        Args:
            value: Value to set for the visible property.
        """
        self._visible = value