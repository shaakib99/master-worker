from fastapi import APIRouter, Depends
from master_service.service import MasterService
from master_service.models import CreateWorkerModel
from typing import Annotated

router = APIRouter(
    prefix="/master",
    tags=["master"],
    responses={
        404: {"description": "Not found"}, 
        500: {"description": "Internal Server Error"}, 
        401: {"description": "Unauthorized"}, 
        403: {"description": "Forbidden"},
        200: {"description": "OK"},
        201: {"description": "Created"},
        202: {"description": "Accepted"},
        204: {"description": "No Content"}
    },
)


@router.post("/create-worker", status_code=201)
async def create_worker(data: CreateWorkerModel, master_service: Annotated[MasterService, Depends(lambda: MasterService())]):
    return await master_service.create_worker(data)

@router.post('/{worker_id}/create-port', status_code=201)
async def create_port(worker_id: str, data, master_service: Annotated[MasterService, Depends(lambda: MasterService())]):
    return await master_service.create_port(worker_id, data)

@router.post('/{worker_id}/create-environment-variable', status_code=201)
async def create_environment_variable(worker_id: str, data, master_service: Annotated[MasterService, Depends(lambda: MasterService())]):
    return await master_service.create_environment_variable(worker_id, data)

@router.patch('/{worker_id}', status_code=202)
async def update_worker(worker_id: str, data, master_service: Annotated[MasterService, Depends(lambda: MasterService())]):
    return await master_service.update_worker(worker_id, data)