from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.infiec61968.infcommon.ratio import Ratio
__all__ = ['CurrentTransformerInfo']

class CurrentTransformerInfo(AssetInfo):
    """Properties of current transformer asset."""
    accuracy_class: Optional[str] = None
    'CT accuracy classification.'
    accuracy_limit: Optional[float] = None
    'Accuracy limit.'
    core_count: Optional[int] = None
    'Number of cores.'
    ct_class: Optional[str] = None
    'CT classification; i.e. class 10P.'
    knee_point_voltage: Optional[int] = None
    'Maximum voltage in volts across the secondary terminals where the CT still displays linear characteristics.'
    max_ratio: Optional[Ratio] = None
    'Maximum ratio between the primary and secondary current.'
    nominal_ratio: Optional[Ratio] = None
    'Nominal ratio between the primary and secondary current; i.e. 100:5'
    primary_ratio: Optional[float] = None
    'Ratio for the primary winding tap changer (numerator).'
    rated_current: Optional[int] = None
    'Rated current on the primary side in amperes.'
    secondary_fls_rating: Optional[int] = None
    'Full load secondary (FLS) rating for secondary winding in amperes.'
    secondary_ratio: Optional[float] = None
    'Ratio for the secondary winding tap changer (denominator).'
    usage: Optional[str] = None
    'Intended usage of the CT; i.e. metering, protection.'