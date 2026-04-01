import os
import subprocess
import pytest


YAML_PATH = "/home/user/finetune_job.yaml"


def _load_yaml():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); print(json.dumps(d))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    import json
    return json.loads(result.stdout)


def test_finetune_job_yaml_exists():
    assert os.path.isfile(YAML_PATH), \
        f"finetune_job.yaml not found at {YAML_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"finetune_job.yaml is not valid YAML: {result.stderr}"


def test_job_name_is_llama_finetune():
    data = _load_yaml()
    assert data.get("name") == "llama-finetune", \
        f"Expected job name 'llama-finetune', got: {data.get('name')}"


def test_accelerators_a100_4():
    data = _load_yaml()
    resources = data.get("resources", {})
    acc = resources.get("accelerators", "")
    acc_str = str(acc)
    assert "A100" in acc_str and "4" in acc_str, \
        f"Expected resources.accelerators to be A100:4, got: {acc_str}"


def test_use_spot_true():
    data = _load_yaml()
    resources = data.get("resources", {})
    assert resources.get("use_spot") is True, \
        f"Expected resources.use_spot: true, got: {resources.get('use_spot')}"


def test_any_of_has_aws_and_gcp():
    data = _load_yaml()
    resources = data.get("resources", {})
    any_of = resources.get("any_of", [])
    import json
    any_of_str = json.dumps(any_of)
    assert "aws" in any_of_str.lower(), \
        f"Expected AWS entry in resources.any_of, got: {any_of_str}"
    assert "gcp" in any_of_str.lower(), \
        f"Expected GCP entry in resources.any_of, got: {any_of_str}"


def test_autostop_30():
    data = _load_yaml()
    resources = data.get("resources", {})
    assert resources.get("autostop") == 30, \
        f"Expected resources.autostop: 30, got: {resources.get('autostop')}"


def test_env_model_name():
    data = _load_yaml()
    envs = data.get("envs", {})
    assert envs.get("MODEL_NAME") == "meta-llama/Llama-3-8B", \
        f"Expected envs.MODEL_NAME to be 'meta-llama/Llama-3-8B', got: {envs.get('MODEL_NAME')}"


def test_workdir_is_dot():
    data = _load_yaml()
    assert data.get("workdir") == ".", \
        f"Expected workdir: '.', got: {data.get('workdir')}"


def test_setup_installs_requirements():
    data = _load_yaml()
    setup = data.get("setup", "")
    assert "requirements.txt" in setup, \
        f"Expected setup to reference requirements.txt, got: {setup}"


def test_run_executes_finetune():
    data = _load_yaml()
    run = data.get("run", "")
    assert "finetune.py" in run, \
        f"Expected run to execute finetune.py, got: {run}"
    assert "MODEL_NAME" in run, \
        f"Expected run to reference MODEL_NAME env var, got: {run}"
