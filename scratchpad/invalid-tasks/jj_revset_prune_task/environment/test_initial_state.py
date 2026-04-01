import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def test_jj_binary_exists():
    assert shutil.which("jj") is not None, "jj binary not found in PATH"

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"

def test_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f".jj directory missing in {REPO_DIR}"
    
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"

def test_initial_files_exist():
    files_to_check = ["init.txt", "debug.js", "work.txt"]
    for filename in files_to_check:
        path = os.path.join(REPO_DIR, filename)
        assert os.path.isfile(path), f"Expected initial file {filename} not found in {REPO_DIR}"

def test_initial_commits_exist():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log_output = result.stdout
    
    expected_descriptions = [
        "initial setup",
        "temporary debug info",
        "wip feature"
    ]
    
    for desc in expected_descriptions:
        assert desc in log_output, f"Expected commit with description '{desc}' not found in history"

def test_bookmark_main_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Expected bookmark 'main' not found"

def test_user_config_set():
    result = subprocess.run(
        ["jj", "config", "list", "--repo"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "jj config list failed"
    assert "user.name" in result.stdout, "user.name config not set in repo"
    assert "user.email" in result.stdout, "user.email config not set in repo"
