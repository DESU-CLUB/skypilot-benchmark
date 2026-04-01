import os
import subprocess
import pytest


REPO_DIR = "/home/user/proj"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_subdir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj subdirectory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_initial_commits_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    assert "init: project scaffold" in output, "Expected 'init: project scaffold' in log"
    assert "feat: add login module" in output, "Expected 'feat: add login module' in log"


def test_dashboard_commits_not_visible_in_default_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    assert "feat: add dashboard module" not in output, (
        "Dashboard module commit should not be visible in default log before recovery"
    )
    assert "wip: dashboard styling" not in output, (
        "Dashboard styling commit should not be visible in default log before recovery"
    )


def test_operation_log_exists():
    result = subprocess.run(
        ["jj", "op", "log"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "Operation log is empty"
