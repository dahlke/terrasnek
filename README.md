# terrasnek

[![CircleCI](https://circleci.com/gh/dahlke/terrasnek.svg?style=svg)](https://circleci.com/gh/dahlke/terrasnek)
[![codecov](https://codecov.io/gh/dahlke/terrasnek/branch/master/graph/badge.svg)](https://codecov.io/gh/dahlke/terrasnek)
[![PyPI version](https://badge.fury.io/py/terrasnek.svg)](https://badge.fury.io/py/terrasnek)
[![Documentation Status](https://readthedocs.org/projects/terrasnek/badge/)](https://terrasnek.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/issues)
[![GitHub license](https://img.shields.io/github/license/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/blob/master/LICENSE)
[![API Method Support](./api_endpoints_implemented.svg)](./API_PARITY_TABLE.md)

_A Python Client for the [Terraform Cloud API](https://www.terraform.io/docs/cloud/api/index.html)._

---

## Overview

The goal of this project is to support all endpoints available in the Terraform
Cloud API. It's possible that some of these endpoints won't work if you're
working against an older version of
[Terraform Enterprise](https://www.terraform.io/docs/enterprise/index.html).

_Note: This project is tested against Terraform Enterprise often, but the code coverage
represented in this repo will always represent coverage against Terraform Cloud
Business Tier (skipping all `admin_` modules), so the coverage percentage
is higher than represented in the badge._

**[Terraform Enterprise Release Notes](https://github.com/hashicorp/terraform-enterprise-release-notes)**
**_This repo has been updated as of TFE version 202007-2._**

_Note: Terraform Enterprise is the self-hosted distribution of Terraform Cloud.
It offers enterprises a private instance of the Terraform Cloud application,
with no resource limits and with additional enterprise-grade architectural
features like audit logging and SAML single sign-on._

### Using `terrasnek`

For more details on using each endpoint, check out the
[docs](https://terrasnek.readthedocs.io/en/latest/) or the [`test`](./test)
directory. I also wrote a
[blog post](https://medium.com/hashicorp-engineering/migrating-a-lot-of-state-with-python-and-the-terraform-cloud-api-997ec798cd11)
showing how this library can be used.

```python3
from terrasnek.api import TFC
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io
# set to True if you want to use HTTP or insecure HTTPS
SSL_VERIFY = os.getenv("SSL_VERIFY", None)

if __name__ == "__main__":
    api = TFC(TFC_TOKEN, url=TFC_URL, ssl_verify=SSL_VERIFY)
    api.set_org("YOUR_ORGANIZATION")
```

### `terrasnek` to Terraform Cloud API Spec Parity

To see the which endpoints are implemented in `terrasnek` compared to those
that are listed on the Terraform Cloud API docs, view the auto-generated
[`API_PARITY_TABLE.md`](API_PARITY_TABLE.md) file.

### `terrasnek` Common Use Case Examples

See the [`terrasnek` documentation](https://terrasnek.readthedocs.io/en/latest/).

### Contributing to `terrasnek`

If you'd like to contribute to `terrasnek`, review [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

_Note: This repo is not officially maintained by HashiCorp._
