import os
import subprocess
import pytest


YAML_PATH = "/home/user/train_job.yaml"


def test_train_job_yaml_exists():
    assert os.path.isfile(YAML_PATH), \
        f"train_job.yaml not found at {YAML_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"train_job.yaml is not valid YAML: {result.stderr}"


def test_accelerator_a100():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml; d=yaml.safe_load(open('{YAML_PATH}')); r=d.get('resources',{{}}); acc=r.get('accelerators',''); print(str(acc))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    output = result.stdout.strip()
    assert "A100" in output, \
        f"Expected 'A100:1' in resources.accelerators, got: {output}"


def test_use_spot_true():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml; d=yaml.safe_load(open('{YAML_PATH}')); r=d.get('resources',{{}}); print(r.get('use_spot',''))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    assert "True" in result.stdout or "true" in result.stdout, \
        f"Expected resources.use_spot: true, got: {result.stdout.strip()}"


def test_autostop_10():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml; d=yaml.safe_load(open('{YAML_PATH}')); r=d.get('resources',{{}}); print(r.get('autostop','not_found'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    assert "10" in result.stdout, \
        f"Expected resources.autostop: 10, got: {result.stdout.strip()}"


def test_any_of_has_aws_and_gcp():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); r=d.get('resources',{{}}); print(json.dumps(r.get('any_of',[])))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    output = result.stdout.strip()
    assert "aws" in output, \
        f"Expected AWS entry in resources.any_of, got: {output}"
    assert "gcp" in output, \
        f"Expected GCP entry in resources.any_of, got: {output}"


def test_setup_installs_torch():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml; d=yaml.safe_load(open('{YAML_PATH}')); print(d.get('setup',''))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    assert "torch" in result.stdout, \
        f"Expected 'torch' in setup section, got: {result.stdout.strip()}"


def test_run_checks_cuda():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml; d=yaml.safe_load(open('{YAML_PATH}')); print(d.get('run',''))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    assert "cuda" in result.stdout.lower() or "torch" in result.stdout.lower(), \
        f"Expected 'torch' or 'cuda' reference in run section, got: {result.stdout.strip()}"
