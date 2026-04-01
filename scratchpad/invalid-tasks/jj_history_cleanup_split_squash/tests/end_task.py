import os
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/messy_project"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_clean_working_copy():
    result = run_jj(["diff"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", f"Working copy is not clean. Diff:\n{result.stdout}"

def test_history_descriptions():
    result = run_jj(["log", "-r", "::", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    
    log_output = result.stdout
    descriptions = [line.strip() for line in log_output.splitlines() if line.strip()]
    
    required_commits = [
        "initial commit",
        "feat: add logger",
        "fix: crash in main",
        "docs: update readme"
    ]
    
    for desc in required_commits:
        assert desc in descriptions, f"Expected commit '{desc}' not found in history."
        
    assert "wip: all the things" not in descriptions, "Commit 'wip: all the things' should not be in the history."

def test_logger_content():
    revset = 'description("feat: add logger")'
    result = run_jj(["file", "show", "src/logger.py", "-r", revset])
    assert result.returncode == 0, f"Failed to show src/logger.py at '{revset}': {result.stderr}"
    
    content = result.stdout
    assert "import sys" in content, "src/logger.py in 'feat: add logger' missing 'import sys'"
    assert "def log(msg):" in content, "src/logger.py in 'feat: add logger' missing 'def log(msg):'"

def test_main_fix_content():
    revset = 'description("fix: crash in main")'
    result = run_jj(["file", "show", "src/main.py", "-r", revset])
    assert result.returncode == 0, f"Failed to show src/main.py at '{revset}': {result.stderr}"
    
    content = result.stdout
    assert "raise Exception" not in content, "src/main.py in 'fix: crash in main' still contains 'raise Exception'"

def test_readme_content():
    revset = 'description("docs: update readme")'
    result = run_jj(["file", "show", "README.md", "-r", revset])
    assert result.returncode == 0, f"Failed to show README.md at '{revset}': {result.stderr}"
    
    content = result.stdout
    assert "- Added logging" in content, "README.md in 'docs: update readme' missing '- Added logging'"
