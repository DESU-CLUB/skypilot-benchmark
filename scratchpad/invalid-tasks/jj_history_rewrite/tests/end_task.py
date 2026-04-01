import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
LOG_FILE = os.path.join(REPO_DIR, "jj_log.txt")

def test_final_history_structure():
    # Check feature B exists
    res_b = subprocess.run(["jj", "log", "-r", 'description("feature B")', "--template", 'commit_id'], cwd=REPO_DIR, capture_output=True, text=True)
    assert res_b.returncode == 0 and res_b.stdout.strip(), "Commit 'feature B' not found."
    
    # Check feature A exists
    res_a = subprocess.run(["jj", "log", "-r", 'description("feature A")', "--template", 'commit_id'], cwd=REPO_DIR, capture_output=True, text=True)
    assert res_a.returncode == 0 and res_a.stdout.strip(), "Commit 'feature A' not found."

    # Check feature B is child of feature A
    res_parent = subprocess.run(["jj", "log", "-r", 'description("feature B")', "--template", 'parents.map(|p| p.description()).join(" ")'], cwd=REPO_DIR, capture_output=True, text=True)
    assert "feature A" in res_parent.stdout, f"Commit 'feature B' does not have 'feature A' as parent. Parent is: {res_parent.stdout}"

def test_file_contents_feature_a():
    # Check content of feature A
    cmd = ["jj", "cat", "file_a.txt", "-r", 'description("feature A")']
    res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Failed to cat file_a.txt: {res.stderr}"
    expected_a = "Line 1\nLine 2\nFeature A\nTypo fix\nMore fixes\n"
    # Normalize newlines just in case
    assert res.stdout.replace('\r\n', '\n') == expected_a, f"file_a.txt content mismatch in feature A commit."

    cmd = ["jj", "cat", "file_b.txt", "-r", 'description("feature A")']
    res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    expected_b_initial = "Line 1\nLine 2\n"
    assert res.stdout.replace('\r\n', '\n') == expected_b_initial, f"file_b.txt content mismatch in feature A commit."

def test_file_contents_feature_b():
    # Check content of feature B
    cmd = ["jj", "cat", "file_b.txt", "-r", 'description("feature B")']
    res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    expected_b = "Line 1\nLine 2\nFeature B\nWorking copy change\n"
    assert res.stdout.replace('\r\n', '\n') == expected_b, f"file_b.txt content mismatch in feature B commit."

    cmd = ["jj", "cat", "file_a.txt", "-r", 'description("feature B")']
    res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    expected_a = "Line 1\nLine 2\nFeature A\nTypo fix\nMore fixes\n"
    assert res.stdout.replace('\r\n', '\n') == expected_a, f"file_a.txt content mismatch in feature B commit."

def test_log_file_verification():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} not found."
    with open(LOG_FILE, "r") as f:
        content = f.read()
    assert "feature A" in content, "Log file missing 'feature A'"
    assert "feature B" in content, "Log file missing 'feature B'"
