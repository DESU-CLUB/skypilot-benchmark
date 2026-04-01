FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: inspect operation log and recover deleted branch commits using op restore"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN mkdir -p /home/user/proj

RUN jj git init /home/user/proj

RUN jj --repository /home/user/proj config set --repo user.name "Test User" && \
    jj --repository /home/user/proj config set --repo user.email "test@example.com"

RUN echo "# Project Scaffold" > /home/user/proj/README.md && \
    jj --repository /home/user/proj describe -m "init: project scaffold" && \
    jj --repository /home/user/proj new

RUN mkdir -p /home/user/proj/src && \
    echo "def login(): pass" > /home/user/proj/src/login.py && \
    jj --repository /home/user/proj describe -m "feat: add login module" && \
    jj --repository /home/user/proj new

RUN echo "def dashboard(): pass" > /home/user/proj/src/dashboard.py && \
    jj --repository /home/user/proj describe -m "feat: add dashboard module" && \
    jj --repository /home/user/proj new

RUN echo "body { color: red; }" > /home/user/proj/src/dashboard.css && \
    jj --repository /home/user/proj describe -m "wip: dashboard styling" && \
    jj --repository /home/user/proj new

RUN jj --repository /home/user/proj abandon "@-" "@--"

WORKDIR /home/user/proj

CMD ["/bin/bash"]
