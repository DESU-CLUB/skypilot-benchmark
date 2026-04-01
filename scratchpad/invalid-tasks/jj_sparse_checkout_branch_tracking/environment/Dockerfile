FROM ubuntu:24.04

LABEL Author="jj-task-builder"
LABEL Description="jj sparse checkout branch tracking task environment"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    python3-pytest \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.email "user@example.com" && \
    git config --global user.name "User"

# Initialize bare remote repo
RUN git init --bare /home/user/platform-mono-remote

# Clone remote into temp repo
RUN git clone /home/user/platform-mono-remote /home/user/platform-mono-temp

# Build initial monorepo structure in temp repo
RUN cd /home/user/platform-mono-temp && \
    mkdir -p infra/terraform infra/kubernetes && \
    mkdir -p services/auth services/payments services/notifications && \
    mkdir -p shared/libs shared/protos && \
    mkdir -p docs && \
    echo "# Platform Mono" > README.md && \
    echo "# Infra" > infra/README.md && \
    echo "# Terraform" > infra/terraform/main.tf && \
    echo "# Kubernetes" > infra/kubernetes/kustomization.yaml && \
    echo "# Services" > services/README.md && \
    echo "# Auth Service" > services/auth/main.go && \
    echo "# Payments Service" > services/payments/main.go && \
    echo "# Notifications Service" > services/notifications/main.go && \
    echo "# Shared Libraries" > shared/libs/utils.go && \
    echo "# Shared Protos" > shared/protos/api.proto && \
    echo "# Documentation" > docs/index.md && \
    git add . && \
    git commit -m "initial commit: monorepo structure" && \
    git push origin HEAD:main

# Create the infra/terraform-refactor branch
RUN cd /home/user/platform-mono-temp && \
    git checkout -b infra/terraform-refactor && \
    echo "# Terraform refactor WIP" > infra/terraform/refactor.tf && \
    git add . && \
    git commit -m "infra: begin terraform refactor" && \
    git push origin infra/terraform-refactor && \
    git checkout main

# Clone using jj from the bare remote
RUN jj git clone /home/user/platform-mono-remote /home/user/platform-mono

# Configure jj user identity in repo
RUN cd /home/user/platform-mono && \
    jj config set --repo user.email "user@example.com" && \
    jj config set --repo user.name "User"

CMD ["/bin/bash"]
