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
LABEL Description="jj repo with linear history containing feature and experiment commits for cleanup task"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "initial content" > file.txt && \
    jj describe -m "Initial setup" && \
    jj new && \
    echo "login feature" > login.txt && \
    jj describe -m "feat: add login" && \
    jj new && \
    echo "experiment 1" > exp1.txt && \
    jj describe -m "experiment: try auth v1" && \
    jj new && \
    echo "logout feature" > logout.txt && \
    jj describe -m "feat: add logout" && \
    jj new && \
    echo "experiment 2" > exp2.txt && \
    jj describe -m "experiment: try auth v2" && \
    jj new && \
    echo "user profile feature" > profile.txt && \
    jj describe -m "feat: user profile"

# Container contents:
# • /home/user/repo — jj repository with linear history:
# - "Initial setup" (file.txt)
# - "feat: add login" (login.txt)
# - "experiment: try auth v1" (exp1.txt)
# - "feat: add logout" (logout.txt)
# - "experiment: try auth v2" (exp2.txt)
# - "feat: user profile" (profile.txt)
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]