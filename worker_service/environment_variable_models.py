from pydantic import BaseModel
from typing import Optional

class EnvironmentVariableModel(BaseModel):
    id: Optional[str] = None
    worker_id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    is_active: Optional[bool] = None
    class Config:
        from_attributes = True

class CreateEnvironmentVariableModel(BaseModel):
    name: str
    value: str