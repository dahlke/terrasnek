# `terrasnek` Documentation


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
api = TFC(TFC_TOKEN, url=TFC_URL)
api.set_org("YOUR_ORGANIZATION")
```

Insecure:

```
api = TFC(TFC_TOKEN, url=TFC_URL, verify=False)
api.set_org("YOUR_ORGANIZATION")
```

Contents
--------

* [Account](account.md)
* [Applies](applies.md)
* [Configuration Versions](config_versions.md)
* [Cost Estimates](cost_estimates.md)
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
* [Variables](variables.md)
* [Workspaces](workspaces.md)