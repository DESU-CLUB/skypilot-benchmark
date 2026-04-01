import os
import stat
import json
import subprocess
import pytest


YAML_PATH = "/home/user/vllm_serve.yaml"
SCRIPT_PATH = "/home/user/deploy.sh"
CONFIG_PATH = "/home/user/serve_config.json"


def _parse_yaml():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    return json.loads(result.stdout)


def test_yaml_exists():
    assert os.path.isfile(YAML_PATH), f"vllm_serve.yaml not found at {YAML_PATH}"


def test_deploy_sh_exists():
    assert os.path.isfile(SCRIPT_PATH), f"deploy.sh not found at {SCRIPT_PATH}"


def test_serve_config_exists():
    assert os.path.isfile(CONFIG_PATH), f"serve_config.json not found at {CONFIG_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"vllm_serve.yaml is not valid YAML: {result.stderr}"


def test_deploy_sh_is_executable():
    st = os.stat(SCRIPT_PATH)
    is_exec = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_exec, "deploy.sh must be executable."


def test_serve_config_is_valid_json():
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    assert isinstance(data, dict), "serve_config.json must be a JSON object."


def test_readiness_probe_path():
    data = _parse_yaml()
    probe = data.get("service", {}).get("readiness_probe", {})
    assert probe.get("path") == "/v1/models", \
        f"Expected readiness_probe.path: /v1/models, got: {probe.get('path')}"


def test_readiness_probe_initial_delay():
    data = _parse_yaml()
    probe = data.get("service", {}).get("readiness_probe", {})
    assert probe.get("initial_delay_seconds") == 30, \
        f"Expected initial_delay_seconds: 30, got: {probe.get('initial_delay_seconds')}"


def test_min_replicas():
    data = _parse_yaml()
    policy = data.get("service", {}).get("replica_policy", {})
    assert policy.get("min_replicas") == 1, \
        f"Expected min_replicas: 1, got: {policy.get('min_replicas')}"


def test_max_replicas():
    data = _parse_yaml()
    policy = data.get("service", {}).get("replica_policy", {})
    assert policy.get("max_replicas") == 5, \
        f"Expected max_replicas: 5, got: {policy.get('max_replicas')}"


def test_target_qps():
    data = _parse_yaml()
    policy = data.get("service", {}).get("replica_policy", {})
    assert policy.get("target_qps_per_replica") == 10, \
        f"Expected target_qps_per_replica: 10, got: {policy.get('target_qps_per_replica')}"


def test_upscale_delay():
    data = _parse_yaml()
    policy = data.get("service", {}).get("replica_policy", {})
    assert policy.get("upscale_delay_seconds") == 60, \
        f"Expected upscale_delay_seconds: 60, got: {policy.get('upscale_delay_seconds')}"


def test_downscale_delay():
    data = _parse_yaml()
    policy = data.get("service", {}).get("replica_policy", {})
    assert policy.get("downscale_delay_seconds") == 300, \
        f"Expected downscale_delay_seconds: 300, got: {policy.get('downscale_delay_seconds')}"


def test_a100_resource():
    data = _parse_yaml()
    acc = str(data.get("resources", {}).get("accelerators", ""))
    assert "A100" in acc, f"Expected A100 in resources.accelerators, got: {acc}"


def test_on_demand_not_spot():
    data = _parse_yaml()
    use_spot = data.get("resources", {}).get("use_spot", True)
    assert use_spot is False, \
        f"Expected resources.use_spot: false (on-demand for serving stability), got: {use_spot}"


def test_model_name_env():
    data = _parse_yaml()
    envs = data.get("envs", {})
    assert envs.get("MODEL_NAME") == "meta-llama/Meta-Llama-3-8B-Instruct", \
        f"Expected MODEL_NAME: meta-llama/Meta-Llama-3-8B-Instruct, got: {envs.get('MODEL_NAME')}"


def test_setup_installs_vllm():
    data = _parse_yaml()
    setup = data.get("setup", "")
    assert "vllm" in setup, f"Expected setup to install vllm, got: {setup}"


def test_run_starts_vllm_server():
    data = _parse_yaml()
    run = data.get("run", "")
    assert "vllm" in run.lower(), f"Expected run to start vllm server, got: {run}"
    assert "8080" in run, f"Expected run to bind to port 8080, got: {run}"


def test_deploy_sh_uses_sky_serve_up():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky serve up" in content, "deploy.sh must use 'sky serve up' command."


def test_deploy_sh_references_yaml():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "vllm_serve.yaml" in content, "deploy.sh must reference vllm_serve.yaml."


def test_deploy_sh_names_service():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "vllm-llama" in content, "deploy.sh must name the service 'vllm-llama'."


def test_deploy_sh_non_interactive():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "-y" in content or "--yes" in content, \
        "deploy.sh must use -y or --yes for non-interactive deployment."


def test_deploy_sh_checks_status():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky serve status" in content, \
        "deploy.sh must check service status with 'sky serve status'."


def test_deploy_sh_writes_status_log():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "serve_status.log" in content, \
        "deploy.sh must write status output to /home/user/serve_status.log."


def test_serve_config_json_values():
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    assert data.get("service_name") == "vllm-llama", \
        f"Expected service_name: vllm-llama, got: {data.get('service_name')}"
    assert data.get("model") == "meta-llama/Meta-Llama-3-8B-Instruct", \
        f"Expected model: meta-llama/Meta-Llama-3-8B-Instruct, got: {data.get('model')}"
    assert data.get("min_replicas") == 1, \
        f"Expected min_replicas: 1, got: {data.get('min_replicas')}"
    assert data.get("max_replicas") == 5, \
        f"Expected max_replicas: 5, got: {data.get('max_replicas')}"
    assert data.get("port") == 8080, \
        f"Expected port: 8080, got: {data.get('port')}"
