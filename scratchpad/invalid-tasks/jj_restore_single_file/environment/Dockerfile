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
LABEL Description="jj repo with a modified file to restore and a new file to preserve"

WORKDIR /home/user/repo
RUN jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p src
RUN cat > src/utils.py <<'EOF'
def help():
    print("helping")
EOF
RUN jj describe -m "feat: add utils" && jj new
RUN cat > src/utils.py <<'EOF'
def help():
    print("helping broken")
EOF
RUN echo "Refactor plan: ..." > src/ideas.md

# Container contents:
# • /home/user/repo — jj repository
# • Current working copy has:
#   - Modified src/utils.py (broken version)
#   - New untracked/added src/ideas.md
# • Python 3, pip, and pytest available.

CMD ["/bin/bash"]
