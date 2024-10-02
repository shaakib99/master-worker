from pydantic import BaseModel

class CommonLabels(BaseModel):
    alertname: str
    instance: str
    job: str
    type: str
    worker_info: dict

class PrometheusCreateWorkerModel(BaseModel):
    commonLabels: CommonLabels

