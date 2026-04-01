You are working in a SkyPilot environment. Write a SkyPilot task YAML at `/home/user/private_train.yaml` that runs a training job requiring a **private GitHub repository** as a dependency.

The job requirements:

1. **Job name**: `private-train`
2. **Compute**: 2 CPUs (no GPU needed).
3. **Secret handling**: The job uses a GitHub personal access token stored in an environment variable called `GIT_TOKEN`. The YAML should declare this environment variable with an empty default (it will be supplied at `sky launch` time with `--env GIT_TOKEN=<token>`).
4. **Setup**: The setup script must:
   - Clone the private repository at `github.com/myorg/private-training-lib` using the `GIT_TOKEN` for authentication (via HTTPS with OAuth2 token pattern).
   - Install the cloned repository as a Python package (editable install using `pip install -e .`).
5. **Run**: Execute `python train.py`.

Save the configuration to `/home/user/private_train.yaml`. The file must be valid YAML.
