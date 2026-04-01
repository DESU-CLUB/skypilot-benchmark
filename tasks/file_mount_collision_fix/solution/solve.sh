#!/bin/bash
# Fix the file_mount collision: mount S3 configs to a different path
# so that setup can git clone into /home/user/training-code without collision.

cat >/home/user/fixed_job.yaml <<'EOF'
name: training-job
file_mounts:
  /home/user/configs:
    source: s3://ml-configs/job-config
    mode: COPY
setup: |
  git clone https://github.com/myorg/training-code.git /home/user/training-code
  cd /home/user/training-code && pip install -e .
run: |
  python /home/user/training-code/train.py
EOF

cat >/home/user/fix_explanation.txt <<'EOF'
SkyPilot processes file_mounts before running setup, so mounting to /home/user/training-code caused the git clone in setup to fail with "directory not empty"; the fix is to mount the S3 configs to a different path (e.g., /home/user/configs) so the clone target is empty.
EOF
