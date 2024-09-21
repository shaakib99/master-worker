from database_service.service import DatabaseService
from worker_service.models import PortModel
from worker_service.schemas import PortsSchema

class PortService:
    def __init__(self, port_model = DatabaseService(PortsSchema)):
        self.port_model = port_model
    
    async def createOne(self, data: PortModel):
        return await self.port_model.createOne(data)