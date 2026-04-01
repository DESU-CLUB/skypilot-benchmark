import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "config-project")


def _jj(*args):
    return subprocess.run(
        ["jj"] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )


def test_main_bookmark_has_no_conflicts():
    result = _jj("resolve", "--list", "-r", "main")
    assert result.returncode == 0, f"jj resolve --list -r main failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        "Expected no conflicts on 'main', but got: " + result.stdout
    )


def test_main_commit_description():
    result = _jj("log", "--no-graph", "-T", "description", "-r", "main")
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Merge feature-timeout and feature-retries: resolve timeout conflict" in result.stdout, (
        "Expected merge commit description not found. Got: " + result.stdout
    )


def test_main_commit_has_two_parents():
    result = _jj("log", "--no-graph", "-T", "parents.len()", "-r", "main")
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "2" in result.stdout, (
        "Expected main commit to have 2 parents, got: " + result.stdout
    )


def test_main_commit_parents_are_feature_branches():
    result = _jj(
        "log", "--no-graph",
        "-T", r'description ++ "\n"',
        "-r", "parents(main)",
    )
    assert result.returncode == 0, f"jj log parents(main) failed: {result.stderr}"
    assert "Increase timeout to 60 for slow networks" in result.stdout, (
        "feature-timeout commit not found among parents of main"
    )
    assert "Reduce timeout to 10 and increase retries to 5" in result.stdout, (
        "feature-retries commit not found among parents of main"
    )


def test_resolved_config_toml_has_correct_values():
    result = _jj("file", "show", "config.toml", "-r", "main")
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    content = result.stdout
    assert "timeout = 60" in content, "Expected timeout=60 in config.toml, got: " + content
    assert "retries = 5" in content, "Expected retries=5 in config.toml, got: " + content
    assert 'host = "localhost"' in content, "Expected host=localhost in config.toml"
    assert "port = 8080" in content, "Expected port=8080 in config.toml"
    assert 'log_level = "info"' in content, "Expected log_level=info in config.toml"


def test_no_conflict_markers_in_resolved_config():
    result = _jj("file", "show", "config.toml", "-r", "main")
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    content = result.stdout
    assert "<<<<<<<" not in content, "Conflict marker '<<<<<<<' still present in config.toml"
    assert ">>>>>>>" not in content, "Conflict marker '>>>>>>>' still present in config.toml"
    assert "+++++++" not in content, "Conflict marker '+++++++' still present in config.toml"
    assert "%%%%%%%" not in content, "Conflict marker '%%%%%%%' still present in config.toml"


def test_feature_timeout_bookmark_still_exists():
    result = _jj("bookmark", "list")
    assert result.returncode == 0
    assert "feature-timeout" in result.stdout, "Bookmark 'feature-timeout' should still exist"


def test_feature_retries_bookmark_still_exists():
    result = _jj("bookmark", "list")
    assert result.returncode == 0
    assert "feature-retries" in result.stdout, "Bookmark 'feature-retries' should still exist"


def test_main_points_to_merge_commit_with_two_parents():
    result = _jj("log", "--no-graph", "-T", "parents.len()", "-r", "main")
    assert result.returncode == 0
    assert "2" in result.stdout, (
        "main bookmark does not point to a merge commit (should have 2 parents)"
    )


def test_working_copy_has_no_conflicts():
    result = _jj("resolve", "--list")
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        "Working copy still has conflicts: " + result.stdout
    )
