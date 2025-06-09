"""
Contains type definitions for :py:class:`encomp.units.Quantity` objects.

The dimensionalities defined in this module can be combined with ``*`` and ``/``.
Some commonly used derived dimensionalities (like density) are defined for convenience.

This module can be star-imported, variables prefixed with ``_`` will not
be imported in this case.
"""
from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Literal, TypeVar, _LiteralGenericAlias
import numpy as np
import pandas as pd
import polars as pl
from pint.util import UnitsContainer
_BASE_SI_UNITS = ('m', 'kg', 's', 'K', 'mol', 'A', 'cd')
DimensionlessUnits = Literal['', '%', '-', 'dimensionless', None]
CurrencyUnits = Literal['SEK', 'EUR', 'USD', 'kSEK', 'kEUR', 'kUSD', 'MSEK', 'MEUR', 'MUSD']
CurrencyPerEnergyUnits = Literal['SEK/MWh', 'EUR/MWh', 'SEK/kWh', 'EUR/kWh', 'SEK/GWh', 'EUR/GWh', 'SEK/TWh', 'EUR/TWh']
CurrencyPerMassUnits = Literal['SEK/kg', 'EUR/kg', 'SEK/t', 'EUR/t', 'SEK/ton', 'EUR/ton', 'SEK/g', 'EUR/g', 'SEK/mg', 'EUR/mg', 'SEK/ug', 'EUR/ug']
CurrencyPerVolumeUnits = Literal['SEK/L', 'EUR/L', 'SEK/l', 'EUR/l', 'SEK/liter', 'EUR/liter', 'SEK/m3', 'EUR/m3', 'SEK/m^3', 'EUR/m^3', 'SEK/m**3', 'EUR/m**3', 'SEK/m³', 'EUR/m³']
CurrencyPerTimeUnits = Literal['SEK/h', 'EUR/h', 'SEK/hr', 'EUR/hr', 'SEK/hour', 'EUR/hour', 'SEK/d', 'EUR/d', 'SEK/day', 'EUR/day', 'SEK/w', 'EUR/w', 'SEK/week', 'EUR/week', 'SEK/y', 'EUR/y', 'SEK/yr', 'EUR/yr', 'SEK/year', 'EUR/year', 'SEK/a', 'EUR/a']
LengthUnits = Literal['m', 'meter', 'km', 'cm', 'mm', 'um']
MassUnits = Literal['kg', 'g', 'ton', 'tonne', 't', 'mg', 'ug']
TimeUnits = Literal['s', 'second', 'min', 'minute', 'h', 'hr', 'hour', 'd', 'day', 'w', 'week', 'y', 'yr', 'a', 'year', 'ms', 'us']
TemperatureUnits = Literal['degC', '°C', 'K', 'degF', '°F', '℃', '℉']
TemperatureDifferenceUnits = Literal['delta_°C', 'delta_degC', 'Δ°C', 'Δ℃', 'delta_°F', 'delta_degF', 'Δ°F', 'Δ℉']
SubstanceUnits = Literal['mol', 'kmol']
MolarMassUnits = Literal['g/mol', 'kg/kmol']
SubstancePerMassUnits = Literal['mol/g', 'kmol/kg']
CurrentUnits = Literal['A', 'mA']
LuminosityUnits = Literal['lm']
AreaUnits = Literal['m2', 'm^2', 'm**2', 'm²', 'cm2', 'cm^2', 'cm**2', 'cm²']
VolumeUnits = Literal['L', 'l', 'liter', 'm3', 'm^3', 'm³', 'm**3', 'dm3', 'dm^3', 'dm³', 'dm**3', 'cm3', 'cm^3', 'cm³', 'cm**3']
NormalVolumeUnits = Literal['normal liter', 'Nm3', 'nm3', 'Nm^3', 'nm^3', 'Nm³', 'nm³', 'Nm**3', 'nm**3']
PressureUnits = Literal['bar', 'kPa', 'Pa', 'MPa', 'mbar', 'mmHg', 'atm']
MassFlowUnits = Literal['kg/s', 'kg/h', 'kg/hr', 'g/s', 'g/h', 'g/hr', 'ton/h', 't/h', 'ton/hr', 't/hr', 't/d', 'ton/day', 't/w', 'ton/week', 't/y', 't/a', 't/year', 'ton/y', 'ton/a', 'ton/year']
VolumeFlowUnits = Literal['m3/s', 'm3/h', 'm3/hr', 'm**3/s', 'm**3/h', 'm**3/hr', 'm^3/s', 'm^3/h', 'm^3/hr', 'm³/s', 'm³/h', 'm³/hr', 'liter/second', 'l/s', 'L/s', 'liter/s', 'liter/hour', 'l/h', 'L/h', 'L/hr', 'l/hr']
NormalVolumeFlowUnits = Literal['Nm3/s', 'Nm3/h', 'Nm3/hr', 'nm3/s', 'nm3/h', 'nm3/hr', 'Nm^3/s', 'Nm^3/h', 'Nm^3/hr', 'nm^3/s', 'nm^3/h', 'nm^3/hr', 'Nm³/s', 'Nm³/h', 'Nm³/hr', 'nm³/s', 'nm³/h', 'nm³/hr', 'Nm**3/s', 'Nm**3/h', 'Nm**3/hr', 'nm**3/s', 'nm**3/h', 'nm**3/hr']
DensityUnits = Literal['kg/m3', 'kg/m**3', 'kg/m^3', 'kg/m³', 'kg/liter', 'g/l', 'g/L', 'gram/liter']
SpecificVolumeUnits = Literal['m3/kg', 'm^3/kg', 'm³/kg', 'l/g', 'L/g']
NormalVolumePerMassUnits = Literal['Nm3/kg', 'Nm^3/kg', 'Nm³/kg', 'nm3/kg', 'nm^3/kg', 'nm³/kg']
EnergyUnits = Literal['J', 'kJ', 'MJ', 'GJ', 'TJ', 'PJ', 'kWh', 'MWh', 'Wh', 'GWh', 'TWh']
PowerUnits = Literal['W', 'kW', 'MW', 'GW', 'TW', 'mW', 'kWh/d', 'kWh/w', 'kWh/y', 'kWh/yr', 'kWh/year', 'MWh/d', 'MWh/w', 'MWh/y', 'MWh/yr', 'MWh/year', 'GWh/d', 'GWh/w', 'GWh/y', 'GWh/yr', 'GWh/year', 'TWh/d', 'TWh/w', 'TWh/y', 'TWh/yr', 'TWh/year']
VelocityUnits = Literal['m/s', 'km/s', 'm/min', 'cm/s', 'cm/min', 'km/h', 'kmh', 'kph']
DynamicViscosityUnits = Literal['Pa*s', 'Pa s', 'cP']
KinematicViscosityUnits = Literal['m2/s', 'm**2/s', 'm^2/s', 'm²/s', 'cSt', 'cm2/s', 'cm**2/s', 'cm^2/s', 'cm²/s']
EnergyPerMassUnits = Literal['MJ/kg', 'MWh/kg', 'kJ/kg', 'kWh/kg', 'MJ/t', 'MWh/t', 'kJ/t', 'kWh/t', 'MJ/ton', 'MWh/ton', 'kJ/ton', 'kWh/ton']
SpecificHeatCapacityUnits = Literal['kJ/kg/K', 'kJ/kg/delta_degC', 'kJ/kg/Δ°C', 'kJ/kg/Δ℃', 'kJ/kg/°C', 'kJ/kg/℃', 'kJ/kg/degC', 'J/kg/K', 'J/kg/delta_degC', 'J/kg/Δ°C', 'J/kg/Δ℃', 'J/kg/°C', 'J/kg/℃', 'J/kg/degC', 'J/g/K', 'J/g/delta_degC', 'J/g/Δ°C', 'J/g/Δ℃', 'J/g/°C', 'J/g/℃', 'J/g/degC']

