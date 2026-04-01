import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
CULPRIT_FILE = "/home/user/culprit_op_id.txt"
SRC_FILE = os.path.join(REPO_DIR, "src/math_utils.py")

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_file_content_recovered():
    assert os.path.exists(SRC_FILE), f"File {SRC_FILE} does not exist."
    with open(SRC_FILE, "r") as f:
        content = f.read()
    assert "def multiply(a, b):" in content, "File src/math_utils.py does not contain the 'multiply' function."

def test_current_revision_description():
    result = run_jj(["log", "-r", "@", "--no-graph", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement multiply" in result.stdout, f"Current revision description incorrect. Expected 'feat: implement multiply', got: {result.stdout}"

def test_bookmark_exists_and_points_to_working_copy():
    # Get change_id of @
    res_wc = run_jj(["log", "-r", "@", "--no-graph", "-T", "change_id"])
    assert res_wc.returncode == 0, f"Failed to get wc change_id: {res_wc.stderr}"
    wc_id = res_wc.stdout.strip()

    # Get change_id of recovered-feat
    res_bm = run_jj(["log", "-r", "recovered-feat", "--no-graph", "-T", "change_id"])
    assert res_bm.returncode == 0, f"Bookmark 'recovered-feat' does not exist or is invalid: {res_bm.stderr}"
    bm_id = res_bm.stdout.strip()

    assert wc_id == bm_id, f"Bookmark 'recovered-feat' ({bm_id}) does not point to working copy ({wc_id})."

def test_culprit_op_id():
    assert os.path.exists(CULPRIT_FILE), f"File {CULPRIT_FILE} missing."
    with open(CULPRIT_FILE, "r") as f:
        op_id = f.read().strip()
    
    assert op_id, "Culprit Operation ID file is empty."
    
    # Check if the operation exists and involves 'abandon'
    # Limiting to last 100 operations to prevent massive output and potential resource issues
    result = run_jj(["op", "log", "--no-graph", "--limit", "100"])
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    
    output = result.stdout
    lines = output.splitlines()
    found_op_abandon = False
    
    # Iterate through lines to find the op_id and check context for 'abandon'
    for i, line in enumerate(lines):
        if op_id in line:
            # Check this line and next few lines for "abandon"
            # The description of the operation usually follows or is on the same line depending on formatting
            context = "\n".join(lines[i:i+10]) # Check a generous window
            if "abandon" in context:
                found_op_abandon = True
                break
    
    assert found_op_abandon, f"Operation ID {op_id} found, but could not confirm it was an 'abandon' operation. Output context checked."
