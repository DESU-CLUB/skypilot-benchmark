import os
import subprocess
import pytest


YAML_PATH = "/home/user/distributed_job.yaml"
SCRIPT_PATH = "/home/user/train.py"


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
        f"distributed_job.yaml not found at {YAML_PATH}"


def test_train_py_exists():
    assert os.path.isfile(SCRIPT_PATH), \
        f"train.py not found at {SCRIPT_PATH}"


def test_yaml_is_valid():
    result = subprocess.run(
        ["python3", "-c", f"import yaml; yaml.safe_load(open('{YAML_PATH}'))"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"distributed_job.yaml is not valid YAML: {result.stderr}"


def test_train_py_is_valid_python():
    result = subprocess.run(
        ["python3", "-m", "py_compile", SCRIPT_PATH],
        capture_output=True, text=True
    )
    assert result.returncode == 0, \
        f"train.py has a syntax error: {result.stderr}"


def test_job_name():
    data = _parse_yaml()
    assert data.get("name") == "ray-distributed-train", \
        f"Expected name 'ray-distributed-train', got: {data.get('name')}"


def test_num_nodes_2():
    data = _parse_yaml()
    assert data.get("num_nodes") == 2, \
        f"Expected num_nodes: 2, got: {data.get('num_nodes')}"


def _strip_comments(text, comment_char="#"):
    """Return only non-comment portions of each line."""
    lines = []
    for line in text.splitlines():
        code = line.split(comment_char, 1)[0]
        lines.append(code)
    return "\n".join(lines)


def test_yaml_uses_port_6379_not_6380():
    with open(YAML_PATH) as f:
        content = f.read()
    code_only = _strip_comments(content)
    assert "6380" not in code_only, \
        "distributed_job.yaml must NOT use port 6380 (reserved for SkyPilot's internal Ray)."
    assert "6379" in content, \
        "distributed_job.yaml must use port 6379 for the user's Ray cluster."


def test_yaml_references_node_rank():
    with open(YAML_PATH) as f:
        content = f.read()
    assert "SKYPILOT_NODE_RANK" in content, \
        "distributed_job.yaml must use $SKYPILOT_NODE_RANK to distinguish head from worker nodes."


def test_yaml_starts_ray_head():
    with open(YAML_PATH) as f:
        content = f.read()
    assert "ray start" in content and "--head" in content, \
        "distributed_job.yaml must contain 'ray start --head' command."


def test_train_py_imports_ray():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "import ray" in content, \
        "train.py must import ray."


def test_train_py_uses_port_6379():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    code_only = _strip_comments(content)
    assert "6379" in content, \
        "train.py must connect to the Ray cluster on port 6379."
    assert "6380" not in code_only, \
        "train.py must NOT use port 6380 (SkyPilot's internal Ray port)."


def test_train_py_no_address_auto():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    code_only = _strip_comments(content)
    assert "address='auto'" not in code_only and 'address="auto"' not in code_only, \
        "train.py must NOT use ray.init(address='auto') — this connects to SkyPilot's internal Ray."


def test_train_py_uses_remote():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "@ray.remote" in content, \
        "train.py must define at least one @ray.remote function."
