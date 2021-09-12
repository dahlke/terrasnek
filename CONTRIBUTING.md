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

Each endpoint must have it's own implementation file, it's own test file, and
corresponding doc file. The docstring must also contain the sample payloads,
target URLs, etc. that are present in all other functions currently. These help
the users, and are used in automation to find missing functionality in
`terrasnek`. More detailed instructions below.

### Adding New Endpoints Details

- Each endpoint must have its own implementation file.
  - The endpoint file should be in the `./terrasnek/` directory with the format `<endpoint_name>.py`.
  - The docstrings for each function in the endpoint must follow the [docstring standard](TODO).
- Update the API class
  - Add an `import` for the new endpoint class.
  - Add the imported class to the right org requirement in `_class_for_attr_dict`.
  - Define the new API class property for the new endpoint class in `__init__`
- Create an test file in the `./test/` directory with the format `<endpoint_name>_test.py`.
  - Test every endpoint that is implemented.
  - Be sure to clean up all resources in the event of failure (`base.py` / `purge_organization`).
  - Make sure the tests do not fail.
- Update the docs to pick up the new class.
  - Create a new file in `./docs` with the format `<endpoint_name>.rst`.
  - Add the new endpoint name to `api.rst` in alphabetical order.

### `terrasnek` Docstring Standard Details

### Other Details

- The Python code (implementation and test) must be linted.
- All Markdown edits _should_ be linted
([markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
[rules](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)).
- The documentation must be rebuilt with any changes you added.
- Before merging to master, it must run the full test suite and generate test
coverage, and all tests must pass.
- The test coverage must be uploaded to CodeCov.

The instructions for doing each of these can be found below.

### Quick Contributions

If you are already familiar with the below processes, and you want to execute
them quickly, use the below. If you are not familiar, this will break and you
will not be able to release.

```bash
source test/secrets/secrets.op.sh
```

If testing against TFE, override some of the defaults in that file for TFE.

```bash
source test/secrets/secrets.op.sh
source test/secrets/secrets.tfe.sh
```

Then run the required processes..

```bash
make pre_release
make release_check
make release
```

### Linting the Library Code

```bash
make lint
```

### Comparing Completeness of `terrasnek` vs Terraform API Spec

This command will generate a markdown table that represents the delta between
what is published Terraform Cloud API Spec and what is implemented in
`terrasnek`. Useful for keeping us honest on it's parity with reality.

```bash
make api_comparison
```

### Building the Docs

The docs are built using [Sphinx](https://www.sphinx-doc.org/en/master/). They
are built upon push by CircleCI, but can be built at any time manually using:

```bash
make docs
```

### Testing

Testing `terrasnek` is a little tricky since Terraform Cloud and Terraform
Enterprise _do_ have some differences in the endpoints they support. This
library is most commonly run against Terraform Cloud, but it is also tested
against Terraform Enterprise often (about once a month, manually). As such,
all published code coverage represents the Terraform Cloud code coverage.

Since this library serves a small number of users, and smaller number of
contributors, for the time being I (@dahlke) will handle unit testing any
changes that are submitted to the project from the community. If the project
grows, we'll consider a more streamlined process for others to test. If you
_want_ to run tests, see `test/secrets/secrets.example.sh` to understand all
the environment variables you will need to consider. You will need to use a
privileged [User Token](https://www.terraform.io/docs/cloud/users-teams-organizations/api-tokens.html#user-api-tokens)
for everything to work as expected. If you have any trouble just drop me
(@dahlke) a line.

_NOTE: If you are running against a Terraform Enterprise instance, be sure to
have enabled Cost Estimates as well a create a user that can be used
for team and organization memberships tests, a this cannot be done
from the API currently. That user's username and email must match those
provided in your `secrets.sh` file._

#### Building Test Data

```bash
cd test/testdata/terraform/
tar -zcvf terrasnek_unittest_config_version.tar.gz src/*
tar -zcvf terrasnek_unittest_module.tar.gz src/*
```

#### Getting Secrets

There is an example secret files at `test/secrets/secrets.example.sh`. You can view that and
manually plug in the values that they need.  I (@eklhad) like to use the
[1password CLI](https://1password.com/downloads/command-line/) to populate mine like below.

```bash
source test/secrets/secrets.op.sh
```

If testing against TFE, override some of the defaults in that file for TFE.

```bash
source test/secrets/secrets.op.sh
source test/secrets/secrets.tfe.sh
```

#### Running Specific Tests

The test suite takes a long time to execute fully, since there is a lot of async
work, and waiting for plans, applies, etc. In the scenario you want to just test
a new implementation or change, use something like the below. You can replace
`test/orgs_test.py` with the test you want to run.

```bash
source test/secrets/secrets.sh
python3 -m unittest test/orgs_test.py
```

_NOTE: Be sure to override the environment variables for TFE if required._

#### Running the Full Test Suite

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
make coverage
```

_NOTE: Be sure to override the environment variables for TFE if required._

#### Uploading Code Coverage

Once the tests have completed and there are *zero* errors, it's safe for us to
upload the code coverage to `codecov.io`. If the tests fail, don't upload the
results, as it's non-representative of the release since there will be no
release with errors in the test suite.

```bash
export CODECOV_TOKEN="<TOKEN>"
make codecov
```

### Releasing a new version of `terrasnek`

Before publishing a new version, all of the previous steps must be executed.
Only then, update [`CHANGELOG.md`](./CHANGELOG.md), [`setup.py`](./setup.py)
[`terrasnek/_constants.py`](./terrasnek/_constants.py), and
[`docs/conf.py`](./docs/conf.py) for the new release version. Then package
it up for PyPi, Publish to PyPi, upload the code coverage results and tag a
release in GitHub.

#### Running the Release Check to Verify Quality

After completing all of the above steps, the release check should be run to
make sure the library is within acceptable parameters of quality. The release
check will confirm that the project is linted (enough), passes (enough) tests,
has all the relevant files updated for the correct version (`./CHANGELOG.md`,
`./setup.py`, `./docs/conf.py`) and that the version being released is greater
than any existing published versions.

```bash
make release_check
```

#### Releasing a New Version

If the release check is passed, the library is good to publish a new version.
Since I (@dahlke) currently own this repo in PyPi, you will not have to deal
with this for the time being.

```bash
make release
```

#### Releasing a New Version to PyPi Test Instance

```bash
make pip-test-publish
```

### Final Notes

Once a new version has been deployed to PyPi, make sure to tag a release in
GitHub to match the newly published version so `readthedocs` can pick up
versions of the documentation.

Thank you for your help or just for using `terrasnek`.

## Addendum

### Setting up TFE for testing

When running the full test suite against a TFE installation, there are several
steps that must be executed ahead of time. With a fresh TFE installation, the
steps when presented with the install UI are:

- Set hostname
- Upload cert and key
- Upload license
- Choose online
- Set admin password
- Confirm pre-flight checks
- Choose demo mode, add an encryption password
- Create a user
- Create an org
- Get a user token
- Get an org token
- Create a user to invite in the tests that matches `secrets.tfe.op.sh`
- Update secrets.tfe.sh
- Run the tests
