from typing import Dict, Sequence, List
from dmt.blueprint import Blueprint
from .blueprints.hlasurface import HLASurfaceBlueprint
from typing import Dict
from sima.hla.hlaobject import HLAObject
from sima.hla.surfacetype import SurfaceType
from sima.sima.scriptablevalue import ScriptableValue

class HLASurface(HLAObject):
    """
    Keyword arguments
    -----------------
    _id : str
         (default "")
    scriptableValues : List[ScriptableValue]
    name : str
         (default "")
    _type : SurfaceType
    transparency : float
         (default 0.0)
    sizeX : float
         (default 0.0)
    sizeY : float
         (default 0.0)
    """

    def __init__(self, _id='', name='', _type=SurfaceType.OCEAN_SURFACE, transparency=0.0, sizeX=0.0, sizeY=0.0, **kwargs):
        super().__init__(**kwargs)
        self._id = _id
        self.scriptableValues = list()
        self.name = name
        self._type = _type
        self.transparency = transparency
        self.sizeX = sizeX
        self.sizeY = sizeY
        for key, value in kwargs.items():
            if not isinstance(value, Dict):
                setattr(self, key, value)

    @property
    def blueprint(self) -> Blueprint:
        """Return blueprint that this entity represents"""
        return HLASurfaceBlueprint()

    @property
    def _id(self) -> str:
        """"""
        return self.___id

    @_id.setter
    def _id(self, value: str):
        """Set _id"""
        self.___id = str(value)

    @property
    def scriptableValues(self) -> List[ScriptableValue]:
        """"""
        return self.__scriptableValues

    @scriptableValues.setter
    def scriptableValues(self, value: List[ScriptableValue]):
        """Set scriptableValues"""
        if not isinstance(value, Sequence):
            raise Exception('Expected sequense, but was ', type(value))
        self.__scriptableValues = value

    @property
    def name(self) -> str:
        """"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set name"""
        self.__name = str(value)

    @property
    def _type(self) -> SurfaceType:
        """"""
        return self.___type

    @_type.setter
    def _type(self, value: SurfaceType):
        """Set _type"""
        self.___type = value

    @property
    def transparency(self) -> float:
        """"""
        return self.__transparency

    @transparency.setter
    def transparency(self, value: float):
        """Set transparency"""
        self.__transparency = float(value)

    @property
    def sizeX(self) -> float:
        """"""
        return self.__sizeX

    @sizeX.setter
    def sizeX(self, value: float):
        """Set sizeX"""
        self.__sizeX = float(value)

    @property
    def sizeY(self) -> float:
        """"""
        return self.__sizeY

    @sizeY.setter
    def sizeY(self, value: float):
        """Set sizeY"""
        self.__sizeY = float(value)