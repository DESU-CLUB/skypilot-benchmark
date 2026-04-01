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


def test_inference_job_yaml_does_not_exist():
    assert not os.path.isfile("/home/user/inference_job.yaml"), \
        "inference_job.yaml should not exist at the start of the task."
