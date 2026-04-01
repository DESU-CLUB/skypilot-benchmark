import os
import shutil
import subprocess
import pytest


def test_sky_binary_available():
    assert shutil.which("sky") is not None, "sky binary not found in PATH."


def test_sky_importable():
    result = subprocess.run(
        ["python3", "-c", "import sky; print(sky.__version__)"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"sky package is not importable: {result.stderr}"


def test_python3_available():
    assert shutil.which("python3") is not None, "python3 not found in PATH."


def test_launch_job_does_not_exist():
    assert not os.path.isfile("/home/user/launch_job.py"), \
        "launch_job.py should not exist at the start of the task."


def test_home_user_dir_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