def get_registered_units() -> dict[str, tuple[str, ...]]:
    ret = {}
    for (k, v) in globals().items():
        if isinstance(v, _LiteralGenericAlias):
            if k.endswith('Units'):
                ret[k.removesuffix('Units')] = v.__args__
    return ret

class Dimensionality(ABC):
    """
    Represents the *dimensionality* of a unit, i.e.
    a combination (product) of the base dimensions (with optional rational exponents).

    A dimension ca be expressed as

    .. math::

        \\Pi \\, d^n_d, d \\in \\{T, L, M ,I, \\Theta, N, J, \\ldots\\}, n_d \\in \\mathbb{Q}

    where $\\{T, L, M, ...\\}$ are the base dimensions (time, length, mass, ...) and $n_d$ is a rational number.

    Subclasses of this abstract base class are used
    as type parameters when creating instances of
    :py:class:`encomp.units.Quantity`.

    The ``dimensions`` class attribute defines the dimensions
    of the dimensionality using an instance of
    ``pint.unit.UnitsContainer``.
    """
    _distinct: bool | None = None
    _intermediate: bool = False
    _UnsetUC = UnitsContainer()
    dimensions: UnitsContainer = _UnsetUC
    _registry: dict[type[Dimensionality], UnitsContainer] = {}
    _registry_reversed: dict[UnitsContainer, type[Dimensionality]] = {}

    def __init_subclass__(cls) -> None:
        if cls._intermediate:
            return
        if cls.dimensions is cls._UnsetUC:
            raise TypeError(f'Cannot initialize {cls}, class attribute "dimensionality" is not defined for this subclass')
        if cls.__name__ in (subcls.__name__ for subcls in cls._registry):
            existing = next(filter(lambda x: x.__name__ == cls.__name__, cls._registry))
            if str(cls.dimensions) != str(existing.dimensions):
                raise TypeError(f'Cannot create dimensionality subclass with name "{cls.__name__}", another subclass with this name already exists and the dimensions do not match: {cls.dimensions} != {existing.dimensions}')
            return
        if cls.dimensions is None:
            return
        if not isinstance(cls.dimensions, UnitsContainer):
            raise TypeError(f'The "dimensions" attribute of the Dimensionality type must be an instance of pint.util.UnitsContainer, {cls} has dimensions: {cls.dimensions} ({type(cls.dimensions)})')
        parent: type[Dimensionality] = cls.__mro__[1]
        if parent.dimensions is not cls._UnsetUC:
            if parent.dimensions != cls.dimensions:
                raise TypeError(f'Cannot create subclass of {parent} where the dimensions do not match. Tried to create subclass with dimensions {cls.dimensions}, but the parent has dimensions {parent.dimensions}')
        if cls in cls._registry:
            return
        cls._registry[cls] = cls.dimensions
        if cls.is_distinct():
            cls._registry_reversed[cls.dimensions] = cls

    @classmethod
    def get_dimensionality(cls, dimensions: UnitsContainer) -> type[Dimensionality]:
        if dimensions in cls._registry_reversed:
            return cls._registry_reversed[dimensions]
        _Dimensionality = type(f'Dimensionality[{dimensions}]', (Dimensionality,), {'dimensions': dimensions})
        return _Dimensionality

    @classmethod
    def is_distinct(cls) -> bool:
        if cls._distinct is None:
            if cls.dimensions is None:
                return True
            ucs = list(cls._registry.values())
            return ucs.count(cls.dimensions) == 1
        return cls._distinct
