import os
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = os.path.join(HOME_DIR, "webserver")


def test_jj_repo_still_valid():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_rs_restored_to_original_content():
    main_rs = os.path.join(REPO_DIR, "src", "main.rs")
    assert os.path.isfile(main_rs), f"src/main.rs does not exist at {main_rs}"
    with open(main_rs) as f:
        content = f.read()
    assert 'println!("Starting webserver...")' in content, (
        'src/main.rs should contain println!("Starting webserver...") from original content'
    )
    assert "TODO: placeholder - needs rewrite" not in content, (
        "src/main.rs should NOT contain the accidentally written placeholder content"
    )


def test_config_rs_exists_and_has_original_content():
    config_rs = os.path.join(REPO_DIR, "src", "config.rs")
    assert os.path.isfile(config_rs), (
        f"src/config.rs must exist at {config_rs} — it was accidentally deleted and should be restored"
    )
    with open(config_rs) as f:
        content = f.read()
    assert "struct Config" in content, (
        "src/config.rs should contain 'struct Config' from the original content"
    )


def test_readme_still_contains_contributor_edit():
    readme = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md not found at {readme}"
    with open(readme) as f:
        content = f.read()
    assert "contributor" in content, (
        "README.md must still contain 'contributor' — the intentional edit must be preserved"
    )


def test_status_shows_only_readme_modified():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    status_output = result.stdout
    # README.md should appear as modified
    assert "README.md" in status_output, (
        "jj status should show README.md as modified (intentional change preserved)"
    )
    # src/main.rs should NOT appear (it was restored)
    assert "main.rs" not in status_output, (
        "jj status should NOT show src/main.rs (it should be restored to match parent)"
    )
    # src/config.rs should NOT appear (it was restored)
    assert "config.rs" not in status_output, (
        "jj status should NOT show src/config.rs (it should be restored to match parent)"
    )


def test_working_copy_commit_description_unchanged():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'add rate limiting feature')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add rate limiting feature" in result.stdout, (
        "Working-copy commit should still have description 'add rate limiting feature'"
    )


def test_initial_scaffold_commit_still_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'initial project scaffold')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial project scaffold" in result.stdout, (
        "The 'initial project scaffold' commit must still exist in history"
    )


def test_no_extra_commits_created():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    # Should have exactly 2 non-empty descriptions (the root commit has empty description)
    non_empty = [l for l in lines if l]
    assert len(non_empty) == 2, (
        f"Expected exactly 2 commits with descriptions (initial + add rate limiting), got {len(non_empty)}: {non_empty}"
    )
