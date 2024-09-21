from worker_service.models import WorkerModel, PortModel, EnvironmentVariableModel
from worker_service.service import WorkerService, PortService, EnvironmentVariableService
from master_service.models import CreateWorkerModel
from common.utils import get_open_port, create_docker_container, update_nginx_upstream_config
import uuid
import os

class MasterService:
    def __init__(self, worker_service = WorkerService(), port_service = PortService(), environment_variable_service = EnvironmentVariableService()):
        self.master_model = None
        self.worker_service = worker_service
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
    
    async def create_worker(self, data: CreateWorkerModel):
        unique_id = str(uuid.uuid4())
        ports: list[PortModel] = []
        environment_variables: list[EnvironmentVariableModel] = []

        for port in data.ports:
            ports.append(PortModel(port = port.port, mapped_port = await get_open_port(), should_add_to_load_balancer = port.should_add_to_load_balancer, is_active = True))
        
        # default ssh port
        ports.append(PortModel(port = 22, mapped_port = await get_open_port(), is_active = True))

        for environment_variable in data.environment_variables:
            environment_variables.append(EnvironmentVariableModel(name = environment_variable.name, value = environment_variable.value))

        # default environment variable is worker_id
        environment_variables.append(EnvironmentVariableModel(name = "WORKER_ID", value = unique_id))
        
        worker = WorkerModel(image_name=data.docker_image_name, unique_id = unique_id, status='INIT', host_ip='127.0.0.1')

        # create docker container
        is_worker_created = await create_docker_container(
            data.docker_image_name, 
            f'worker-{unique_id}', 
            [ f'{port.mapped_port}:{port.port}' for port in ports ], 
            [ f'{env_var.name}={env_var.value}' for env_var in environment_variables ]
            )

        if is_worker_created is False:
            return {"message": "worker creation failed"}

        worker_data = await self.worker_service.createOne(worker)

        for port in ports:
            port.worker_id = worker.id
            await self.port_service.createOne(port)
        
        for env_var in environment_variables:
            env_var.worker_id = worker.id
            await self.environment_variable_service.createOne(env_var)
        
        for port in ports:
            if port.should_add_to_load_balancer:
                commnad = f'ansible-playbook -i inventory master_service/ansible/inventories/add_server_upstream.yaml -e child_server="localhost:{port.mapped_port}" -e host_root_password={os.getenv("HOST_ROOT_PASSWORD")}'
                await update_nginx_upstream_config(commnad)
        
        return WorkerModel.model_validate(worker_data)
    
    async def update_worker(self, id: str, data):
        return await self.worker_service.updateOne(id, data)
    
    async def create_port(self, worker_id: str, data):
        return await self.port_service.createOne(PortModel(worker_id = worker_id, **data))
    
    async def create_environment_variable(self, worker_id: str, data):
        return await self.environment_variable_service.createOne(EnvironmentVariableModel(worker_id = worker_id, **data))
    async def update_port(self, id: str, data):
        return await self.port_service.updateOne(id, data)

    async def update_environment_variable(self, id: str, data):
        return await self.environment_variable_service.updateOne(id, data)
    
    async def build_image_and_create_worker(self, data):
        pass