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
LABEL Description="jj repo with messy history for cleanup task"

WORKDIR /home/user/workspace/messy_project
RUN jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p src
RUN cat > src/main.py <<'EOF'
def main():
    print("Hello")
    raise Exception("Crash")
EOF
RUN cat > README.md <<'EOF'
# Project
EOF
RUN jj describe -m "initial commit" && jj new
RUN cat > src/logger.py <<'EOF'
def log(msg):
    print(f"LOG: {msg}")
EOF
RUN cat > src/main.py <<'EOF'
def main():
    print("Hello")
EOF
RUN cat > README.md <<'EOF'
# Project
- Added logging
EOF
RUN jj describe -m "wip: all the things" && jj new
RUN cat > src/logger.py <<'EOF'
import sys
def log(msg):
    print(f"LOG: {msg}")
EOF

# Container contents:
# • /home/user/workspace/messy_project - jj repo
# • Commits: "initial commit", "wip: all the things"
# • Working copy has uncommitted changes to src/logger.py

CMD ["/bin/bash"]