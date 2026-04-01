import os
import pytest
import subprocess

def test_initial_state():
    home = os.environ.get("HOME", "/home/user")
    repo_path = os.path.join(home, "monorepo")
    
    # Check that repo does NOT exist initially (the user will create it)
    assert not os.path.exists(repo_path), f"Repo {repo_path} should not exist before the task."
