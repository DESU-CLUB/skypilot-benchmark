import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
OUTPUT_FILE = "/home/user/remaining_commits.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"File {OUTPUT_FILE} does not exist."

def test_output_file_content():
    if not os.path.exists(OUTPUT_FILE):
        pytest.fail(f"File {OUTPUT_FILE} missing, cannot check content.")
    
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()
    
    # Verify content as per Truth items 3-7
    assert "experiment" not in content, "Found 'experiment' in remaining_commits.txt"
    assert "Initial setup" in content, "Missing 'Initial setup' in remaining_commits.txt"
    assert "feat: add login" in content, "Missing 'feat: add login' in remaining_commits.txt"
    assert "feat: add logout" in content, "Missing 'feat: add logout' in remaining_commits.txt"
    assert "feat: user profile" in content, "Missing 'feat: user profile' in remaining_commits.txt"

def test_repo_state_no_experiments():
    # Verify experimental commits are actually gone from the repo
    result = run_jj(["log", "--no-graph", "-r", "all()", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "experiment" not in result.stdout, "Experimental commits still exist in the repository."

def test_repo_structure_linear():
    # Verify the linear history structure as per Truth item 8
    # Ensure "feat: add logout" is a child of "feat: add login"
    result = run_jj(["log", "--no-graph", "-r", 'parents(description("feat: add logout"))', "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add login" in result.stdout, f"Expected parent of 'feat: add logout' to be 'feat: add login', got: {result.stdout.strip()}"

    # Ensure "feat: user profile" is a child of "feat: add logout"
    result = run_jj(["log", "--no-graph", "-r", 'parents(description("feat: user profile"))', "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add logout" in result.stdout, f"Expected parent of 'feat: user profile' to be 'feat: add logout', got: {result.stdout.strip()}"
