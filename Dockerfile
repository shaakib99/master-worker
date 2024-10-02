FROM ubuntu:latest

WORKDIR /app

COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    openssh-server \ 
    prometheus \
    prometheus-alertmanager \
    docker \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# Setup prometheus
COPY ./master_service/prometheus/*.yml /etc/prometheus/
COPY ./master_service/prometheus/*.json /etc/prometheus/

RUN systemctl restart prometheus

# Setup alertmanager
RUN systemctl restart prometheus-alertmanager

# Setup targets.json
RUN chown prometheus:prometheus /etc/prometheus/targets.json

# Setup SSH
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN /usr/sbin/sshd -D


# Install Python requirements
RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "main.py"]