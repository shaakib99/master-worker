from fastapi import FastAPI
from dotenv import load_dotenv
from master_service.route import router as master_router
from database_service.service import DatabaseService

async def lifespan(app):
    load_dotenv()
    DatabaseService(None).connect()
    yield

app = FastAPI(lifespan=lifespan)

routers = [master_router]

for router in routers:
    app.include_router(router)
