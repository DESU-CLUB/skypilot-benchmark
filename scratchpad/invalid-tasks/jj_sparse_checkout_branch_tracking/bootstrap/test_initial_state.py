import os
import subprocess
import pytest


REPO_DIR = "/home/user/platform-mono"


def test_jj_binary_exists():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_subdir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_initial_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    output = result.stdout
    assert "main" in output, "Expected bookmark 'main' not found"


def test_remote_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list --all-remotes failed: {result.stderr}"
    output = result.stdout
    assert "infra/terraform-refactor" in output, (
        "Expected remote bookmark 'infra/terraform-refactor' not found"
    )


def test_repo_has_commits():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "Expected repository to have commits"


def test_monorepo_structure_present():
    for subdir in ["infra", "shared", "docs", "services"]:
        path = os.path.join(REPO_DIR, subdir)
        assert os.path.isdir(path), f"Expected directory {path} to exist in repo"
