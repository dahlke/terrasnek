# terrasnek

![Python unittest Code Coverage](coverage.svg)

_A Python Client for the [Terraform Enterprise API](https://www.terraform.io/docs/cloud/api/index.html)._


### Using `terrasnek`

For more details on using each endpoint, checkout the [`test`](./test) directory.

```
from terrasnek.api import TFE
import os

TFE_TOKEN = os.getenv("TFE_TOKEN", None)

if __name__ == "__main__":
    api = TFE(TFE_TOKEN)
    api.set_organization("YOUR_ORGANIZATION")
```

#### Contributing to `terrasnek`

Currently the following endpoints are supported:

- [x] [Accounts](https://www.terraform.io/docs/enterprise/api/account.html)
- [x] [Configuration Versions](https://www.terraform.io/docs/enterprise/api/configuration-versions.html)
- [x] [OAuth Clients](https://www.terraform.io/docs/enterprise/api/oauth-clients.html)
- [x] [OAuth Tokens](https://www.terraform.io/docs/enterprise/api/oauth-tokens.html)
- [x] [Organizations](https://www.terraform.io/docs/enterprise/api/organizations.html)
- [x] [Organization Tokens](https://www.terraform.io/docs/enterprise/api/organization-tokens.html)
- [x] [Policies](https://www.terraform.io/docs/enterprise/api/policies.html)
- [x] [Policy Sets](https://www.terraform.io/docs/enterprise/api/policy-sets.html)
- [x] [Policy Checks](https://www.terraform.io/docs/enterprise/api/policy-checks.html)
- [ ] [Registry Modules](https://www.terraform.io/docs/enterprise/api/modules.html)
- [x] [Runs](https://www.terraform.io/docs/enterprise/api/run.html)
- [x] [SSH Keys](https://www.terraform.io/docs/enterprise/api/ssh-keys.html)
- [x] [State Versions](https://www.terraform.io/docs/enterprise/api/state-versions.html)
- [x] [Team Access](https://www.terraform.io/docs/enterprise/api/team-access.html)
- [x] [Team Memberships](https://www.terraform.io/docs/enterprise/api/team-members.html)
- [x] [Team Tokens](https://www.terraform.io/docs/enterprise/api/team-tokens.html)
- [x] [Teams](https://www.terraform.io/docs/enterprise/api/teams.html)
- [x] [Variables](https://www.terraform.io/docs/enterprise/api/variables.html)
- [x] [Workspaces](https://www.terraform.io/docs/enterprise/api/workspaces.html)
- [ ] [Admin](https://www.terraform.io/docs/enterprise/api/admin/index.html)



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

#### Running the Tests with Coverage Info

```
source test/secrets/secrets.sh
make coverage
```