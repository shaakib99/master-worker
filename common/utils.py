import subprocess
import socket
import json

async def create_docker_container(image_name: str, container_name: str,  ports_map: list[str] = [], environment_variable_map: list[str] = []):
    try:
        command = f'docker run -it -d --name={container_name} --memory="512m" --cpus="1" -v /var/run/docker.sock:/var/run/docker.sock'

        for port in ports_map:
            command += f' -p {port} '
        
        for env_var in environment_variable_map:
            command += f' -e {env_var} '

        command += image_name
        subprocess.run(command, shell=True)
        return True
    except Exception as e:
        print(e)
        return False

async def remove_docker_container(container_name: str):
    try:
        command = f'docker rm -f {container_name}'
        subprocess.run(command, shell=True)
        return True
    except Exception as e:
        print(e)
        return False
    
async def update_nginx_upstream_config(command: str):
    try:
        subprocess.run(command, shell=True)
        return True
    except Exception as e:
        print(e)
        return False

async def add_observer_prometheus_config(target: str):
    file_path = '/etc/prometheus/targets.json'
    try:
        data = []
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        data[0]['targets'].append(target)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(e)
        return False

async def remove_observer_prometheus_config(target: str):
    file_path = '/etc/prometheus/targets.json'
    try:
        data = []
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        data[0]['targets'].remove(target)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(e)
        return False
    
async def get_open_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port