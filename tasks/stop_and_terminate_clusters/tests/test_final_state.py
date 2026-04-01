import os
import stat
import subprocess
import pytest


SCRIPT_PATH = "/home/user/cleanup.sh"


def test_cleanup_script_exists():
    assert os.path.isfile(SCRIPT_PATH), \
        f"cleanup.sh not found at {SCRIPT_PATH}"


def test_cleanup_script_is_executable():
    st = os.stat(SCRIPT_PATH)
    is_exec = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_exec, "cleanup.sh must be executable (chmod +x)."


def test_script_contains_sky_stop_all():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    has_stop_all = "sky stop --all" in content or "sky stop -a" in content
    assert has_stop_all, \
        "cleanup.sh must contain 'sky stop --all' to stop all clusters."


def test_script_contains_sky_down_all():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    has_down_all = "sky down --all" in content or "sky down -a" in content
    assert has_down_all, \
        "cleanup.sh must contain 'sky down --all' to terminate all clusters."


def test_script_uses_non_interactive_flags():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    # Check that -y or --yes flag is used somewhere with sky stop/down
    assert "-y" in content or "--yes" in content, \
        "cleanup.sh must use -y or --yes flag to skip confirmation prompts."


def test_stop_before_down():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    stop_pos = content.find("sky stop")
    down_pos = content.find("sky down")
    assert stop_pos != -1, "sky stop command not found in cleanup.sh."
    assert down_pos != -1, "sky down command not found in cleanup.sh."
    assert stop_pos < down_pos, \
        "sky stop must appear before sky down in cleanup.sh."
