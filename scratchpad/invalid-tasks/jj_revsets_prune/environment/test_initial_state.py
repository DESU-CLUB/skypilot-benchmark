import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"

def test_user_config_name():
    result = subprocess.run(
        ["jj", "config", "get", "user.name"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to get user.name: {result.stderr}"
    assert "Test User" in result.stdout, f"Expected user.name 'Test User', got '{result.stdout.strip()}'"

def test_user_config_email():
    result = subprocess.run(
        ["jj", "config", "get", "user.email"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to get user.email: {result.stderr}"
    assert "test@example.com" in result.stdout, f"Expected user.email 'test@example.com', got '{result.stdout.strip()}'"

def test_initial_commits_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    
    expected_commits = [
        "Initial setup",
        "feat: add login",
        "experiment: try auth v1",
        "feat: add logout",
        "experiment: try auth v2",
        "feat: user profile"
    ]
    
    for desc in expected_commits:
        assert desc in log, f"Expected initial commit '{desc}' not found in log."
