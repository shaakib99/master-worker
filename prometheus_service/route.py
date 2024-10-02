from fastapi import APIRouter, Depends
from typing import Annotated
from prometheus_service.service import PrometheusService
from prometheus_service.models import PrometheusCreateWorkerModel

router = APIRouter(
    prefix="/prometheus",
    tags=["prometheus"],
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

@router.post("/create")
async def create_worker(data: PrometheusCreateWorkerModel, prometheus_service: Annotated[PrometheusService, Depends(lambda: PrometheusService())]):
    return await prometheus_service.create_worker(data)