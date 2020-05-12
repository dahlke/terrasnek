# terrasnek

[![CircleCI](https://circleci.com/gh/dahlke/terrasnek.svg?style=svg)](https://circleci.com/gh/dahlke/terrasnek)
[![codecov](https://codecov.io/gh/dahlke/terrasnek/branch/master/graph/badge.svg)](https://codecov.io/gh/dahlke/terrasnek)
[![PyPI version](https://badge.fury.io/py/terrasnek.svg)](https://badge.fury.io/py/terrasnek)
[![Documentation Status](https://readthedocs.org/projects/terrasnek/badge/)](https://terrasnek.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/issues)
[![GitHub license](https://img.shields.io/github/license/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/blob/master/LICENSE)

_A Python Client for the [Terraform Cloud API](https://www.terraform.io/docs/cloud/api/index.html)._

---

### Overview
The goal of this project is to support all endpoints available in the Terraform
Cloud API. It's possible that some of these endpoints won't work if you're
working against an older version of
[Terraform Enterprise](https://www.terraform.io/docs/enterprise/index.html).
This has been tested against TFE `v202002-2 (419)`.

_Note: Terraform Enterprise is the self-hosted distribution of Terraform Cloud.
It offers enterprises a private instance of the Terraform Cloud application,
with no resource limits and with additional enterprise-grade architectural
features like audit logging and SAML single sign-on._

### Requirements

To make full usage of all the tools and commands here, you should have installed:

- `python3`
- `make`
- `pylint`
- `coverage`
- `ag`

All Python requirements are outlined in `pip-reqs.txt`.

### Using `terrasnek`

For more details on using each endpoint, check out the
[docs](https://terrasnek.readthedocs.io/en/latest/) or the [`test`](./test)
directory. I also wrote a [blog post](https://medium.com/hashicorp-engineering/migrating-a-lot-of-state-with-python-and-the-terraform-cloud-api-997ec798cd11)
showing how this library can be used.

```
from terrasnek.api import TFC
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io
SSL_VERIFY = os.getenv("SSL_VERIFY", None)  # set to True if you want to use HTTP or insecure HTTPS

if __name__ == "__main__":
    api = TFC(TFC_TOKEN, url=TFC_URL, ssl_verify=SSL_VERIFY)
    api.set_org("YOUR_ORGANIZATION")
```

##### Endpoints
<details>
  <summary>Supported Endpoints</summary>

    * [Account](https://www.terraform.io/docs/cloud/api/account.html)
    * [Applies](https://www.terraform.io/docs/cloud/api/applies.html)
    * [Configuration Versions](https://www.terraform.io/docs/cloud/api/configuration-versions.html)
    * [Cost Estimates](https://www.terraform.io/docs/cloud/api/cost-estimates.html)
    * [Notification Configurations](https://www.terraform.io/docs/cloud/api/notification-configurations.html)
    * [OAuth Clients](https://www.terraform.io/docs/cloud/api/oauth-clients.html)
    * [OAuth Tokens](https://www.terraform.io/docs/cloud/api/oauth-tokens.html)
    * [Orgs](https://www.terraform.io/docs/cloud/api/organizations.html)
    * [Org Memberships](https://www.terraform.io/docs/cloud/api/organization-memberships.html)
    * [Org Tokens](https://www.terraform.io/docs/cloud/api/organization-tokens.html)
    * [Plan Exports](https://www.terraform.io/docs/cloud/api/plan-exports.html)
    * [Plans](https://www.terraform.io/docs/cloud/api/plans.html)
    * [Policies](https://www.terraform.io/docs/cloud/api/policies.html)
    * [Policy Sets](https://www.terraform.io/docs/cloud/api/policy-sets.html)
    * [Policy Set Parameters](http://www.terraform.io/docs/cloud/api/policy-set-params.html)
    * [Runs](https://www.terraform.io/docs/cloud/api/run.html)
    * [Run Triggers](https://www.terraform.io/docs/cloud/api/run-triggers.html)
    * [SSH Keys](https://www.terraform.io/docs/cloud/api/ssh-keys.html)
    * [State Versions](https://www.terraform.io/docs/cloud/api/state-versions.html)
    * [State Version Outputs](https://www.terraform.io/docs/cloud/api/state-version-outputs.html)
    * [Team Access](https://www.terraform.io/docs/cloud/api/team-access.html)
    * [Team Memberships](https://www.terraform.io/docs/cloud/api/team-members.html)
    * [Team Tokens](https://www.terraform.io/docs/cloud/api/team-tokens.html)
    * [Teams](https://www.terraform.io/docs/cloud/api/teams.html)
    * [User Tokens](https://www.terraform.io/docs/cloud/api/user-tokens.html)
    * [Users](https://www.terraform.io/docs/cloud/api/users.html)
    * [Variables](https://www.terraform.io/docs/cloud/api/variables.html)
    * [Workspaces](https://www.terraform.io/docs/cloud/api/workspaces.html)
    * [Admin Orgs](https://www.terraform.io/docs/cloud/api/admin/organizations.html)
    * [Admin Runs](https://www.terraform.io/docs/cloud/api/admin/runs.html)
    * [Admin Settings](https://www.terraform.io/docs/cloud/api/admin/settings.html)
    * [Admin Terraform Versions](https://www.terraform.io/docs/cloud/api/admin/terraform-versions.html)
    * [Admin Users](https://www.terraform.io/docs/cloud/api/admin/users.html)
    * [Admin Workspaces](https://www.terraform.io/docs/cloud/api/admin/workspaces.html)
</details>

<details>
  <summary>Unsupported Endpoints</summary>

    * [ ] [Policy Checks](https://www.terraform.io/docs/cloud/api/policy-checks.html)
    * [ ] [Registry Modules](https://www.terraform.io/docs/cloud/api/modules.html)
</details>


### Contributing to `terrasnek`

If you'd like to contribute to `terrasnek`, review [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

_Note: This repo is not officially maintained by HashiCorp._