FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-venv bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install pytest pyyaml skypilot --quiet || pip install pytest pyyaml "skypilot[aws]" --quiet

RUN mkdir -p /home/user && chmod 0755 /home/user

# Pre-create the broken YAML that the user must diagnose and fix
RUN cat >/home/user/broken_job.yaml <<'EOF'
name: training-job
file_mounts:
  /home/user/training-code:
    source: s3://ml-configs/job-config
    mode: COPY
setup: |
  git clone https://github.com/myorg/training-code.git /home/user/training-code
  cd /home/user/training-code && pip install -e .
run: |
  python /home/user/training-code/train.py
EOF

LABEL Author="any-task-builder"
LABEL Description="SkyPilot debug environment: broken YAML with file_mount/git-clone collision to diagnose and fix."

# Container contents:
#   - /opt/venv — Python venv with skypilot, pyyaml, pytest
#   - /home/user/broken_job.yaml — pre-existing broken YAML with mount collision
#   - /home/user/fixed_job.yaml — does NOT exist yet (user must create it)

CMD ["/bin/bash"]
