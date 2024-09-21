from pydantic import BaseModel
from typing import Optional

class WorkerModel(BaseModel):
    id: Optional[int] = None
    image_name: Optional[str] = None
    unique_id: Optional[str] = None
    host_ip: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class PortModel(BaseModel):
    id: Optional[int] = None
    worker_id: Optional[str] = None
    port: Optional[int] = None
    mapped_port: Optional[int] = None
    should_add_to_load_balancer: Optional[bool] = False
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True

class EnvironmentVariableModel(BaseModel):
    id: Optional[str] = None
    worker_id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True


# CRUD
class CreatePortModel(BaseModel):
    port: int
    should_add_to_load_balancer: bool = False

class CreateEnvironmentVariableModel(BaseModel):
    name: str
    value: str

class ResponseWorkerModel(BaseModel):
    id: Optional[str] = None
    unique_id: Optional[str] = None
    host_ip: Optional[str] = None
    status: Optional[str] = None
    ports: Optional[list["PortModel"]] = []
    environment_variables: Optional[list["EnvironmentVariableModel"]] = []
    class Config:
        from_attributes = True