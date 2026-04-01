FROM ubuntu:22.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflicting changes in main and feature bookmarks"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p src && \
    echo "[server]" > src/config.toml && \
    jj describe -m "initial config" && \
    jj bookmark create initial && \
    jj new initial && \
    echo "[server]" > src/config.toml && \
    echo "timeout = 30" >> src/config.toml && \
    jj describe -m "add timeout" && \
    jj bookmark create main && \
    jj new initial && \
    echo "[server]" > src/config.toml && \
    echo "max_retries = 5" >> src/config.toml && \
    jj describe -m "add max_retries" && \
    jj bookmark create feature && \
    jj bookmark delete initial && \
    jj edit feature

# Container contents:
# • /home/user/repo — jj repository with divergent history:
#   - "initial" revision (root)
#   - "main" bookmark: adds timeout = 30
#   - "feature" bookmark: adds max_retries = 5 (conflict source)
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]