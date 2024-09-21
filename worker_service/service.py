from database_service.service import DatabaseService
from worker_service.schemas import WorkerSchema, PortsSchema, EnvironmentVariablesSchema
from worker_service.port_service import PortService
from worker_service.environment_variable_service import EnvironmentVariableService
from worker_service.models import WorkerModel, CreateWorkerModel
from worker_service.port_models import CreatePortModel
from worker_service.environment_variable_models import CreateEnvironmentVariableModel
from database_service.models.query_param import QueryParamsModel
from common.utils import create_docker_container, update_nginx_upstream_config, remove_docker_container
import uuid
import os

class WorkerService:
    def __init__(self, worker_model = DatabaseService[WorkerSchema](WorkerSchema), port_service = PortService(), environment_variable_service = EnvironmentVariableService()):
        self.worker_model = worker_model
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
    
    async def createOne(self, data: CreateWorkerModel):
        unique_id = str(uuid.uuid4())
        ports: list[PortsSchema] = []
        environment_variables: list[EnvironmentVariablesSchema] = []

        worker = WorkerModel(image_name=data.docker_image_name, unique_id = unique_id, status='INIT', host_ip='127.0.0.1')

        worker_data =  await self.worker_model.createOne(worker)

        for port in [*data.ports, CreatePortModel(port=22, should_add_to_load_balancer=False)]:
            port.worker_id = worker_data.id
            port_data = await self.port_service.createOne(port)
            ports.append(port_data)
        
        for env_var in [*data.environment_variables, CreateEnvironmentVariableModel(name='WORKER_ID', value=unique_id)]:
            env_var.worker_id = worker_data.id
            env_var_data = await self.environment_variable_service.createOne(env_var)
            environment_variables.append(env_var_data)
        
        # create docker container
        is_worker_created = await create_docker_container(
            data.docker_image_name, 
            f'worker-{unique_id}', 
            [ f'{port.mapped_port}:{port.port}' for port in ports ], 
            [ f'{env_var.name}={env_var.value}' for env_var in environment_variables ]
            )
        
        if is_worker_created is False:
            return {"message": "worker creation failed"}
        
        for port in ports:
            if port.should_add_to_load_balancer:
                commnad = f'ansible-playbook -i inventory master_service/ansible/inventories/add_server_upstream.yaml -e child_server="localhost:{port.mapped_port}" -e host_root_password={os.getenv("HOST_ROOT_PASSWORD")}'
                await update_nginx_upstream_config(commnad)
        
        return WorkerModel.model_validate(worker_data)

    async def getOne(self, id: int):
        return await self.worker_model.getOne(id)
    
    async def deleteOne(self, id: int):
        worker_data = await self.getOne(id)
        port_query = QueryParamsModel()
        port_query.filter_by = f'worker_id = {worker_data.id}'
        ports = await self.port_service.getAll(port_query)
        for port in ports:
            if port.should_add_to_load_balancer:
                commnad = f'ansible-playbook -i inventory master_service/ansible/inventories/remove_server_upstream.yaml -e child_server="localhost:{port.mapped_port}" -e host_root_password={os.getenv("HOST_ROOT_PASSWORD")}'
                await update_nginx_upstream_config(commnad)

        await remove_docker_container(f'worker-{worker_data.unique_id}')
        return await self.worker_model.deleteOne(id)