import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/rebase_verification.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_file_content():
    result = run_jj(["file", "show", "src/config.toml", "-r", "feature"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    content = result.stdout
    assert "[server]" in content, "File src/config.toml missing '[server]' header"
    assert "timeout = 30" in content, "File src/config.toml missing 'timeout = 30'"
    assert "max_retries = 5" in content, "File src/config.toml missing 'max_retries = 5'"

def test_graph_structure():
    # Verify feature is a direct child of main
    # We check if the intersection of feature's parents and main is non-empty
    result = run_jj(["log", "-r", "parents(feature) & main", "--no-graph"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip(), "The 'feature' bookmark is not a direct child of 'main'"

def test_no_conflicts():
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", "conflicts"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", "Conflict detected in 'feature' revision"

def test_log_file():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist"
    with open(LOG_FILE, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, "Log file is empty"
    # Basic check to ensure it looks like a jj log (contains commit info or bookmark names)
    assert "feature" in content or "change-id" in content or "commit-id" in content, "Log file content does not appear to be a jj log"
