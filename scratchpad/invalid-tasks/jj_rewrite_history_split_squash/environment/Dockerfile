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
LABEL Description="jj repo with messy history (buggy modules followed by fix) in /home/user/messy-project"

RUN mkdir -p /home/user/messy-project && \
    cd /home/user/messy-project && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# Project" > README.md && \
    jj describe -m "Initial commit" && \
    jj new && \
    echo "def add(a, b): return a - b # Buggy" > math_lib.py && \
    echo "def shout(s): return s.upper()" > string_lib.py && \
    jj describe -m "Add modules" && \
    jj new && \
    echo "def add(a, b): return a + b # Fixed" > math_lib.py && \
    jj describe -m "Fix math bug"

# Container contents:
# • /home/user/messy-project — jj repository with 3 commits:
#   - "Initial commit"
#   - "Add modules" (Introduces math_lib.py [buggy] and string_lib.py)
#   - "Fix math bug" (Fixes math_lib.py)
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]