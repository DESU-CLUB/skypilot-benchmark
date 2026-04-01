import os
import subprocess
import pytest


REPO_DIR = "/home/user/proj"
RECOVERY_REPORT = "/home/user/proj/recovery_report.txt"


def test_all_four_commits_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    assert "init: project scaffold" in output, "Missing 'init: project scaffold' in log"
    assert "feat: add login module" in output, "Missing 'feat: add login module' in log"
    assert "feat: add dashboard module" in output, "Missing 'feat: add dashboard module' in log"
    assert "wip: dashboard styling" in output, "Missing 'wip: dashboard styling' in log"


def test_bookmark_recovered_dashboard_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "recovered-dashboard" in result.stdout, (
        "Bookmark 'recovered-dashboard' not found"
    )


def test_bookmark_points_to_wip_dashboard_styling():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "recovered-dashboard"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for bookmark failed: {result.stderr}"
    assert "wip: dashboard styling" in result.stdout, (
        "Bookmark 'recovered-dashboard' does not point to 'wip: dashboard styling'"
    )


def test_recovery_report_exists():
    assert os.path.isfile(RECOVERY_REPORT), (
        f"recovery_report.txt not found at {RECOVERY_REPORT}"
    )


def test_recovery_report_abandoned_commits_line():
    with open(RECOVERY_REPORT, "r") as f:
        content = f.read()
    lines = {line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
             for line in content.splitlines() if ":" in line}
    assert "abandoned_commits" in lines, "Missing 'abandoned_commits:' line in recovery_report.txt"
    val = lines["abandoned_commits"]
    assert "feat: add dashboard module" in val, (
        "abandoned_commits should include 'feat: add dashboard module'"
    )
    assert "wip: dashboard styling" in val, (
        "abandoned_commits should include 'wip: dashboard styling'"
    )


def test_recovery_report_recovery_method_line():
    with open(RECOVERY_REPORT, "r") as f:
        content = f.read()
    lines = {line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
             for line in content.splitlines() if ":" in line}
    assert "recovery_method" in lines, "Missing 'recovery_method:' line in recovery_report.txt"
    assert "op restore" in lines["recovery_method"], (
        "recovery_method should be 'op restore'"
    )


def test_recovery_report_bookmark_created_line():
    with open(RECOVERY_REPORT, "r") as f:
        content = f.read()
    lines = {line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
             for line in content.splitlines() if ":" in line}
    assert "bookmark_created" in lines, "Missing 'bookmark_created:' line in recovery_report.txt"
    assert "recovered-dashboard" in lines["bookmark_created"], (
        "bookmark_created should be 'recovered-dashboard'"
    )


def test_working_copy_is_on_or_above_wip_dashboard_styling():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "ancestors(@, 5)"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for ancestors failed: {result.stderr}"
    assert "wip: dashboard styling" in result.stdout, (
        "Working copy is not on or above 'wip: dashboard styling'"
    )
