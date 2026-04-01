FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: configure log aliases and pager settings for a new teammate onboarding to jj"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Create the jj user config directory with identity only (no aliases, no paginate)
RUN mkdir -p /home/user/.config/jj && \
    printf '[user]\nname = "Test User"\nemail = "test@example.com"\n' \
    > /home/user/.config/jj/config.toml

# Initialize the jj repository
RUN mkdir -p /home/user/myrepo && \
    cd /home/user/myrepo && \
    HOME=/home/user jj git init --no-colocate .

# Create an initial commit
RUN cd /home/user/myrepo && \
    echo "# My Repo" > README.md && \
    HOME=/home/user jj describe -m "Initial commit: add README" && \
    HOME=/home/user jj new

CMD ["/bin/bash"]
