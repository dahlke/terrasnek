# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.10] - 2022-04-13

- Implemented the new Config Version endpoints
- Implemented the new State Version endpoints
- Implemented the Comments endpoints
- Implemented the Workspace Resources endpoints
- Implemented the new Run Task Integration endpoints
- Fixed the docstring in `var_sets`
- Added a `search` parameter to the Workspaces `list_all` method

## [0.1.9] - 2022-02-09

- Linted and tested with coverage against TFC and TFE
- Fixed all the tests that were failing due to bad `DELETE`s
- Added `"search"` parameter to the list workspaces endpoint
- Updated CircleCI image for new API docs parser

## [0.1.8] - 2022-01-01

- Happy New Years!
- New List State Version Outputs Method
- Making tests more reliable
- Clearing out TODOs
- Type checking filters / include parameters (lists)
- Adding documentation for new filter / include behavior
- Forcing endpoint calls to go to the `_destroy` method, not `_delete`
- Fix the registry modules test.
- New API docs parser that uses the GitHub repo Markdown and not the website
- TFE tests passing reliably.
- Fixing an issue in the registry_module_test

## [0.1.7] - 2021-12-02

- Implemented Registry Providers.
- Immplemented Variable Sets.
- Adding a `list_all` helper to Terraform Versions.
- Adding `list_all` to Registry Modules.
- Adding new options to Registry Modules `list` function.
- Updating the Run Tasks code to fit the new URLs (formerly Event Hooks). (BETA)
- Updating docs copy.
- Remove `GITHUB_SECRET` from the requirements for testing.
- Change what gets reported on for code coverage.
- Removing all params from docstrings, they change too much. Instead, relying on sharing the relevant link.
- `api_comparison` properly reports missing docs pages now.
- Clearing out TODOs.

## [0.1.6] - 2021-09-19

- Implemented Run Tasks endpoints
- Clarified CircleCI jobs
- Updated docs on endpoint contribution and testing against TFE
- Added notes on how to download docs as a PDF
- Changed all tests to use constants for page and page sizes
- Added separate coverage files for TFC and TFE

## [0.1.5] - 2021-08-23

- Implemented Workspace State Consumer endpoints
- Implemented new Config Version endpoints
- Implemented new Agent endpoints
- Implemented new Workspace Tag endpoints
- Implemented new Org Tag endpoints
- Added TFC API Changelog link in docs
- Transitioned Registry Modules endpoints to new ones
- Added Better exception handling
- Updated example code in README
- Upgraded CircleCI testing image
- API script now detects deprecated endpoints and treats them as such
- Fixed tests to handle new API behavior

## [0.1.4] - 2021-08-20

- Bad release, skipping to `0.1.5`.

## [0.1.3] - 2021-04-15

- Adding related resources to all endpoints that support them (`include`)
- Create a shared `list_all` function in the endpoint class.
- Adding in all the new module sharing endpoints.
- Update requests to 2.22.0.
- Added VCS Events endpoints.
- Updated contributor docs and tables.
- Updated CircleCI for new contributor requirements.
- Fix some tests that failed intermittently.
- Add Terrasnek version to the API object.
- Cleaned up the information on contributing to `terrasnek`.
- Higher threshold for "incompleteness" in CircleCI to keep up to date.
- Adding a check for staged or modified files to the release check.

## [0.1.2] - 2021-03-16

- Loosen install_requires entry for `requests`.
- Adding an auditable action to the audit trails test.
- Clean up how the base test org is set.
- Make the applies test wait for the apply to actually finish.
- Add cron job to compare endpoint implementations against the API docs nightly.
- Update package makefile logic.
- Make it easier and safer to release versions to PyPi.

## [0.1.1] - 2021-02-09

I started working on this project about a half a year or so ago, and never
thought it would get this far, but it did. This library has been tested in a
bunch of different places, and I feel confident in it going forward, so today
I will move it to `0.1.1`. There is certainly room for improvement (and I'd
like help to do so if you're willing), but I'm confident you can use this
library for it's utility at this stage.

- Cleared out a bunch of TODOs
- Implemented a bunch of TFC specific endpoints (like subscriptions, invoices, etc.)
- New TFCHTTPRequestRateLimit exception
- Tweaks to the documentation to include more of the library
- Added new TFC entitlements
- 196/196 Implemented endpoints at time of release

## [0.0.16] - 2020-12-23

- Adding new Admin Orgs API endpoint.
- Add the new Admin Module Sharing API
- Make it easier to understand when to run things against TFE or TFC.

## [0.0.15] - 2020-12-14

- Implement the get policy text function for the policies api.
- Implement paging for run triggers API.

## [0.0.14] - 2020-12-14

- Adding a list all function to:
  - workspaces
  - audit trails
  - config versions
  - state versions
  - org memberships
  - policies
  - policy sets
  - runs

## [0.0.13] - 2020-12-14

- Merge in the upload TF config version from string.
- Exceptions log to debug, let the app handle logging errors.

## [0.0.12] - 2020-12-02

- Updating some of the organization purge logic before running tests
- Making it easier to retrieve important values from the API class
- Making it easier to retrieve important values from the Endpoint class

## [0.0.11] - 2020-11-23

- More API tests.
- Purging org memberships and agent pools at the start of a test
- Implement new agent pool endpoints
- Add debug logic to all API requests for prod debugging
- Pass error information back up through exceptions

## [0.0.10] - 2020-11-17

- Make required entitlements a private method.
- Adding typing to the API endpoints per `mcandries` request.
- Raise exceptions for non 2XX 3XX HTTP error codes.
- Update the library to throw API exceptions.
- Update all the tests so to work with exceptions thrown>

## [0.0.9] - 2020-10-20

- Updating docstrings across all methods for method use clarity.
- Updating Registry Modules API to support all methods.
- Standardize how payloads are taken by each endpoint.
- More test streamlining.

## [0.0.8] - 2020-09-17

- Adding more information on query parameters for each relevant endpoint.
- Fix a bug in the Team Access API.
- Update the documentation to add the latest endpoints supported.

## [0.0.7] - 2020-08-26

- Added Agents API for Terraform Cloud Business Tier
- Added Agents Tokens API for Terraform Cloud Business Tier
- Added Audit Trails API for Terraform Cloud Business Tier
- Added missing endpoints in Module Registry, Plans, Policy Sets endpoints.

## [0.0.6] - 2020-07-01

- Make sure endpoint docstrings match the API docs path for automated checks
- Implemented APIs: Workspace Variables, Egress IP Ranges
- Added endpoints for Plans API JSON downloads
- Added endpoints for Team Access API statefile access
- Added endpoints for Teams API statefile access
- API method comparison script and output tables
- Markdown linting
- CircleCI testing docker image and script to upload env vars
- Hitting uncovered lines in Plan Exports, OAuth Clients, Registry Modules, Runs.
- Added TFE release notes links to README.
- Added methods implemented badge to README.

## [0.0.5] - 2020-05-22

### Added

- A CHANGELOG. :)
- All existing endpoints as of today are implemented, documented and tested.
