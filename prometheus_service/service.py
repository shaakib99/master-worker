from worker_service.service import WorkerService
from worker_service.environment_variable_service import EnvironmentVariableService
from worker_service.port_models import CreatePortModel
from worker_service.environment_variable_models import CreateEnvironmentVariableModel
from prometheus_service.models import PrometheusCreateWorkerModel
from worker_service.models import CreateWorkerModel
from worker_service.port_service import PortService
from database_service.models.query_param import QueryParamsModel
from fastapi import HTTPException

class PrometheusService():
    def __init__(self, worker_service = WorkerService(), port_service = PortService(), environment_variable_service = EnvironmentVariableService()) -> None:
        self.worker_service = worker_service
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
    
    async def create_worker(self, data: PrometheusCreateWorkerModel):
        worker = await self.worker_service.getAll(QueryParamsModel(filter_by=f'unique_id = "{data.worker_id}"', limit=1))

        if len(worker) == 0:
            raise HTTPException(status_code=404, detail="worker not found")

        worker = worker[0]

        ports = await self.port_service.getAll(QueryParamsModel(filter_by=f"worker_id = {worker.id} and should_add_to_load_balancer = true"))
        environment_variables = await self.environment_variable_service.getAll(QueryParamsModel(filter_by=f"worker_id = {worker.id}"))
        

        create_port_models = []
        create_environment_variable_models = []

        for port in ports:
            create_port_models.append(CreatePortModel(
                worker_id=port.worker_id,
                port=port.port,
                should_add_to_load_balancer=port.should_add_to_load_balancer
            ))
        
        for environment_variable in environment_variables:
            create_environment_variable_models.append(CreateEnvironmentVariableModel(
                worker_id=environment_variable.worker_id,
                name=environment_variable.name,
                value=environment_variable.value
            ))

        new_worker = CreateWorkerModel(
            docker_image_name=worker.image_name,
            ports=create_port_models,
            environment_variables=create_environment_variable_models
        )

        return await self.worker_service.createOne(new_worker)