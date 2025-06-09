from datetime import datetime
from typing import List, Optional, Sequence, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field, validator
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.primitive_datatypes import Code, time
from fhirkit.elements import CodeableConcept, Identifier, Period, Quantity, Range, Ratio, Reference, BackboneElement
ValueType = Union[str, Quantity, int, CodeableConcept, bool, Range, Ratio, time, datetime, Period]
ObservationStatus = Literal['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'enterred-in-error', 'unknown']

class ObservationComponent(BackboneElement):
    code: CodeableConcept
    valueString: Optional[str] = Field(None, exclude=True)
    valueQuantity: Optional[Quantity] = Field(None, exclude=True)
    valueInteger: Optional[int] = Field(None, exclude=True)
    valueCodeableConcept: Optional[CodeableConcept] = Field(None, exclude=True)
    valueBoolean: Optional[bool] = Field(None, exclude=True)
    valueRatio: Optional[Ratio] = Field(None, exclude=True)
    valueTime: Optional[time] = Field(None, exclude=True)
    valueDateTime: Optional[datetime] = Field(None, exclude=True)
    valuePeriod: Optional[Period] = Field(None, exclude=True)
    value: Optional[ValueType] = ChoiceType(None)

    @validator('value', pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)

class Observation(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal['Observation'] = Field('Observation', const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    partOf: Optional[List[Reference]] = Field([], repr=True)
    status: ObservationStatus = Field('final', repr=True)
    category: Optional[Sequence[CodeableConcept]] = Field([], repr=True)
    code: CodeableConcept = Field(..., repr=True)
    subject: Optional[Reference]
    encounter: Optional[Reference]
    effectivePeriod: Optional[Period] = Field(None, exclude=True)
    effectiveDateTime: Optional[datetime] = Field(None, exclude=True)
    effective: Union[datetime, Period, str] = ChoiceType(None)
    performer: Optional[Reference]
    valueString: Optional[str] = Field(None, exclude=True)
    valueQuantity: Optional[Quantity] = Field(None, exclude=True)
    valueInteger: Optional[int] = Field(None, exclude=True)
    valueCodeableConcept: Optional[CodeableConcept] = Field(None, exclude=True)
    valueBoolean: Optional[bool] = Field(None, exclude=True)
    valueRatio: Optional[Ratio] = Field(None, exclude=True)
    valueTime: Optional[time] = Field(None, exclude=True)
    valueDateTime: Optional[datetime] = Field(None, exclude=True)
    valuePeriod: Optional[Period] = Field(None, exclude=True)
    value: Optional[ValueType] = ChoiceType(None)
    method: Optional[Code] = Field(None, repr=False)
    derivedFrom: Optional[Reference]
    component: List[ObservationComponent] = Field([], repr=True)

    @validator('value', pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)

    @validator('effective', pre=True, always=True)
    def validate_effective(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)