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
LABEL Description="jj repo with linear history and working copy changes for rewrite task"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf "Line 1\nLine 2\n" > file_a.txt && \
    printf "Line 1\nLine 2\n" > file_b.txt && \
    jj describe -m "initial" && \
    jj new && \
    printf "Line 1\nLine 2\nFeature A\n" > file_a.txt && \
    printf "Line 1\nLine 2\nFeature B\n" > file_b.txt && \
    jj describe -m "feature A and B" && \
    jj new && \
    printf "Line 1\nLine 2\nFeature A\nTypo fix\n" > file_a.txt && \
    jj describe -m "fix typo in A" && \
    jj new && \
    printf "Line 1\nLine 2\nFeature A\nTypo fix\nMore fixes\n" > file_a.txt && \
    jj describe -m "more fixes for A" && \
    jj new && \
    printf "Line 1\nLine 2\nFeature B\nWorking copy change\n" > file_b.txt

# Container contents:
# • /home/user/repo - jj repository with messy history
# • Commits:
#   - "initial"
#   - "feature A and B"
#   - "fix typo in A"
#   - "more fixes for A"
# • Working copy has uncommitted changes in file_b.txt
# • Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]