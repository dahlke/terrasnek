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
`terrasnek` has been tested against TFE `v202002-2 (419)` and is subject to this
[stability policy](https://www.terraform.io/docs/cloud/api/stability-policy.html).

_Note: Terraform Enterprise is the self-hosted distribution of Terraform Cloud.
It offers enterprises a private instance of the Terraform Cloud application,
with no resource limits and with additional enterprise-grade architectural
features like audit logging and SAML single sign-on._

### Requirements

To make full usage of all the tools and commands here, you should have installed:

- `ag`
- [`coverage`](https://coverage.readthedocs.io/en/coverage-5.1/)
- `make`
- [`pylint`](https://www.pylint.org/)
- `python3`

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

### `terrasnek` to Terraform Cloud API Spec Parity
To see the feature parity between the Terraform Cloud API spec and the available methods in
`terrasnek`, view the auto-generated [`API_COMPARISON.md`](API_COMPARISON.md) file.

### `terrasnek` Common Use Case Examples
See the [`terrasnek` documentation](https://terrasnek.readthedocs.io/en/latest/).

### Contributing to `terrasnek`

If you'd like to contribute to `terrasnek`, review [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

_Note: This repo is not officially maintained by HashiCorp._