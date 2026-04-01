FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-venv bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install pytest "skypilot" --quiet || pip install pytest skypilot --quiet

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="SkyPilot environment for writing a cluster cleanup shell script."

# Container contents:
#   - /opt/venv — Python venv with skypilot and pytest
#   - /home/user — working directory (cleanup.sh does not exist yet)

CMD ["/bin/bash"]
