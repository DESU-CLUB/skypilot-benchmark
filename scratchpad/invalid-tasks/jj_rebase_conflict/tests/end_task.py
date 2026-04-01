import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_config_content_resolved():
    config_path = os.path.join(REPO_DIR, "config.toml")
    assert os.path.isfile(config_path), "config.toml is missing."
    
    with open(config_path, "r") as f:
        content = f.read()
    
    assert 'version = "1.1-beta"' in content, f"Expected 'version = \"1.1-beta\"' in config.toml, found:\n{content}"
    assert 'name = "my-app"' in content, "config.toml missing 'name = \"my-app\"'"
    
    assert "<<<<<<<" not in content, "Conflict markers found in config.toml"
    assert ">>>>>>>" not in content, "Conflict markers found in config.toml"

def test_jj_status_clean():
    result = run_jj(["status"])
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    assert "Conflicted" not in result.stdout, f"jj status reports conflicts:\n{result.stdout}"
    
    result_resolve = run_jj(["resolve", "--list"])
    assert result_resolve.returncode == 0
    assert not result_resolve.stdout.strip(), f"Unresolved conflicts found:\n{result_resolve.stdout}"

def test_solution_file():
    solution_path = os.path.join(REPO_DIR, "solution.txt")
    assert os.path.isfile(solution_path), "solution.txt is missing."
    
    with open(solution_path, "r") as f:
        content = f.read()
    
    assert "set beta version" in content, f"solution.txt missing 'set beta version'. Content:\n{content}"
