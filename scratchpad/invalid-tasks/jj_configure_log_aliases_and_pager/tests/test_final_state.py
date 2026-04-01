import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "myrepo")
CONFIG_FILE = os.path.join(HOME, ".config", "jj", "config.toml")


def _jj(*args):
    """Run a jj command in REPO_DIR with the correct HOME."""
    return subprocess.run(
        ["jj"] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )


def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), (
        f"User config file does not exist: {CONFIG_FILE}"
    )


def test_aliases_ll_is_set():
    result = _jj("config", "get", "aliases.ll")
    assert result.returncode == 0, (
        f"aliases.ll is not set.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_aliases_ll_value_is_correct():
    # jj config get returns a TOML-formatted value for arrays
    result = _jj("config", "get", "aliases.ll")
    assert result.returncode == 0, "aliases.ll is not set"
    output = result.stdout.strip()
    # The value should be a TOML array containing "log", "-r", "::@ ~ root()"
    assert "log" in output, f"aliases.ll does not contain 'log': {output}"
    assert "-r" in output, f"aliases.ll does not contain '-r': {output}"
    assert "::@ ~ root()" in output, (
        f"aliases.ll does not contain '::@ ~ root()': {output}"
    )


def test_revsets_log_is_set():
    result = _jj("config", "get", "revsets.log")
    assert result.returncode == 0, (
        f"revsets.log is not set.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_revsets_log_value_is_correct():
    result = _jj("config", "get", "revsets.log")
    assert result.returncode == 0, "revsets.log is not set"
    output = result.stdout.strip()
    expected = "present(@) | ancestors(immutable_heads().., 2) | trunk()"
    assert expected in output, (
        f"revsets.log does not have the expected value.\n"
        f"Expected to contain: {expected!r}\n"
        f"Got: {output!r}"
    )


def test_ui_paginate_is_set():
    result = _jj("config", "get", "ui.paginate")
    assert result.returncode == 0, (
        f"ui.paginate is not set.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_ui_paginate_value_is_never():
    result = _jj("config", "get", "ui.paginate")
    assert result.returncode == 0, "ui.paginate is not set"
    output = result.stdout.strip()
    assert output == "never", (
        f"ui.paginate should be 'never' but got: {output!r}"
    )


def test_settings_are_user_level():
    """All three settings must be present at the user config level."""
    result = _jj("config", "list", "--user", "aliases.ll")
    assert result.returncode == 0, (
        f"aliases.ll is not set at the user level.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    result2 = _jj("config", "list", "--user", "revsets.log")
    assert result2.returncode == 0, (
        f"revsets.log is not set at the user level.\nstdout: {result2.stdout}\nstderr: {result2.stderr}"
    )
    result3 = _jj("config", "list", "--user", "ui.paginate")
    assert result3.returncode == 0, (
        f"ui.paginate is not set at the user level.\nstdout: {result3.stdout}\nstderr: {result3.stderr}"
    )


def test_ll_alias_runs_as_log():
    """Running jj ll should succeed (alias expands to jj log -r '::@ ~ root()')."""
    result = _jj("ll")
    assert result.returncode == 0, (
        f"jj ll alias failed to run.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
