from pydantic import BaseModel
from typing import Optional

class PortModel(BaseModel):
    id: Optional[int] = None
    worker_id: Optional[int] = None
    port: Optional[int] = None
    mapped_port: Optional[int] = None
    should_add_to_load_balancer: Optional[bool] = False
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True

class CreatePortModel(BaseModel):
    worker_id: Optional[int] = None
    port: int
    should_add_to_load_balancer: bool = False
    update_prometheus_config: bool = False