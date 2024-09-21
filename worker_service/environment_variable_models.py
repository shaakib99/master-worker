from pydantic import BaseModel
from typing import Optional

class EnvironmentVariableModel(BaseModel):
    id: Optional[int] = None
    worker_id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True

class CreateEnvironmentVariableModel(BaseModel):
    worker_id: Optional[int] = None
    name: str
    value: str