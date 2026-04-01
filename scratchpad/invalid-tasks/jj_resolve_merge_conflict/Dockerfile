FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: resolve conflicts in merge-like flows - reviewer validating conflict workflows"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj git init /home/user/config-project

WORKDIR /home/user/config-project

RUN jj config set --repo user.name "Test User" \
    && jj config set --repo user.email "test@example.com"

RUN printf '[server]\nhost = "localhost"\nport = 8080\ntimeout = 30\nretries = 3\nlog_level = "info"\n' > config.toml \
    && jj describe -m "Initial config with server defaults" \
    && jj bookmark create main -r @

RUN jj new main -m "Increase timeout to 60 for slow networks" \
    && printf '[server]\nhost = "localhost"\nport = 8080\ntimeout = 60\nretries = 3\nlog_level = "info"\n' > config.toml \
    && jj describe -m "Increase timeout to 60 for slow networks" \
    && jj bookmark create feature-timeout -r @

RUN jj new main -m "Reduce timeout to 10 and increase retries to 5" \
    && printf '[server]\nhost = "localhost"\nport = 8080\ntimeout = 10\nretries = 5\nlog_level = "info"\n' > config.toml \
    && jj describe -m "Reduce timeout to 10 and increase retries to 5" \
    && jj bookmark create feature-retries -r @

RUN jj new feature-timeout feature-retries -m "Merge feature-timeout and feature-retries"

CMD ["/bin/bash"]
