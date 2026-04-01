import os
import subprocess
import ast
import pytest


SCRIPT_PATH = "/home/user/launch_job.py"


def test_launch_job_exists():
    assert os.path.isfile(SCRIPT_PATH), \
        f"launch_job.py not found at {SCRIPT_PATH}"


def test_script_is_valid_python():
    result = subprocess.run(
        ["python3", "-m", "py_compile", SCRIPT_PATH],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"launch_job.py has a syntax error: {result.stderr}"


def test_imports_sky():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "import sky" in content, \
        "launch_job.py must contain 'import sky'."


def test_uses_sky_resources():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky.Resources(" in content, \
        "launch_job.py must use sky.Resources() to define compute resources."


def test_uses_sky_task():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky.Task(" in content, \
        "launch_job.py must use sky.Task() to define the job."


def test_uses_set_resources():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert ".set_resources(" in content, \
        "launch_job.py must call .set_resources() to attach resources to the task."


def test_uses_sky_launch():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky.launch(" in content, \
        "launch_job.py must call sky.launch() to submit the job."


def test_uses_stream_and_get():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky.stream_and_get(" in content or "stream_and_get(" in content, \
        "launch_job.py must call sky.stream_and_get() to wait for the async result (v0.8.1+ pattern)."


def test_cluster_name_eval_cluster():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "eval-cluster" in content, \
        "sky.launch() must be called with cluster_name='eval-cluster'."


def test_prints_job_id():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "JOB_ID:" in content, \
        "launch_job.py must print the job_id in the format 'JOB_ID: <id>'."
