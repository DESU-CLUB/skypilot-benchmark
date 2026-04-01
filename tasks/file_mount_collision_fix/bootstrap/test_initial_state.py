import os
import shutil
import subprocess
import pytest

BROKEN_YAML = "/home/user/broken_job.yaml"


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


def test_broken_job_yaml_exists():
    assert os.path.isfile(BROKEN_YAML), \
        f"broken_job.yaml must be pre-created at {BROKEN_YAML}."


def test_broken_yaml_is_valid_yaml():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{BROKEN_YAML}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"broken_job.yaml must be parseable YAML: {result.stderr}"


def test_broken_yaml_has_collision():
    """Verify the broken YAML actually has the file_mount/clone collision."""
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{BROKEN_YAML}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    import json
    data = json.loads(result.stdout)
    mounts = data.get("file_mounts", {})
    assert "/home/user/training-code" in mounts, \
        "broken_job.yaml must mount to /home/user/training-code (the collision path)."


def test_fixed_yaml_does_not_exist():
    assert not os.path.isfile("/home/user/fixed_job.yaml"), \
        "fixed_job.yaml should not exist at start of task."
