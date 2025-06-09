from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from brayns.core import Model, deserialize_model
from brayns.network import Instance
from brayns.utils import Color4, JsonSchema, Vector, deserialize_schema

class AtlasUsecase(ABC):
    """Base class for all atlas visualization usecases."""

    @classmethod
    @property
    @abstractmethod
    def name(cls) -> str:
        """Low level API."""
        pass

    @abstractmethod
    def get_properties(self) -> dict[str, Any]:
        """Low level API."""
        pass

    def run(self, instance: Instance, model_id: int) -> Model:
        """Create a model to visualize the usecase on an atlas volume.

        :param instance: Instance.
        :type instance: Instance
        :param model_id: ID of the atlas volume model.
        :type model_id: int
        :return: Model created for the usecase.
        :rtype: Model
        """
        params = {'model_id': model_id, 'use_case': self.name, 'params': self.get_properties()}
        result = instance.request('visualize-atlas-usecase', params)
        return deserialize_model(result)

class AtlasDensity(AtlasUsecase):
    """Display the volume density.

    The relation between the density and the color can be changed using the
    color ramp of the model created.
    """

    @classmethod
    @property
    def name(cls) -> str:
        return 'Density'

    def get_properties(self) -> dict[str, Any]:
        return {}

class AtlasFlatmapAreas(AtlasUsecase):
    """Display the volumne flatmap areas."""

    @classmethod
    @property
    def name(cls) -> str:
        return 'Flatmap areas'

    def get_properties(self) -> dict[str, Any]:
        return {}

class ColumnPosition(Vector[int]):
    """Column position XZ.

    :param x: X component.
    :type x: float
    :param z: Z component.
    :type z: float
    """

    def __new__(cls, x: int=0, z: int=0) -> ColumnPosition:
        return super().__new__(cls, x, z)

    @property
    def x(self) -> float:
        return self[0]

    @property
    def z(self) -> float:
        return self[1]

@dataclass
class ColumnNeighbor:
    """Column neighbor position and color.

    The position is relative to the main column coordinates.
    """
    position: ColumnPosition
    color: Color4

@dataclass
class AtlasColumnHighlight(AtlasUsecase):
    """Place a column and (optionally) its neighbors.

    Columns are always aligned on the Y axis so their position uses only XZ.

    :param position: Column coordinates.
    :type position: ColumnPosition
    :param color: Color to apply to the column.
    :type color: Color4
    :param neighbors: Neighbors to color, defaults to empty.
    :type neighbors: list[ColumnNeighbor], optional
    """
    position: ColumnPosition
    color: Color4
    neighbors: list[ColumnNeighbor] = field(default_factory=list)

    @classmethod
    @property
    def name(cls) -> str:
        return 'Highlight columns'

    def get_properties(self) -> dict[str, Any]:
        return {'xz_coordinate': list(self.position), 'color': list(self.color), 'neighbours': [{'relative_xz': list(neighbor.position), 'color': list(neighbor.color)} for neighbor in self.neighbors]}

class AtlasDistanceType(Enum):
    """Type of distance displayed for an atlas layer.

    :params LOWER: Distance of the current layer from the one below.
    :params UPPER: Distance of the current layer from the one above.
    """
    LOWER = 'lower'
    UPPER = 'upper'

@dataclass
class AtlasLayerDistance(AtlasUsecase):
    """Display the volume as the distance of a layer from its neighbors."""
    distance_type: AtlasDistanceType

    @classmethod
    @property
    def name(cls) -> str:
        return 'Layer distance'

    def get_properties(self) -> dict[str, Any]:
        return {'type': self.distance_type.value}

class AtlasOrientationField(AtlasUsecase):
    """Display the volume data as an orientation field."""

    @classmethod
    @property
    def name(cls) -> str:
        return 'Orientation field'

    def get_properties(self) -> dict[str, Any]:
        return {}

class AtlasShellOutline(AtlasUsecase):
    """Display the volume using its shell outline.

    This is the default atlas volume usecase and is always supported.
    """

    @classmethod
    @property
    def name(cls) -> str:
        return 'Outline mesh shell'

    def get_properties(self) -> dict[str, Any]:
        return {}

def get_atlas_usecases(instance: Instance, model_id: int) -> list[tuple[str, JsonSchema]]:
    """Return the list of visualization usecases supported by an atlas volume.

    :param instance: Instance.
    :type instance: Instance
    :param model_id: ID of the atlas volume model.
    :type model_id: int
    :return: Names of the supported usecase (see ``AtlasUsecase.name``)
    :rtype: list[str]
    """
    params = {'model_id': model_id}
    result: list[dict[str, Any]] = instance.request('get-available-atlas-usecases', params)
    return [(item['name'], deserialize_schema(item['params_schema'])) for item in result]