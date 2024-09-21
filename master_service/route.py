from fastapi import APIRouter

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