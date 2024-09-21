import subprocess
import socket

async def create_docker_container(image_name: str, container_name: str,  ports_map: list[str] = [], environment_variable_map: list[str] = []):
    try:
        command = f'docker run -it -d --name={container_name}'

        for port in ports_map:
            command += f' -p {port} '
        
        for env_var in environment_variable_map:
            command += f' -e {env_var} '

        command += image_name
        print(f'running command: {command}')
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

async def get_open_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port