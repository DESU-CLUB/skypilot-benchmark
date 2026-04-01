import os
import subprocess
import pytest


YAML_PATH = "/home/user/private_train.yaml"


def _load_yaml_content():
    with open(YAML_PATH) as f:
        return f.read()


def _parse_yaml():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    import json
    return json.loads(result.stdout)


def test_private_train_yaml_exists():
    assert os.path.isfile(YAML_PATH), \
        f"private_train.yaml not found at {YAML_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"private_train.yaml is not valid YAML: {result.stderr}"


def test_job_name_is_private_train():
    data = _parse_yaml()
    assert data.get("name") == "private-train", \
        f"Expected job name 'private-train', got: {data.get('name')}"


def test_envs_declares_git_token():
    data = _parse_yaml()
    envs = data.get("envs", {})
    assert "GIT_TOKEN" in envs, \
        "Expected 'GIT_TOKEN' declared in envs section."


def test_setup_uses_git_token():
    content = _load_yaml_content()
    assert "GIT_TOKEN" in content or "git_token" in content.lower(), \
        "setup must reference GIT_TOKEN environment variable."
    assert "$GIT_TOKEN" in content or "${GIT_TOKEN}" in content, \
        "setup must use $GIT_TOKEN or ${GIT_TOKEN} for authentication."


def test_setup_clones_private_repo():
    content = _load_yaml_content()
    assert "git clone" in content, \
        "setup must contain a git clone command."
    assert "myorg/private-training-lib" in content, \
        "setup must clone github.com/myorg/private-training-lib."


def test_setup_editable_install():
    content = _load_yaml_content()
    assert "pip install -e" in content or "pip install -e." in content, \
        "setup must install the cloned repo with 'pip install -e .'."


def test_run_executes_train_py():
    data = _parse_yaml()
    run = data.get("run", "")
    assert "train.py" in run, \
        f"Expected run to execute train.py, got: {run}"
