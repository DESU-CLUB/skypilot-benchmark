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
LABEL Description="jj repo with conflict scenario (main vs feature)"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf "[package]\nname = \"my-app\"\nversion = \"1.0\"\n" > config.toml && \
    jj describe -m "initial config" && \
    jj bookmark create base && \
    jj new base -m "update to 1.1" && \
    printf "[package]\nname = \"my-app\"\nversion = \"1.1\"\n" > config.toml && \
    jj bookmark create main && \
    jj new base -m "set beta version" && \
    printf "[package]\nname = \"my-app\"\nversion = \"1.0-beta\"\n" > config.toml && \
    jj bookmark create feature && \
    jj edit feature

# Container contents:
# • /home/user/repo — jj repository with divergent history
# - base: version 1.0
# - main: version 1.1
# - feature: version 1.0-beta (checked out)
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
