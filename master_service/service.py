# from worker_service.service import WorkerService
from worker_service.models import WorkerModel, PortModel, EnvironmentVariableModel
from master_service.models import CreateWorkerModel
from common.utils import get_open_port, create_docker_container
import uuid

class MasterService:
    def __init__(self, worker_service = None):
        self.master_model = None
        self.worker_model = worker_service
    
    async def create_worker(self, data: CreateWorkerModel):
        unique_id = str(uuid.uuid4())
        ports: list[PortModel] = []
        environment_variables: list[EnvironmentVariableModel] = []

        for port in data.ports:
            ports.append(PortModel(port = port.port, mapped_port = await get_open_port(), is_active = True))
        
        # default ssh port
        ports.append(PortModel(port = 22, mapped_port = await get_open_port(), is_active = True))

        for environment_variable in data.environment_variables:
            environment_variables.append(EnvironmentVariableModel(name = environment_variable.name, value = environment_variable.value))

        # default environment variable is worker_id
        environment_variables.append(EnvironmentVariableModel(name = "WORKER_ID", value = unique_id))
        
        worker = WorkerModel(unique_id = unique_id, status='INIT', host_ip='127.0.0.1')

        # create docker container
        is_worker_created = await create_docker_container(
            data.docker_image_name, 
            f'worker-{unique_id}', 
            [ f'{port.port}:{port.mapped_port}' for port in ports ], 
            [ f'{env_var.name}={env_var.value}' for env_var in environment_variables ]
            )

        if is_worker_created is False:
            return {"message": "worker creation failed"}

        worker = self.worker_model.createOne(worker)

        for port in ports:
            port.worker_id = worker.id
            self.worker_model.createOne(port)
        
        for env_var in environment_variables:
            env_var.worker_id = worker.id
            self.worker_model.createOne(env_var)
        
        return worker