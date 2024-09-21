FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    python3-pip \
    openssh-server \ 
    docker \
    ansible \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "main.py"]