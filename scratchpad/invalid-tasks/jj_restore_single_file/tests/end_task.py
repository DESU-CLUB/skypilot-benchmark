import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_utils_py_content():
    file_path = os.path.join(REPO_DIR, "src", "utils.py")
    assert os.path.exists(file_path), f"{file_path} does not exist"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Truth: src/utils.py MUST contain exactly:
    # def help():
    #     print("helping")
    expected_content = 'def help():\n    print("helping")'
    
    assert expected_content.strip() == content.strip(), \
        f"src/utils.py content does not match expected state.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_ideas_md_preserved():
    file_path = os.path.join(REPO_DIR, "src", "ideas.md")
    assert os.path.exists(file_path), f"{file_path} does not exist"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Truth: src/ideas.md MUST exist and contain Refactor plan: ...
    assert "Refactor plan:" in content, \
        f"src/ideas.md does not contain expected text 'Refactor plan:'.\nGot:\n{content}"

def test_final_status_report_artifact():
    report_path = os.path.join(REPO_DIR, "final_status.txt")
    assert os.path.exists(report_path), "final_status.txt does not exist"
    
    with open(report_path, "r") as f:
        content = f.read()
    
    # Truth: The content of final_status.txt must NOT show src/utils.py as modified.
    assert "src/utils.py" not in content, \
        f"final_status.txt implies src/utils.py is modified/tracked, but it should be clean.\nReport content:\n{content}"
    
    # Truth: The content of final_status.txt SHOULD show src/ideas.md
    assert "src/ideas.md" in content, \
        f"final_status.txt does not list src/ideas.md, but it should be present (as new/modified).\nReport content:\n{content}"

def test_actual_repo_status():
    # Verify the actual repository state using jj, confirming the user's action
    result = run_jj(["status"])
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    
    # src/utils.py should be clean (restored to parent)
    assert "src/utils.py" not in result.stdout, \
        f"jj status shows src/utils.py as modified, but it should be clean.\nOutput:\n{result.stdout}"
    
    # src/ideas.md should be present (either added or untracked)
    assert "src/ideas.md" in result.stdout, \
        f"jj status does not show src/ideas.md, but it should be present.\nOutput:\n{result.stdout}"
