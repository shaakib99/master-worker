from pydantic import BaseModel
from typing import Optional
from worker_service.models import CreatePortModel, CreateEnvironmentVariableModel

class CreateWorkerModel(BaseModel):
    docker_image_name: Optional[str] = None
    ports: Optional[list[CreatePortModel]] = []
    environment_variables: Optional[list[CreateEnvironmentVariableModel]] = []