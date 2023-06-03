# terrasnek

[![GitHub Actions](https://github.com/dahlke/terrasnek/actions/workflows/main.yml/badge.svg)](https://github.com/dahlke/terrasnek/actions)
[![codecov](https://codecov.io/gh/dahlke/terrasnek/branch/main/graph/badge.svg)](https://codecov.io/gh/dahlke/terrasnek)
[![PyPI version](https://badge.fury.io/py/terrasnek.svg)](https://badge.fury.io/py/terrasnek)
[![Documentation Status](https://readthedocs.org/projects/terrasnek/badge/)](https://terrasnek.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/issues)
[![GitHub license](https://img.shields.io/github/license/dahlke/terrasnek.svg)](https://github.com/dahlke/terrasnek/blob/main/LICENSE)
[![API Method Support](./api_endpoints_implemented.svg)](./TERRASNEK_API_COVERAGE_COMPLETENESS.md)

_A Python Client for the [Terraform Cloud API](https://www.terraform.io/docs/cloud/api/index.html)._

---

![terrasnek logo](/img/tsnk1_md.png)


## Overview

The goal of this project is to support all endpoints available in the
[Terraform Cloud API](https://developer.hashicorp.com/terraform/cloud-docs/api-docs)
and [Terraform Enterprise](https://www.terraform.io/docs/enterprise/index.html) API.
In general, `terrasnek` is developed against the Terraform Cloud APIs first (as
most features are released there first and may not be available in Terraform
Enterprise), but all endpoints are loved equally and this project intends to
support both types of users.

_Note: This project is tested against Terraform Enterprise often, but the code coverage
represented in this repo will always represent coverage against Terraform Cloud
Business Tier (skipping all `admin` modules), so the coverage percentage
is higher than represented in the badge._

**[Terraform Enterprise Release Notes](https://github.com/hashicorp/terraform-enterprise-release-notes)**
**[Terraform Cloud API Changelog](https://www.terraform.io/docs/cloud/api/changelog.html)**

_Note: Terraform Enterprise is the self-hosted distribution of Terraform Cloud.
It offers enterprises a private instance of the Terraform Cloud application,
with no resource limits and with additional enterprise-grade architectural
features like audit logging and SAML single sign-on._

### Using `terrasnek`

For more details on using each endpoint, check out the
[docs](https://terrasnek.readthedocs.io/en/latest/) or the [`test`](./test)
directory.

```python3
from terrasnek.api import TFC
import os

TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)  # ex: https://app.terraform.io
# set to True if you want to use HTTP or insecure HTTPS
SSL_VERIFY = os.getenv("SSL_VERIFY", False)

if __name__ == "__main__":
    api = TFC(TFC_TOKEN, url=TFC_URL, verify=SSL_VERIFY)
    api.set_org("YOUR_ORGANIZATION")
```

### `terrasnek` to Terraform Cloud API Spec Completeness

To compare `terrasnek` implemented endpoints to those listed on the Terraform
 Cloud API docs, view the auto-generated
[`TERRASNEK_API_COVERAGE_COMPLETENESS.md`](TERRASNEK_API_COVERAGE_COMPLETENESS.md)
file. The goal is to always have over 95% of all published endpoints implemented
at any time.

### `terrasnek` Common Use Case Examples

See the [`terrasnek` docs](https://terrasnek.readthedocs.io/en/latest/). You
can download the docs as a PDF directly from `readthedocs.io`.

### Contributing to `terrasnek`

If you'd like to contribute to `terrasnek`, review [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Relevant Blogs
- [Migrating a Lot of State with Python and the Terraform Cloud API](https://medium.com/hashicorp-engineering/migrating-a-lot-of-state-with-python-and-the-terraform-cloud-api-997ec798cd11)
- [The Power of the Terraform API: How to Easily Migrate Any Data Between Enterprise and Cloud ](https://medium.com/hashicorp-engineering/the-power-of-the-terraform-api-how-to-easily-migrate-any-data-between-enterprise-and-cloud-596e7023eb7f)

---

_Note: This repo is not officially maintained by HashiCorp._