_DimensionlessUC = UnitsContainer({})
_CurrencyUC = UnitsContainer({'[currency]': 1})
_NormalUC = UnitsContainer({'[normal]': 1})
_LengthUC = UnitsContainer({'[length]': 1})
_MassUC = UnitsContainer({'[mass]': 1})
_TimeUC = UnitsContainer({'[time]': 1})
_TemperatureUC = UnitsContainer({'[temperature]': 1})
_SubstanceUC = UnitsContainer({'[substance]': 1})
_CurrentUC = UnitsContainer({'[current]': 1})
_LuminosityUC = UnitsContainer({'[luminosity]': 1})

class Unknown(Dimensionality):
    dimensions = None
if TYPE_CHECKING:
    MT = TypeVar('MT', float, list[float], np.ndarray, pd.Series, pd.DatetimeIndex, pd.Timestamp, pl.Series, pl.Expr, default=np.ndarray)
    MT_ = TypeVar('MT_', float, list[float], np.ndarray, pd.Series, pd.DatetimeIndex, pd.Timestamp, pl.Series, pl.Expr, default=np.ndarray)
    DT = TypeVar('DT', bound=Dimensionality, default=Unknown)
    DT_ = TypeVar('DT_', bound=Dimensionality, default=Unknown)
else:
    MT = TypeVar('MT', float, list[float], np.ndarray, pd.Series, pd.DatetimeIndex, pd.Timestamp, pl.Series, pl.Expr)
    MT_ = TypeVar('MT_', float, list[float], np.ndarray, pd.Series, pd.DatetimeIndex, pd.Timestamp, pl.Series, pl.Expr)
    DT = TypeVar('DT', bound=Dimensionality)
    DT_ = TypeVar('DT_', bound=Dimensionality)

