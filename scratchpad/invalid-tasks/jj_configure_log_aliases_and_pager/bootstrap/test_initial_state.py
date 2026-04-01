import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "myrepo")


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_jj_directory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory does not exist in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0, (
        f"jj status failed in {REPO_DIR}:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_user_config_identity_set():
    result = subprocess.run(
        ["jj", "config", "get", "user.name"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0, "user.name is not configured"
    assert result.stdout.strip() != "", "user.name is empty"


def test_alias_ll_not_yet_set():
    """The ll alias should NOT exist in the initial state (user will create it)."""
    result = subprocess.run(
        ["jj", "config", "get", "aliases.ll"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode != 0, (
        "aliases.ll should not be set in the initial state, but it was found"
    )


def test_ui_paginate_not_yet_set():
    """ui.paginate should NOT be set to 'never' in the initial state."""
    result = subprocess.run(
        ["jj", "config", "get", "ui.paginate"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    # It may not be set at all (returncode != 0) or may be set to something other than 'never'
    if result.returncode == 0:
        assert result.stdout.strip() != "never", (
            "ui.paginate is already set to 'never' in the initial state"
        )
