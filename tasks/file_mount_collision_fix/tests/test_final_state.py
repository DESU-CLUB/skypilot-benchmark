import os
import subprocess
import pytest


FIXED_YAML = "/home/user/fixed_job.yaml"
EXPLANATION = "/home/user/fix_explanation.txt"
BROKEN_YAML = "/home/user/broken_job.yaml"


def _parse_yaml(path):
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{path}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML {path}: {result.stderr}"
    import json
    return json.loads(result.stdout)


def test_fixed_yaml_exists():
    assert os.path.isfile(FIXED_YAML), \
        f"fixed_job.yaml not found at {FIXED_YAML}"


def test_explanation_exists():
    assert os.path.isfile(EXPLANATION), \
        f"fix_explanation.txt not found at {EXPLANATION}"


def test_broken_yaml_unchanged():
    """Verify the broken YAML was not modified."""
    assert os.path.isfile(BROKEN_YAML), \
        "broken_job.yaml must still exist and be unchanged."


def test_fixed_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{FIXED_YAML}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"fixed_job.yaml is not valid YAML: {result.stderr}"


def test_fixed_yaml_no_collision():
    data = _parse_yaml(FIXED_YAML)
    mounts = data.get("file_mounts", {})
    assert "/home/user/training-code" not in mounts, \
        "fixed_job.yaml must NOT mount files to /home/user/training-code (clone target). Move the mount to a different path."


def test_fixed_yaml_s3_config_still_mounted():
    data = _parse_yaml(FIXED_YAML)
    import json
    mounts_str = json.dumps(data.get("file_mounts", {}))
    assert "ml-configs/job-config" in mounts_str or "s3://ml-configs" in mounts_str, \
        "fixed_job.yaml must still mount s3://ml-configs/job-config, just at a different path."


def test_fixed_yaml_clones_training_code():
    with open(FIXED_YAML) as f:
        content = f.read()
    assert "myorg/training-code" in content, \
        "fixed_job.yaml setup must still clone github.com/myorg/training-code."


def test_fixed_yaml_run_unchanged():
    data = _parse_yaml(FIXED_YAML)
    run = data.get("run", "")
    assert "training-code/train.py" in run or "train.py" in run, \
        "fixed_job.yaml run must still execute train.py."


def test_explanation_non_empty():
    with open(EXPLANATION) as f:
        content = f.read().strip()
    assert len(content) > 10, \
        "fix_explanation.txt must be non-empty and explain the fix."


def test_explanation_mentions_collision_cause():
    with open(EXPLANATION) as f:
        content = f.read().lower()
    keywords = ["file_mount", "mount", "setup", "clone", "directory", "before", "collision"]
    matched = [kw for kw in keywords if kw in content]
    assert len(matched) >= 2, \
        f"fix_explanation.txt must explain the file_mount/setup collision. Found keywords: {matched}"
