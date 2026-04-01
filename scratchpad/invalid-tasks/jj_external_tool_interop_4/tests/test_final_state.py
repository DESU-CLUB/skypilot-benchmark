import os
import subprocess
import json

def test_final_state():
    home = os.environ.get("HOME", "/home/user")
    repo_path = os.path.join(home, "monorepo")
    
    # 1. Repo exists
    assert os.path.exists(repo_path), "Repo must exist"
    assert os.path.exists(os.path.join(repo_path, ".jj")), ".jj directory must exist"
    
    # 2. bookmark tool-integration-ready exists and points to a commit with 2 parents
    # Let's get parents of tool-integration-ready
    try:
        output = subprocess.check_output(
            ["jj", "log", "-r", "tool-integration-ready", "-T", "parents.map(|c| c.commit_id()).join(',')", "--no-graph"],
            cwd=repo_path,
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        assert False, "Failed to get tool-integration-ready bookmark"
    
    parents = [p for p in output.split(',') if p]
    assert len(parents) == 2, f"Commit at tool-integration-ready should have 2 parents, found {len(parents)}"
    
    # 3. tools_config.json contains {"enabled": true, "timeout": 30}
    config_path = os.path.join(repo_path, "tools_config.json")
    assert os.path.exists(config_path), "tools_config.json must exist"
    with open(config_path, "r") as f:
        data = json.load(f)
    assert data.get("enabled") is True, "tools_config.json must have enabled: true"
    assert data.get("timeout") == 30, "tools_config.json must have timeout: 30"
    
    # linter_rules.yaml exists
    linter_path = os.path.join(repo_path, "linter_rules.yaml")
    assert os.path.exists(linter_path), "linter_rules.yaml must exist"
    with open(linter_path, "r") as f:
        linter_data = f.read()
    assert "rules: strict" in linter_data, "linter_rules.yaml must contain rules: strict"
    
    # 4. /home/user/monorepo/jj_op_log_export.txt exists and contains operation log entries
    export_path = os.path.join(repo_path, "jj_op_log_export.txt")
    assert os.path.exists(export_path), "jj_op_log_export.txt must exist"
    with open(export_path, "r") as f:
        export_data = f.read()
    assert len(export_data.strip().split('\n')) >= 3, "jj_op_log_export.txt should contain multiple operation log entries"
    # Check if format looks somewhat correct (short id and description)
    # usually 12 chars hex and some description
    assert any(" " in line for line in export_data.strip().split('\n')), "Export format does not seem to match 'id description'"
