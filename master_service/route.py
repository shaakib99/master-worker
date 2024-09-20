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


@router.post("/create/worker", status_code=201)
async def create_worker(data: CreateWorkerModel, master_service: Annotated[MasterService, Depends(lambda: MasterService())]):
    return await master_service.create_worker(data)