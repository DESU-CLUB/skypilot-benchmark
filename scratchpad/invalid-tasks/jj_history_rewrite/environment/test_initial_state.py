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

def test_initial_commits_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "initial" in log, "Expected initial commit 'initial' not found."
    assert "feature A and B" in log, "Expected commit 'feature A and B' not found."
    assert "fix typo in A" in log, "Expected commit 'fix typo in A' not found."
    assert "more fixes for A" in log, "Expected commit 'more fixes for A' not found."

def test_initial_files_present():
    file_a = os.path.join(REPO_DIR, "file_a.txt")
    file_b = os.path.join(REPO_DIR, "file_b.txt")
    assert os.path.isfile(file_a), f"Expected file {file_a} not found."
    assert os.path.isfile(file_b), f"Expected file {file_b} not found."

def test_working_copy_has_changes():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    status_output = result.stdout
    assert "file_b.txt" in status_output, "Expected uncommitted changes to file_b.txt not found."
