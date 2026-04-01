import os
import shutil
import subprocess
import pytest


REPO_DIR = "/home/user/audit-repo"


def test_jj_binary_in_path():
    assert shutil.which("jj") is not None, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory does not exist: {REPO_DIR}"


def test_jj_directory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory does not exist in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_commit_count():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "root()..@-", "-T", "commit_id ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 commits, got {len(lines)}"


def test_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "root()..@-", "-T", "description.first_line() ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    expected_descriptions = [
        "ingest: load raw CSV files from landing zone",
        "transform: normalize column types and rename fields",
        "validate: run schema checks on transformed dataset",
        "enrich: join with reference table for geo lookups",
        "export: write final parquet files to output bucket",
    ]
    for desc in expected_descriptions:
        assert desc in output, f"Expected description not found: {desc}"


def test_author_email():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "root()..@-", "-T", "author.email() ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    for line in lines:
        assert line == "data-bot@company.com", f"Unexpected author email: {line}"


def test_ticket_trailers_present():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph", "-r", "root()..@-",
            "-T", "trailers.filter(|t| t.key() == \"Ticket\").map(|t| t.value()).join(\",\") ++ \"\\n\"",
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 ticket trailer lines, got {len(lines)}"
    expected_tickets = {"DATA-101", "DATA-102", "DATA-103", "DATA-104", "DATA-105"}
    found_tickets = set(lines)
    assert found_tickets == expected_tickets, f"Ticket mismatch: {found_tickets}"


def test_audit_log_files_do_not_exist_yet():
    for fname in ["audit_summary.log", "audit_full.log", "audit_tickets.log"]:
        path = os.path.join(REPO_DIR, fname)
        assert not os.path.exists(path), f"File should not exist yet: {path}"
