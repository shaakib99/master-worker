from pydantic import BaseModel
from typing import Optional

class WorkerModel(BaseModel):
    id: Optional[str] = None
    class Config:
        from_attributes = True