class Unset(Dimensionality):
    dimensions = None

class Variable(Dimensionality):
    dimensions = None

class Dimensionless(Dimensionality):
    dimensions = _DimensionlessUC

class Normal(Dimensionality):
    dimensions = _NormalUC

class Length(Dimensionality):
    dimensions = _LengthUC

class Mass(Dimensionality):
    dimensions = _MassUC

class Time(Dimensionality):
    dimensions = _TimeUC

class Temperature(Dimensionality):
    _distinct = True
    dimensions = _TemperatureUC

class TemperatureDifference(Dimensionality):
    dimensions = _TemperatureUC

class Substance(Dimensionality):
    dimensions = _SubstanceUC

class Current(Dimensionality):
    dimensions = _CurrentUC

class Luminosity(Dimensionality):
    dimensions = _LuminosityUC
_AreaUC = _LengthUC ** 2
_VolumeUC = _LengthUC ** 3
_NormalVolumeUC = _VolumeUC * _NormalUC
_PressureUC = _MassUC / _LengthUC / _TimeUC ** 2
_MassFlowUC = _MassUC / _TimeUC
_VolumeFlowUC = _VolumeUC / _TimeUC
_NormalVolumeFlowUC = _NormalVolumeUC / _TimeUC
_DensityUC = _MassUC / _VolumeUC
_SpecificVolumeUC = 1 / _DensityUC
_EnergyUC = _MassUC * _LengthUC ** 2 / _TimeUC ** 2
_PowerUC = _EnergyUC / _TimeUC
_VelocityUC = _LengthUC / _TimeUC
_DynamicViscosityUC = _MassUC / _LengthUC / _TimeUC
_KinematicViscosityUC = _LengthUC ** 2 / _TimeUC
_FrequencyUC = 1 / _TimeUC
_MolarMassUC = _MassUC / _SubstanceUC
_MolarDensityUC = _SubstanceUC / _VolumeUC
_CurrencyPerEnergyUC = _CurrencyUC / _EnergyUC
_CurrencyPerMassUC = _CurrencyUC / _MassUC
_CurrencyPerVolumeUC = _CurrencyUC / _VolumeUC
_CurrencyPerTimeUC = _CurrencyUC / _TimeUC
_PowerPerLengthUC = _PowerUC / _LengthUC
_PowerPerAreaUC = _PowerUC / _AreaUC
_PowerPerVolumeUC = _PowerUC / _VolumeUC
_PowerPerTemperatureC = _PowerUC / _TemperatureUC
_ThermalConductivityUC = _PowerUC / _LengthUC / _TemperatureUC
_HeatTransferCoefficientUC = _PowerUC / _AreaUC / _TemperatureUC
_MassPerNormalVolumeUC = _MassUC / _NormalVolumeUC
_MassPerEnergyUC = _MassUC / _EnergyUC
_MolarSpecificEntropyUC = _EnergyUC / _TemperatureUC / _SubstanceUC

class Area(Dimensionality):
    dimensions = _AreaUC

class Volume(Dimensionality):
    dimensions = _VolumeUC

class NormalVolume(Dimensionality):
    dimensions = _NormalVolumeUC

class Pressure(Dimensionality):
    dimensions = _PressureUC

class MassFlow(Dimensionality):
    dimensions = _MassFlowUC

class VolumeFlow(Dimensionality):
    dimensions = _VolumeFlowUC

