import os
import subprocess
import pytest

REPO_DIR = "/home/user/octopus_sim"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), f"jj repository not found at {REPO_DIR}"

def test_octopus_merge_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "octopus_merge", "-T", "commit_id"])
    assert result.returncode == 0, "Bookmark 'octopus_merge' does not exist."

def test_octopus_merge_parents():
    result = run_jj(["log", "--no-graph", "-r", "parents(octopus_merge)", "-T", "commit_id ++ \"\n\""])
    assert result.returncode == 0, f"Failed to get parents: {result.stderr}"
    parents = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    assert len(parents) == 3, f"Expected exactly 3 parents for octopus_merge, found {len(parents)}."

def test_files_in_octopus_merge():
    expected_files = {
        "base.txt": "base\n",
        "a.txt": "A\n",
        "b.txt": "B\n",
        "c.txt": "C\n",
        "merge.txt": "merged\n"
    }
    
    for filename, expected_content in expected_files.items():
        result = run_jj(["file", "show", filename, "-r", "octopus_merge"])
        assert result.returncode == 0, f"File {filename} not found in octopus_merge commit."
        # Allow for missing trailing newline in user's file
        assert result.stdout.strip() == expected_content.strip(), f"Content of {filename} is incorrect. Expected '{expected_content.strip()}', got '{result.stdout.strip()}'"

def test_merge_rev_log():
    log_path = os.path.join(REPO_DIR, "merge_rev.log")
    assert os.path.isfile(log_path), f"Log file {log_path} not found."
    
    with open(log_path, "r") as f:
        log_content = f.read().strip()
        
    result = run_jj(["log", "--no-graph", "-r", "octopus_merge", "-T", "commit_id"])
    assert result.returncode == 0
    commit_id = result.stdout.strip()
    
    assert commit_id in log_content, f"Commit ID {commit_id} not found in {log_path}."
