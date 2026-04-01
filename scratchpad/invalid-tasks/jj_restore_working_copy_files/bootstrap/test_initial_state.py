import os
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = os.path.join(HOME_DIR, "webserver")


def test_jj_binary_exists():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    readme = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md not found at {readme}"


def test_cargo_toml_exists():
    cargo = os.path.join(REPO_DIR, "Cargo.toml")
    assert os.path.isfile(cargo), f"Cargo.toml not found at {cargo}"


def test_src_directory_exists():
    src = os.path.join(REPO_DIR, "src")
    assert os.path.isdir(src), f"src/ directory not found at {src}"


def test_initial_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'initial project scaffold')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial project scaffold" in result.stdout, (
        "Expected commit with description 'initial project scaffold' not found"
    )


def test_working_copy_description_is_add_rate_limiting():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'add rate limiting feature')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add rate limiting feature" in result.stdout, (
        "Expected working-copy description 'add rate limiting feature' not found"
    )


def test_main_rs_has_been_accidentally_modified():
    main_rs = os.path.join(REPO_DIR, "src", "main.rs")
    assert os.path.isfile(main_rs), f"src/main.rs does not exist at {main_rs}"
    with open(main_rs) as f:
        content = f.read()
    assert "TODO: placeholder - needs rewrite" in content, (
        "src/main.rs should contain the accidentally written placeholder content"
    )


def test_config_rs_has_been_accidentally_deleted():
    config_rs = os.path.join(REPO_DIR, "src", "config.rs")
    assert not os.path.isfile(config_rs), (
        "src/config.rs should be deleted (accidental deletion scenario)"
    )


def test_readme_contains_contributor():
    readme = os.path.join(REPO_DIR, "README.md")
    with open(readme) as f:
        content = f.read()
    assert "contributor" in content, (
        "README.md should contain 'contributor' from the intentional edit"
    )


def test_working_copy_shows_changes():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0
    # The working copy should show some changes (README.md modified, main.rs modified, config.rs deleted)
    assert result.stdout.strip() != "", "jj status should show changes in the working copy"
