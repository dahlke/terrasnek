# Contributing to `terrasnek`

Before contributing to `terrasnek` or publishing to PyPi, there are a few must-dos.

- Each endpoint must have it's own implementation file, it's own test file, and corresponding doc file.
- The Python code (implementation and test) must be linted.
- The documentation must be rebuilt with any changes you added.
- Before merging to master, it must run the full test suite and generate test coverage, and all tests must pass.
- The test coverage must be uploaded to CodeCov.


The instructions for doing each of these can be found below. This process is not automated
for now due to some of the limitations of the free Terraform Cloud offering. In the
future, if some of the limitations are lifted, these checks will be automated in CircleCI.

Here is a summary of the commands:

```
make lint-lib
make lint-tests
make docs
make coverage
make codecov
make pip-publish
```

#### Linting the Code

###### Lint Library Code
```
make lint-lib
```

###### Lint Test Code
```
make lint-tests
```

#### Building Test Data

```
cd test/testdata/terraform/
tar -zcvf terrasnek_unittest_config_version.tar.gz src/*
```

#### Testing

It is recommended that when running the entire suite of tests, you use a
sandbox Terraform Enterprise instance. This will allow you to test the
Admin Endpoints without any worry of error, and you will not have any
run limits.

Due to those limitations, this library does not currently test the full
suite of tests in CircleCI. It is recommended that you run the tests
locally before submitting pull requests, or at the very least, verify
all of the tests that touch code you are contributing.

If you are running against a Terraform Enterprise instance, be sure to
have enabled Cost Estimates as well a create a user that can be used
for team and organization memberships tests, a this cannot be done
from the API currently. That user's username and email must match those
provided in your `secrets.sh` file.

###### Running Specific Tests

The test suite takes a long time to execute fully, since there is a lot of async work, and waiting
for plans, applies, etc. In the scenario you want to just test a new implementation or change,
use the below.

```
source test/secrets/secrets.sh
python3 -m unittest test/applies_test.py
```

###### Running All Tests

_Note: When you run all of the tests, you will have to create a user (that
matches your `TEST_USER` in `secrets.sh`) manually ahead of executing the tests
if you don't have an existing user in the system already. Currently not possible
to create users with the API, and some of the tests involve adding a user to
teams and organizations. Not all endpoints are available in the free Terraform Cloud
offering. In order for you to test or use all of the endpoints, you'll need
the proper packages for Terraform Cloud or your own private Terraform
Enterprise instance._

```
source test/secrets/secrets.sh
make test
```

###### Running the Tests with Coverage Info

```
source test/secrets/secrets.sh
make coverage
```

###### Uploading Coverage Stats to CodeCov.io
```
export CODECOV_TOKEN="<TOKEN>"
bash <(curl -s https://codecov.io/bash)
```

#### Building the Documentation
```
make docs
```

#### Publishing to PyPi

###### Production
```
make pip-publish
```

###### Test

```
make pip-test-publish
```
