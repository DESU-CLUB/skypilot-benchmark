import os
import shutil
import subprocess
import pytest


REPO_DIR = "/home/user/audit-repo"
AUDIT_SUMMARY_LOG = "/home/user/audit-repo/audit_summary.log"
AUDIT_FULL_LOG = "/home/user/audit-repo/audit_full.log"
AUDIT_TICKETS_LOG = "/home/user/audit-repo/audit_tickets.log"


def test_audit_summary_log_exists():
    assert os.path.isfile(AUDIT_SUMMARY_LOG), f"File does not exist: {AUDIT_SUMMARY_LOG}"


def test_audit_full_log_exists():
    assert os.path.isfile(AUDIT_FULL_LOG), f"File does not exist: {AUDIT_FULL_LOG}"


def test_audit_tickets_log_exists():
    assert os.path.isfile(AUDIT_TICKETS_LOG), f"File does not exist: {AUDIT_TICKETS_LOG}"


def test_audit_summary_log_has_5_lines():
    with open(AUDIT_SUMMARY_LOG, "r") as f:
        lines = [l for l in f.readlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 lines in audit_summary.log, got {len(lines)}"


def test_audit_summary_log_contains_email():
    with open(AUDIT_SUMMARY_LOG, "r") as f:
        content = f.read()
    assert "data-bot@company.com" in content, "audit_summary.log does not contain data-bot@company.com"


def test_audit_summary_log_pipe_separated():
    with open(AUDIT_SUMMARY_LOG, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    for line in lines:
        parts = line.split(" | ")
        assert len(parts) == 3, f"Expected 3 pipe-separated fields in line: {line!r}"
        commit_id_prefix, email, first_line = parts
        assert len(commit_id_prefix) == 8, f"Expected 8-char commit id prefix, got {commit_id_prefix!r}"
        assert "@" in email, f"Expected email in second field, got {email!r}"
        assert len(first_line) > 0, f"Expected non-empty description first line"


def test_audit_summary_log_contains_all_descriptions():
    with open(AUDIT_SUMMARY_LOG, "r") as f:
        content = f.read()
    expected_descriptions = [
        "ingest: load raw CSV files from landing zone",
        "transform: normalize column types and rename fields",
        "validate: run schema checks on transformed dataset",
        "enrich: join with reference table for geo lookups",
        "export: write final parquet files to output bucket",
    ]
    for desc in expected_descriptions:
        assert desc in content, f"Description not found in audit_summary.log: {desc}"


def test_audit_full_log_has_5_blocks():
    with open(AUDIT_FULL_LOG, "r") as f:
        content = f.read()
    separators = [line for line in content.splitlines() if line.strip() == "---"]
    assert len(separators) == 5, f"Expected 5 '---' separators in audit_full.log, got {len(separators)}"


def test_audit_full_log_has_required_keys():
    with open(AUDIT_FULL_LOG, "r") as f:
        content = f.read()
    required_keys = ["commit_id=", "author=", "author_email=", "timestamp=", "description="]
    for key in required_keys:
        assert key in content, f"Required key not found in audit_full.log: {key}"


def test_audit_full_log_commit_ids_are_full_length():
    with open(AUDIT_FULL_LOG, "r") as f:
        lines = f.readlines()
    commit_id_lines = [l.strip() for l in lines if l.startswith("commit_id=")]
    assert len(commit_id_lines) == 5, f"Expected 5 commit_id= lines, got {len(commit_id_lines)}"
    for line in commit_id_lines:
        val = line[len("commit_id="):]
        assert len(val) >= 40, f"Expected full commit id (>=40 chars), got {val!r}"


def test_audit_full_log_timestamps_utc_format():
    with open(AUDIT_FULL_LOG, "r") as f:
        lines = f.readlines()
    ts_lines = [l.strip() for l in lines if l.startswith("timestamp=")]
    assert len(ts_lines) == 5, f"Expected 5 timestamp= lines, got {len(ts_lines)}"
    import re
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    for line in ts_lines:
        val = line[len("timestamp="):]
        assert pattern.match(val), f"Timestamp does not match expected format: {val!r}"


def test_audit_full_log_author_email_present():
    with open(AUDIT_FULL_LOG, "r") as f:
        lines = f.readlines()
    email_lines = [l.strip() for l in lines if l.startswith("author_email=")]
    assert len(email_lines) == 5, f"Expected 5 author_email= lines, got {len(email_lines)}"
    for line in email_lines:
        val = line[len("author_email="):]
        assert val == "data-bot@company.com", f"Unexpected author_email: {val!r}"


def test_audit_tickets_log_has_5_lines():
    with open(AUDIT_TICKETS_LOG, "r") as f:
        lines = [l for l in f.readlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 lines in audit_tickets.log, got {len(lines)}"


def test_audit_tickets_log_contains_all_tickets():
    with open(AUDIT_TICKETS_LOG, "r") as f:
        content = f.read()
    expected_tickets = ["DATA-101", "DATA-102", "DATA-103", "DATA-104", "DATA-105"]
    for ticket in expected_tickets:
        assert ticket in content, f"Ticket not found in audit_tickets.log: {ticket}"


def test_audit_tickets_log_format():
    with open(AUDIT_TICKETS_LOG, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    for line in lines:
        assert " | Ticket=" in line, f"Line does not contain ' | Ticket=': {line!r}"
        parts = line.split(" | Ticket=")
        assert len(parts) == 2, f"Expected exactly one ' | Ticket=' separator: {line!r}"
        ticket_val = parts[1]
        assert ticket_val.startswith("DATA-"), f"Ticket value does not start with DATA-: {ticket_val!r}"


def test_jj_log_still_shows_5_commits():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "root()..@-", "-T", "commit_id ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 commits still in repo, got {len(lines)}"
