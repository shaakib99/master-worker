from database_service.service import DatabaseService
from worker_service.models import PortModel, CreatePortModel
from worker_service.schemas import PortsSchema
from common.utils import get_open_port

class PortService:
    def __init__(self, port_model = DatabaseService[PortsSchema](PortsSchema)):
        self.port_model = port_model
    
    async def createOne(self, data: CreatePortModel):
        port_model = PortModel(worker_id=data.worker_id, port=data.port, mapped_port=await get_open_port(), should_add_to_load_balancer=data.should_add_to_load_balancer, is_active=True)
        return await self.port_model.createOne(port_model)