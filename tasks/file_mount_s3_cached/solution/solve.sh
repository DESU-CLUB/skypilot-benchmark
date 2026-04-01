#!/bin/bash

cat > /home/user/inference_job.yaml << 'EOF'
name: batch-inference

resources:
  accelerators: A100:4
  use_spot: true

file_mounts:
  /data:
    source: s3://ml-datasets/imagenet
    mode: MOUNT_CACHED
  /checkpoint:
    source: s3://ml-checkpoints/resnet50
    mode: COPY

setup: |
  pip install torch torchvision boto3

run: |
  python infer.py --data /data --checkpoint /checkpoint/model.pth --output /tmp/results.json
EOF
