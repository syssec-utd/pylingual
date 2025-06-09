from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import AnyUrl, BaseModel, Extra, Field
from .. import connectionBasicType

class DagsterType(Enum):
    Dagster = 'Dagster'

class DagsterConnection(BaseModel):

    class Config:
        extra = Extra.forbid
    type: Optional[DagsterType] = Field(DagsterType.Dagster, description='Service Type', title='Service Type')
    hostPort: AnyUrl = Field(..., description='Pipeline Service Management/UI URI.', title='Host And Port')
    numberOfStatus: Optional[int] = Field('10', description='Pipeline Service Number Of Status')
    supportsMetadataExtraction: Optional[connectionBasicType.SupportsMetadataExtraction] = Field(None, title='Supports Metadata Extraction')