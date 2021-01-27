# Contributing to `terrasnek`

## Requirements

To make full usage of all the tools and commands here, you should have installed:

- [`python3`](https://www.python.org/downloads/)
- [`ag`](https://github.com/ggreer/the_silver_searcher)
- [`coverage`](https://coverage.readthedocs.io/en/coverage-5.1/)
- [`make`](https://www.man7.org/linux/man-pages/man1/make.1.html)
- [`pylint`](https://www.pylint.org/)
- [`circleci`](https://circleci.com/docs/2.0/local-cli/#installation)

All Python requirements are outlined in `pip-reqs.txt`.

## Overview

Before contributing to `terrasnek` or publishing to PyPi, there are a few must-dos.

- Each endpoint must have it's own implementation file, it's own test file, and
corresponding doc file.
- The Python code (implementation and test) must be linted.
- All Markdown edits _should_ be linted
([markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
[rules](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)).
- The documentation must be rebuilt with any changes you added.
- Before merging to master, it must run the full test suite and generate test
coverage, and all tests must pass.
- The test coverage must be uploaded to CodeCov.

View the auto-generated
[`CONTRIBUTING_REQS_TABLE.md`](CONTRIBUTING_REQS_TABLE.md) file.

The instructions for doing each of these can be found below. This process is not
automated for now due to some of the limitations of the free Terraform Cloud
offering. In the future, if some of the limitations are lifted, these checks
will be automated in CircleCI.

Here is a summary of the commands:

```bash
make lint
make api_comparison
make docs
make coverage # the results of this depend on the endpoint you hit.
make contributor_check
```

Before merging to master and publishing a new version, update [`CHANGELOG.md`](./CHANGELOG.md),
[`setup.py`](./setup.py) and [`docs/conf.py`](./docs/conf.py) for the new release
version. Merge the changes to the master branch, then publish.

```bash
make pip-package
make pip-publish
make codecov
```

Once a new version has been deployed to PyPi, make sure to tag a release in
GitHub to match the newly published version so `readthedocs` can pick up
versions of the documentation.

### Helpful Git Hooks

There are some pre-commit hooks that are useful since the same tests will be run
in CircleCI. They are located in the `./hooks/pre-commit/` folder here. Symlink
them to the git repo using:

```bash
cd .git/hooks
ln -s -f ../../hooks/pre-commit ./pre-commit
chmod +x ../../hooks/pre-commit ./pre-commit
```

### Linting the Code

#### Lint Library Code

```bash
make lint
```

### Building the Docs

The docs are built using [Sphinx](https://www.sphinx-doc.org/en/master/). They
are built upon push by CircleCI, but can be built at any time manually using:

```bash
make docs
```

### Testing

It is recommended that when running the entire suite of tests, you use a
sandbox Terraform Enterprise instance. This will allow you to test the
Admin Endpoints without any worry of error, and you will not have any
run limits. It is currently required that you run the entire test suite
with a [User Token](https://www.terraform.io/docs/cloud/users-teams-organizations/api-tokens.html#user-api-tokens)
of an admin user, in order to fully test all the endpoints. You can run
the test suite against Terraform Cloud, but tests will be skipped.

Due to those limitations, this library does not currently test the full
suite of tests in CircleCI. It is recommended that you run the tests
locally before submitting pull requests, or at the very least, verify
all of the tests that touch code you are contributing.

If you are running against a Terraform Enterprise instance, be sure to
have enabled Cost Estimates as well a create a user that can be used
for team and organization memberships tests, a this cannot be done
from the API currently. That user's username and email must match those
provided in your `secrets.sh` file.

#### Building Test Data

```bash
cd test/testdata/terraform/
tar -zcvf terrasnek_unittest_config_version.tar.gz src/*
tar -zcvf terrasnek_unittest_module.tar.gz src/*
```

#### Running Specific Tests

The test suite takes a long time to execute fully, since there is a lot of async
work, and waiting for plans, applies, etc. In the scenario you want to just test
a new implementation or change, use the below.

```bash
source test/secrets/secrets.sh
python3 -m unittest test/orgs_test.py
```

#### Running All Tests

_Note: When you run all of the tests, you will have to create a user (that
matches your `TEST_USER` in `secrets.sh`) manually ahead of executing the tests
if you don't have an existing user in the system already. Currently not possible
to create users with the API, and some of the tests involve adding a user to
teams and organizations. Not all endpoints are available in the free Terraform Cloud
offering. In order for you to test or use all of the endpoints, you'll need
the proper packages for Terraform Cloud or your own private Terraform
Enterprise instance._

```bash
source test/secrets/secrets.sh
make test
```

#### Running the Tests with Coverage Info

```bash
source test/secrets/secrets.sh
make coverage
```

#### Uploading Coverage Stats to CodeCov.io

```bash
export CODECOV_TOKEN="<TOKEN>"
bash <(curl -s https://codecov.io/bash)
```

#### Building the Documentation

```bash
make docs
```

#### Comparing Completeness of `terrasnek` vs Terraform API Spec

```bash
make api_comparison
```

#### Publishing to PyPi

##### Production

```bash
make pip-publish
```

##### Test

```bash
make pip-test-publish
```
