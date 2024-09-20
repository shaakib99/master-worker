FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3-pip \
    openssh-server \ 
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd

WORKDIR /app

RUN echo 'root:root' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

CMD ["/usr/sbin/sshd", "-D"]