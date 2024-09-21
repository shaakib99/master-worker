from fastapi import APIRouter, Depends
from worker_service.service import WorkerService
from typing import Annotated
from worker_service.models import CreateWorkerModel

router = APIRouter(
    prefix="/workers",
    tags=["worker"],
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

@router.post("", status_code=201)
async def create_worker(data: CreateWorkerModel, worker_service: Annotated[WorkerService, Depends(lambda: WorkerService())]):
    return await worker_service.createOne(data)

@router.get("/{id}", status_code=200)
async def getOne(id: int, worker_service: Annotated[WorkerService, Depends(lambda: WorkerService())]):
    return await worker_service.getOne(id)

@router.delete("/{id}", status_code=200)
async def deleteOne(id: int, worker_service: Annotated[WorkerService, Depends(lambda: WorkerService())]):
    return await worker_service.deleteOne(id)