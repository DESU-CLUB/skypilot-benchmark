import os
import subprocess
import pytest


YAML_PATH = "/home/user/inference_job.yaml"


def _parse_yaml():
    result = subprocess.run(
        ["python3", "-c",
         f"import yaml, json; d=yaml.safe_load(open('{YAML_PATH}')); print(json.dumps(d, default=str))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse YAML: {result.stderr}"
    import json
    return json.loads(result.stdout)


def test_inference_job_yaml_exists():
    assert os.path.isfile(YAML_PATH), \
        f"inference_job.yaml not found at {YAML_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"inference_job.yaml is not valid YAML: {result.stderr}"


def test_job_name_batch_inference():
    data = _parse_yaml()
    assert data.get("name") == "batch-inference", \
        f"Expected name 'batch-inference', got: {data.get('name')}"


def test_accelerators_a100_4():
    data = _parse_yaml()
    resources = data.get("resources", {})
    acc = str(resources.get("accelerators", ""))
    assert "A100" in acc and "4" in acc, \
        f"Expected resources.accelerators: A100:4, got: {acc}"


def test_use_spot():
    data = _parse_yaml()
    resources = data.get("resources", {})
    assert resources.get("use_spot") is True, \
        f"Expected resources.use_spot: true, got: {resources.get('use_spot')}"


def test_file_mounts_data_mount_cached():
    data = _parse_yaml()
    mounts = data.get("file_mounts", {})
    data_mount = mounts.get("/data", {})
    assert data_mount, "Expected /data entry in file_mounts."
    assert "ml-datasets/imagenet" in str(data_mount.get("source", "")), \
        f"Expected /data source to be s3://ml-datasets/imagenet, got: {data_mount.get('source')}"
    assert str(data_mount.get("mode", "")).upper() == "MOUNT_CACHED", \
        f"Expected /data mount mode MOUNT_CACHED, got: {data_mount.get('mode')}"


def test_file_mounts_checkpoint_copy():
    data = _parse_yaml()
    mounts = data.get("file_mounts", {})
    chk_mount = mounts.get("/checkpoint", {})
    assert chk_mount, "Expected /checkpoint entry in file_mounts."
    assert "ml-checkpoints/resnet50" in str(chk_mount.get("source", "")), \
        f"Expected /checkpoint source to be s3://ml-checkpoints/resnet50, got: {chk_mount.get('source')}"
    assert str(chk_mount.get("mode", "")).upper() == "COPY", \
        f"Expected /checkpoint mount mode COPY, got: {chk_mount.get('mode')}"


def test_setup_installs_packages():
    data = _parse_yaml()
    setup = data.get("setup", "")
    assert "torch" in setup, "Expected setup to install torch."
    assert "torchvision" in setup, "Expected setup to install torchvision."
    assert "boto3" in setup, "Expected setup to install boto3."


def test_run_executes_infer():
    data = _parse_yaml()
    run = data.get("run", "")
    assert "infer.py" in run, f"Expected run to execute infer.py, got: {run}"
    assert "/data" in run, f"Expected run to reference /data mount, got: {run}"
    assert "/checkpoint" in run, f"Expected run to reference /checkpoint mount, got: {run}"
