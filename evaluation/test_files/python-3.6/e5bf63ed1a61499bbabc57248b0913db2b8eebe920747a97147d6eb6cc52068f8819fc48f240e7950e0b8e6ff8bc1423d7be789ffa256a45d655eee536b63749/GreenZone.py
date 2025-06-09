from __future__ import annotations
from typing import TYPE_CHECKING, List
from ..ns import *
from .Facility import Facility
if TYPE_CHECKING:
    from ontopia_py.mu.Value import Value
    from rdflib import Graph
    from .Plant import Plant

class GreenZone(Facility):
    __type__ = ONTOIM['GreenZone']
    hasPlant: List[Plant] = None
    hasSurface: List[Value] = None

    def _addProperties(self, g: Graph):
        super()._addProperties(g)
        if self.hasPlant:
            for hasPlant in self.hasPlant:
                g.add((self.uriRef, ONTOIM['hasPlant'], hasPlant.uriRef))
        if self.hasSurface:
            for hasSurface in self.hasSurface:
                g.add((self.uriRef, ONTOIM['hasSurface'], hasSurface.uriRef))