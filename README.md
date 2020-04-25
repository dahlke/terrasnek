# terrasnek

![Python unittest Code Coverage](coverage.svg)

_A Python Client for the [Terraform Cloud API](https://www.terraform.io/docs/cloud/api/index.html)._


### Using `terrasnek`

For more details on using each endpoint, checkout the [`test`](./test) directory.

```
from terrasnek.api import TFC
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)

if __name__ == "__main__":
    api = TFC(TFC_TOKEN)
    api.set_organization("YOUR_ORGANIZATION")
```

#### Contributing to `terrasnek`

Currently the following endpoints are supported:

##### Standard Endpoints
- [ ] [Account](https://www.terraform.io/docs/cloud/api/account.html)
- [x] [Applies](https://www.terraform.io/docs/cloud/api/applies.html)
- [x] [Configuration Versions](https://www.terraform.io/docs/cloud/api/configuration-versions.html)
- [ ] [Cost Estimates](https://www.terraform.io/docs/cloud/api/cost-estimates.html)
- [x] [Notification Configurations](https://www.terraform.io/docs/cloud/api/notification-configurations.html)
- [x] [OAuth Clients](https://www.terraform.io/docs/cloud/api/oauth-clients.html)
- [x] [OAuth Tokens](https://www.terraform.io/docs/cloud/api/oauth-tokens.html)
- [x] [Organizations](https://www.terraform.io/docs/cloud/api/organizations.html)
- [x] [Organization Memberships](https://www.terraform.io/docs/cloud/api/organization-memberships.html)
- [x] [Organization Tokens](https://www.terraform.io/docs/cloud/api/organization-tokens.html)
- [x] [Plan Exports](https://www.terraform.io/docs/cloud/api/plan-exports.html)
- [x] [Plans](https://www.terraform.io/docs/cloud/api/plans.html)
- [x] [Policies](https://www.terraform.io/docs/cloud/api/policies.html)
- [ ] [Policy Checks](https://www.terraform.io/docs/cloud/api/policy-checks.html)
- [x] [Policy Sets](https://www.terraform.io/docs/cloud/api/policy-sets.html)
- [x] [Policy Set Parameters](http://www.terraform.io/docs/cloud/api/policy-set-params.html)
- [ ] [Registry Modules](https://www.terraform.io/docs/cloud/api/modules.html)
- [x] [Runs](https://www.terraform.io/docs/cloud/api/run.html)
- [x] [Run Triggers](https://www.terraform.io/docs/cloud/api/run-triggers.html)
- [x] [SSH Keys](https://www.terraform.io/docs/cloud/api/ssh-keys.html)
- [x] [State Versions](https://www.terraform.io/docs/cloud/api/state-versions.html)
- [x] [State Version Outputs](https://www.terraform.io/docs/cloud/api/state-version-outputs.html)
- [x] [Team Access](https://www.terraform.io/docs/cloud/api/team-access.html)
- [x] [Team Memberships](https://www.terraform.io/docs/cloud/api/team-members.html)
- [x] [Team Tokens](https://www.terraform.io/docs/cloud/api/team-tokens.html)
- [x] [Teams](https://www.terraform.io/docs/cloud/api/teams.html)
- [x] [User Tokens](https://www.terraform.io/docs/cloud/api/user-tokens.html)
- [x] [Users](https://www.terraform.io/docs/cloud/api/users.html)
- [x] [Variables](https://www.terraform.io/docs/cloud/api/variables.html)
- [x] [Workspaces](https://www.terraform.io/docs/cloud/api/workspaces.html)

##### Admin Endpoints
- [x] [Admin Organizations](https://www.terraform.io/docs/cloud/api/admin/organizations.html)
- [ ] [Admin Runs](https://www.terraform.io/docs/cloud/api/admin/runs.html)
- [ ] [Admin Settings](https://www.terraform.io/docs/cloud/api/admin/settings.html)
- [ ] [Admin Terraform Versions](https://www.terraform.io/docs/cloud/api/admin/terraform-versions.html)
- [x] [Admin Users](https://www.terraform.io/docs/cloud/api/admin/users.html)
- [ ] [Admin Workspaces](https://www.terraform.io/docs/cloud/api/admin/workspaces.html)


### Contributing to `terrasnek`

#### Linting the Code

```
make lint
```

#### Building Test Data

```
cd test/testdata/terraform/
tar -zcvf terrasnek_unittest_config_version.tar.gz src/*
```

#### Running Specific Tests

The test suite takes a long time to execute fully, since there is a lot of async work, and waiting
for plans, applies, etc. In the scenario you want to just test a new implementation or change,
use the below.

```
source test/secrets/secrets.sh
python3 -m unittest test/applies_test.py
```

#### Running All Tests

```
source test/secrets/secrets.sh
make coverage
```

#### Running the Tests with Coverage Info

```
source test/secrets/secrets.sh
make coverage
```

#### Publishing to PyPi

```
make pip-package
make pip-publish
```

---

_Note: This repo is not officially maintained by HashiCorp._