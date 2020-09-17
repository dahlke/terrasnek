# `terrasnek` Documentation

_[GitHub Repository](https://github.com/dahlke/terrasnek)_

### Installation

```
pip install terrasnek
```

### Getting Started

Recommended Env Var Usage:

```
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io
```

Using TLS:

```
from terrasnek.api import TFC

api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org("YOUR_ORGANIZATION")
```

Insecure:

```
from terrasnek.api import TFC

api = TFC(TFC_TOKEN, url=TFC_URL, verify=False)
api.set_org("YOUR_ORGANIZATION")
```

### Examples

#### Configure the API Class
```
import os
from terrasnek.api import TFC

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io

api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org("YOUR_ORGANIZATION")
```

#### Create a Workspace
```
create_workspace_payload = {
    # https://www.terraform.io/docs/cloud/api/workspaces.html#sample-payload
}

created_workspace = api.workspaces.create(create_workspace_payload)
created_workspace_id = created_workspace["data]["id"]
```

#### Add Variables to a Workspace
```
create_variable_payload = {
    # https://www.terraform.io/docs/cloud/api/variables.html#sample-payload
}

api.vars.create(create_variable_payload)
```

#### Create a Run on a Workspace
```
create_run_payload = {
    # https://www.terraform.io/docs/cloud/api/run.html#sample-payload
}

run = api.runs.create(create_run_payload)
run_id = self._run["data"]["id"]
```

#### Override a Failed Policy Check
```
pol_checks = api.pol_checks.list(run_id)
api.pol_checks.override(pol_checks["data"][0]["id"])
```

#### Apply a Run on a Workspace
```
applied_run = api.runs.apply(run_id)
```

_For more examples, see the `./test` directory in the repository._


### `terrasnek` to Terraform Cloud API Parity

```eval_rst
.. include:: api_parity_table.rst
```

Contents
--------

* [Account](account.md)
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
* [Workspace Variables](workspace_vars.md)
* [Workspaces](workspaces.md)