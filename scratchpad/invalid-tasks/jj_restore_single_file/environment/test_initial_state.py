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

def test_initial_utils_py_content():
    utils_path = os.path.join(REPO_DIR, "src", "utils.py")
    assert os.path.isfile(utils_path), f"File {utils_path} does not exist."
    with open(utils_path, "r") as f:
        content = f.read()
    assert 'print("helping broken")' in content, f"File {utils_path} does not contain expected broken content in initial state."

def test_initial_ideas_md_content():
    ideas_path = os.path.join(REPO_DIR, "src", "ideas.md")
    assert os.path.isfile(ideas_path), f"File {ideas_path} does not exist."
    with open(ideas_path, "r") as f:
        content = f.read()
    assert "Refactor plan:" in content, f"File {ideas_path} does not contain expected content in initial state."
