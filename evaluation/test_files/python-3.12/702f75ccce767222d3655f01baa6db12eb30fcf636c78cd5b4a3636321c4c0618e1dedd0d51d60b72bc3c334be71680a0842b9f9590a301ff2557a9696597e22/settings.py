from typing import Optional
import strawberry
from strawberry.scalars import JSON
from orchestrator.graphql.schemas.errors import Error
from orchestrator.schemas import WorkerStatus
from orchestrator.schemas.engine_settings import EngineSettingsSchema
CACHE_FLUSH_OPTIONS: dict[str, str] = {'all': 'All caches'}

@strawberry.experimental.pydantic.type(model=WorkerStatus, all_fields=True)
class WorkerStatusType:
    pass

@strawberry.experimental.pydantic.type(model=EngineSettingsSchema, all_fields=True)
class EngineSettingsType:
    pass

@strawberry.type
class StatusType:
    engine_settings: Optional[EngineSettingsType]
    worker_status: Optional[WorkerStatusType]
    cache_names: Optional[JSON]

@strawberry.type
class CacheClearSuccess:
    deleted: int
CacheClearResponse = strawberry.union('CacheClearResponse', types=(CacheClearSuccess, Error))
StatusUpdateResponse = strawberry.union('StatusUpdateResponse', types=(EngineSettingsType, Error))