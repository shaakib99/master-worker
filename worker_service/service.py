from database_service.service import DatabaseService
from worker_service.schemas import WorkerSchema
from worker_service.port_service import PortService
from worker_service.environment_variable_service import EnvironmentVariableService
from worker_service.models import WorkerModel, PortModel, EnvironmentVariableModel, CreateWorkerModel
from common.utils import get_open_port, create_docker_container, update_nginx_upstream_config
import uuid
import os

class WorkerService:
    def __init__(self, worker_model = DatabaseService[WorkerSchema](WorkerSchema), port_service = PortService(), environment_variable_service = EnvironmentVariableService()):
        self.worker_model = worker_model
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
    
    async def createOne(self, data: CreateWorkerModel):
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

        worker_data =  await self.worker_model.createOne(worker)

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

    async def getOne(self, id: int):
        return await self.worker_model.getOne(id)