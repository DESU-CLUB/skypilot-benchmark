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
LABEL Description="jj repo where a feature was accidentally abandoned, for recovery training"

WORKDIR /home/user/repo
RUN jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p src
RUN cat > src/math_utils.py <<'EOF'
def add(a, b):
    return a + b
EOF
RUN jj describe -m "initial: add function" && jj new
RUN cat > src/math_utils.py <<'EOF'
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
EOF
RUN jj describe -m "feat: implement multiply" && jj abandon @

# Container contents:
# • /home/user/repo — jj repository
# • Initial state: "initial: add function"
# • History contains an abandoned commit "feat: implement multiply"
# • Python 3, pip, and pytest available

CMD ["/bin/bash"]