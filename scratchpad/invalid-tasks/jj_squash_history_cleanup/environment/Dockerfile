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
LABEL Description="jj repo with history to squash in /home/user/weather_app"

RUN jj git init /home/user/weather_app && \
    cd /home/user/weather_app && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# Weather App" > README.md && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new && \
    echo "def track_rain(amount):" > rain.py && \
    echo "    return amount" >> rain.py && \
    jj describe -m "feat: add rain tracking" && \
    jj new && \
    echo "def track_rain(amount):" > rain.py && \
    echo "    # Fix: ensure non-negative" >> rain.py && \
    echo "    if amount < 0: return 0" >> rain.py && \
    echo "    return amount" >> rain.py && \
    jj describe -m "fix: calculation error" && \
    jj new && \
    echo "# Weather App" > README.md && \
    echo "" >> README.md && \
    echo "## Features" >> README.md && \
    echo "- Rain tracking" >> README.md && \
    jj describe -m "docs: update readme" && \
    jj bookmark create feature/precip

# Container contents:
# • /home/user/weather_app - jj repository with:
#   - main bookmark at "Initial commit"
#   - feature/precip bookmark at "docs: update readme"
#   - Intermediate commits "feat: add rain tracking" and "fix: calculation error"
# • Python 3, pip, and pytest available.

CMD ["/bin/bash"]