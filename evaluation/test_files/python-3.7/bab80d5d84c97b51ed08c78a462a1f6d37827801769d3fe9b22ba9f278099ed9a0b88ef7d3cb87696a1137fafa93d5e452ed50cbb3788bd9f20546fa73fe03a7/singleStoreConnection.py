from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Extra, Field, SecretStr
from .. import connectionBasicType

class SingleStoreType(Enum):
    SingleStore = 'SingleStore'

class SingleStoreScheme(Enum):
    mysql_pymysql = 'mysql+pymysql'

class SingleStoreConnection(BaseModel):

    class Config:
        extra = Extra.forbid
    type: Optional[SingleStoreType] = Field(SingleStoreType.SingleStore, description='Service Type', title='Service Type')
    scheme: Optional[SingleStoreScheme] = Field(SingleStoreScheme.mysql_pymysql, description='SQLAlchemy driver scheme options.', title='Connection Scheme')
    username: str = Field(..., description='Username to connect to SingleStore. This user should have privileges to read all the metadata in MySQL.', title='Username')
    password: Optional[SecretStr] = Field(None, description='Password to connect to SingleStore.', title='Password')
    hostPort: str = Field(..., description='Host and port of the SingleStore service.', title='Host and Port')
    databaseSchema: Optional[str] = Field(None, description='databaseSchema of the data source. This is optional parameter, if you would like to restrict the metadata reading to a single databaseSchema. When left blank, OpenMetadata Ingestion attempts to scan all the databaseSchema.', title='databaseSchema')
    connectionOptions: Optional[connectionBasicType.ConnectionOptions] = Field(None, title='Connection Options')
    connectionArguments: Optional[connectionBasicType.ConnectionArguments] = Field(None, title='Connection Arguments')
    supportsMetadataExtraction: Optional[connectionBasicType.SupportsMetadataExtraction] = Field(None, title='Supports Metadata Extraction')
    supportsProfiler: Optional[connectionBasicType.SupportsProfiler] = Field(None, title='Supports Profiler')
    supportsQueryComment: Optional[connectionBasicType.SupportsQueryComment] = Field(None, title='Supports Query Comment')