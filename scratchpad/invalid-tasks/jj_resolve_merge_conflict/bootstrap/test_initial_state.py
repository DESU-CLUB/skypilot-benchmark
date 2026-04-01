import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "config-project")


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_jj_repo_dot_dir_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), ".jj directory not found in repo"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_config_toml_exists():
    result = subprocess.run(
        ["jj", "file", "show", "config.toml", "-r", "main"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"config.toml not found in 'main' commit: {result.stderr}"


def test_bookmark_main_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Bookmark 'main' not found"


def test_bookmark_feature_timeout_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0
    assert "feature-timeout" in result.stdout, "Bookmark 'feature-timeout' not found"


def test_bookmark_feature_retries_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0
    assert "feature-retries" in result.stdout, "Bookmark 'feature-retries' not found"


def test_merge_commit_is_conflicted():
    # The merge commit created by jj new feature-timeout feature-retries should be conflicted
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "change_id ++ \" \" ++ description ++ \" \" ++ conflict ++ \"\\n\""],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # Check that there's at least one commit marked as conflict=true
    assert "true" in result.stdout, "No conflicted commit found in the log"


def test_feature_timeout_changes_timeout_to_60():
    result = subprocess.run(
        ["jj", "file", "show", "config.toml", "-r", "feature-timeout"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not show config.toml at feature-timeout: {result.stderr}"
    assert "timeout = 60" in result.stdout, "feature-timeout branch does not have timeout=60"


def test_feature_retries_changes_timeout_to_10_and_retries_to_5():
    result = subprocess.run(
        ["jj", "file", "show", "config.toml", "-r", "feature-retries"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not show config.toml at feature-retries: {result.stderr}"
    assert "timeout = 10" in result.stdout, "feature-retries branch does not have timeout=10"
    assert "retries = 5" in result.stdout, "feature-retries branch does not have retries=5"
