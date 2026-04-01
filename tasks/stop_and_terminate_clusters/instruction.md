You are working in a SkyPilot environment. Your goal is to write a Bash cleanup script at `/home/user/cleanup.sh` that safely stops and then permanently terminates all SkyPilot clusters.

The script must:
1. First **stop** all clusters (gracefully halts them while preserving cloud resources like disks).
2. Then **terminate** (permanently delete) all clusters without requiring interactive confirmation.
3. Be executable (chmod +x).

The script will be run as: `bash /home/user/cleanup.sh`

Constraints:
- Use the `sky` CLI — do not use cloud-provider CLIs directly (no `aws`, `gcloud`, etc.).
- The commands must work non-interactively (no prompts).
- Save the script to exactly `/home/user/cleanup.sh`.
