import os
import subprocess
import pytest


REPO_DIR = "/home/user/platform-mono"
BACKEND_TF = "/home/user/platform-mono/infra/terraform/backend.tf"

EXPECTED_SPARSE_PATTERNS = ["infra/", "shared/", "docs/", "services/notifications/"]

EXPECTED_BACKEND_TF_CONTENT = (
    'terraform {\n'
    '  backend "s3" {\n'
    '    bucket = "platform-tf-state"\n'
    '    key    = "infra/terraform.tfstate"\n'
    '    region = "us-west-2"\n'
    '  }\n'
    '}\n'
)


def test_sparse_patterns_infra():
    result = subprocess.run(
        ["jj", "sparse", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj sparse list failed: {result.stderr}"
    assert "infra/" in result.stdout, "Sparse pattern 'infra/' not found"


def test_sparse_patterns_shared():
    result = subprocess.run(
        ["jj", "sparse", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj sparse list failed: {result.stderr}"
    assert "shared/" in result.stdout, "Sparse pattern 'shared/' not found"


def test_sparse_patterns_docs():
    result = subprocess.run(
        ["jj", "sparse", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj sparse list failed: {result.stderr}"
    assert "docs/" in result.stdout, "Sparse pattern 'docs/' not found"


def test_sparse_patterns_services_notifications():
    result = subprocess.run(
        ["jj", "sparse", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj sparse list failed: {result.stderr}"
    assert "services/notifications/" in result.stdout, (
        "Sparse pattern 'services/notifications/' not found"
    )


def test_tracked_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "infra/terraform-refactor" in result.stdout, (
        "Bookmark 'infra/terraform-refactor' not found in bookmark list"
    )


def test_tracked_bookmark_tracks_origin():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    output = result.stdout
    assert "infra/terraform-refactor" in output, (
        "Bookmark 'infra/terraform-refactor' not found"
    )
    assert "@origin" in output, (
        "No remote tracking found; expected infra/terraform-refactor@origin to be tracked"
    )


def test_backend_tf_file_exists():
    assert os.path.isfile(BACKEND_TF), (
        f"File {BACKEND_TF} does not exist"
    )


def test_backend_tf_content_bucket():
    with open(BACKEND_TF, "r") as f:
        content = f.read()
    assert 'bucket = "platform-tf-state"' in content, (
        "backend.tf missing bucket setting"
    )


def test_backend_tf_content_key():
    with open(BACKEND_TF, "r") as f:
        content = f.read()
    assert 'key    = "infra/terraform.tfstate"' in content, (
        "backend.tf missing key setting"
    )


def test_backend_tf_content_region():
    with open(BACKEND_TF, "r") as f:
        content = f.read()
    assert 'region = "us-west-2"' in content, (
        "backend.tf missing region setting"
    )


def test_commit_with_description_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-r", 'description("infra: add terraform s3 backend configuration")',
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log failed: {result.stderr}"
    )
    assert len(result.stdout.strip()) > 0, (
        "No commit found with description 'infra: add terraform s3 backend configuration'"
    )


def test_jj_status_exits_zero():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed with code {result.returncode}: {result.stderr}"
