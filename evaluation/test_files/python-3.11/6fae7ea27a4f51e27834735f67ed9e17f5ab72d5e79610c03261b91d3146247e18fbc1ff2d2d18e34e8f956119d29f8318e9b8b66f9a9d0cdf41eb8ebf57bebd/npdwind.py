from typing import Dict, Sequence, List
from dmt.blueprint import Blueprint
from .blueprints.npdwind import NPDWindBlueprint
from typing import Dict
from sima.environment.wind import Wind
from sima.sima.scriptablevalue import ScriptableValue

class NPDWind(Wind):
    """
    Keyword arguments
    -----------------
    _id : str
         (default "")
    scriptableValues : List[ScriptableValue]
    direction : float
         Wind propagation direction(default 0.0)
    profileExponent : float
         Wind profile exponent(default 0.11)
    averageVelocity : float
         Average velocity at reference height(default 0.0)
    friction : float
         Surface drag coefficient.
Also used for transverse gust spectrum, if specified in DYNMOD.(default 0.002)
    referenceHeight : float
         Reference height for wind velocity, fixed = 10 m.(default 10.0)
    """

    def __init__(self, _id='', direction=0.0, profileExponent=0.11, averageVelocity=0.0, friction=0.002, referenceHeight=10.0, **kwargs):
        super().__init__(**kwargs)
        self._id = _id
        self.scriptableValues = list()
        self.direction = direction
        self.profileExponent = profileExponent
        self.averageVelocity = averageVelocity
        self.friction = friction
        self.referenceHeight = referenceHeight
        for key, value in kwargs.items():
            if not isinstance(value, Dict):
                setattr(self, key, value)

    @property
    def blueprint(self) -> Blueprint:
        """Return blueprint that this entity represents"""
        return NPDWindBlueprint()

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
    def direction(self) -> float:
        """Wind propagation direction"""
        return self.__direction

    @direction.setter
    def direction(self, value: float):
        """Set direction"""
        self.__direction = float(value)

    @property
    def profileExponent(self) -> float:
        """Wind profile exponent"""
        return self.__profileExponent

    @profileExponent.setter
    def profileExponent(self, value: float):
        """Set profileExponent"""
        self.__profileExponent = float(value)

    @property
    def averageVelocity(self) -> float:
        """Average velocity at reference height"""
        return self.__averageVelocity

    @averageVelocity.setter
    def averageVelocity(self, value: float):
        """Set averageVelocity"""
        self.__averageVelocity = float(value)

    @property
    def friction(self) -> float:
        """Surface drag coefficient.
Also used for transverse gust spectrum, if specified in DYNMOD."""
        return self.__friction

    @friction.setter
    def friction(self, value: float):
        """Set friction"""
        self.__friction = float(value)

    @property
    def referenceHeight(self) -> float:
        """Reference height for wind velocity, fixed = 10 m."""
        return self.__referenceHeight

    @referenceHeight.setter
    def referenceHeight(self, value: float):
        """Set referenceHeight"""
        self.__referenceHeight = float(value)