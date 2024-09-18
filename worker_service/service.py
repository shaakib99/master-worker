from database_service.service import DatabaseService
from worker_service.schemas import WorkerSchema

class WorkerService:
    def __init__(self, worker_model = DatabaseService(WorkerSchema)):
        self.worker_model = worker_model