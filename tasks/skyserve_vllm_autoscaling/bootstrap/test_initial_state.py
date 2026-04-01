import os
import shutil
import subprocess
import pytest


def test_sky_binary_available():
    assert shutil.which("sky") is not None, "sky binary not found in PATH."


def test_pyyaml_importable():
    result = subprocess.run(
        ["python3", "-c", "import yaml; print(yaml.__version__)"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"PyYAML is not importable: {result.stderr}"


def test_home_user_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."


def test_vllm_serve_yaml_does_not_exist():
    assert not os.path.isfile("/home/user/vllm_serve.yaml"), \
        "vllm_serve.yaml should not exist at the start of the task."


def test_deploy_sh_does_not_exist():
    assert not os.path.isfile("/home/user/deploy.sh"), \
        "deploy.sh should not exist at the start of the task."


def test_serve_config_json_does_not_exist():
    assert not os.path.isfile("/home/user/serve_config.json"), \
        "serve_config.json should not exist at the start of the task."
