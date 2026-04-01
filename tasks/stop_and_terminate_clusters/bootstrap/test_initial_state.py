import os
import shutil
import subprocess
import pytest


def test_sky_binary_available():
    assert shutil.which("sky") is not None, "sky binary not found in PATH."


def test_python3_available():
    assert shutil.which("python3") is not None, "python3 not found in PATH."


def test_cleanup_script_does_not_exist():
    assert not os.path.isfile("/home/user/cleanup.sh"), \
        "cleanup.sh should not exist at the start of the task."


def test_home_user_dir_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
