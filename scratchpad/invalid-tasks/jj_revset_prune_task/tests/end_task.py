import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
ID_FILE = "/home/user/bad_revision_id.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_id_file_exists():
    assert os.path.exists(ID_FILE), f"File {ID_FILE} does not exist"

def test_correct_id_captured():
    with open(ID_FILE, "r") as f:
        change_id = f.read().strip()
    
    # Verify the ID corresponds to the "temporary debug info" revision (searching hidden revisions)
    # We use change() revset to ensure it matches a Change ID
    result = run_jj(["log", "--hidden", "--no-graph", "-r", f'change("{change_id}")', "-T", "description"])
    
    # If the ID is invalid or not found, jj log might fail or return empty
    assert result.returncode == 0, f"jj log failed with ID '{change_id}': {result.stderr}"
    assert "temporary debug info" in result.stdout, f"The ID '{change_id}' does not correspond to a revision with description 'temporary debug info'. Got: {result.stdout}"

def test_bad_revision_abandoned():
    # It should not appear in the standard log (visible graph)
    result = run_jj(["log", "--no-graph", "-r", 'description("temporary debug info")'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", "Revision 'temporary debug info' is still visible in the graph"

def test_graph_structure():
    # Verify "clean feature" has "initial setup" as direct parent
    # First check if 'clean feature' exists to give a better error message
    check_exists = run_jj(["log", "--no-graph", "-r", 'description("clean feature")'])
    assert check_exists.returncode == 0
    assert check_exists.stdout.strip() != "", "Revision with description 'clean feature' not found in visible history"

    result = run_jj(["log", "--no-graph", "-r", 'parents(description("clean feature"))', "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial setup" in result.stdout, f"Expected parent of 'clean feature' to be 'initial setup'. Got: {result.stdout}"

def test_status_file_content():
    # Verify status.txt in the current working copy contains 'ready'
    status_path = os.path.join(REPO_DIR, "status.txt")
    assert os.path.exists(status_path), "status.txt does not exist in the working copy"
    
    with open(status_path, "r") as f:
        content = f.read().strip()
    
    assert content == "ready", f"Expected status.txt content 'ready', got '{content}'"
