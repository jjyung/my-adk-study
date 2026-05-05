# caveman-agent

Caveman-style text compression agent
Agent generated with `agents-cli` version `0.1.2`

## Project Structure

```
caveman-agent/
├── app/         # Core agent code
│   ├── agent.py               # Main agent logic
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

Install required packages:

```bash
agents-cli install
```

Run a quick compression:

```bash
agents-cli run "Rewrite this in caveman style: <your verbose text>"
```

Or use interactive testing:

```bash
agents-cli playground
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli run "..."` | Run one-shot compression in terminal |
| `agents-cli playground` | Launch local development environment |
| `agents-cli lint`    | Run code quality checks                                                               |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit behavior in `app/agent.py`. The root agent (`caveman_compressor`) is configured to:
- compress verbose input into terse technical text
- preserve facts, commands, paths, and numeric values
- avoid adding new facts

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

### Manual Terraform (Create / Destroy)

If you want to manage infra manually with Terraform (single-project mode):

1) Prepare tfvars from example

```bash
cp deployment/terraform/single-project/vars/env.tfvars.example deployment/terraform/single-project/vars/env.tfvars
```

2) Edit `deployment/terraform/single-project/vars/env.tfvars` and set:
- `project_id`
- `region` (for example `asia-east1`)

3) Create infrastructure

```bash
terraform -chdir=deployment/terraform/single-project init
terraform -chdir=deployment/terraform/single-project plan -var-file=vars/env.tfvars
terraform -chdir=deployment/terraform/single-project apply -var-file=vars/env.tfvars
```

4) Deploy app code to Cloud Run

```bash
agents-cli deploy --project <your-project-id> --region <your-region> --no-confirm-project
```

5) Destroy infrastructure (when done)

```bash
terraform -chdir=deployment/terraform/single-project destroy -var-file=vars/env.tfvars
```

Notes:
- `.tfstate` and `.tfvars` are gitignored to avoid committing local/sensitive Terraform files.
- Keep `*.example` files in git as templates, and use local `env.tfvars` for real values.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.
