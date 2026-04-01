import os
import subprocess
import pytest

REPO_DIR = "/home/user/weather_app"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_bookmark_exists():
    result = run_jj(["bookmark", "list", "feature/precip"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/precip" in result.stdout, "Bookmark 'feature/precip' must exist."

def test_final_commit_description():
    result = run_jj(["log", "-r", "feature/precip", "-T", "description", "--no-graph"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    description = result.stdout.strip()
    expected = "feat: complete rain tracking feature"
    assert expected in description, f"Commit description must be '{expected}', got '{description}'"

def test_history_is_squashed():
    # Verify that the old commits are NO LONGER in the history of the feature bookmark
    result = run_jj(["log", "-r", "::feature/precip", "-T", "description\n", "--no-graph"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log_output = result.stdout
    
    forbidden_descriptions = [
        "feat: add rain tracking",
        "fix: calculation error",
        "docs: update readme"
    ]
    
    for desc in forbidden_descriptions:
        assert desc not in log_output, f"Old commit '{desc}' found in history. Squash/cleanup was not completed successfully."

def test_single_commit_structure():
    # The feature/precip commit should be a direct child of the base, so its parent should NOT be one of the intermediate commits.
    # We've already verified the descriptions are gone.
    # Let's verify that the feature/precip commit is not a merge commit (unless specified, but squash usually results in a normal commit)
    result = run_jj(["log", "-r", "feature/precip", "-T", "parents.len()", "--no-graph"])
    assert result.returncode == 0
    # This is a weak check but ensures it's not a complex merge if not intended.
    # A better check for "clean history" is that there is exactly 1 commit with the new description in the revset.
    result = run_jj(["log", "-r", "::feature/precip", "-T", "description\n", "--no-graph"])
    descriptions = [line for line in result.stdout.splitlines() if "feat: complete rain tracking feature" in line]
    assert len(descriptions) == 1, f"Expected exactly 1 commit with the final description, found {len(descriptions)}"

def test_content_merged_via_diff():
    # Verify that the changes from the original commits are present in the final commit.
    # We check the diff of the feature commit relative to its parent.
    result = run_jj(["diff", "-r", "feature/precip"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    diff_output = result.stdout.lower()
    
    # We expect to see changes related to rain tracking and readme updates.
    # Since we don't know exact implementation details, we check for keywords likely present in the diffs (filenames or content).
    
    # "rain" from "rain tracking"
    assert "rain" in diff_output, "Expected 'rain' related changes in the final commit diff."
    
    # "readme" from "docs: update readme" - likely a file path or content
    assert "readme" in diff_output, "Expected 'readme' related changes in the final commit diff."

def test_operation_log_reflects_cleanup():
    result = run_jj(["op", "log", "--limit", "20", "--no-graph"])
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    ops = result.stdout.lower()
    # Looking for operations that imply history rewriting
    valid_ops = ["squash", "amend", "rebase", "describe"]
    assert any(op in ops for op in valid_ops), "Operation log should reflect history cleanup (squash, amend, rebase, or describe)."
