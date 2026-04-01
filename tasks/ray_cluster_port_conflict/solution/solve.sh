#!/bin/bash
set -e

# Write the SkyPilot task YAML with 2 nodes using port 6379 (not 6380)
cat > /home/user/distributed_job.yaml << 'EOF'
name: ray-distributed-train

resources:
  cpus: 4

num_nodes: 2

run: |
  # SkyPilot uses port 6380 internally — start our Ray cluster on port 6379
  if [ "$SKYPILOT_NODE_RANK" == "0" ]; then
    # Head node: start Ray head on port 6379
    ray start --head --port=6379 --dashboard-port=8265
  else
    # Worker nodes: join the head node's Ray cluster on port 6379
    ray start --address="$(echo $SKYPILOT_NODE_IPS | cut -d' ' -f1):6379"
  fi
  python /home/user/train.py
EOF

# Write the Python training script that connects on port 6379
cat > /home/user/train.py << 'EOF'
import ray

# Connect to our Ray cluster on port 6379 (NOT 6380 which is SkyPilot's internal Ray)
ray.init(address="ray://127.0.0.1:6379")


@ray.remote
def run_task():
    return "ray task complete"


result = ray.get(run_task.remote())
print(result)
EOF
