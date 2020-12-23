# `terrasnek` Documentation

_[GitHub Repository](https://github.com/dahlke/terrasnek)_

## Installation

```bash
pip install terrasnek
```

## Getting Started

Recommended Env Var Usage:

```python
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io
```

Using TLS:

```python
from terrasnek.api import TFC

api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org("YOUR_ORGANIZATION")
```

Insecure:

```python
from terrasnek.api import TFC

api = TFC(TFC_TOKEN, url=TFC_URL, verify=False)
api.set_org("YOUR_ORGANIZATION")
```

### Examples

_NOTE: Every endpoint supported in `terrasnek` has an API reference in its docstring_.

#### Configure the API Class

```python
import os
from terrasnek.api import TFC

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io

api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org("YOUR_ORGANIZATION")
```

#### Create a Workspace

```python
create_workspace_payload = {
    # https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload
}

created_workspace = api.workspaces.create(create_workspace_payload)
created_workspace_id = created_workspace["data"]["id"]
```

#### Add Variables to a Workspace [Deprecated]

```python
create_var_payload = {
    # https://www.terraform.io/docs/cloud/api/variables.html#sample-payload
}

api.vars.create(create_var_payload)
```

#### Add Workspace Variables

```python
create_ws_var_payload = {
    # https://www.terraform.io/docs/cloud/api/variables.html#sample-payload
}
workspace_id = "ws-foo"

api.workspace_vars.create(workspace_id, create_ws_var_payload)
```

#### Create a Run on a Workspace

```python
create_run_payload = {
    # https://www.terraform.io/docs/cloud/api/run.html#sample-payload
}

run = api.runs.create(create_run_payload)
run_id = self._run["data"]["id"]
```

#### Override a Failed Policy Check

```python
pol_checks = api.pol_checks.list(run_id)
api.pol_checks.override(pol_checks["data"][0]["id"])
```

#### Apply a Run on a Workspace

```python
applied_run = api.runs.apply(run_id)
```

_For more examples, see the `./test` directory in the repository._

### `terrasnek` to Terraform Cloud API Completeness

```eval_rst
.. include:: TERRASNEK_API_COVERAGE_COMPLETENESS.rst
```

## Contents

* [Account](account.md)
* [Admin Module Sharing](admin_module_sharing.md)
* [Admin Runs](admin_runs.md)
* [Admin Orgs](admin_orgs.md)
* [Admin Users](admin_users.md)
* [Admin Settings](admin_settings.md)
* [Admin Terraform Versions](admin_terraform_versions.md)
* [Admin Workspaces](admin_workspaces.md)
* [Agents](agents.md)
* [Agent Tokens](agent_tokens.md)
* [Applies](applies.md)
* [Audit Trails](audit_trails.md)
* [Config Versions](config_versions.md)
* [Cost Estimates](cost_estimates.md)
* [IP Ranges](ip_ranges.md)
* [Notification Configurations](notification_configs.md)
* [OAuth Clients](oauth_clients.md)
* [OAuth Tokens](oauth_tokens.md)
* [Orgs](orgs.md)
* [Org Memberships](org_memberships.md)
* [Org Tokens](org_tokens.md)
* [Plan Exports](plan_exports.md)
* [Plans](plans.md)
* [Policies](policies.md)
* [Policy Checks](policy_checks.md)
* [Policy Sets](policy_sets.md)
* [Policy Set Params](policy_set_params.md)
* [Registry Modules](registry_modules.md)
* [Runs](runs.md)
* [Run Triggers](run_triggers.md)
* [SSH Keys](ssh_keys.md)
* [State Versions](state_versions.md)
* [State Version Outputs](state_version_outputs.md)
* [Team Access](team_access.md)
* [Team Memberships](team_memberships.md)
* [Team Tokens](team_tokens.md)
* [Teams](teams.md)
* [User Tokens](user_tokens.md)
* [Users](users.md)
* [Vars](vars.md)
* [Workspace Vars](workspace_vars.md)
* [Workspaces](workspaces.md)
