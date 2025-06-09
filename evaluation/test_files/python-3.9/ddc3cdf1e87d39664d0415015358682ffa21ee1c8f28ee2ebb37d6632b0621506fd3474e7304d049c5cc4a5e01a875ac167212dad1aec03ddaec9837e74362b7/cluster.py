from typing import List, Dict, Optional, Any, Union
from uuid import UUID
import pydantic
from pydantic import Field
from bodosdk.models.base import ClusterStatus, CamelCaseBase

class InstanceType(CamelCaseBase):
    name: str
    vcpus: int
    cores: int
    memory: int
    efa: Optional[bool] = None
    accelerated_networking: Optional[bool] = Field(None, alias='acceleratedNetworking')

class InstanceCategory(pydantic.BaseModel):
    name: str
    instance_types: Dict[str, InstanceType]

class BodoImage(pydantic.BaseModel):
    image_id: str
    bodo_version: str

class ClusterMetadata(pydantic.BaseModel):
    name: str
    uuid: str
    status: ClusterStatus
    description: str

class ClusterDefinition(CamelCaseBase):
    name: str
    instance_type: str = Field(..., alias='instanceType')
    workers_quantity: int = Field(..., alias='workersQuantity')
    auto_shutdown: Optional[int] = Field(0, alias='autoShutdown')
    auto_pause: Optional[int] = Field(60, alias='autoPause')
    image_id: Optional[str] = Field(None, alias='imageId')
    bodo_version: str = Field(..., alias='bodoVersion')
    description: Optional[str] = None
    accelerated_networking: Optional[bool] = Field(False, alias='acceleratedNetworking')
    is_job_dedicated: Optional[bool] = Field(False, alias='isJobDedicated')
    availability_zone: Optional[str] = Field(None, alias='availabilityZone')
    aws_deployment_subnet_id: Optional[str] = Field(None, alias='awsDeploymentSubnetId')
    instance_role_uuid: Optional[str] = Field(None, alias='instanceRoleUUID')

class ClusterResponse(CamelCaseBase):
    name: str
    uuid: Union[str, UUID]
    status: ClusterStatus
    description: Optional[str] = ''
    instance_type: str = Field(..., alias='instanceType')
    workers_quantity: int = Field(..., alias='workersQuantity')
    auto_shutdown: Optional[int] = Field(None, alias='autoShutdown')
    auto_pause: Optional[int] = Field(None, alias='autoPause')
    nodes_ip: Optional[List[str]] = Field(None, alias='nodesIp')
    bodo_version: Optional[str] = Field(None, alias='bodoVersion')
    image_id: str = Field(..., alias='imageId')
    cores_per_worker: Optional[int] = Field(None, alias='coresPerWorker')
    accelerated_networking: bool = Field(..., alias='acceleratedNetworking')
    autoscaling_identifier: Optional[str] = Field(None, alias='autoscalingIdentifier')
    last_asg_activity_id: Optional[str] = Field(None, alias='lastAsgActivityId')
    created_at: str = Field(..., alias='createdAt')
    is_job_dedicated: bool = Field(..., alias='isJobDedicated')
    last_known_activity: Optional[str] = Field(None, alias='lastKnownActivity')
    node_metadata: Optional[object] = Field(None, alias='nodeMetadata')
    asg_metadata: Optional[object] = Field(None, alias='asgMetadata')
    workspace: Any

class ClusterTaskInfo(CamelCaseBase):
    uuid: str
    status: str
    task_type: str = Field(..., alias='taskType')
    logs: str

class ScaleCluster(CamelCaseBase):
    uuid: Union[str, UUID]
    workers_quantity: int = Field(..., alias='workersQuantity')