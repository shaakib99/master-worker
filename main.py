from fastapi import FastAPI, Response
from dotenv import load_dotenv
from master_service.route import router as master_router
from worker_service.route import router as worker_router
from prometheus_service.route import router as prometheus_router
from database_service.service import DatabaseService
from master_service.prometheus.scrape_data import generate_data

async def lifespan(app):
    load_dotenv()
    DatabaseService(None).connect()
    yield

app = FastAPI(lifespan=lifespan)

routers = [master_router, worker_router, prometheus_router]

for router in routers:
    app.include_router(router)

@app.get("/metrics")
async def metrics():
    return Response(content=generate_data(), media_type="text/plain")