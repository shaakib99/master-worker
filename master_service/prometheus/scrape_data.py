from prometheus_client import Counter, Gauge, generate_latest
import psutil

request_counter = Counter('request_counter', 'request counter')
cpu_usage = Gauge('cpu_usage', 'cpu usage')
ram_usage = Gauge('ram_usage', 'ram usage')
storage_usage = Gauge('storage_usage', 'storage usage')

def generate_data():
    request_counter.inc()
    cpu_usage.set(psutil.cpu_percent())
    ram_usage.set(psutil.virtual_memory().percent)
    storage_usage.set(psutil.disk_usage('/').percent)
    return generate_latest()