from database_service.service import DatabaseService
from worker_service.schemas import EnvironmentVariablesSchema
from worker_service.models import EnvironmentVariableModel

class EnvironmentVariableService:
    def __init__(self, environment_variable_model = DatabaseService(EnvironmentVariablesSchema)):
        self.environment_variable_model = environment_variable_model
    
    async def createOne(self, data: EnvironmentVariableModel):
        return await self.environment_variable_model.createOne(data)