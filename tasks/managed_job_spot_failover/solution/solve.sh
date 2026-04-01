#!/bin/bash
# Solution: Create managed_train.yaml and submit_job.sh

cat > /home/user/managed_train.yaml << 'EOF'
name: resilient-train

resources:
  accelerators: A100:1
  use_spot: true
  job_recovery:
    strategy: FAILOVER
    max_restarts_on_errors: 3
    retry_on_return_codes:
      - 33
      - 1
  any_of:
    - infra: aws/us-east-1
    - infra: gcp/us-central1
    - infra: azure/eastus

setup: |
  pip install torch

run: |
  python train.py
EOF

cat > /home/user/submit_job.sh << 'EOF'
#!/bin/bash
sky jobs launch /home/user/managed_train.yaml --name resilient-train -y
sky jobs queue > /home/user/job_status.log
EOF

chmod +x /home/user/submit_job.sh
