import os
import subprocess
import pytest

REPO_DIR = "/home/user/messy-project"
ID_FILE = "/home/user/final_change_id.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_history_structure_and_descriptions():
    # 1. Verify tip (@) is "Add string library"
    res_tip = run_jj(["log", "-r", "@", "-T", "description"])
    assert res_tip.returncode == 0, f"jj log failed: {res_tip.stderr}"
    assert "Add string library" in res_tip.stdout, f"Tip description mismatch. Expected 'Add string library', got '{res_tip.stdout.strip()}'"

    # 2. Verify parent (@-) is "Add math library"
    res_parent = run_jj(["log", "-r", "@-", "-T", "description"])
    assert res_parent.returncode == 0, f"jj log failed: {res_parent.stderr}"
    assert "Add math library" in res_parent.stdout, f"Parent description mismatch. Expected 'Add math library', got '{res_parent.stdout.strip()}'"

    # 3. Verify grandparent (@--) is "Initial commit"
    res_grandparent = run_jj(["log", "-r", "@--", "-T", "description"])
    assert res_grandparent.returncode == 0, f"jj log failed: {res_grandparent.stderr}"
    assert "Initial commit" in res_grandparent.stdout, f"Grandparent description mismatch. Expected 'Initial commit', got '{res_grandparent.stdout.strip()}'"

def test_old_commits_gone():
    # Verify "Add modules" and "Fix math bug" are gone from the history
    res = run_jj(["log", "-r", "::@", "-T", "description"])
    assert res.returncode == 0, f"jj log failed: {res.stderr}"
    history = res.stdout
    assert "Add modules" not in history, "Commit 'Add modules' should be squashed/rewritten and not appear in history."
    assert "Fix math bug" not in history, "Commit 'Fix math bug' should be squashed/rewritten and not appear in history."

def test_tip_files_content():
    # Verify string_lib.py exists at tip and has correct content
    res_string = run_jj(["file", "show", "string_lib.py", "-r", "@"])
    assert res_string.returncode == 0, "string_lib.py missing at tip"
    assert "def shout(s): return s.upper()" in res_string.stdout, "string_lib.py content incorrect at tip"

    # Verify math_lib.py exists at tip and has FIXED content
    res_math = run_jj(["file", "show", "math_lib.py", "-r", "@"])
    assert res_math.returncode == 0, "math_lib.py missing at tip"
    assert "return a + b" in res_math.stdout, "math_lib.py does not contain the fix at tip"

def test_parent_files_content():
    # Verify parent (@-) has math_lib.py but NOT string_lib.py
    res_list = run_jj(["file", "list", "-r", "@-"])
    assert res_list.returncode == 0, f"jj file list failed: {res_list.stderr}"
    files = res_list.stdout
    
    assert "math_lib.py" in files, "math_lib.py missing in parent commit"
    assert "string_lib.py" not in files, "string_lib.py should not exist in parent commit (should be introduced in tip)"

    # Verify math_lib.py in parent is the FIXED version
    # This ensures the fix was squashed into the parent, not just applied at the tip
    res_content = run_jj(["file", "show", "math_lib.py", "-r", "@-"])
    assert res_content.returncode == 0, "Failed to read math_lib.py at parent revision"
    content = res_content.stdout
    assert "return a + b" in content, f"math_lib.py in parent does not contain the fix. Content:\n{content}"

def test_change_id_file():
    assert os.path.exists(ID_FILE), f"File {ID_FILE} does not exist."
    
    with open(ID_FILE, "r") as f:
        user_id = f.read().strip()
    
    # Get the Change ID of the tip
    res = run_jj(["log", "-r", "@", "-T", "change_id"])
    assert res.returncode == 0, f"jj log failed: {res.stderr}"
    actual_id = res.stdout.strip()
    
    assert user_id == actual_id, f"Change ID in file ({user_id}) does not match actual tip Change ID ({actual_id})"
