from worker_service.service import WorkerService, PortService, EnvironmentVariableService

class MasterService:
    def __init__(self, worker_service = WorkerService(), port_service = PortService(), environment_variable_service = EnvironmentVariableService()):
        self.master_model = None
        self.worker_service = worker_service
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
    
    async def createOne(self, data):
        pass

    async def build_image_and_create_worker(self, data):
        pass