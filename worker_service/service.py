from database_service.service import DatabaseService
from worker_service.schemas import WorkerSchema, PortsSchema, EnvironmentVariablesSchema
from worker_service.models import WorkerModel, PortModel, EnvironmentVariableModel

class WorkerService:
    def __init__(self, worker_model = DatabaseService[WorkerSchema](WorkerSchema)):
        self.worker_model = worker_model
    
    async def createOne(self, data: WorkerModel):
        return await self.worker_model.createOne(data)


class PortService:
    def __init__(self, port_model = DatabaseService(PortsSchema)):
        self.port_model = port_model
    
    async def createOne(self, data: PortModel):
        return await self.port_model.createOne(data)

class EnvironmentVariableService:
    def __init__(self, environment_variable_model = DatabaseService(EnvironmentVariablesSchema)):
        self.environment_variable_model = environment_variable_model
    
    async def createOne(self, data: EnvironmentVariableModel):
        return await self.environment_variable_model.createOne(data)