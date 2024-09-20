from fastapi import FastAPI
from dotenv import load_dotenv
from master_service.route import router as master_router

async def lifespan(app):
    load_dotenv()
    yield

app = FastAPI(lifespan=lifespan)

routers = [master_router]

for router in routers:
    app.include_router(router)
