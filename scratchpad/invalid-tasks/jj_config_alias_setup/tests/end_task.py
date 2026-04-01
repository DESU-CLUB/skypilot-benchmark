import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_local_config_file_exists_and_content():
    config_path = os.path.join(REPO_DIR, ".jj/repo/config.toml")
    assert os.path.isfile(config_path), ".jj/repo/config.toml does not exist. Configuration must be repository-local."
    
    with open(config_path, "r") as f:
        content = f.read()
    
    assert "Dev One" in content, "user.name 'Dev One' not found in local config.toml"
    assert "dev@company.com" in content, "user.email 'dev@company.com' not found in local config.toml"
    assert "st" in content, "Alias 'st' not found in local config.toml"
    assert "status" in content, "Alias target 'status' not found in local config.toml"

def test_effective_config_values():
    # Verify user.name
    res_name = run_jj(["config", "get", "user.name"])
    assert res_name.returncode == 0, f"jj config get user.name failed: {res_name.stderr}"
    assert "Dev One" in res_name.stdout, f"Effective user.name is not 'Dev One'. Got: {res_name.stdout.strip()}"

    # Verify user.email
    res_email = run_jj(["config", "get", "user.email"])
    assert res_email.returncode == 0, f"jj config get user.email failed: {res_email.stderr}"
    assert "dev@company.com" in res_email.stdout, f"Effective user.email is not 'dev@company.com'. Got: {res_email.stdout.strip()}"

    # Verify alias
    res_alias = run_jj(["config", "get", "aliases.st"])
    assert res_alias.returncode == 0, f"jj config get aliases.st failed: {res_alias.stderr}"
    assert "status" in res_alias.stdout, f"Effective alias 'st' does not resolve to 'status'. Got: {res_alias.stdout.strip()}"

def test_readme_modified_content():
    readme_path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme_path), "README.md is missing."
    
    with open(readme_path, "r") as f:
        content = f.read()
    
    assert "# Project Documentation" in content, "Original README content missing."
    assert "Environment verified." in content, "'Environment verified.' not found in README.md"

def test_verification_file_content():
    ver_path = os.path.join(REPO_DIR, "verification.txt")
    assert os.path.isfile(ver_path), "verification.txt is missing."
    
    with open(ver_path, "r") as f:
        content = f.read()
    
    # Check that it resembles status output and mentions README.md
    assert "README.md" in content, "verification.txt does not mention README.md modification."
    
    # Run status to compare basics
    status_res = run_jj(["status"])
    assert status_res.returncode == 0
    
    # If the file was created using `jj st > verification.txt`, it should match roughly
    # We check for key indicators of a modified file in status output
    # Usually "Modified regular file README.md" or similar
    # We'll just assert that the file is not empty and contains the filename
    assert len(content.strip()) > 0, "verification.txt is empty."