class NormalVolumeFlow(Dimensionality):
    dimensions = _NormalVolumeFlowUC

class Density(Dimensionality):
    dimensions = _DensityUC

class SpecificVolume(Dimensionality):
    dimensions = _SpecificVolumeUC

class Energy(Dimensionality):
    dimensions = _EnergyUC

class Power(Dimensionality):
    dimensions = _PowerUC

class Velocity(Dimensionality):
    dimensions = _VelocityUC

class DynamicViscosity(Dimensionality):
    dimensions = _DynamicViscosityUC

class KinematicViscosity(Dimensionality):
    dimensions = _KinematicViscosityUC

class Frequency(Dimensionality):
    dimensions = _FrequencyUC

class MolarMass(Dimensionality):
    dimensions = _MolarMassUC

class SubstancePerMass(Dimensionality):
    dimensions = 1 / _MolarMassUC

class MolarDensity(Dimensionality):
    dimensions = _MolarDensityUC

class Currency(Dimensionality):
    dimensions = _CurrencyUC

class CurrencyPerEnergy(Dimensionality):
    dimensions = _CurrencyPerEnergyUC

class CurrencyPerMass(Dimensionality):
    dimensions = _CurrencyPerMassUC

class CurrencyPerVolume(Dimensionality):
    dimensions = _CurrencyPerVolumeUC

class CurrencyPerTime(Dimensionality):
    dimensions = _CurrencyPerTimeUC

class PowerPerLength(Dimensionality):
    dimensions = _PowerPerLengthUC

class PowerPerArea(Dimensionality):
    dimensions = _PowerPerAreaUC

class PowerPerVolume(Dimensionality):
    dimensions = _PowerPerVolumeUC

class PowerPerTemperature(Dimensionality):
    dimensions = _PowerPerTemperatureC

class ThermalConductivity(Dimensionality):
    dimensions = _ThermalConductivityUC

class HeatTransferCoefficient(Dimensionality):
    dimensions = _HeatTransferCoefficientUC

class MassPerNormalVolume(Dimensionality):
    dimensions = _MassPerNormalVolumeUC

class MassPerEnergy(Dimensionality):
    dimensions = _MassPerEnergyUC

class MolarSpecificEntropy(Dimensionality):
    dimensions = _MolarSpecificEntropyUC

class NormalVolumePerMass(Dimensionality):
    dimensions = 1 / _MassPerNormalVolumeUC

class NormalTemperature(Dimensionality):
    dimensions = _TemperatureUC * _NormalUC

class EnergyPerMass(Dimensionality):
    _distinct = True
    dimensions = _EnergyUC / _MassUC

class HeatingValue(Dimensionality):
    dimensions = _EnergyUC / _MassUC

class LowerHeatingValue(Dimensionality):
    dimensions = _EnergyUC / _MassUC

class HigherHeatingValue(Dimensionality):
    dimensions = _EnergyUC / _MassUC

class SpecificEnthalpy(Dimensionality):
    dimensions = _EnergyUC / _MassUC

class SpecificInternalEnergy(Dimensionality):
    dimensions = _EnergyUC / _MassUC

class MolarSpecificEnthalpy(Dimensionality):
    _distinct = True
    dimensions = _EnergyUC / _SubstanceUC

class MolarSpecificInternalEnergy(Dimensionality):
    dimensions = _EnergyUC / _SubstanceUC

class SpecificHeatCapacity(Dimensionality):
    _distinct = True
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class SpecificEntropy(Dimensionality):
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class IndistinctDimensionality(Dimensionality):
    _intermediate = True
    _distinct = False

class SpecificHeatPerDryAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class SpecificHeatPerHumidAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class MixtureEnthalpyPerDryAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC

class MixtureEnthalpyPerHumidAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC

class MixtureEntropyPerDryAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class MixtureEntropyPerHumidAir(IndistinctDimensionality):
    dimensions = _EnergyUC / _MassUC / _TemperatureUC

class MixtureVolumePerDryAir(IndistinctDimensionality):
    dimensions = _VolumeUC / _MassUC

class MixtureVolumePerHumidAir(IndistinctDimensionality):
    dimensions = _VolumeUC / _MassUC