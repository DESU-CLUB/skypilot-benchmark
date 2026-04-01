import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/messy_project"

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

def test_initial_files_exist():
    files_to_check = [
        "src/main.py",
        "src/logger.py",
        "README.md"
    ]
    for rel_path in files_to_check:
        full_path = os.path.join(REPO_DIR, rel_path)
        assert os.path.exists(full_path), f"Expected file {rel_path} not found in {REPO_DIR}."

def test_initial_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "wip: all the things" in log, "Expected commit 'wip: all the things' not found in history."
    assert "initial commit" in log, "Expected 'initial commit' not found in history."

def test_working_copy_has_changes():
    result = subprocess.run(
        ["jj", "diff", "--summary"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert "src/logger.py" in result.stdout, "Expected uncommitted changes in 'src/logger.py' not found in working copy diff."
