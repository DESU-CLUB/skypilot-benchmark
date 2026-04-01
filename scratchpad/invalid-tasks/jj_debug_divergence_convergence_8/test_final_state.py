import os
import subprocess
import pytest

REPO_DIR = "/home/user/divergence-repo"

def test_bookmark_is_resolved():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-branch" in result.stdout, "Bookmark 'feature-branch' is missing."
    assert "(conflicted)" not in result.stdout, "Bookmark 'feature-branch' is still conflicted."

def test_feature_txt_content():
    result = subprocess.run(
        ["jj", "file", "show", "feature.txt", "-r", "feature-branch"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert result.stdout.strip() == "Resolved changes", f"Expected 'Resolved changes' but got: {result.stdout}"

def test_no_conflicts():
    result = subprocess.run(
        ["jj", "log", "-r", "feature-branch", "--no-graph", "-T", "conflict"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "true" not in result.stdout.lower(), "Commit pointed to by 'feature-branch' has file conflicts."
