import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
FILE_PATH = os.path.join(REPO_DIR, "src/math_utils.py")

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

def test_source_file_exists():
    assert os.path.isfile(FILE_PATH), f"Source file {FILE_PATH} does not exist."

def test_source_file_content_is_reverted():
    with open(FILE_PATH, "r") as f:
        content = f.read()
    
    assert "def add(a, b):" in content, f"File {FILE_PATH} missing 'add' function (initial state)."
    assert "def multiply(a, b):" not in content, f"File {FILE_PATH} contains 'multiply' function. It should have been reverted/abandoned."

def test_operation_log_accessible():
    result = subprocess.run(
        ["jj", "op", "log", "--limit", "1"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
