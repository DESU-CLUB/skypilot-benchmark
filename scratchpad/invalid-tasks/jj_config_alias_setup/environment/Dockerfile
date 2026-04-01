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
LABEL Description="jj repo configured with initial commit and main bookmark"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Repo Admin" && \
    jj config set --repo user.email "admin@example.com" && \
    echo "# Project Documentation" > README.md && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new

# Container contents:
# • /home/user/repo — jj repository initialized
# - Initial commit with README.md
# - main bookmark created
# - Working copy ready for task
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]