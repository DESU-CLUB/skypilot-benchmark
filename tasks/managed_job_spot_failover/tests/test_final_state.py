import os
import stat
import subprocess
import pytest


YAML_PATH = "/home/user/managed_train.yaml"
SCRIPT_PATH = "/home/user/submit_job.sh"


def _parse_yaml():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    import json
    return json.loads(result.stdout)


def test_yaml_exists():
    assert os.path.isfile(YAML_PATH), \
        f"managed_train.yaml not found at {YAML_PATH}"


def test_submit_script_exists():
    assert os.path.isfile(SCRIPT_PATH), \
        f"submit_job.sh not found at {SCRIPT_PATH}"


def test_submit_script_is_executable():
    st = os.stat(SCRIPT_PATH)
    is_exec = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_exec, "submit_job.sh must be executable (chmod +x)."


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"managed_train.yaml is not valid YAML: {result.stderr}"


def test_job_name():
    data = _parse_yaml()
    assert data.get("name") == "resilient-train", \
        f"Expected name 'resilient-train', got: {data.get('name')}"


def test_use_spot():
    data = _parse_yaml()
    assert data.get("resources", {}).get("use_spot") is True, \
        "Expected resources.use_spot: true."


def test_a100_accelerator():
    data = _parse_yaml()
    acc = str(data.get("resources", {}).get("accelerators", ""))
    assert "A100" in acc, f"Expected A100 in resources.accelerators, got: {acc}"


def test_any_of_three_clouds():
    data = _parse_yaml()
    import json
    any_of_str = json.dumps(data.get("resources", {}).get("any_of", []))
    assert "aws" in any_of_str.lower(), "Expected AWS in resources.any_of."
    assert "gcp" in any_of_str.lower(), "Expected GCP in resources.any_of."
    assert "azure" in any_of_str.lower(), "Expected Azure in resources.any_of."


def test_job_recovery_strategy_failover():
    data = _parse_yaml()
    recovery = data.get("resources", {}).get("job_recovery", {})
    assert str(recovery.get("strategy", "")).upper() == "FAILOVER", \
        f"Expected job_recovery.strategy: FAILOVER, got: {recovery.get('strategy')}"


def test_max_restarts_on_errors_3():
    data = _parse_yaml()
    recovery = data.get("resources", {}).get("job_recovery", {})
    assert recovery.get("max_restarts_on_errors") == 3, \
        f"Expected max_restarts_on_errors: 3, got: {recovery.get('max_restarts_on_errors')}"


def test_retry_on_exit_codes():
    data = _parse_yaml()
    recovery = data.get("resources", {}).get("job_recovery", {})
    codes = recovery.get("retry_on_return_codes", [])
    codes_int = [int(c) for c in codes]
    assert 33 in codes_int, f"Expected exit code 33 in retry_on_return_codes, got: {codes}"
    assert 1 in codes_int, f"Expected exit code 1 in retry_on_return_codes, got: {codes}"


def test_submit_script_uses_sky_jobs_launch():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky jobs launch" in content, \
        "submit_job.sh must use 'sky jobs launch' to submit the managed job."


def test_submit_script_references_yaml():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "managed_train.yaml" in content, \
        "submit_job.sh must reference managed_train.yaml."


def test_submit_script_non_interactive():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "-y" in content or "--yes" in content, \
        "submit_job.sh must use -y or --yes for non-interactive mode."


def test_submit_script_uses_sky_jobs_queue():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "sky jobs queue" in content, \
        "submit_job.sh must check job status with 'sky jobs queue'."


def test_submit_script_writes_status_log():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "job_status.log" in content, \
        "submit_job.sh must write sky jobs queue output to /home/user/job_status.log."
