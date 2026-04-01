#!/bin/bash

# 1. Create the SkyServe YAML for vLLM with autoscaling
cat > /home/user/vllm_serve.yaml << 'EOF'
service:
  readiness_probe:
    path: /v1/models
    initial_delay_seconds: 30
  replica_policy:
    min_replicas: 1
    max_replicas: 5
    target_qps_per_replica: 10
    upscale_delay_seconds: 60
    downscale_delay_seconds: 300

resources:
  accelerators: A100:1
  cloud: aws
  use_spot: false

envs:
  MODEL_NAME: meta-llama/Meta-Llama-3-8B-Instruct

setup: |
  pip install vllm

run: |
  python -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --port 8080 \
    --host 0.0.0.0
EOF

# 2. Create the deployment script
cat > /home/user/deploy.sh << 'EOF'
#!/bin/bash
sky serve up /home/user/vllm_serve.yaml --name vllm-llama -y
sky serve status vllm-llama > /home/user/serve_status.log
EOF

chmod +x /home/user/deploy.sh

# 3. Create the service config JSON
cat > /home/user/serve_config.json << 'EOF'
{
  "service_name": "vllm-llama",
  "model": "meta-llama/Meta-Llama-3-8B-Instruct",
  "min_replicas": 1,
  "max_replicas": 5,
  "port": 8080
}
EOF
