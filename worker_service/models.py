from pydantic import BaseModel
from typing import Optional
from worker_service.port_models import PortModel, CreatePortModel
from worker_service.environment_variable_models import EnvironmentVariableModel, CreateEnvironmentVariableModel

class WorkerModel(BaseModel):
    id: Optional[int] = None
    image_name: Optional[str] = None
    unique_id: Optional[str] = None
    host_ip: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class CreateWorkerModel(BaseModel):
    docker_image_name: Optional[str] = None
    ports: Optional[list[CreatePortModel]] = []
    environment_variables: Optional[list[CreateEnvironmentVariableModel]] = []

class ResponseWorkerModel(BaseModel):
    id: Optional[str] = None
    unique_id: Optional[str] = None
    host_ip: Optional[str] = None
    status: Optional[str] = None
    ports: Optional[list["PortModel"]] = []
    environment_variables: Optional[list["EnvironmentVariableModel"]] = []
    class Config:
        from_attributes = True