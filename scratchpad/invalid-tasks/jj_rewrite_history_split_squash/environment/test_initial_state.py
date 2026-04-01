import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/messy-project"

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

def test_initial_commits_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "Initial commit" in log, "Expected commit 'Initial commit' not found in log."
    assert "Add modules" in log, "Expected commit 'Add modules' not found in log."
    assert "Fix math bug" in log, "Expected commit 'Fix math bug' not found in log."

def test_initial_files_present():
    # The setup script creates these files in the working copy at the end
    expected_files = ["README.md", "math_lib.py", "string_lib.py"]
    for filename in expected_files:
        filepath = os.path.join(REPO_DIR, filename)
        assert os.path.isfile(filepath), f"Expected initial file {filename} missing in {REPO_DIR}."
